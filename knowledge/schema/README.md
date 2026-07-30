# Knowledge Schema Foundation

**Module:** `knowledge/schema`  
**Version:** V1.0.0  
**Status:** Official Data Contract  
**JSON Schema:** Draft 2020-12  

---

## Single source of truth

Authoritative schemas live only in `knowledge/schema/`.

If a Canon domain still contains a local `*.schema.json`, it MUST be a pointer:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://bte-platform.org/schema/knowledge/canon/five_element.schema.json",
  "$ref": "../../schema/five_element.schema.json"
}
```

Do not duplicate Base or module contracts inside `knowledge/knowledge_canon/`.

---

## Purpose

This directory is the **single Data Contract** for Knowledge Canon records used by:

- Knowledge Canon
- Registry
- Rule Loader
- Knowledge Loader
- Validator
- Interpretation Engine
- Report Engine

It defines structure only. It does **not** contain Knowledge Records, academic content, or Rules.

---

## Architecture

```
knowledge_record.schema.json          ← Base Schema
        │
        │  allOf + $ref
        ▼
┌───────────────────────────────────┐
│ Module schemas (extensions only)  │
│ five_element / heavenly_stem / …  │
└───────────────────────────────────┘
```

### Layers

| Layer | File | Responsibility |
|-------|------|----------------|
| Base | `knowledge_record.schema.json` | Shared sections for every Knowledge Record |
| Module | `*.schema.json` | Domain-specific extension fields only |

Module schemas **must not** copy the Base Schema. They inherit it.

---

## Base Schema Sections

Every Knowledge Record includes:

1. `identity`
2. `classification`
3. `definition`
4. `characteristics`
5. `relationships`
6. `references`
7. `metadata`
8. `validation`
9. `revision_history`

Shared reusable types live under Base `$defs` (for example `knowledge_id`, `reference`, `relationship_link`).

---

## Inheritance Model

Module schemas use Draft 2020-12 composition:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://bte-platform.org/schema/knowledge/five_element.schema.json",
  "allOf": [
    { "$ref": "knowledge_record.schema.json" },
    {
      "type": "object",
      "required": ["correspondences"],
      "properties": {
        "correspondences": { "$ref": "#/$defs/correspondences" },
        "classification": {
          "type": "object",
          "properties": {
            "domain": { "const": "five_elements" },
            "category": { "const": "element" }
          }
        }
      }
    }
  ],
  "unevaluatedProperties": false,
  "$defs": {
    "correspondences": { "type": "object", "properties": { "...": {} } }
  }
}
```

### Rules

- Use `$ref` to the Base Schema (never duplicate base properties).
- Use `allOf` to combine Base + module extension.
- Put module-only types in local `$defs`.
- Use `unevaluatedProperties: false` on module schemas to keep contracts closed.
- Constrain `classification.domain` / `classification.category` with `const` per module.

---

## How to use `$ref`

### Relative file reference

```json
{ "$ref": "knowledge_record.schema.json" }
```

### Pointer into Base `$defs`

```json
{
  "$ref": "knowledge_record.schema.json#/$defs/relationship_link"
}
```

### Local `$defs`

```json
{ "$ref": "#/$defs/correspondences" }
```

Resolvers (Python `jsonschema` / AJV) must load schemas from this directory so relative `$ref` paths resolve.

---

## Extending a new module

1. Create `knowledge/schema/<module>.schema.json`.
2. Set `$id` under `https://bte-platform.org/schema/knowledge/`.
3. `allOf`:
   - `$ref` → `knowledge_record.schema.json`
   - extension object with **only** new fields
4. Add module `$defs` for extension types.
5. Set `classification.domain` / `category` constants.
6. Set `unevaluatedProperties: false`.
7. Run `python knowledge/schema/validate_schemas.py`.
8. Do **not** edit Base fields unless a MAJOR version bump is approved.

---

## Module catalog

| Schema | Domain const | Extension object |
|--------|--------------|------------------|
| `five_element.schema.json` | `five_elements` | `correspondences` |
| `heavenly_stem.schema.json` | `heavenly_stems` | `stem_attributes` |
| `earthly_branch.schema.json` | `earthly_branches` | `branch_attributes` |
| `hidden_stem.schema.json` | `hidden_stems` | `hidden_stem_attributes` |
| `yin_yang.schema.json` | `yin_yang` | `polarity_attributes` |
| `ten_god.schema.json` | `ten_gods` | `ten_god_attributes` |
| `strength.schema.json` | `strength` | `strength_attributes` |
| `pattern.schema.json` | `patterns` | `pattern_attributes` |
| `useful_god.schema.json` | `useful_gods` | `useful_god_attributes` |
| `combination.schema.json` | `combinations` | `combination_attributes` |
| `clash.schema.json` | `clashes` | `clash_attributes` |
| `punishment.schema.json` | `punishments` | `punishment_attributes` |
| `harm.schema.json` | `harms` | `harm_attributes` |
| `transformation.schema.json` | `transformations` | `transformation_attributes` |
| `seasonal_qi.schema.json` | `seasonal_qi` | `seasonal_qi_attributes` |
| `temperature.schema.json` | `temperature` | `temperature_attributes` |
| `shensha.schema.json` | `shensha` | `shensha_attributes` |
| `luck_cycle.schema.json` | `luck_cycles` | `luck_cycle_attributes` |
| `special_case.schema.json` | `special_cases` | `special_case_attributes` |

---

## Versioning

| Field | Meaning |
|-------|---------|
| Foundation version | This folder release (`V1.0.0`) |
| `metadata.schema_version` | Contract generation locked to `1.0.0` in Base |
| `metadata.version` | Per-record semantic version |

### Compatibility policy

| Change | Version impact |
|--------|----------------|
| Add optional module field | MINOR |
| Add optional Base field | MINOR |
| Tighten validation / remove field / rename | MAJOR |
| Change `$id` host path | MAJOR |

Backward compatibility: consumers MUST ignore unknown optional fields only when reading older contracts; writers MUST validate against the target schema version.

---

## Validation

```bash
# Python jsonschema (Draft 2020-12)
python knowledge/schema/validate_schemas.py

# AJV (Node)
node knowledge/schema/validate_ajv.mjs
```

Acceptance criteria:

- Valid Draft 2020-12 documents
- No circular `$ref`
- Resolvable relative `$ref`
- Pass Python `jsonschema`
- Pass AJV

---

## Non-goals

- No Knowledge Records in this folder
- No academic prose payloads
- No Rule definitions
- No edits to `knowledge/knowledge_canon/`
- No Registry Specification changes

---

## Related

- Architecture specs (read-only): `knowledge/knowledge_canon/` domain docs
- Registry metadata schemas: `knowledge/registry/schemas/` (separate contract plane)
