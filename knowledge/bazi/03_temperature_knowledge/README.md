# Temperature Knowledge

**Module:** `knowledge/bazi/03_temperature_knowledge`  
**Version:** V1.0.0  
**Status:** Draft (Blueprint)  
**Phase:** Structure only — no academic Knowledge Records

---

## Purpose

Climate and temperature regulation knowledge structures for future records.

This module is an implementation-ready blueprint for future BaZi knowledge development.

---

## Scope

In scope:

- Module documentation and authoring guides
- Empty `knowledge_records/` reservation
- Example and template JSON placeholders
- Validation checklist documentation

Out of scope:

- Academic Knowledge Records
- Rule / scoring / interpretation logic
- Modifications to Knowledge Foundation or Knowledge Canon

---

## Dependencies

- `01_fundamental_knowledge`
- `knowledge/references`
- `knowledge/terminology`

Foundation (frozen; read-only for this module):

- `knowledge/references`
- `knowledge/terminology`
- `knowledge/citation_rules`
- `knowledge/governance`
- `knowledge/schema` (for future schema validation)

---

## Consumers

- `05_useful_god_knowledge`
- `04_pattern_knowledge`
- `13_health_knowledge`

Future consumers (not implemented in this sprint):

- Interpretation / Report layers
- Rule Database mapping (separate authorization)

---

## Directory structure

```
03_temperature_knowledge/
├── README.md
├── MODULE_SPEC.md
├── FIELD_GUIDE.md
├── validation.md
├── CHANGELOG.md
├── knowledge_records/      # reserved; empty in blueprint
├── examples/
│   ├── example_record.json
│   └── template_record.json
└── docs/
    └── README.md
```

---

## Development workflow

1. Read `MODULE_SPEC.md` and `FIELD_GUIDE.md`
2. Allocate Knowledge IDs per governance / registry process
3. Author records into `knowledge_records/` (future sprint)
4. Cite only Foundation Reference IDs (`REF-*`)
5. Use Foundation terminology (`TERM-*`)
6. Run schema + Foundation integrity validation
7. Submit Technical Review then Academic Review then Official

Do not invent references, terminology, or academic content in the blueprint phase.
