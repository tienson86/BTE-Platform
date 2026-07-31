# Entity Template

**Template ID:** TPL-KR-ENTITY-001  
**Version:** 1.0.0  
**Status:** Specification  
**Knowledge type:** Entity  
**Node type (graph):** `Entity` or catalogued Concept-as-entity set (e.g. stems/branches)  
**Extends:** `knowledge_record_template.md`

---

## Authoring instructions

Use for named entity systems or catalogs (e.g. Heavenly Stems, Earthly Branches).  
Replace all `{{PLACEHOLDER}}` values. List members explicitly; do not invent member properties without sources.

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
| Knowledge Type | Entity |
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
| Primary Category | Entity |
| Secondary Category | `{{SECONDARY_CATEGORY}}` |
| Academic Layer | `{{ACADEMIC_LAYER}}` |
| Computational Layer | `{{COMPUTATIONAL_LAYER}}` |
| Entity set size | `{{ENTITY_SET_SIZE}}` |
| Ordering rule | `{{ORDERING_RULE}}` |

Hierarchy:

```text
{{HIERARCHY_PATH}}
```

---

# 3. Canonical Definition

> {{CANONICAL_DEFINITION}}

**Scope:** {{SCOPE}}

**Out of scope:** {{OUT_OF_SCOPE}}

**Membership rule:** {{MEMBERSHIP_RULE}}

---

# 4. Entity catalog

| Member ID | Name | Vietnamese | Chinese | Notes |
|-----------|------|------------|---------|-------|
| `{{MEMBER_ID_1}}` | {{MEMBER_NAME_1}} | {{MEMBER_VI_1}} | {{MEMBER_ZH_1}} | {{MEMBER_NOTES_1}} |
| `{{MEMBER_ID_2}}` | {{MEMBER_NAME_2}} | {{MEMBER_VI_2}} | {{MEMBER_ZH_2}} | {{MEMBER_NOTES_2}} |

Add rows as required. Incomplete catalogs MUST set Status `draft` and list gaps under `TODO_REVIEW`.

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
| enumeration_complete | `{{ENUM_COMPLETE}}` |
| yin_yang_mapping | `{{YIN_YANG_MAPPING}}` |
| element_mapping | `{{ELEMENT_MAPPING}}` |
| {{CHAR_KEY_EXTRA}} | {{CHAR_VALUE_EXTRA}} |

---

# 7. Relationships

Typical edges: `DEPENDS_ON`, `CLASSIFIES`, `RELATED_TO`, `REFERENCES`, `SUPPORTED_BY`.

| Rel ID | Type | Target | Strength | Status |
|--------|------|--------|----------|--------|
| `{{REL_ID}}` | `{{REL_TYPE}}` | `{{REL_TARGET}}` | {{REL_STRENGTH}} | {{REL_STATUS}} |

---

# 8. Examples

| Example ID | Title | Kind |
|------------|-------|------|
| `{{EX_ID}}` | {{EX_TITLE}} | illustrative |

{{EX_DESCRIPTION}}

---

# 9. Computational / Validation / Governance / Release

| Field | Value |
|------|-------|
| Knowledge nature | `{{KNOWLEDGE_NATURE}}` |
| Engine compatibility | `{{ENGINE_COMPATIBILITY}}` |
| Checklist status | `{{CHECKLIST_STATUS}}` |
| Owner | `{{OWNER}}` |
| Reviews (A/T/G) | `{{ACADEMIC_REVIEW_STATUS}}` / `{{TECHNICAL_REVIEW_STATUS}}` / `{{GOVERNANCE_REVIEW_STATUS}}` |
| Approval / Freeze | `{{APPROVAL_STATUS}}` / `{{FREEZE_STATUS}}` |
| Release status | `{{RELEASE_STATUS}}` |

---

## Compiler mapping

Entity members SHOULD be compiler-stable lists (no silent reorder after `official`).  
Index `canonical_key`: `{{CANONICAL_KEY}}`.
