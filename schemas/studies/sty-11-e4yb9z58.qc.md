# sty-11-e4yb9z58 — Data quality / cross-source audit

**Study:** Seasonal activities of the phyllosphere microbiome of perennial crops
**NMDC:** `nmdc:sty-11-e4yb9z58`
**Source registry:** GOLD only — `gold:Gs0128851`, `jgi.proposal:503249`
**NCBI BioProject:** none recorded on NMDC study

Audit date: **2026-06-19**.

## No NCBI BioProject ingest possible

This study has no INSDC BioProject ID on the NMDC study record — only GOLD and JGI proposal identifiers. `nmdc-ingest-agent` (NCBI-only as of 0.1.0) cannot ingest from these sources, so the four-source comparison used in other QC.md files reduces here to NMDC ↔ bermap profile only.

## env_triad has a category mismatch

All 192 biosamples carry an identical and conceptually odd triad:

| Slot | NMDC asserts | NMDC label | Issue |
|---|---|---|---|
| `env_broad_scale` | `ENVO:01001442` | agricultural biome | ✓ defensible for cropland phyllosphere |
| `env_local_scale` | `ENVO:01001442` | **phyllosphere biome** | ❌ category mismatch — `*_biome` belongs to broad_scale, not local_scale. MIxS local_scale should be an environmental feature, e.g. ENVO:00002030 (phyllosphere) at the part level |
| `env_medium` | `ENVO:01000001` | **plant-associated biome** | ❌ same category mismatch — `*_biome` is broad-scale; medium should be an environmental material. ENVO:00002030 (phyllosphere) or PO:0009025 (leaf) would be more appropriate |

NMDC assigned `*_biome` terms to all three slots — the broad_scale duplicates into local_scale, and the medium uses another biome term. The MIxS env triad expects: biome (broad) → environmental feature (local) → environmental material (medium). This study violates that progression.

## Design recoverable from `samp_name`

Sample names follow the GLBRC plot-code pattern (e.g., `G5R1_MAIN_09MAY2016`):

```
G<plot-type>R<replicate>_MAIN_<DDMmmYYYY>
```

- `G5` = switchgrass (Panicum virgatum cv. Cave-in-rock), per GLBRC MLE convention shared with `sty-11-wbc14h22`
- `R1`–`R4` = block replicate
- `MAIN` = main plot identifier
- Date encodes the seasonal sampling timepoint

Not surfaced as structured NMDC fields. Same MMPRNT cohort / Marginal Land Experiment design as `sty-11-wbc14h22`.

## Site

All 192 samples: `USA: Michigan, Kellogg Biological Station` — single site.

## Open items

- env_triad needs full re-curation: broad_scale OK, local_scale and medium need terms outside the `*_biome` family
- The companion `sty-11-vh2hty57.yaml` and `sty-11-wbc14h22.yaml` ground `host_crop` as `HostCropEnum`; the bermap profile for this study uses the same pattern with `switchgrass` and `miscanthus` levels (correct)
- `other_treatment` / `experimental_factor_other` / `cur_vegetation` all NULL for this study — design factors invisible to NMDC queries

## Known limitations of this audit

- Cannot ingest from NCBI for comparison (no BioProject recorded)
- JGI proposal data was not fetched — there may be additional metadata on the JGI portal under proposal 503249
- The GLBRC sustainability data portal almost certainly has the seasonal sampling design + N fertilization for these G5 plots (cf. wbc14h22 qc.md — same MMPRNT cohort)
