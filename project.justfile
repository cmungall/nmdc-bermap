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

# Generate interactive HTML browser for the database
gen-browser:
  uv run python scripts/generate_html_browser.py

# Fetch all BRC datasets from API and save as individual YAML files
fetch-brc-datasets:
  uv run python src/nmdc_sfas_brcs/scripts/fetch_brc_datasets.py --summary

# Fetch BRC datasets for a specific center (GLBRC, JBEI, CABBI, CBI)
fetch-brc-datasets-center CENTER:
  uv run python src/nmdc_sfas_brcs/scripts/fetch_brc_datasets.py --center {{CENTER}} --summary

# Generate interactive association chord diagrams (keyword-keyword, datatype-datatype, keyword-datatype)
gen-associations:
  uv run python scripts/generate_association_viz.py
