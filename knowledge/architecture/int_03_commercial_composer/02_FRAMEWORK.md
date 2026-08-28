# 02 — Commercial Framework

| Field | Value |
|-------|--------|
| Document | INT-03A Commercial Framework |
| Version | 1.0.0 |
| Status | Canonical for INT-03A |

---

## 1. Seven required sections

Every Commercial Narrative Unit contains exactly these sections, in this order:

| Order | Slot | Section id | Vietnamese title | English title |
|-------|------|------------|------------------|---------------|
| 1 | `executive_summary` | `sec-commercial-executive` | Tổng quan | Executive Summary |
| 2 | `overall_reading` | `sec-commercial-reading` | Luận giải tổng thể | Overall Reading |
| 3 | `current_situation` | `sec-commercial-situation` | Hiện trạng | Current Situation |
| 4 | `strengths` | `sec-commercial-strengths` | Điểm mạnh | Main Strengths |
| 5 | `risks` | `sec-commercial-risks` | Rủi ro chính | Main Risks |
| 6 | `key_recommendation` | `sec-commercial-recommendation` | Khuyến nghị trọng tâm | Key Recommendation |
| 7 | `conclusion` | `sec-commercial-conclusion` | Kết luận | Conclusion |

No commercial unit may omit a section.

A section with no publishable Integrated sentence uses `Chưa có dữ liệu`.

---

## 2. Section meaning

| Section | Speaks | Must not |
|---------|--------|----------|
| Executive Summary | Lead published facts from Integrated executive summary | Invent a consulting persona or career thesis |
| Overall Reading | Chart-level Integrated summary | Add a second wrap that Integrated did not publish |
| Current Situation | What Integrated observed | Explain, advise, or predict |
| Main Strengths | Published constructive impact | Rank, score, or invent advantages |
| Main Risks | Published restraint / negative Integrated lines | Forecast misfortune or invent warnings |
| Key Recommendation | Published Integrated recommendation | Invent actions or domain advice |
| Conclusion | Settled restatement of published summary + recommendation | Open a new topic |

---

## 3. Source map (structural)

| Commercial section | Integrated blocks |
|--------------------|-------------------|
| Executive Summary | `executive_summary` |
| Overall Reading | `summary` |
| Current Situation | `observation` |
| Main Strengths | `impact` |
| Main Risks | `reasoning` and `recommendation`, only sentences whose Integrated `source_path` already marks restraint (`negative`, `unfavorable`) |
| Key Recommendation | `recommendation` |
| Conclusion | first published sentence of `summary`, then first published sentence of `recommendation` |

This map is composition, not calculation.

Selecting restraint paths is not a new classification. Those paths were already published by Integrated Narrative.

---

## 4. Voice

Brand Language: consultant, not calculator.

INT-03A runtime copies Integrated wording. Later sprints may rewrite or simplify **the same sentences** through a sentence library. They may not add facts.

---

## 5. Insufficient data

`Chưa có dữ liệu`

Do not use `N/A`, `null`, `Không`, or `Chờ dữ liệu`.

---

END
