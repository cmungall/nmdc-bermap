# Agentic ingest snapshot — sty-11-kfvmk798

Frozen output from running [`nmdc-ingest-agent`](https://github.com/microbiomedata/nmdc-ingest-agent) against `PRJNA784967` (Populus trichocarpa chronic drought, PI Melissa Cregger).

**Study profile**: [`../../../schemas/studies/sty-11-kfvmk798.yaml`](../../../schemas/studies/sty-11-kfvmk798.yaml)
**Cross-source QC audit**: [`../../../schemas/studies/sty-11-kfvmk798.qc.md`](../../../schemas/studies/sty-11-kfvmk798.qc.md)
**Ingest date**: 2026-06-19
**Tool**: `nmdc-ingest-agent` 0.1.0
**ID shoulder**: `99` (placeholder)

## Sample-count context

NCBI deposit carries **384 biosamples** (= 192 physical samples × 2 amplicon assays: 16S + ITS). NMDC currently has only 64 — see qc.md for the discrepancy.

## Files

| File | Bytes | What |
|---|---:|---|
| `PRJNA784967.nmdc.json` | 1.2 MB | NMDC-schema `Database` — 384 biosamples |
| `PRJNA784967.curation_inputs.json` | 287 KB | NCBI title + raw attributes sidecar |
| `PRJNA784967.curation_report.json` | 429 KB | per-(biosample, slot) outcomes |

## Curation outcomes

| Slot | predicted | resolved_from_raw | resolved_at_pipeline | left_sentinel | validator_rejected |
|---|---:|---:|---:|---:|---:|
| `env_broad_scale` | 0 | **384** | 0 | 0 | 0 |
| `env_local_scale` | 0 | **384** | 0 | 0 | 0 |
| `env_medium` | **384** | 0 | 0 | 0 | 0 |

**Zero sentinels, zero rejections.** Submitter provided usable raw values for broad/local; agent committed via §1a resolution. Medium predicted from `isolation_source` decoding (128 rhizosphere / 128 root endosphere / 128 bulk soil).

- `env_broad_scale = ENVO:01000221` (temperate woodland biome) for all 384 — agent committed despite the Boardman common-garden context being a defensible alternative; raw value was "common garden"
- `env_local_scale = ENVO:00000011` (garden) for all 384
- `env_medium`:
  - **128 rhizosphere** (`ENVO:00005801`)
  - **128 root tissue** → `ENVO:01001121` (plant matter) — ENVO has no dedicated root-endosphere material; flagged for curator
  - **128 bulk soil** (`ENVO:00005802`)

The pipeline thus separates rhizosphere / root / bulk soil whereas the parallel NMDC ingest collapses all 64 samples to a single `env_medium = ENVO:00005801 rhizosphere`.

## Open items not handled by this pass

- **Host taxon**: NCBI carries `host = Populus trichocarpa` per biosample — could ground to `NCBITaxon:3694` on a follow-up pass. Agent flagged but did not commit.
- **Drought tolerance class** and **irrigation regime** are in NMDC's `other_treatment` field (`host common name: poplar; irrigation: full_irrigation`) and in NCBI sample attributes — neither was lifted into a structured slot.
- ENVO needs a "root endosphere material" term (current best fit: `plant matter`).
