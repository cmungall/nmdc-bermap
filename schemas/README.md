# Per-study LinkML data-dictionary profiles

Each study's variable catalog is expressed here as a small, real LinkML schema (a
"data-dictionary profile"). Because each profile is genuine LinkML, `gen-doc`,
`gen-pydantic`, `linkml-validate`, and lint all work on it directly.

Design spec: [`docs/superpowers/specs/2026-06-13-per-study-linkml-profiles-design.md`](../docs/superpowers/specs/2026-06-13-per-study-linkml-profiles-design.md).

## Layout

```
schemas/
  base.yaml                       # hand-authored: shared slots + DYNAMIC, vocabulary-governed enums
  studies/<study_id>.yaml         # generated: one data-dictionary per study (×81), imports base
  studies/<study_id>.sssom.yaml   # generated: that study's ontology mappings (SSSOM MappingSet)
  sites/<site_id>.yaml            # generated: per-site environmental context (×40), imports base
  sssom-profile.yaml              # minimal SSSOM LinkML profile used to validate the mapping tables
  level_meanings.yaml             # curated, OLS-verified level-text -> CURIE groundings
  generate_profiles.py            # forward: db/sfas-brcs.yaml -> profiles + SSSOM
  generate_variables.py           # reverse: profiles + SSSOM -> variables (the SoT flip)
  validate_profiles.py            # loads each profile via SchemaView; checks imports + ranges
```

`<study_id>` is the NMDC study id local part (e.g. `sty-11-e4yb9z58`) or a slug of the
study name. The unit is the **study**; datasets reference the study profile they conform to.

## Mappings live in SSSOM, not in the schema

Slot → ontology mappings (the variables' `mixs_terms`/`bervo_term`/`unit_term`/`ontology_mappings`)
are **not** inline in the profiles. Each study gets a sibling `*.sssom.yaml` (an SSSOM
`MappingSet`): rows of `subject_id` (the profile slot), `predicate_id`, `object_id`, and
**`object_label`**. Keeping the labels here makes the mappings (a) cleanly separated from the
schema, (b) round-trippable back into the DB's `{id, label}` objects, and (c) validatable —
`just validate-profile-mappings` runs `linkml-term-validator` so every `object_label` must match
`object_id`'s ontology label (or an exact synonym). The source bucket is recovered on the reverse
trip from the object CURIE prefix (`MIXS:`→mixs_terms, `BERVO:`→bervo_term, `UO:`→unit_term,
else→ontology_mappings).

## Conventions

- **Static enum** — lists `permissible_values`, optionally with `meaning:` (an ontology CURIE).
  Used for study-specific categorical levels (e.g. `host crop` → switchgrass/miscanthus).
- **Dynamic enum** — has `reachable_from` (an ontology subtree) or an `annotations.source`
  (an external governing vocabulary). Members are not enumerated. Defined once in `base.yaml`
  (`EnvBroadScaleEnum`, `EnvLocalScaleEnum`, `EnvMediumEnum`, `HostCommonNameEnum`,
  `GoldEcosystemPathEnum`, `EnvPackageEnum`) and reused by every study by import.
- **No NMDC import.** Linkage to MIxS/ENVO/NCBITaxon/GOLD is by SSSOM mappings and
  `reachable_from` only — profiles stay small and hand-authorable.
- Each curated `Variable` facet maps to a LinkML slot facet (range, `unit`, `aliases`
  = source field names, `annotations.role`/`value_type`/`time_series`/etc.); ontology mappings
  go to the SSSOM table. See the spec for the full mapping table.

## Source of truth

The inline `variables` catalog in `db/sfas-brcs.yaml` remains authoritative for now (decision
i-a, "coexist"), but the **reverse generator proves the profiles + SSSOM are a complete,
lossless representation**: `just sync-variables --check` reconstructs every study's `variables`
from `profiles + SSSOM` and confirms **81/81 studies are byte-for-byte identical** to the DB. That
is what makes flipping the Source of Truth (edit profiles → regenerate the DB block) provably safe.
`base.yaml` is hand-authored and never overwritten. Level `meaning:` groundings are harvested from
the DB's own `ontology_mappings`/`bervo_term` plus the curated `level_meanings.yaml`.

## Regenerate / validate

```bash
just gen-profiles              # forward: rebuild profiles + *.sssom.yaml from the DB
just sync-variables --check    # reverse: prove profiles + SSSOM round-trip to the DB variables
just validate-profiles         # load every profile via SchemaView; verify imports + ranges resolve
just validate-profile-terms    # vet enum permissible-value meaning: CURIEs against ontologies (OAK)
just validate-profile-mappings # vet every SSSOM object_label against object_id's ontology label
```

`validate-profile-terms` runs `linkml-term-validator` (strict) over every profile that carries
`meaning:` fields, confirming each CURIE resolves to a term whose label matches the level text.
This is what guarantees the groundings are real — it caught a wrong seed (`miscanthus` →
`NCBITaxon:62324`, which is *Anopheles funestus*) during initial curation. Because it checks
label equality (not common-name synonyms), `level_meanings.yaml` only grounds level texts that
match a term label; common names like `switchgrass` are left to the dynamic `HostCommonNameEnum`.

## Current coverage

81 study profiles (540 slots, 54 static enums, 145 permissible values) + 40 site profiles.
60 slots bind to the shared dynamic enums; **48 of 145 permissible values carry an ontology
`meaning:`** (across NCBITaxon/ENVO/PO/CHEBI), every one passing `just validate-profile-terms`.
Grounding grows by extending the curated, verified `level_meanings.yaml`.
