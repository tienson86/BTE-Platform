# P7-IMP-05 RUNTIME REPORT

**Task:** P7-IMP-05 — Ten Gods Combination & Ecosystem, live vertical slice  
**Date:** 2026-09-05  
**Status:** PASS

Natal combination + ecosystem only. No Shen Sha, Evidence Priority, domains, luck, temporal, optimization, or narrative composer.

---

## Status

PASS

---

## Combination Engine

Deterministic DI-02 engine consumes P7-IMP-04 natal profiles. Co-presence never becomes `confirmed`. Generation chains may confirm as meaning-modifiers without MC-01 Support. Damage / Rescue families stay `unresolved` with `unresolved_dependency` while MC-01 is unbound. Tài → Quan → Ấn shares one `causal_group`; the two-link findings point at the three-node chain and are not shown separately in customer UI.

---

## Required combinations supported

Frozen V1 IDs (ticket aliases mapped, not stored):

1. `shi_shen_generates_wealth`
2. `shang_guan_generates_wealth`
3. `wealth_generates_officer`
4. `officer_generates_resource` (`officer_generates_seal`)
5. `wealth_officer_resource_chain` (`wealth_officer_seal_chain`)
6. `killer_resource_day_master_chain` (`sha_yin_mutual_generation`)
7. `hurting_officer_meets_officer` (`hurting_officer_attacks_officer`)
8. `owl_robs_food_combination` (`owl_robs_food`)
9. `peer_competes_wealth` (`peer_robs_wealth`)
10. `officer_killer_mixed` (`mixed_officer_killer`)
11. `wealth_exceeds_day_master` (`wealth_overloads_weak_day_master`)
12. `killer_exceeds_day_master` (`killer_overloads_weak_day_master`)
13. `resource_strong_day_master_strong` (`seal_excess_strong_day_master`)
14. `strong_day_master_uses_wealth`
15. `strong_day_master_uses_officer`
16. `strong_day_master_uses_output`
17. `weak_day_master_uses_resource` (`weak_day_master_uses_seal`)
18. `weak_day_master_uses_peer`

---

## Active combinations — CASE-0001

Fresh Analyze, Nguyễn Tiến Sơn 21/01/1987 04:30:

- Tài → Quan → Ấn — Đang hoạt động (`confirmed`, functional)
- Thân vượng dụng Tài — Đang hoạt động
- Thân vượng dụng Quan — Đang hoạt động

Weak but structurally indicated:

- Thương Quan → Tài — Yếu
- Thân vượng dụng Thực/Thương — Yếu

Broken (missing source node):

- Thực Thần → Tài — Chưa hoàn chỉnh

---

## Conditional/unresolved combinations — CASE-0001

MC-01 unbound; no Damage / Rescue IDs created:

- Sát → Ấn → Thân — Chưa đủ dữ liệu để chốt
- Tỷ Kiếp đoạt Tài — Chưa đủ dữ liệu để chốt
- Quan Sát hỗn tạp — Chưa đủ dữ liệu để chốt

Inactive catalog rows are not shown in customer UI.

---

## Ecosystem

Live CASE-0001 customer projection:

| Role | Value |
| --- | --- |
| Driver | Chính Ấn |
| Support | Thất Sát |
| Blocked | Không áp dụng |
| Suppressed | Không áp dụng |
| Excessive | Không áp dụng |
| Deficient | Thực Thương |
| Missing | Không áp dụng |
| Bottleneck | Thiên Tài (weakest link of an active chain) |
| Flow | Thương Quan → Thiên Tài |
| Flow Quality | Bị hạn |

Driver is Pattern primary Chính Ấn, not occurrence count. Bottleneck is bound to an active chain. Missing is not labeled bad.

---

## MC-01 dependency handling

PARTIAL.

MC-01 remains unbound. Generation / use-chains still evaluate from DI-01 evidence. Damage / Rescue combinations stay unresolved. Diagnostics Combination and Ecosystem = **PARTIAL**. No Pack 07 Damage or Rescue IDs.

---

## Runtime binding

`CanonicalRuntimeResult.interpretation.ten_gods.natal`  
`CanonicalRuntimeResult.interpretation.ten_gods.combinations`  
`CanonicalRuntimeResult.interpretation.ten_gods.ecosystem`

Public Analyze stays internal for the full contract. Additive customer projection only:

- `data.ten_gods.detailed`
- `data.ten_gods.relations`
- `data.ten_gods.ecosystem`

---

## Developer diagnostics

`POST /api/v1/dev/pack07/diagnostics` (dev-only). Live CASE:

| Layer | Status |
| --- | --- |
| Contracts | PASS |
| Contexts | PASS |
| Validators | PASS |
| MC-01 | NOT_BOUND |
| Ten Gods | PARTIAL |
| Ten God Combination | PARTIAL |
| Ten Gods Ecosystem | PARTIAL |
| Shen Sha | NOT_IMPLEMENTED |
| Evidence Priority | NOT_IMPLEMENTED |
| Domains | NOT_EVALUATED |
| Luck | NOT_IMPLEMENTED |
| Temporal | NOT_EVALUATED |
| Optimization | NOT_EVALUATED |
| Narrative | NOT_EVALUATED |
| Runtime Contract | PASS |

---

## UI integration

Existing THẬP THẦN card. No second top-level section.

Kept: Lộ rõ placements, Tàng Can names, P7-IMP-04 compact 10-chip detail.

Still bypassed when Pack 07 detailed is present: dictionary commercial cards and combination “Mô hình tạo giá trị”.

Added below natal detail:

- Quan hệ Thập Thần — compact expandable rows of meaningful combinations only
- Hệ Thập Thần — compact ecosystem grid

---

## Visual layout

One-line combination rows with one-at-a-time expand. Ecosystem is a summary grid, not a prose wall. No JSON, no debug IDs, no mixed dictionary + Pack 07 combination truth.

---

## Build

PASS (`python tools/build.py`; `npm run build:result`)

---

## Type Check

PASS (Pack 07 mypy, 46 files)

---

## Tests

- `tests/detailed_interpretation` — **64 passed**
- `tests/ten_gods_engine` — **62 passed**
- Analyze / portal / history / PDF / DOCX (`test_production_readiness`, `test_g2_04_customer_export`, `test_g2_05_history_snapshot`, `test_portal`, `test_integration_api`) — **25 passed** in the combined regression batch with Ten Gods engine (87 passed together)

Unrelated failures not repaired.

---

## Runtime

| Endpoint | Result |
| --- | --- |
| `GET /api/v1/health` | 200 |
| `POST /api/v1/analyze` | 200; pipeline unchanged; `pack07_context` absent; 10 detailed items; relations + ecosystem present |
| `/result` | 200; THẬP THẦN shows natal + Quan hệ + Hệ |
| `/history` | 200 |
| `POST /api/v1/dev/pack07/diagnostics` | 200; Combination PARTIAL, Ecosystem PARTIAL |

---

## Screenshots

- `implementation/pack_07/screenshots/p7_imp_05_result_overview.png`
- `implementation/pack_07/screenshots/p7_imp_05_ten_gods_desktop.png`
- `implementation/pack_07/screenshots/p7_imp_05_combinations.png`
- `implementation/pack_07/screenshots/p7_imp_05_ecosystem.png`
- `implementation/pack_07/screenshots/p7_imp_05_combination_expanded.png`
- `implementation/pack_07/screenshots/p7_imp_05_ten_gods_mobile.png`
- Diagnostics: `implementation/pack_07/P7-IMP-05_diagnostics.json`

---

## PDF

PASS (regression). Pack 07 combinations / ecosystem **intentionally not** exported.

---

## DOCX

PASS (regression). Pack 07 combinations / ecosystem **intentionally not** exported.

---

## History

PASS. No persistence change. `pack07_context` is not stored.

---

## System consistency

PASS.

CASE-0001 Lộ rõ still matches Bát Tự: Năm Thất Sát, Tháng Kiếp Tài, Ngày Nhật Chủ, Giờ Thiên Ấn.

Combination participants reuse P7-IMP-04 identity. Ecosystem consumes combination results. No second Ten Gods identity. No Pattern / Grade mutation.

---

## Business logic introduced

TEN GOD COMBINATION + ECOSYSTEM ONLY

---

## Files changed

Added:

- `engines/detailed_interpretation_engine/ten_gods/combinations/`
- `engines/detailed_interpretation_engine/ten_gods/ecosystem/`
- `tests/detailed_interpretation/test_p7_imp_05_combinations.py`
- `applications/customer_portal/scripts/capture_p7_imp_05_live.py`
- `implementation/pack_07/P7-IMP-05_diagnostics.json`
- screenshots listed above
- `implementation/pack_07/P7-IMP-05_RUNTIME_REPORT.md`

Modified:

- Pack 07 enums, constants, evidence, validators, diagnostics, schema registry, models, public `__init__`
- `engines/detailed_interpretation_engine/ten_gods/engine.py`
- `engines/detailed_interpretation_engine/ten_gods/presentation.py`
- `applications/api/services/orchestrator.py`
- THẬP THẦN adapter / card / types / DTO / CSS / fixture

---

## Known limitations

- MC-01 unbound → Damage / Rescue combinations stay unresolved; diagnostics PARTIAL
- `hurting_officer_meets_officer` / `owl_robs_food_combination` cannot confirm
- Driver unresolved when Pattern does not name a material Ten God
- Combinations / ecosystem not in PDF / DOCX
- History does not persist Pack 07

---

## Next

Do not begin Shen Sha.

Do not begin Domains.

Do not begin Narrative.

STOP and wait for Product Owner review.
