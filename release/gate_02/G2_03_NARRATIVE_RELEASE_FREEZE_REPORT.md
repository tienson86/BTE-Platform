# G2-03 — Interpretation / Narrative release freeze report

**Status: G2-03: INTERPRETATION / NARRATIVE FROZEN — READY FOR G2-04**

Date: 2026-08-20  
Entry: G2-02 Customer Result UI frozen  
This is **not** a narrative enhancement sprint. Prose was not made longer, deeper, more literary, or more predictive.

## Hard freeze

Gate 1 analytics are unchanged. G2-01R identity/routing/`@1.5` is unchanged. G2-02 Result layout is unchanged except interpretation **empty-state** when `narrative_result` is missing (spec 28).

If narrative had looked wrong because an analytical value was wrong, this gate would have **stopped**. Ten control cases remain **0 analytical diffs**.

## Canonical path

One V1.0 customer spine:

`build_narrative_result_dict` → Narrative Composer V2 → `pack05_narrative_result_v1` → Portal `/result` interpretation + Full Report + Report/PDF binding.

Pack 05 `NarrativeEngine` remains compatibility fallback only.

Full contract: `release/gate_02/G2_03_NARRATIVE_CONTRACT.md`.

## Presentation-only defects closed

| Defect | Fix (not engines) |
|--------|-------------------|
| Commercial projection read `pattern.dung_than` / `pattern.ky_than` | Read `useful_display` / `unfavorable_display` only |
| 0–1 Strength score treated as 0–100 → strong charts called `mỏng lực` | Band wins; 0–1 unit scale |
| Insufficient Hỷ phrased as a definite supporting god | HK-R1H copy; no invented Hỷ environment action |
| `Than nhược` / `Than trung hòa` leaking from rule labels | Narrative `normalize_text` + commercial replacements; CSV untouched |
| HTTP narrative `run_id` not aligned with `analysis_id` | Stamp copies request_id onto empty `run_id` |
| Missing narrative fabricated a 3-block chart essay | Limited empty interpretation state |

## Acceptance

| Check | Result |
|-------|--------|
| One canonical narrative path | PASS |
| Same analysis ID (HTTP stamp) | PASS |
| 10 control cases consistent | PASS 10/10 · analytical MATCH 10/10 |
| No Strength / Pattern / Dụng contradiction | PASS |
| No unsupported Hỷ invention | PASS |
| Điều hậu remains separate | PASS |
| LEVEL-1 special wording safe | PASS |
| No stale active-customer strings | PASS |
| No rule IDs / unresolved placeholders | PASS |
| Fallback does not fabricate chart-specific truth | PASS |
| Old History version policy respected | PASS (G2-01R notice) |
| Gate-1 analytical files changed | **0** |

## Tests

```
python -m pytest tests/commercial_knowledge applications/api/tests/test_result_identity.py applications/api/tests/test_narrative_result_canonical_binding.py tests/interpretation_engine/foundation/interpreters/test_useful_god_interpreter.py -q
npx vitest run tests/js/g2_03_narrative_freeze.test.ts tests/js/g2_02_customer_result_ui.test.tsx tests/js/canonical_result_routing.test.ts tests/js/g2_01r_canonical_binding.test.ts
python release/gate_02/_g2_03_narrative_probe.py
```

- Python (those modules): **pass** (commercial_knowledge  + identity + narrative binding + useful-god interpreter)
- Portal: **41 passed / 0 failed** (4 files, including 6 new G2-03 tests)
- Ten-case probe: **fail: []**
- Result bundle rebuilt: `npm run build:result`

Existing G1 tests were **not** rewritten to weaken asserts. G2-03 added:

- `applications/customer_portal/tests/js/g2_03_narrative_freeze.test.ts`
- `tests/commercial_knowledge/test_g2_03_signal_projection.py`
- one identity assert in `applications/api/tests/test_result_identity.py`

## Diff audit (this phase)

Analytical engine / rule files changed: **0** (`database/`, Calendar, BaZi, Score, Pattern, Useful God winner/rules, Strength, Luck: clean).

Allowed changes: commercial presentation, explainer wording, narrative text sanitize, identity stamp, interpretation empty-state, tests, release docs, Result bundle.

## Remaining (not blocking)

- In-process orchestrator still has empty `analysis_id`/`run_id` (equal). Customer HTTP stamps both.
- Some repetition between Exec commercial copy and interpretation sections is retained (spec 31).
- PDF layout freeze is **G2-04**. Narrative **source** is already the same canonical blob.

## Deliverables

- `release/gate_02/G2_03_NARRATIVE_RELEASE_FREEZE_REPORT.md` (this file)
- `release/gate_02/G2_03_CONTROL_CASE_NARRATIVE_MATRIX.md`
- `release/gate_02/G2_03_STALE_STRING_AUDIT.md`
- `release/gate_02/G2_03_NARRATIVE_CONTRACT.md`
- `release/gate_02/G2_03_REFREEZE_CHECKLIST.md`
- Probe: `release/gate_02/G2_03_NARRATIVE_PROBE.json`

## Next

Do **not** start G2-04 automatically. G2-04 begins only after Product Owner accepts this freeze.
