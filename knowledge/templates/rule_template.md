# Rule Template

**Template ID:** TPL-KR-RULE-001  
**Version:** 1.0.0  
**Status:** Specification  
**Knowledge type:** Rule  
**Node type (graph):** `Rule`  
**Extends:** `knowledge_record_template.md`

---

## Authoring instructions

Use for formal rules that engines or interpreters may later consume.  
Business logic belongs in Rule Database / this record — **do not** invent rule text without sources. Mark gaps `TODO_REVIEW`.

---

# 1. Identity

| Field | Value |
|------|-------|
| Record ID | `{{RECORD_ID}}` |
| Canonical Name | `{{CANONICAL_NAME}}` |
| Vietnamese Name | `{{VIETNAMESE_NAME}}` |
| Chinese | `{{CHINESE_NAME}}` |
| Pinyin | `{{PINYIN}}` |
| Pack | `{{PACK_ID}}` |
| Module | `{{MODULE_ID}}` |
| Knowledge Type | Rule |
| Rule code (optional) | `{{RULE_CODE}}` |
| Priority | `{{RULE_PRIORITY}}` |
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
| Primary Category | Rule |
| Secondary Category | `{{SECONDARY_CATEGORY}}` |
| Rule family | `{{RULE_FAMILY}}` |
| Academic Layer | `{{ACADEMIC_LAYER}}` |
| Computational Layer | `{{COMPUTATIONAL_LAYER}}` |

---

# 3. Canonical Definition

> {{CANONICAL_DEFINITION}}

**Scope:** {{SCOPE}}

**Out of scope:** {{OUT_OF_SCOPE}}

---

# 4. Rule specification

### Premises / inputs

- {{RULE_PREMISE_1}}
- {{RULE_PREMISE_2}}

### Conditions

```text
{{RULE_CONDITIONS}}
```

### Conclusion / effect

```text
{{RULE_CONCLUSION}}
```

### Exceptions

- {{RULE_EXCEPTION_1}}

### Priority / conflict policy

{{RULE_CONFLICT_POLICY}}

> If multiple rules apply, resolve by `priority` — not by file order.

---

# 5. Academic Context

| Source ID | Role | Notes |
|-----------|------|-------|
| `{{SRC_PRIMARY_1}}` | primary | {{SRC_PRIMARY_1_NOTES}} |

| Assertion ID | Statement | Sources | Confidence | Status |
|--------------|-----------|---------|------------|--------|
| `{{ASR_ID}}` | {{ASR_STATEMENT}} | `{{ASR_SOURCE_IDS}}` | {{ASR_CONFIDENCE}} | {{ASR_STATUS}} |

`TODO_REVIEW`: {{TODO_REVIEW_NOTES}}

---

# 6. Characteristics

| Key | Value |
|-----|-------|
| determinism | `{{RULE_DETERMINISM}}` |
| side_effects | `{{RULE_SIDE_EFFECTS}}` |
| {{CHAR_KEY_EXTRA}} | {{CHAR_VALUE_EXTRA}} |

---

# 7. Relationships

Typical edges: `IMPLEMENTS`, `DEPENDS_ON`, `CONFLICTS_WITH`, `SUPPORTED_BY`, `REFERENCES`.

| Rel ID | Type | Target | Strength | Status |
|--------|------|--------|----------|--------|
| `{{REL_ID}}` | `{{REL_TYPE}}` | `{{REL_TARGET}}` | {{REL_STRENGTH}} | {{REL_STATUS}} |

---

# 8. Examples

| Example ID | Title | Kind |
|------------|-------|------|
| `{{EX_ID}}` | {{EX_TITLE}} | computational / boundary |

{{EX_DESCRIPTION}}

---

# 9. Computational / Validation / Governance / Release

| Field | Value |
|------|-------|
| Knowledge nature | procedural / hybrid |
| Engine compatibility | `{{ENGINE_COMPATIBILITY}}` |
| Explainability contract | `{{EXPLAINABILITY_CONTRACT}}` |
| Checklist status | `{{CHECKLIST_STATUS}}` |
| Owner | `{{OWNER}}` |
| Reviews (A/T/G) | `{{ACADEMIC_REVIEW_STATUS}}` / `{{TECHNICAL_REVIEW_STATUS}}` / `{{GOVERNANCE_REVIEW_STATUS}}` |
| Approval / Freeze | `{{APPROVAL_STATUS}}` / `{{FREEZE_STATUS}}` |
| Release status | `{{RELEASE_STATUS}}` |

---

## Compiler mapping

Rule body MUST remain structured for future rule-database projection.  
Do not hard-code engine `if/else` replacements in application code when the rule belongs here.
