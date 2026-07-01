All 9 BioProjects processed and validated. Here is the consolidated report.

## Curation pass summary — 9 BioProjects, 2151 biosamples

All files updated in place (`*.nmdc.json`, `*.curation_report.json`). All 9 NMDC JSONs validate cleanly against the schema. No real IDs were minted.

### Per-study × per-slot outcomes

| Study | env_broad_scale | env_local_scale | env_medium |
|---|---|---|---|
| **PRJNA938072** soil_pore_space (874 BS) | predicted=874 (cropland biome) | predicted=874 (agricultural field) | resolved_from_raw=873 / predicted=1 (agricultural soil) |
| **PRJNA385484** populus_holobiont bact (300) | resolved_from_raw=300 (temperate broadleaf forest biome) | **validator_rejected=300** | resolved_from_raw=300 (plant matter / soil) |
| **PRJNA384978** populus_holobiont fungal (290) | resolved_from_raw=290 (temperate broadleaf forest biome) | **validator_rejected=290** | resolved_from_raw=290 (plant matter / soil) |
| **PRJNA726831** climate_divergence (539) | **validator_rejected=539** | **validator_rejected=539** | resolved_from_raw=539 (bulk soil) |
| **PRJNA834153** corynebacterial phage (18) | **validator_rejected=18** | **validator_rejected=18** | **validator_rejected=18** |
| **PRJNA268032** enigma_groundwater (16) | predicted=16 (freshwater biome) | predicted=16 (underground water body) | predicted=16 (groundwater) |
| **PRJNA1322484** populus_variovorax (15) | **validator_rejected=15** | resolved_from_raw=8 (rhizosphere) / validator_rejected=7 (endosphere) | predicted=15 (plant matter) |
| **PRJNA961726** sorghum/colleto in planta (95) | **validator_rejected=95** | **validator_rejected=95** | predicted=95 (plant matter) |
| **PRJNA1114779** sorghum/colleto in vitro (4) | **validator_rejected=4** | **validator_rejected=4** | **validator_rejected=4** |

**Totals across all 9 × 3 slots = 6453 rows:** predicted=1907 · resolved_from_raw=2600 · validator_rejected=1946 · left_sentinel=0 · resolved_at_pipeline=0.

### Per-slot reasoning notes

- **PRJNA938072** — Lab microcosm decomposition of KBS LTER agricultural soil; committed cropland biome / agricultural field / agricultural soil. One sample had empty `isolation_source` so its env_medium counts as predicted rather than resolved.
- **PRJNA385484 / PRJNA384978** — Both populus_holobiont studies share identical raw triads. "Plantation" rejected because ENVO:00000117 sits under *anthropogenic environment*, not *astronomical body part* — the env_local_scale anchor fails. Used ENVO:01001121 plant matter as fallback for plant leaves/roots/stem (per cross-cutting guidance, no perfect ENVO term).
- **PRJNA726831** — Raw env_broad ("High elevation watersheds in the Rocky Mountains, USA") is a geographic phrase, not a biome; 539 samples span W. US sites at 1.4–2.8 km elevation with multiple surrounding biomes — refused per Rule 4. Raw env_local "Riparian ecosystems" has no ENVO equivalent under astronomical body part. Bulk soil resolved cleanly.
- **PRJNA834153** — All 18 samples are lab cultures of *C. glutamicum* and its phages (Microbe.1.0); per cross-cutting guidance treated as indoor/microcosm → validator_rejected on all three slots.
- **PRJNA268032** — Rifle, CO aquifer groundwater. Committed freshwater biome / underground water body / groundwater. Rejected candidates recorded (aquifer = layer not body part; water well = no explicit per-sample well evidence).
- **PRJNA1322484** — Axenic Populus root microcosm with synthetic Variovorax SynCom28 → no natural biome. Rhizosphere samples got ENVO:00005801 for local_scale; endosphere samples have no ENVO local-scale term. All medium = plant matter (ENVO:01001121 fallback).
- **PRJNA961726** — Greenhouse sorghum leaf RNA-seq (Plant.1.0). No phyllosphere/leaf-surface ENVO term under the env_local_scale anchor; env_medium = plant matter.
- **PRJNA1114779** — In vitro fungal culture on PDA. All three slots rejected.

### Cross-cutting issues affecting multiple studies

1. **nmdc-submission-schema not importable** in the active env → MIxS soil-package valueset constraint NOT enforced for PRJNA726831 and (implicitly) for the soil samples in PRJNA385484/PRJNA384978. Flagged in their report rows. This is a known gap — would re-validate against the soil valueset once the package is installable.
2. **ENVO:00000117 "plantation"** lives under *anthropogenic environment*, not *astronomical body part*. Any study lifting raw "plantation" to env_local_scale will fail the anchor check — affected 590 rows (PRJNA385484 + PRJNA384978). Worth flagging upstream as a recurring submitter pattern with no clean ENVO mapping.
3. **No ENVO term for "phyllosphere" / "plant leaf surface" / "root endosphere"** as features under astronomical body part — recurring fallback to validator_rejected for env_local_scale on plant-tissue samples (PRJNA961726 + 7 endosphere samples in PRJNA1322484). ENVO:01001121 plant matter remains the workable env_medium fallback (per guidance) but the local-scale gap is a real ontology hole.
4. **No ENVO "riparian zone" term** under the env_local_scale anchor — affected PRJNA726831 (539 rows). Closest hit wetland ecosystem rejected as semantically wrong.
5. **Microbe.1.0 / in-vitro packages produce all-validator_rejected triads** (PRJNA834153 + PRJNA1114779 = 22 BS × 3 slots = 66 rows). Per guidance these are correctly refused; just noting they accumulate quickly.

### Host / taxon and other slots
- Per your guidance I did not write to slots the curation report doesn't include (host, samp_taxon_id).
- `samp_taxon_id` was already populated at pipeline stage from NCBI taxonomy where present.
- No new host inference was attempted — flagged here that the populus_holobiont studies and PRJNA1322484 (Populus *trichocarpa*/​*deltoides*) and the sorghum studies (Sorghum *bicolor*) have unambiguous hosts upstream that the report could be extended to track if desired.

No qc.md files written.