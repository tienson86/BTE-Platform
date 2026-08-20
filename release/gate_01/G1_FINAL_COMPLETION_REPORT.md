# G1-FINAL — Completion report

**Date:** 2026-08-20  
**Final status:** G1-FINAL: PASS — BTE V1.0 GATE 1 CORE ENGINE FROZEN

G1-FINAL was a freeze/release documentation phase. No Calendar, BaZi, Ten Gods, Strength, Pattern, Temperature, Five Elements, Useful God, Dụng/Hỷ/Kỵ, ShenSha, Luck, Score, rule-priority, or knowledge-rule code was modified.

---

## 1. Freeze input verification

All six G1-PREFINAL artifacts present:

- `G1_PREFINAL_CONTRACT_CLEANUP_REPORT.md`
- `G1_PREFINAL_GOLDEN_MIGRATION_REPORT.md`
- `G1_PREFINAL_FULL_REGRESSION_REPORT.md`
- `G1_PREFINAL_CONTROL_CASES.md`
- `G1_PREFINAL_FREEZE_MANIFEST.md`
- `G1_PREFINAL_CHECKLIST.md`

Truth dump and Portal bundle hashes **match** the expected values. Files were **not** regenerated.

| Artifact | Expected SHA256 | Observed |
|----------|-----------------|----------|
| `G1_PREFINAL_101_TRUTH.json` | `46386BC955119F5DFE9482E7D620767BFB8BB74003A0968A17A6F82017FFA5CC` | match |
| `static/dist/result.js` | `DE5BA4972962ACF38B5B19DD15D53BBB5D83E3CDCA726C191352E4827D0C134C` | match |

HEAD: `ed6dba05fd7683ed686c1d0035767ede6b5532f3`.

---

## 2. Contract freeze

Live customer contract: **`analysis_result.UsefulGodView@1.5`**.

- Internal `favorable_gods` ≠ customer Hỷ
- Customer Hỷ source = `favorable_display`
- Dụng / căn cứ / Hỷ / Kỵ / Điều hậu remain separate layers

---

## 3. Control cases

Ten PREFINAL cases locked. Table generated from `G1_PREFINAL_CONTROL_CASES.json` (not hand-typed, not recomputed):

`release/gate_01/G1_FINAL_CONTROL_CASES.md`

LEVEL-1 Mạnh (`jia_wang`) and Dũng (`gia_sac`) remain **detected** with override authority **false**.

---

## 4. Regression re-run (exact PREFINAL Gate-1 command)

```
python -m pytest tests applications/api/tests applications/tests -q --tb=line
  --ignore=tests/test_builder.py
  --ignore=tests/test_pipeline.py
  --ignore=tests/test_rule_loader.py
  --ignore=tests/test_rule_matcher.py
  --ignore=tests/test_rule_scoring.py
  --ignore=tests/test_sentence_generator.py
```

**Result: 2 failed, 1806 passed, 10 subtests passed.** Failures are the documented Class-D knowledge-canon pair.

```
cd applications/customer_portal
npm test
```

**Result: 39 files, 254 passed, 0 failed, 0 skipped.**

Counts did not change vs G1-PREFINAL. No repair was performed.

HTML/PDF/DOCX: PREFINAL four-case smoke remains PASS (`G1_PREFINAL_EXPORT_SMOKE.json`). Exports were not regenerated in G1-FINAL.

---

## 5. Known non-blocking issues

| Item | Class | Why non-blocking |
|------|-------|------------------|
| `tests/knowledge/test_indexes_cli.py::test_cli_real_scaffold` | D | `wood.json` broken KNO-00000x refs |
| `tests/knowledge/test_validators.py::test_real_scaffold_foundation` | D | same |
| Six collectors importing `interpretation_engine` | D | pre-Gate-1 leftover; ignored at CLI |

No unresolved Frozen Truth / hash / Gate-1 engine mismatch.

---

## 6. Tag / packaging

Existing convention: GitHub Release workflow on `v*.*.*`. Tag `v1.0.0` already exists.

**No tag created. No push. No GitHub Release. No production package.**

---

## 7. Deliverables

- `release/gate_01/G1_FINAL_FREEZE.md`
- `release/gate_01/G1_FINAL_FREEZE_MANIFEST.md`
- `release/gate_01/G1_FINAL_ACCEPTANCE_CHECKLIST.md`
- `release/gate_01/G1_FINAL_CONTROL_CASES.md`
- `release/gate_01/G1_FINAL_V1_1_BACKLOG.md`
- `release/gate_01/G1_FINAL_COMPLETION_REPORT.md`

---

## 8. Out of scope (not started)

Gate 2, production deploy, DigitalOcean, customer publish, domain, billing, commercial launch.
