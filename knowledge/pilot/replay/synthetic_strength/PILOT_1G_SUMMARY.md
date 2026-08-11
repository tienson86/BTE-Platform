# PILOT_1G_SUMMARY — Synthetic Strength Stress Replay V1

**Purpose:** Create and execute a 21-case synthetic Strength stress dataset covering seven candidate taxonomy levels.

**Scope:** Engine testing only. Synthetic fixtures + harness + reports. No production Strength changes.

## Outcome

- Created **21** SYN-STR cases (`SYN-STR-000001` … `SYN-STR-000021`).
- Replayed all **21** against existing Strength Engine.
- Exact v1-projection matches: **16**.
- Mismatches: **5** (diagnostic; not patched).

## Extreme tests

- VERY_WEAK extremes: directionally detected as weak.
- VERY_STRONG extremes: NOT distinguishable from STRONG (score ceiling 1.000).
- BALANCED: all three matched.

## Score-only finding

Score-only mapping is **NOT_SUFFICIENT** for seven-level taxonomy: similar scores can carry different synthetic labels, and STRONG/VERY_STRONG both saturate at 1.000.

## Artifacts

- `datasets/`, `results/`, `harness/`, `tests/`
- `SYNTHETIC_STRENGTH_REPLAY_REPORT.md`
- `MISMATCH_ANALYSIS.md`
- `SCORE_DISTRIBUTION_ANALYSIS.md`
- `validation/VALIDATION.json`

---

Status:
- SYNTHETIC_CASES_CREATED: 21
- SYNTHETIC_CASES_REPLAYED: 21
- EXACT_MATCHES: 16
- MISMATCHES: 5
- VERY_WEAK_CASES: 3
- WEAK_CASES: 3
- SLIGHTLY_WEAK_CASES: 3
- BALANCED_CASES: 3
- SLIGHTLY_STRONG_CASES: 3
- STRONG_CASES: 3
- VERY_STRONG_CASES: 3
- CALIBRATION_CASES_CHANGED: NO
- GOLDEN_EXPECTED_CHANGED: NO
- PRODUCTION_CODE_CHANGED: NO
- STRENGTH_ENGINE_CHANGED: NO
- KNOWLEDGE_PACKAGES_CHANGED: NO
- AF1_CHANGED: NO
- TEST_REGRESSION: NO

Final Decision:
SYNTHETIC_REPLAY_PARTIAL

Recommendation:
- NEXT_ACTION: Analyze synthetic mismatches without modifying production Strength behavior.
