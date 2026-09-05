# CP-BUG-002 CANONICAL CUNG PHI ROUTING REPORT

## Status

PASS

## Root cause

Technical Information read **Gregorian birth-year digit-sum** Cung Phi (`calculate_cung_phi(year=1987, gender=male)` → remainder 7 → **Tốn** → Đông Tứ Trạch), while Tứ Trụ Year Cung Phi used **Tam Nguyên year-ganzhi routing** (Bính Dần / Hạ Nguyên yuan-year 1986, male remainder 6 → **Khôn**).

Two publishers existed for the same analysis:

1. `calendar.ganzhi_routing.year.cung_phi` / `bazi.year_pillar.cung_phi` → Khôn (correct Tứ Trụ Year)
2. `calendar.cung_phi` from raw birth-year digits, plus `feng_shui.gua_name` from the same digit-sum → Tốn

Frontend `adaptIdentityHeader` previously preferred `calendar.cung_phi` / `feng.gua_name` for the Technical Information block, so the same `analysis_id` showed Khôn on Tứ Trụ and Tốn on Technical Information.

This is not a display-text bug. 1966 male coincidentally matches (yuan-year 1966 = birth year), which is why G1-10C did not catch 1987.

## Canonical owner

**Calendar Engine Tam Nguyên year-ganzhi routing** owns personal Cung Phi / Mệnh Quái / Hành Cung / Nhóm Trạch.

Formula:

```text
year Can Chi + birth Tam Nguyên + person gender
        → cung_for_ganzhi(...)
        → house_group_for_cung / element_label_for_cung
```

Published on `CalendarResult.cung_phi` (and `menh_quai`, `hanh_cung`, `nhom_trach`).

For males this equals Tứ Trụ Year Cung Phi. For females it stays gendered (example: 1966 female personal **Cấn**, Year palace still **Đoài**).

Not canonical: Feng Shui Gua digit-sum, raw Gregorian birth-year digit-sum, stale History/feng objects, hard-coded year maps.

## CASE validation

Nguyễn Tiến Sơn · Nam · 21/01/1987 04:30 · Hà Nội

| Field | Value |
|---|---|
| Cung Phi | Khôn |
| Mệnh Quái | Khôn |
| Hành Cung | Thổ |
| Nhóm Trạch | Tây Tứ Trạch |

Tứ Trụ Year Cung Phi = Khôn (unchanged pillar rule). Digit-sum of 1987 remains Tốn inside `calculate_cung_phi` and is **not** published as personal identity.

## Routing before

```text
Gregorian year 1987 digit-sum
        → calculate_cung_phi → Tốn
        → calendar.cung_phi / feng_shui.gua_name
        → Technical Information / Good Date person / leftover presenters
```

Parallel (correct) path for Tứ Trụ Year:

```text
Bính Dần + Hạ Nguyên
        → ganzhi_routing.year.cung_phi = Khôn
        → Tứ Trụ Năm
```

## Routing after

```text
Canonical year-ganzhi + Tam Nguyên + gender
        → CalendarResult.cung_phi / menh_quai / hanh_cung / nhom_trach
        → Analyze payload
        → bindPersonalCungPhiIdentity
        → Technical Information / Overview context / Full Report / PDF / DOCX
```

Guards:

- Orchestrator does not overlay Feng Shui identity onto calendar when `calendar.cung_phi` is already set.
- Male/unknown frontend binding prefers year-routing palace over stale `calendar.cung_phi=Tốn`.
- Female binding prefers gendered `calendar.cung_phi` over Year male palace.
- Nhóm Trạch is derived from the chosen palace (Khôn → Tây Tứ Trạch; Tốn → Đông Tứ Trạch). Cross-family pairs are rejected.
- Date Selection `person_profile` uses `calendar.cung_phi` + `trach_from_cung`. Day scoring rules are unchanged.
- Legacy `chart_info.js` `resolveBatTrach` now prefers calendar / year-routing over `feng_shui`.

## Tests

| Suite | Result |
|---|---|
| `pytest tests/calendar -q` | 135 passed |
| `pytest tests/date_selection -q` | 128 passed |
| `pytest applications/api/tests/test_production_readiness.py -q` | 3 passed (1987 male now Khôn / Thổ / Tây Tứ Trạch) |
| `vitest tests/js/cp_bug_002_personal_cung_phi.test.tsx` | 4 passed (stale Tốn cannot override Year Khôn; 1966 female stays Cấn) |
| `vitest tests/js/g1_10c_tutru_cung_phi.test.tsx` | 2 passed |
| `vitest tests/js/canonical_desktop_adapter.test.tsx` | 5 passed |

New coverage:

- `tests/calendar/test_cp_bug_002_canonical_personal_cung.py` — 1987 male Khôn not Tốn; 1966 male Đoài; 1966 female Cấn; Khôn→Thổ→Tây / Tốn→Mộc→Đông invariant; Good Date person matches calendar.
- `applications/customer_portal/tests/js/cp_bug_002_personal_cung_phi.test.tsx` — Technical Information must not show Tốn when Year is Khôn; stale current payload cannot override year routing.

## Cross-surface parity

Same personal identity for the live CASE:

| Surface | Cung Phi | Mệnh Quái | Hành Cung | Nhóm Trạch |
|---|---|---|---|---|
| /result Tứ Trụ Year | Khôn | — | — | — |
| /result Technical Information | Khôn | Khôn | Thổ | Tây Tứ Trạch |
| /result Overview | no personal Cung Phi field (Cân Xương only) | | | |
| Good Date / Choose Date person | Khôn | same palace | Thổ | Tây Tứ Trạch |
| History (`?from=history&id=`) | same analysis payload + same binder | | | |
| Full Report HTML | Khôn | Khôn | Thổ | Tây Tứ Trạch |
| PDF / DOCX | calendar.cung_phi / menh_quai / hanh_cung / nhom_trach | | | |
| API `data.calendar` | Khôn | Khôn | Thổ | Tây Tứ Trạch |

Feng Shui Gua calculator is unchanged and is **not** the personal-identity source.

## Runtime screenshot

`implementation/bugfixes/screenshots/CP-BUG-002_result_cung_phi_parity.png`

Proof JSON: `implementation/bugfixes/CP-BUG-002_live_proof.json`

Live servers left running at `http://localhost:8081/result` after a fresh analyze of this CASE.

## Files changed

Calendar / identity owner

- `engines/calendar_engine/cung_phi.py`
- `engines/calendar_engine/engine.py`
- `engines/date_selection/service.py` (person identity only)

API / report copy path

- `applications/api/services/orchestrator.py`
- `applications/api/services/customer_report_input.py`
- `applications/api/tests/test_production_readiness.py`
- `engines/report_engine/contracts/report_input_v1.py`
- `engines/report_engine/adapters/report_input_v1_adapter.py`
- `engines/report_engine/rendering/report_sections_v1.py`

Frontend binding

- `applications/customer_portal/src/adapters/personalCungPhi.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/adapter.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/types.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/IdentityRegions.tsx`
- `applications/customer_portal/src/adapters/canonicalDesktopAdapter.ts`
- `applications/customer_portal/src/report/fullReportViewModel.ts`
- `applications/customer_portal/src/screens/result/adapters/resultPresentationAdapter.ts`
- `applications/customer_portal/src/screens/result/viewModels.ts`
- `applications/customer_portal/src/screens/result/zones/ContextZone.tsx`
- `applications/customer_portal/static/js/presenters/chart_info.js`

Tests / proof

- `tests/calendar/test_cp_bug_002_canonical_personal_cung.py`
- `applications/customer_portal/tests/js/cp_bug_002_personal_cung_phi.test.tsx`
- `applications/customer_portal/scripts/capture_cp_bug_002_live.py`
- `implementation/bugfixes/CP-BUG-002_live_proof.json`
- `implementation/bugfixes/screenshots/CP-BUG-002_result_cung_phi_parity.png`

Not part of this bug (already present Pack 07 work in the working tree): `engines/detailed_interpretation_engine/**`, `applications/api/contracts/pack07_runtime.py`, `applications/api/app.py` register_all_engines, `engines/core/register_engines.py`, `applications/api/models/analysis_result.py` pack07_context.

## Analytical engines changed

Calendar **personal identity publisher** was repaired. That was the incorrect upstream value for Technical Information.

Unchanged: BaZi pillars, Strength, Pattern, Useful God, Feng Shui Gua calculator, MC-01, Pack 07, Narrative, Good Date **day scoring** rules, Tứ Trụ pillar Cung Phi binding.

## Regression

PASS for the requested 1987 male CASE and preserved 1966 male Đoài / 1966 female Cấn / 1984 / 2026 verification years.

Remaining unrelated failures (not this bug, tests not edited): some ResultStore boot tests still reject fixtures that omit `calendar.calendar_rule_version = G1-10C` (`full_report_composition` K, `canonical_result_routing` A–L, UI-03 G15).

## STOP

Do not resume P7-IMP-02. Waiting for Product Owner review.
