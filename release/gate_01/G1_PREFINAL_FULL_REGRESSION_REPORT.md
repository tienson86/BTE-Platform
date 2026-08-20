# G1-PREFINAL — Full regression report

**Date:** 2026-08-20

---

## Python

### Command actually run (Gate-1 suite)

```
python -m pytest tests applications/api/tests applications/tests -q --tb=line
  --ignore=tests/test_builder.py
  --ignore=tests/test_pipeline.py
  --ignore=tests/test_rule_loader.py
  --ignore=tests/test_rule_matcher.py
  --ignore=tests/test_rule_scoring.py
  --ignore=tests/test_sentence_generator.py
```

**Result: 1806 passed, 2 failed, 10 subtests passed.**

`pytest tests --collect-only --continue-on-collection-errors`: **1808 collected, 6 collection errors.**

Bare repo-root `pytest -q` also descends into `knowledge/packages/**` (historical ~68 collection errors). CI uses `tools/run_tests.py --suite applications`, not that glob. Gate-1 analytical lock is `tests/` + applications tests.

### Remaining failures — class D only

| Test | Class | Why non-blocking |
|------|-------|------------------|
| `tests/knowledge/test_indexes_cli.py::test_cli_real_scaffold` | **D** | `knowledge/knowledge_canon/01_five_elements/knowledge_records/wood.json` broken KNO-00000x relationships. Knowledge-canon scaffold, not Gate-1 engines. |
| `tests/knowledge/test_validators.py::test_real_scaffold_foundation` | **D** | Same canon file. |
| `tests/test_builder.py` (and 5 siblings) | **D** | Collection: `import interpretation_engine` without `engines.` prefix. Pre-Gate-1 leftover modules. Ignored at command line. |

No unresolved **A** (stale expectation), **B** (binding), or **C** (real engine regression) remain in the executed suite.

### Classification of the 51 failures found before cleanup

Almost all were **A**: Huỳnh still expected Đinh/sea_004/strong 0.66; Sơn still expected climate Thực Thần as Overall; customer Hỷ still expected internal `favorable_gods`. Those tests were updated to Frozen Truth.

One presentation **B**: customer `KY_SCOPE_NOTE` contained English `rule` — wording fixed; Kỵ values untouched.

No **C** (unexpected engine result vs Frozen Truth) was found.

---

## Portal / Vitest

```
cd applications/customer_portal
npm test
```

| | |
|--|--|
| Files | 39 |
| Tests | **254 passed / 0 failed / 0 skipped** |
| Command | `vitest run` |

Stale English LP-005/LP-006 labels, internal Hỷ, and `CÂN BẰNG` / catalog-order Ten Gods assertions were updated. Adapters were not reverted.

---

## Export (HTML / PDF / DOCX)

Four control cases via `ProductionEngineRunner` + `ReportExportServiceV1`. Artifacts: `release/gate_01/g1_prefinal_exports/{SON,TUYEN,DUNG,TRUONG}.{pdf,docx}`.

| Case | Unicode name | Gender Nam/Nữ | Dụng + reason | Customer Hỷ | Kỵ | Điều hậu separate | No `str_*`/`spc_*` |
|------|--------------|---------------|---------------|-------------|-----|-------------------|---------------------|
| Nguyễn Tiến Sơn | yes | Nam | yes | insufficient | yes | yes | yes |
| Vũ Thị Thanh Tuyền | yes | Nữ | yes | insufficient | yes | yes | yes |
| Ngô Đắc Dũng | yes | Nam | yes (Tiết) | insufficient | yes | Cần ôn ấm | yes |
| Cao Xuân Trường | yes | Nam | yes (Sinh) | `Thủy · Nhâm · Tỷ Kiên` | yes | yes | yes |

---

## API / live runtime

Fresh in-process `TestClient(create_app())` POST `/api/v1/analyze` for Sơn:

- HTTP 200, `request_id=da9c328e-c837-4674-a50c-31905ba4b29d`
- Contract `@1.5`
- Dụng `Hỏa · Đinh · Chính Quan`
- Customer Hỷ insufficient; canonical Hỷ distinct
- Pillars `Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần`
- `short_reason` has no `str_003`

Portal `npm run build:result` succeeded (2026-08-20 21:11:28 local). Bundle: `applications/customer_portal/static/dist/result.js` SHA256 `DE5BA4972962ACF38B5B19DD15D53BBB5D83E3CDCA726C191352E4827D0C134C`.

ResultStore was not reused (new TestClient process; no last-result key).
