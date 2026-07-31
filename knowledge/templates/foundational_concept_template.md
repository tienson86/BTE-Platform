# Foundational Concept Template

**Template ID:** TPL-KR-CONCEPT-001  
**Version:** 1.0.0  
**Status:** Specification  
**Knowledge type:** Foundational Concept  
**Node type (graph):** `Concept`  
**Extends:** `knowledge_record_template.md`

---

## Authoring instructions

Use for base academic concepts (e.g. Yin Yang, Qi, Wu Xing system framing).  
Replace all `{{PLACEHOLDER}}` values. Prefer this over the generic shell when `knowledge_type = Foundational Concept`.

---

# 1. Identity

| Field | Value |
|------|-------|
| Record ID | `{{RECORD_ID}}` |
| Canonical Name | `{{CANONICAL_NAME}}` |
| Vietnamese Name | `{{VIETNAMESE_NAME}}` |
| Chinese | `{{CHINESE_NAME}}` |
| Pinyin | `{{PINYIN}}` |
| Aliases | `{{ALIASES}}` |
| Pack | `{{PACK_ID}}` |
| Module | `{{MODULE_ID}}` |
| Knowledge Type | Foundational Concept |
| Status | `{{STATUS}}` |
| Version | `{{VERSION}}` |
| Compiler Status | `{{COMPILER_STATUS}}` |

```text
{{RECORD_ID}}
```

---

# 2. Classification

| Field | Value |
|------|-------|
| Primary Category | Fundamental Concept |
| Secondary Category | `{{SECONDARY_CATEGORY}}` |
| Academic Layer | `{{ACADEMIC_LAYER}}` |
| Computational Layer | Base Knowledge Node |
| Domain | `{{DOMAIN}}` |
| Discipline | `{{DISCIPLINE}}` |

Hierarchy:

```text
{{HIERARCHY_PATH}}
```

---

# 3. Canonical Definition

> {{CANONICAL_DEFINITION}}

**Scope:** {{SCOPE}}

**Out of scope:** {{OUT_OF_SCOPE}}

**Why foundational:** {{FOUNDATIONAL_RATIONALE}}

**Downstream dependents (planned):** `{{DOWNSTREAM_RECORD_IDS}}`

---

# 4. Academic Context

| Source ID | Role | Notes |
|-----------|------|-------|
| `{{SRC_PRIMARY_1}}` | primary | {{SRC_PRIMARY_1_NOTES}} |

| Assertion ID | Statement | Sources | Confidence | Status |
|--------------|-----------|---------|------------|--------|
| `{{ASR_ID}}` | {{ASR_STATEMENT}} | `{{ASR_SOURCE_IDS}}` | {{ASR_CONFIDENCE}} | {{ASR_STATUS}} |

`TODO_REVIEW`: {{TODO_REVIEW_NOTES}}

---

# 5. Characteristics

| Key | Value |
|-----|-------|
| polarity_or_structure | `{{CHAR_STRUCTURE}}` |
| dynamism | `{{CHAR_DYNAMISM}}` |
| computational_role | `{{CHAR_COMPUTATIONAL_ROLE}}` |
| {{CHAR_KEY_EXTRA}} | {{CHAR_VALUE_EXTRA}} |

---

# 6. Relationships

Typical edges for foundational concepts: `FOUNDATIONAL_FOR`, `CLASSIFIES`, `RELATED_TO`, `SUPPORTED_BY`.

| Rel ID | Type | Target | Strength | Status |
|--------|------|--------|----------|--------|
| `{{REL_ID}}` | `{{REL_TYPE}}` | `{{REL_TARGET}}` | {{REL_STRENGTH}} | {{REL_STATUS}} |

---

# 7. Examples

| Example ID | Title | Kind |
|------------|-------|------|
| `{{EX_ID}}` | {{EX_TITLE}} | illustrative |

{{EX_DESCRIPTION}}

---

# 8. Computational / Validation / Governance / Release

| Field | Value |
|------|-------|
| Knowledge nature | foundational |
| Explainability contract | `{{EXPLAINABILITY_CONTRACT}}` |
| Checklist status | `{{CHECKLIST_STATUS}}` |
| Owner | `{{OWNER}}` |
| Academic / Technical / Governance review | `{{ACADEMIC_REVIEW_STATUS}}` / `{{TECHNICAL_REVIEW_STATUS}}` / `{{GOVERNANCE_REVIEW_STATUS}}` |
| Approval / Freeze | `{{APPROVAL_STATUS}}` / `{{FREEZE_STATUS}}` |
| Release status | `{{RELEASE_STATUS}}` |

---

## Compiler mapping

Maps to KR schema sections `identity` … `release` (see `knowledge_record_template.md`).  
Graph node_type MUST be `Concept`. Index `canonical_key`: `{{CANONICAL_KEY}}`.
