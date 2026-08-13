# REGRESSION_RULES

| Field | Value |
|-------|-------|
| Document | REGRESSION_RULES |
| Dataset | GOLDEN_DATASET_V1 |
| Status | **FROZEN** |
| Date | 2026-08-13 |

---

## Prime rule

**No improvement may regress a previous Golden Case.**

If CASE_0001 (or any later Frozen case) loses commercial meaning, chart identity, or customer-pass status, the change is rejected — even if CASE_0002 or CASE_0003 improves.

---

## What “regress” means

A Golden Case has regressed if any of the following move without an approved version bump:

| ID | Must hold |
|----|-----------|
| R-ID | Four pillars and day master identity |
| R-STR | Strength band and published score class (e.g. CASE_0001 strong ≈ 0.87) |
| R-PAT | Pattern family / direction (e.g. CASE_0001 Chính Ấn) |
| R-UG | Useful God identity and published favor / unfavor |
| R-TG | Leading ten-god character (not a renamed story) |
| R-THEME | Primary commercial theme family (e.g. OPERATING_SELF_CARRY vs OPERATING_OUTPUT) |
| R-CX | Customer-facing Identity / Career / Executive remain commercially passing |
| R-DIV | No leakage of another case’s memory / insight template into the Golden Case |
| R-PKG | Customer Mode still hides diagnostics, Draft labels, and engineering appendices |

CASE_0001 freeze contract (do not duplicate here):

- `knowledge/validation/CASE_0002/REGRESSION.md`
- `knowledge/validation/CASE_0003/REGRESSION.md`
- `knowledge/validation/CASE_0002/REVALIDATION_V1_1/CASE_0001_REGRESSION.md`
- `knowledge/commercial_language/IMPLEMENTATION_V1_2/CASE_0001_REGRESSION.md`
- `knowledge/reasoning_engine/CROSS_DOMAIN_V1_1/CASE_0001_REGRESSION.md`
- `knowledge/reasoning_engine/PACK_01_STRENGTH/FREEZE/CASE_0001_GOLDEN_REFERENCE.md`

---

## Anti-regression (implementation)

| Rule | Statement |
|------|-----------|
| AR1 | No case-id special-case in the production orchestrator |
| AR2 | Do not thin a Golden commercial sample to match a weaker generic composer |
| AR3 | Template fixes must remain correct for the Golden chart type, not only the new case |
| AR4 | New structure language (follow, weak, child) is **additive** |
| AR5 | Do not edit frozen Master Interpretations or Golden feature samples to absorb a new case |
| AR6 | Do not “fix” Golden by changing expected fixtures or this laboratory’s recorded scores |

---

## Minimum release rules

A change that touches customer language, reasoning, packaging, or engines may release only if:

1. **All Frozen Golden Cases** re-run PASS on R-ID through R-PKG.
2. **No new S0** on any Golden Case.
3. **Commercial Score** of each Frozen case does not fall below its freeze floor (CASE_0001 floor: overall ≥ 7.0 and commercial acceptance PASS).
4. **Identity / Career / Executive** of each Frozen case remain at or above freeze floors (CASE_0001: Identity ≥ 8.0, Career ≥ 8.0, Executive ≥ 8.5 — from published reviews; do not lower floors to pass a new case).
5. **Module tests** required by the owning layer are green (prerequisite only; not a substitute for Golden review).
6. **Issue register** updated for any new Golden finding.

If a non-Golden case improves and a Golden case is not re-run, the release is invalid.

---

## Stress cases

STRESS cases (CASE_0003 today) are **not** Golden.

They must still be re-run after improvements that claim to fix their class (weak, child, follow), but:

- A STRESS score remaining below commercial floor is not a Golden regression.
- A STRESS case **must not** be used as the reason to weaken Golden copy.

---

## Failure response

```text
Golden FAIL
  ↓
Stop merge
  ↓
Register issue against the change
  ↓
Revert or isolate
  ↓
Do not lower Golden floors
```

---

## Test suites (CASE_0001 — as already required)

Recorded in existing regression docs; not expanded here:

- `tests/production`
- `tests/report_engine/test_case_0001_report_input.py`
- `engines/interpretation_engine_v2/strength/tests`
- `tests/ten_gods_engine`
- commercial_language `test_case_0001_regression` where present

Laboratory rule: those suites are **evidence**. This document is the **policy**.

---

END
