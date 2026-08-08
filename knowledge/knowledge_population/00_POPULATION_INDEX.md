# 00 — Population Index

Version: 1.1  
Status: **EPIC 3 · Framework frozen · Golden Review complete**  
Date: 2026-08-08  
Depends on: EPIC 2 Knowledge Model (`knowledge/knowledge_enhancement/model/`) — **frozen**  
Scope: Population framework + Golden Review docs — Wave 1.1 units remain `awaiting_review` until Product authorize status change  

---

## 1. Purpose

This folder defines the official **Knowledge Population Framework**: *how* Knowledge Units will be created, reviewed, validated, versioned, and published.

| This epic defines | This epic does not |
|-------------------|--------------------|
| Workflows & gates | Unit `body` content |
| Review & approval | Database rows |
| Validation & versioning | Engine / Portal / Report code |
| Wave execution plan | Physical store format choice (deferred to impl epic) |

**Commercial Knowledge remains the advisory SSOT.**  
Population produces **Published Knowledge Units** that composition/retrieval may later consume.

---

## 2. Reading order

| Order | File | Content |
|------:|------|---------|
| 0 | `00_POPULATION_INDEX.md` | This index |
| 1 | `01_POPULATION_WORKFLOW.md` | End-to-end author → publish flow |
| 2 | `02_REVIEW_PROCESS.md` | Technical, Knowledge, Commercial, Narrative reviews |
| 3 | `03_VALIDATION_RULES.md` | Quality gates & checklists |
| 4 | `04_VERSIONING_POLICY.md` | Ids, semver, supersession, deprecation |
| 5 | `05_WAVE_EXECUTION_PLAN.md` | Waves aligned to catalog P0–P2 |
| 6 | `06_GOLDEN_KNOWLEDGE_STANDARD.md` | Official Golden quality criteria |
| 7 | `07_KNOWLEDGE_REVIEW_GUIDE.md` | Review order including Product Review |
| 8 | `08_KNOWLEDGE_QUALITY_SCORE.md` | 0–10 × 10 categories scoring |
| 9 | `09_GOLDEN_UNIT_REFERENCE.md` | Wave 1.1 unit evaluation |
| 10 | `10_WAVE_1_1_FINAL_APPROVAL.md` | Official APPROVED + publish HOLD |

**Reviewers (framework):** 00 → 01 → 02 → 03 → 04 → 05.  
**Reviewers (Golden):** 00 → 06 → 07 → 08 → 09 → 10.  
**Future authors:** 00 → 06 → 08 → 15 (EPIC 2) → 05 → catalog.

---

## 3. Dependency on EPIC 2

```
EPIC 2 Model (frozen)
  11–15 Knowledge Unit + lifecycle + authoring
  16–20 Catalog + implementation plan
        ↓
EPIC 3 Sprint A Population Framework (this folder)
        ↓ (after review + content authorization)
Future content sprints (author bodies → Published)
        ↓ (separate implementation epic)
Retrieval / composition wiring
```

| EPIC 2 source | Used here for |
|---------------|---------------|
| `14_KNOWLEDGE_LIFECYCLE.md` | Stage names & owners |
| `15_KNOWLEDGE_AUTHORING_STANDARD.md` | Author rules & naming |
| `12_KNOWLEDGE_UNIT_SCHEMA.md` | Field validation |
| `16_KNOWLEDGE_CATALOG.md` | What to populate |
| `20_KNOWLEDGE_IMPLEMENTATION_PLAN.md` | Phase/wave targets |
| `19_NARRATIVE_SUPPORT_MATRIX.md` | Narrative gates / min pack |

---

## 4. Architectural invariants

| Invariant | Meaning |
|-----------|---------|
| No Rule Database duplication | Population never copies thresholds/weights |
| No Narrative invention | Units supply meaning; Narrative composes |
| No Foundation edits | Voice constraints only |
| Catalog-first | Prefer reserved ids from `16`; amend catalog before inventing ids |
| Published-only production | Draft/Approved never feed prod Narrative |
| Honesty over filler | Prefer insufficient over fake Advance |

---

## 5. Roles (summary)

| Role | Responsibility |
|------|----------------|
| Knowledge Author | Draft units per catalog wave |
| Technical Reviewer | Schema, conditions, no rule duplication |
| Knowledge Reviewer | BaZi meaning, ethics correctness |
| Commercial Reviewer | Customer value, brand, priority fit |
| Narrative Reviewer | Pack 05 / Content Quality fit |
| Release / Knowledge Ops | Approve → Publish, manifests, deprecation |
| Knowledge Architect | Catalog amendments, conflict policy |

Detail: `02_REVIEW_PROCESS.md`.

---

## 6. Success criteria (Sprint A)

| Criterion | Status target |
|-----------|---------------|
| Author workflow defined | `01` |
| Review workflow defined | `02` |
| Validation / quality gates defined | `03` |
| Versioning policy defined | `04` |
| Wave planning defined | `05` |
| Zero Knowledge Units created | Required |
| Zero database population | Required |

---

## 7. Stop line

Sprint A ends at review.  
**Do not create Knowledge Units. Do not populate databases.**

---

END
