# G1-PREFINAL — Freeze manifest

**Status:** G1-PREFINAL complete. Do not start G1-FINAL from this document automatically.

**Date:** 2026-08-20

---

## Canonical modules (Frozen — not retuned this phase)

| Domain | Canonical module / SSOT |
|--------|-------------------------|
| Calendar month pillar | Lunar month + Ngũ Hổ Độn (`BTE-MONTH-PILLAR-LUNAR-V1.0`); Solar Terms for season/climate/Luck timing |
| Ten Gods | Day stem = Nhật Chủ; same stem elsewhere = Tỷ Kiên; hidden preserved |
| Strength | `strength.strength_score`; 3 classes weak / balanced / strong |
| Pattern | Month branch → main qi → Ten God; no silent complete-chart fallback |
| Temperature | Climate state + imbalance score; Điều hậu ≠ Overall |
| Five Elements | Structural distribution; customer “Phân bố Ngũ hành” |
| Useful God Overall | Strength / valid follow / flow; climate does not dominate |
| Special Pattern | LEVEL-1 may detect; may not override Overall |
| Follow Pattern | Weak-follow requires weak; canonical tokens |
| Customer Hỷ/Kỵ | HK-R1H; Kỵ V1.0 values; Điều hậu separate |
| Luck | Existing LuckEngine sequence; no algorithm change |

---

## Frozen rule / contract versions

| Item | Version |
|------|---------|
| Customer Useful God view | `analysis_result.UsefulGodView@1.5` |
| ReportInputV1 | `1.0` |
| AnalysisResult envelope | `1.0` |
| Database / rule CSVs | Unchanged this phase (V1.0 freeze) |

---

## Golden dataset

| Item | Value |
|------|-------|
| 101-case freeze dump | `release/gate_01/G1_PREFINAL_101_TRUTH.json` |
| SHA256 | `46386BC955119F5DFE9482E7D620767BFB8BB74003A0968A17A6F82017FFA5CC` |
| Report CASE-0001 expected | `tests/golden_dataset/report_v1/CASE-0001/expected_report_input.json` (recomputed) |
| Interpretation expected | `tests/golden_dataset/expected/case_0001.json` (unchanged; still matches runner) |

---

## Frontend bundle

| Item | Value |
|------|-------|
| Command | `npm run build:result` in `applications/customer_portal` |
| Artifact | `applications/customer_portal/static/dist/result.js` |
| Built | 2026-08-20 21:11:28 (local) |
| SHA256 | `DE5BA4972962ACF38B5B19DD15D53BBB5D83E3CDCA726C191352E4827D0C134C` |
| Also | `static/dist/result.css`, `static/dist/chunks/fullReportViewModel-obzyoA5U.js` |

---

## Backend commit / hash

| Item | Value |
|------|-------|
| Branch | `release/v1.0-final` |
| HEAD at start of freeze docs | `ed6dba05fd7683ed686c1d0035767ede6b5532f3` |
| HEAD message | Refine UsefulGod HY classification and wording |
| This phase | Uncommitted test/Golden/presentation-copy + freeze docs (not a new engine commit) |

---

## Test status

| Suite | Result |
|-------|--------|
| Python Gate-1 (`tests` + applications tests, 6 legacy collectors ignored) | **1806 passed**, 2 documented D |
| Portal Vitest | **254 passed / 0 failed / 0 skipped** (39 files) |
| Export HTML/PDF/DOCX (4 control cases) | PASS |

---

## Control-case truth table

See `release/gate_01/G1_PREFINAL_CONTROL_CASES.md`.

---

## Known V1.1 limitations (not fixed)

**Strength:** deeper root quality; hidden control weighting; advanced model reconciliation.

**Useful God:** strong→Hao/Tài; strong+Thất Sát→Chế; Pattern-main reconciliation; Flow competitiveness; Tiết vs Chế; absent-element candidate theory.

**Special Pattern:** deep qualification; phá cách / tạp khí; visible Wealth/Officer break; element-specific chuyên.

**Hỷ/Kỵ:** independently derived Hỷ; whole-chart Kỵ; excess/pressure reconciliation; competing-candidate confidence.
