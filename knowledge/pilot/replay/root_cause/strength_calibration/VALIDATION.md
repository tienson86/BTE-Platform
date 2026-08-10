# VALIDATION — PILOT-1B

## Scope confirmations

| Constraint | Status |
|---|---|
| No Knowledge Package changes | **Confirmed** |
| No Golden Dataset Expected changes | **Confirmed** |
| No AF-1 changes | **Confirmed** |
| No API contract changes | **Confirmed** |
| No UI changes | **Confirmed** |
| No pipeline changes | **Confirmed** |
| No case-specific patches | **Confirmed** |
| No test weakening / deletion | **Confirmed** |
| No fabricated birth/case data | **Confirmed** |
| No silent fixture mutation | **Confirmed** (CASE-0006 correction applied only in analysis notes / live chart) |
| Score conclusions traceable | **Confirmed** (`evidence/*.json` + ledgers) |
| Taxonomy recommendations evidence-based | **Confirmed** (partial support; n=7) |

## Tests executed

| Suite | Result | Classification |
|---|---|---|
| `python -m pytest tests/golden_dataset/test_golden_dataset.py -q` | **1 passed** | — |
| `python -m pytest tests/score/test_strength.py -q` | **1 passed** | — |

No Strength production code modified; no new regressions introduced by this sprint.

## Replay

CASE-0001…0007 strength extraction completed via:

```text
knowledge/pilot/replay/root_cause/strength_calibration/_extract_evidence.py
```

CASE-0006 judged on live **Mậu Ngọ** chart (PILOT-1A corrected interpretation).

## Production-code change gate

| Question | Answer |
|---|---|
| Objective calculation/polarity bug proven? | **No** |
| Fix implemented? | **No** |
| Fix proposed? | N/A (no P0) |

## Final decision cross-check

Documented in `PILOT_1B_SUMMARY.md`:

**STRENGTH_TAXONOMY_LIMITATION_CONFIRMED**
