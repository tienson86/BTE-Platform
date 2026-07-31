# Example Template

**Template ID:** TPL-KR-EXAMPLE-001  
**Version:** 1.0.0  
**Status:** Specification  
**Knowledge type:** Example  
**Node type (graph):** `Example`  
**ID pattern:** `EX-NNNNNN`  
**Extends:** sections of `knowledge_record_template.md` (lightweight)

---

## Authoring instructions

Use for illustrative, boundary, counter, or computational examples attached to a parent KR.  
Examples are **not** academic authorities by themselves — bind them with `SUPPORTED_BY` / `REFERENCES` as needed.

---

# 1. Identity

| Field | Value |
|------|-------|
| Example ID | `{{EX_ID}}` |
| Title | `{{EX_TITLE}}` |
| Parent Record ID | `{{PARENT_RECORD_ID}}` |
| Kind | `{{EX_KIND}}` <!-- illustrative \| boundary \| counterexample \| computational --> |
| Status | `{{EX_STATUS}}` |
| Pack / Module | `{{PACK_ID}}` / `{{MODULE_ID}}` |
| Author | `{{PRIMARY_AUTHOR}}` |

---

# 2. Description

{{EX_DESCRIPTION}}

---

# 3. Setup / inputs

```text
{{EX_SETUP}}
```

---

# 4. Expected observation (non-test)

{{EX_EXPECTED_OBSERVATION}}

> This section is pedagogical. It is **not** a golden test expected output and MUST NOT be used to rewrite snapshots.

---

# 5. Linked assertions / sources

| Assertion ID | Source IDs | Notes |
|--------------|------------|-------|
| `{{ASR_ID}}` | `{{ASR_SOURCE_IDS}}` | {{ASR_NOTES}} |

`TODO_REVIEW`: {{TODO_REVIEW_NOTES}}

---

# 6. Relationships

| Rel ID | Type | Source | Target | Status |
|--------|------|--------|--------|--------|
| `{{REL_ID}}` | `REFERENCES` / `RELATED_TO` | `{{EX_ID}}` | `{{PARENT_RECORD_ID}}` | `{{REL_STATUS}}` |

---

# 7. Validation & Governance

| Field | Value |
|------|-------|
| Checklist status | `{{CHECKLIST_STATUS}}` |
| Academic review | `{{ACADEMIC_REVIEW_STATUS}}` |
| Technical review | `{{TECHNICAL_REVIEW_STATUS}}` |
| Approval | `{{APPROVAL_STATUS}}` |
| Freeze | `{{FREEZE_STATUS}}` |

---

## Compiler mapping

Maps to KR `examples.items[]` (`example.schema.json`).  
Index optionally via keyword/topic indexes; do not create a second canonical Concept for an example.
