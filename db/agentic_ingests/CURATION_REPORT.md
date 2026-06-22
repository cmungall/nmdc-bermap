# Agentic curation pass — consolidated report (2026-06-20)

After the bulk deterministic ingest of 35 BioProjects (committed under each `<study-dir>/`), the `/ncbi-to-nmdc` agentic skill workflow was run across all 29 non-NMDC studies + the 5 NMDC-linked ones, organized into batches A/B/C/D plus the earlier NMDC pass. This file consolidates the per-batch outcome reports and cross-cutting findings.

Each `<study-dir>/<PRJNA>.nmdc.json` had its env triad committed in place where possible, with the corresponding `<study-dir>/<PRJNA>.curation_report.json` updated with per-(biosample, slot) outcomes, evidence, candidate alternatives, and validator status.

## Headline

| Batch | Studies | BioProjects | Biosamples | Wall time | Backlog (left_sentinel) | validator_rejected |
|---|---:|---:|---:|---:|---:|---:|
| **earlier (NMDC pass)** | 5 | 7 | 4,627 | ~25 min | ~3,200 (wbc14h22 MMPRNT-NNNN) | 175 (ev70y104 indoor) |
| **A** | 7 | 7 | 3,326 | ~18 min | 1,548 | 6 |
| **B** | 9 | 9 | 2,151 | ~17 min | 0 | 1,946 |
| **C** | 10 | 10 | 2,644 | ~18 min | 97 | ~1,400 |
| **D** | 7 | 7 | 1,500 | ~15 min | 794 | 106 |
| **Total** | 38 | 40 | 14,248 | ~1.5 h wall × 4 parallel sessions | ~5,640 | ~3,633 |

## Outcome categories — what each means

- **`predicted`** — agent inferred a value with cited per-sample evidence (§1b workflow). Committed.
- **`resolved_from_raw`** — submitter provided usable raw text; agent lifted to a CURIE (§1a workflow). Committed.
- **`resolved_at_pipeline`** — pipeline already committed a valid CURIE before the agent saw it. Kept.
- **`left_sentinel`** — agent honestly refused to commit (insufficient evidence, semantic ambiguity, ontology gap). `ENVO:00000000` remains.
- **`validator_rejected`** — pipeline-supplied or submitter-supplied CURIE failed strict anchor-class membership; agent surfaced the rejection with explanatory evidence. `ENVO:00000000` set with rationale.

Both `left_sentinel` and `validator_rejected` are **curator-follow-up backlog** — but they're the right kind of "I don't know" rather than confidently-wrong commitments.

## Cross-cutting findings

### 1. `nmdc-submission-schema` not importable in this env
Soil-package valueset constraint **NOT enforced** for any soil biosamples in this pass. Affects:
- batch-a: 1,829 rows (soil-package biosamples in switchgrass + seasonality_populus)
- batch-b: PRJNA726831, PRJNA385484, PRJNA384978
- batch-c: PRJNA862978, PRJNA561781, PRJNA1080623
- batch-d: PRJNA741261, PRJNA745191, PRJNA1156252

Predicted CURIEs were chosen from anchor-class descendants only. Once the package is installable, all these should re-validate against the soil valueset. Known gap.

### 2. `ENVO:01001001 plant-associated environment` — common submitter mistake
Fails all three MIxS anchor checks (biome, astronomical body part, env material). Observed in PRJNA1205755 (NMDC pass), PRJNA1002602/03, PRJNA933671 (batch-c). When seen, overridden with the appropriate compartment term. Worth a one-shot QC rule upstream in `nmdc-ingest-agent`.

### 3. No ENVO term for "phyllosphere" / "leaf endosphere" / "root endosphere"
As env_local_scale (astronomical body part anchor). Recurring fallback to `validator_rejected`. Real ontology hole. Examples:
- seasonality_populus: 1,454 root + leaf endosphere samples → left_sentinel
- populus_holobiont (PRJNA385484/PRJNA384978): 590 "plantation" → validator_rejected (plantation is under anthropogenic environment, not astronomical body part)
- populus_variovorax_syncom28: 7 root endosphere samples → validator_rejected
- sorghum/colleto in planta (PRJNA961726): 95 leaf interior → validator_rejected
- All compartment refusals across batch-c: > 700 rows
- Populus common gardens (PRJNA666202): 66 endosphere → left_sentinel

`ENVO:01001121 plant matter` is the workable **material** fallback per cross-batch guidance, but no MIxS-anchor-compliant **feature** exists for tissue interiors.

### 4. No ENVO term for "riparian zone" or "high elevation watersheds"
PRJNA726831 climate_driven_divergence: 539 env_broad_scale + env_local_scale rows → validator_rejected. "High elevation watersheds in the Rocky Mountains, USA" is a geographic phrase, not a biome. Closest hit `wetland ecosystem` rejected as semantically wrong.

### 5. Indoor / lab-microcosm / in-vitro studies have no MIxS env_triad fit
Cross-batch guideline: leave `validator_rejected` rather than guess. Affected:
- ev70y104 (NMDC pass): 175 broad-scale rejected
- batch-a: novosphingobium DAP-seq (1 sample × 3 slots), colletotrichum on PDA (1 × 3) = 6 rows
- batch-b: corynebacterial phage Microbe.1.0 (18 × 3 = 54 rows), sorghum/colleto in vitro PDA (4 × 3 = 12 rows)
- batch-c: sugarcane greenhouse (200 × 1 = 200), brachypodium Conviron (71 × 1 = 71)
- batch-d: e_coli_phage Microbe.1.0 (357 × 3 = 1,071 rows — single largest sentinel group)

These are correctly refused per env-triad skill Rule 4.

### 6. Pipeline anchor-check missing for submitter-supplied CURIEs
When NCBI BioSamples carry bare ENVO CURIEs in env_triad attribute strings, the pipeline copies them to `term.id` and sets `term.name == CURIE` (no resolution). Multiple submitter-supplied CURIEs fail anchor checks the pipeline doesn't run:
- `ENVO:01001244 cropland ecosystem` (PRJNA1205755) → fails biome anchor
- `ENVO:01001790 terrestrial ecosystem` (batch-c) → fails biome anchor
- `ENVO:00002259 agricultural soil` (batch-c) → not a biome
- `ENVO:01000352 field` (PRJNA1156252 KBS) → not a biome
- `BTO:0001181 endophyte` (batch-c) → not in ENVO at all

Recommended upstream fix: pre-commit anchor check in `mfd.py` / generic ENVO parsing path, with the curation report flagging anchor failures rather than silently passing through.

### 7. Duplicate dir: oak_ridge_groundwater + oak_ridge_sediment_and_groundwater
Both `oak_ridge_groundwater_100_well_survey_metagenomes/` and `oak_ridge_sediment_and_groundwater_metagenomes/` curate the same NCBI BioProject `PRJNA1001011` with the same 140 BioSamples. Confirm one should be retired in `db/sfas-brcs.yaml` before any real ingest.

### 7b. MAG-only BioProjects are deliberately empty in this ingest

`bioreactor_fermentation_microbiomes` contains 3 BioProjects (PRJNA1040840, PRJNA1159295, PRJNA768492) that produced 0 NMDC biosamples each. The first two have 164+ MIMAG (Metagenome-Assembled Genome) biosamples at NCBI; nmdc-ingest-agent deliberately excludes MAG-only biosamples because NMDC's `Biosample` class represents environmental samples, not computational assemblies. The third has no BioSample records at all. See [`bioreactor_fermentation_microbiomes/README.md`](bioreactor_fermentation_microbiomes/README.md) for the full explanation.

If MAG support is wanted in bermap, it would require a different ingestion path (MetagenomeAssembly / MagBin classes in NMDC) — not a bug in the current pipeline.

### 8. Host taxon resolution deferred
Per the curation skill scope, no edits attempted to `samp_taxon_id` or host fields. Pipeline-supplied values kept. The following unambiguous hosts could be lifted on a follow-up pass:
- NCBITaxon:183674 Miscanthus × giganteus (PRJNA601860)
- NCBITaxon:4577 Zea mays (PRJNA601860 Corn samples)
- NCBITaxon:3694 Populus trichocarpa (PRJNA784967, PRJNA666202)
- NCBITaxon:62336 Miscanthus (PRJNA561781, PRJNA745191)
- NCBITaxon:62337 Miscanthus sinensis, NCBITaxon:154761 M. floridulus (PRJNA561781)
- NCBITaxon:38727 Panicum virgatum (PRJNA1002602/03)
- NCBITaxon:4558 Sorghum bicolor (PRJNA1205755, PRJNA741261, PRJNA862978, PRJNA844896, PRJNA961726)
- NCBITaxon:15368 Brachypodium distachyon (PRJNA1120948)
- NCBITaxon:4546 Saccharum sp. (PRJNA892137)

## Per-batch reports

See the four batch reports in [`.curation_reports/`](.curation_reports/):
- [`batch-a_report.md`](.curation_reports/batch-a_report.md) — seasonality_populus, switchgrass, phage, east_fork_sediment, bacillus, novosphingobium, colletotrichum
- [`batch-b_report.md`](.curation_reports/batch-b_report.md) — soil_pore_space, populus_holobiont × 2, climate_divergence, corynebacterial, enigma_gw, populus_variovorax, sorghum_colleto × 2
- [`batch-c_report.md`](.curation_reports/batch-c_report.md) — sorghum_phyllosphere × 2, transgenic_switchgrass × 2, poplar_rhizo, native_miscanthus, sugarcane, brachypodium, plant_nitrifier, terpene_sorghum
- [`batch-d_report.md`](.curation_reports/batch-d_report.md) — e_coli_phage, sorghum_rhiz, lamps_miscanthus, cultivating_populus, oak_ridge × 2, kbs_mcse

## Validation status

All `*.nmdc.json` files validate against `nmdc_schema.Database`. IDs remain placeholders (shoulder `99`). Re-run with `--mint-real-ids` per study to promote.
