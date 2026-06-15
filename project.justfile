## Add your own just recipes here. This is imported by the main justfile.

# Validate db/sfas-brcs.yaml against the schema
validate-db:
  uv run linkml-validate -s src/nmdc_sfas_brcs/schema/nmdc_sfas_brcs.yaml -C ResearchProgramCollection db/sfas-brcs.yaml

# Validate enum permissible value ontology mappings
validate-enums *ARGS:
  uv run python -m nmdc_sfas_brcs.validators.enum_evaluator src/nmdc_sfas_brcs/schema/nmdc_sfas_brcs.yaml {{ARGS}}

# Validate enum PVs with verbose output
validate-enums-verbose:
  uv run python -m nmdc_sfas_brcs.validators.enum_evaluator src/nmdc_sfas_brcs/schema/nmdc_sfas_brcs.yaml -v

# Validate enum PVs in strict mode (warnings become errors)
validate-enums-strict:
  uv run python -m nmdc_sfas_brcs.validators.enum_evaluator src/nmdc_sfas_brcs/schema/nmdc_sfas_brcs.yaml --strict

# Validate ontology term IDs and labels in schema/data using linkml-term-validator
validate-terms *ARGS:
  uv run linkml-term-validator validate-schema src/nmdc_sfas_brcs/schema/nmdc_sfas_brcs.yaml -c src/nmdc_sfas_brcs/validators/oak_config.yaml {{ARGS}}
  uv run linkml-term-validator validate-data db/sfas-brcs.yaml -s src/nmdc_sfas_brcs/schema/nmdc_sfas_brcs.yaml -t ResearchProgramCollection -c src/nmdc_sfas_brcs/validators/oak_config.yaml {{ARGS}}

# Inspect NMDC biosample attributes for a catalogued NMDC study
check-nmdc-sample-attributes STUDY_ID *ARGS:
  uv run python -m nmdc_sfas_brcs.validators.nmdc_sample_attribute_validator db/sfas-brcs.yaml --study-id {{STUDY_ID}} --show-attributes {{ARGS}}

# Validate catalogued sample-like variables against NMDC biosample attributes
validate-nmdc-sample-attributes *ARGS:
  uv run python -m nmdc_sfas_brcs.validators.nmdc_sample_attribute_validator db/sfas-brcs.yaml {{ARGS}}

# Strict NMDC sample attribute validation (fails on uncovered non-admin NMDC sample attributes)
validate-nmdc-sample-attributes-strict *ARGS:
  uv run python -m nmdc_sfas_brcs.validators.nmdc_sample_attribute_validator db/sfas-brcs.yaml --strict {{ARGS}}

# Convert database to TTL and merge with TBox OWL
gen-abox-tbox:
  -mkdir -p db/owl
  uv run linkml-convert -s src/nmdc_sfas_brcs/schema/nmdc_sfas_brcs.yaml -C ResearchProgramCollection -t ttl db/sfas-brcs.yaml -o db/owl/sfas-brcs-abox.ttl
  robot merge --input project/owl/nmdc_sfas_brcs.owl.ttl --input db/owl/sfas-brcs-abox.ttl --output db/owl/sfas-brcs-merged.owl.ttl

# Validate references in db/sfas-brcs.yaml (fetches and caches publication metadata)
validate-refs *ARGS:
  uv run linkml-reference-validator validate data db/sfas-brcs.yaml --schema src/nmdc_sfas_brcs/schema/nmdc_sfas_brcs.yaml {{ARGS}}

# Cache a specific reference (e.g., just cache-ref doi:10.1038/s41586-020-03127-1 or PMID:33505029)
cache-ref REF:
  uv run linkml-reference-validator cache reference {{REF}}

# Validate references with verbose output
validate-refs-verbose:
  uv run linkml-reference-validator validate data db/sfas-brcs.yaml --schema src/nmdc_sfas_brcs/schema/nmdc_sfas_brcs.yaml --verbose

# Build the intermediate variable index (profiles + SSSOM -> schemas/variable-index.yaml)
gen-variable-index:
  uv run python schemas/generate_variables.py --index

# Generate interactive HTML browser for the database (study variables sourced from the index)
gen-browser: gen-variable-index
  uv run python scripts/generate_html_browser.py

# Generate per-study/-site LinkML data-dictionary profiles (schemas/studies, schemas/sites)
gen-profiles:
  uv run python schemas/generate_profiles.py

# Validate the generated LinkML profiles (load, imports, range resolution)
validate-profiles:
  uv run python schemas/validate_profiles.py

# Vet the ontology CURIEs in profile enum permissible values (linkml-term-validator)
validate-profile-terms:
  #!/usr/bin/env bash
  set -euo pipefail
  for f in schemas/base.yaml $(grep -l 'meaning:' schemas/studies/*.yaml); do
    echo "== $f =="
    uv run linkml-term-validator validate-schema "$f" -c src/nmdc_sfas_brcs/validators/oak_config.yaml --strict
  done

# Vet the per-schema SSSOM mapping tables: object_label must match object_id's ontology label
validate-profile-mappings:
  #!/usr/bin/env bash
  set -euo pipefail
  files=$(find schemas -name '*.sssom.yaml' | sort)
  uv run linkml-term-validator validate-data $files -s schemas/sssom-profile.yaml -t MappingSet \
    -c src/nmdc_sfas_brcs/validators/oak_config.yaml --no-dynamic-enums --labels

# Reverse generator: reconstruct the variables catalog from profiles + SSSOM. --check proves
# round-trip identity against db/sfas-brcs.yaml (reverse(forward(variables)) == variables).
sync-variables *ARGS:
  uv run python schemas/generate_variables.py {{ARGS}}

# Fetch all BRC datasets from API and save as individual YAML files
fetch-brc-datasets:
  uv run python src/nmdc_sfas_brcs/scripts/fetch_brc_datasets.py --summary

# Fetch BRC datasets for a specific center (GLBRC, JBEI, CABBI, CBI)
fetch-brc-datasets-center CENTER:
  uv run python src/nmdc_sfas_brcs/scripts/fetch_brc_datasets.py --center {{CENTER}} --summary

# Generate interactive association chord diagrams (keyword-keyword, datatype-datatype, keyword-datatype)
gen-associations:
  uv run python scripts/generate_association_viz.py


sync:
  scp docs/browser.html cmungall@perlmutter.nersc.gov:/global/cfs/cdirs/m3408/www/nmdc-sfas-brcs/
  scp docs/variables.html docs/variable-index.yaml cmungall@perlmutter.nersc.gov:/global/cfs/cdirs/m3408/www/nmdc-sfas-brcs/
