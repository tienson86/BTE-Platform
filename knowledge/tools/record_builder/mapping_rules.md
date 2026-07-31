# Mapping Rules

**Document:** mapping_rules  
**Module:** `knowledge/tools/record_builder`  
**Version:** V1.0.0  

---

## 1. Principle

Approved design sections map to JSON paths defined by the official base schema.

Do not invent alternate top-level keys.

---

## 2. Official top-level keys

Required by `knowledge_record.schema.json`:

- `identity`
- `classification`
- `definition`
- `characteristics`
- `relationships`
- `references`
- `metadata`
- `validation`
- `revision_history`

---

## 3. Core mappings

| Design section | JSON path | Notes |
|----------------|-----------|-------|
| Identity | `identity.*` | Includes `knowledge_id`, names, `pinyin`, etc. |
| Classification | `classification.*` | `domain`, `category`, optional `subcategory`, `tags` |
| Definition | `definition` | **String** (not an object). Entire approved definition text. |
| Characteristics | `characteristics.*` | `nature`, `symbolism`, `summary`, `notes` only (base schema) |
| Relationships | `relationships` | **Object** of typed arrays/links — not a bare top-level array |
| References | `references[]` | Each item: `reference_id`, `title`, optional `chapter`, `notes`, `uri` |
| Metadata | `metadata.*` | `version`, `status`, dates, owner, reviewer, `schema_version` |
| Validation | `validation.*` | Boolean gate flags + optional validator metadata |
| Revision History | `revision_history[]` | `version`, `date`, `summary`, optional `author` |

---

## 4. Definition mapping clarification

Design docs may label a block “Definition”.

Compiler mapping:

```text
Definition (design)
        ↓
definition                 # JSON string
```

If a design uses `definition.summary`, flatten into the single `definition` string unless a future schema ADR changes the base type.

---

## 5. Relationships mapping clarification

```text
Relationships (design)
        ↓
relationships.depends_on[]
relationships.related_to[]
relationships.see_also[]
relationships.<approved_typed_slot>   # when schema allows additionalProperties
```

Each link requires:

- `knowledge_id` (`KNO-NNNNNN`)
- `relationship_type`
- optional `notes`

---

## 6. Forbidden mappings

- Planning ID (`FND-INV-*`) → `identity.knowledge_id`  
- Free-text title-only citation → `references[]` without `reference_id`  
- Academic invention to fill empty design fields  
- Module-private keys not present in schema (unless overlay authorized)

---

## 7. Empty / deferred values

| Situation | Rule |
|-----------|------|
| Scholarly uncertainty | `TODO_REVIEW` where string fields allow |
| Not yet allocated ID | Do not compile Official JSON |
| Optional characteristic slot unused | Omit key or use empty string per overlay rules |

---

## 8. See also

`RECORD_MAPPING_TEMPLATE.md`
