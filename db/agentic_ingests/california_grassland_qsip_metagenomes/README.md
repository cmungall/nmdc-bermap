# Agentic ingest snapshot — California Grassland qSIP Metagenomes

**Status: ingest blocked by upstream bug**

Tried to ingest PRJNA718849 via [`nmdc-ingest-agent`](https://github.com/microbiomedata/nmdc-ingest-agent) 0.1.0 on 2026-06-19. Failed with:

```
ValueError: has_unit must be supplied
```

The NMDC `QuantityValue` class requires a `has_unit` field; the agent's NCBI translator emits a `QuantityValue` for some BioSample attribute (likely a numeric depth or concentration) without populating `has_unit`. The downstream `linkml_runtime` strict validation rejects the construction.

This is a real bug in `nmdc-ingest-agent` that needs upstream fixing — either default `has_unit` to the source unit string, or fall back to a free-text wrapper when no unit is parseable.

## Workaround options

1. **Fix nmdc-ingest-agent**: trace which attribute triggers the `QuantityValue` without unit, then either populate it or wrap as `TextValue`.
2. **Skip this BioProject**: NMDC doesn't have this study, so the snapshot would only be exploratory anyway.

## To regenerate (once upstream fixed)

```bash
cd ~/nmdc-ingest-agent && uv sync
uv run nmdc-ingest-ncbi PRJNA718849 --out PRJNA718849.json
```
