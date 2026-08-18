# B1_P0_003_TEN_GODS_PROFESSIONAL_WRITING_REPORT

| Field | Value |
|-------|-------|
| Issue | B1-P0-003 Professional Writing — Ten Gods Domain |
| Date | 2026-08-18 |
| Type | PRODUCT QUALITY |
| Severity | P0 |
| Engine changes | **NONE** |
| Architecture changes | **NONE** |
| Knowledge changes | **NONE** |

---

## 1. Status

**COMPLETE — READY_FOR_ARTIFACT_REVIEW**

The Professional Ten Gods chapter is now a chart-specific consultation.

It no longer publishes Knowledge cards, Useful God glossary lines, or the Ten Gods catalogue.

Every important natal Ten God is written from the chart: where it sits, how it lives with Pattern / Strength / Useful God / current Da Yun, then opportunity, risk, and one practical implication.

Three Professional PDFs were generated.

Product check: **PASS**.

---

## 2. Writing principles applied

| Principle | How it was applied |
|-----------|--------------------|
| Begin from the chart, not the definition | Every chapter opens with `Trong lá số này`. Role slots open with `{God} đang đóng vai trò… vì đang {lộ/tàng} ở {trụ}` |
| Answer why this Ten God matters here | Only Pattern, Useful God seating, and the strongest visible natal roles are kept. Cap: 3. Nhật Chủ is not treated as a Ten God chapter |
| Influence on this customer | Strength, lộ/tàng, lệnh tháng, and current Da Yun are bound into slot 2 |
| Cooperate / conflict with Pattern, Strength, Useful God, current direction | Slot 3 binds Pattern and Useful God seating. Overview names Da Yun ten-god. Risk names Kỵ only when this role or its sitting stem is already listed as Kỵ |
| Never isolated encyclopedia | Dictionary openings (`{God} là quan hệ nhật chủ…`, `Là Dụng thần:`) are rejected. Unused gods are not printed |
| Do not repeat the same explanation | Slot templates are shared. Seating, Pattern, Useful God, Kỵ touch, and Da Yun differ by chart, so the consultation meaning differs |
| Knowledge ownership | Knowledge JSON is not rewritten. Copy reads `title` channel, `positive_meaning`, `negative_meaning`, recommendations, and warnings |
| No new analytical truth | Positions, distribution, Pattern, Strength, Useful God, Hỷ/Kỵ, and Da Yun ten-god are stamped from production facts |

Required structure for each important Ten God:

1. Role in this chart
2. Current influence
3. Contribution to the overall structure
4. Opportunity
5. Risk
6. Practical implication

---

## 3. Three-case comparison

The three chapters share a slot shape. They do not share a consultation.

| | Nguyễn Tiến Sơn | Lương Ngọc Huỳnh | Ngô Đặng Minh Tân |
|--|-----------------|------------------|-------------------|
| Nhật chủ | Canh (Kim) | Bính (Hỏa) | Bính (Hỏa) |
| Cục | Chính Ấn | Chính Tài | Chính Ấn |
| Thân | vượng | vượng | trung hòa |
| Dụng | Thực Thần — **chưa ngồi trên trụ** | Đinh — **ngồi dưới nhãn Kiếp Tài** | Canh — **chưa ngồi trên trụ** |
| Đại vận | Ất Tỵ 2022–2031 · Chính Tài | Quý Mão 2021–2030 · Chính Quan | Đinh Tỵ 2024–2033 · Kiếp Tài |
| Important Ten Gods | Chính Ấn · Thất Sát · Thiên Ấn | Chính Tài · Kiếp Tài · Thiên Tài | Chính Ấn · Thực Thần · Chính Tài |
| Why these | Hidden month Pattern; year Thất Sát; hour Thiên Ấn | Hidden month Pattern; month Kiếp Tài is the Useful stem; hour Thiên Tài | Visible month Pattern; year Thực Thần; hour Chính Tài |
| Chart-specific conflict | Dụng Thực Thần absent while Ấn is the seated structure | Cục Chính Tài tàng by Tân, and Tân is Kỵ; hour Thiên Tài sits on Canh, also Kỵ | Cục Chính Ấn lộ by Ất at month command, and Ất is Kỵ |
| Paragraphs | 19 | 19 | 19 |
| PDF | 12 pages | 12 pages | 11 pages |

Sơn and Tân both have cục Chính Ấn. They do not share a chapter:

- Sơn: Ấn is **tàng** at month, body is **vượng**, Dụng is the **absent** role Thực Thần, living decade is Chính Tài.
- Tân: Ấn is **lộ** at month on **Ất / Kỵ**, body is **trung hòa**, Dụng is the **absent** stem Canh, living decade is Kiếp Tài, and Thực Thần is actually seated.

Huỳnh and Tân both mention Chính Tài. They do not share a meaning:

- Huỳnh: Chính Tài **is the Pattern**, hidden in Dậu, and its sitting stem Tân is Kỵ.
- Tân: Chính Tài is the **hour visible** channel beside cục Chính Ấn, not the Pattern.

---

## 4. Before / After chapter comparison

### Before

Professional `sec-ten_gods` harvested existing evidence with role-why markers. Live PDFs therefore mixed:

- dictionary Knowledge: `{God} là quan hệ nhật chủ…`
- Useful God cards: `Là Dụng thần:…` / `Là Kỵ thần hoặc dùng quá mức:…`

| Chart | Before | Problem |
|-------|--------|---------|
| Sơn | 3 paragraphs, mostly Kỵ/Dụng cards | Did not seat Thất Sát / Thiên Ấn / hidden Chính Ấn. Did not say Thực Thần is selected but absent |
| Huỳnh | 6 paragraphs, dictionary Chính Tài + Thiên Tài + Dụng Đinh cards | Taught Thiên Tài/Chính Tài as definitions. Did not say Đinh sits as Kiếp Tài, or that Tân/Canh of the seated channels are Kỵ |
| Tân | 5 paragraphs, dictionary Chính Tài + Dụng Canh / Kỵ Giáp·Ất cards | Taught Chính Tài as a glossary entry. Did not consult visible month Chính Ấn or year Thực Thần |

The same Chính Tài dictionary paragraph appeared on Huỳnh and Tân.

### After

One overview from this chart, then six consultation slots per important natal Ten God.

Rejected:

- `{God} là quan hệ nhật chủ`
- `Là Dụng thần:` / `Là Hỷ thần:` / `Là Kỵ thần hoặc`
- Nhật Chủ as a Ten God lesson
- the ten-god catalogue

Kept:

- every selected seating (pillar, stem, lộ/tàng)
- Pattern, Strength, Useful God, Hỷ/Kỵ
- current Da Yun identity already published
- Knowledge opportunity / risk / action fields, rewritten into consultant voice

---

## 5. Professional PDF artifacts

`knowledge/editorial_validation/exports/b1_p0_003_ten_gods/professional/`

| Chart | HTML | PDF | Pages |
|-------|------|-----|------:|
| Nguyễn Tiến Sơn | `BTE_CASE-0001_Production_E2E.html` | `BTE_CASE-0001_Production_E2E.pdf` | 12 |
| Lương Ngọc Huỳnh | `BTE_HUYNH_Production_E2E.html` | `BTE_HUYNH_Production_E2E.pdf` | 12 |
| Ngô Đặng Minh Tân | `BTE_TAN_Production_E2E.html` | `BTE_TAN_Production_E2E.pdf` | 11 |

Product metrics: `knowledge/editorial_validation/exports/b1_p0_003_ten_gods/_metrics.json`

Product check: `knowledge/editorial_validation/b1_p0_003_ten_gods_writing_product_test.py` → **pass: true**

---

## 6. Files changed

| File | Change |
|------|--------|
| `engines/interpretation_engine/foundation/narrative/publish/ten_gods_copy.py` | **New.** Stamp chart facts. Assemble Professional Ten Gods consultation copy. Does not calculate Ten Gods |
| `engines/interpretation_engine/foundation/narrative/publish/professional.py` | Page 4 uses assembled consultation instead of Knowledge/Useful God evidence harvest |
| `engines/interpretation_engine/foundation/narrative/publish/editions.py` | `sec-ten_gods` limit 6 → 20 so three roles × six slots + overview can publish |
| `applications/api/services/narrative_result_truth.py` | Stamp `ten_gods_consultation` onto narrative metadata. Same choke point as luck/interaction stamps |
| `knowledge/editorial_validation/b1_p0_003_ten_gods_writing_product_test.py` | **New.** Three-case writing gate |
| `knowledge/editorial_validation/exports/b1_p0_003_ten_gods/` | Professional HTML/PDF artifacts |

---

## 7. Engine changes

**NONE**

TenGodsEngine, Useful God selection, Pattern, Strength, and luck calculation are untouched.

---

## 8. Architecture changes

**NONE**

No new Narrative framework. No new composer. No Publisher redesign.

Publication copy for Professional page 4 follows the existing Luck Analysis copy pattern: stamp facts → write customer sentences → select the page.

```
TenGodsEngine / Pattern / Strength / UsefulGod / Luck facts
        ↓
stamp_ten_gods_consultation   (metadata only)
        ↓
assemble_ten_gods_consultation  (Professional writing)
        ↓
sec-ten_gods
```

Executive edition is unchanged.

---

## 9. Knowledge changes

**NONE**

`knowledge/interpretation/domains/ten_gods/*.json` is not edited.

The copy layer reads already-approved fields (`title` channel, positive/negative meaning, recommendations, warnings). It does not rewrite the glossary.

---

## 10. Final verdict

**READY_FOR_ARTIFACT_REVIEW**

A customer reading only the Ten Gods chapter can see:

- which Ten Gods were chosen and why they matter on **this** chart
- how they sit with Pattern, Strength, Useful God, and the living decade
- what to use and what to watch

without reading the rest of the report.

STOP.
