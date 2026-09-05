# P7-IMP-13 LIFE OPTIMIZATION RUNTIME REPORT

**Task:** P7-IMP-13 / P7-IMP-13C — Life Optimization Engine — live Action Plan vertical slice and final acceptance  
**Date:** 2026-09-05  
**Case:** CASE-0001 · Nguyễn Tiến Sơn · male · 21/01/1987 04:30 · Hà Nội

Optimization consumes truth. It does not create natal, luck, interaction, temporal, Useful God, temperature, five-element, Ten Gods, or Shen Sha truth. Narrative Composer was not implemented.

---

## Status

PASS

## Optimization model

Frozen findings are consumed into `OptimizationAction` keys. Evidence Priority supplies the tier floor; the engine does not rerank DI-07. Inside a floor, category order is saturation / critical risk / leakage / bottleneck / Useful God function.

Natal and temporal plans are distinct objects. Actions are not written into Domain or Temporal results.

Bind path: `CanonicalRuntimeResult.optimization`. Schema: `bte.detailed_interpretation.life_optimization.v1`. Ruleset: `bte.detailed_interpretation.life_optimization.rules.v1`.

Customer stamp: `payload["optimization"]` from `present_life_optimization_customer`.

---

## Top 3 actions

Live orchestrator CASE-0001. Rank is Evidence Priority floor first, then category. Not template domain order (Authority → Career → Wealth).

### Ưu tiên 1 — Giữ kỷ luật vốn

| Field | Live value |
|---|---|
| Action | `opt.wealth.retain_capital_discipline` · Giữ kỷ luật vốn |
| Target | Tài / capital_discipline |
| Reason | Tài biến động cao, cần bảo vệ giữ vốn (`wealth.volatility_high`) |
| Evidence source | Domain Wealth P0 · leakage `creation` · bottleneck Thiên Tài · volatility `above_average` · retention/accumulation stronger than creation |
| Evidence Priority | `E-DI-EPR-004` P0 `ecosystem.bottleneck` · `E-DI-EPR-006` P1 `wealth:financial_volatility` · `E-DI-EPR-007` P1 `wealth:wealth_creation` · `E-DI-EPR-011/012` retention/accumulation |
| Condition | Không phải khuyến nghị giao dịch cụ thể |
| Scope | Dài hạn |

### Ưu tiên 2 — Kiểm soát khối lượng việc

| Field | Live value |
|---|---|
| Action | `opt.career.protect_workload.current_annual` · Kiểm soát khối lượng việc |
| Target | Sự nghiệp / workload_control |
| Reason | Sự nghiệp đang quá tải, cần kiểm soát trước khi mở rộng |
| Evidence source | Luck + Annual saturation `overloaded` · natal bottleneck Ấn quá vượng kìm biểu đạt · career_pressure elevated |
| Evidence Priority | `E-DI-EPR-013` P1 `career.drivers` |
| Condition | Không tăng khối lượng việc khi đang quá tải |
| Scope | Năm hiện tại 2026 |

### Ưu tiên 3 — Phục hồi năng lực bền

| Field | Live value |
|---|---|
| Action | `opt.vitality.recover_capacity.current_luck_cycle` · Phục hồi năng lực bền |
| Target | Sinh lực / recovery |
| Reason | Sự nghiệp đang chuyển áp lực sang sinh lực |
| Evidence source | Luck Interaction `DI-10-career-vitality-stress_transfer` · natal leakage `stress` · recovery moderate |
| Evidence Priority | vitality/capacity P1 combination and condition findings (`E-DI-EPR-008` …) |
| Condition | Không phải lời khuyên y khoa |
| Scope | Vận hiện tại 2022–2031 |

Trace chain for each item: Evidence Priority → Domain finding → Bottleneck / Leakage / Temporal stress → Optimization target → Action.

---

## Natal plan

Dài hạn. Action IDs disjoint from temporal.

- Tài: giữ kỷ luật vốn; hạn chế mở rộng
- Quan hệ: tăng chất lượng giao tiếp
- Sinh lực: bảo vệ phục hồi
- Sự nghiệp: hỗ trợ chức năng hành (Useful God function, not decorative)

## Temporal plan

Vận hiện tại / Năm 2026. Luck window 2022–2031. Does not rewrite natal.

- Quyền lực: kiểm soát áp lực quyền; không tăng thêm quyền/trách nhiệm (luck + annual overload)
- Sự nghiệp: kiểm soát khối lượng việc; không tăng khối lượng việc (luck + annual overload)
- Sinh lực: phục hồi năng lực bền (career → vitality stress transfer)

Metamorphic: changing only annual identity keeps natal action IDs identical (`test_annual_change_keeps_natal_plan`).

---

## Authority plan

Conditional. Luck/Annual overloaded. Target: quá tải áp lực quyền hạn. Action: kiểm soát áp lực quyền. Caution: không tăng thêm quyền/trách nhiệm. Condition: không tăng thêm quyền khi đang quá tải.

## Career plan

Conditional. Bottleneck: Ấn quá vượng kìm biểu đạt. Conversion: skill → role. Natal expansion blocked by saturation. Temporal: kiểm soát khối lượng việc. Caution: không tăng khối lượng việc.

## Wealth plan

Fragmented / P0. Creation weak, retention/accumulation stronger, volatility high, leakage `creation`. Target/action: giữ kỷ luật vốn. Caution: hạn chế mở rộng. Condition: not a specific trade recommendation. No investment picks.

## Relationship plan

Fragmented. Driver: giao tiếp. Bottleneck: khe hở giao tiếp. Leakage: communication. Action: tăng chất lượng giao tiếp. No marriage prediction.

## Legacy plan

Conditional. No transmission leakage on this live chart. No invented develop-transmission action. Leakage-first: not_applicable.

## Vitality plan

Conditional. Driver: bền bỉ. Leakage: stress. Natal: bảo vệ phục hồi. Temporal: phục hồi năng lực bền from career → vitality stress. Condition: không phải lời khuyên y khoa.

---

## Bottleneck-first

PASS

Wealth volatility / Thiên Tài bottleneck outranks “increase creation”. Overloaded Career does not add workload. Vitality recovery/stress is protected rather than adding capacity demand.

## Leakage-first

PASS

| Domain | Leakage | Result |
|---|---|---|
| Wealth | creation + high volatility | retain/avoid expansion before output growth |
| Relationship | communication | develop communication |
| Legacy | none | not_applicable |
| Vitality | stress | protect recovery before more demand |

## Saturation / overload guard

PASS

Authority Luck = overloaded. Career Luck = overloaded. Annual 2026 strengthens both envelopes. Emitted keys contain protect/avoid only. Absent: `strengthen_workload`, `increase_output`, `expand_responsibility`, investment keys.

## Cross-domain conflicts

- Career ↔ Vitality — Sự nghiệp cần đầu ra, sinh lực cần phục hồi. Resolution: keep both; do not silently choose. Severity: high. Source: Luck Interaction stress transfer.
- Career ↔ Wealth — Cần cân bằng giữa hai hướng. Resolution: conditional balance. Severity: high. Source: Luck Interaction conflict.

Authority → Career support is consumed as a Luck Interaction finding and is not flattened into a single recommendation. It is support, not a conflict.

## Useful God functional plan

Chính Quan. Functions: activation, warmth, visibility, communication, leadership expression. Domains: sự nghiệp, quyền lực, tài. Kỵ (Tỷ Kiên, Kiếp Tài) is avoidance of reinforcement, not a total ban. No wear-red / object / direction advice.

## Five Element functional plan

Hỏa. Current role: useful_god. Desired role: functional_support. Direction: cần tăng chức năng. Reason: hỗ trợ chức năng hành, không thêm hành theo số đếm. Low element does not auto-add.

## Function-first boundary

PASS

## Safety boundaries

PASS

Customer compact and `/result` contain none of: medical diagnosis/treatment/medication, specific securities, buy/sell, leverage, guaranteed outcome, marriage prediction, promotion prediction.

## Natal immutability

PASS

MC-01, Ten Gods, Combinations, Ecosystem, Shen Sha, Evidence Priority, Domains unchanged after optimization bind. Object identity preserved for luck/interaction/temporal.

## Temporal immutability

PASS

Luck Activation, Luck Interaction, and Temporal Activation objects are unchanged after optimization. Temporal actions do not rewrite natal.

## Runtime binding

`CanonicalRuntimeResult.optimization`

Customer: `payload["optimization"]`. No duplicate customer-side optimization root. No actions written into Domain or Temporal objects.

## Developer diagnostics

Live CASE-0001 POST `/api/v1/dev/pack07/diagnostics`:

| Layer | Status |
|---|---|
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
| Optimization | PASS |
| Narrative | NOT_EVALUATED |
| Runtime Contract | PASS |

Empty GET `/api/v1/dev/pack07/diagnostics`: Optimization `NOT_EVALUATED`.

## UI integration

Existing card title remains **KẾ HOẠCH HÀNH ĐỘNG**. Inner subtitle **KẾ HOẠCH TỐI ƯU**.

Visible: Top 3, NÊN PHÁT HUY, CẦN CẢI THIỆN, CẦN KIỂM SOÁT, NÊN TRÁNH / HẠN CHẾ, THEO VẬN HIỆN TẠI, Dài hạn vs Vận hiện tại / Năm 2026, Cần cân bằng, expandable six domains (Target / Why / Action / Condition / Caution), Chức năng Dụng thần, Chức năng ngũ hành.

No trace IDs, raw engine IDs, JSON, or debug copy on `/result`.

## Build

PASS (`python tools/build.py` — compileall applications, tools, engines)

## Type Check

PASS. Pack 07 scoped mypy: **112 source files**, no issues.

`python -m mypy --explicit-package-bases --follow-imports=skip engines/detailed_interpretation_engine applications/api/contracts/pack07_runtime.py applications/api/routes/pack07_dev.py`

## Tests

| Suite | Result |
|---|---|
| `tests/detailed_interpretation` | 214 collected, included in combined run |
| `test_p7_imp_13_life_optimization.py` | **18 passed** |
| Luck contract + G1-08 + PDF + DOCX + History | included |
| Combined pytest (detailed_interpretation + luck contract + G1-08 + PDF renderer/exporter + DOCX renderer/exporter + history snapshot + portal history) | **238 passed** |
| Portal vitest `p7_imp_13_optimization` + `ui12_action_plan` | **23 passed** |

Metamorphic tests re-run inside IMP-13: bottleneck urgency, volatility removal, recovery urgency, annual-only natal identity.

## Transient failures resolved

- StressTransfer field rename: `from_domain`/`to_domain` → `source_domain`/`target_domain`. Pack 07 mypy 112 files PASS.
- UI-12 A13 / expand mid-binding failures. Final IMP-13 + UI-12: 23 passed.

## Pre-existing unrelated failures

UI-10 L25 ResultStore `empty` vs `current`.

introduced by P7-IMP-13: **NO**

Not repaired in P7-IMP-13C.

## Runtime

- `GET /api/v1/health` — 200 ok
- `POST /api/v1/analyze` CASE-0001 — 200, `data.optimization` present, Top 3 present
- `/result` — live Action Plan (`data-ap-opt=true`)
- `/history` — 200, no persistence change
- `GET /api/v1/dev/pack07/diagnostics` — Optimization NOT_EVALUATED
- `POST /api/v1/dev/pack07/diagnostics` — Optimization PASS

## Screenshots

- `implementation/pack_07/screenshots/p7_imp_13_result_overview.png`
- `implementation/pack_07/screenshots/p7_imp_13_top3.png`
- `implementation/pack_07/screenshots/p7_imp_13_natal_plan.png`
- `implementation/pack_07/screenshots/p7_imp_13_temporal_plan.png`
- `implementation/pack_07/screenshots/p7_imp_13_career_expanded.png`
- `implementation/pack_07/screenshots/p7_imp_13_wealth_expanded.png`
- `implementation/pack_07/screenshots/p7_imp_13_vitality_expanded.png`
- `implementation/pack_07/screenshots/p7_imp_13_career_vitality_conflict.png`
- `implementation/pack_07/screenshots/p7_imp_13_useful_god_five_element.png`
- `implementation/pack_07/screenshots/p7_imp_13_five_element.png`
- `implementation/pack_07/screenshots/p7_imp_13_mobile_optimization.png`
- `implementation/pack_07/screenshots/p7_imp_13_diagnostics.png`

Proof dump: `implementation/pack_07/P7-IMP-13_diagnostics.json`

## PDF

PASS / intentionally unchanged

## DOCX

PASS / intentionally unchanged

## History

PASS / intentionally unchanged

## System consistency

PASS

Evidence Priority floor → domain bottleneck/leakage/saturation → optimization target → action. Internal traces exist. Customer compact strips traces.

## Business logic introduced

LIFE OPTIMIZATION ONLY

## Files changed

- `engines/detailed_interpretation_engine/life_optimization/` (`__init__.py`, `constants.py`, `models.py`, `facts.py`, `evaluate.py`, `labels.py`, `presentation.py`, `engine.py`, `validation.py`)
- `engines/detailed_interpretation_engine/optimization.py`
- `engines/detailed_interpretation_engine/constants.py`
- `engines/detailed_interpretation_engine/diagnostics.py`
- `engines/detailed_interpretation_engine/validators.py`
- `applications/api/services/orchestrator.py`
- `applications/customer_portal/src/models/dto.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/ActionPlanCard.tsx`
- `applications/customer_portal/src/screens/commercial_dashboard/actionPlanAdapter.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/CommercialDashboardPage.tsx`
- `applications/customer_portal/src/screens/commercial_dashboard/types.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/cards.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/commercial-dashboard.css`
- `applications/customer_portal/src/screens/commercial_dashboard/index.ts`
- `applications/customer_portal/scripts/capture_p7_imp_13_live.py`
- `applications/customer_portal/tests/js/p7_imp_13_optimization.test.tsx`
- `tests/detailed_interpretation/test_p7_imp_13_life_optimization.py`
- `tests/detailed_interpretation/test_p7_imp_12_temporal_activation.py` (live Optimization diagnostic expected PASS)
- `implementation/pack_07/P7-IMP-13_RUNTIME_REPORT.md`
- `implementation/pack_07/P7-IMP-13_diagnostics.json`

P7-IMP-13C only: domain-detail fallback from temporal when natal recommended is empty; visible Useful God functional block; extra Career/Vitality/function-plan screenshots; this report closure.

## Known limitations

- `evaluate.py` is longer than the 500-line recommendation.
- Luck/annual protect actions are duplicated per layer to keep scopes distinct.
- Legacy domain card is unresolved on this live chart because leakage/evidence does not support transmission.
- Public analyze payload is customer-stripped; rebinding optimization from that payload can miss wealth volatility. Live orchestrator compact is the source of truth.
- Customer compact can still include conversion codes (`skill_to_role`) in domain metadata.
- UI-10 L25 ResultStore empty/current remains pre-existing.

## Next

STOP.

Do not implement Narrative Composer.  
Do not begin P7-IMP-14.  
Wait for Product Owner approval.
