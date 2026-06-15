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


def main() -> int:
    check = "--check" in sys.argv
    db = yaml.safe_load(DB_PATH.read_text())
    studies = [(study_id(s), s) for pk in PROG_KEYS for p in db.get(pk) or []
               for s in p.get("studies") or [] if s.get("variables")]

    if not check:
        print(f"Reconstructed variables for {len(studies)} studies (use --check to verify).")
        return 0

    mismatches = 0
    for sid, study in studies:
        original = study.get("variables") or []
        rebuilt = reconstruct_study(sid)
        if [_norm(v) for v in original] != [_norm(v) for v in rebuilt]:
            mismatches += 1
            print(f"❌ {sid}: variables differ")
            for i, (a, b) in enumerate(zip(original, rebuilt)):
                if _norm(a) != _norm(b):
                    da = {k: a.get(k) for k in set(a) | set(b) if a.get(k) != b.get(k)}
                    db_ = {k: b.get(k) for k in set(a) | set(b) if a.get(k) != b.get(k)}
                    print(f"    var[{i}] {a.get('name')!r}: DB={da}  REBUILT={db_}")
            if len(original) != len(rebuilt):
                print(f"    length differs: DB={len(original)} REBUILT={len(rebuilt)}")
    total = len(studies)
    print(f"\nRound-trip: {total - mismatches}/{total} studies identical.")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
