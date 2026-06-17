# Per-study LinkML data-dictionary profiles

**Date:** 2026-06-13
**Status:** Approved (brainstorming) → implementing

## Goal

Represent each study's variable catalog as a small, real LinkML schema (a "data-dictionary
profile") instead of recapitulating LinkML's enum/slot machinery inside the main
`nmdc_sfas_brcs.yaml` schema. Each profile is a genuine LinkML schema, so `gen-doc`,
`gen-pydantic`, `linkml-validate`, and lint all work on it for free.

The driving need is **ontology-grounded harmonization** of categorical variables:
- **static** study-specific levels (e.g. `host crop` → switchgrass/miscanthus) become real
  `enum`s whose `permissible_values` carry `meaning:` (ontology CURIEs);
- **dynamic** vocabulary-governed levels (e.g. `ecosystem`, `env_medium`, `host_common_name`)
  bind once, centrally, to their source vocabulary rather than being re-enumerated per study.

## Non-goals

- Not importing the full NMDC/MIxS schema (decision **ii**, light linkage only).
- Not retiring the inline `variables` catalog yet (decision **i-a**, coexist). The browser and
  existing validators continue to read `db/sfas-brcs.yaml`.
- Not grounding every level's `meaning:` in this pass. The generator emits text-only
  `permissible_values`; meanings are applied from a curated map and grown incrementally.

## Unit & layering

The unit is the **study** (81), matching where curated `variables` already live. Datasets are
thin pointers (no local attributes; 686 BRC files + 89 inline) so they are the wrong unit; they
reference the study profile they conform to. Sites (40) carry shared environmental context →
reusable mixin, not standalone dictionaries.

```
schemas/
  base.yaml                       # light NMDC/MIxS/ENVO linkage: shared slots + DYNAMIC enums
  sites/<site_id>.yaml      ×40   # per-site environmental-context mixin
  studies/<study_id>.yaml   ×81   # the data dictionary; imports base (+ its site)
  README.md                       # index + conventions
```

Heterogeneous datasets within a study (decision **A**): one profile per study, with **multiple
record `classes`** (e.g. `Biosample`, `FluxRecord`) when needed — not one file per dataset.
Default is a single record class.

## Variable → LinkML slot mapping

| `variables` facet | LinkML profile facet |
|---|---|
| `name` | slot key (slug) + `title:` (original name) |
| `description` | `description:` |
| `value_type` | `range:` — NUMERIC→`float`, INTEGER→`integer`, CATEGORICAL→`<Enum>` or `string`, BOOLEAN→`boolean`, DATETIME→`datetime`, TEXT→`string`, IDENTIFIER→`string` (`identifier: true`), ONTOLOGY_TERM→`uriorcurie`, ARRAY→`multivalued: true` (range `string`), OBJECT→`string` + `annotations.shape: object` |
| `units` | `unit:` `{descriptive_name: <label>, ucum_code: <code if known>}` |
| `levels` (static) | a generated `enum` → `permissible_values` (`text` + optional `meaning`) |
| governed field (dynamic) | `range:` a **base** enum (no per-study enumeration) |
| `mixs_terms`/`bervo_term`/`unit_term`/`ontology_mappings` | `exact_mappings:` (all); `slot_uri:` = most specific (skip generic `MIXS:0000008`) |
| `source_field_names` | `aliases:` |
| `roles` | `annotations: {role: "<; joined>"}` |
| `measured_entity`/`material_or_matrix`/`method`/`temporal_resolution`/`spatial_resolution` | `annotations` |

## `base.yaml` (hand-authored)

- `prefixes`: MIXS, ENVO, NCBITaxon, GOLD, OBI, UO, nmdc, plus the profile base URI.
- `imports: [linkml:types]` only. **No NMDC import.**
- Shared **slots** for recurring sample attributes (`collection_date`→`MIXS:0000011`,
  `depth`→`MIXS:0000018`, `lat_lon`, `elevation`, …) with `slot_uri`.
- **Dynamic enums** for governed categoricals, defined once:
  - ENVO-subtree enums via `reachable_from` (`source_ontology: obo:envo`, `source_nodes`,
    `relationship_types: [rdfs:subClassOf]`) — e.g. `EnvBroadScaleEnum`, `EnvMediumEnum`.
  - Vocabulary-governed enums that are not OBO trees (GOLD ecosystem path, MIxS
    `env_package`, NCBITaxon host names) represented as an `enum` with a
    `source` annotation (URI/name of the governing vocabulary) and left open
    (`permissible_values` empty) — i.e. dynamic by reference, not enumerated.

Convention: a **dynamic** enum is one with `reachable_from` or an `annotations.source`; a
**static** enum lists `permissible_values`.

## `studies/<id>.yaml` (generated)

`id` under `https://w3id.org/nmdc-sfas-brcs/profiles/studies/<id>`, `name` = slug of study name,
`title` = study name, `imports: [../base]` (+ `../sites/<site>` when the study has one
`field_site_id`; multiple sites → import all). `default_range: string`. One `classes:` record
(slots = the study's variables) plus extra record classes only when datasets are heterogeneous.
Study-specific `slots:` and static `enums:` as per the mapping table.

## `sites/<id>.yaml` (generated)

Environmental-context slots/enums derived from site fields (location, ecosystem path,
env package). Imported by the study profiles that reference the site. Minimal in v1.

## Generator

`schemas/generate_profiles.py` (+ `just gen-profiles`):
- Reads `db/sfas-brcs.yaml` (and `src/.../nmdc_sfas_brcs.yaml` for enum context).
- Deterministic (no Date.now/random); stable slug + ID rules; sorted output.
- Curated side-maps kept in the script (grown over time):
  - `UCUM` — unit label → ucum_code for the ~16 units in use.
  - `MEANINGS` — `(slug, level)` → ontology CURIE for high-confidence groundings
    (e.g. host crops → NCBITaxon, compartments → ENVO). Ungrounded levels emit text only.
  - `DYNAMIC_BINDINGS` — governed field/source-field → base enum name.
- Emits `schemas/studies/*.yaml`, `schemas/sites/*.yaml`; leaves `base.yaml` hand-authored.
- Source of truth stays `variables` (decision **i-a**); profiles are a regenerable artifact.

## Validation / tooling

- `just gen-profiles` regenerates all profiles.
- `just validate-profiles` runs `linkml-validate`/lint (or `gen-pydantic` smoke test) over
  `base.yaml` and every generated profile, confirming imports resolve and schemas are well-formed.
- Existing `just validate-db` and the browser are unaffected.

## Phasing

1. `base.yaml` + generator + proof on 1–2 studies; confirm `gen-pydantic`/validate on a profile.
2. Generate all 81 study + 40 site profiles; validate the whole set.
3. (Ongoing) grow `MEANINGS`/`DYNAMIC_BINDINGS` to deepen ontology grounding.

## Future (deferred)

Decision **i-b** promotion: make profiles authoritative and regenerate/retire inline
`variables`, switching the browser to read profiles. Revisit once v1 is proven. Optional w3id
registration of the profile base URI.
