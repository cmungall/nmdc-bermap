"""Validate catalogued variables against NMDC biosample attributes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import requests
import yaml

NMDC_API_BASE = "https://api.microbiomedata.org/nmdcschema"
DEFAULT_PAGE_SIZE = 500

PROGRAM_COLLECTION_KEYS = (
    "bioenergy_research_centers",
    "genomic_science_sfas",
    "environmental_system_science_sfas",
    "user_facilities",
    "ai_projects",
    "other_programs",
)

ADMIN_SAMPLE_ATTRIBUTES = {
    "analysis_type",
    "associated_studies",
    "alternative_identifiers",
    "biosample_categories",
    "description",
    "emsl_biosample_identifiers",
    "gold_biosample_identifiers",
    "id",
    "img_identifiers",
    "insdc_biosample_identifiers",
    "misc_param",
    "name",
    "ncbi_taxonomy_name",
    "provenance_metadata",
    "samp_name",
    "samp_store_temp",
    "samp_taxon_id",
    "source_mat_id",
    "store_cond",
    "type",
}

NON_SAMPLE_SOURCE_FIELD_PATTERNS = (
    "abundance",
    "activity",
    "annotation",
    "assembly",
    "bin",
    "counts",
    "diversity",
    "expression",
    "feature",
    "functional_profile",
    "gene_expression",
    "genome",
    "mag",
    "metabolite",
    "metabolomic",
    "metagenome",
    "model",
    "otu_table",
    "pathway",
    "phenotype",
    "profile",
    "protein",
    "rate",
    "taxonomic_profile",
    "transcript",
)

NON_SAMPLE_VALUE_TYPES = {"ARRAY", "OBJECT"}

SAMPLE_METADATA_ROLES = {
    "COVARIATE",
    "DATE_TIME_VARIABLE",
    "GROUPING",
    "IDENTIFIER",
    "SPATIAL_INDEX",
    "STUDY_DESIGN_CONTROLLED_VARIABLE",
    "STUDY_DESIGN_INDEPENDENT_VARIABLE",
}

# Common MIxS slots as they are typically represented on NMDC biosamples.
# This is only a validation hint for this catalog; term ID/label validation is
# still handled by linkml-term-validator.
MIXS_TO_NMDC_FIELD_HINTS = {
    "MIXS:0000008": {"experimental_factor"},
    "MIXS:0000009": {"lat_lon"},
    "MIXS:0000010": {"geo_loc_name"},
    "MIXS:0000011": {"collection_date"},
    "MIXS:0000012": {"env_broad_scale"},
    "MIXS:0000013": {"env_local_scale"},
    "MIXS:0000014": {"env_medium"},
    "MIXS:0000018": {"depth"},
    "MIXS:0000093": {"elev"},
    "MIXS:0000100": {"humidity"},
    "MIXS:0000102": {"tot_nitro"},
    "MIXS:0000185": {"water_content"},
    "MIXS:0000248": {"host_common_name"},
    "MIXS:0000250": {"host_taxid"},
    "MIXS:0000251": {"host_life_stage"},
    "MIXS:0000255": {"host_age"},
    "MIXS:0000257": {"host_dry_mass"},
    "MIXS:0000264": {"host_height"},
    "MIXS:0000310": {"carb_nitro_ratio"},
    "MIXS:0000312": {"cur_vegetation"},
    "MIXS:0000322": {"sieving"},
    "MIXS:0000425": {"nitrate", "nitrate_nitrogen"},
    "MIXS:0000426": {"nitrite", "nitrite_nitrogen"},
    "MIXS:0000427": {"ammonium", "ammonium_nitrogen"},
    "MIXS:0000430": {"potassium"},
    "MIXS:0000431": {"magnesium"},
    "MIXS:0000432": {"calcium"},
    "MIXS:0000365": {"host_genotype"},
    "MIXS:0000525": {"tot_carb"},
    "MIXS:0000530": {"tot_nitro_content"},
    "MIXS:0000556": {"fertilizer_regm", "fertilizer_regimen"},
    "MIXS:0000591": {"watering_regm", "watering_regimen"},
    "MIXS:0000639": {"agrochem_addition"},
    "MIXS:0000725": {"photon_flux"},
    "MIXS:0000751": {"chem_administration", "chemical_administration"},
    "MIXS:0000754": {"perturbation"},
    "MIXS:0000757": {"wind_direction"},
    "MIXS:0000829": {"season"},
    "MIXS:0001001": {"ph"},
    "MIXS:0001038": {"biotic_regm"},
    "MIXS:0001041": {"cult_root_med"},
    "MIXS:0001043": {"growth_facil"},
    "MIXS:0001057": {"plant_growth_med", "plant_growth_medium"},
    "MIXS:0001060": {"plant_struc"},
    "MIXS:0001107": {"samp_name"},
    "MIXS:0001163": {"soil_temp", "soil_temperature"},
    "MIXS:0001320": {"samp_taxon_id"},
}


@dataclass(frozen=True)
class StudyContext:
    """Catalog context for a study with an NMDC study identifier."""

    nmdc_study_id: str
    study_name: str
    program_id: str | None
    program_name: str | None
    study: Mapping[str, Any]


@dataclass(frozen=True)
class CatalogVariable:
    """Variable metadata needed for sample attribute validation."""

    name: str
    source_field_names: tuple[str, ...]
    roles: tuple[str, ...]
    value_type: str | None
    mixs_terms: tuple[Mapping[str, Any], ...]


@dataclass(frozen=True)
class SampleAttributeSet:
    """Distinct attributes found on NMDC biosamples for a study."""

    nmdc_study_id: str
    sample_count: int
    attributes: frozenset[str]


@dataclass(frozen=True)
class MissingVariableMatch:
    """A catalogued variable that looks sample-like but has no NMDC sample match."""

    variable_name: str
    source_field_names: tuple[str, ...]
    mixs_term_ids: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "variable_name": self.variable_name,
            "source_field_names": list(self.source_field_names),
            "mixs_term_ids": list(self.mixs_term_ids),
        }


@dataclass(frozen=True)
class StudyAttributeValidation:
    """Validation result for one NMDC study."""

    nmdc_study_id: str
    study_name: str
    program_id: str | None
    program_name: str | None
    sample_count: int
    sample_attributes: frozenset[str]
    matched_sample_attributes: frozenset[str]
    matched_source_fields: frozenset[str]
    matched_by_mixs: frozenset[str]
    admin_sample_attributes: frozenset[str]
    uncovered_sample_attributes: frozenset[str]
    variables_without_sample_attribute: tuple[MissingVariableMatch, ...]

    @property
    def has_strict_errors(self) -> bool:
        return self.sample_count == 0 or bool(self.uncovered_sample_attributes)

    def as_dict(self) -> dict[str, Any]:
        return {
            "nmdc_study_id": self.nmdc_study_id,
            "study_name": self.study_name,
            "program_id": self.program_id,
            "program_name": self.program_name,
            "sample_count": self.sample_count,
            "sample_attributes": sorted(self.sample_attributes),
            "matched_sample_attributes": sorted(self.matched_sample_attributes),
            "matched_source_fields": sorted(self.matched_source_fields),
            "matched_by_mixs": sorted(self.matched_by_mixs),
            "admin_sample_attributes": sorted(self.admin_sample_attributes),
            "uncovered_sample_attributes": sorted(self.uncovered_sample_attributes),
            "variables_without_sample_attribute": [
                item.as_dict() for item in self.variables_without_sample_attribute
            ],
        }


def normalize_field_name(value: str) -> str:
    """Normalize a source label or NMDC key for conservative matching."""

    normalized = re.sub(r"[^0-9A-Za-z]+", "_", value.strip().lower())
    return re.sub(r"_+", "_", normalized).strip("_")


def _attribute_lookup(attributes: set[str] | frozenset[str]) -> dict[str, set[str]]:
    lookup: dict[str, set[str]] = {}
    for attribute in attributes:
        lookup.setdefault(normalize_field_name(attribute), set()).add(attribute)
    return lookup


def _matching_attributes(keys: Sequence[str], attributes: set[str] | frozenset[str]) -> set[str]:
    lookup = _attribute_lookup(attributes)
    matches: set[str] = set()
    for key in keys:
        matches.update(lookup.get(normalize_field_name(key), set()))
    return matches


def load_database(path: Path) -> Mapping[str, Any]:
    with path.open() as stream:
        data = yaml.safe_load(stream)
    if not isinstance(data, Mapping):
        msg = f"Expected mapping at database root: {path}"
        raise ValueError(msg)
    _overlay_index_variables(data, path)
    return data


def _overlay_index_variables(data: Mapping[str, Any], db_path: Path) -> None:
    """Source study variables from schemas/variable-index.yaml (profiles + SSSOM) when present,
    so this validator works after the inline db.variables catalog is dropped (single Source of
    Truth). Studies absent from the index keep whatever inline variables they have."""
    index_path = db_path.parent.parent / "schemas" / "variable-index.yaml"
    if not index_path.exists():
        return
    studies_idx = (yaml.safe_load(index_path.read_text()) or {}).get("studies") or {}
    for collection_key in PROGRAM_COLLECTION_KEYS:
        for program in data.get(collection_key) or []:
            for study in program.get("studies") or []:
                sid = study.get("nmdc_study_id")
                key = sid.split(":")[-1] if sid else None
                if key and key in studies_idx:
                    study["variables"] = studies_idx[key]["variables"]


def iter_nmdc_studies(
    database: Mapping[str, Any], selected_study_ids: set[str] | None = None
) -> list[StudyContext]:
    """Find studies in the catalog that have an NMDC study ID."""

    contexts: list[StudyContext] = []
    for collection_key in PROGRAM_COLLECTION_KEYS:
        for program in database.get(collection_key) or []:
            if not isinstance(program, Mapping):
                continue
            for study in program.get("studies") or []:
                if not isinstance(study, Mapping):
                    continue
                nmdc_study_id = study.get("nmdc_study_id")
                if not nmdc_study_id:
                    continue
                if selected_study_ids and nmdc_study_id not in selected_study_ids:
                    continue
                contexts.append(
                    StudyContext(
                        nmdc_study_id=nmdc_study_id,
                        study_name=str(study.get("name") or ""),
                        program_id=program.get("id"),
                        program_name=program.get("name"),
                        study=study,
                    )
                )
    return contexts


def _iter_variable_dicts(study: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    variables: list[Mapping[str, Any]] = []
    for variable in study.get("variables") or []:
        if isinstance(variable, Mapping):
            variables.append(variable)
    for dataset in study.get("datasets") or []:
        if not isinstance(dataset, Mapping):
            continue
        for variable in dataset.get("variables") or []:
            if isinstance(variable, Mapping):
                variables.append(variable)
    return variables


def catalog_variables(study: Mapping[str, Any]) -> list[CatalogVariable]:
    """Collect variable records from a study and nested study datasets."""

    variables: list[CatalogVariable] = []
    for variable in _iter_variable_dicts(study):
        variables.append(
            CatalogVariable(
                name=str(variable.get("name") or ""),
                source_field_names=tuple(str(v) for v in variable.get("source_field_names") or []),
                roles=tuple(str(v) for v in variable.get("roles") or []),
                value_type=variable.get("value_type"),
                mixs_terms=tuple(v for v in variable.get("mixs_terms") or [] if isinstance(v, Mapping)),
            )
        )
    return variables


def mixs_field_hints(variable: CatalogVariable) -> set[str]:
    """Return NMDC biosample field hints implied by a variable's MIxS mappings."""

    hints: set[str] = set()
    for term in variable.mixs_terms:
        term_id = term.get("id")
        if term_id in MIXS_TO_NMDC_FIELD_HINTS:
            hints.update(MIXS_TO_NMDC_FIELD_HINTS[str(term_id)])
        label = term.get("label")
        if label:
            hints.add(str(label))
    return hints


def is_probably_non_sample_variable(variable: CatalogVariable) -> bool:
    """Identify variables that are likely omics results, derived values, or assays."""

    source_fields = " ".join(variable.source_field_names).lower()
    if variable.value_type in NON_SAMPLE_VALUE_TYPES:
        return True
    if any(pattern in source_fields for pattern in NON_SAMPLE_SOURCE_FIELD_PATTERNS):
        return True
    return False


def is_sample_metadata_candidate(variable: CatalogVariable) -> bool:
    """Return true when a variable is expected to correspond to sample metadata."""

    if is_probably_non_sample_variable(variable):
        return False
    if variable.mixs_terms:
        return True
    if set(variable.roles) & SAMPLE_METADATA_ROLES:
        return True
    return False


def fetch_nmdc_biosample_attributes(
    nmdc_study_id: str,
    *,
    session: requests.Session | None = None,
    api_base: str = NMDC_API_BASE,
    page_size: int = DEFAULT_PAGE_SIZE,
    max_pages: int | None = None,
) -> SampleAttributeSet:
    """Fetch NMDC biosamples for a study and union their top-level attribute keys."""

    http = session or requests.Session()
    url = f"{api_base.rstrip('/')}/biosample_set"
    params: dict[str, Any] | None = {
        "filter": json.dumps({"associated_studies": nmdc_study_id}),
        "max_page_size": page_size,
    }
    attributes: set[str] = set()
    sample_count = 0
    page_count = 0

    while True:
        page_count += 1
        response = http.get(url, params=params, timeout=60)
        response.raise_for_status()
        payload = response.json()
        resources = payload.get("resources") or []
        for resource in resources:
            if not isinstance(resource, Mapping):
                continue
            sample_count += 1
            attributes.update(str(key) for key in resource.keys())

        if max_pages is not None and page_count >= max_pages:
            break

        next_page_token = payload.get("next_page_token")
        if not next_page_token:
            break
        params = {
            "filter": json.dumps({"associated_studies": nmdc_study_id}),
            "max_page_size": page_size,
            "page_token": next_page_token,
        }

    return SampleAttributeSet(
        nmdc_study_id=nmdc_study_id,
        sample_count=sample_count,
        attributes=frozenset(attributes),
    )


def validate_study_sample_attributes(
    study_context: StudyContext, sample_attributes: SampleAttributeSet
) -> StudyAttributeValidation:
    """Compare catalogued variables to distinct NMDC biosample attributes."""

    variables = catalog_variables(study_context.study)
    all_attributes = set(sample_attributes.attributes)
    matched_sample_attributes: set[str] = set()
    matched_source_fields: set[str] = set()
    matched_by_mixs: set[str] = set()
    missing_variables: list[MissingVariableMatch] = []

    for variable in variables:
        source_matches = _matching_attributes(variable.source_field_names, all_attributes)
        mixs_matches = _matching_attributes(tuple(mixs_field_hints(variable)), all_attributes)
        matched_sample_attributes.update(source_matches)
        matched_sample_attributes.update(mixs_matches)
        if source_matches:
            matched_source_fields.update(
                field
                for field in variable.source_field_names
                if _matching_attributes((field,), all_attributes)
            )
        if mixs_matches:
            matched_by_mixs.update(mixs_matches)
        if (
            is_sample_metadata_candidate(variable)
            and not source_matches
            and not mixs_matches
        ):
            missing_variables.append(
                MissingVariableMatch(
                    variable_name=variable.name,
                    source_field_names=variable.source_field_names,
                    mixs_term_ids=tuple(
                        str(term["id"]) for term in variable.mixs_terms if term.get("id")
                    ),
                )
            )

    admin_attributes = all_attributes & ADMIN_SAMPLE_ATTRIBUTES
    uncovered = all_attributes - matched_sample_attributes - admin_attributes
    return StudyAttributeValidation(
        nmdc_study_id=study_context.nmdc_study_id,
        study_name=study_context.study_name,
        program_id=study_context.program_id,
        program_name=study_context.program_name,
        sample_count=sample_attributes.sample_count,
        sample_attributes=frozenset(all_attributes),
        matched_sample_attributes=frozenset(matched_sample_attributes),
        matched_source_fields=frozenset(matched_source_fields),
        matched_by_mixs=frozenset(matched_by_mixs),
        admin_sample_attributes=frozenset(admin_attributes),
        uncovered_sample_attributes=frozenset(uncovered),
        variables_without_sample_attribute=tuple(missing_variables),
    )


def validate_database(
    database: Mapping[str, Any],
    *,
    study_ids: set[str] | None = None,
    session: requests.Session | None = None,
    api_base: str = NMDC_API_BASE,
    page_size: int = DEFAULT_PAGE_SIZE,
    max_pages: int | None = None,
) -> list[StudyAttributeValidation]:
    """Validate all selected NMDC studies in a catalog database."""

    results: list[StudyAttributeValidation] = []
    for study_context in iter_nmdc_studies(database, study_ids):
        attributes = fetch_nmdc_biosample_attributes(
            study_context.nmdc_study_id,
            session=session,
            api_base=api_base,
            page_size=page_size,
            max_pages=max_pages,
        )
        results.append(validate_study_sample_attributes(study_context, attributes))
    return results


def _format_list(values: Sequence[str], max_items: int = 20) -> str:
    if not values:
        return "none"
    displayed = list(values[:max_items])
    suffix = "" if len(values) <= max_items else f" ... (+{len(values) - max_items} more)"
    return ", ".join(displayed) + suffix


def print_text_report(results: Sequence[StudyAttributeValidation], *, show_attributes: bool) -> None:
    for result in results:
        print(f"{result.nmdc_study_id} - {result.study_name}")
        print(f"  samples: {result.sample_count}")
        print(f"  distinct sample attributes: {len(result.sample_attributes)}")
        print(f"  catalog-covered sample attributes: {len(result.matched_sample_attributes)}")
        if result.matched_by_mixs:
            print(f"  matched via MIxS hints: {_format_list(sorted(result.matched_by_mixs), 12)}")
        if show_attributes:
            print(f"  sample attributes: {_format_list(sorted(result.sample_attributes), 80)}")
        if result.uncovered_sample_attributes:
            print(
                "  uncovered sample attributes: "
                f"{_format_list(sorted(result.uncovered_sample_attributes), 30)}"
            )
        if result.variables_without_sample_attribute:
            print("  sample-like variables without NMDC attribute match:")
            for variable in result.variables_without_sample_attribute[:10]:
                source_fields = _format_list(sorted(variable.source_field_names), 8)
                mixs_ids = _format_list(sorted(variable.mixs_term_ids), 8)
                print(f"    - {variable.variable_name} (source: {source_fields}; MIxS: {mixs_ids})")
            remaining = len(result.variables_without_sample_attribute) - 10
            if remaining > 0:
                print(f"    ... (+{remaining} more)")
        print()


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch NMDC biosamples for catalogued studies, union their sample "
            "attributes, and compare those attributes to catalogued variables."
        )
    )
    parser.add_argument(
        "db_path",
        nargs="?",
        default="db/sfas-brcs.yaml",
        type=Path,
        help="Path to the YAML ResearchProgramCollection database.",
    )
    parser.add_argument(
        "--study-id",
        action="append",
        dest="study_ids",
        help="NMDC study ID to validate. May be provided more than once.",
    )
    parser.add_argument("--api-base", default=NMDC_API_BASE, help="Base NMDC schema API URL.")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE)
    parser.add_argument("--max-pages", type=int, help="Limit pages fetched per study.")
    parser.add_argument(
        "--show-attributes",
        action="store_true",
        help="Print the full distinct NMDC sample attribute list for each study.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if true NMDC sample attributes are not represented in catalog variables.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    database = load_database(args.db_path)
    study_ids = set(args.study_ids) if args.study_ids else None
    results = validate_database(
        database,
        study_ids=study_ids,
        api_base=args.api_base,
        page_size=args.page_size,
        max_pages=args.max_pages,
    )

    if study_ids and len(results) != len(study_ids):
        found_ids = {result.nmdc_study_id for result in results}
        missing_ids = sorted(study_ids - found_ids)
        print(f"Study ID not found in catalog: {', '.join(missing_ids)}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps([result.as_dict() for result in results], indent=2))
    else:
        print_text_report(results, show_attributes=args.show_attributes)

    if args.strict and any(result.has_strict_errors for result in results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
