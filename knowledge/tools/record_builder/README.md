# Knowledge Record Builder

**Path:** `knowledge/tools/record_builder/`  
**Version:** V1.0.0  
**Status:** Prepared — Pipeline only  
**Phase:** Compiler Preparation (no record generation)

---

## Purpose

Prepare the implementation pipeline that converts **approved design documents** into Knowledge Record JSON.

This toolkit does **not** generate Knowledge Records in this sprint.

---

## Structure

```
knowledge/tools/record_builder/
├── README.md
├── builder_spec.md
├── mapping_rules.md
├── validation_rules.md
├── RECORD_MAPPING_TEMPLATE.md
├── JSON_COMPILATION_CHECKLIST.md
├── COMPILATION_REPORT_TEMPLATE.md
└── KNOWLEDGE_RECORD_TEMPLATE.json
```

---

## Inputs (future)

- Approved design artifacts under `knowledge/bazi/**/design/PACK_*/records/`
- Ownership Matrix / Planning IDs
- Globally allocated `KNO-*` (when issued)
- Foundation `REF-*` / `TERM-*`
- Official schemas under `knowledge/schema/` (read-only)

---

## Outputs (future)

- Knowledge Record JSON conforming to `knowledge_record.schema.json` (+ module overlay when authorized)
- Compilation report (from template)

---

## Non-goals (this sprint)

- Authoring academic content
- Allocating Knowledge IDs
- Writing builder runtime code
- Populating Official `knowledge_records/`
- Modifying Foundation / Canon / schemas

---

## Related documents

| File | Role |
|------|------|
| `builder_spec.md` | Pipeline specification |
| `mapping_rules.md` | Design → JSON mapping rules |
| `RECORD_MAPPING_TEMPLATE.md` | Section-by-section mapping template |
| `validation_rules.md` | Validation gates |
| `JSON_COMPILATION_CHECKLIST.md` | Operator checklist |
| `COMPILATION_REPORT_TEMPLATE.md` | Report form |
| `KNOWLEDGE_RECORD_TEMPLATE.json` | Empty JSON shell (official base schema shape) |

---

## Stop

Await Design approval + compilation authorization before generating any Knowledge Record.
