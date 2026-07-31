# Builder Specification

**Document:** builder_spec  
**Module:** `knowledge/tools/record_builder`  
**Version:** V1.0.0  
**Status:** Prepared  

---

## 1. Mission

Define the future compiler that transforms approved design documents into schema-conformant Knowledge Records.

No records are compiled in this preparation sprint.

---

## 2. Pipeline stages

```text
Approved Design Artifact
        ↓
Input Verification
        ↓
Field Mapping (design → JSON paths)
        ↓
Draft JSON Assembly
        ↓
Schema Validation
        ↓
Reference Validation
        ↓
Relationship Validation
        ↓
Integrity Validation
        ↓
Output Validation
        ↓
Compilation Report
        ↓
(Authorized) Write to knowledge_records/
```

---

## 3. Preconditions

Compilation MAY proceed only when:

1. Design pack Academic Review is approved for the target Planning ID  
2. Ownership Matrix status is Resolved (not `TODO_REVIEW`)  
3. Knowledge ID is issued by Global Allocator (`KNO-NNNNNN`)  
4. Canon link-only concepts are **not** compiled into BaZi duplicate Official JSON  
5. Schemas remain unchanged (read-only consume)

---

## 4. Schema authority

| Layer | Authority |
|-------|-----------|
| Base record shape | `knowledge/schema/knowledge_record.schema.json` |
| Module overlays | Module schemas via `allOf` + `$ref` when authorized |
| References | Foundation `references.json` |
| Terminology | Foundation `glossary.json` |

---

## 5. Builder responsibilities

| Does | Does not |
|------|----------|
| Map approved fields to JSON paths | Invent academic text |
| Enforce empty/`TODO_REVIEW` policy for uncertain scholarly fields | Allocate `KNO-*` / `REF-*` |
| Run validation gates | Modify Canon / Foundation / schemas |
| Emit compilation reports | Skip Academic Review |

---

## 6. Artifact types

| Artifact | Description |
|----------|-------------|
| Design note | Human-approved design sections |
| Draft JSON | Intermediate compile output |
| Official JSON | Written only after all gates pass + authorization |
| Compilation report | Filled from `COMPILATION_REPORT_TEMPLATE.md` |

---

## 7. Failure policy

Any ERROR-severity validation failure blocks Official write.

WARNINGS (e.g. `TODO_REVIEW` bibliographic fields) may pass Draft but block Official unless policy allows.

---

## 8. Future implementation note

Runtime builder code (CLI/service) is **out of scope** for this sprint. Specs and templates only.
