# Feature Matrix V1.0 — Full Matrix

| Field | Value |
|-------|-------|
| Document | FEATURE_MATRIX |
| Version | 1.0.0 |

Legend: **R** Required · **O** Optional · **U** Unavailable · Priority **P0/P1/P2**

Commercial output codes:

| Code | Output |
|------|--------|
| ID | Identity chapter |
| SYS | Operating system chapter |
| STR | Structure / destiny frame |
| BAL | Balance strategy |
| EXT | External influences |
| TIME | Life timeline |
| EXEC | Executive consulting report |
| CAREER | Career consulting block |
| REL | Relationship block |
| PDF | PDF deliverable |
| SUM | Shareable summary |

---

## Matrix (Top 50)

| ID | Priority | S | TG | P | UG | SS | L | EX | Interpretation focus | Commercial output |
|----|----------|---|----|---|----|----|---|-----|----------------------|-------------------|
| Q01 | P0 | R | R | R | O | O | U | R | Integrated identity | ID + EXEC |
| Q02 | P0 | R | R | R | R | O | O | R | Priorities synthesis | EXEC |
| Q03 | P0 | R | R | O | O | O | U | O | Strengths | ID |
| Q04 | P0 | O | R | O | R | O | U | O | Challenges / load | SYS + BAL |
| Q05 | P0 | R | R | R | R | U | O | R | Career path | CAREER + EXEC |
| Q06 | P0 | O | R | R | O | U | U | O | Role fit | CAREER |
| Q07 | P0 | R | R | O | R | U | U | O | Pressure management | SYS + BAL |
| Q08 | P1 | O | R | R | O | U | U | O | Environment fit | CAREER |
| Q09 | P0 | R | O | O | R | U | U | O | Balance when heavy | BAL |
| Q10 | P0 | R | R | R | R | O | U | R | One insight | EXEC |
| Q11 | P0 | O | R | O | R | U | U | O | Stop / unload | BAL + EXEC |
| Q12 | P0 | R | R | R | R | O | U | R | Act this month | EXEC + PDF |
| Q13 | P1 | U | U | O | U | U | R | O | Current chapter | TIME |
| Q14 | P1 | O | O | O | O | U | R | O | Expand vs protect | TIME |
| Q15 | P1 | O | O | O | O | U | R | O | Commitment timing | TIME |
| Q16 | P1 | U | U | O | U | U | R | O | Decade narrative | TIME |
| Q17 | P1 | O | O | R | O | U | R | O | Prepare next chapter | TIME + STR |
| Q18 | P2 | O | O | O | O | U | R | O | Year career moves | TIME (+OTH later) |
| Q19 | P1 | O | R | O | R | U | R | O | Move / launch timing | TIME + CAREER |
| Q20 | P2 | U | U | U | U | U | R | U | Past year map | TIME |
| Q21 | P2 | U | O | O | U | U | R | O | Decade emotion | TIME |
| Q22 | P1 | U | U | O | U | U | R | O | Full timeline | TIME + PDF |
| Q23 | P1 | O | R | O | O | O | U | O | Relationship style | REL |
| Q24 | P1 | O | R | O | O | O | U | O | Partner dynamics | REL |
| Q25 | P2 | U | O | U | U | R | U | O | Attraction pattern | EXT |
| Q26 | P1 | O | R | O | O | O | U | O | Conflict handling | REL |
| Q27 | P1 | U | U | U | U | R | U | O | Supportive people | EXT |
| Q28 | P1 | O | R | R | O | O | U | O | Family / duty | REL + STR |
| Q29 | P1 | O | R | R | O | U | U | O | Solo vs team | CAREER + REL |
| Q30 | P1 | O | R | O | R | O | U | O | Habit change | REL + BAL |
| Q31 | P1 | O | R | O | O | U | U | O | Money style | CAREER |
| Q32 | P1 | R | O | O | R | U | O | O | Risk now | BAL + EXEC |
| Q33 | P1 | O | R | R | R | U | U | O | Business model | CAREER |
| Q34 | P0 | R | R | O | R | U | U | O | Energy ROI | BAL + SYS |
| Q35 | P1 | R | O | R | R | U | O | O | Stability vs opp. | EXEC |
| Q36 | P0 | R | R | R | O | U | U | R | Success definition | EXEC |
| Q37 | P1 | R | O | O | R | O | U | O | Recovery | BAL |
| Q38 | P0 | R | R | R | R | O | O | R | 2–3y focus | EXEC + PDF |
| Q39 | P1 | R | O | O | R | U | U | O | Stress system | BAL |
| Q40 | P1 | R | O | O | R | U | U | O | Weekly rhythm | BAL |
| Q41 | P0 | R | R | O | R | U | U | O | Burnout risk | BAL + SYS |
| Q42 | P1 | R | O | O | R | U | U | O | Rest protocol | BAL |
| Q43 | P1 | R | O | O | R | U | U | O | Warning signs | BAL |
| Q44 | P1 | R | O | O | R | O | U | O | Rebuild plan | BAL |
| Q45 | P0 | O | O | O | O | O | O | R | Trust narrative | EXEC + SUM |
| Q46 | P0 | O | O | O | O | O | O | R | Honesty / gaps | EXEC |
| Q47 | P0 | R | R | R | R | O | U | R | One report | EXEC + PDF |
| Q48 | P0 | O | O | O | O | O | U | R | Shareable summary | SUM |
| Q49 | P0 | R | R | R | R | O | O | O | Consistency | Product trust |
| Q50 | P1 | O | O | O | O | O | O | R | Next step | Funnel CTA |

---

## Reading rule

If any **R** domain is Unavailable in production:

- Feature ships as **PARTIAL** or **NOT_AVAILABLE**
- EX may still answer with explicit restraint (Q46)
- Never fill Luck/ShenSha gaps with Strength prose
