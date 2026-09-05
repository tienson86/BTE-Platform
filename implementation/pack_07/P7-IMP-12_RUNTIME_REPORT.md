# P7-IMP-12 TEMPORAL ACTIVATION RUNTIME REPORT

**Task:** P7-IMP-12 — Temporal Activation Engine — annual live vertical slice  
**Date:** 2026-09-05  
**Status:** PASS

Live CASE-0001: Nguyễn Tiến Sơn, male, 21/01/1987 04:30, Hà Nội.

Natal Truth → Luck Cycle Activation → Luck Interaction → Annual Modifier → Temporal Expression.

Annual does not rewrite Natal. Annual does not rewrite Luck Cycle. Specificity is not dominance. No arithmetic stacking. No event prediction. Life Optimization and Narrative Composer were not implemented.

---

## Status

PASS

Temporal Activation Engine publishes a separate annual refinement onto `CanonicalRuntimeResult.temporal.temporal_activation`. Schema: `bte.detailed_interpretation.temporal_activation.v1`. Ruleset: `bte.detailed_interpretation.temporal_activation.rules.v1`.

Luck Activation and Luck Interaction remain separate objects on the same temporal section.

---

## Canonical annual owner

Exact owner: `engines.luck_engine.providers.liunian.DefaultLiunianProvider`

Orchestrated by: `engines.luck_engine.engine.LuckEngine.build`

Model: `engines.luck_engine.models.periods.LiunianPeriod` via `LuckContext.current_liunian`

Public identity stamp (no recalculation): `applications.api.services.luck_truth.shape_luck_payload` → `luck.annual_identity`

Pack 07 consumes that identity. It does not call `year_ganzhi` or rebuild the annual pillar.

---

## Current annual layer

Canonical calendar runtime through LuckEngine, not hard-coded.

- Civil / BaZi year: **2026**
- Pillar: **Bính Ngọ**
- Stem / branch: Bính / Ngọ
- Stem / branch element: Hỏa / Hỏa
- Annual Ten God actor vs Day Master Canh: **Thất Sát** (`annual_killer`)
- Time window: **2026**
- Parent envelope: Đại Vận Ất Tỵ · 2022–2031

Customer UI shows `Năm 2026`. Canonical contract never uses `năm nay`.

---

## Temporal hierarchy

```
natal
↓
luck_cycle     evaluated (bind DI-09 by reference)
↓
annual         evaluated (current year only)
↓
monthly        not_evaluated
↓
daily          not_evaluated
↓
hourly         not_evaluated
```

Requested: `luck_cycle`, `annual`. Evaluated: those two. Child refines parent. Specificity ≠ dominance.

---

## Activation Envelope

Luck cycle copies each domain’s `activation_state` as the annual operating envelope. Annual modifiers move expression inside that envelope. Luck Activation objects stay identical.

Live example:

- Luck Career = overloaded
- Annual Career = strengthen (officer/killer year on an already overloaded envelope)
- Result: Đại Vận remains overloaded; annual expression stays overloaded because more activation is not automatically better

Live counter-example of non-dominance:

- Luck Relationship = dormant
- Annual Relationship = stress
- Result: Luck stays dormant; annual expression is only weak

---

## Authority

| Layer | Result |
| --- | --- |
| Natal | conditional |
| Luck | overloaded (`temporal_wealth`) |
| Annual | modifier `strengthen` · expression **overloaded** · driver `annual_killer` · bottleneck `annual_carrying_capacity` · stress high · recovery none |

No office/promotion prediction.

---

## Career

| Layer | Result |
| --- | --- |
| Natal | conditional |
| Luck | overloaded (`temporal_wealth`) |
| Annual | modifier `strengthen` · expression **overloaded** · driver `annual_killer` · bottleneck `annual_carrying_capacity` · stress high · recovery none |

No job-change prediction.

---

## Wealth

| Layer | Result |
| --- | --- |
| Natal | fragmented |
| Luck | conditional (`temporal_wealth`) |
| Annual | modifier `stabilize` · expression **transition** / Ổn định · driver `not_applicable` · bottleneck none |

Officer/killer year does not rewrite natal Five Element balance and does not turn Wealth into a luck-cycle rewrite. No wealth-event prediction.

---

## Relationship

| Layer | Result |
| --- | --- |
| Natal | fragmented |
| Luck | dormant |
| Annual | modifier `stress` · expression **weak** · driver `annual_killer` · bottleneck `annual_officer_pressure` · stress moderate |

No marriage/divorce prediction. Dormant Đại Vận is not overwritten to strong.

---

## Legacy

| Layer | Result |
| --- | --- |
| Natal | conditional |
| Luck | conditional |
| Annual | modifier `stabilize` · expression **transition** / Ổn định · driver `not_applicable` |

No fertility prediction.

---

## Vitality

| Layer | Result |
| --- | --- |
| Natal | conditional |
| Luck | dormant |
| Annual | modifier `stress` · expression **weak** · driver `annual_killer` · bottleneck `annual_officer_pressure` · stress moderate |

No diagnosis. Existing MC-01 Damage/Rescue may surface as `damage_activation` / `rescue_activation` on annual conditions. No new natal Damage or Rescue is created.

---

## Temporal salience

`authority`, `career`

These are already-important natal domains most activated in 2026. Natal Evidence Priority is not reranked. Authority remains natal P0 even though annual salience is also Authority.

---

## Dominant annual activation

`authority` / Quyền hạn

---

## Dominant annual suppression

`authority` / Quyền hạn

Overloaded + high annual stress on the same domain. Not a bad-event flag.

---

## Natal immutability

PASS

Snapshot before/after Temporal: MC-01, Evidence Priority, Domains, natal Ten Gods, natal Shen Sha unchanged. Pattern and Grade untouched. Annual Ten God actors stay on the annual layer.

---

## Luck immutability

PASS

`LuckActivationResult` object identity is preserved across bind. Activation states are copied into the envelope, never written back.

---

## Interaction immutability

PASS

`LuckInteractionResult` object identity is preserved. Interaction driver/bottleneck/findings are not recalculated by Temporal.

---

## Monthly/Daily/Hourly

Contract shells present:

| Layer | State |
| --- | --- |
| monthly | `not_evaluated` |
| daily | `not_evaluated` |
| hourly | `not_evaluated` |

No monthly reasoning. No Good Date decision. No hourly evaluation. No 10y × 12m × day × hour grid.

---

## Runtime binding

`CanonicalRuntimeResult.temporal.temporal_activation`

Kept separate from:

- `temporal.luck_activation`
- `temporal.luck_interaction`

Customer compact: `payload["luck"]["annual"]` on the existing Đại Vận object. Canonical identity: `payload["luck"]["annual_identity"]`.

---

## Developer diagnostics

Live POST `/api/v1/dev/pack07/diagnostics`:

| Field | Status |
| --- | --- |
| Contracts | PASS |
| Contexts | PASS |
| Validators | PASS |
| MC-01 | PASS |
| Ten Gods | PASS |
| Combination | PASS |
| Ten Gods Ecosystem | PASS |
| Shen Sha | PASS |
| Shen Sha Ecosystem | PARTIAL |
| Evidence Priority | PASS |
| Domains | PASS |
| Luck Activation | PASS |
| Luck Interaction | PASS |
| Temporal Activation | PASS |
| Optimization | NOT_EVALUATED |
| Narrative | NOT_EVALUATED |
| Runtime Contract | PASS |

Empty GET keeps `temporal = NOT_EVALUATED`.

---

## UI integration

Existing Đại Vận `LuckCard`. Below Luck Interaction: **BIỂU HIỆN LƯU NIÊN** (`data-luck-section="annual"`).

Compact summary: Năm 2026, Bính Ngọ, dominant activation, main suppression, stress, recovery, six-domain comparison grid `Nền | Đại vận | Năm 2026` with expandable annual detail.

Empty luck still has no `data-luck-section`. PDF/DOCX/History were not forced to carry annual detail.

---

## Build

PASS

`python tools/build.py` — compileall applications, tools, engines.

---

## Type Check

PASS

Pack 07 scoped mypy: 103 source files, no issues.

---

## Tests

| Suite | Result |
| --- | --- |
| `tests/detailed_interpretation` | 196 passed |
| `test_p7_imp_12_temporal_activation` | 15 passed |
| Luck contract + G1-08 + identity publish | included in 49 passed with PDF/DOCX/history |
| PDF renderer | PASS |
| DOCX renderer | PASS |
| History snapshot + portal history | PASS |
| Analyze e2e + calendar Gan-Zhi routing | 15 passed |
| Portal vitest UI-10 / UI-10R / UI-10R1 | 50 passed, 1 pre-existing fail |

Remaining failure: UI-10 L25 `ResultStore` `empty` vs `current`. Pre-existing from P7-IMP-11. Not repaired.

---

## Runtime

| Endpoint | Result |
| --- | --- |
| GET `/api/v1/health` | 200 ok |
| POST `/api/v1/analyze` CASE-0001 | 200, `luck.annual` present, year 2026, pillar Bính Ngọ |
| `/result` | live annual section renders |
| `/history` | 200, no persistence change |
| POST `/api/v1/dev/pack07/diagnostics` | temporal PASS |
| GET `/api/v1/dev/pack07/diagnostics` | temporal NOT_EVALUATED |

---

## Screenshots

| Shot | Path |
| --- | --- |
| /result overview | `implementation/pack_07/screenshots/p7_imp_12_result_overview.png` |
| current Đại Vận | `implementation/pack_07/screenshots/p7_imp_12_luck_current.png` |
| Luck Activation | `implementation/pack_07/screenshots/p7_imp_12_luck_activation.png` |
| Luck Interaction | `implementation/pack_07/screenshots/p7_imp_12_luck_interaction.png` |
| Annual Temporal summary | `implementation/pack_07/screenshots/p7_imp_12_annual_summary.png` |
| Natal/Luck/Annual comparison | `implementation/pack_07/screenshots/p7_imp_12_annual_comparison.png` |
| one annual Domain expanded | `implementation/pack_07/screenshots/p7_imp_12_annual_domain_expanded.png` |
| mobile Annual view | `implementation/pack_07/screenshots/p7_imp_12_mobile_annual.png` |
| diagnostics Temporal PASS | `implementation/pack_07/screenshots/p7_imp_12_diagnostics.png` |

---

## PDF

PASS / intentionally unchanged

---

## DOCX

PASS / intentionally unchanged

---

## History

PASS / intentionally unchanged

---

## System consistency

PASS

Natal unchanged. Luck Activation unchanged. Luck Interaction unchanged. Annual is a separate refinement inside the luck envelope. Clash ≠ bad event. Combination ≠ good event. Annual Ten God ≠ natal Ten God collection.

---

## Business logic introduced

TEMPORAL ACTIVATION — ANNUAL ONLY

---

## Files changed

- `engines/detailed_interpretation_engine/temporal_activation/__init__.py`
- `engines/detailed_interpretation_engine/temporal_activation/constants.py`
- `engines/detailed_interpretation_engine/temporal_activation/models.py`
- `engines/detailed_interpretation_engine/temporal_activation/facts.py`
- `engines/detailed_interpretation_engine/temporal_activation/labels.py`
- `engines/detailed_interpretation_engine/temporal_activation/evaluate.py`
- `engines/detailed_interpretation_engine/temporal_activation/presentation.py`
- `engines/detailed_interpretation_engine/temporal_activation/engine.py`
- `engines/detailed_interpretation_engine/temporal_activation/validation.py`
- `engines/detailed_interpretation_engine/temporal.py`
- `engines/detailed_interpretation_engine/constants.py`
- `engines/detailed_interpretation_engine/validators.py`
- `engines/detailed_interpretation_engine/diagnostics.py`
- `engines/detailed_interpretation_engine/__init__.py`
- `applications/api/services/luck_truth.py`
- `applications/api/services/orchestrator.py`
- `applications/customer_portal/src/models/dto.ts`
- `applications/customer_portal/src/models/index.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/types.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/luckAdapter.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/luckFixture.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/LuckCard.tsx`
- `applications/customer_portal/src/screens/commercial_dashboard/commercial-dashboard.css`
- `applications/customer_portal/scripts/capture_p7_imp_12_live.py`
- `tests/detailed_interpretation/test_p7_imp_12_temporal_activation.py`
- `implementation/pack_07/P7-IMP-12_diagnostics.json`
- `implementation/pack_07/screenshots/p7_imp_12_*.png`
- `implementation/pack_07/P7-IMP-12_RUNTIME_REPORT.md`

---

## Known limitations

- Monthly / daily / hourly remain `not_evaluated` shells.
- Good Date / date-selection decision logic is out of scope.
- Annual detail is not forced into PDF/DOCX export.
- `luck.annual_identity` is a compact LuckEngine identity stamp for Pack 07; customer UI reads `luck.annual` only.
- Rebuild-from-customer-payload diagnostics can show Wealth natal `weak` while the live orchestrator annual compact keeps natal `fragmented`. Temporal bind itself does not mutate natal Domain state.
- UI-10 L25 ResultStore `empty` vs `current` remains a pre-existing portal test failure.

---

## Next

STOP.

Do not implement Optimization automatically.
Do not implement Narrative Composer.
