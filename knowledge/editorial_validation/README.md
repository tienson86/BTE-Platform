# Golden Dataset Editorial Validation V1

| Field | Value |
|-------|-------|
| Phase | Product validation |
| Status | Evidence collected — waiting for Product Owner review |
| Date | 2026-08-16 |
| Standard | BTE Editorial Standard v1.0 |
| Code changed | NONE |

This is a **product validation** folder.

It is not an architecture sprint, not an engine sprint, not a narrative rewrite, and not a new framework.

## Purpose

Evaluate real production PDFs across genuinely different BaZi charts and discover:

- where reports become repetitive
- where different charts collapse into the same story
- where customer relevance is weak
- where editorial rules fail
- where existing domain knowledge is insufficient
- what recurring product-level patterns should be fixed later

The central question:

> Does BTE produce a consultation for **this** person, or the same consultation with different BaZi tokens?

## What this phase does

1. Inventory real/bound charts already in the repository or supplied by Product Owner.
2. Generate current production PDFs **without changing code**.
3. Review the customer PDF (HTML sidecar used only as the same rendered customer artifact).
4. Score, compare, and aggregate findings.
5. **STOP.** Do not implement fixes.

## What this phase does not do

- Modify production code, engines, or Narrative Composer
- Create Story Engine / Story Seed Generator / new knowledge frameworks
- Fabricate birth data
- Repair defects while reviewing
- Start Luck Domain, Temperature Domain, or Case Identity Engine

## Dataset rule applied

| Available distinct real cases | Rule |
|-------------------------------|------|
| 10 named/bound charts with birth datetime and a generated production PDF | Provisional product conclusions allowed |
| 20 unnamed `validation/real_cases/case_01`–`case_20` inputs | **Not used** for editorial review (no customer identity; pipeline fixtures) |
| Pilot CASE-0008 / CASE-0009 | Unusable (no birth datetime) |
| Synthetic Readiness Subject | Excluded (explicitly synthetic) |

Target was 20–30 real charts. Fewer than 20 usable named cases exist. Every valid named case was used. No cases were invented.

## How to read this folder

| File | Role |
|------|------|
| `GOLDEN_DATASET_MANIFEST.json` | Case inventory, sources, PDF paths, live analytical truth |
| `COVERAGE_MATRIX.md` | Strength / pattern / Useful God / Day Master / gender / age / luck coverage |
| `EDITORIAL_VALIDATION_STATUS.md` | Phase status and stop condition |
| `GOOD_PATTERN_LIBRARY.md` | Consultant-grade lines that already work (evidence, not templates) |
| `CROSS_CASE_SIMILARITY.md` | Pairwise collapse vs legitimate similarity, including Sơn vs Tân |
| `GOLDEN_DATASET_EDITORIAL_VALIDATION_REPORT.md` | Dataset-level report (31 required sections) |
| `cases/EV-XXXX/` | Per-case review pack |
| `exports/` | Production PDFs + HTML sidecars generated for this phase |

## Per-case files

```text
cases/EV-XXXX/
  INPUT.md
  ANALYTICAL_TRUTH.md
  PRODUCT_REVIEW.md
  SCORECARD.json
  FINDINGS.md
  PDF.md                 # path to the customer PDF
```

Editorial IDs (`EV-0001` … `EV-0010`) are used because repository `CASE-0002` / `CASE-0003` collide across pilot, production, and validation folders.

## Review method

- Artifact reviewed: customer PDF (`exports/BTE_*_Production_E2E.pdf`).
- HTML sidecar is the same commercial report Playwright prints; it was used to quote exact customer text.
- JSON / engine internals were used only to record live analytical truth and to flag discrepancies. They were not the review object.

## Verdict (provisional)

See `GOLDEN_DATASET_EDITORIAL_VALIDATION_REPORT.md`.

**READY_FOR_PRODUCT_REPAIR_PLANNING** (provisional; n=10).

Wait for Product Owner review before any repair work.
