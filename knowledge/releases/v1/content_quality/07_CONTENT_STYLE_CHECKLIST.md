# 07 — Content Style Checklist

Version: 1.0  
Status: **Release B — Content Quality**  
Date: 2026-08-08  
Scope: Review gate for future content reviews — no runtime change

---

## 1. Purpose

Use this checklist for every narrative and commercial copy review after Release B.

A piece of content passes only when it is:

**Clear · Natural · Evidence-based · Respectful · Professional · Readable · Actionable · Traceable**

Results: `PASS` / `PASS WITH FLAGS` / `FAIL`

---

## 2. When to use

| Content type | Use checklist |
|--------------|---------------|
| Executive Summary | Full §3 + §4 Executive |
| Observation / Reasoning / Impact | Full §3 |
| Recommendation | Full §3 + §5 Recommendation |
| Warning | Full §3 + §6 Warning |
| Conclusion | Full §3 |
| Knowledge entries | Full §3 + §7 Knowledge |
| Portal chrome / states | §3 relevant rows + §8 Copy |

---

## 3. Universal narrative checklist

### Clear

- [ ] C1 One idea per sentence  
- [ ] C2 Reader can paraphrase the point in one plain sentence  
- [ ] C3 No ambiguous pronouns that hide the subject  

### Natural

- [ ] N1 Sounds like a consultant speaking, not a system log  
- [ ] N2 No rule-engine phrasing (“Kích hoạt khi…”, “Áp dụng bảng…”)  
- [ ] N3 No developer phrasing (mock, placeholder, TODO, PACK_0x, ViewModel)  
- [ ] N4 No English UI leftovers in Vietnamese commercial body  

### Evidence-based

- [ ] E1 Every claim is supported by Interpretation / Evidence  
- [ ] E2 No invented facts, timelines, or percentages  
- [ ] E3 Certainty matches evidence strength  
- [ ] E4 Insufficient slots use approved insufficient narrative — no soft filler  

### Respectful

- [ ] R1 No shaming language  
- [ ] R2 No moral judgment of the person’s worth  
- [ ] R3 Weaknesses framed as cautions, not condemnations  

### Professional

- [ ] P1 Tone matches component role (briefing / factual / explanatory / empathic / directive / cautionary / settling)  
- [ ] P2 No hype marketing  
- [ ] P3 No fortune-telling absolute prophecy  

### Readable

- [ ] D1 Paragraph length appropriate (typically 2–4 sentences for body roles)  
- [ ] D2 Commercial Vietnamese grammar is clean  
- [ ] D3 Skimmable structure (lead → support → optional bridge)  

### Actionable

- [ ] A1 Where the role requires action or caution, the reader knows what to do or watch  
- [ ] A2 Recommendations are specific — not generic slogans  
- [ ] A3 Warnings include mitigation when supported; otherwise caution only  

### Traceable

- [ ] T1 Meaning lock preserved (no inverted analysis)  
- [ ] T2 Role purity preserved (Observation ≠ Recommendation ≠ Warning)  
- [ ] T3 Evidence / interpretation references remain valid in the pipeline  

---

## 4. Executive Summary extras

- [ ] X1 Who is this person? answered or insufficient  
- [ ] X2 Core strengths present or insufficient  
- [ ] X3 Core weaknesses present or insufficient  
- [ ] X4 Primary opportunities expressed (or covered via strengths/priority) without invention  
- [ ] X5 Primary risks expressed (or covered via weaknesses) without invention  
- [ ] X6 Immediate priority clear  
- [ ] X7 Next action clear  
- [ ] X8 No generic filler briefing  

---

## 5. Recommendation extras

- [ ] Rec1 Specific to this analysis  
- [ ] Rec2 Actionable next step  
- [ ] Rec3 Reason grounded in evidence — not score dump  
- [ ] Rec4 Does not merely repeat Observation  
- [ ] Rec5 No unsupported conclusion or guaranteed outcome  
- [ ] Rec6 Priority coherent with Executive Summary  

---

## 6. Warning extras

- [ ] W1 Risk explained clearly  
- [ ] W2 No fear theater  
- [ ] W3 No false certainty  
- [ ] W4 Mitigation offered only when supported  
- [ ] W5 Severity within source claims  

---

## 7. Knowledge extras

- [ ] K1 Educates a term used by the analysis  
- [ ] K2 Does not interrupt core reading flow  
- [ ] K3 Not textbook / encyclopedia dump  
- [ ] K4 No technical / English jargon labels  

---

## 8. Portal copy extras

- [ ] U1 Titles / buttons / labels match one VI commercial voice  
- [ ] U2 Loading / empty / error states are Vietnamese, calm, and helpful  
- [ ] U3 No TECHNICAL leakage (`Score payload`, `Insight`, `N/A`, EN gates)  
- [ ] U4 No PLACEHOLDER leakage in production paths  
- [ ] U5 CTA tells the user the next useful step  

---

## 9. Forbidden pattern quick scan

Fail immediately if any appear in customer-facing copy:

| Class | Examples |
|-------|----------|
| Rule engine | Kích hoạt khi…, Áp dụng bảng… |
| Developer | (mock), placeholder, TODO, chờ engine, PACK_0x |
| Prophecy | chắc chắn sẽ…, định mệnh không thể đổi |
| Fear | thảm họa chắc chắn… |
| Shame | mệnh xấu tuyệt đối… |
| Calculator dump | điểm số chứng minh bạn kém… |
| English UI on VI | Loading executive summary, Knowledge, Score payload |

---

## 10. Scoring guidance

| Result | Rule |
|--------|------|
| **PASS** | All required checks for the content type pass |
| **PASS WITH FLAGS** | Minor polish issues only; no meaning / safety / jargon failures |
| **FAIL** | Any invention, fear/prophecy/shame, technical leakage, or role violation |

Flags should list exact strings and the checklist id (e.g. `N3`, `Rec4`).

---

## 11. Relationship to Pack 05 checklist

Pack 05 `19_NARRATIVE_QUALITY_CHECKLIST.md` remains the Narrative Engine architecture / writing-system gate (G/T/S/W/E ids).

This Release B checklist is the **commercial content review gate** for product quality after architecture freeze.

Use both when reviewing NarrativeResult prose. Use §8 alone for pure Portal chrome reviews.
