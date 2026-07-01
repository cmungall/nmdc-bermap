"""GLBRC MMPRNT env-triad curation for PRJNA73310{9,5,4}.

Applies §1b inference rules from .claude/skills/nmdc-env-triad.md, with
plot/site context drawn from biosample.ncbi_title where possible.
"""
import json
import re
from copy import deepcopy

# Validated ENVO terms (from runoak info / ancestors checks in this run).
ENVO = {
    "cropland_biome":      ("ENVO:01000245", "cropland biome"),
    "agricultural_field":  ("ENVO:00000114", "agricultural field"),
    "farm_soil":           ("ENVO:00005749", "farm soil"),
    "grassland_biome":     ("ENVO:01000177", "grassland biome"),
    "prairie":             ("ENVO:00000260", "prairie"),
    "grassland_area":      ("ENVO:00000106", "grassland area"),
    "grassland_soil":      ("ENVO:00005750", "grassland soil"),
    "soil":                ("ENVO:00001998", "soil"),
    "sentinel":            ("ENVO:00000000", "(not provided)"),
}

STRUCTURED_RE = re.compile(
    r"^(?P<setid>\d+)_(?P<date>\d{6})_MMPRNT_(?P<site>[A-Z]+)_(?P<plot>G\d+)_"
    r"(?:rep(?P<rep>\d+)|composite)_(?P<fert>Fert|Unfert)_(?:pseudo\d+|r\w+)$"
)
MMPRNT_NUMERIC_RE = re.compile(r"^MMPRNT-?\d+$")
# Composite / non-structured G5 references that still encode plot=G5
G5_FALLBACK_RES = [
    re.compile(r"^MMPRNT-?(LUX|LC|RHN|ESC|HAN|ORG)G5\d+$"),
    re.compile(r"^MMPRNT(LUX|LC|RHN|ESC|HAN|ORG)G5\d+$"),
    re.compile(r"^(LUX|LC|RHN|ESC|HAN|ORG)\d+G5_[A-Z]$"),
]
# Mock-community / lab-standard / unresolved control patterns → left_sentinel
CONTROL_PATTERNS = [
    re.compile(r"^Zymo", re.IGNORECASE),
    re.compile(r"^MMPRNT-Zymo", re.IGNORECASE),
    re.compile(r"^ZymoMock", re.IGNORECASE),
    re.compile(r"^Freeze-", re.IGNORECASE),
    re.compile(r"^error-", re.IGNORECASE),
    re.compile(r"^CTRL-", re.IGNORECASE),
]


def is_control(title: str) -> bool:
    return any(p.search(title) for p in CONTROL_PATTERNS)


def classify(title: str, project_year: int):
    """Return (kind, plot_or_None, evidence_quote)."""
    if is_control(title):
        return ("control", None, "mock / kit / freeze / error / control")
    m = STRUCTURED_RE.match(title)
    if m:
        return ("structured", m.group("plot"), f"title encodes {m.group('plot')}/{m.group('site')}")
    for r in G5_FALLBACK_RES:
        if r.match(title):
            return ("structured", "G5", "title encodes G5 plot")
    if MMPRNT_NUMERIC_RE.match(title) or title.startswith("MMPRNT-"):
        return ("numeric_unmapped", None, "MMPRNT-NNNN; plot mapping in OSF supplement (unavailable)")
    return ("unknown", None, f"unrecognised pattern {title!r}")


def triad_for(kind: str, plot: str | None, project_year: int):
    """Return dict {slot: (curie,label,evidence_rows,candidates)} or None for sentinel.

    Returns slot-keyed mapping. Slot value None means leave sentinel.
    """
    out = {"env_broad_scale": None, "env_local_scale": None, "env_medium": None}

    if kind == "control":
        return out  # all sentinel; controls don't belong to a biome
    if kind == "unknown":
        return out

    if kind == "structured":
        if plot == "G5":
            out["env_broad_scale"] = ENVO["cropland_biome"]
            out["env_local_scale"] = ENVO["agricultural_field"]
            out["env_medium"]      = ENVO["farm_soil"]
        elif plot == "G10":
            out["env_broad_scale"] = ENVO["grassland_biome"]
            out["env_local_scale"] = ENVO["prairie"]
            out["env_medium"]      = ENVO["grassland_soil"]
        elif plot == "G11":
            out["env_broad_scale"] = ENVO["grassland_biome"]
            out["env_local_scale"] = ENVO["grassland_area"]
            out["env_medium"]      = ENVO["grassland_soil"]
        else:
            # Unrecognised plot code (e.g. G6/G7/G8/G9) — leave sentinel; user noted only G5/G10/G11
            pass
        return out

    if kind == "numeric_unmapped":
        # No per-sample plot — leave broad/local sentinel; soil medium is the only
        # safely-inferred slot because isolation_source = "Switchgrass Soils" applies per-sample.
        out["env_medium"] = ENVO["soil"]
        return out

    return out


def build_evidence(kind: str, plot: str | None, title: str, attrs: dict, study_title: str):
    """Return a list of evidence rows shared by the slot's commit."""
    rows = []
    if kind == "structured":
        rows.append({"source": "biosample.title", "quote_or_paraphrase": f"plot={plot} from sample name"})
        if attrs.get("isolation_source"):
            rows.append({"source": "biosample.attributes.isolation_source",
                          "quote_or_paraphrase": attrs["isolation_source"][:80]})
        rows.append({"source": "BioProject.title", "quote_or_paraphrase": "GLBRC MMPRNT marginal lands experiment"})
    elif kind == "numeric_unmapped":
        if attrs.get("isolation_source"):
            rows.append({"source": "biosample.attributes.isolation_source",
                          "quote_or_paraphrase": attrs["isolation_source"][:80]})
        rows.append({"source": "BioProject.title", "quote_or_paraphrase": study_title[:80]})
    return rows


def update_report_row(row, curie_label, evidence, candidates, validator_pass):
    if curie_label is None:
        row["outcome"] = "left_sentinel"
        row["committed_curie"] = None
        row["committed_label"] = None
        row["evidence"] = evidence
        row["candidates_considered"] = candidates
        row["validator"] = {"info_ok": None, "anchor_ok": None, "valueset_ok": None}
        return
    curie, label = curie_label
    row["outcome"] = "predicted"
    row["committed_curie"] = curie
    row["committed_label"] = label
    row["evidence"] = evidence
    row["candidates_considered"] = candidates
    row["validator"] = {"info_ok": True, "anchor_ok": True, "valueset_ok": None}


def set_biosample_slot(biosample, slot, curie_label, raw_value=""):
    if curie_label is None:
        # leave sentinel exactly as the pipeline emitted it
        return
    curie, label = curie_label
    biosample[slot] = {
        "type": "nmdc:ControlledIdentifiedTermValue",
        "has_raw_value": raw_value,
        "term": {
            "id": curie,
            "type": "nmdc:OntologyClass",
            "name": label,
        },
    }


def curate_project(accession: str, year: int):
    base = f"/tmp/wbc_ingest/{accession}"
    db = json.load(open(f"{base}.json"))
    inputs = json.load(open(f"{base}_curation_inputs.json"))
    report = json.load(open(f"{base}_curation_report.json"))

    bs_by_id = {b["id"]: b for b in db["biosample_set"]}
    inputs_by_id = inputs["biosamples"]
    study_title = inputs["study"]["title"]

    # Group report rows by biosample for fast lookup
    rows_by_bsm = {}
    for row in report["rows"]:
        rows_by_bsm.setdefault(row["biosample_id"], {})[row["slot"]] = row

    summary = {slot: {"predicted": 0, "resolved_from_raw": 0, "resolved_at_pipeline": 0,
                       "left_sentinel": 0, "validator_rejected": 0}
                for slot in ("env_broad_scale", "env_local_scale", "env_medium")}

    for bid, bsm in bs_by_id.items():
        ctx = inputs_by_id.get(bid, {})
        title = ctx.get("ncbi_title", "")
        attrs = ctx.get("attributes", {})

        kind, plot, kind_quote = classify(title, year)
        triad = triad_for(kind, plot, year)
        evidence = build_evidence(kind, plot, title, attrs, study_title)
        # one classification evidence row at the head
        head = [{"source": "biosample.title", "quote_or_paraphrase": f"{kind}: {kind_quote}"}]

        for slot in ("env_broad_scale", "env_local_scale", "env_medium"):
            cl = triad.get(slot)
            row = rows_by_bsm[bid][slot]
            ev = head + evidence if cl is not None else []
            set_biosample_slot(bsm, slot, cl)
            update_report_row(row, cl, ev, [], validator_pass=True)
            summary[slot][row["outcome"]] += 1

    json.dump(db,      open(f"{base}.json", "w"),      indent=2)
    json.dump(report,  open(f"{base}_curation_report.json", "w"),  indent=2)

    return summary


if __name__ == "__main__":
    grand = {slot: {"predicted": 0, "resolved_from_raw": 0, "resolved_at_pipeline": 0,
                     "left_sentinel": 0, "validator_rejected": 0}
              for slot in ("env_broad_scale", "env_local_scale", "env_medium")}
    for acc, year in [("PRJNA733109", 2016), ("PRJNA733505", 2017), ("PRJNA733764", 2018)]:
        s = curate_project(acc, year)
        print(f"\n=== {acc} ({year}) ===")
        for slot, c in s.items():
            print(f"  {slot}: {c}")
            for k, v in c.items():
                grand[slot][k] += v
    print("\n=== CONSOLIDATED ===")
    for slot, c in grand.items():
        print(f"  {slot}: {c}")
    print(f"\nTotal left_sentinel backlog (sum across 3 slots): "
           f"{sum(grand[s]['left_sentinel'] for s in grand)}")
