# 05 — Acceptance Criteria

Version: 1.0  
Status: **OFFICIAL — Commercial Consulting Acceptance Criteria**  
Date: 2026-08-08  
Depends on: `01`, `03`, `04` · Wave 1.1 · EPIC 4 Sprint B  
Scope: Documentation only — release gate definition  

---

## 1. Purpose

Define the **minimum consulting quality** required before commercial release of BTE consultation output.

Passing engineering tests is not enough.  
Cases in the commercial release set must pass this gate via the Case Review Workflow (`03`).

---

## 2. Release objects

| Object | Gate applies? |
|--------|:-------------:|
| NarrativeResult for Result / consultation surfaces | Yes |
| Wave 1.1 Commercial Knowledge enrichment | Yes (when selected) |
| Engine unit tests / golden analytical tests | Prerequisite only |
| Portal chrome / Design System polish | Out of scope (Foundation frozen) |
| Wave 1.2+ knowledge depth | Not required for this gate |

---

## 3. Minimum scorecard thresholds

A case is **consulting-accepted** only if all of the following hold:

| Rule | Minimum |
|------|---------|
| Overall rating | **Acceptable** or better (`04` §5) |
| Dimension average | ≥ **7.0** |
| Accuracy | ≥ **7** |
| Trustworthiness | ≥ **7** |
| Professionalism | ≥ **7** |
| Actionability | ≥ **7** |
| Consistency | ≥ **7** |
| Naturalness | ≥ **6** |
| Readability | ≥ **6** |
| Empathy | ≥ **6** |
| Commercial Value | ≥ **7** |
| Decision Support | ≥ **7** |
| Blocker defects | **0** |
| Major defects | **0** open (all Major closed or waived by Product in writing) |

**Launch recommendation (Product may tighten):** prefer release set average overall **Good**, with ≥ 80% of cases ≥ Acceptable and zero Blockers across the set.

---

## 4. Surface-level must-pass criteria

### 4.1 Executive Summary

| Criterion | Required |
|-----------|----------|
| Identity understandable in consultant language | Yes |
| No invented analytical facts | Yes |
| No technical wording leak | Yes |
| Strength/weakness honesty appropriate to signals | Yes |
| Aligns with Recommendation priority | Yes |

### 4.2 Recommendation

| Criterion | Required |
|-----------|----------|
| Clear primary action (not token-only) when useful god present | Yes |
| Reason present when commercial enrichment applies | Yes |
| No guaranteed-returns / medical-legal overclaim | Yes |
| Does not overwrite analytical meaning (scores/grades/truth) | Yes |

### 4.3 Warning

| Criterion | Required |
|-----------|----------|
| Present when material risk/weakness signals exist | Yes |
| Calm, non-shaming tone | Yes |
| Absent invention when no risk signal | Yes (insufficient OK) |

### 4.4 Narrative

| Criterion | Required |
|-----------|----------|
| No contradiction across Exec / Rec / Warning | Yes |
| Insufficient slots not padded with fiction | Yes |
| Wave 1.1-only knowledge (no undeclared units) | Yes |

---

## 5. Hard fail conditions (automatic non-acceptance)

Any one of the following **fails** the case regardless of average:

1. Contradicts Analysis on day master / strength band / useful god / core pattern when those signals exist  
2. Invents chart facts or Wave 1.2 knowledge  
3. Ethics breach (shame, doom marketing, medical diagnosis, guaranteed outcomes)  
4. Technical residue in customer text (`kích hoạt khi`, matched-rules dumps, placeholders)  
5. Recommendation that reverses Dụng thần without explicit, evidence-bound rationale  
6. Loss of required provenance for commercial claims under review (no KU id when Wave 1.1 text is used)  

---

## 6. Case-set acceptance (commercial release)

Product releases consulting commercially only when:

| Gate | Criterion |
|------|-----------|
| Case coverage | Agreed fixture set reviewed under `03` (strong, weak, no useful god, thin evidence at minimum) |
| Per-case | Each included case meets §3–§5 |
| Knowledge | Only Wave 1.1 approved source for commercial enrichment |
| Engineering | Relevant module tests green (prerequisite) |
| Product sign-off | Written approval recorded |

A single failing critical fixture blocks release until Revise or fixture replacement.

---

## 7. Waivers

| Waiver type | Allowed? | Authority |
|-------------|----------|-----------|
| Minor polish deferred | Yes | Consultant Reviewer + note |
| Major defect open | No (unless Product written waiver with expiry) | Product |
| Blocker | Never waived for commercial release | — |
| Missing Wave 1.2 depth | Not a defect | — |

---

## 8. Out of scope for this gate

- Visual Design System compliance (separate Foundation checklist)  
- Report Engine completeness  
- Multi-language locales beyond current commercial VI  
- Knowledge Publish workflow mechanics (EPIC 3) beyond Wave 1.1 allow-list policy  

---

## 9. Success definition for EPIC 5 Sprint A

Documentation complete when Product can answer:

1. What dimensions we score (`01`)  
2. How reviewers evaluate surfaces (`02`)  
3. How cases move to approval (`03`)  
4. How scores become ratings (`04`)  
5. What minimums unlock commercial release (`05`)  

Implementation of tooling is **out of scope** for Sprint A.

---

## 10. Stop line

Acceptance criteria defined.  
**Stop after Sprint A. Wait for Product review. No runtime. No Wave 1.2.**

---

END
