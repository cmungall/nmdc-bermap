# sty-11-n7mtj961 — Data quality / cross-source audit

**Study:** Impact of modulating bioenergy traits on the sorghum microbiome under drought conditions
**NMDC:** `nmdc:sty-11-n7mtj961`
**NCBI BioProject:** PRJNA1205755
**PI:** Henrik Vibe Scheller

Audit date: **2026-06-19**.

## Massive sample-count divergence

| Source | n biosamples |
|---|---:|
| NMDC ingest | 16 |
| NCBI BioProject (via nmdc-ingest-agent fetch) | **683** |
| bermap `sample_count` | (matches NMDC) |

**~43× divergence.** This is the largest NMDC ↔ NCBI sample-count gap in the cohort. NMDC carries only 16 samples for this study; NCBI's BioProject PRJNA1205755 contains 683 deposited biosamples. Why the NMDC subset is so small wasn't investigated — could be a pilot batch, a specific sub-question, or an incomplete ingest.

If the full study is downstream-relevant, the 667 missing samples are now available via the agentic ingest snapshot under `db/agentic_ingests/sty-11-n7mtj961/`.

## env_triad — clean for the small NMDC subset

All 16 NMDC biosamples carry an identical triad:

| Slot | Term | Label |
|---|---|---|
| `env_broad_scale` | ENVO:01000245 | cropland biome ✓ |
| `env_local_scale` | ENVO:00005801 | rhizosphere ✓ |
| `env_medium` | ENVO:00001998 | soil ✓ |

This is the cleanest small-cohort triad in the audit. The Davis, CA field site is described as a sorghum field, which matches cropland biome; the samples are rhizosphere soil; using the generic `soil` for medium (rather than `farm soil` or `rhizosphere soil`) is a defensible curator choice.

## Site, host, factor

Per the study description:
- **Site**: Davis, California — sorghum field plots
- **Host**: Sorghum bicolor genotype 'Wheatland' (commercial grain variety)
- **Year**: 2022
- **Factor**: drought + modulated bioenergy traits

But in NMDC:
- `geo_loc_name = "USA: California, Davis"` ✓
- Host genotype, drought treatment, year — none surfaced as structured fields
- `other_treatment` / `experimental_factor_other` / `cur_vegetation` all NULL

Sample names follow `RHZA025`, `RHZA082`, `RHZA127`:
- `RHZ` = rhizosphere
- `A` = batch / cohort / location code
- numeric ID = sample within batch

## Sample-name divergence between NMDC and NCBI

The 16 NMDC sample names (`RHZAXXX`) are a specific subset; the 683 NCBI samples may include rhizosphere, root endosphere, leaf, and bulk soil compartments across multiple genotypes and timepoints. Worth investigating which 16 of the 683 NMDC chose to ingest.

## Agent curation pass (2026-06-19)

Full `/ncbi-to-nmdc` workflow run against PRJNA1205755 (the 683-sample NCBI deposit, vs NMDC's 16-sample subset). Outcomes:

| Slot | predicted | resolved_from_raw | resolved_at_pipeline | left_sentinel | validator_rejected |
|---|---:|---:|---:|---:|---:|
| `env_broad_scale` | 0 | **683** | 0 | 0 | 0 |
| `env_local_scale` | 0 | 287 | **396** | 0 | 0 |
| `env_medium` | 0 | 287 | **396** | 0 | 0 |

**Zero sentinels.** Submitter pre-embedded ENVO CURIEs in free-text env-triad fields; pipeline parsed them. Curator overrides corrected three anchor-failing values:

- `env_broad_scale`: 683× `ENVO:01001244 cropland ecosystem` (fails biome anchor) → `ENVO:01000245 cropland biome`
- `env_local_scale` for 287 Root samples: `ENVO:01001001 plant-associated environment` (fails anchor) → `ENVO:00005801 rhizosphere`
- `env_medium` for 287 Root samples: `ENVO:01001001` (fails anchor) → `ENVO:01001121 plant matter`

Final values:
- broad: cropland biome (683)
- local: rhizosphere (288 RHZ + 287 Root) + bulk soil (108 Soil/NPS)
- medium: rhizosphere (288) + plant matter (287) + soil (108)

Required a one-line patch to `nmdc-ingest-agent` (`_infer_analyte_category` returned `"metabarcode"` which isn't in NMDC's `NucleotideSequencingEnum`; corrected to `"amplicon_sequencing_assay"`).

See [`../../db/agentic_ingests/sty-11-n7mtj961/`](../../db/agentic_ingests/sty-11-n7mtj961/) for the curated artifacts and detailed README.

## Open items

- **Investigate the 16/683 ingest gap** — major audit finding. Why does NMDC have only 2.3% of the deposited BioProject?
- Host genotype (sorghum 'Wheatland'), drought treatment, sampling timepoints — none in structured NMDC fields
- bermap profile slot inventory not reviewed against the recovered NCBI data

## Known limitations of this audit

- Per-sample mapping between the 16 NMDC and the 683 NCBI samples not done
- NCBI custom attributes not enumerated to identify what design factors are deposited
- The 683 NCBI samples may span more diversity (compartments, timepoints, genotypes) than the NMDC subset suggests
