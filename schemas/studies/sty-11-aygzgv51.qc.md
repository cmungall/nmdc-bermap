# sty-11-aygzgv51 — Data quality / cross-source audit

**Study:** Riverbed sediment microbial communities from the Columbia River, Washington, USA
**NMDC:** `nmdc:sty-11-aygzgv51`
**Source registry:** GOLD only — `gold:Gs0114663`

Audit date: **2026-06-19**.

## No NCBI BioProject ingest possible

GOLD-only ingest; `nmdc-ingest-agent` cannot re-ingest. Audit reduces to NMDC ↔ bermap profile.

## env_triad — heterogeneous, hyporheic zone study

Three distinct env triad combinations across 84 biosamples:

| n | broad | local | medium |
|---:|---|---|---|
| 34 | hot desert biome [ENVO:00000873] | shore [ENVO:00000022] | mineral material [ENVO:01000017] |
| 33 | freshwater river biome [ENVO:01000253] | wave [ENVO:00000384] | sediment [ENVO:00002007] |
| 17 | freshwater river biome | microcosm [ENVO:01000621] | mineral material |

(`label = NULL` for all of these because NMDC didn't populate `*_term_name`, same pattern as `sty-11-076c9980` — backfill needed.)

### Issues with the triad
- **`hot desert biome` for 34 samples is wrong** for Columbia River, Washington — this is a temperate riverine environment, not desert. Possibly a confusion of `Hanford` (the DOE site location in eastern Washington) with desert; while the Hanford area is shrub-steppe, ENVO has more appropriate terms (e.g. ENVO:01001369 *Mediterranean shrubland biome* or ENVO:01000219 *temperate desert biome*; ideally a riverine/aquatic biome since the samples are riverbed sediment).
- **`wave [ENVO:00000384]` as env_local_scale for 33 samples is suspect** — waves are physical features; for hyporheic zone studies the local scale would typically be `riverbed [ENVO:00000148]` or `hyporheic zone [ENVO:01000584]`.
- The **`microcosm`** value for 17 samples suggests **lab-incubation samples** were mixed into the field-sample ingest — different sample type, should arguably be flagged.

## Hyporheic zone context

Per the study description, this is about the groundwater-surface water mixing zone (hyporheic) at the Hanford site on the Columbia River. The bermap profile would benefit from a `sample_compartment` slot distinguishing field riverbed samples from lab-incubation microcosm samples.

## Design factor in `samp_name`

Sample names appear to encode transect position and sampling date:

```
GW-RW T4_25-Nov-14   # Groundwater-RiverWater transect, position T4, 25 Nov 2014
GW-RW T3_23-Sept-14
GW-RW T3_25-Nov-14
```

- `GW-RW` = Groundwater–River Water mixing
- `T3` / `T4` = transect position
- date is the collection date

Not surfaced as structured NMDC fields beyond `collection_date_has_raw_value`.

## Open items

- env_triad needs full re-curation: `hot desert biome` is wrong; `wave` is suspect; the field/lab distinction (microcosm subset) should be lifted to a structured field
- `*_term_name` columns are NULL — labels need backfilling from ENVO (same gap as `sty-11-076c9980`)
- Transect position (T3/T4/etc.) and groundwater-vs-river-water role not surfaced in structured fields

## Known limitations of this audit

- Cannot ingest from NCBI for comparison (no BioProject recorded)
- The 34/33/17 cohort split wasn't drilled into to verify which samples belong to which physical location
- The bermap profile entry should be inspected to see if the hyporheic zone framing is reflected
