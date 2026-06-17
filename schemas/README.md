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

## Source of truth — the profiles + SSSOM (single SoT)

**Variables live ONLY here.** The inline `db.variables` catalog has been dropped (DB shrank by
~7,250 lines), so there is exactly one place to edit each kind of data:

- a study/dataset **variable** (its mappings, levels, groundings) → edit `schemas/{studies,datasets}/<id>.yaml`
  (+ `<id>.sssom.yaml` for ontology mappings, `level_meanings.yaml` for level groundings), then
  `just gen-variable-index`;
- a **program / study / dataset / site** (structure, descriptions, PIs) → edit `db/sfas-brcs.yaml`.

Every study and dataset that has variables gets a profile (81 + 3). `base.yaml` is hand-authored.

`schemas/variable-index.yaml` is the **single producer** of all variable-derived data:
per-owner variables (`studies`/`datasets`), a `by_term` inverted index, and the flat
`variable_index` view (records + BERVO/MIxS groupings) the variable pages render. **All HTML is a
render of the union of `db/sfas-brcs.yaml` (programs/studies/datasets/sites) and this index** —
`generate_html_browser.py` derives no variable structures of its own. The NMDC sample-attribute
validator also sources study variables from the index.

> `gen-profiles` was the one-time **bootstrap** (db.variables → profiles). It now refuses to run
> (the DB has no inline variables) so it can't clobber the hand-authored profiles. Don't run it.

How we got here safely: the reverse generator reconstructed every owner's `variables` from
profiles + SSSOM and proved **84/84 owners byte-identical** to the DB before the drop.

## Regenerate / validate

```bash
just gen-variable-index        # build schemas/variable-index.yaml from the profiles + SSSOM (SoT)
just gen-browser               # re-render docs (reads the index)
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

81 study + 3 dataset profiles (547 slots, 547 variables, 55 static enums) + 40 site profiles.
Slots bind to the shared dynamic enums; **~48 permissible values carry an ontology `meaning:`**
(across NCBITaxon/ENVO/PO/CHEBI), every one passing `just validate-profile-terms`. Grounding grows
by extending the curated, verified `level_meanings.yaml`.
