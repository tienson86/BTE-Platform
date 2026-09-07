# TV1-B08 — Testing & Golden Validation

Status: COMPLETE  
Module: TV-01 Marriage Consulting  
Date: 2026-09-07

This phase is testing only. No product features were added. No COMMON, Canonical Mathematics, or Decision Mathematics files were modified. No production TV-01 semantics were changed.

## 1. Test matrix

| ID | Category | Result |
|----|----------|--------|
| A | Input / Truth boundary | PASS |
| B | Evidence families | PASS |
| C | Findings | PASS |
| D | Decision states | PASS (reachable states only) |
| E | Recommendations | PASS |
| F | Narrative semantic fidelity | PASS |
| G | Report Customer Story | PASS |
| H | Public API | PASS |
| I | Presentation / UI | PASS |
| J | Cross-layer traceability | PASS |
| K | Determinism ×10 | PASS |
| L | B01–B07 regression | PASS (`tests/consulting` 214) |
| M | Golden Dataset CASE-M01..M12 | PASS |
| N | Adversarial / boundary | PASS |
| — | State isolation | PASS |
| — | Live Canonical E2E (3 pairs) | PASS |
| — | Browser desktop + mobile | PASS |

## 2. Golden Dataset

Frozen semantic signatures: `tests/consulting/golden/expected/CASE-M*.json`

| Case | Intent | Observed overall | Notes |
|------|--------|------------------|-------|
| CASE-M01 | Strong structural support | mixed | D1 supportive; D2 mixed from stem/branch catalog density |
| CASE-M02 | Mixed support + clash | mixed | Frozen golden pair |
| CASE-M03 | Pressure with rescue | mixed | Clash/harm rescued; atoms retained |
| CASE-M04 | Asymmetric A_TO_B | mixed | Useful support A→B only |
| CASE-M05 | Asymmetric B_TO_A | mixed | Useful support B→A only |
| CASE-M06 | Secondary favorable, core mixed | mixed | Same natal overall as M02 |
| CASE-M07 | Missing Person A hour | mixed | `birth_time_unknown` limitation |
| CASE-M08 | Missing both hours | mixed | Limitation, not marital risk |
| CASE-M09 | Finance finding/action | mixed | `financial_structure` published |
| CASE-M10 | Timing if legitimate | mixed | `luck_alignment` + `timing_awareness`; natal overall unchanged |
| CASE-M11 | D4/D6/D7 unavailable | mixed | interaction/family/children insufficient |
| CASE-M12 | Semantic dedup | mixed | Findings with `source_count` 16 / 10 / 3 |

Overall `supportive` / `pressured` / `balanced` / `critical` were not manufactured. Domain-level `supportive`, `mixed`, `pressured`, `balanced`, and `insufficient` are all present in the dataset.

## 3. Coverage

- Truth Boundary: complete A/B, missing A/B/both hours, optional place, invalid date/time, missing gender, no defaults, distinct correlation ids, no raw-birth reread after snapshots.
- Evidence: Five Elements / Useful God, Stem/Branch, Ten Gods, Finance, Timing, Secondary; positive / conflict / absence / A_TO_B / B_TO_A / SHARED; secondary cannot dominate.
- Finding: empty evidence → no finding; same-semantic merge with multiple source ids; conflicts and rescue preserved; unavailable domains not fabricated; deterministic `F-####` order.
- Decision: natal overall from Tier 1; timing does not rewrite natal; D4/D6/D7 insufficient; score/grade null; `critical` not reachable (no P0 rule).
- Recommendation: all five frozen action types observed across Golden + live; no action without source Finding; same-intent merge; priority ≠ urgency catalog; missing data does not create negative advice.
- Journey: identity → executive_summary → compatibility_hero → strengths → risks → (timing if present) → domain_analysis → action_plan → confidence_limitations → conclusion → appendix.

## 4. Traceability / determinism / adversarial / isolation / API

Traceability: all 12 Golden cases have action Narrative → Recommendation → Finding → Evidence → Canonical `source_refs`, and non-action Narrative → Finding → Evidence → Canonical source.

Determinism: 10 repeats of CASE-M01, M02, M09, M12 plus 10 Fake-Canonical API POSTs; semantic signatures identical; consultation ids distinct.

Adversarial: duplicate atoms, opposing evidence, large atom lists, secondary-only, no rec-generating finding, empty evidence, missing timing, timing vs natal, expert after customer, malformed `expert`, unicode/long names, unknown place, idempotent replay, customer JSON id leak.

Isolation: two consultations, scoped A/B ids, GET does not mutate Decision, isolated idempotency keys, 404 does not disturb stored rows.

API: POST/GET consultation/summary/report/history, invalid, 404, replay, conflict, warnings, customer/expert, pagination, score/grade null. Covered by B06 tests plus B08 layers/adversarial/live.

## 5. Browser

Isolated host `python -m consulting.marriage.ui.capture_b08`. Desktop 1280 and mobile 390. Verification: `docs/reports/tv01_marriage/b08/browser_verification.json` — no fake score, no EV/F/RC leak, no overflow, no empty interaction card.

## 6. Performance baseline

Live pair 1987-01-21 / 1990-05-15 (representative, not an SLA):

| Stage | ms |
|-------|----|
| API total | 4381.491 |
| Canonical runtime | 4335.213 |
| Decision | 5.365 |
| Recommendation | 0.622 |
| Narrative + Report | 6.360 |

Source: `docs/reports/tv01_marriage/b08/performance_baseline.json`

## 7. Bugs

Found: none BLOCKER, none MAJOR.

Fixed: none. No production TV-01 files were modified in B08.

Open limitations / debt:

- Overall `supportive`/`pressured`/`balanced`/`critical` not currently produced by implemented extractors on legitimate pairs (Tier 1 mix is typical). Domain-level states are covered.
- Customer warning strings remain English API copy from B06 (`TIMEZONE_UNSPECIFIED`, `DOMAIN_UNAVAILABLE`). Frozen contract; not changed.
- `datetime.utcnow` deprecation originates in Canonical `<string>`, not TV-01. Count from `pytest tests/consulting`: 449 DeprecationWarning + 1 Starlette/httpx warning.
- `mypy consulting`: 1 pre-existing arg-type on `CANONICAL_STOP_STAGE` in B02 `canonical_runtime.py`. Not introduced by B08 tests.
- Repo-wide `tsc --noEmit`: pre-existing unrelated files (see completion report). No Marriage Consulting errors.

## 8. Architecture compliance

COMMON unchanged. Canonical unchanged. Decision Mathematics unchanged. B03–B07 semantics unchanged. Score/Grade still unavailable. No PDF/DOCX. No durable persistence. Isolated UI composition unchanged. TV1-B09 not started.
