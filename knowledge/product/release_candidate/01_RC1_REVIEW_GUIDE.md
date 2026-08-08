# 01 — RC1 Review Guide · Commercial V1 Release Candidate

Version: 1.0.0  
Status: **OFFICIAL — Human Consulting Validation Package**  
Date: 2026-08-08  
Release candidate: **Commercial V1 · RC1**  
Scope: Documentation only — package & verify; no runtime / Knowledge / Narrative / Portal changes  

---

## 1. Purpose

Commercial V1 engineering is complete. Architecture is frozen. Capability Registry lists:

| Capability | Registry ID | Capability status |
|------------|-------------|-------------------|
| Career Selection Assessment | CAP-CAREER-SEL-001 | Released (production path) |
| Promotion Readiness Assessment | CAP-CAREER-PRO-001 | Released (production path) |

**Commercial V1 as a product release** is still gated by **Human Consulting Validation**.

This guide explains how Product / consulting reviewers validate the **customer-facing Result report** for RC1.

**Do not declare Commercial V1 Released in this sprint.**

---

## 2. Review objectives

1. Confirm the full Result experience feels like a **senior consultant**, not a rule dump.  
2. Confirm **Career Selection Assessment** is primary Career Strategy and clearly findable.  
3. Confirm **Promotion Readiness Assessment** is a secondary career milestone and clearly findable.  
4. Confirm Executive Summary and Recommendation meet Commercial V1 polish bar (structure + actionability).  
5. Produce a signed **Consulting Acceptance** and an official **RC1 Release Decision** (GO / GO WITH MINOR FIXES / NO GO).

---

## 3. Review process

```
Prep package (this folder)
        ↓
Assign reviewers + cases
        ↓
Independent case review (Checklist + Scoring Sheet)
        ↓
Consolidate Acceptance Forms
        ↓
Product records RC1 Release Decision
        ↓
(If GO / GO WITH MINOR FIXES) schedule Commercial V1 release notes update
(If NO GO) return to polish backlog — no capability expansion
```

### Steps

| Step | Action | Owner |
|------|--------|-------|
| 1 | Read this Guide + Acceptance minima (`consulting_quality/05`) | Reviewer |
| 2 | Run / view each mandatory case Result (customer-facing only) | Reviewer |
| 3 | Complete `02_CASE_REVIEW_CHECKLIST.md` per case | Reviewer |
| 4 | Complete `03_CASE_SCORING_SHEET.md` per case | Reviewer |
| 5 | Submit `04_CONSULTING_ACCEPTANCE_FORM.md` | Reviewer |
| 6 | Fill `05_RC1_RELEASE_DECISION.md` | Product Owner |

---

## 4. Review roles

| Role | Responsibility |
|------|----------------|
| **Product Owner** | Final RC1 decision; waiver authority for minor fixes |
| **Consulting Reviewer** | Scores cases; Pass / Pass with minor fixes / Reject |
| **Engineering (support only)** | Provides Result access / fixtures — **no code changes during RC1 review** |
| **Domain Knowledge (optional)** | Advises on accuracy disputes — does not override Product decision |

---

## 5. Review criteria (summary)

Aligned with Consulting Quality Acceptance and Commercial V1 P0 polish:

| Criterion | Minimum expectation |
|-----------|---------------------|
| Accuracy | No invented facts; aligns with chart signals |
| Completeness | Exec, Rec, Career, Promotion (as secondary), Knowledge path coherent |
| Clarity | First-time customer can follow central message |
| Commercial value | Customer would pay for decision support |
| Actionability | Primary Rec has What / Why / How / When / Expected outcome |
| Trustworthiness | Ethical hedges; no salary/title guarantees |
| Tone | Consultant, not calculator |
| Consistency | Career primary; Promotion secondary; no contradictory advice |

Full per-case checklist: `02`.  
Numeric scoring: `03`.  
Decision form: `04`.  
Release outcomes: `05`.

---

## 6. Surfaces in scope

Review the **complete customer-facing report**:

1. Executive Summary  
2. Analysis  
3. Visualization  
4. Career Selection Assessment  
5. Promotion Readiness Assessment  
6. Recommendations (primary + secondary milestone)  
7. Knowledge / Interpretation depth  
8. Overall consulting experience (trust → understanding → action)

Out of scope for RC1 human review: Foundation redesign, new Capabilities, Engine correctness re-litigation (engineering Golden Cases are prerequisites).

---

## 7. Mandatory case set

| Case id | Profile | Focus |
|---------|---------|-------|
| RC1-STRONG | Strong + useful god | Baseline commercial quality |
| RC1-WEAK | Weak + enemy + useful god | Mitigate-first honesty |
| RC1-MIXED | Strong + enemy + useful god | Balanced strength + caution |
| RC1-CAREER | Strong + useful god | Career Selection as primary |
| RC1-PROMOTE | Strong + useful god | Promotion as secondary milestone |

Engineering fixture donors: `tests/domain01/conftest.py` (strong / weak / mixed).  
Prior P0-06 package: `knowledge/product/commercial_v1/10_HUMAN_CONSULTING_REVIEW_PACKAGE.md`.

---

## 8. Expected outputs

| Output | File |
|--------|------|
| Per-case checklist | Completed copies of `02` |
| Per-case scores | Completed copies of `03` |
| Reviewer acceptance | Completed copies of `04` |
| Official RC1 decision | Completed `05` (Product Owner) |

---

## 9. Prerequisites verified (engineering — not human sign-off)

| Prerequisite | Evidence |
|--------------|----------|
| Capability Registry lists SEL + PRO | `knowledge/product/01_CAPABILITY_REGISTRY.md` |
| Release notes (capability) | Domain `23`, `30` |
| Golden Cases | Domain `22`, `25`, `29`; `tests/domain01` |
| Regression | `tests/commercial_knowledge` + Domain validation reports |
| P0 polish engineering | `commercial_v1/07`–`09` |
| Commercial V1 product Released? | **Not declared** — pending this human gate |

---

## 10. Stop line

RC1 Review Guide published.  

**Wait for Product / consulting review. Do not declare Commercial V1 Released.**

---

END
