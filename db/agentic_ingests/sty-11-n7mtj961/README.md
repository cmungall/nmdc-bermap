# Agentic ingest snapshot — sty-11-n7mtj961

Frozen output from running [`nmdc-ingest-agent`](https://github.com/microbiomedata/nmdc-ingest-agent) against `PRJNA1205755` (Sorghum bicolor 'Wheatland' microbiome under drought + bioenergy trait modulation, JBEI/Davis CA, PI Henrik Vibe Scheller).

**Study profile**: [`../../../schemas/studies/sty-11-n7mtj961.yaml`](../../../schemas/studies/sty-11-n7mtj961.yaml) (placeholder — bermap profile is the generic JBEI sorghum entry)
**Cross-source QC audit**: [`../../../schemas/studies/sty-11-n7mtj961.qc.md`](../../../schemas/studies/sty-11-n7mtj961.qc.md)
**Ingest date**: 2026-06-19
**Tool**: `nmdc-ingest-agent` 0.1.0 with a one-line patch to `_infer_analyte_category` (see Caveats)
**ID shoulder**: `99` (placeholder)

## Sample-count context

NCBI deposit carries **683 biosamples**. NMDC currently has only **16** — a **43× divergence** flagged in the qc.md as a major audit finding.

## Files

| File | Bytes | What |
|---|---:|---|
| `PRJNA1205755.nmdc.json` | 2.1 MB | NMDC-schema `Database` — 683 biosamples |
| `PRJNA1205755.curation_inputs.json` | 519 KB | NCBI title + raw attributes sidecar |
| `PRJNA1205755.curation_report.json` | 985 KB | per-(biosample, slot) outcomes |

## Curation outcomes

| Slot | predicted | resolved_from_raw | resolved_at_pipeline | left_sentinel | validator_rejected |
|---|---:|---:|---:|---:|---:|
| `env_broad_scale` | 0 | **683** | 0 | 0 | 0 |
| `env_local_scale` | 0 | 287 | **396** | 0 | 0 |
| `env_medium` | 0 | 287 | **396** | 0 | 0 |

**Zero sentinels, zero rejections.** Submitter pre-embedded ENVO CURIEs in the free-text env-triad fields; the pipeline parsed them. Sample classification by `SampleType` prefix: **288** RHZ / **287** Root / **108** Soil/NPS.

Curator overrides applied:
- `env_broad_scale`: replaced submitter's `ENVO:01001244` (cropland ecosystem) with `ENVO:01000245` (cropland biome) for all 683 — original term fails the biome anchor check
- `env_local_scale` for 287 Root samples: replaced `ENVO:01001001` (plant-associated environment) with `ENVO:00005801` (rhizosphere) — original fails astronomical-body-part anchor
- `env_medium` for 287 Root samples: replaced `ENVO:01001001` with `ENVO:01001121` (plant matter) — same reason

Final values:
- `env_broad_scale = ENVO:01000245` (cropland biome) for all 683
- `env_local_scale`: rhizosphere for RHZ+Root (575); bulk soil for Soil/NPS (108)
- `env_medium`: rhizosphere (288), plant matter (287), soil (108)

## Caveats

**Required a patch to `nmdc-ingest-agent`**: the deterministic CLI's `_infer_analyte_category` returned `"metabarcode"` for amplicon strategies, which isn't a valid `NucleotideSequencingEnum` value. Patched locally in `~/nmdc-ingest-agent/src/nmdc_ingest_agent/sources/ncbi/translate.py:712` to return `"amplicon_sequencing_assay"`. Worth upstreaming.

**`ENVO:01001001 plant-associated environment` is a common submitter mistake** — appears in this study and PRJNA1151037; fails all three MIxS anchor checks (biome, astronomical body part, env material). Worth a one-shot QC rule in nmdc-ingest-agent to flag and rewrite.

## Open items not handled by this pass

- Sorghum genotype 'Wheatland', drought treatment, sampling timepoints — design factors not lifted from `samp_name`
- 667 NCBI biosamples missing from NMDC — worth understanding the filter criterion
