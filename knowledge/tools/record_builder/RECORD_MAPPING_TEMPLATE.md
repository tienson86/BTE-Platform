# Record Mapping Template

**Document:** RECORD_MAPPING_TEMPLATE  
**Module:** `knowledge/tools/record_builder`  
**Version:** V1.0.0  

Use one copy per approved Planning ID during compilation.

---

## Header

| Field | Value |
|-------|-------|
| Planning ID | |
| Knowledge ID | |
| Pack | |
| Owner module | |
| Design artifact path | |
| Compiler operator | |
| Date | |

---

## Section → JSON map

### Identity

```text
Identity (design)
        ↓
identity.knowledge_id
identity.canonical_name
identity.chinese
identity.traditional_chinese
identity.simplified_chinese
identity.pinyin
identity.vietnamese
identity.english_name
identity.aliases[]
```

| Design field | JSON path | Source value | Status |
|--------------|-----------|--------------|--------|
| Knowledge ID | `identity.knowledge_id` | | |
| Canonical Name | `identity.canonical_name` | | |
| Chinese | `identity.chinese` | | |
| Pinyin | `identity.pinyin` | | |
| English Name | `identity.english_name` | | |
| … | … | | |

---

### Classification

```text
Classification (design)
        ↓
classification.domain
classification.category
classification.subcategory
classification.tags[]
```

---

### Definition

```text
Definition (design)
        ↓
definition
```

> Official base schema: `definition` is a **string**, not `definition.summary`.

| Design field | JSON path | Source value | Status |
|--------------|-----------|--------------|--------|
| Definition text | `definition` | | |

---

### Characteristics

```text
Characteristics (design)
        ↓
characteristics.nature
characteristics.symbolism
characteristics.summary
characteristics.notes
```

---

### Relationships

```text
Relationships (design)
        ↓
relationships.depends_on[]
relationships.related_to[]
relationships.see_also[]
relationships.<typed_slot>   # if overlay/base allows
```

Each array item:

```text
→ knowledge_id
→ relationship_type
→ notes
```

---

### References

```text
References (design)
        ↓
references[]
    → reference_id
    → title
    → chapter
    → notes
    → uri
```

---

### Metadata

```text
Metadata (design)
        ↓
metadata.version
metadata.status
metadata.owner
metadata.created_date
metadata.updated_date
metadata.reviewer
metadata.schema_version
```

---

### Validation

```text
Validation (design / compiler gates)
        ↓
validation.schema_valid
validation.reference_valid
validation.relationship_valid
validation.integrity_valid
validation.validated_at
validation.validator
```

---

### Revision History

```text
Revision History (design)
        ↓
revision_history[]
    → version
    → date
    → summary
    → author
```

---

## Mapping completion

- [ ] All required JSON paths assigned or explicitly deferred  
- [ ] No Planning ID written into `identity.knowledge_id`  
- [ ] No invented academic text introduced by mapping  
- [ ] Ready for `JSON_COMPILATION_CHECKLIST.md`  
