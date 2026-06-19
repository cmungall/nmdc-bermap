# sty-11-kfvmk798 — Data quality / cross-source audit

**Study:** Chronic drought differentially alters the belowground microbiome of drought tolerant and drought susceptible genotypes of Populus trichocarpa
**NMDC:** `nmdc:sty-11-kfvmk798`
**NCBI BioProject:** PRJNA784967
**PI:** Melissa Cregger

Audit date: **2026-06-19**.

## Sample-count divergence

| Source | n biosamples |
|---|---:|
| NMDC ingest | 64 |
| NCBI BioProject (via nmdc-ingest-agent fetch) | 384 |
| bermap `sample_count` | (matches NMDC) |

**6× divergence** — NMDC has only 64 of the 384 NCBI samples for this BioProject. Reason not investigated; could be a filtered subset (specific genotypes / timepoints) or partial ingest. The 320 NMDC-missing samples are recoverable via the agentic ingest snapshot under `db/agentic_ingests/sty-11-kfvmk798/`.

## env_triad — partial mismatch

All 64 NMDC biosamples carry an identical triad:

| Slot | Term | Label | Issue |
|---|---|---|---|
| `env_broad_scale` | ENVO:01000177 | grassland biome | ⚠️ Boardman, Oregon site is described as common-garden poplar — could be argued either way; the original poplar habitat is temperate forest, but Boardman is an agricultural/cropland zone |
| `env_local_scale` | ENVO:00000011 | garden | ✓ correct — Boardman common garden plot |
| `env_medium` | ENVO:00005801 | rhizosphere | ⚠️ correct for rhizosphere samples; wrong for any root endosphere samples in the cohort |

The study description explicitly states samples were taken from **both rhizosphere AND root endosphere**, but env_medium is uniformly rhizosphere — repeats the flattening pattern seen in `sty-11-vh2hty57` and `sty-11-wbc14h22`.

## Treatment design in `other_treatment`

Uniquely for this study, the **irrigation treatment is stored as a semicolon-delimited string** in `other_treatment`:

```
other_treatment = 'host common name: poplar; irrigation: full_irrigation'
other_treatment = 'host common name: poplar; irrigation: reduced_irrigation'
```

The two host common name + irrigation regime values are encoded as key:value pairs in one field. Recoverable by parsing the semicolon-separated key:value structure. `experimental_factor_other` and `cur_vegetation_has_raw_value` are NULL.

## Per-variable diff

| Variable | NCBI BioSample | NMDC `biosample_set` | bermap profile slot | Status |
|---|---|---|---|---|
| Drought tolerance class (tolerant vs susceptible genotype) | (not yet inspected) | not surfaced as a structured field | not in profile | ❌ design factor invisible to NMDC |
| Irrigation regime (full vs reduced) | (not yet inspected) | embedded in `other_treatment` string | not in profile | ⚠️ stored unstructured |
| Compartment (rhizosphere vs root endosphere) | (not yet inspected) | flattened to rhizosphere in `env_medium` | bermap profile has `BelowgroundCompartmentEnum` with `root endosphere → GOLDPATH:5304`, `rhizosphere → ENVO:00005801` | ❌ NMDC flattens; bermap profile is more accurate |
| Host genotype | partially in `samp_name` | not surfaced as structured | not in profile | ❌ |

## Agent curation pass (2026-06-19)

Full `/ncbi-to-nmdc` workflow run against PRJNA784967. Outcomes:

| Slot | predicted | resolved_from_raw | resolved_at_pipeline | left_sentinel | validator_rejected |
|---|---:|---:|---:|---:|---:|
| `env_broad_scale` | 0 | **384** | 0 | 0 | 0 |
| `env_local_scale` | 0 | **384** | 0 | 0 | 0 |
| `env_medium` | **384** | 0 | 0 | 0 | 0 |

**Zero sentinels.** Submitter provided usable raw values for broad/local; agent lifted via §1a resolution. Medium predicted by decoding `isolation_source`:

- All 384 → `env_broad_scale = ENVO:01000221` (temperate woodland biome)
- All 384 → `env_local_scale = ENVO:00000011` (garden)
- env_medium split into three compartments:
  - **128 rhizosphere** (`ENVO:00005801`)
  - **128 root tissue** → `ENVO:01001121` (plant matter) — ENVO has no dedicated root-endosphere material term
  - **128 bulk soil** (`ENVO:00005802`)

This recovers the compartment distinction NMDC's parallel ingest flattens (NMDC's 64 samples are all `env_medium = rhizosphere`).

See [`../../db/agentic_ingests/sty-11-kfvmk798/`](../../db/agentic_ingests/sty-11-kfvmk798/) for the curated artifacts and detailed README.

## Open items

- 320 NCBI biosamples missing from NMDC ingest — worth understanding the filter criterion
- Drought tolerant vs susceptible Populus genotype groupings not in any structured field
- `other_treatment` key:value pair encoding is unusual; the bermap profile could expose this as separate `host_common_name` and `irrigation_regime` slots
- Root endosphere vs rhizosphere flattening in `env_medium`

## Known limitations of this audit

- Per-sample mapping between NMDC's 64 and NCBI's 384 not done
- NCBI custom attributes not yet enumerated for this study
- The samp_name format (`1016-1-14-3`) wasn't fully decoded
