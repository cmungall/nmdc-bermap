# sty-11-zs2syx06 — Data quality / cross-source audit

**Study:** Meadow Soil Metagenomes from the Angelo Coast Range Reserve
**NMDC:** `nmdc:sty-11-zs2syx06`
**Source registry:** GOLD only — `gold:Gs0110119`
**PI:** Jillian F. Banfield

Audit date: **2026-06-19**.

## No NCBI BioProject ingest possible

GOLD-only ingest; `nmdc-ingest-agent` cannot re-ingest. Audit reduces to NMDC ↔ bermap profile.

## env_triad — clean and consistent

| Slot | Term | Label | Coverage |
|---|---|---|---|
| `env_broad_scale` | ENVO:01000177 | grassland biome | 60/60 |
| `env_local_scale` | ENVO:00000376 | meadow | 60/60 |
| `env_medium` | ENVO:00005750 | grassland soil | 58/60 |
| `env_medium` | ENVO:00002258 | bog soil | 2/60 |

This is a well-curated NMDC env triad — grassland biome / meadow / grassland soil correctly describes the Angelo Coast Range Reserve meadow site, and the 2 bog soil samples reflect actual heterogeneity. Contrast with `sty-11-vh2hty57` (uniform bulk soil regardless of compartment) and `sty-11-wbc14h22` (uniform farm soil regardless of land use).

## Design factor in `samp_name`

Sample names carry sampling year + plot + depth:

```
14_0903_02_20cm    # 2014, Sept 3, plot 02, 20 cm depth
14_0927_02_40cm    # 2014, Sept 27, plot 02, 40 cm depth
```

Likely format: `<YY>_<MMDD>_<plot>_<depth>cm`. This is part of an **ongoing climate-change manipulation experiment** (per the description) — some meadow plots receive supplemental water, others are controls. That treatment isn't surfaced in any NMDC structured field; would need to be parsed from samp_name + cross-referenced to the experiment's site map.

## Open items

- Climate-change treatment (water-amended vs control) not visible in NMDC structured data
- Depth is encoded in `samp_name` (`20cm`, `30cm`, `40cm`) — could be backfilled into NMDC's `depth_*` fields
- Bog vs grassland soil compartment difference (2 samples) is the only structured heterogeneity flag
- 60 biosamples — single small study; bermap `sample_count` aligns

## Known limitations of this audit

- Cannot ingest from NCBI for comparison (no BioProject recorded)
- The GOLD record (Gs0110119) may carry additional plot/treatment metadata that wasn't crosswalked into NMDC
