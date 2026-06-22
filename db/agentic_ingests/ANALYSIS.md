# Patterns across the agentic ingest pass

Systematic analysis across the 44 NMDC database JSONs in `db/agentic_ingests/` (36 study directories, 8 MIxS packages, ~14,250 biosamples). Findings concentrate on (a) cross-cutting patterns visible only at scale, (b) alignment between bermap-profile-curated variables and what the NCBI ingest actually carries.

Audit date: **2026-06-22**. Source data: per-(biosample, slot) outcomes from each `*.curation_report.json` and packages / attributes from `*.curation_inputs.json`.

## 1. Where the env-triad agent succeeded

Outcome distribution across **42,653 (slot, biosample) rows**:

| Outcome | env_broad_scale | env_local_scale | env_medium |
|---|---:|---:|---:|
| `predicted` (agent inferred, evidence-backed) | 5,647 (39.6%) | 4,574 (32.1%) | **9,404 (66.0%)** |
| `resolved_from_raw` (lifted submitter text) | 5,034 (35.3%) | 2,829 (19.9%) | 3,530 (24.8%) |
| `resolved_at_pipeline` (already committed) | 0 (0%) | 710 (5.0%) | 780 (5.5%) |
| `left_sentinel` (refused honestly) | 2,342 (16.4%) | **3,862 (27.1%)** | 510 (3.6%) |
| `validator_rejected` (anchor-check fail) | 1,225 (8.6%) | 2,273 (16.0%) | 24 (0.2%) |

**Key takeaway:** env_medium is by far the easiest slot to commit — 90% predicted or lifted, only 4% sentinel. env_local_scale is the hardest — 43% honest refusals because ENVO has no anchor-compliant features for plant tissue interiors, lab microcosms, riparian zones, or shorelines. env_broad_scale sits between the two; the agent could often infer a biome from study description / geo_loc_name even when the submitter didn't provide one.

## 2. The MIxS package is a strong predictor of curation outcome

| Package | n studies | rows | top outcome |
|---|---:|---:|---|
| `Metagenome.environmental.1.0` | 13 | 19,518 | **71.9% predicted** |
| `MIMARKS.survey.plant-associated.6.0` | 6 | 13,449 | **51.6% resolved_from_raw** |
| `MIMARKS.survey.soil.6.0` | 6 | 5,919 | 60.4% resolved_from_raw + **18.2% rejected** |
| `MIMS.me.plant-associated.6.0` | 1 | 1,566 | 83.9% predicted |
| `Microbe.1.0` | 5 | 1,158 | **93.5% sentinel** |
| `MIMS.me.miscellaneous.6.0` | 1 | 525 | 53% pipeline + 47% rejected |
| `MIMS.me.soil.6.0` | 1 | 318 | 67% pipeline + 33% rejected |
| `Plant.1.0` | 1 | 285 | 33% predicted + **66.7% rejected** |
| `MIGS.eu.plant-associated.6.0` | 1 | 3 | 100% rejected |

### Recurring patterns

1. **`Microbe.1.0` (lab cultures) → 93.5% sentinel**. Five studies (corynebacterial phage, sorghum/colleto in vitro, geochemical constraints, e_coli phage, novosphingobium DAP-seq) use this package — all are pure cultures, in-vitro assays, or DAP-seq epigenomics. MIxS env triad doesn't semantically apply. The agent's blanket-sentinel response is correct; this is **the right answer**, not a failure mode. **Recommendation**: tag these in bermap with a `sample_class: lab_isolate` and skip env-triad curation for them by default.

2. **`MIMARKS.survey.soil.6.0` (6 studies) → 18% validator_rejected**. Submitters of soil studies often provide ENVO CURIEs in env triad attribute strings that *fail the anchor check* — e.g., `ENVO:01001244 cropland ecosystem` (ecosystem, not biome), `ENVO:00002259 agricultural soil` (material, not biome), `ENVO:01001790 terrestrial ecosystem` (ecosystem). The pipeline propagates the bad value; the agent overturns it. **Recommendation**: add an anchor-class pre-check to `nmdc-ingest-agent`'s NCBI translator so submitter CURIEs get validated before they hit the database object.

3. **`Plant.1.0` and `MIGS.eu.plant-associated.6.0`** → near-total rejection. These are for plant tissue (leaves, roots in vitro) where ENVO has no env_local_scale term — see §4.

## 3. Bermap `nmdc_ingest_priority` correctly identifies "untreatable" BPs

The bermap `nmdc_ingest_priority: LOW` annotation appears on exactly one study cluster — `bioreactor_fermentation_microbiomes` (3 BPs). The reason:

- Both PRJNA1040840 (122 BS) and PRJNA1159295 (42 BS) deposit **MAGs** (Metagenome-Assembled Genomes) under the `MIMAG.miscellaneous.6.0` package
- `nmdc-ingest-agent` deliberately excludes MAG-only biosamples because the NMDC `Biosample` class is for environmental samples, not computational assemblies
- PRJNA768492 has no BioSamples in NCBI at all

**The LOW priority designation correctly predicted that these BPs are not amenable to the current NMDC ingest path.** MAG support would require a different code path (`MetagenomeAssembly` / `MagBin` classes).

| Priority | Total curation rows | predicted % | sentinel+rejected % |
|---|---:|---:|---:|
| HIGH | 23,664 | 44.8% | 23.6% |
| MEDIUM | 9,249 | 56.0% | 10.8% |
| LOW | 3 | — | 66.7% |
| (no priority set) | — | — | — |

HIGH and MEDIUM curate roughly equivalently — both succeed at lifting submitter values; HIGH has more sentinel-prone studies (Populus tissue compartments, indoor microcosms). LOW is the clean signal of "skip these for the current ingest path".

## 4. Bermap profiles are systematically misaligned with NCBI attribute names

**34 of 36 studies** with bermap profiles have **profile slot ↔ NCBI attribute mismatches** — either slots in the profile have aliases that never appear in any biosample, or attributes appear in the data that no slot covers.

### Recurring "unmapped" NCBI attribute names

These NCBI biosample attribute names appear across many studies but are not covered by any alias in the corresponding bermap profile:

| NCBI attribute | studies | Why it's unmapped |
|---|---:|---|
| `geo_loc_name` | 29 | bermap profiles use slot name `geographic_location_name`, alias `geo_loc_name` — but the alias is sometimes missing |
| `lat_lon` | 26 | bermap profiles use `latitude_and_longitude`, alias missing |
| `collection_date` | 25 | profile name matches, alias should be auto |
| `host` | 19 | no bermap slot for host taxon — a real gap, not just a naming issue |
| `isolation_source` | 18 | no bermap slot — NCBI carries this, bermap doesn't model it |
| `env_broad_scale`, `env_local_scale`, `env_medium` | 13–14 each | profiles use verbose names like `broad_scale_environmental_context` — the MIxS-canonical NCBI short names aren't in the aliases |
| `elev` | 7 | profile uses `elevation`; the `elev` alias isn't always set |
| `replicate` | 7 | bermap typically lacks a structured replicate slot |
| `depth` | 6 | profile uses `soil_sampling_depth`; alias missing |
| `strain` | 6 | no bermap slot |
| `sample_type` | 5 | no bermap slot |
| `treatment` | 4 | sometimes covered by `other_treatment` aliases, often not |

### Orphan slots (in profile, no NCBI attribute)

Common orphans across studies:
- `environmental_package`, `ecosystem`, `ecosystem_*`, `specific_ecosystem`, `growth_facility` — these are present in NMDC's `biosample_set` but **not as NCBI attribute names**. The bermap profile slots expect NMDC-side fields, not NCBI fields. (Most studies have parallel NMDC ingests with these fields populated; the agentic re-ingest from NCBI doesn't see them.)
- `*_community_composition` measured-outcome slots — these are dependent variables, not biosample attributes; they belong to data_generation outputs, not biosample metadata.
- `stand_age`, `nitrogen_fertilizer_rate`, `host_crop`, `soil_compartment` — bermap's **derived** slots that recover information from `samp_name`. No NCBI attribute by these names; the aliases match samp_name encoding hints, not biosample attribute keys.

### Recommendation

Add a one-time pass on `schemas/base.yaml` to populate the standard MIxS-short-name aliases on each shared slot:

```yaml
slots:
  collection_date:
    aliases: [collection_date]
  elevation:
    aliases: [elev]
  geo_loc_name:
    aliases: [geo_loc_name]
  lat_lon:
    aliases: [lat_lon]
  env_broad_scale:
    aliases: [env_broad_scale, broad_scale_environmental_context]
  env_local_scale:
    aliases: [env_local_scale, local_environmental_context]
  env_medium:
    aliases: [env_medium, environmental_medium]
  env_package:
    aliases: [env_package, environmental_package]
```

This alone would clear the unmapped-attribute warnings for ~70 of the recurring mismatches across the cohort.

Also, **bermap should add base slots for `host`, `isolation_source`, `replicate`, `depth`, `strain`** — these recur in ≥6 studies each but no bermap profile carries them.

## 5. Most-used ENVO terms (cohort consensus)

`env_broad_scale` (excluding sentinels):
- **`ENVO:01000245 cropland biome`** — 5,310 biosamples (the dominant biome — switchgrass / Miscanthus / sorghum / agricultural soils)
- `ENVO:01000202 temperate broadleaf forest biome` — 3,237 (poplar studies)
- `ENVO:01000174 forest biome` — 509 (Luquillo tropical soil)
- `ENVO:01000192 tropical grassland biome` — 466 (Native Miscanthus Taiwan)
- `ENVO:01000221 temperate woodland biome` — 384 (Populus drought Boardman — possibly mislabeled; defensible)
- `ENVO:01000177 grassland biome` — 288 (Angelo meadow)
- `ENVO:00000873 freshwater biome` — 288 (Oak Ridge groundwater × 2)

`env_local_scale` (excluding sentinels):
- `ENVO:00000114 agricultural field` — 2,891
- `ENVO:00005801 rhizosphere` — 1,661
- `ENVO:00001998 soil` — 691
- `ENVO:00005749 farm soil` — 648
- `ENVO:00000011 garden` — 450 (common gardens — poplar, Miscanthus)
- `ENVO:00000260 prairie` — 144 (sty-11-wbc14h22 G10/G11 plots)
- `ENVO:00000106 grassland area` — 144

`env_medium` (excluding sentinels):
- `ENVO:00001998 soil` — 5,287
- `ENVO:01001121 plant matter` — **3,728** (fallback for plant tissue endosphere — see §4)
- `ENVO:00002259 agricultural soil` — 1,162
- `ENVO:00005802 bulk soil` — 829
- `ENVO:00005801 rhizosphere` — 614
- `ENVO:00005749 farm soil` — 596

The repeated use of `ENVO:01001121 plant matter` (3,728 commits) is the agreed-upon fallback for plant tissue endosphere samples — a real ENVO term but explicitly chosen because the ontology has no more-specific "root endosphere material" / "leaf endosphere material" term.

## 6. Detected cohorts / duplicates / shared experimental designs

### Duplicate study directory

- `oak_ridge_groundwater_100_well_survey_metagenomes/` and `oak_ridge_sediment_and_groundwater_metagenomes/` curate the **same NCBI BioProject (`PRJNA1001011`, 140 BioSamples)**. The first 50 sample names match exactly (`EB271_05_03`, etc.). One bermap entry should be retired before any real ingest.

### Same-study split across two amplicon assays

These pairs are 16S + ITS (or similar) sequencing of the same physical samples:
- `populus_holobiont_niche_and_genotype_effects`: PRJNA384978 (290 BS) + PRJNA385484 (300 BS), `UPMTD*` prefix
- `sorghum_phyllosphere_microbiome`: PRJNA844896 (239 BS) + PRJNA862978 (306 BS)
- `transgenic_switchgrass_microbiome_effects`: PRJNA1002602 (198 BS) + PRJNA1002603 (324 BS), `TRSI*` / `TRSITSI*` prefix
- `sty-11-wbc14h22`: 3 BPs split across years (2016 / 2017 / 2018)

These don't need bermap normalization, but downstream consumers should be aware they're two views of one experimental design.

### GLBRC MMPRNT cohort (Kellogg Biological Station / Lux Arbor / Lake City / Escanaba / Hancock / Rhinelander)

Spans at least three bermap studies that share the GLBRC Marginal Land Experiment plot structure (G5 = switchgrass, G10 = native prairie, G11 = historical-vegetation control, +N/0N split-plot):
- `sty-11-wbc14h22` (Maren Friesen, 2,737 BS across 2016-2018)
- `sty-11-e4yb9z58` (Ashley Shade, phyllosphere, 192 BS — same `G5R*` plot codes)
- `kbs_mcse_long_term_cropping_experiment_metagenomes` (Sarah Roley, 106 BS — uses KBS LTER plot identifiers)

These should share enum definitions (`HostCropEnum`, `NitrogenTreatmentEnum`) and the plot/site code legend. They currently don't — would benefit from a shared `glbrc_mle_*` base module.

### Populus common-garden cohort (PMI SFA, Oak Ridge)

Multiple studies use overlapping `BESC-`, `GW-`, `DD176-`, `UPMTD` Populus genotype codes:
- `cultivating_bacterial_microbiota_of_populus_roots`
- `populus_holobiont_niche_and_genotype_effects`
- `poplar_rhizosphere_microbiota_assembly_dynamics`
- `seasonality_and_temporal_dynamics_in_populus_microbiome`
- `sty-11-kfvmk798` (Boardman drought)
- `sty-11-r2h77870` (Bio-Scales)
- `sty-11-1t150432`
- `climate_driven_divergence_in_plant_microbiome_interactions`

A unified `PopulusGenotypeEnum` populated across these (currently a "27 P. trichocarpa genotypes" placeholder) would be high-impact.

### Sample-name format heterogeneity

Quick glance at one sample per study (from the curated `.nmdc.json` files): every study uses a different `samp_name` convention. Highlights:

| Study | First samp_name |
|---|---|
| sty-11-vh2hty57 | `5108_M_2016_P60_N200_B_20180703_CABBI` (CABBI plot code) |
| seasonality_and_temporal_dynamics_in_populus_microbiome | `S9H-P4-Root-ITS` |
| populus_variovorax_syncom28_compartment_partitioning | `Pt_rhizo_4` |
| oak_ridge_groundwater | `EB271_05_03` (well + depth) |
| sorghum_phyllosphere_microbiome | `WR5P6.90DAE` |
| brachypodium_core_root_microbiome_metabarcoding | `Trainline rhizosphere 6` |
| e_coli_phage_resistance_landscape | `pFAB5554_Escherichia_bl21_Bagseq_DN` |
| transgenic_switchgrass_microbiome_effects | `TRSRI1F3` |

This heterogeneity is why per-study `samp_name` parsers exist for sty-11-vh2hty57 and sty-11-wbc14h22 — generalizing requires per-cohort rules.

## 7. Highest-value next actions

1. **Fix base.yaml slot aliases** to include MIxS short names (`elev`, `geo_loc_name`, `lat_lon`, `env_broad_scale`, `env_local_scale`, `env_medium`, `env_package`). One commit, clears ~70 alignment warnings.
2. **Add base slots for `host`, `isolation_source`, `replicate`, `depth`, `strain`** — recurring NCBI attrs that no bermap profile covers.
3. **Retire one of the two duplicate Oak Ridge dirs** in `db/sfas-brcs.yaml` to avoid double-counting before ingest.
4. **Tag `Microbe.1.0` studies in bermap** with a `sample_class: lab_isolate` to skip MIxS env-triad expectations.
5. **Build the unified `PopulusGenotypeEnum`** from the 27+ BESC / GW / DD176 / UPMTD codes that recur across 8+ studies.
6. **Build a shared GLBRC MMPRNT plot-code legend** as a base module for the 3+ studies using the G5/G10/G11/+N/0N design.
7. **File upstream bugs against `nmdc-ingest-agent`**:
   - `_infer_analyte_category` returning `"metabarcode"` (patched locally; needs upstream PR)
   - `QuantityValue` without required `has_unit` blocking PRJNA718849
   - Pipeline missing anchor-class pre-check for submitter-supplied ENVO CURIEs
8. **Plan a separate ingest path for MAGs** (`MetagenomeAssembly` / `MagBin`) so the bioreactor study and similar deposits can be brought into NMDC.
