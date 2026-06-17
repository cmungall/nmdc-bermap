"""Reverse generator: reconstruct each study's `variables` catalog from its LinkML profile
(schemas/studies/<id>.yaml) + its SSSOM mapping table (schemas/studies/<id>.sssom.yaml).

This is the Source-of-Truth flip: profiles + SSSOM -> variables. Run with `--check` to prove
round-trip identity against the current db/sfas-brcs.yaml (reverse(forward(variables)) == variables).
Run with: just sync-variables [--check]
"""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "db" / "sfas-brcs.yaml"
OUT_STUDIES = ROOT / "schemas" / "studies"
OUT_DATASETS = ROOT / "schemas" / "datasets"
INDEX_PATH = ROOT / "schemas" / "variable-index.yaml"
PROG_KEYS = [
    "bioenergy_research_centers", "genomic_science_sfas", "environmental_system_science_sfas",
    "user_facilities", "ai_projects", "other_programs",
]
ANNOT_FACETS = ("measured_entity", "material_or_matrix", "method",
                "temporal_resolution", "spatial_resolution", "notes")
DEFAULT_PREDICATE = {"mixs": "skos:exactMatch", "bervo": "skos:exactMatch",
                     "unit": "skos:closeMatch", "onto": "skos:relatedMatch"}
SKOS_TO_REL = {"skos:exactMatch": "EXACT_MATCH", "skos:closeMatch": "CLOSE_MATCH",
               "skos:relatedMatch": "RELATED_MATCH", "skos:broadMatch": "BROAD_MATCH",
               "skos:narrowMatch": "NARROW_MATCH"}


def study_id(study: dict) -> str:
    sid = study.get("nmdc_study_id")
    return sid.split(":")[-1] if sid else _slug(study.get("name"))


def dataset_id(dataset: dict) -> str:
    return _slug(dataset.get("name"))


def owners(db: dict):
    """Yield (kind, oid, out_dir, program_id, owner) for every variable-bearing study/dataset."""
    for pk in PROG_KEYS:
        for p in db.get(pk) or []:
            pid = p.get("id")
            for s in p.get("studies") or []:
                if s.get("variables"):
                    yield "study", study_id(s), OUT_STUDIES, pid, s
            for d in p.get("datasets") or []:
                if d.get("variables"):
                    yield "dataset", dataset_id(d), OUT_DATASETS, pid, d


def _slug(name):
    import re
    s = re.sub(r"[^0-9a-zA-Z]+", "_", (name or "").lower())
    return re.sub(r"_+", "_", s).strip("_")


def sssom_by_subject(sssom_path: Path) -> dict:
    out = {}
    if sssom_path.exists():
        for row in (yaml.safe_load(sssom_path.read_text()) or {}).get("mappings") or []:
            out.setdefault(row["subject_id"], []).append(row)
    return out


def reconstruct_variable(sname: str, slot: dict, enums: dict, rows: list) -> dict:
    ann = slot.get("annotations") or {}
    var = {"name": slot.get("title") or sname}
    if slot.get("description"):
        var["description"] = slot["description"]
    if ann.get("role"):
        var["roles"] = ann["role"].split("; ")
    var["value_type"] = ann.get("value_type")

    rng = slot.get("range")
    if rng in enums:
        var["levels"] = list((enums[rng].get("permissible_values") or {}).keys())
    elif ann.get("levels"):
        var["levels"] = ann["levels"].split(" | ")
    if slot.get("unit"):
        var["units"] = slot["unit"]["descriptive_name"]

    # mappings from SSSOM, routed back to source bucket by object CURIE prefix
    mixs, bervo, unit_term, onto = [], None, None, []
    for r in rows:
        prefix = r["object_id"].split(":")[0]
        bucket = {"MIXS": "mixs", "BERVO": "bervo", "UO": "unit"}.get(prefix, "onto")
        obj = {"id": r["object_id"], "label": r["object_label"]}
        pred = r.get("predicate_id")
        if pred and pred != DEFAULT_PREDICATE[bucket]:
            obj["mapping_relation"] = SKOS_TO_REL.get(pred, pred)
        if r.get("comment"):
            obj["mapping_note"] = r["comment"]
        if bucket == "mixs":
            mixs.append(obj)
        elif bucket == "bervo":
            bervo = obj
        elif bucket == "unit":
            unit_term = obj
        else:
            onto.append(obj)
    if bervo:
        var["bervo_term"] = bervo
    if unit_term:
        var["unit_term"] = unit_term
    if mixs:
        var["mixs_terms"] = mixs
    if onto:
        var["ontology_mappings"] = onto

    for facet in ANNOT_FACETS:
        if ann.get(facet):
            var[facet] = ann[facet]
    if ann.get("time_series") == "true":
        var["time_series"] = True
    if slot.get("aliases"):
        var["source_field_names"] = list(slot["aliases"])
    return var


def reconstruct_owner(out_dir: Path, oid: str) -> list:
    profile = yaml.safe_load((out_dir / f"{oid}.yaml").read_text())
    enums = profile.get("enums") or {}
    rows = sssom_by_subject(out_dir / f"{oid}.sssom.yaml")
    out = []
    for sname in profile["classes"]["Record"]["slots"]:
        slot = profile["slots"][sname]
        out.append(reconstruct_variable(sname, slot, enums, rows.get(f"profiles:{sname}", [])))
    return out


def _norm(v):
    """Normalize a variable dict for order-insensitive comparison of its keys."""
    return {k: v[k] for k in sorted(v)}


def dynamic_enum_names() -> set:
    base = yaml.safe_load((ROOT / "schemas" / "base.yaml").read_text())
    return {n for n, e in (base.get("enums") or {}).items()
            if e.get("reachable_from") or ((e.get("annotations") or {}).get("source"))}


def term_ids(v: dict) -> set:
    ids = {t["id"] for t in (v.get("mixs_terms") or []) + (v.get("ontology_mappings") or [])}
    if v.get("bervo_term"):
        ids.add(v["bervo_term"]["id"])
    ids |= {lt["id"] for lt in v.get("level_terms") or [] if lt.get("id")}
    return ids


def _enriched_variables(kind: str, oid: str, out_dir: Path, dynamic: set, by_term: dict) -> list:
    profile = yaml.safe_load((out_dir / f"{oid}.yaml").read_text())
    enums = profile.get("enums") or {}
    slot_order = profile["classes"]["Record"]["slots"]
    rows = sssom_by_subject(out_dir / f"{oid}.sssom.yaml")
    variables = reconstruct_owner(out_dir, oid)
    owner_key = f"{kind}:{oid}"
    for v, sname in zip(variables, slot_order):
        rng = profile["slots"][sname].get("range")
        pred = {r["object_id"]: r["predicate_id"].split(":")[-1]
                for r in rows.get(f"profiles:{sname}", [])}
        if rng in enums:
            v["enum_kind"] = "static"
            v["level_terms"] = [{"value": lv, "id": (meta or {}).get("meaning")}
                                for lv, meta in (enums[rng].get("permissible_values") or {}).items()]
        elif rng in dynamic:
            v["enum_kind"] = "dynamic"
            v["enum_source"] = rng
        for t in (v.get("mixs_terms") or []) + (v.get("ontology_mappings") or []):
            if t["id"] in pred:
                t["mapping_relation"] = pred[t["id"]]
        if v.get("bervo_term") and v["bervo_term"]["id"] in pred:
            v["bervo_term"]["mapping_relation"] = pred[v["bervo_term"]["id"]]
        for tid in term_ids(v):
            by_term.setdefault(tid, []).append({"owner": owner_key, "variable": v["name"]})
    return variables


def build_index() -> dict:
    """The intermediate indexing product the browser consumes: variables for every study and
    dataset reconstructed from their profiles + SSSOM, enriched for the variable pages (enum
    kind, level->CURIE badges, mapping predicates), plus a `by_term` inverted index (ontology
    CURIE -> owners/variables) for cross-owner harmonization.
    """
    db = yaml.safe_load(DB_PATH.read_text())
    dynamic = dynamic_enum_names()
    studies, datasets, by_term = {}, {}, {}
    for kind, oid, out_dir, pid, owner in owners(db):
        entry = {"program": pid, "name": owner.get("name"),
                 "variables": _enriched_variables(kind, oid, out_dir, dynamic, by_term)}
        (studies if kind == "study" else datasets)[oid] = entry

    owned_by = {t: {o["owner"] for o in occ} for t, occ in by_term.items()}
    for kind, group in (("study", studies), ("dataset", datasets)):
        for oid, entry in group.items():
            self_key = f"{kind}:{oid}"
            for v in entry["variables"]:
                shared = {tid: len(owned_by.get(tid, set()) - {self_key}) for tid in term_ids(v)}
                shared = {k: n for k, n in shared.items() if n > 0}
                if shared:
                    v["shared"] = shared
    return {"studies": studies, "datasets": datasets, "by_term": dict(sorted(by_term.items()))}


def roundtrip_check() -> int:
    db = yaml.safe_load(DB_PATH.read_text())
    items = list(owners(db))
    mismatches = 0
    for kind, oid, out_dir, _pid, owner in items:
        original = owner.get("variables") or []
        rebuilt = reconstruct_owner(out_dir, oid)
        if [_norm(v) for v in original] != [_norm(v) for v in rebuilt]:
            mismatches += 1
            print(f"❌ {kind} {oid}: variables differ")
            for i, (a, b) in enumerate(zip(original, rebuilt)):
                if _norm(a) != _norm(b):
                    keys = {k for k in set(a) | set(b) if a.get(k) != b.get(k)}
                    print(f"    var[{i}] {a.get('name')!r}: "
                          f"DB={ {k: a.get(k) for k in keys} }  REBUILT={ {k: b.get(k) for k in keys} }")
            if len(original) != len(rebuilt):
                print(f"    length differs: DB={len(original)} REBUILT={len(rebuilt)}")
    total = len(items)
    print(f"\nRound-trip: {total - mismatches}/{total} owners (studies + datasets) identical.")
    return 1 if mismatches else 0


def write_back() -> int:
    """Mirror the profiles + SSSOM back into db/sfas-brcs.yaml: rewrite a study's `variables`
    block only when it differs from what the profile reconstructs. Uses ruamel line numbers +
    raw line-surgery so untouched studies stay byte-identical (no dumper reflow)."""
    from ruamel.yaml import YAML
    text = DB_PATH.read_text()
    raw = text.splitlines(keepends=True)
    rdata = YAML().load(text)
    plain = yaml.safe_load(text)

    def indent(line):
        s = line.rstrip("\n")
        return len(s) - len(s.lstrip(" ")) if s.strip() else 10 ** 9

    edits, changed = [], []
    for pk in PROG_KEYS:
        for pp, rp in zip(plain.get(pk) or [], rdata.get(pk) or []):
            for ps, rs in zip(pp.get("studies") or [], rp.get("studies") or []):
                if not ps.get("variables"):
                    continue
                sid = study_id(ps)
                rebuilt = reconstruct_owner(OUT_STUDIES, sid)
                if [_norm(v) for v in ps["variables"]] == [_norm(v) for v in rebuilt]:
                    continue
                changed.append(sid)
                vline = rs.lc.key("variables")[0]
                end = vline + 1
                while end < len(raw):
                    if not raw[end].strip():
                        end += 1
                        continue
                    ind = indent(raw[end])
                    if ind > 4 or (ind == 4 and raw[end].lstrip().startswith("- ")):
                        end += 1
                        continue
                    break
                block = yaml.safe_dump(rebuilt, sort_keys=False, allow_unicode=True,
                                       width=100, default_flow_style=False)
                new_lines = ["    " + ln if ln.strip() else ln
                             for ln in block.splitlines(keepends=True)]
                edits.append((vline + 1, end, new_lines))

    if not edits:
        print("sync-variables: db/sfas-brcs.yaml already mirrors profiles + SSSOM (no changes).")
        return 0
    for start, end, lines in sorted(edits, key=lambda e: e[0], reverse=True):
        raw[start:end] = lines
    DB_PATH.write_text("".join(raw))
    print(f"sync-variables: rewrote {len(changed)} study variables block(s): {', '.join(changed)}")
    return 0


def main() -> int:
    if "--index" in sys.argv:
        index = build_index()
        INDEX_PATH.write_text(yaml.safe_dump(index, sort_keys=False, allow_unicode=True, width=100))
        entries = list(index["studies"].values()) + list(index.get("datasets", {}).values())
        nvar = sum(len(e["variables"]) for e in entries)
        print(f"Wrote {INDEX_PATH.relative_to(ROOT)} ({len(index['studies'])} studies, "
              f"{len(index.get('datasets', {}))} datasets, {nvar} variables, "
              f"{len(index['by_term'])} indexed terms)")
        return 0
    if "--check" in sys.argv:
        return roundtrip_check()
    return write_back()


if __name__ == "__main__":
    sys.exit(main())
