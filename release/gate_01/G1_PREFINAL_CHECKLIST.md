# G1-PREFINAL — Checklist

**Date:** 2026-08-20

- [x] Frozen Truth baseline treated as canonical (G1-01 … HK-R1H, CAL-P0B)
- [x] No Strength / Pattern / UG winner / Dụng-Hỷ-Kỵ semantics / Temperature / Five Elements / Ten Gods / ShenSha / Luck / Month Pillar SSOT retune
- [x] Stale `tests/useful_god` (+ report / production / interpretation / Portal) expectations updated
- [x] Contract matrix: live `@1.5`; `@1.2` tests removed; launch fixtures `@1.0` marked synthetic
- [x] Golden inventory listed; only locked files migrated
- [x] CASE-0001 ReportInput Golden recomputed from production
- [x] 101-case freeze dump from production (`G1_PREFINAL_101_TRUTH.json`)
- [x] CAL-P0B 22/22 month pillars match live dump
- [x] Useful God dump: climate ≠ Overall; LEVEL-1 override=0; 4 follow `spc_*`; HK-R1H Hỷ 85/16
- [x] Pattern dump distinguishes detection vs override
- [x] Customer presentation Golden/tests lock Dụng, căn cứ, Hỷ, Kỵ, Điều hậu; no rule IDs; no Dụng duplicate under Hỷ
- [x] 10 control cases recomputed (human table)
- [x] Fresh Analyze (TestClient) agrees with Frozen Sơn
- [x] Portal rebuilt (`build:result`)
- [x] Full Python Gate-1 suite: 1806 passed; 2 D documented
- [x] Full Portal suite: 254 passed
- [x] HTML/PDF/DOCX for Sơn, Tuyền, Dũng, Trường
- [x] API contract: internal `canonical_favorable_display` ≠ customer `favorable_display`
- [x] Golden change report with cause breakdown
- [x] V1.1 backlog carried forward
- [x] Acceptance items 1–10
- [x] G1-FINAL **not** started

## Acceptance vs result

| # | Requirement | Result |
|---|-------------|--------|
| 1 | Full Python green **or** documented D | **1806 passed**; D = knowledge_canon + 6 legacy collectors |
| 2 | Full Portal green | 254/254 |
| 3 | No stale customer contract assertions | `@1.5`; Hỷ customer vs internal split |
| 4 | Golden synchronized | CASE-0001 ReportInput + 101 dump |
| 5 | 10 control cases | `G1_PREFINAL_CONTROL_CASES.md` |
| 6 | API/Result/Report/PDF/DOCX agree | TestClient + export smoke |
| 7 | No stale runtime | New app process; new bundle |
| 8 | No algorithm change | Presentation `quy tắc` wording only |
| 9 | V1.1 backlog preserved | Manifest § limitations |
| 10 | No unresolved canonical mismatch | None in Gate-1 suite |

## Remaining D (approved non-blocking)

1. `tests/knowledge/test_indexes_cli.py::test_cli_real_scaffold`
2. `tests/knowledge/test_validators.py::test_real_scaffold_foundation`
3. Collection: `tests/test_builder.py`, `test_pipeline.py`, `test_rule_loader.py`, `test_rule_matcher.py`, `test_rule_scoring.py`, `test_sentence_generator.py`
