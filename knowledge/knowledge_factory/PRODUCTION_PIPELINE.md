# Production Pipeline — V1.0

| Field | Value |
|-------|-------|
| Document | PRODUCTION_PIPELINE |
| Version | 1.0.0 |
| Section | 2 — Pipeline |

---

# 2.1 Frozen pipeline

```text
Idea
  ↓  [QG0]
Draft (Knowledge Library)
  ↓  [QG1]
Knowledge Catalog
  ↓  [QG2]
QA
  ↓  [QG3]
Review
  ↓  [QG4]
Validation
  ↓  [QG5]
Freeze
  ↓  [QG6]
Production
  ↓  [QG7]
Release
```

**No stage may continue without passing its quality gate.**

Gates: [QUALITY_GATES.md](QUALITY_GATES.md).

---

# 2.2 Stage definitions

## Stage 0 — Idea

| Field | Value |
|-------|-------|
| **Input** | Domain need, pack charter, Interpretation Standard alignment |
| **Output** | Approved pack scope document |
| **Owner** | Chief Reviewer + Product |
| **Artifact** | Pack charter (in pack README or governance record) |

Professional domain is identified. No prose yet.

---

## Stage 1 — Draft (Knowledge Library)

| Field | Value |
|-------|-------|
| **Input** | Pack charter, Rule Database fact boundaries |
| **Output** | Interpretation Knowledge prose chapters |
| **Owner** | Knowledge Author |
| **Artifact** | `knowledge/interpretation_knowledge/PACK_XX_*/` |
| **Unit status** | N/A — prose, not catalog units |

Consulting-grade chapters: meanings, causes, advantages, life domains, recommendations, edge cases, examples.

Detail: [AUTHORING_PIPELINE.md](AUTHORING_PIPELINE.md).

---

## Stage 2 — Knowledge Catalog

| Field | Value |
|-------|-------|
| **Input** | Approved Knowledge Library |
| **Output** | Deterministic Knowledge Units (Draft) |
| **Owner** | Knowledge Author (+ Cursor assist) |
| **Artifact** | `knowledge/knowledge_catalog/PACK_XX_*/catalog/` |
| **Unit status** | **Draft** |

One claim per unit. Schema per pack. Source trace required.

Detail: [CATALOG_PIPELINE.md](CATALOG_PIPELINE.md).

---

## Stage 3 — QA

| Field | Value |
|-------|-------|
| **Input** | Draft catalog units (by topic phase) |
| **Output** | Phase QA reviews with PASS / REVIEW / FAIL |
| **Owner** | QA Assistant (Cursor may assist) |
| **Artifact** | `knowledge/knowledge_qa/PACK_XX_*/PHASE_NN_*_REVIEW.md` |
| **Unit status** | Remains **Draft** |

Scores twelve criteria per Knowledge QA Standard V1.0. Does not rewrite knowledge.

Detail: [QA_PIPELINE.md](QA_PIPELINE.md).

---

## Stage 4 — Review

| Field | Value |
|-------|-------|
| **Input** | QA PASS units + documented REVIEW items |
| **Output** | Domain Reviewer acceptance; units → **Reviewed** |
| **Owner** | Domain Reviewer |
| **Artifact** | Sign-off in phase review + QA_CHECKLIST |
| **Unit status** | **Reviewed** |

Human accepts or rejects QA. Resolves Borderline. Cursor is not final authority.

Detail: [APPROVAL_FLOW.md](APPROVAL_FLOW.md).

---

## Stage 5 — Validation

| Field | Value |
|-------|-------|
| **Input** | Reviewed units; Reasoning golden cases |
| **Output** | Golden alignment confirmed; units → **Validated** |
| **Owner** | Domain Reviewer + Reasoning governance |
| **Artifact** | Validation record; golden pin updates if needed |
| **Unit status** | **Validated** |

Proves selected units work in golden narratives. Does not run full Reasoning Engine in Factory V1.0 — validates **alignment**, not code.

Detail: [VALIDATION_PIPELINE.md](VALIDATION_PIPELINE.md).

---

## Stage 6 — Freeze

| Field | Value |
|-------|-------|
| **Input** | All production-scope units Validated |
| **Output** | Immutable catalog version |
| **Owner** | Chief Reviewer + Governance |
| **Artifact** | Catalog version bump; FREEZE record |
| **Unit status** | **Frozen** |

No silent edits after freeze.

Detail: [FREEZE_PIPELINE.md](FREEZE_PIPELINE.md).

---

## Stage 7 — Production

| Field | Value |
|-------|-------|
| **Input** | Frozen catalog |
| **Output** | Reasoning Engine loads Frozen units only |
| **Owner** | Production Owner |
| **Artifact** | Production config pointing to catalog version |
| **Unit status** | **Frozen** (consumed) |

Production Engine reads Frozen catalog. Factory does not implement engine.

Detail: [RELEASE_PIPELINE.md](RELEASE_PIPELINE.md).

---

## Stage 8 — Release

| Field | Value |
|-------|-------|
| **Input** | Production-verified pack |
| **Output** | Customer-visible knowledge release |
| **Owner** | Release Manager |
| **Artifact** | Release version tag; release notes |
| **Unit status** | **Frozen** |

Release is the **business event**. Freeze is the **technical immutability event**.

---

# 2.3 Parallel work

| Parallel track | Rule |
|----------------|------|
| Authoring next topic while QA prior topic | Allowed |
| Catalog before Library complete | Not allowed for that topic |
| QA before Catalog | Not allowed |
| Validation before Review | Not allowed |
| Production before Freeze | Not allowed |

---

# 2.4 Rollback

| From | Rollback to | Requires |
|------|-------------|----------|
| Reviewed | Draft | Domain Reviewer note; re-QA |
| Validated | Reviewed | Governance note |
| Frozen | — | New catalog version only (no unfreeze) |
| Production | Previous Frozen version | Production Owner + Release Manager |
| Released | Prior release version | Change pipeline |

Detail: [CHANGE_PIPELINE.md](CHANGE_PIPELINE.md).

---

END
