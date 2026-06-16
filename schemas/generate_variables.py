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
INDEX_PATH = ROOT / "schemas" / "variable-index.yaml"
PROG_KEYS = [
    "bioenergy_research_centers", "genomic_science_sfas", "environmental_system_science_sfas",
    "user_facilities", "ai_projects", "other_programs",
]
ANNOT_FACETS = ("measured_entity", "material_or_matrix", "method",
                "temporal_resolution", "spatial_resolution", "notes")


def study_id(study: dict) -> str:
    sid = study.get("nmdc_study_id")
    return sid.split(":")[-1] if sid else _slug(study.get("name"))


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
        obj = {"id": r["object_id"], "label": r["object_label"]}
        prefix = r["object_id"].split(":")[0]
        if prefix == "MIXS":
            mixs.append(obj)
        elif prefix == "BERVO":
            bervo = obj
        elif prefix == "UO":
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


def reconstruct_study(sid: str) -> list:
    profile = yaml.safe_load((OUT_STUDIES / f"{sid}.yaml").read_text())
    enums = profile.get("enums") or {}
    rows = sssom_by_subject(OUT_STUDIES / f"{sid}.sssom.yaml")
    out = []
    for sname in profile["classes"]["Record"]["slots"]:
        slot = profile["slots"][sname]
        out.append(reconstruct_variable(sname, slot, enums, rows.get(f"profiles:{sname}", [])))
    return out


def _norm(v):
    """Normalize a variable dict for order-insensitive comparison of its keys."""
    return {k: v[k] for k in sorted(v)}


def build_index() -> dict:
    """The intermediate indexing product the browser consumes: variables reconstructed from
    study metadata (profiles + SSSOM), plus a `by_term` inverted index (ontology CURIE ->
    studies/variables) for cross-study harmonization.
    """
    db = yaml.safe_load(DB_PATH.read_text())
    studies, by_term = {}, {}
    for pk in PROG_KEYS:
        for p in db.get(pk) or []:
            pid = p.get("id")
            for s in p.get("studies") or []:
                if not s.get("variables"):
                    continue
                sid = study_id(s)
                profile = yaml.safe_load((OUT_STUDIES / f"{sid}.yaml").read_text())
                enums = profile.get("enums") or {}
                variables = reconstruct_study(sid)
                studies[sid] = {"program": pid, "name": s.get("name"), "variables": variables}
                for v in variables:
                    maps = list(v.get("mixs_terms") or [])
                    if v.get("bervo_term"):
                        maps.append(v["bervo_term"])
                    if v.get("unit_term"):
                        maps.append(v["unit_term"])
                    maps += list(v.get("ontology_mappings") or [])
                    for m in maps:
                        by_term.setdefault(m["id"], []).append(
                            {"study": sid, "variable": v["name"], "via": "mapping"})
                for sname in profile["classes"]["Record"]["slots"]:
                    rng = profile["slots"][sname].get("range")
                    if rng in enums:
                        for lv, meta in (enums[rng].get("permissible_values") or {}).items():
                            if meta and meta.get("meaning"):
                                by_term.setdefault(meta["meaning"], []).append(
                                    {"study": sid, "variable": profile["slots"][sname].get("title") or sname,
                                     "level": lv, "via": "level"})
    return {"studies": studies, "by_term": dict(sorted(by_term.items()))}


def roundtrip_check() -> int:
    db = yaml.safe_load(DB_PATH.read_text())
    studies = [(study_id(s), s) for pk in PROG_KEYS for p in db.get(pk) or []
               for s in p.get("studies") or [] if s.get("variables")]
    mismatches = 0
    for sid, study in studies:
        original = study.get("variables") or []
        rebuilt = reconstruct_study(sid)
        if [_norm(v) for v in original] != [_norm(v) for v in rebuilt]:
            mismatches += 1
            print(f"❌ {sid}: variables differ")
            for i, (a, b) in enumerate(zip(original, rebuilt)):
                if _norm(a) != _norm(b):
                    keys = {k for k in set(a) | set(b) if a.get(k) != b.get(k)}
                    print(f"    var[{i}] {a.get('name')!r}: "
                          f"DB={ {k: a.get(k) for k in keys} }  REBUILT={ {k: b.get(k) for k in keys} }")
            if len(original) != len(rebuilt):
                print(f"    length differs: DB={len(original)} REBUILT={len(rebuilt)}")
    total = len(studies)
    print(f"\nRound-trip: {total - mismatches}/{total} studies identical.")
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
                rebuilt = reconstruct_study(sid)
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
        nvar = sum(len(s["variables"]) for s in index["studies"].values())
        print(f"Wrote {INDEX_PATH.relative_to(ROOT)} "
              f"({len(index['studies'])} studies, {nvar} variables, {len(index['by_term'])} indexed terms)")
        return 0
    if "--check" in sys.argv:
        return roundtrip_check()
    return write_back()


if __name__ == "__main__":
    sys.exit(main())
