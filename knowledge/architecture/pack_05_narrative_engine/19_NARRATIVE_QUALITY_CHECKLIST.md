# 19_NARRATIVE_QUALITY_CHECKLIST.md

Version: 1.0

Status: DRAFT — Sprint C Writing System

Pack: 05 (Narrative Engine)

Depends on: Sprint A (frozen) · Sprint B (frozen) · `13`–`18`

---

# 1. Purpose

This checklist is the official **quality gate** for BTE Narrative writing quality.

Use before accepting a NarrativeResult as commercially publishable.

It is documentation for review discipline — not runtime code.

---

# 2. Gate Result

| Result | Meaning |
|--------|---------|
| PASS | Publishable commercially |
| PASS WITH FLAGS | Publishable; insufficient slots explicitly marked |
| FAIL | Must not publish as complete commercial narrative |

Any FAIL item blocks commercial PASS.

---

# 3. Architecture / Grammar Gates (Sprint A / B)

| # | Check | Pass criteria |
|---|-------|---------------|
| G1 | Official flow order | Executive → Observation → Reasoning → Impact → Recommendation → Warning → Conclusion |
| G2 | Component shells present | All seven present (content may be Insufficient Evidence) |
| G3 | Meaning lock | No contradiction of AnalysisResult / validated Interpretation |
| G4 | No invention | No unsupported conclusions |
| G5 | Evidence refs | Filled units trace to evidence |
| G6 | Insufficient handling | Gaps use Insufficient Evidence — not filler |
| G7 | Role purity | Components do not steal each other’s jobs |

---

# 4. Voice / Tone Gates (Sprint C)

| # | Check | Pass criteria |
|---|-------|---------------|
| T1 | Consultant voice | Sounds like consultant, not calculator |
| T2 | Respect | No shame / insult / doom sales |
| T3 | Component tone | Tone matches component (esp. Warning calm; Recommendation clear) |
| T4 | Certainty match | Language strength matches evidence strength |
| T5 | Brand path | Supports trust → understanding → action |

---

# 5. Sentence / Paragraph Gates

| # | Check | Pass criteria |
|---|-------|---------------|
| S1 | One idea per sentence | No mega multi-role sentences |
| S2 | One role per paragraph | No mixed Observation+Action paragraphs |
| S3 | Compactness | No unnecessary walls of text |
| S4 | Balance readiness | Writing density allows presentation balance |
| S5 | No new claims in Conclusion | Close only |

---

# 6. Wording Gates

| # | Check | Pass criteria |
|---|-------|---------------|
| W1 | No rule-engine prose | No “Kích hoạt khi…”, procedure dumps |
| W2 | No developer prose | No mock/placeholder/PACK_/ViewModel |
| W3 | No absolute prophecy | No unsupported “chắc chắn sẽ…” |
| W4 | Terminology consistency | Same concepts named consistently |
| W5 | No internal IDs | No rule codes as customer text |
| W6 | Language | Customer narrative language rules respected |
| W7 | Numbers | Scores used with meaning, not as a dump |

---

# 7. Executive Summary Gates

| # | Check | Pass criteria |
|---|-------|---------------|
| E1 | Five slots addressed | Identity, strengths, weaknesses, priority, next action |
| E2 | Slot honesty | Missing → Insufficient Evidence flag |
| E3 | Alignment | Matches body components |
| E4 | Brevity | Scannable briefing, not a full essay |

---

# 8. Commercial Readiness Mini-Gate

Ask:

1. Who is this person? — answered or insufficient  
2. Main strengths? — answered or insufficient  
3. Main weaknesses? — answered or insufficient  
4. Priority recommendation? — answered or insufficient  
5. Next action? — answered or insufficient  

If any answered slot fails wording/tone/evidence checks → FAIL.

---

# 9. Reviewer Sign-off Block

| Field | Value |
|-------|-------|
| Narrative run id | |
| Reviewer | |
| Date | |
| Gate result | PASS / PASS WITH FLAGS / FAIL |
| Failed item ids | |
| Notes | |

---

# 10. Out of Scope for This Checklist

✗ UI layout / Design System compliance (other checklists)  
✗ Score correctness (Score Engine tests)  
✗ Runtime performance  
✗ Template authoring completeness (future content sprint)  

---

END
