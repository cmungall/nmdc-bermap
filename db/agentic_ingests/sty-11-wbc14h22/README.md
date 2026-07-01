# Agentic ingest snapshot — sty-11-wbc14h22

Frozen output from running [`nmdc-ingest-agent`](https://github.com/microbiomedata/nmdc-ingest-agent) against the three NCBI BioProjects backing NMDC study `nmdc:sty-11-wbc14h22` (GLBRC Marginal Lands Experiment / MMPRNT cohort).

**Study profile**: [`../../../schemas/studies/sty-11-wbc14h22.yaml`](../../../schemas/studies/sty-11-wbc14h22.yaml)
**Cross-source QC audit (cites this snapshot)**: [`../../../schemas/studies/sty-11-wbc14h22.qc.md`](../../../schemas/studies/sty-11-wbc14h22.qc.md)

**Ingest date**: 2026-06-18
**Tool version**: `nmdc-ingest-agent` 0.1.0 (deterministic CLI + agent-driven skill curation)
**ID shoulder**: `99` (placeholder — not ingestable; re-run with `--mint-real-ids` to promote)

## What's here

Three sets of files, one per BioProject:

| File | Bytes | What it is |
|---|---:|---|
| `PRJNA<acc>.nmdc.json` | 2.8–3.1 MB | NMDC-schema-compliant `Database` JSON. The curated artifact — biosamples carry committed ENVO triad terms where the agent could infer them and `ENVO:00000000` sentinels where it correctly refused to guess. Validates against `nmdc_schema.Database`. |
| `PRJNA<acc>.curation_inputs.json` | ~540 KB | Per-biosample sidecar holding the full NCBI title, MIxS package, and raw attribute dump that the curation skill consumed. Input to the curation step. |
| `PRJNA<acc>.curation_report.json` | 1.4–2.3 MB | One row per (biosample, slot) for the env triad, recording `outcome` (`predicted` / `resolved_from_raw` / `resolved_at_pipeline` / `left_sentinel` / `validator_rejected`), `committed_curie`, `committed_label`, `evidence`, `candidates_considered`, and validator status. The deliverable for downstream curators. |

Plus the agent's curation script:

| File | What |
|---|---|
| `curate.py` | The Python script the agent wrote to apply env-triad §1b inference rules from `.claude/skills/nmdc-env-triad.md`, with plot/site context drawn from `biosample.ncbi_title` where parseable. Records validated ENVO CURIEs and their anchor-class checks inline. Kept here for transparency about what the agent committed. |

## Source BioProjects

| Accession | Year | NCBI title | Biosample count (agent) | Biosample count (NMDC) | Title pattern |
|---|:-:|---|:-:|:-:|---|
| `PRJNA733109` | 2016 | Soil bacterial communities of Switchgrass and other biofuel grasses (MI/WI) | 873 | 864 | 864 with structured title `1_<MMDDYY>_MMPRNT_<site>_<plot>_rep<n>_<Fert\|Unfert>_pseudo<n>`; 9 controls |
| `PRJNA733505` | 2017 | …(2017) | 978 | 942 | Mostly bare `MMPRNT-NNNN` field IDs |
| `PRJNA733764` | 2018 | Soil **and root** bacterial communities …(2018) | 886 | 870 | Mostly bare `MMPRNT-NNNN` field IDs |

The 61-sample gap between agent (2,737) and NMDC ingest (2,676) is fully accounted for by ZymoBiomics mock standards and technical re-runs that NMDC drops; the QC.md has the full breakdown.

## What the curation pass did

See the consolidated outcomes table and per-sample diff in `../../../schemas/studies/sty-11-wbc14h22.qc.md` § "Agent curation pass". Headline:

- **864 structured-title 2016 samples** got full env-triad commits, with plot-type-aware divergence (G5 → cropland/agricultural field/farm soil; G10/G11 → grassland/grassland area/grassland soil)
- **876 of 886 2018 samples** got `env_medium = soil [ENVO:00001998]` committed from `isolation_source = "Switchgrass Soils"`; broad/local left as honest sentinels pending OSF crosswalk
- **1,836 MMPRNT-NNNN samples** (2017 + most 2018) have broad/local scale `left_sentinel` — plot/site mapping needs the OSF supplement (`MMPRNT_2018.metadata_mapp_coverage.csv` at https://osf.io/5vw9c/) to clear
- **17 mock / kit / unknown-control samples** intentionally left sentinel (synthetic, not environmental)

All three `*.nmdc.json` pass LinkML validation against `nmdc_schema.Database`.

## How to regenerate

From a checkout of `nmdc-ingest-agent` synced with `uv`:

```bash
cd ~/nmdc-ingest-agent
uv sync

mkdir -p /tmp/wbc_ingest
for bp in PRJNA733109 PRJNA733505 PRJNA733764; do
  uv run nmdc-ingest-ncbi $bp --out /tmp/wbc_ingest/${bp}.json
done
```

That produces the deterministic step (`*.json` + `*_curation_inputs.json` + an unfilled `*_curation_report.json`). The skill-based curation step is then driven from a Claude Code session inside the repo by invoking `/ncbi-to-nmdc` per accession; see [`nmdc-ingest-agent`'s README](https://github.com/microbiomedata/nmdc-ingest-agent#usage). To promote to real NMDC IDs, set `NMDC_RUNTIME_CLIENT_ID` / `NMDC_RUNTIME_CLIENT_SECRET` and add `--mint-real-ids`.

## Caveats for downstream consumers

- **Placeholder IDs**: every `nmdc:bsm-99-…`, `nmdc:sty-99-…`, `nmdc:dgns-99-…` here is a placeholder. The `99` shoulder is reserved for non-canonical IDs. Do not ingest.
- **2017/2018 broad/local-scale backlog**: `MMPRNT-NNNN` samples can't be resolved without joining against the OSF supplement. The agent correctly refuses to guess; downstream curators should plan to clear ~1,836 (biosample × 2 slots) by hand or with a crosswalk script.
- **2018 root subset**: the 2018 BioProject title is "Soil **and** root" but every `isolation_source` says "Switchgrass Soils". If a root subset exists, `env_medium = soil` is wrong for those samples.
- **MIxS soil-package valueset not enforced**: NCBI packages are `Metagenome.environmental.1.0`, not the MIxS soil package, so the soil-package allowed-term constraint was not applied. `nmdc-submission-schema` was not consulted.
- **`Sequecing_run`** typo on the NCBI side is preserved verbatim in `curation_inputs.json`.
