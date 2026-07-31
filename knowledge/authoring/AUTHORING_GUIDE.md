# Authoring Guide

**Document:** AUTHORING_GUIDE  
**Version:** 1.0.0  
**Status:** Specification  
**Audience:** Knowledge Authors

---

## 1. Goal

Write Knowledge Records that are academically honest, machine-mappable, reviewable, and publishable under BTE governance.

---

## 2. Choose the right template

| If you are writing… | Use |
|---------------------|-----|
| Generic KR shell | `knowledge/templates/knowledge_record_template.md` |
| Foundational Concept | `foundational_concept_template.md` |
| Entity / catalog | `entity_template.md` |
| Rule | `rule_template.md` |
| Example only | `example_template.md` |
| Golden candidate overlay | `golden_record_template.md` |

Copy the template; do not edit the template file in place for content authoring.

---

## 3. Authoring sequence

```text
1. Allocate / confirm RECORD_ID (KR-NNNNNN)
2. Fill Identity + Classification
3. Write Canonical Definition (scope + out of scope)
4. Attach Academic Assertions + SRC-* sources
5. List Characteristics
6. Declare Relationships (approved edge types only)
7. Add Examples (pedagogical)
8. Fill Computational Metadata
9. Self-validate (CHECKLIST.md + quality metrics)
10. Submit for review (draft → review)
```

Do not skip to “official” language before review.

---

## 4. How to write a Knowledge Record

### 4.1 Identity

- One concept → one `KR-*`.
- Canonical Name is unique in the canon for that concept.
- Vietnamese / Chinese / Pinyin are mandatory when the concept is classical Chinese metaphysics content unless explicitly waived with `TODO_REVIEW`.

### 4.2 Canonical Definition rules

1. **One definition block** — a single clear definition string/paragraph, not competing definitions.
2. **Scope** — what the record covers.
3. **Out of scope** — what it deliberately does not answer (e.g. luck calculation, engine scoring).
4. **No engine logic** — definition is academic/structural, not Python `if/else`.
5. **No silent expansion** — new meanings require a change request after freeze.

Good shape:

> {{Concept}} is … within {{domain}}. It is used to … . It does not …

### 4.3 Academic Assertions

| Field | Rule |
|-------|------|
| `assertion_id` | `ASR-NNNNNN` |
| `statement` | Falsifiable / reviewable claim |
| `source_ids` | ≥1 existing `SRC-*` |
| `confidence` | `high` \| `medium` \| `low` \| `pending_review` |
| `status` | lifecycle-aligned (`draft` …) |

Rules:

- Every non-trivial academic claim SHOULD be an assertion or clearly sourced prose.
- `confidence=high` forbids open `TODO_REVIEW` on that claim.
- Unknown → `TODO_REVIEW` / `pending_review`. **Never invent** classical citations.

### 4.4 Examples

- Use `EX-NNNNNN`.
- Kinds: `illustrative`, `boundary`, `counterexample`, `computational`.
- Link to parent `KR-*`.
- Must not be treated as golden dataset expected output or snapshot text.

### 4.5 Relationship rules

1. Use only ontology edge types from `knowledge/graph/edge_types.json`.
2. Prefer `FOUNDATIONAL_FOR` for academic foundation; `DEPENDS_ON` for structural dependency.
3. No cycles on `FOUNDATIONAL_FOR` / `DEPENDS_ON`.
4. No duplicate `(type, source, target)` triples.
5. `RELATED_TO` is weak association — do not use it to hide missing foundation links.

### 4.6 Ontology rules

| Node type | When |
|-----------|------|
| Concept | Foundational / principle concepts |
| Entity | Named catalogs / entity sets |
| Rule | Formal rules |
| Pattern | Pattern types |
| Example | Examples |
| Source | Bibliography `SRC-*` |
| Pack / Module | Organizational containers only |

One canonical Concept node per `record_id`. Aliases are not second identities.

### 4.7 Review workflow (author view)

```text
draft → (submit) → review
         ├─ Academic review
         ├─ Technical review
         └─ Governance review → approved
              → freeze candidate → frozen → released/official
```

Authors prepare content and self-checklist; they do not self-approve official promotion.

Details: [REVIEW_GUIDE.md](REVIEW_GUIDE.md), `knowledge/governance/review_workflow.json`.

---

## 5. Indexes at authoring time

Authors SHOULD note intended:

- `canonical_key`
- aliases
- keywords / topics

Index files are updated at publication (`PB-03`), not by inventing parallel IDs during draft.

---

## 6. Done means

A draft is ready for review when:

- All mandatory template sections filled or explicitly `TODO_REVIEW`
- No invented `SRC-*`
- Relationships use approved types
- [CHECKLIST.md](CHECKLIST.md) completed
- Status remains `draft` until submit
