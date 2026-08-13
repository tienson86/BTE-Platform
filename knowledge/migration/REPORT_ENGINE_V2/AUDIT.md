# AUDIT — Legacy Report Engine (pre-migration)

Date: 2026-08-13

---

## Runtime that actually printed the customer PDF

Production already composed Identity / Career / Executive via CLL.

The PDF exporter **ignored** those features and rendered `ReportInputV1` through `report_sections_v1.py`.

```
ProductionEndToEndOrchestrator
  → build_report_input_v1 (engine dump)
  → _enrich_report_with_composition (domain dumps + features)
  → ReportExportServiceV1 / HtmlReportV1Renderer
  → build_presented_report()   ← 17 legacy sections
  → PDF
```

Identity / Career / Executive sections were attached to `ReportInputV1.interpretation.sections` but **never selected** by the presenter (it only looked for career / wealth / marriage / health / children aliases).

---

## Legacy customer sections (removed from customer PDF)

| # | Section | Type | Commercial value |
|---|---------|------|------------------|
| 01 | Thông tin lá số | Profile table | Cover only (name / date) |
| 02 | Tứ Trụ | Pillar cards + table | Engine dump |
| 03 | Ngũ hành | Score table | Engine dump |
| 04 | Thân vượng nhược | Scores + reasoning | Engine dump |
| 05 | Thập thần | Raw list | Engine dump |
| 06 | Mệnh cục / Cách cục | Pattern dump | Engine dump |
| 07 | Dụng thần – Hỷ – Kỵ | Rule dump | Engine dump |
| 08 | Thần sát | Evidence table | Engine dump |
| 09 | Đại vận | Cycle table + runtime gap note | Engine dump |
| 10 | Luận giải tổng thể | Stitched summary | Legacy filler |
| 11–15 | Nghề / Tài / Hôn / Sức / Tử tức | Domain placeholders | Empty / runtime gap |
| 16 | Khuyến nghị | List | Replaced by Executive priorities |
| 17 | Tổng kết | Placeholder | Replaced by Executive conclusion |

---

## Legacy templates still on disk (not used by customer PDF)

| Path | Role after V2 |
|------|----------------|
| `engines/report_engine/templates/v1/report_v1.html` | Shared HTML shell (CSS reused) |
| `engines/report_engine/templates/v1/report_v1.css` | Shared print CSS |
| `engines/report_engine/templates/default.md` | Legacy markdown |
| `engines/report_engine/rendering/report_sections_v1.py` | Legacy 17-section presenter — **compatibility only** |
| `engines/report_engine/report_builder.py` | Old scoring builder — unused by production PDF |
| `knowledge/report_templates/**` | Knowledge templates — not customer PDF |
| `knowledge/packages/report_presets/**` | Package presets — not customer PDF |

---

## Rule / engine dumps previously injected

From `_enrich_report_with_composition`:

- `Luận giải strength`
- `Luận giải ten_gods`
- `Luận giải pattern`
- `Luận giải useful_god`

From `ReportInputV1Adapter`:

- Strength scores, seasonal/root support, reasoning
- Useful god reasoning
- Pattern confidence / status
- Shen Sha evidence rows
- Five-element values
- Luck cycle diagnostics (`RUNTIME_GAP_MESSAGE`, `FULL_LUCK_CYCLES_GAP_NOTE`)

---

## Developer / template language found in the old customer path

Examples (must never appear in Customer PDF):

- “Áp dụng bảng trạng thái…”
- “Kích hoạt…”
- “Tính cách phản ánh…”
- Rule IDs / `matched_rules` / `reason_codes`
- `CAREER_REPORT_HIDDEN_BY_PRODUCT_CONTEXT` (marker, not consulting)
- “Chưa đủ dữ liệu để đưa ra kết luận.” as empty-domain filler
- Footer: `Report V1 · engine_version`

---

## Product features that were READY but not rendered

| Feature | Composer | Status before |
|---------|----------|---------------|
| Identity Report | `IdentityFeatureComposer` → CLL | Composed, not in PDF |
| Career Report | `CareerFeatureComposer` → CLL | Composed, not in PDF |
| Executive Consulting | `ExecutiveConsultingComposer` → CLL | Composed, not in PDF |
| Commercial Theme Library | `knowledge/commercial_theme_library/` | Catalog READY, **not wired** |
| Commercial Language Layer | `applications/production/language/` | Wired to composers, **not** to PDF |
| Product Context / Parent | `ContextDeliveryAdapter` | Live in customer payload, **not** in PDF |

---

## What was not audited for change

Calendar, BaZi, Strength, Pattern, Useful God, Ten Gods, Knowledge, Reasoning, CDR, CLL internals, Theme Library catalog files, Golden Dataset, Quality Gates, Product Context engine, Product Backlog.

END
