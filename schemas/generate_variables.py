"""Build the variable index (schemas/variable-index.yaml) from the per-owner LinkML profiles +
SSSOM mapping tables (schemas/{studies,datasets}/<id>.yaml + .sssom.yaml), which are now the
single Source of Truth for variables. Reconstructs each study's/dataset's variable catalog,
enriches it for the variable pages, and adds a `by_term` inverted index for harmonization.

Run with: just gen-variable-index
"""

import re
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


def make_anchor_id(value: str) -> str:
    """HTML anchor slug — kept identical to the browser so variable-page links match program pages."""
    return re.sub(r"[^a-z0-9_-]+", "-", (value or "").lower()).strip("-")


def owner_anchor(program_id: str, kind: str, name: str) -> str:
    return make_anchor_id(f"{program_id}-{kind}-{name}")


def owners(db: dict):
    """Yield (kind, oid, out_dir, collection_key, program, owner) for every study/dataset that has
    a profile. Gated on profile-file existence (not db.variables), since the profiles are now the
    Source of Truth and the inline db.variables catalog has been dropped."""
    for pk in PROG_KEYS:
        for p in db.get(pk) or []:
            for s in p.get("studies") or []:
                oid = study_id(s)
                if (OUT_STUDIES / f"{oid}.yaml").exists():
                    yield "study", oid, OUT_STUDIES, pk, p, s
            for d in p.get("datasets") or []:
                oid = dataset_id(d)
                if (OUT_DATASETS / f"{oid}.yaml").exists():
                    yield "dataset", oid, OUT_DATASETS, pk, p, d


def _slug(name):
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


def variable_record(variable: dict, program: dict, collection_key: str, kind: str, owner: dict) -> dict:
    """Flatten one variable into the record the variable pages render (owner/program context +
    HTML anchors + enrichment). Kept structurally identical to what the browser produced."""
    owner_name = owner.get("name", "unknown")
    program_id = program.get("id") or make_anchor_id(program.get("name", "program"))
    return {
        "id": make_anchor_id(f"{program_id}-{kind}-{owner_name}-{variable.get('name', 'variable')}"),
        "name": variable.get("name"),
        "description": variable.get("description"),
        "roles": variable.get("roles") or [],
        "value_type": variable.get("value_type"),
        "units": variable.get("units"),
        "measured_entity": variable.get("measured_entity"),
        "material_or_matrix": variable.get("material_or_matrix"),
        "method": variable.get("method"),
        "time_series": variable.get("time_series"),
        "temporal_resolution": variable.get("temporal_resolution"),
        "spatial_resolution": variable.get("spatial_resolution"),
        "levels": variable.get("levels") or [],
        "level_terms": variable.get("level_terms") or [],
        "enum_kind": variable.get("enum_kind"),
        "enum_source": variable.get("enum_source"),
        "shared": variable.get("shared") or {},
        "source_field_names": variable.get("source_field_names") or [],
        "mappings": {
            "bervo": variable.get("bervo_term"),
            "mixs": variable.get("mixs_terms") or [],
            "other": variable.get("ontology_mappings") or [],
            "unit": variable.get("unit_term"),
        },
        "owner": {
            "type": kind,
            "name": owner_name,
            "anchor_id": owner_anchor(program_id, kind, owner_name),
            "nmdc_study_id": owner.get("nmdc_study_id"),
            "bioproject_ids": owner.get("bioproject_ids") or [],
            "doi": owner.get("doi"),
            "url": owner.get("url"),
            "primary_reference": owner.get("primary_reference_info", {}).get("reference", {}).get("id"),
        },
        "program": {
            "collection": collection_key,
            "id": program.get("id"),
            "name": program.get("name"),
            "acronym": program.get("acronym"),
            "anchor_id": program_id,
        },
    }


def build_variable_view(records: list) -> dict:
    """The flat, BERVO/MIxS-grouped variable index the variable pages render."""
    records = sorted(records, key=lambda r: (r["name"] or "").lower())
    by_bervo, by_mixs = {}, {}
    for r in records:
        bervo = r["mappings"].get("bervo")
        if bervo:
            by_bervo.setdefault(bervo["id"], {"term": bervo, "variable_ids": []})["variable_ids"].append(r["id"])
        for mixs in r["mappings"].get("mixs") or []:
            by_mixs.setdefault(mixs["id"], {"term": mixs, "variable_ids": []})["variable_ids"].append(r["id"])
    key = lambda g: (g["term"].get("label") or g["term"]["id"]).lower()
    without_bervo = [r["id"] for r in records if not r["mappings"].get("bervo")]
    return {
        "summary": {
            "variable_count": len(records),
            "study_variable_count": sum(1 for r in records if r["owner"]["type"] == "study"),
            "dataset_variable_count": sum(1 for r in records if r["owner"]["type"] == "dataset"),
            "bervo_mapped_variable_count": len(records) - len(without_bervo),
            "bervo_term_count": len(by_bervo),
            "mixs_term_count": len(by_mixs),
            "without_bervo_count": len(without_bervo),
        },
        "records": records,
        "records_by_id": {r["id"]: r for r in records},
        "by_bervo": sorted(by_bervo.values(), key=key),
        "by_mixs": sorted(by_mixs.values(), key=key),
        "without_bervo": without_bervo,
    }


def build_index() -> dict:
    """The single producer of all variable-derived data the HTML consumes: per-owner variables
    (for the program pages) reconstructed from profiles + SSSOM and enriched (enum kind,
    level->CURIE badges, mapping predicates, shared counts); a `by_term` inverted index; and the
    flat `variable_index` view (records + BERVO/MIxS groupings) for the variable pages. The browser
    is a thin renderer of union(db, this index).
    """
    db = yaml.safe_load(DB_PATH.read_text())
    dynamic = dynamic_enum_names()
    studies, datasets, by_term, contexts = {}, {}, {}, []
    for kind, oid, out_dir, ck, program, owner in owners(db):
        entry = {"program": program.get("id"), "name": owner.get("name"),
                 "variables": _enriched_variables(kind, oid, out_dir, dynamic, by_term)}
        (studies if kind == "study" else datasets)[oid] = entry
        contexts.append((kind, ck, program, owner, entry["variables"]))

    owned_by = {t: {o["owner"] for o in occ} for t, occ in by_term.items()}
    for kind, group in (("study", studies), ("dataset", datasets)):
        for oid, entry in group.items():
            self_key = f"{kind}:{oid}"
            for v in entry["variables"]:
                shared = {tid: len(owned_by.get(tid, set()) - {self_key}) for tid in sorted(term_ids(v))}
                shared = {k: n for k, n in shared.items() if n > 0}
                if shared:
                    v["shared"] = shared

    records = [variable_record(v, program, ck, kind, owner)
               for kind, ck, program, owner, variables in contexts for v in variables]
    return {"studies": studies, "datasets": datasets,
            "by_term": dict(sorted(by_term.items())), "variable_index": build_variable_view(records)}


def main() -> int:
    """Build the variable index from the profiles + SSSOM (the Source of Truth). The inline
    db.variables catalog has been dropped, so there is no longer a mirror/round-trip to db."""
    index = build_index()
    INDEX_PATH.write_text(yaml.safe_dump(index, sort_keys=False, allow_unicode=True, width=100))
    entries = list(index["studies"].values()) + list(index.get("datasets", {}).values())
    nvar = sum(len(e["variables"]) for e in entries)
    print(f"Wrote {INDEX_PATH.relative_to(ROOT)} ({len(index['studies'])} studies, "
          f"{len(index.get('datasets', {}))} datasets, {nvar} variables, "
          f"{len(index['by_term'])} indexed terms)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
