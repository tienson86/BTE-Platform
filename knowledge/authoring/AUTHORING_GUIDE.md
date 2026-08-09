# Authoring Guide

**Document:** AUTHORING_GUIDE  
**Version:** 1.1.0  
**Status:** Specification  
**Audience:** Knowledge Authors, Technical Reviewers, Domain Reviewers, Release Managers

This guide covers:

- **Part A** — Knowledge Package authoring (Sprint KD-4)
- **Part B** — Knowledge Record authoring (Sprint 4B, unchanged in intent)

---

# Part A — Knowledge Package authoring (KD-4)

## A1. Authoring philosophy

Knowledge is a **governed product**, not a dump of notes.

1. **Package first** — the deployable unit is a KD-3 Knowledge Package, not a loose file.
2. **Honesty over completeness** — unknown classical claims stay `TODO_REVIEW`; never invent sources.
3. **Determinism** — the same package bytes always validate and release the same way.
4. **Separation of duties** — authors draft; they do not sole-approve official release.
5. **Immutability after release** — fixes are new versions.
6. **Scale** — process must work for 100,000+ objects, parallel authors, multilingual and multi-school packages, and future AI-assisted tools.
7. **Additive compatibility** — existing Rule Database and Knowledge Records remain valid; this pipeline is the path for *new* official packages.

## A2. Validation philosophy

Validation is a **specified sequence**, not a single boolean.

- Run stages in declared order (`validation/validation_sequence.json`).
- Fail closed on errors; warnings require acknowledgment at release.
- No runtime validators are implemented in KD-4; future tools MUST follow this spec.
- Golden Dataset validation consumes existing golden tests; it MUST NOT modify golden files.

## A3. Review philosophy

Reviews protect readers and downstream engines.

- **Internal review** checks completeness and style.
- **Technical validation** checks schema, ids, dependencies, integrity.
- **Knowledge / domain review** checks academic meaning and school consistency.
- Reviewers record findings; they do not silently rewrite released meaning.
- AI-assisted drafts are allowed; human Domain Reviewer remains accountable for classical content.

## A4. Release philosophy

Release is a **publication event**.

- Only `release_candidate` (KD-3 `validated`) packages may enter the release pipeline.
- Checksum, notes, compatibility, and immutability are mandatory.
- Publication updates indexes/registries; it does not mutate sealed artifacts afterward.

## A5. How to start a package

1. Copy `package_template/` to a new folder named exactly `package_id`.
2. Replace placeholders using `templates/PACKAGE_TEMPLATE.json` and `MANIFEST_TEMPLATE.json`.
3. Add objects from `RULE_TEMPLATE.json` / `METADATA_TEMPLATE.json` (or KR templates from Part B).
4. Complete [checklists/draft_checklist.md](checklists/draft_checklist.md).
5. Follow [authoring_pipeline.md](authoring_pipeline.md) states through release.

Do not edit template files in place to store real knowledge.

## A6. Package authoring sequence

```text
idea → draft → internal_review → technical_validation
     → knowledge_review → release_candidate → released
     → deprecated → archived
```

Map to KD-3 `PACKAGE.json` `status` in `workflow/states.json`.

## A7. Done means (package draft)

A draft is ready for internal review when:

- `PACKAGE.json` + `MANIFEST.json` + `README.md` exist and match KD-3 schemas (after placeholder substitution)
- `domain_id` exists in taxonomy
- identifiers follow naming rules
- [checklists/draft_checklist.md](checklists/draft_checklist.md) completed
- status remains `draft` until submit

---

# Part B — Knowledge Record authoring (Sprint 4B)

**Audience:** Knowledge Authors writing KR markdown records.

## 1. Goal

Write Knowledge Records that are academically honest, machine-mappable, reviewable, and publishable under BTE governance.

When a KR ships inside a Knowledge Package, Part A gates still apply to the package.

## 2. Choose the right template

| If you are writing… | Use |
|---------------------|-----|
| Generic KR shell | `knowledge/templates/knowledge_record_template.md` |
| Foundational Concept | `foundational_concept_template.md` |
| Entity / catalog | `entity_template.md` |
| Rule (KR markdown) | `rule_template.md` |
| Rule (KD-3 JSON object) | `knowledge/authoring/templates/RULE_TEMPLATE.json` |
| Example only | `example_template.md` |
| Golden candidate overlay | `golden_record_template.md` |

Copy the template; do not edit the template file in place for content authoring.

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

For **packages**, use the KD-4 workflow in [authoring_pipeline.md](authoring_pipeline.md) instead of this KR-only path.

Authors prepare content and self-checklist; they do not self-approve official promotion.

Details: [REVIEW_GUIDE.md](REVIEW_GUIDE.md), `knowledge/governance/review_workflow.json`, `workflow/approvals.json`.

---

## 5. Indexes at authoring time

Authors SHOULD note intended:

- `canonical_key`
- aliases
- keywords / topics

Index files are updated at publication, not by inventing parallel IDs during draft.

---

## 6. Done means (KR draft)

A draft is ready for review when:

- All mandatory template sections filled or explicitly `TODO_REVIEW`
- No invented `SRC-*`
- Relationships use approved types
- [CHECKLIST.md](CHECKLIST.md) completed
- Status remains `draft` until submit
