# 04 — Consulting Scorecard

Version: 1.0  
Status: **OFFICIAL — Consulting Scorecard**  
Date: 2026-08-08  
Depends on: `01_CONSULTING_QUALITY_FRAMEWORK.md`  
Scope: Documentation only — scoring instrument  

---

## 1. Purpose

Provide the official scorecard for human consulting-quality review.

Each dimension is scored **0–10**.  
Overall rating is derived from averages and hard gates (see §5 and `05`).

---

## 2. Scoring scale (per dimension)

| Score | Meaning |
|------:|---------|
| 0–2 | **Failing** — harmful, inventing, or unusable |
| 3–4 | **Poor** — major consulting defects |
| 5–6 | **Borderline** — partially usable; not commercial-ready alone |
| 7–8 | **Good** — professional consultation with minor issues |
| 9–10 | **Excellent** — release exemplar for this dimension |

Reviewers must use integers. Half-points are not used in Sprint A.

---

## 3. Dimension scorecard (blank)

| # | Dimension | Score (0–10) | Notes / evidence |
|--:|-----------|:------------:|------------------|
| 1 | Accuracy | | |
| 2 | Professionalism | | |
| 3 | Naturalness | | |
| 4 | Readability | | |
| 5 | Actionability | | |
| 6 | Commercial Value | | |
| 7 | Consistency | | |
| 8 | Empathy | | |
| 9 | Trustworthiness | | |
| 10 | Decision Support | | |

**Dimension average** = sum(scores) / 10  

Round overall average to one decimal for reporting.

---

## 4. Surface coverage checklist

Mark each surface reviewed:

| Surface | Reviewed? | Critical defects |
|---------|:---------:|------------------|
| Executive Summary | ☐ | |
| Recommendation | ☐ | |
| Warning | ☐ | |
| Narrative (full) | ☐ | |

A scorecard is incomplete if Exec or Recommendation is unchecked.

---

## 5. Overall rating bands

| Overall rating | Rule (default) |
|----------------|----------------|
| **Excellent** | Average ≥ 9.0 **and** no dimension &lt; 8 **and** no Blocker defects |
| **Good** | Average ≥ 8.0 **and** no dimension &lt; 7 **and** no Blocker defects |
| **Acceptable** | Average ≥ 7.0 **and** no dimension &lt; 6 **and** Accuracy ≥ 7 **and** Trustworthiness ≥ 7 **and** no Blocker defects |
| **Needs Improvement** | Any of the above not met |

Hard overrides (always **Needs Improvement** or Reject path):

- Accuracy ≤ 5  
- Trustworthiness ≤ 5  
- Any Blocker ethics / invention / guarantee defect  

Commercial release uses `05_ACCEPTANCE_CRITERIA.md` (stricter than “Acceptable” may be required for launch).

---

## 6. Case header (required fields)

| Field | Value |
|-------|-------|
| Case id | |
| Scenario id | |
| Run id | |
| Knowledge wave | W-P0-1.1-CORE |
| Reviewer | |
| Date | |
| Narrative status | |
| Bundle status (if any) | |
| Decision | Approve / Revise / Reject / Escalate |
| Overall rating | Excellent / Good / Acceptable / Needs Improvement |
| Dimension average | |

---

## 7. Defect log (attach)

| ID | Surface | Severity | Dimension(s) | Description | Resolution |
|----|---------|----------|--------------|-------------|------------|
| D-001 | | Blocker/Major/Minor/Observation | | | |

---

## 8. Scoring guidance (anchors)

| Dimension | 4 (Poor) | 7 (Good) | 9 (Excellent) |
|-----------|----------|----------|---------------|
| Accuracy | Contradicts signal | Aligns; minor wording stretch | Precise bind; no overclaim |
| Professionalism | Shame / hype / calculator dump | Calm consultant | Exemplar brand voice |
| Naturalness | Label dump / template glue | Readable prose | Feels like a live consult |
| Readability | Dense / flat | Clear hierarchy | Scannable in &lt; 1 minute |
| Actionability | Vague or token-only | Clear priority + step | Action/reason/next crisp |
| Commercial Value | No lift vs calculator | Worth paid glance | Customer leaves with plan |
| Consistency | Exec↔Rec conflict | Aligned story | Seamless arc |
| Empathy | Blame or fear | Calm limits | Care without soft-washing truth |
| Trustworthiness | Fake certainty | Honest insufficient | Transparent + traced |
| Decision Support | Pure description | Usable posture | Clear prepare/prioritize path |

---

## 9. Worked example (illustrative only)

Not a Golden Dataset. Hypothetical strong + useful-god case after Wave 1.1:

| Dimension | Score |
|-----------|------:|
| Accuracy | 9 |
| Professionalism | 8 |
| Naturalness | 8 |
| Readability | 8 |
| Actionability | 9 |
| Commercial Value | 8 |
| Consistency | 8 |
| Empathy | 8 |
| Trustworthiness | 8 |
| Decision Support | 9 |
| **Average** | **8.3** |
| **Overall** | **Good** |

---

## 10. Stop line

Scorecard defined. Acceptance thresholds for commercial release: `05`.

---

END
