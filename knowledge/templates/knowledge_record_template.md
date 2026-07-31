# Knowledge Record Template

**Template ID:** TPL-KR-001  
**Version:** 1.0.0  
**Status:** Specification  
**Applies to:** All Knowledge Records  
**Based on:** Sprint 3A KR schema sections · Sprint 3E governance lifecycle

---

## Authoring instructions

1. Copy this file to the target module `records/` folder (or design workspace).
2. Rename to `{{RECORD_ID}}_{{CANONICAL_KEY}}.md`.
3. Replace every `{{PLACEHOLDER}}`.
4. Run self-check against `knowledge/quality/review_checklist.json`.
5. Submit via review workflow (`draft` → `review`).

Do **not** invent bibliography sources. Use existing `SRC-*` or mark `TODO_REVIEW`.

---

# Part 1 — Identity

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
| Knowledge Type | `{{KNOWLEDGE_TYPE}}` |
| Domain | `{{DOMAIN}}` |
| Discipline | `{{DISCIPLINE}}` |
| Status | `{{STATUS}}` <!-- draft \| review \| approved \| official \| deprecated --> |
| Version | `{{VERSION}}` |
| Language | `{{LANGUAGE}}` |
| Primary Author | `{{PRIMARY_AUTHOR}}` |
| Review Status | `{{REVIEW_STATUS}}` |
| Compiler Status | `{{COMPILER_STATUS}}` <!-- not_compiled \| compiled_draft \| ... --> |

### Canonical Identifier

```text
{{RECORD_ID}}
```

Record ID SHALL remain immutable for the lifetime of the record.

---

# Part 2 — Classification

| Field | Value |
|------|-------|
| Primary Category | `{{PRIMARY_CATEGORY}}` |
| Secondary Category | `{{SECONDARY_CATEGORY}}` |
| Academic Layer | `{{ACADEMIC_LAYER}}` |
| Computational Layer | `{{COMPUTATIONAL_LAYER}}` |

### Hierarchy path

```text
{{HIERARCHY_PATH}}
```

---

# Part 3 — Canonical Definition

### Definition

> {{CANONICAL_DEFINITION}}

### Scope

{{SCOPE}}

### Out of scope

{{OUT_OF_SCOPE}}

### Constraints

- {{CONSTRAINT_1}}
- {{CONSTRAINT_2}}

---

# Part 4 — Academic Context

### Primary sources (`SRC-*`)

| Source ID | Notes |
|-----------|-------|
| `{{SRC_PRIMARY_1}}` | {{SRC_PRIMARY_1_NOTES}} |

### Secondary sources

| Source ID | Notes |
|-----------|-------|
| `{{SRC_SECONDARY_1}}` | {{SRC_SECONDARY_1_NOTES}} |

### Assertions

| Assertion ID | Statement | Source IDs | Confidence | Status |
|--------------|-----------|------------|------------|--------|
| `{{ASR_ID}}` | {{ASR_STATEMENT}} | `{{ASR_SOURCE_IDS}}` | {{ASR_CONFIDENCE}} | {{ASR_STATUS}} |

Uncertain claims: `TODO_REVIEW` — {{TODO_REVIEW_NOTES}}

---

# Part 5 — Characteristics

| Key | Value | Notes |
|-----|-------|-------|
| `{{CHAR_KEY_1}}` | {{CHAR_VALUE_1}} | {{CHAR_NOTES_1}} |

---

# Part 6 — Relationships

Use approved graph edge types only (`FOUNDATIONAL_FOR`, `DEPENDS_ON`, `CLASSIFIES`, `REFERENCES`, `SUPPORTED_BY`, `RELATED_TO`, `CONFLICTS_WITH`, `IMPLEMENTS`).

| Rel ID | Type | Source | Target | Strength | Direction | Status |
|--------|------|--------|--------|----------|-----------|--------|
| `{{REL_ID}}` | `{{REL_TYPE}}` | `{{REL_SOURCE}}` | `{{REL_TARGET}}` | {{REL_STRENGTH}} | {{REL_DIRECTION}} | {{REL_STATUS}} |

No cyclic `FOUNDATIONAL_FOR` / `DEPENDS_ON`. No duplicate triples.

---

# Part 7 — Examples

| Example ID | Title | Kind | Status |
|------------|-------|------|--------|
| `{{EX_ID}}` | {{EX_TITLE}} | {{EX_KIND}} | {{EX_STATUS}} |

{{EX_DESCRIPTION}}

---

# Part 8 — Computational Metadata

| Field | Value |
|------|-------|
| Schema version | `1.0.0` |
| Knowledge nature | `{{KNOWLEDGE_NATURE}}` |
| Engine compatibility | `{{ENGINE_COMPATIBILITY}}` |
| Explainability contract | `{{EXPLAINABILITY_CONTRACT}}` |
| Tags | `{{TAGS}}` |

---

# Part 9 — Validation

| Field | Value |
|------|-------|
| Checklist status | `{{CHECKLIST_STATUS}}` |
| Quality notes | {{VALIDATION_NOTES}} |
| Blocking issues | {{VALIDATION_ERRORS}} |

Map to metrics: Completeness, Consistency, Traceability, Compiler Compatibility, Relationship Integrity, Bibliography Integrity, Graph Integrity, Governance Compliance.

---

# Part 10 — Governance

| Field | Value |
|------|-------|
| Owner | `{{OWNER}}` |
| Stewards | `{{STEWARDS}}` |
| Academic review | `{{ACADEMIC_REVIEW_STATUS}}` |
| Technical review | `{{TECHNICAL_REVIEW_STATUS}}` |
| Governance review | `{{GOVERNANCE_REVIEW_STATUS}}` |
| Approval | `{{APPROVAL_STATUS}}` |
| Freeze | `{{FREEZE_STATUS}}` |

Lifecycle: `draft` → `review` → `approved` → `official` → (`deprecated` → `archived` → `retired`).

---

# Part 11 — Release

| Field | Value |
|------|-------|
| Release status | `{{RELEASE_STATUS}}` |
| Canon version | `{{CANON_VERSION}}` |
| Changelog | {{CHANGELOG}} |

`released` REQUIRES `freeze=frozen` and `approval=approved`.

---

# Compiler mapping hints (non-executable)

| Markdown section | KR schema section |
|------------------|-------------------|
| Part 1 | `identity` |
| Part 2 | `classification` |
| Part 3 | `canonical_definition` |
| Part 4 | `academic_context` |
| Part 5 | `characteristics` |
| Part 6 | `relationships` |
| Part 7 | `examples` |
| Part 8 | `computational_metadata` |
| Part 9 | `validation` |
| Part 10 | `governance` |
| Part 11 | `release` |
