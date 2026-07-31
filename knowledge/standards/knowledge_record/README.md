# Knowledge Record Infrastructure

**Sprint:** 3A  
**Location:** `knowledge/standards/knowledge_record/`  
**Schema draft:** JSON Schema Draft 2020-12  
**Status:** Infrastructure (not academic content)

---

## Purpose

This folder defines the **master Knowledge Record (KR) schema suite** that every KR instance MUST satisfy when authored or compiled under the BTE Knowledge Canon standards track.

It is infrastructure only. It does not author academic Knowledge Records and does not modify:

- `knowledge/bazi/**`
- `knowledge/bibliography/**`
- `knowledge/compiler/**`
- `PACK_01_DESIGN.md`
- Any Knowledge Record file

---

## Folder tree

```text
knowledge/standards/knowledge_record/
├── README.md
├── knowledge_record.schema.json          # master KR schema
├── knowledge_record_validation.json      # validation rules + pass criteria
├── relationship.schema.json
├── metadata.schema.json
├── assertion.schema.json
├── example.schema.json
├── review.schema.json
└── examples/
    └── kr_infrastructure_example.json    # synthetic fixture (not canon)
```

---

## Master schema sections

`knowledge_record.schema.json` requires these top-level sections:

| Section | Role |
|---------|------|
| `identity` | `KR-*` ID, names, status, version |
| `classification` | discipline, pack/module, categories, layers |
| `canonical_definition` | definition string, scope, constraints |
| `academic_context` | `SRC-*` sources + assertions |
| `characteristics` | keyed characteristic items |
| `relationships` | array of `REL-*` links |
| `examples` | array of `EX-*` examples |
| `computational_metadata` | versioning, compiler status, engine tags |
| `validation` | checklist result + schema id |
| `governance` | owner + nested review object |
| `release` | release status + canon version |

Satellite schemas are `$ref`'d from the master where applicable.

---

## ID patterns

| Kind | Pattern |
|------|---------|
| Knowledge Record | `KR-NNNNNN` |
| Relationship | `REL-NNNNNN` |
| Assertion | `ASR-NNNNNN` |
| Example | `EX-NNNNNN` |
| Bibliography source | `SRC-NNNNNN` |

---

## Relationship to `knowledge/schema/`

Platform SSOT schemas may also exist under `knowledge/schema/`. This standards suite is the **Sprint 3A standards track** for KR structure under `knowledge/standards/`.

- Compiler mapping between the two locations is **out of scope** for Sprint 3A.
- Production academic KRs continue to be authored separately (e.g. markdown records under bazi).
- Do not treat `examples/kr_infrastructure_example.json` as canon content.

---

## Validation

1. All `*.schema.json` files use Draft **2020-12**.
2. Rules and pass criteria: `knowledge_record_validation.json`.
3. Fixture instance: `examples/kr_infrastructure_example.json`.

Validate locally (example):

```bash
python -c "import json,jsonschema; from pathlib import Path; from jsonschema import Draft202012Validator; root=Path('knowledge/standards/knowledge_record'); schemas={p.name:json.loads(p.read_text(encoding='utf-8')) for p in root.glob('*.schema.json')}; store={s['$id']:s for s in schemas.values()}; resolver=jsonschema.RefResolver.from_schema(schemas['knowledge_record.schema.json'], store=store); Draft202012Validator.check_schema(schemas['knowledge_record.schema.json']); inst=json.loads((root/'examples/kr_infrastructure_example.json').read_text(encoding='utf-8')); Draft202012Validator(schemas['knowledge_record.schema.json'], resolver=resolver).validate(inst); print('PASS')"
```

---

## Design notes

- `canonical_definition.definition` is a **string** (not an object).
- `relationships` / `examples` / `characteristics` are **typed objects** with an `items` array (stable extension point).
- `governance.review` embeds academic, technical, governance, approval, and freeze blocks per `review.schema.json`.
- Assertions require at least one `SRC-*` source id; academic truth is not invented in this sprint.
