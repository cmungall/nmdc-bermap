# Agentic ingest snapshot — sty-11-vh2hty57

Frozen output from running [`nmdc-ingest-agent`](https://github.com/microbiomedata/nmdc-ingest-agent) against `PRJNA601860` (CABBI Miscanthus × Corn chronosequence, Iowa State, PI Adina Howe).

**Study profile**: [`../../../schemas/studies/sty-11-vh2hty57.yaml`](../../../schemas/studies/sty-11-vh2hty57.yaml)
**Cross-source QC audit**: [`../../../schemas/studies/sty-11-vh2hty57.qc.md`](../../../schemas/studies/sty-11-vh2hty57.qc.md)
**Ingest date**: 2026-06-19
**Tool**: `nmdc-ingest-agent` 0.1.0 (deterministic CLI + skill workflow)
**ID shoulder**: `99` (placeholder — re-run with `--mint-real-ids` to promote)

## Files

| File | Bytes | What |
|---|---:|---|
| `PRJNA601860.nmdc.json` | 2.1 MB | NMDC-schema `Database` — 648 biosamples, all 3 env-triad slots fully `predicted` from `samp_name` parse |
| `PRJNA601860.curation_inputs.json` | 497 KB | NCBI title + raw attributes sidecar |
| `PRJNA601860.curation_report.json` | 713 KB | per-(biosample, slot) outcomes |

## Curation outcomes

| Slot | predicted | resolved_from_raw | resolved_at_pipeline | left_sentinel | validator_rejected |
|---|---:|---:|---:|---:|---:|
| `env_broad_scale` | **648** | 0 | 0 | 0 | 0 |
| `env_local_scale` | **648** | 0 | 0 | 0 | 0 |
| `env_medium` | **648** | 0 | 0 | 0 | 0 |

**Zero sentinels, zero rejections** — cleanest curation in the cohort. Agent decoded `samp_name` `<num>_<crop>_<yr>_P<plot>_N<n>_[<rep>_]<date>_CABBI` to classify each sample, then committed:

- `env_broad_scale = ENVO:01000245` (cropland biome) for all 648
- `env_local_scale = ENVO:00005749` (farm soil) for all 648
- `env_medium`:
  - **486 rhizosphere** (`ENVO:00005801`) — `samp_name` rep ∈ {A, B, C}
  - **162 bulk soil** (`ENVO:00005802`) — 7-part names without rep letter, pre-planting 2018-04-25 timepoint

This recovers the env_medium discrepancy flagged in the parallel NMDC ingest (where all 696 are uniformly bulk soil) — see the qc.md.

## Open items not handled by this pass

- **Host taxon**: NCBI carries `Plant=Miscanthus` (468) / `Plant=Corn` (180) — could ground to `NCBITaxon:183674 (Miscanthus × giganteus)` and `NCBITaxon:4577 (Zea mays)` on a follow-up pass. The agent flagged this but did not commit since the curation report doesn't track host slots.
- The 48 bulk-soil samples in NMDC that are NOT in PRJNA601860 (CABBI-specific deposits) are not in this snapshot — they only live in the parallel NMDC ingest.
- Placeholder IDs. Re-run with `--mint-real-ids` to promote.

## How to regenerate

```bash
cd ~/nmdc-ingest-agent
uv sync
uv run nmdc-ingest-ncbi PRJNA601860 --out PRJNA601860.json
# Then run /ncbi-to-nmdc in a Claude Code session
```
