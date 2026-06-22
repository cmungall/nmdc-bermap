# Agentic ingest snapshot — Bioreactor Fermentation Microbiomes

Frozen output from running [`nmdc-ingest-agent`](https://github.com/microbiomedata/nmdc-ingest-agent) (deterministic step) against the NCBI BioProject(s) backing this study.

**Ingest date:** 2026-06-19
**Tool:** `nmdc-ingest-agent` 0.1.0 (deterministic CLI)
**ID shoulder:** `99` (placeholder — re-run with `--mint-real-ids` to promote)

## Files

| File | NMDC biosamples | NCBI biosamples | What |
|---|---:|---:|---|
| `PRJNA1159295.nmdc.json` | 0 | 42 (all MIMAG) | NMDC `Database` JSON — MAG biosamples excluded by agent |
| `PRJNA1040840.nmdc.json` | 0 | 122 (all MIMAG; ~366 linked total) | NMDC `Database` JSON — MAG biosamples excluded by agent |
| `PRJNA768492.nmdc.json` | 0 | 0 in NCBI BioSample registry | NMDC `Database` JSON — truly empty BioProject |

Plus matching `.curation_inputs.json` and `.curation_report.json` sidecars per BioProject.

## Why 0 NMDC biosamples

This study is about **microbial communities fermenting agroindustrial residues**, and the BioProjects PRJNA1040840 and PRJNA1159295 collectively contain **164+ Metagenome-Assembled Genome (MAG) deposits** under the MIxS `MIMAG.miscellaneous.6.0` package. The nmdc-ingest-agent's deterministic pipeline deliberately excludes MAG-only biosamples:

```
Excluded N BioSample(s) using MAG-only MIxS packages (MIMAG.miscellaneous.6.0=N);
NMDC Biosample is for environmental samples.
```

The NMDC `Biosample` class represents **environmental / physical** samples, not computational genome assemblies. MAGs are downstream products derived from environmental samples (the parent BioSamples carry `derived-from SAMN...` pointers); in NMDC's data model they belong to `MetagenomeAssembly` or `MagBin` collections instead.

The third BioProject PRJNA768492 has no BioSample records at all in the NCBI BioSample registry — just SRA/Assembly deposits without registered biological samples.

Concrete result: no NMDC ingest is possible for this bermap study via `nmdc-ingest-agent` 0.1.0. The MAG metadata is rich (each carries pH, temperature, dissolved oxygen, geo_loc_name, isolation_source for the parent bioreactor, etc.) and would be valuable in NMDC if a future ingestion path for MAGs / MetagenomeAssemblies is added — see, e.g., SAMN38266644's parent environmental sample SAMN38199233.

The included `*.nmdc.json` files contain only the study record (no biosamples / data_generations / data_objects).

## Curation status

**N/A** — no biosamples to curate. Curation reports are empty by construction.

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
