# sty-11-vh2hty57 — Data quality / cross-source audit

**Study:** The Impact of Stand Age and Fertilization on the Soil Microbiome of *Miscanthus × giganteus*
**NMDC:** `nmdc:sty-11-vh2hty57`
**NCBI BioProject:** `PRJNA601860`
**DOI:** [10.1094/PBIOMES-01-20-0014-FI](https://doi.org/10.1094/PBIOMES-01-20-0014-FI)
**PI:** Adina Howe (Iowa State / CABBI)

Companion to `sty-11-vh2hty57.yaml` (LinkML profile) and `sty-11-vh2hty57.sssom.yaml` (mappings).
Captures discrepancies between the four representations of this study:

1. **Original deposited data** — what's in `samp_name` and the submitter's filenames (CABBI plot codes)
2. **NCBI BioSample / EBI BioSamples** — INSDC public record under PRJNA601860 (~648 samples)
3. **NMDC** — `nmdc_metadata.biosample_set` ingest (696 samples)
4. **bermap profile** — `schemas/studies/sty-11-vh2hty57.yaml` (the logical/intended schema)

Audit date: **2026-06-17**.

## Sample-count divergence

| Source | n biosamples | What's included |
|---|---:|---|
| NMDC ingest | 696 | 648 rhizosphere + 48 bulk-soil DNA samples (CABBI submitter codes) |
| NCBI PRJNA601860 | 648 | rhizosphere only — bulk-soil DNA never deposited |
| bermap `sample_count` | 648 | currently matches NCBI subset, **not** NMDC scope |

**Action item:** decide whether bermap `sample_count` should track NMDC (696) or NCBI (648). Currently it understates NMDC scope.

## Study-description gap

| Source | Title / description | Mentions Corn? |
|---|---|:---:|
| NMDC portal | *The Impact of Stand Age and Fertilization on the Soil Microbiome of Miscanthus × giganteus* | ❌ |
| NCBI BioProject PRJNA601860 | title: *soil bacterial microbial community associated with Miscanthus giganteus*; description: *…effects of planting year of Miscanthus and nitrogen fertilization rates…* | ❌ |
| bermap profile (pre-audit) | inherited the Miscanthus-only framing; no `host_crop` slot | ❌ |
| Deposited data | `other_treatment=Corn` (228/696 = 33%); `Plant=Corn` (216/648 NCBI); samp_name starts with `_C_` | ✅ |
| bermap profile (post-audit) | Added `host_crop` slot — explicitly Miscanthus vs Corn comparator | ✅ |

## Per-variable three-way diff (one biosample: SAMN13875904 / nmdc:bsm-11-01gd8h56)

| Variable | Original (samp_name + submitter) | NCBI BioSample | NMDC `biosample_set` | bermap profile slot | Status |
|---|---|---|---|---|---|
| Crop / host | `_M_` in `4095_M_2017_P50_N200_A_20180530_CABBI` | `Plant=Miscanthus` (custom) | `other_treatment=Miscanthus` | `host_crop` → `miscanthus` (NCBITaxon:62336) | ✅ post-audit |
| Stand age (yr) | `_2017_` token implies 1-yr stand (sampled 2018) | `Year=2017` (custom) | not surfaced | `stand_age` → integer (derived from samp_name) | ⚠️ derived, no NMDC source |
| N fertilization rate (kg/ha) | `_N200_` token | `Nitrogen=200`, `fertilizer=yes` (custom) | `experimental_factor_other = "N_fertilization_rate: 200 kg/ha"` (string!) | `nitrogen_fertilizer_rate` → float kg/har | ⚠️ stored as string; satellite `_fertilizer_regm` is empty |
| Plot ID | `_P50_` token | `Plot=50` (custom) | not surfaced | `plot_id` → string (derived from samp_name) | ⚠️ derived, no NMDC source |
| Replicate | `_A_` marker; sequential IDs on 2018-04-25 batch | `replicate=biological replicate 1` (custom) | dropped | `biological_replicate` → string (derived) | ⚠️ derived, no NMDC source |
| Soil compartment | rhizosphere (no `_Bulk_` marker) | `Soil=Rizosphere` (custom); `isolation_source=soil` (harmonized) | `env_medium=bulk soil` [ENVO:00005802] uniformly across all 696 | `soil_compartment` → `rhizosphere` (ENVO:00005801) | ❌ NMDC mislabel for 648 samples; ✅ profile recovers via new slot |
| `env_medium` (MIxS) | n/a | `isolation_source=soil` | `bulk soil [ENVO:00005802]` (all 696) | `environmental_medium` → uriorcurie | ❌ NMDC over-specialized `soil` → `bulk soil`; wrong for 648 |
| Soil depth | n/a | not surfaced | `depth_has_minimum_numeric_value=0.0`, `_maximum=0.1`, range 0–0.1 m | `soil_sampling_depth` → float m | ⚠️ scalar collapse — NMDC has range, profile has single value |
| `geo_loc_name` | n/a | `USA: central IA` (raw) | `USA: Iowa, Ames` (curator-refined) | `geographic_location_name` → string | ✅ NMDC enriches |
| `lat_lon` | n/a | `42.013 N 93.743 W` (string) | string `42.013` / `-93.743` (two cols) | `latitude_and_longitude` → string | ⚠️ none store as numeric pair; new `nmdc-ingest-agent` snapshot does |
| `collection_date` | `_20180530_` token | `2018-05-30` | `2018-05-30` | `collection_date` → datetime | ✅ |
| `samp_taxon_id` | n/a | `taxonomy_id=410658` (soil metagenome) | ❌ not stored | not in profile | ⚠️ NMDC drops; new ingest-agent snapshot keeps |

Legend: ✅ aligned · ⚠️ derived or partial · ❌ disagreement or missing

## Cross-source data flow (best understanding)

```
                ┌─────────────────────┐
                │  CABBI submitter    │   (Iowa State, Adina Howe)
                │  filename codes     │   samp_name = 4095_M_2017_P50_N200_A_20180530_CABBI
                └──────────┬──────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
  ┌─────────────────────┐    ┌─────────────────────┐
  │ NMDC submission     │    │ NCBI BioSample      │
  │ (BRC pipeline)      │    │ (INSDC deposit)     │
  │ → biosample_set     │    │ → SAMN…             │
  │ 696 records         │    │ 648 records         │
  └──────────┬──────────┘    └──────────┬──────────┘
             │                          │
             │ (insdc_biosample_         │ (mirrored)
             │  identifiers back-link)   │
             ▼                          ▼
                              ┌─────────────────────┐
                              │ EBI BioSamples      │
                              │ (mirror, web view)  │
                              └─────────────────────┘
```

**Key takeaway:** NMDC did *not* ingest from NCBI; the two ingests are parallel from the submitter.

## Known limitations of this audit

- `samp_taxon_id`, `Days`, `Type`, `Comparing` NCBI custom attributes not yet mirrored into the bermap profile.
- The NMDC env_medium mislabel is flagged here but no upstream curation issue has been filed against NMDC (yet).
- Stand age formula (`collection_year − planting_year`) assumes single-season sampling; revisit if multi-year resampling is added.
