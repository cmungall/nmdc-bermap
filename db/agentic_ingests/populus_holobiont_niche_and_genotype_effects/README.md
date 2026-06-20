# Agentic ingest snapshot — Populus Holobiont Niche and Genotype Effects

Frozen output from running [`nmdc-ingest-agent`](https://github.com/microbiomedata/nmdc-ingest-agent) (deterministic step) against the NCBI BioProject(s) backing this study.

**Ingest date:** 2026-06-19
**Tool:** `nmdc-ingest-agent` 0.1.0 (deterministic CLI)
**ID shoulder:** `99` (placeholder — re-run with `--mint-real-ids` to promote)

## Files

| File | Biosamples | What |
|---|---:|---|
| `PRJNA385484.nmdc.json` | 300 | NMDC `Database` JSON |
| `PRJNA384978.nmdc.json` | 290 | NMDC `Database` JSON |

Plus matching `.curation_inputs.json` and `.curation_report.json` sidecars per BioProject.

## Curation status

**Deterministic pass only.** ENVO env-triad sentinels (`ENVO:00000000`) remain. The `/ncbi-to-nmdc` skill workflow has not been run on these BioProjects. See [`docs/data_quality_pattern.md`](../../../docs/data_quality_pattern.md) for how to complete curation.

## Regen

```bash
cd ~/nmdc-ingest-agent && uv sync
uv run nmdc-ingest-ncbi PRJNA385484 --out PRJNA385484.json
uv run nmdc-ingest-ncbi PRJNA384978 --out PRJNA384978.json
```

## Curation pass (2026-06-20)

Full `/ncbi-to-nmdc` skill workflow run; env_triad slots committed where evidence supported, `left_sentinel` / `validator_rejected` otherwise. Per-(biosample, slot) outcomes in the `.curation_report.json` sidecar.

Outcome counts per BioProject:

| BioProject | Slot | predicted | resolved_from_raw | resolved_at_pipeline | left_sentinel | validator_rejected |
|---|---|---:|---:|---:|---:|---:|
| `PRJNA384978` | `env_broad_scale` | – | 290 | – | – | – |
| `PRJNA384978` | `env_local_scale` | – | – | – | – | 290 |
| `PRJNA384978` | `env_medium` | – | 290 | – | – | – |
| `PRJNA385484` | `env_broad_scale` | – | 300 | – | – | – |
| `PRJNA385484` | `env_local_scale` | – | – | – | – | 300 |
| `PRJNA385484` | `env_medium` | – | 300 | – | – | – |

See [../CURATION_REPORT.md](../CURATION_REPORT.md) for the consolidated cross-batch analysis (cross-cutting issues, anchor failures, ontology gaps).
