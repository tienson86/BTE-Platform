# ISSUE_B1_P0_001_REPORT

| Field | Value |
|-------|-------|
| Issue | B1-P0-001 Current Da Yun Interpretation |
| Date | 2026-08-17 |
| Edition | Professional |
| Luck Domain | **Not built** |

---

## 1. Status

**COMPLETE — ready for Product Review.**

Professional Report now has a Current Da Yun consultation assembled from existing natal narrative and already-copied cycle labels.

No Luck Domain.
No ten-cycle calculation.
No Luck Engine redesign.
No new analytical truth.

---

## 2. Root cause

The Professional `sec-luck` page only harvested sentences that named the cycle:

- `Khung thời gian của bản luận là Đại vận {label}.`
- `Đại vận hiện tại: {label}.`

Those lines were copied as a **time frame**, by design, when Luck Domain was refused. `_select_luck` then published the name, plus any warning that happened to contain “vượng / thoát / tải”.

PUBLISH01 Professional PDFs therefore had a luck page of **3 paragraphs** that did not answer why this decade matters, what to emphasize, or what to avoid.

---

## 3. Current Da Yun section

Professional page **Đại vận hiện tại** now has seven paragraphs:

1. Current decade (named)
2. Why this decade matters (existing case thesis)
3. Interaction with the natal chart (Pattern, Strength, Dụng, Hỷ, Kỵ — already on the chart)
4. Main opportunity (existing career implication)
5. Main risk (existing thesis risk)
6. Recommended operating direction (existing corrective + career implication)
7. Next Da Yun, briefly (already-computed next label only)

The page does not explain Da Yun theory.
It does not list all ten cycles.
It does not interpret the luck pillar’s elements as a new calculation.

---

## 4. Three case comparison

| | Sơn | Huỳnh | Tân |
|--|-----|-------|-----|
| Current | Ất Tỵ 2022–2031 | Quý Mão 2021–2030 | Đinh Tỵ 2024–2033 |
| Next (copied) | Bính Ngọ 2032–2041 | Giáp Thìn 2031–2040 | Mậu Ngọ 2034–2043 |
| Person | Người tự gánh | Người kiến tạo | Người chỉnh trục |
| Chart | Chính Ấn · Thân vượng · Thực Thần | Chính Tài · Thân vượng · Đinh | Chính Ấn · Trung hòa · Canh |
| Opportunity | Finish visible work; do not add load | Refine at the heat point; do not freeze-cut | Cut surplus; install usable discipline |
| Luck words | 328 | 301 | 326 |
| Identical luck paragraphs | none across pairs | | |
| Token overlap | Sơn–Huỳnh 0.56 · Sơn–Tân 0.55 · Huỳnh–Tân 0.55 | | |

The three sections share a **slot shape**. They do not share a consultation.

---

## 5. Professional PDF before

`knowledge/editorial_validation/exports/publish01/professional/`

| Chart | sec-luck paragraphs | Content |
|-------|--------------------:|---------|
| Sơn | 3 | Cycle name / frame |
| Huỳnh | 3 | Cycle name / frame |
| Tân | 3 | Cycle name / frame |

Cover already showed the current label. The luck **chapter** did not consult.

---

## 6. Professional PDF after

`knowledge/editorial_validation/exports/b1_p0_001/professional/`

| Chart | Pages | sec-luck | PDF |
|-------|------:|---------:|-----|
| Nguyễn Tiến Sơn | 11 | 7 | `BTE_CASE-0001_Production_E2E.pdf` |
| Lương Ngọc Huỳnh | 11 | 7 | `BTE_HUYNH_Production_E2E.pdf` |
| Ngô Đặng Minh Tân | 11 | 7 | `BTE_TAN_Production_E2E.pdf` |

Metrics: `knowledge/editorial_validation/exports/b1_p0_001/_metrics.json`

---

## 7. Acceptance

| Gate | Result |
|------|--------|
| Only Da Yun name shown | Rejected — 7 consulting paragraphs |
| Generic wording as the whole page | Rejected — thesis/career/risk are case-true |
| Same paragraph reused | None identical across the three charts |
| Prediction without evidence | None invented; no luck-pillar five-element math |
| Glossary dump | None |
| Customer can see why the decade matters | Yes — named decade + thesis |
| What to emphasize / avoid | Yes — opportunity and risk |
| Connection to natal chart | Yes — Pattern, Strength, Dụng, Hỷ, Kỵ |

Product test `b1_p0_001_product_test.py`: **pass**.

This is **not** Luck Domain interpretation of the decade’s own stems/branches.
It is the natal consultation applied to the living decade.

---

## 8. Files changed

- `engines/interpretation_engine/foundation/narrative/publish/current_dayun.py` — assemble Professional luck page
- `engines/interpretation_engine/foundation/narrative/publish/professional.py` — use assembler
- `engines/interpretation_engine/foundation/narrative/publish/editions.py` — luck page limit 7
- `engines/interpretation_engine/foundation/narrative/production.py` — copy next cycle label
- `engines/interpretation_engine/foundation/narrative/adapters.py` — ChartFocus.next_dayun
- `engines/interpretation_engine/foundation/narrative/input.py` — ChartFocus.next_dayun
- `applications/api/services/narrative_result_truth.py` — stamp luck_frame
- `knowledge/editorial_validation/b1_p0_001_product_test.py`
- `knowledge/editorial_validation/exports/b1_p0_001/`
- `knowledge/editorial_validation/ISSUE_B1_P0_001_REPORT.md`

---

## 9. Engine changes

**NONE**

Calendar, BaZi, Strength, Pattern, Useful God, Luck Engine, Ten Gods, Shen Sha were not modified.

---

## 10. Architecture changes

**NONE**

No Luck Domain.
No new engine.
No new publisher.
No new composer.

---

## 11. Tests

`pytest tests/interpretation_engine/narrative tests/report_engine/test_narrative_canonical_binding.py -q`

**72 passed.** Tests were not modified.

---

## 12. Final verdict

**READY_FOR_PRODUCT_REVIEW**

STOP.

Do not implement Luck Domain.
