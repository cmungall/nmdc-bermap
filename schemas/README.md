# Per-study LinkML data-dictionary profiles

Each study's variable catalog is expressed here as a small, real LinkML schema (a
"data-dictionary profile"). Because each profile is genuine LinkML, `gen-doc`,
`gen-pydantic`, `linkml-validate`, and lint all work on it directly.

Design spec: [`docs/superpowers/specs/2026-06-13-per-study-linkml-profiles-design.md`](../docs/superpowers/specs/2026-06-13-per-study-linkml-profiles-design.md).

## Layout

```
schemas/
  base.yaml                  # hand-authored: shared slots + DYNAMIC, vocabulary-governed enums
  studies/<study_id>.yaml    # generated: one data-dictionary per study (×81), imports base
  sites/<site_id>.yaml       # generated: per-site environmental context (×40), imports base
  generate_profiles.py       # generator (db/sfas-brcs.yaml -> profiles)
  validate_profiles.py       # loads each profile via SchemaView; checks imports + ranges
```

`<study_id>` is the NMDC study id local part (e.g. `sty-11-e4yb9z58`) or a slug of the
study name. The unit is the **study**; datasets reference the study profile they conform to.

## Conventions

- **Static enum** — lists `permissible_values`, optionally with `meaning:` (an ontology CURIE).
  Used for study-specific categorical levels (e.g. `host crop` → switchgrass/miscanthus).
- **Dynamic enum** — has `reachable_from` (an ontology subtree) or an `annotations.source`
  (an external governing vocabulary). Members are not enumerated. Defined once in `base.yaml`
  (`EnvBroadScaleEnum`, `EnvLocalScaleEnum`, `EnvMediumEnum`, `HostCommonNameEnum`,
  `GoldEcosystemPathEnum`, `EnvPackageEnum`) and reused by every study by import.
- **No NMDC import.** Linkage to MIxS/ENVO/NCBITaxon/GOLD is by `slot_uri`/`exact_mappings`
  and `reachable_from` only — profiles stay small and hand-authorable.
- Each curated `Variable` facet maps to a LinkML slot facet (range, `unit`, `aliases`
  = source field names, `exact_mappings`/`slot_uri` = MIxS/BERVO terms, `annotations.role`,
  etc.). See the spec for the full mapping table.

## Source of truth

The inline `variables` catalog in `db/sfas-brcs.yaml` remains authoritative; these profiles
are a **regenerable artifact** (decision i-a, "coexist"). `base.yaml` is hand-authored and is
never overwritten by the generator. Ontology groundings (level `meaning:`s) are harvested from
the database's own existing `ontology_mappings`/`bervo_term` plus a small verified seed set, and
grow over time — ungrounded levels are emitted as text-only permissible values.

## Regenerate / validate

```bash
just gen-profiles        # rebuild schemas/studies/*.yaml and schemas/sites/*.yaml
just validate-profiles   # load every profile via SchemaView; verify imports + ranges resolve
```

## Current coverage

81 study profiles (540 slots, 54 static enums, 145 permissible values) + 40 site profiles.
60 slots bind to the shared dynamic enums; **51 of 145 permissible values carry an ontology
`meaning:`** (27 distinct terms across NCBITaxon/ENVO/PO/CHEBI), all OLS-verified. Grounding
grows by extending the curated, verified `level_meanings.yaml`.
