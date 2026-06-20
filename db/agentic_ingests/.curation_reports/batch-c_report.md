## Consolidated curation report — 10 BioProjects, 2,644 biosamples

All 10 NMDC JSONs validate against `nmdc.Database`. Files updated in place; curation reports rewritten with evidence, candidates, and validator dicts. Counts below: **P**redicted / **R**aw / **PL** = resolved_at_pipeline / **LS** = left_sentinel / **VR** = validator_rejected.

| Study (PRJ) | env_broad_scale | env_local_scale | env_medium |
|---|---|---|---|
| PRJNA862978 sorghum rhizo pot (306) | R 220, LS 86 | R 220, LS 86 | R 220, LS 86 |
| PRJNA844896 sorghum phyllosphere field (239) | R 239 | VR 239 | R 228, LS 11 |
| PRJNA1002602 switchgrass QsuB 16S (198) | P 198 | P 90, VR 108 | P 198 |
| PRJNA1002603 switchgrass QsuB ITS (324) | P 324 | P 180, VR 144 | P 324 |
| PRJNA1017804 poplar France (509) | P 509 | P 255, VR 254 | P 509 |
| PRJNA561781 native miscanthus Taiwan (466) | P 466 | R 466 | R 233, P 233 |
| PRJNA892137 sugarcane/oilcane greenhouse (200) | VR 200 | P 80, VR 120 | P 200 |
| PRJNA1120948 brachypodium Conviron (71) | VR 71 | P 48, VR 23 | P 71 |
| PRJNA1080623 plant-nitrifier topsoil (103) | P 103 | PL 103 | PL 103 |
| PRJNA933671 terpene sorghum (228) | P 228 | P 168, VR 60 | P 228 |

### Cross-cutting issues

1. **Plant compartments (root/leaf/inflorescence/shoot) lack ENVO local-scale terms** — affects 5 studies (1002602, 1002603, 1017804, 892137, 1120948, 933671). All `env_local_scale` for these compartments → validator_rejected with candidate notes. `env_medium` falls back to ENVO:01001121 (plant matter) per cross-cutting guidance.
2. **Indoor/microcosm has no good ENVO biome** — applied to PRJNA892137 (greenhouse) and PRJNA1120948 (Conviron). `env_broad_scale` → validator_rejected per guidance (271 biosamples).
3. **`ENVO:01001001` plant-associated-environment submitter mistake** — confirmed: fails biome, feat, and material anchors. Replaced wherever pipeline carried it forward (PRJNA1002602/03, PRJNA933671 — 90 biosamples in env_broad slot, plus more local/medium uses).
4. **Pipeline accepted free CURIEs without anchor validation** — for studies where submitters supplied ENVO/BTO CURIEs in attributes (PRJNA561781, PRJNA1080623, PRJNA1002602/03, PRJNA933671), the pipeline copied them straight through with `term.name == CURIE`. I overwrote `term.name` with the official ENVO label and rejected those that fail anchor checks (ENVO:01001790 terrestrial ecosystem → biome failure; ENVO:00002259 agricultural soil → biome failure; BTO:0001181 endophyte → not in ENVO).
5. **Phyllosphere & epicuticular wax / mucilage have no ENVO terms** — PRJNA844896 env_local_scale all 239 → validator_rejected. env_medium uses ENVO:01001121 plant matter fallback for 228 real samples; 11 controls → left_sentinel.
6. **Soil-package valueset constraint not enforced** — `nmdc-submission-schema` was not consulted. Multiple studies use `MIMARKS.survey.soil.6.0` (PRJNA862978, PRJNA561781, PRJNA1080623) — known gap, called out explicitly.

### Curator follow-up backlog (left_sentinel)

- PRJNA862978: 86 negative-control biosamples (extraction blanks, all 3 slots each).
- PRJNA844896: 11 medium-only sentinels (9 negative + 2 positive controls).
- All other studies have zero `left_sentinel` — refusals went to `validator_rejected` with explanatory candidate entries instead.

### Notes on host / taxon

Host fields not in scope (skill says to flag only). Hosts of interest worth a future taxon pass: Switchgrass / Sorghum / Populus tremula tremuloides (incl. transgenic clones T89 NR1E, T89 ACO1) / Miscanthus floridulus + M. sinensis / Saccharum spp. hybrid (oilcane) / Brachypodium distachyon.