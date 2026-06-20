# Agentic ingest snapshot — Bioreactor Fermentation Microbiomes

Frozen output from running [`nmdc-ingest-agent`](https://github.com/microbiomedata/nmdc-ingest-agent) (deterministic step) against the NCBI BioProject(s) backing this study.

**Ingest date:** 2026-06-19
**Tool:** `nmdc-ingest-agent` 0.1.0 (deterministic CLI)
**ID shoulder:** `99` (placeholder — re-run with `--mint-real-ids` to promote)

## Files

| File | Biosamples | What |
|---|---:|---|
| `PRJNA1159295.nmdc.json` | 0 | NMDC `Database` JSON |
| `PRJNA1040840.nmdc.json` | 0 | NMDC `Database` JSON |
| `PRJNA768492.nmdc.json` | 0 | NMDC `Database` JSON |

Plus matching `.curation_inputs.json` and `.curation_report.json` sidecars per BioProject.

## Curation status

**Deterministic pass only.** ENVO env-triad sentinels (`ENVO:00000000`) remain. The `/ncbi-to-nmdc` skill workflow has not been run on these BioProjects. See [`docs/data_quality_pattern.md`](../../../docs/data_quality_pattern.md) for how to complete curation.

## Regen

```bash
cd ~/nmdc-ingest-agent && uv sync
uv run nmdc-ingest-ncbi PRJNA1159295 --out PRJNA1159295.json
uv run nmdc-ingest-ncbi PRJNA1040840 --out PRJNA1040840.json
uv run nmdc-ingest-ncbi PRJNA768492 --out PRJNA768492.json
```

## Curation pass (2026-06-20)

Full `/ncbi-to-nmdc` skill workflow run; env_triad slots committed where evidence supported, `left_sentinel` / `validator_rejected` otherwise. Per-(biosample, slot) outcomes in the `.curation_report.json` sidecar.

Outcome counts per BioProject:

| BioProject | Slot | predicted | resolved_from_raw | resolved_at_pipeline | left_sentinel | validator_rejected |
|---|---|---:|---:|---:|---:|---:|
| `PRJNA1040840` | `env_broad_scale` | – | – | – | – | – |
| `PRJNA1040840` | `env_local_scale` | – | – | – | – | – |
| `PRJNA1040840` | `env_medium` | – | – | – | – | – |
| `PRJNA1159295` | `env_broad_scale` | – | – | – | – | – |
| `PRJNA1159295` | `env_local_scale` | – | – | – | – | – |
| `PRJNA1159295` | `env_medium` | – | – | – | – | – |
| `PRJNA768492` | `env_broad_scale` | – | – | – | – | – |
| `PRJNA768492` | `env_local_scale` | – | – | – | – | – |
| `PRJNA768492` | `env_medium` | – | – | – | – | – |

See [../CURATION_REPORT.md](../CURATION_REPORT.md) for the consolidated cross-batch analysis (cross-cutting issues, anchor failures, ontology gaps).
