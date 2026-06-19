# Agentic ingest snapshot — sty-11-ev70y104

Frozen output from running [`nmdc-ingest-agent`](https://github.com/microbiomedata/nmdc-ingest-agent) against `PRJNA1151037` (EcoFAB 2.0 Root Microbiome Ring Trial, multi-lab reproducibility study, PI Trent R. Northen).

**Study profile**: [`../../../schemas/studies/sty-11-ev70y104.yaml`](../../../schemas/studies/sty-11-ev70y104.yaml)
**Cross-source QC audit**: [`../../../schemas/studies/sty-11-ev70y104.qc.md`](../../../schemas/studies/sty-11-ev70y104.qc.md)
**Ingest date**: 2026-06-19
**Tool**: `nmdc-ingest-agent` 0.1.0
**ID shoulder**: `99` (placeholder)

## Sample-count context

NCBI deposit carries **175 biosamples** (~163 DataGenerations — 12 mock samples have no sequencing data). NMDC currently has 140 — small gap.

## Files

| File | Bytes | What |
|---|---:|---|
| `PRJNA1151037.nmdc.json` | 540 KB | NMDC-schema `Database` — 175 biosamples (163 DataGenerations) |
| `PRJNA1151037.curation_inputs.json` | 268 KB | NCBI title + raw attributes sidecar |
| `PRJNA1151037.curation_report.json` | 211 KB | per-(biosample, slot) outcomes |

## Curation outcomes

| Slot | predicted | resolved_from_raw | resolved_at_pipeline | left_sentinel | validator_rejected |
|---|---:|---:|---:|---:|---:|
| `env_broad_scale` | 0 | 0 | 0 | 0 | **175** |
| `env_local_scale` | 0 | 0 | **105** | 0 | **70** |
| `env_medium` | 0 | 0 | **175** | 0 | 0 |

**This is the only study in the cohort with `validator_rejected` outcomes** — and they're principled, not failures.

- `env_broad_scale` rejected for all 175: pipeline-emitted `ENVO:01001001 plant-associated environment` fails the biome anchor check (it's not a biome). **There is no good ENVO biome term for an indoor EcoFAB microcosm setup** — this is the curator-follow-up backlog. Sentinel until ENVO adds an appropriate term or the curator decides on a fallback.
- `env_local_scale`:
  - **105 root samples** → kept `ENVO:00005801` rhizosphere (passes validators) as `resolved_at_pipeline`
  - **70 sterile-water mocks** → rejected `ENVO:01000621 microcosm` (it's under "manufactured product", not astronomical body part). Curator should choose an appropriate alternative.
- `env_medium` accepted for all 175:
  - 105 root: `ENVO:01000349 root matter`
  - 70 mocks: `ENVO:00005791 sterile water`

## Notable design

This is a **global multi-lab reproducibility study** — labs A/B/C/D (or similar) participated using standardized EcoFAB 2.0 plant growth devices. The participating-lab identifier is the primary independent variable. NMDC carries it only embedded in `samp_name` (e.g., `LabA_01_Axe_1`); the bermap profile's `LaboratorySiteEnum` placeholder ("four participating laboratories") should be reified.

## Caveats

- **12 mock samples have no DataGeneration**: pipeline emitted 163 DataGenerations for 175 Biosamples.
- **`samp_taxon_id` for the 70 mocks is dubious**: pipeline assigned `NCBITaxon:1118232 root metagenome`. Sterile water is not a root metagenome. The curation report doesn't track `samp_taxon_id` so this wasn't fixed in this pass.
- **No good ENVO biome for indoor lab work**: the 175 `validator_rejected` broad-scale rows are not fixable without a new ENVO term or a curator policy decision.

## Open items not handled by this pass

- Participating lab identifiers: reify from `samp_name` parse
- Mock sample taxon: clean up `samp_taxon_id = root metagenome` for sterile water samples
- EcoFAB growth-system enum: bermap's placeholder needs the actual list
