## Consolidated batch report (7 BioProjects · ~1500 biosamples)

### Per-study per-slot outcome counts

| Study | Slot | predicted | resolved_from_raw | resolved_at_pipeline | left_sentinel | validator_rejected |
|---|---|---:|---:|---:|---:|---:|
| 1. PRJNA645443 E. coli phage (357) | env_broad_scale | 0 | 0 | 0 | 357 | 0 |
| | env_local_scale | 0 | 0 | 0 | 357 | 0 |
| | env_medium | 0 | 0 | 0 | 357 | 0 |
| 2. PRJNA741261 sorghum rhiz (288) | env_broad_scale | 0 | 288 | 0 | 0 | 0 |
| | env_local_scale | 0 | 288 | 0 | 0 | 0 |
| | env_medium | 0 | 288 | 0 | 0 | 0 |
| 3. PRJNA745191 Miscanthus (271) | env_broad_scale | 0 | 271 | 0 | 0 | 0 |
| | env_local_scale | 0 | 271 | 0 | 0 | 0 |
| | env_medium | 0 | 271 | 0 | 0 | 0 |
| 4. PRJNA666202 Populus (198) | env_broad_scale | 198 | 0 | 0 | 0 | 0 |
| | env_local_scale | 132 | 0 | 0 | 66 | 0 |
| | env_medium | 198 | 0 | 0 | 0 | 0 |
| 5. PRJNA1001011 OR groundwater (140) | env_broad_scale | 136 | 0 | 0 | 4 | 0 |
| | env_local_scale | 136 | 0 | 0 | 4 | 0 |
| | env_medium | 136 | 0 | 0 | 4 | 0 |
| 6. PRJNA1001011 OR sed+gw (140) | env_broad_scale | 136 | 0 | 0 | 4 | 0 |
| | env_local_scale | 136 | 0 | 0 | 4 | 0 |
| | env_medium | 136 | 0 | 0 | 4 | 0 |
| 7. PRJNA1156252 KBS MCSE (106) | env_broad_scale | 0 | 0 | 0 | 0 | 106 |
| | env_local_scale | 0 | 0 | 106 | 0 | 0 |
| | env_medium | 0 | 0 | 106 | 0 | 0 |

### Resolutions committed
- **Sorghum (Study 2)**: `temperate broadleaf forest biome` / `agricultural field` / `agricultural soil` — lifted from raw text on all 288 BS.
- **Miscanthus (Study 3)**: `cropland biome` (from "agriculturalbiome" typo) / `soil` / `soil` — all 271 BS.
- **Populus common gardens (Study 4)**: `anthropogenic terrestrial biome` × 3 isolation_sources. Local scale: `garden` for bulk soil, `rhizosphere` for rhizosphere, **left_sentinel for 66 endosphere rows** (no ENVO local-scale term). Medium: `soil` for soil/rhiz, `plant matter` (ENVO:01001121) for endosphere per cross-batch guidance.
- **Oak Ridge (Studies 5 & 6)**: `freshwater biome` × groundwater→`water well`+`groundwater`, sediment→`continental subsurface zone`+`sediment`. 4 negative/extraction controls per study left sentinel.
- **KBS (Study 7)**: pipeline-supplied `ENVO:01000352` (field) for env_broad_scale **fails the biome anchor** → all 106 reverted to sentinel with `validator_rejected`. Local & medium CURIEs passed; labels repaired in the JSON.

### Cross-cutting issues flagged
1. **Soil package valueset not enforced** for Studies 2, 3, 7 (MIMARKS/MIMS soil packages). `nmdc-submission-schema` was not installed; commits were anchor-class-only. Surface as known gap (per env-triad skill § Soil package).
2. **Pipeline CURIE pass-through** (Study 7): when submitter put bare ENVO CURIEs in env_triad attrs, the pipeline copies them into `term.id` and `term.name` without checking biome/anchor membership. `ENVO:01000352` (field) is not a biome — submitter mistake the pipeline propagated. Worth a pre-commit anchor-check in `mfd.py` / generic ENVO parsing path.
3. **Endosphere local scale gap**: ENVO has no fit for "root endosphere" as an env_local_scale (rhizosphere only). 66 left_sentinel rows in Study 4 — curator follow-up.
4. **Lab microcosm studies** (Study 1): all 357 BS are Microbe.1.0 in-vitro E. coli with phages — no MIxS env_triad applies. 1071 rows left_sentinel per microcosm guidance, annotated with one-line evidence on every row.
5. **Negative / sequencing controls** appear in Oak Ridge (8) and KBS (2). Oak Ridge controls were left sentinel; KBS controls inherited the same (incorrectly) submitter-supplied soil triad — surfaced via env_broad_scale validator_rejected.
6. **Studies 5 & 6 are duplicates**: same NCBI accession PRJNA1001011, identical BioSample set (just different generated NMDC IDs). Confirm one should be retired before ingest.
7. **Host / samp_taxon**: not part of the curation report skeleton this round, so no edits attempted — Study 4 has Populus trichocarpa host strings the curator may want to lift to NCBITaxon; the rest are environmental or lab samples.

### Files updated (in place)
For each study: `<DIR>/<PRJNA>.nmdc.json` (env_triad term IDs/labels) and `<DIR>/<PRJNA>.curation_report.json` (outcomes, evidence, validator). Curation inputs unchanged. No qc.md written.