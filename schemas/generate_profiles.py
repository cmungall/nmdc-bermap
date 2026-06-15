"""Generate per-study (and per-site) LinkML data-dictionary profiles from db/sfas-brcs.yaml.

See docs/superpowers/specs/2026-06-13-per-study-linkml-profiles-design.md.

Source of truth remains the inline `variables` catalog in db/sfas-brcs.yaml (decision i-a);
these profiles are a regenerable artifact. base.yaml is hand-authored and never overwritten.
Run with: just gen-profiles
"""

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "db" / "sfas-brcs.yaml"
SCHEMAS = ROOT / "schemas"
OUT_STUDIES = SCHEMAS / "studies"
OUT_SITES = SCHEMAS / "sites"
BASE_URI = "https://w3id.org/nmdc-sfas-brcs/profiles"

PROG_KEYS = [
    "bioenergy_research_centers",
    "genomic_science_sfas",
    "environmental_system_science_sfas",
    "user_facilities",
    "ai_projects",
    "other_programs",
]

PREFIXES = {
    "linkml": "https://w3id.org/linkml/",
    "profiles": "https://w3id.org/nmdc-sfas-brcs/profiles/",
    "MIXS": "https://w3id.org/mixs/",
    "ENVO": "http://purl.obolibrary.org/obo/ENVO_",
    "PO": "http://purl.obolibrary.org/obo/PO_",
    "NCBITaxon": "http://purl.obolibrary.org/obo/NCBITaxon_",
    "CHEBI": "http://purl.obolibrary.org/obo/CHEBI_",
    "BERVO": "http://purl.obolibrary.org/obo/BERVO_",
    "OBI": "http://purl.obolibrary.org/obo/OBI_",
    "UO": "http://purl.obolibrary.org/obo/UO_",
    "obo": "http://purl.obolibrary.org/obo/",
    "nmdc": "https://w3id.org/nmdc/",
    "GOLD": "https://gold.jgi.doe.gov/",
}

# LinkML range per Variable.value_type (CATEGORICAL and ARRAY handled specially).
VALUE_TYPE_RANGE = {
    "NUMERIC": "float",
    "INTEGER": "integer",
    "BOOLEAN": "boolean",
    "DATETIME": "datetime",
    "TEXT": "string",
    "IDENTIFIER": "string",
    "ONTOLOGY_TERM": "uriorcurie",
    "OBJECT": "string",
}

# Unit label -> UCUM code, for the ~16 unit labels in use. None = no clean UCUM (label only).
UCUM = {
    "meter": "m",
    "m": "m",
    "centimeter": "cm",
    "cm": "cm",
    "gram": "g",
    "degree Celsius": "Cel",
    "degree": "deg",
    "percent": "%",
    "day": "d",
    "days": "d",
    "years": "a",
    "liter": "L",
    "milligram per kilogram": "mg/kg",
    "microgram per gram": "ug/g",
    "meter per second": "m/s",
    "kilogram per hectare": "kg/Har",
    "micromole per square meter per second": "umol/(m2.s)",
    "gram per milliliter": "g/mL",
    "dimensionless": "1",
    "practical salinity units": None,
    "log2 fold change": None,
    "infectious units per milliliter": None,
    "seconds or minutes": None,
}

# Governed categoricals (no per-study enumeration) -> dynamic enum defined in base.yaml.
# Matched against the variable slug and its source_field_names.
DYNAMIC_BINDINGS = {
    "ecosystem": "GoldEcosystemPathEnum",
    "ecosystem_category": "GoldEcosystemPathEnum",
    "ecosystem_type": "GoldEcosystemPathEnum",
    "ecosystem_subtype": "GoldEcosystemPathEnum",
    "specific_ecosystem": "GoldEcosystemPathEnum",
    "environmental_package": "EnvPackageEnum",
    "env_package": "EnvPackageEnum",
    "host_common_name": "HostCommonNameEnum",
    "env_broad_scale": "EnvBroadScaleEnum",
    "env_local_scale": "EnvLocalScaleEnum",
    "env_medium": "EnvMediumEnum",
}

LEVEL_MEANINGS_PATH = SCHEMAS / "level_meanings.yaml"


def slugify(name: str) -> str:
    s = re.sub(r"[^0-9a-zA-Z]+", "_", (name or "").strip().lower())
    return re.sub(r"_+", "_", s).strip("_")


def ncname(s: str) -> str:
    """Make a valid NCName (schema/enum/slot names): must not start with a digit."""
    s = s or "x"
    return "_" + s if s[0].isdigit() else s


def camel(slug: str) -> str:
    return "".join(p.capitalize() for p in slug.split("_") if p)


def harvest_meanings(db: dict) -> dict:
    """Build {level_text_lower: CURIE} from the DB's OWN vetted ontology mappings.

    Reuses ids the project already curated (ontology_mappings / bervo_term), then overlays the
    curated, OLS-verified groundings in level_meanings.yaml. No CURIEs are invented here.
    """
    out = {}
    for prog_key in PROG_KEYS:
        for prog in db.get(prog_key) or []:
            for study in prog.get("studies") or []:
                for v in study.get("variables") or []:
                    for m in v.get("ontology_mappings") or []:
                        if m.get("label") and m.get("id"):
                            out.setdefault(m["label"].strip().lower(), m["id"])
                    bv = v.get("bervo_term")
                    if bv and bv.get("label") and bv.get("id"):
                        out.setdefault(bv["label"].strip().lower(), bv["id"])
    curated = yaml.safe_load(LEVEL_MEANINGS_PATH.read_text()) or {}
    out.update({str(k).strip().lower(): v for k, v in curated.items()})
    return out


def slot_mappings(v: dict) -> list:
    """Slot -> ontology mappings as (object_id, object_label, predicate), emitted to SSSOM
    (not inline in the schema). Source bucket is recoverable from the object CURIE prefix on
    the reverse trip: MIXS->mixs_terms, BERVO->bervo_term, UO->unit_term, else->ontology_mappings.
    """
    out = []
    for m in v.get("mixs_terms") or []:
        if m.get("id"):
            out.append((m["id"], m.get("label"), "skos:exactMatch"))
    bv = v.get("bervo_term")
    if bv and bv.get("id"):
        out.append((bv["id"], bv.get("label"), "skos:exactMatch"))
    ut = v.get("unit_term")
    if ut and ut.get("id"):
        out.append((ut["id"], ut.get("label"), "skos:closeMatch"))
    for m in v.get("ontology_mappings") or []:
        if m.get("id"):
            out.append((m["id"], m.get("label"), "skos:relatedMatch"))
    return out


def dynamic_binding(slug: str, source_fields: list) -> str | None:
    if slug in DYNAMIC_BINDINGS:
        return DYNAMIC_BINDINGS[slug]
    for sf in source_fields or []:
        if slugify(sf) in DYNAMIC_BINDINGS:
            return DYNAMIC_BINDINGS[slugify(sf)]
    return None


def build_unit(label: str) -> dict:
    unit = {"descriptive_name": label}
    code = UCUM.get(label, "MISSING")
    if code not in (None, "MISSING"):
        unit["ucum_code"] = code
    return unit


def build_variable(v: dict, enums: dict, meanings: dict):
    """Return (slot_name, slot_dict); register any generated static enum into `enums`."""
    name = v.get("name")
    slug = slugify(name)
    slot = {}
    if name != slug:
        slot["title"] = name
    if v.get("description"):
        slot["description"] = v["description"]

    vt = v.get("value_type")
    source_fields = v.get("source_field_names") or []
    if vt == "CATEGORICAL":
        levels = v.get("levels")
        if levels:
            enum_name = ncname(camel(slug) + "Enum")
            pvs = {}
            for lv in levels:
                meaning = meanings.get(str(lv).strip().lower())
                pvs[lv] = {"meaning": meaning} if meaning else None
            enums[enum_name] = {"permissible_values": pvs}
            slot["range"] = enum_name
        else:
            dyn = dynamic_binding(slug, source_fields)
            slot["range"] = dyn if dyn else "string"
    elif vt == "ARRAY":
        slot["multivalued"] = True
        slot["range"] = "string"
    else:
        slot["range"] = VALUE_TYPE_RANGE.get(vt, "string")

    if v.get("units"):
        slot["unit"] = build_unit(v["units"])

    if source_fields:
        slot["aliases"] = list(source_fields)

    ann = {}
    if v.get("roles"):
        ann["role"] = "; ".join(v["roles"])
    for facet in ("measured_entity", "material_or_matrix", "method",
                  "temporal_resolution", "spatial_resolution", "notes"):
        if v.get(facet):
            ann[facet] = v[facet]
    # non-CATEGORICAL variables can still carry example levels (NUMERIC bins, IDENTIFIER
    # examples); CATEGORICAL levels live in the enum, these go in an annotation.
    if v.get("levels") and vt != "CATEGORICAL":
        ann["levels"] = " | ".join(v["levels"])
    if v.get("time_series"):
        ann["time_series"] = "true"
    ann["value_type"] = vt
    slot["annotations"] = ann
    return ncname(slug), slot, slot_mappings(v)


def study_id(study: dict) -> str:
    sid = study.get("nmdc_study_id")
    if sid:
        return sid.split(":")[-1]
    return slugify(study.get("name"))


def dump(path: Path, data: dict):
    text = yaml.safe_dump(data, sort_keys=False, default_flow_style=False,
                          allow_unicode=True, width=100)
    path.write_text(text)


def generate():
    db = yaml.safe_load(DB_PATH.read_text())
    meanings = harvest_meanings(db)
    OUT_STUDIES.mkdir(parents=True, exist_ok=True)
    OUT_SITES.mkdir(parents=True, exist_ok=True)

    n_study = n_slot = n_enum = 0
    for prog_key in PROG_KEYS:
        for prog in db.get(prog_key) or []:
            for study in prog.get("studies") or []:
                variables = study.get("variables") or []
                if not variables:
                    continue
                sid = study_id(study)
                slots, enums, mappings = {}, {}, []
                for v in variables:
                    sname, sdict, vmaps = build_variable(v, enums, meanings)
                    slots[sname] = sdict
                    for oid, olabel, pred in vmaps:
                        mappings.append({
                            "subject_id": f"profiles:{sname}",
                            "subject_label": v.get("name"),
                            "predicate_id": pred,
                            "object_id": oid,
                            "object_label": olabel,
                            "mapping_justification": "semapv:ManualMappingCuration",
                        })
                imports = ["../base"]
                for fs in study.get("field_site_ids") or []:
                    imports.append("../sites/" + fs.split(":")[-1])
                profile = {
                    "id": f"{BASE_URI}/studies/{sid}",
                    "name": ncname(slugify(study.get("name")) or sid),
                    "title": study.get("name"),
                    "description": (study.get("description") or "").strip() or None,
                    "prefixes": PREFIXES,
                    "default_prefix": "profiles",
                    "default_range": "string",
                    "imports": imports,
                    "classes": {
                        "Record": {
                            "description": f"Per-record data dictionary for study {sid}.",
                            "slots": list(slots.keys()),
                        }
                    },
                    "slots": dict(slots),
                }
                if enums:
                    profile["enums"] = dict(enums)
                profile = {k: v for k, v in profile.items() if v is not None}
                dump(OUT_STUDIES / f"{sid}.yaml", profile)
                if mappings:
                    dump(OUT_STUDIES / f"{sid}.sssom.yaml", {"mappings": mappings})
                n_study += 1
                n_slot += len(slots)
                n_enum += len(enums)

    n_site = 0
    for site in db.get("sites") or []:
        sid = site.get("id", "").split(":")[-1]
        if not sid:
            continue
        slots = {}
        if site.get("location"):
            slots["location"] = {"description": "Geographic location of the site.",
                                 "annotations": {"value": site["location"]}}
        if site.get("site_type"):
            slots["site_type"] = {"annotations": {"value": site["site_type"]}}
        if site.get("elevation_m") is not None:
            slots["elevation"] = {"range": "float",
                                  "unit": {"descriptive_name": "meter", "ucum_code": "m"}}
        if site.get("mean_annual_temp_c") is not None:
            slots["mean_annual_temperature"] = {
                "range": "float", "unit": {"descriptive_name": "degree Celsius", "ucum_code": "Cel"}}
        if site.get("mean_annual_precip_cm") is not None:
            slots["mean_annual_precipitation"] = {
                "range": "float", "unit": {"descriptive_name": "centimeter", "ucum_code": "cm"}}
        if site.get("contaminants"):
            slots["contaminants"] = {"multivalued": True, "range": "string"}
        profile = {
            "id": f"{BASE_URI}/sites/{sid}",
            "name": ncname(slugify(site.get("name")) or sid),
            "title": site.get("name"),
            "description": (site.get("description") or "").strip() or None,
            "prefixes": PREFIXES,
            "default_prefix": "profiles",
            "default_range": "string",
            "imports": ["../base"],
            "classes": {
                "SiteContext": {
                    "description": f"Environmental context for site {sid}.",
                    "slots": sorted(slots.keys()),
                }
            },
        }
        if slots:
            profile["slots"] = dict(sorted(slots.items()))
        profile = {k: v for k, v in profile.items() if v is not None}
        dump(OUT_SITES / f"{sid}.yaml", profile)
        n_site += 1

    print(f"Wrote {n_study} study profiles ({n_slot} slots, {n_enum} static enums) "
          f"and {n_site} site profiles to {SCHEMAS}")


if __name__ == "__main__":
    generate()
