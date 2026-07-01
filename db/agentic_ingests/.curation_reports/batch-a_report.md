All 7 studies validated. Here's the consolidated report:

## Batch curation report (7 BioProjects, 3,326 biosamples)

### Per-study per-slot outcome counts

| Study (PRJNA) | N | Slot | predicted | resolved_from_raw | resolved_at_pipeline | left_sentinel | validator_rejected |
|---|---|---|---|---|---|---|---|
| **seasonality_populus (PRJNA993999)** | 2359 | env_broad_scale | – | 2359 | – | – | – |
| | | env_local_scale | – | 905 | – | 1454 | – |
| | | env_medium | 2359 | – | – | – | – |
| **switchgrass (PRJNA799201)** | 957 | env_broad_scale | 926 | – | – | 31 | – |
| | | env_local_scale | 926 | – | – | 31 | – |
| | | env_medium | 926 | – | – | 31 | – |
| **phage (PRJNA576510)** | 6 | env_broad_scale | – | – | – | 6 | – |
| | | env_local_scale | – | – | – | 6 | – |
| | | env_medium | 6 | – | – | – | – |
| **east_fork_sediment (PRJNA670906)** | 1 | env_broad_scale | 1 | – | – | – | – |
| | | env_local_scale | 1 | – | – | – | – |
| | | env_medium | 1 | – | – | – | – |
| **bacillus_eb14 (PRJNA681597)** | 1 | env_broad_scale | – | – | – | 1 | – |
| | | env_local_scale | – | – | – | 1 | – |
| | | env_medium | – | 1 | – | – | – |
| **novosphingobium (PRJNA1228656)** | 1 | env_broad_scale | – | – | – | – | 1 |
| | | env_local_scale | – | – | – | – | 1 |
| | | env_medium | – | – | – | – | 1 |
| **colletotrichum (PRJNA659716)** | 1 | env_broad_scale | – | – | – | – | 1 |
| | | env_local_scale | – | – | – | – | 1 |
| | | env_medium | – | – | – | – | 1 |

### Key commitments

- **seasonality_populus** — all env_broad_scale lifted to `ENVO:01000202` (temperate broadleaf forest biome, from "Temperate Forest" + Oak Ridge TN). env_local_scale=`ENVO:00005801` (rhizosphere) for soil samples; left sentinel for 1454 root/leaf endosphere samples. env_medium=soil for rhizosphere, plant matter (`ENVO:01001121`) for endosphere — submitter's "Common Garden" raw treated as a study-design label, not material.
- **switchgrass** — 924 soil + 2 root samples predicted (cropland biome / agricultural field / soil; rhizosphere + plant matter for the 2 root samples). 31 PCR-blank/mock/CONTROL wells left sentinel.
- **phage** — env_medium = `ENVO:00002007` (sediment) from `isolation_source=aquatic sediment` for all 6 (bioreactor + 5 pure cultures). env_broad_scale/local left sentinel: Berkeley shoreline ambiguous between freshwater lagoon and SF Bay.
- **east_fork_sediment** — freshwater stream biome / stream / stream sediment predicted from isolation_source + study description.
- **bacillus_eb14** — "endophytes" lifted to plant matter for env_medium. "Populus microbiome"/"Leaf microbiome" cannot anchor biome/feature → sentinel.
- **novosphingobium DAP-seq** + **colletotrichum** — both validator_rejected across all three slots (indoor lab culture / DAP-seq context, no fitting ENVO biome/feature/material).

### Cross-cutting issues

1. **`nmdc-submission-schema` not importable** — soil-package valueset constraint **not enforced** for any soil biosamples (924 in switchgrass + 905 rhizosphere in seasonality_populus = 1,829 affected). Predicted CURIEs were chosen from anchor-class descendants only.
2. **No ENVO env_local_scale anchor descendant for "Root endosphere" / "Leaf endosphere"** — 1,454 sentinel rows in seasonality_populus (887 root + 567 leaf). ENVO has `root matter` and `plant matter` (material) and `rhizoplane` (surface layer), but no astronomical-body-part feature for tissue interiors. Curator follow-up backlog.
3. **`isolation_source` ≠ submitter env_medium** — multiple studies (phage, east_fork) had empty env_medium raw but informative `isolation_source` attribute. Treated as predicted, not resolved_from_raw, since the lift is from a sibling attribute rather than the env_medium slot itself.
4. **"Common Garden" as env_medium raw** (seasonality_populus, all 2359) is a study-design label, not a material — overridden with the actual sampled compartment material derived from env_local_scale.
5. **Cultured-isolate / lab-technique biosamples** (colletotrichum on PDA, novosphingobium DAP-seq) — applied `validator_rejected` per the cross-cutting indoor/microcosm guidance; 2 biosamples × 3 slots = 6 rows.

Total **curator backlog (left_sentinel)**: 1,548 rows. Total **validator_rejected**: 6 rows.