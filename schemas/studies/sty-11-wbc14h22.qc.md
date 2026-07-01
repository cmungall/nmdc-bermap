# sty-11-wbc14h22 — Data quality / cross-source audit

**Study:** Switchgrass cropping systems affect soil carbon and nitrogen and microbial diversity and activity on marginal lands
**NMDC:** `nmdc:sty-11-wbc14h22`
**NCBI BioProjects:** `PRJNA733109`, `PRJNA733505`, `PRJNA733764`
**DOI:** [10.1186/s40793-023-00504-x](https://doi.org/10.1186/s40793-023-00504-x)
**PI:** Maren Friesen (GLBRC)

Companion to `sty-11-wbc14h22.yaml` (LinkML profile) and `sty-11-wbc14h22.sssom.yaml` (mappings).

Audit date: **2026-06-18**.

## Sample-count divergence

| Source | n biosamples | Notes |
|---|---:|---|
| NMDC ingest | 2,676 | all carry INSDC IDs |
| NCBI (3 BioProjects combined) | 2,676 | mirrors NMDC |
| bermap `sample_count` | 2,971 | **doesn't match either source** — likely from publication or earlier submission; need verification |

## Five vs six locations

Study description says "five locations in the Great Lakes Region." NMDC data has **six** distinct `geo_loc_name` values:

| `geo_loc_name_has_raw_value` | n |
|---|---:|
| USA: Michigan, Delton | 1,176 |
| USA: Michigan, Lake City | 744 |
| USA: Michigan, Escanaba | 216 |
| USA: Wisconsin, Rhinelander | 216 |
| USA: Wisconsin, Hancock | 180 |
| USA: Wisconsin, Oregon | 144 |

The Wisconsin Oregon site (144 samples) is the extra one. Possible explanations: a sub-site within one of the "five" locations, or one publication counted two sites as one. Worth resolving with the submitter.

## env_triad curation issues (multiple)

All 2,676 biosamples carry a uniform env triad in NMDC:

| Slot | NMDC asserts | NMDC label | Issue |
|---|---|---|---|
| `env_broad_scale` | `ENVO:01000221` | temperate woodland biome | ❌ wrong — these are cropland/grassland fields, not woodland. `ENVO:01000245` (cropland biome) or `ENVO:01000177` (grassland biome) would be more appropriate, with the value depending on plot type |
| `env_local_scale` | `ENVO:00000114` | agricultural field | ⚠️ correct for switchgrass plots (G5); wrong for restored prairie (G10) and historical-vegetation control (G11) |
| `env_medium` | `ENVO:00005749` | farm soil | ⚠️ correct for G5; wrong for G10/G11 — should be grassland soil [ENVO:00005774] or similar |

`cur_vegetation` breakdown shows the actual heterogeneity:

| `cur_vegetation_has_raw_value` / `experimental_factor_other` | n |
|---|---:|
| Switchgrass | 1,884 |
| Restored Prairie | 396 |
| Undisturbed Control | 396 |

NMDC flattened all three land-use classes — and across biome / local-scale / medium — to a single (and biome-wise incorrect) triad. Recoverable via `cur_vegetation_has_raw_value` or `experimental_factor_other`. **Same flattening pattern as sty-11-vh2hty57** (which flattens bulk vs rhizosphere to bulk soil).

## Redundant storage

`cur_vegetation_has_raw_value` and `experimental_factor_other` carry **identical values** across all 2,676 samples — both encode the same Switchgrass/Restored Prairie/Undisturbed Control trichotomy. Either is sufficient; profile slot `current_vegetation` is the MIxS-aligned choice.

## NCBI-side metadata is unusually thin

| NCBI custom attribute | n samples |
|---|---:|
| `LinkerPrimerSequence` | 2,676 |
| `Sequecing_run` (sic — missing 'n') | 2,676 |
| `BarcodeSequence` | 2,676 |
| `isolation_source` (harmonized) | 2,676 |
| `collection_date` (harmonized) | 2,676 |
| `lat_lon` (harmonized) | 2,676 |
| `geo_loc_name` (harmonized) | 2,676 |

**No experimental design metadata in NCBI** — no fertilization, no land use, no growing-season year, no plot, no replicate. This is the **inverse** of the sty-11-vh2hty57 pattern: there, NCBI had design factors and NMDC dropped them; here, NMDC has design factors and NCBI never received them.

Practical consequence: for this study, NMDC is the authoritative source for the experimental design. Re-ingesting from NCBI (e.g., via nmdc-ingest-agent) would lose nearly all metadata of interest.

The `Sequecing_run` typo is in the NCBI deposit itself, not the NMDC ingest. Minor but worth flagging upstream.

## Per-variable three-way diff (one biosample, representative)

| Variable | NCBI BioSample | NMDC `biosample_set` | bermap profile slot | Status |
|---|---|---|---|---|
| Land use / treatment | not surfaced | `cur_vegetation_has_raw_value` = `experimental_factor_other` = `Switchgrass` \| `Restored Prairie` \| `Undisturbed Control` | `current_vegetation`, `other_experimental_factor` (redundant) | ⚠️ NMDC carries it; NCBI does not |
| N fertilization regime | encoded in NCBI `description_title` for 864 samples (2016); only as `MMPRNT-NNNN` field ID for 1812 samples (2017+2018) | not surfaced | `nitrogen_treatment` → enum (was ungrounded; now grounded to GLBRC MLE +N/0N split-plot design) | ⚠️ recoverable from NCBI title or OSF supplement; not from NMDC |
| Growing season year | not surfaced as field; encoded in BioProject (PRJNA733109=2016, PRJNA733505=2017, PRJNA733764=2018) and `collection_date` | not surfaced as a separate field, but `collection_date` carries it | not in profile | ⚠️ recoverable from collection_date or BioProject |
| Plot / replicate | encoded in NCBI title (rep1-rep4) for 864 samples | not surfaced | not in profile | ❌ not surfaced anywhere structured for 1812 of 2676 |
| `env_medium` | `isolation_source = soil` (harmonized) | `farm soil [ENVO:00005749]` (all 2676) | `environmental_medium` → uriorcurie | ❌ NMDC mislabel for 792 samples |
| `geo_loc_name` | matches | 6 distinct values | `geographic_location_name` → string | ⚠️ description says 5 |
| Sequencing artifacts | `LinkerPrimerSequence`, `BarcodeSequence`, `Sequecing_run` | not stored | not in profile | ⚠️ NCBI-only |

## Recovered: this is the GLBRC Marginal Land Experiment (MLE)

After the initial audit, deeper investigation located the full design. This study is the **GLBRC Marginal Land Experiment** ([KBS LTER overview](https://lter.kbs.msu.edu/glbrc-marginal-land-experiment/)), established 2013 across six sites in Michigan and Wisconsin. Internally referenced as the MMPRNT cohort.

### Plot-type code legend (GLBRC MLE)

| Code | Treatment | In wbc14h22? |
|---|---|:---:|
| **G5** | switchgrass (Panicum virgatum cv. Cave-in-rock) | ✅ dominant (1884 samples = Switchgrass) |
| G6 | giant miscanthus | — |
| G7 | 5-species native grass mix | — |
| G8 | hybrid poplar | — |
| G9 | early successional community | — |
| **G10** | native prairie | ✅ (correlates with NMDC "Restored Prairie") |
| **G11** | no-change control (historical vegetation) | ✅ (correlates with NMDC "Undisturbed Control") |

The G5/G10/G11 codes used in the OSF data and NCBI titles correspond exactly to the three vegetation categories NMDC carries as `Switchgrass` / `Restored Prairie` / `Undisturbed Control`.

### Site code legend

| Code | Resolved by NMDC `geo_loc_name` |
|---|---|
| LUX | (Lux Arbor) — appears as `USA: Michigan, Delton` |
| LC | (Lake City) — `USA: Michigan, Lake City` |
| ESC | (Escanaba) — `USA: Michigan, Escanaba` |
| RHN | (Rhinelander) — `USA: Wisconsin, Rhinelander` |
| HAN | (Hancock) — `USA: Wisconsin, Hancock` |
| — | `USA: Wisconsin, Oregon` (sixth NMDC site; not in 2018 OSF table — possibly different site code in 2016/17 or absent from the publication subset) |

### N fertilization design — binary split-plot

Split-plot treatment initiated 2014–2016 to compare:
- **Fert (+N)** — nitrogen-amended
- **Unfert (0N)** — unfertilized control

Balanced 50/50 across all cropping systems and sites (verified: 505 Fert vs 505 Unfert in 2018 bacterial subset). The exact kg N/ha rate isn't published on the LTER summary page but lives in the [KBS GLBRC sustainability data portal](https://data.sustainability.glbrc.org/) (Soil Properties — Marginal Land Experiment dataset 132). For the bermap profile, the binary Fert/Unfert categorization is sufficient.

The bermap `nitrogen_treatment` enum's `low nitrogen` / `high nitrogen` levels are semantically misleading — the actual design is `Unfert` (0 N) vs `Fert` (+N at one rate), not low vs high N. Should be renamed.

### Where the design metadata actually lives

Three external sources carry the design info NMDC and NCBI structured fields don't:

1. **NCBI `description_title`** field — for the 864 2016 samples (BioProject PRJNA733109), the title encodes everything as `<seq_round>_<MMDDYY>_MMPRNT_<siteID>_<plotType>_rep<n>_<Fert|Unfert>_pseudo<n>`. For the 1,812 2017+2018 samples, the title is only `MMPRNT-<field_id>` and the design lives elsewhere.
2. **OSF supplementary data**: https://osf.io/5vw9c/ — Bell-Dereske et al. 2023 deposit. The `Publish_data` folder contains:
   - `MMPRNT_2018.metadata_mapp_coverage.csv` — 870 rows × 73 columns, full design + plant/soil/weather covariates
   - `metadata_GLBRC018_OTU_bact_MMPRNT_mock_bact_rar.csv` — bacterial sample metadata with FertStatus, plotType, siteID, plotRep mapping
3. **Primary publication**: [Bell-Dereske et al. 2023](https://doi.org/10.1186/s40793-023-00504-x) (Environmental Microbiome 18:50) — covers the 2018 BioProject. The 2016 and 2017 BioProjects may belong to earlier/companion publications.
4. **Code & figures**: [Zenodo 7307179](https://doi.org/10.5281/zenodo.7307179)
5. **GLBRC sustainability data portal**: https://data.sustainability.glbrc.org/datasets/132 (Soil Properties — Marginal Land Experiment) — for exact N application rate.

### MMPRNT acronym

"MMPRNT" appears throughout sample names and OSF files but isn't defined in the LTER summary page; likely an internal cohort/protocol acronym for the marginal-lands microbiome sampling effort.

## `nmdc-ingest-agent` re-ingest (2026-06-18)

Ran [`nmdc-ingest-agent`](https://github.com/microbiomedata/nmdc-ingest-agent) against all three BioProjects (placeholder IDs, no --mint-real-ids):

```bash
uv run nmdc-ingest-ncbi PRJNA733109 --out /tmp/wbc_ingest/PRJNA733109.json   # 873 biosamples
uv run nmdc-ingest-ncbi PRJNA733505 --out /tmp/wbc_ingest/PRJNA733505.json   # 978 biosamples
uv run nmdc-ingest-ncbi PRJNA733764 --out /tmp/wbc_ingest/PRJNA733764.json   # 886 biosamples
```

### Sample-count divergence resolved

| Source | n biosamples |
|---|---:|
| Ingest-agent (3 BPs combined) | 2,737 |
| Existing NMDC ingest | 2,676 |
| bermap `sample_count` | 2,971 |

The 61-sample gap between agent and NMDC is fully accounted for by samples NMDC dropped:
- 16 ZymoBiomics mock community standards (e.g. `ZymoMock_B`, `ZymoBiomics Microbial DNA standard r20170912B`)
- Several technical re-runs (e.g. `2_071117_MMPRNT_LC_G5_composite_Unfert_r20170902`, `r20170912A`, `r20170912B` — same field plot resequenced)
- A handful of MMPRNT-NNNN field samples (e.g. `MMPRNT-LCG514`)

All 2,676 NMDC samples have a match in the agent output; the inverse is not true. The bermap `sample_count = 2,971` matches neither — likely from publication or an earlier deposit.

### What the agent preserves vs. what existing NMDC carries

| Field | Existing NMDC | Ingest-agent (raw) |
|---|---|---|
| `name` | `A1`, `A10`, `AA12` (just sequential codes) | full NCBI title preserved → `1_071916_MMPRNT_HAN_G10_rep3_Unfert_pseudo1` for the 864 2016 samples |
| `samp_name` | same as `name` (sequential codes) | NCBI primary name (`T19`, `ZymoMockB`, etc.) — different again |
| `env_broad_scale` | `ENVO:01000221` (temperate woodland biome — wrong) | `ENVO:00000000` sentinel — pipeline correctly refuses to guess |
| `env_local_scale` | `ENVO:00000114` (agricultural field) | `ENVO:00000000` sentinel |
| `env_medium` | `ENVO:00005749` (farm soil) | `ENVO:00000000` sentinel |
| `samp_taxon_id` | (not stored) | `NCBITaxon:410658` (soil metagenome) — added |
| `lat_lon` | string pair | numeric `GeolocationValue` — improved structure |
| `experimental_factor_other` | `Switchgrass`/`Restored Prairie`/`Undisturbed Control` | not extracted |
| FertStatus / plotType / siteID / rep | not extracted | **structured title preserved in `name`**, ready for skill-based parsing |

### What this run did NOT do

The ingest-agent CLI is the **deterministic** step. The full workflow requires running the skills (`/ncbi-to-nmdc`, then `nmdc-env-triad`, `nmdc-taxon-resolution`) to:
1. Resolve the env-triad sentinels (`ENVO:00000000`) — 2,619 + 2,934 + 2,658 = 8,211 (slot, biosample) pairs across the three BPs need curation
2. Parse the structured title into discrete design factors (siteID, plotType, FertStatus, plotRep)
3. Cross-reference the MMPRNT-NNNN field IDs against the OSF supplementary metadata for the 2017+2018 samples

Curation sidecars produced (one per BioProject) carry the inputs and skeleton report rows. For an analyst wanting the design data today, joining the agent output's `name` field against a regex parser + the OSF `MMPRNT_2018.metadata_mapp_coverage.csv` table is sufficient.

### Files

The deterministic step's intermediate output lived in `/tmp/wbc_ingest/`. After the agent curation pass (next section), the curated artifacts are committed to bermap at [`db/agentic_ingests/sty-11-wbc14h22/`](../../db/agentic_ingests/sty-11-wbc14h22/) — see that directory's README for file-by-file inventory and regen recipe.

## Known limitations of this audit

- The exact +N application rate (kg N/ha) isn't recorded in the data we inspected; the [GLBRC sustainability portal](https://data.sustainability.glbrc.org/datasets/132) likely has it.
- The 6-vs-5 location discrepancy: NMDC's 6 sites include "Wisconsin, Oregon" which doesn't appear in the OSF 2018 table. May be a site that was sampled in 2016/17 but dropped by 2018, or a site code mismatch.
- Only the 2018 bacterial metadata was downloaded; 2017 and 2016 batch metadata likely exist in companion repositories (or earlier OSF folders).
- The publication is paywalled by the redirect chain (DOI → BMC → Springer 303); read directly from OSF / Zenodo rather than the publisher landing page.

## Agent curation pass (2026-06-18)

A follow-up run executed the `nmdc-env-triad` skill against the three ingest-agent JSON files in place. Plot-code (G5 / G10 / G11) parsed from the structured NCBI title for 2016 samples; 2017/2018 `MMPRNT-NNNN` samples cannot be plot-resolved without the OSF crosswalk, so honest sentinels were preserved.

### Per-slot outcome counts (rows from `_curation_report.json`)

| BioProject | Slot | predicted | resolved_from_raw | resolved_at_pipeline | left_sentinel | validator_rejected |
|---|---|---:|---:|---:|---:|---:|
| PRJNA733109 (2016, 873) | env_broad_scale | 870 | 0 | 0 | 3 | 0 |
| | env_local_scale | 870 | 0 | 0 | 3 | 0 |
| | env_medium | 870 | 0 | 0 | 3 | 0 |
| PRJNA733505 (2017, 978) | env_broad_scale | 8 | 0 | 0 | 970 | 0 |
| | env_local_scale | 8 | 0 | 0 | 970 | 0 |
| | env_medium | 974 | 0 | 0 | 4 | 0 |
| PRJNA733764 (2018, 886) | env_broad_scale | 6 | 0 | 0 | 880 | 0 |
| | env_local_scale | 6 | 0 | 0 | 880 | 0 |
| | env_medium | 876 | 0 | 0 | 10 | 0 |
| **Total** | | **3,622** | 0 | 0 | **3,123** | 0 |

### Improvements over the existing NMDC ingest

- **Broad scale corrected**: NMDC's uniform `ENVO:01000221` temperate woodland biome is replaced by `ENVO:01000245` cropland biome (G5 plots) or `ENVO:01000177` grassland biome (G10 / G11) where the plot is known. Sentinel where it is not.
- **Local scale corrected for G10 / G11**: `ENVO:00000260` prairie (G10) / `ENVO:00000106` grassland area (G11) instead of NMDC's uniform `ENVO:00000114` agricultural field. G5 plots keep agricultural field.
- **Medium corrected for G10 / G11**: `ENVO:00005750` grassland soil instead of NMDC's uniform `ENVO:00005749` farm soil. G5 plots keep farm soil.
- **2017 / 2018 MMPRNT-NNNN handled honestly**: rather than uniformly mislabeling 1,836 samples (as NMDC did), broad/local are left `ENVO:00000000` sentinel for the curator. Medium falls back to the generic `ENVO:00001998` soil (a valid ancestor of farm soil and grassland soil) anchored on the per-sample `isolation_source = "Switchgrass Soils"`.
- **Mock / kit / control standards** (Zymo, Freeze-*, CTRL-*, error-*) retained with all three slots `left_sentinel` — they aren't environmental samples.

### Open items

- **OSF crosswalk for 2017 / 2018**: clearing the 1,840-row broad/local-scale backlog requires joining `MMPRNT-NNNN` against the OSF `MMPRNT_2018.metadata_mapp_coverage.csv` + analogous 2017 file (per qc § Where the design metadata actually lives). Once crosswalked, the same G5/G10/G11 → triad map applies.
- **2018 root samples**: BioProject title mentions "Soil **and** root" but per-sample `isolation_source` is uniformly `Switchgrass Soils`. If a subset is actually root tissue, the `soil` medium prediction will need to be split.
- **MIxS soil-package valueset not enforced**: NCBI packages are `Metagenome.environmental.1.0`, not the soil package, so the soil-package allowed-term constraint was not applied. `nmdc-submission-schema` was not consulted.
- **Site code `ORG`** (72 samples in 2016) is not in the LUX/LC/ESC/HAN/RHN site list and could not be resolved to a `geo_loc_name`.

### Curated artifacts (committed to bermap)

Three sets of files, one per BioProject, at [`db/agentic_ingests/sty-11-wbc14h22/`](../../db/agentic_ingests/sty-11-wbc14h22/) (see that directory's [README](../../db/agentic_ingests/sty-11-wbc14h22/README.md) for file-by-file inventory and regen recipe):

- `PRJNA733109.nmdc.json` + `.curation_inputs.json` + `.curation_report.json`
- `PRJNA733505.nmdc.json` + `.curation_inputs.json` + `.curation_report.json`
- `PRJNA733764.nmdc.json` + `.curation_inputs.json` + `.curation_report.json`
- `curate.py` — the curation script the agent wrote

All three `*.nmdc.json` pass `nmdc_schema.Database` LinkML validation. IDs remain placeholders (`bsm-99-…`); a `--mint-real-ids` re-run is still required for ingest.
