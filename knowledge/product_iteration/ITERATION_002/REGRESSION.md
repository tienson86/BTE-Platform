# REGRESSION

| Field | Value |
|-------|-------|
| Step | 6 |
| Golden Dataset | **FROZEN — not edited** |
| Quality Gates | **FROZEN — not edited** |
| Tests | **Not edited** |

---

## Command

```text
py -3.14 -m pytest tests/production/test_commercial_language.py \
  tests/production/test_product_context.py \
  tests/production/test_case_0001_regression.py -q
```

| Result | Value |
|--------|-------|
| Exit | **0** |
| Passed | **34** |
| Failed | **0** |
| Skipped | **0** |

Full-project pytest was **not** run (module-only rule).

---

## Golden

| Chart | Requirement | Result |
|-------|-------------|--------|
| CASE_0001 | Frozen Golden regression **PASS** | **PASS** (`test_case_0001_regression`) |
| Snapshots / expected | Untouched | **PASS** |
| Dataset files | Untouched | **PASS** |

---

## Product holds

| Chart | Hold | Result |
|-------|------|--------|
| CASE_0002 | OUTPUT room + 8.0 Overall | **PASS** (8.0 hold) |
| CASE_0003 | Parent pack + Career hidden | **PASS** (7.5 hold) |

---

## Layers not changed (must stay clean)

| Layer | Status |
|-------|--------|
| Engines / Rule Database / Knowledge | Untouched |
| CDR / Reasoning | Untouched |
| Product Context adaptive | Untouched |
| Theme Library catalog | Untouched |
| CLL specification markdown | Untouched |
| Quality Gates markdown | Untouched |

---

## Remaining failures

**None** on the module set above.

Known product residuals (not test failures): PB-005, PB-006, PB-007, PB-008, PB-010.

---

END
