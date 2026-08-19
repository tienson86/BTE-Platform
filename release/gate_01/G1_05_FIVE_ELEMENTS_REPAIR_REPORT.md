# G1-05 — Five Elements Repair Report

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-05 Phase 2 |
| **Date** | 2026-08-19 |
| **Product decision** | Option A — V1.0 shows only **Phân bố Ngũ hành** |
| **Canonical production** | `RuleContextBuilder._build_wuxing` → `data.five_elements.counts` |
| **Customer model** | Structural occurrence (unweighted) |
| **Status** | FINAL FREEZE READY |

No Score Engine edit. No Strength / Temperature / Pattern / Ten Gods / Useful God formula change. No Deep Five Elements interpretation. Counting formula unchanged.

---

## 1. Semantic cũ và mới

| Surface | Trước | Sau (V1.0) |
|---------|--------|------------|
| Canonical Desktop S04 | **CÂN BẰNG NGŨ HÀNH** + Mạnh/Yếu từ % + `{max} vượng • {min} thiếu • Điểm {score.grade}` | **PHÂN BỐ NGŨ HÀNH** + count + provenance |
| S02 chip | `{topElement} nổi` (Thổ nổi trên CASE-0001) | `Mộc 4 · Hỏa 5 · Thổ 6 · Kim 3 · Thủy 1` |
| Portal Result card | `NGŨ HÀNH` + status Mạnh/Yếu copied from S04 | `PHÂN BỐ NGŨ HÀNH` + count; status only if count = 0 |
| Full Report | heading `Ngũ hành` | `Phân bố Ngũ hành` + provenance note |
| Report V1 HTML/PDF/DOCX | `03. Ngũ hành` / cột `Giá trị` | `03. Phân bố Ngũ hành` / cột `Số đơn vị` + notes |
| Score `wuxing_score` | Mixed into S04 as grade; executive bar labeled `Ngũ hành` | Not bound to distribution. Executive bar labeled **Điểm module Ngũ hành** |

Official V1.0 name: **Phân bố Ngũ hành** (Structural Five Elements Distribution).

Not shown in V1.0 as separate widgets: sức mạnh ngũ hành, cân bằng, vượng/suy, hành thiếu, weighted element strength.

---

## 2. Canonical counting model

Unchanged. Owner:

```text
BaziEngine.pillars + hidden_stems
    → RuleContextBuilder._build_wuxing
    → rule_context["wuxing"]["counts"]
    → build_five_elements_payload
    → data.five_elements.counts
```

Model C (every contribution = +1):

- each Thiên can → +1 to its element
- each Địa chi → +1 to **bản hành of the chi**
- each Tàng can **occurrence** → +1 (duplicates count twice; no main/middle/residual weight)

Not in this count: mùa, nguyệt lệnh, đắc lệnh, thông căn, mạnh/yếu, sinh khắc, Temperature, Strength, Useful God, weighted power.

`FiveElementCalculator` (hidden 0.5) remains unused on the Orchestrator path.

Published extras (not a new count): `method_note`, `unit_total`, `count_model`.

---

## 3. CASE-0001 reconstruction

Chart: Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần.

| Source | Units |
|--------|--------|
| Visible stems | Bính→Hỏa, Tân→Kim, Canh→Kim, Mậu→Thổ |
| Branch bản hành | Dần→Mộc, Sửu→Thổ, Ngọ→Hỏa, Dần→Mộc |
| Hidden | Dần: Giáp Mộc, Bính Hỏa, Mậu Thổ; Sửu: Kỷ Thổ, Quý Thủy, Tân Kim; Ngọ: Đinh Hỏa, Kỷ Thổ; Dần: Giáp Mộc, Bính Hỏa, Mậu Thổ |

Hidden list (11): Giáp, Bính, Mậu, Kỷ, Quý, Tân, Đinh, Kỷ, Giáp, Bính, Mậu.

| Hành | Count |
|------|-------|
| Mộc | 4 |
| Hỏa | 5 |
| Thổ | 6 |
| Kim | 3 |
| Thủy | 1 |
| **Total** | **19** = 4 stems + 4 branch elements + 11 hidden |

---

## 4. UI labels removed

Removed from the distribution widget (inferred from count / % only):

- Mạnh / Rất mạnh / Yếu / Rất yếu / Trung bình (as element strength)
- Vượng / Suy / Thiếu / Dư
- `{hành} nổi` / hành trội / hành yếu nhất
- Score grade on S04 (`Điểm B+` style)

Count = 0 may only show: **Không xuất hiện trong phân bố cấu trúc**.

Not replaced with another narrative.

---

## 5. `wuxing_score` separation

`score.wuxing_score` remains Score Engine quality (CASE-0001 live = **0.0**).

It is not:

- a bar on Phân bố Ngũ hành
- a reason to treat counts as wrong or unbalanced
- mixed into `data.five_elements.counts`

Desktop and Report V1 no longer fall back to `score.wuxing_series` when `five_elements` is present or missing. Report shows the runtime gap if counts are unpublished.

Legacy executive summary still shows the Score module scalar under **Điểm module Ngũ hành**, not as the customer distribution.

---

## 6. Score grade handling

S04 previously appended `Điểm {score.grade}`. That grade belongs to Score Engine.

Repair: **removed from S04**. Grade remains in Technical Info as `score_grade` / Điểm tổng, separate from Phân bố Ngũ hành. No new distribution grade was invented.

---

## 7. Analytical 15-tally separation

| Counter | Formula | CASE-0001 total | Audience |
|---------|---------|-----------------|----------|
| Customer Phân bố Ngũ hành | stems + branch bản hành + hidden occurrences | **19** | Desktop / Portal / Report / PDF / DOCX |
| Pattern / Useful God `element_distribution` | visible stems + hidden occurrences | **15** | Internal engines |
| Strength `element_distribution` | stems + hidden keyed by unique branch (duplicate Dần once) | **12** | Internal Strength only |

V1.0 must not expose the 15-tally (or Strength’s 12) under the customer label Phân bố Ngũ hành. The two (three) totals serve different purposes and are not interchangeable. G1-05 did not change the 15-tally.

---

## 8. Cross-surface result

CASE-0001 customer fact, same numbers, no renderer recount:

`Mộc 4 · Hỏa 5 · Thổ 6 · Kim 3 · Thủy 1`

| Surface | Source |
|---------|--------|
| Canonical Desktop S04 / S02 | `data.five_elements.counts` |
| Portal Result card | same ViewModel rows |
| Full Report HTML | `analyticalFiveElementCounts` |
| Report V1 HTML / PDF / DOCX | `ReportInputV1.five_elements` from `five_elements.analytical_counts` |

Provenance on live cards / report notes:

`Tính theo Thiên can · bản hành Địa chi · Tàng can`

`Tổng đơn vị cấu trúc: 19`

---

## 9. Tests

Added / kept:

- `tests/five_elements/test_g1_05_five_elements_binding.py`
- `tests/report_engine/test_g1_05_five_elements_binding.py`
- `applications/customer_portal/tests/js/g1_05_five_elements_binding.test.ts`

Coverage: CASE-0001 4/5/6/3/1; total 19; duplicate Dần deterministic; repeated hidden per occurrence; count = 0 absence; Portal/Report same counts; `wuxing_score` does not override; Score grade not on S04; renderer does not emit Mạnh/Yếu/Vượng/Thiếu from count; Strength/Pattern/Temperature/Ten Gods/Useful God unchanged on CASE-0001.

Module runs: 17 pytest (G1-05 + HTML headings) passed. Portal G1-05 + related canonical tests passed.

---

## 10. Remaining V1.1 backlog

- Separate widgets for ngũ hành strength / balance / vượng-suy / hành thiếu / weighted power.
- Deep Five Elements interpretation (do not add in V1.0).
- G1-06 Useful God still reads the internal 15-tally (`flo_*` “Mộc quá thịnh”). Do not treat that as customer Phân bố.
- Interpretation pack04 still has a Score-oriented sentence “Cân bằng Ngũ hành đạt điểm {five_elements_score}” — Score narrative, not this widget. Not edited in G1-05.
- RuleContext still stores internal `STRONG` / `MISSING` / `EXCESS` on counts; customer UI no longer displays them.
- Legacy `static/js/report/report_model.js` can still prefer `wuxing_series` on the old JS report path; Canonical V1 uses Report Engine + Full Report ViewModel.
- BaZi adapter keeps `wuxing_series` only when `five_elements` is absent (old fixtures). Live analyze always publishes `five_elements`.

Stop: do not start G1-06. Do not edit Useful God selection.

G1-05 STATUS: FINAL FREEZE READY
