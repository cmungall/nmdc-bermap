# Capturing cross-source discrepancies (data quality pattern)

When a study's representation diverges between sources — submitter, NCBI/EBI BioSample, NMDC, and the bermap profile — capture the discrepancy at the level it belongs to. Don't over-engineer: three lightweight hooks, used selectively.

## The three hooks

### 1. Study-level — `study.ncbi_data_quality_notes` in `db/sfas-brcs.yaml`

One paragraph per study. Use for divergences about scope or scale that can't be pinned to a single variable:

- Sample-count divergence between sources (e.g., NMDC has N samples, NCBI has M)
- Description / abstract gaps (study description omits a comparator that's in the data)
- Whole-pipeline curation patterns (ingest flattening, dropped attributes)

Always end with a pointer to the sibling `<study-id>.qc.md` when one exists. Datestamp the audit so future readers can judge staleness.

Worked example: see `db/sfas-brcs.yaml` study entry for `nmdc:sty-11-vh2hty57`.

### 2. Per-variable — `annotations.data_source_notes` on profile slots

One tight sentence per affected slot in `schemas/studies/<study-id>.yaml`. Use for representation issues that travel with the variable:

- "Profile slot is correct; ingest is mislabeled" (and how to recover)
- "Stored as string in NMDC; parse for numeric"
- "Derived — no NMDC source column; recovery recipe"

The key is a free-form custom annotation. The variable-index generator passes it through without complaint, but doesn't validate against the LinkML schema. Datestamp it.

Worked example: see `environmental_medium`, `stand_age`, `nitrogen_fertilizer_rate` slots in `schemas/studies/sty-11-vh2hty57.yaml`.

### 3. Sibling diff file — `schemas/studies/<study-id>.qc.md`

Reserve for studies where the cross-source story is genuinely tangled. Skip for studies with no real issues.

Recommended sections:
- Header with NMDC ID, BioProject, DOI, PI, audit date
- Sample-count divergence table
- Study-description gap table (NMDC portal vs NCBI vs bermap vs deposited data)
- Per-variable three-way (or four-way, counting bermap) diff table
- ASCII data-flow diagram showing how the sources relate (NMDC ←/→ NCBI ←/→ submitter)
- Known limitations of the audit

Worked example: `schemas/studies/sty-11-vh2hty57.qc.md`.

### 4. Frozen ingest snapshots — `db/agentic_ingests/<study-id>/`

Optional fourth hook. When the QC.md references the output of a re-ingest tool (e.g., `nmdc-ingest-agent` re-pulling from NCBI), keep the output files under `db/agentic_ingests/<study-id>/` so the QC.md's claims are auditable against frozen artifacts. Follows the same data-vs-schema separation as the existing `db/brc_datasets/<center>/` pattern.

Each subdirectory should contain a `README.md` documenting:
- What ingestion produced the files (tool, version, date)
- What's in each file (and what to ignore)
- Regen recipe
- Caveats for downstream consumers (placeholder IDs, known gaps)

Worked example: `db/agentic_ingests/sty-11-wbc14h22/` (NCBI BioProjects PRJNA733109 / 733505 / 733764, curated via `nmdc-ingest-agent` + skill workflow).

## When to add each hook

| Discrepancy type | Hook |
|---|---|
| Sample count mismatch across sources | 1 (study-level) |
| Study description omits a population in the data | 1 (study-level) |
| Variable is mislabeled / overspecialized in one source | 2 (per-variable) |
| Variable is stored as string when it should be numeric | 2 (per-variable) |
| Variable has no source column — must be derived | 2 (per-variable) |
| Multiple intertwined discrepancies + back-references between them | 3 (QC.md) |
| Re-ingest produces a snapshot worth comparing against current NMDC state | 4 (frozen ingest under `db/agentic_ingests/`) |

A study can have any subset of the four hooks. Don't add a hook just to have one.

## Maintenance

These notes will rot as ingest pipelines fix issues upstream. Mitigations:

- **Datestamp** every entry (`Audit 2026-06-17`)
- Keep entries **short and observational**, not prescriptive — record what's wrong, not how to fix it (the fix belongs in an issue or PR)
- When an upstream fix lands, **remove the note rather than annotating it as resolved** — `git log` retains the history

If a study's QC.md grows past ~200 lines, consider splitting per-variable detail back into slot annotations and keeping the QC.md as a top-of-table summary.
