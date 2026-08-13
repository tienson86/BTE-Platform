# PIPELINE MAPPING — Legacy → Product Pipeline V2

Date: 2026-08-13

---

## Before (what the PDF actually did)

```
Calendar / BaZi / Strength / Pattern / Useful God / Ten Gods
        ↓
Interpretation V1 (legacy) + domain composers
        ↓
ReportInputV1Adapter          ← engine dump
        ↓
enrich: domain dumps + unused feature sections
        ↓
HtmlReportV1 / report_sections_v1   ← 17 legacy templates
        ↓
PDF
```

---

## After (customer PDF)

```
Truth Layer (engines, unchanged)
        ↓
Domain composers (unchanged)
        ↓
Cross-Domain Reasoning
        ↓
ExecutiveClaimPlan
        ↓
Commercial Theme Library hook   ← NEW runtime select
        ↓
Commercial Language Layer       ← Identity / Career / Executive
        ↓
Product Context delivery        ← parent / hide career
        ↓
Commercial Report Builder       ← Cover → Identity → Career → Executive
        ↓
Leak filter (customer only)
        ↓
Commercial HTML → PDF
```

Advisor Mode adds Appendix after Executive. Customer Mode never does.

---

## Stage names (production)

| Stage | Role |
|-------|------|
| calendar … ten_gods | Truth (unchanged) |
| interpretation_* | Domain composition (unchanged) |
| cross_domain_reasoning | CDR (unchanged) |
| identity_report / career_report / executive_consulting | Features via CLL (unchanged) |
| product_context / context_delivery | Audience (unchanged) |
| report_input_v1 | Diagnostics only — **not** customer body |
| commercial_theme_library | Runtime theme select |
| commercial_language | Confirm CLL features are the body source |
| commercial_report_builder | Compose customer document |
| pdf_export | Commercial PDF |

---

## Theme Library hook

| CDR / capacity signal | Library theme |
|-----------------------|---------------|
| `OPERATING_OUTPUT` | operating: Người ra kết quả |
| `OPERATING_SELF_CARRY` | operating: Người tự gánh |
| `OPERATING_STANDARDS` | operating: Người giữ chuẩn |
| `BALANCE_DIRECTION` | operating: Người điều tiết |
| `FOLLOW_STRUCTURE` | overlay: FOLLOW_FRAME |
| weak / `CAPACITY_WEAK` | overlay: CONSERVING |
| published conflicts | overlay: TENSION_HOLDER |

Variant: `formal` default; `premium` for Package C/D; `short` for Package A.

Cover prints the **customer name** of the operating theme (Vietnamese). Parent Context omits adult class on cover.

---

## Language Layer

CLL is not rewritten. Composers already call:

- `CommercialLanguageService.compose_identity`
- `CommercialLanguageService.compose_career`
- `CommercialLanguageService.compose_executive`

V2 **wires that output into the PDF**. Previously it stopped at `CustomerDeliverable` JSON.

---

## Compatibility

| Consumer | Path |
|----------|------|
| Customer / production PDF | Commercial V2 |
| `tests/report_engine` ReportInputV1 HTML/PDF | Legacy presenter (unchanged) |
| Advisor PDF | Commercial V2 + appendix |

END
