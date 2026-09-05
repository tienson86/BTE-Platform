# P7-IMP-04 RUNTIME REPORT

**Task:** P7-IMP-04 — Ten Gods Detailed Interpretation, first live vertical slice  
**Date:** 2026-09-05  
**Status:** PASS

Natal Ten God interpretation only. No combinations, ecosystem, Shen Sha, Evidence Priority, domains, luck, temporal, optimization, or narrative composer.

---

## Status

PASS

---

## Upstream Ten Gods source

Canonical identity owner:

`engines.ten_gods_engine` via `applications.api.services.ten_gods_truth.shape_ten_gods_payload`

Published facts consumed (not recalculated): `god_id`, Vietnamese label, pillar, stem/hidden stem, visibility, hidden-stem layer (`primary` / `secondary` / `tertiary`), element.

Day Master Strength consumed from `strength.strength_level`. Pattern label consumed from `pattern.cach_cuc` when present. Useful God consumed from `useful_god.useful_ten_god` / element fields when present.

---

## Ten Gods implemented

All 10 canonical IDs:

- `bi_jian` — Tỷ Kiên
- `jie_cai` — Kiếp Tài
- `shi_shen` — Thực Thần
- `shang_guan` — Thương Quan
- `pian_cai` — Thiên Tài
- `zheng_cai` — Chính Tài
- `qi_sha` — Thất Sát (Thiên Quan is display alias only)
- `zheng_guan` — Chính Quan
- `pian_yin` — Thiên Ấn
- `zheng_yin` — Chính Ấn

---

## Evaluation dimensions

Per deity, from available evidence only:

- presence (`absent` / `hidden_only` / `visible` / `visible_and_rooted` + overlays `repeated` / `concentrated` / `structurally_dominant`)
- unflattened visibility (year/month/day/hour stems, main/middle/residual qi)
- root from hidden-stem layer (not invented from count)
- local categorical effective strength (not Day Master Strength, not Pattern Strength)
- structural role (Pattern mention → `primary_pattern`; otherwise capacity support/pressure from consumed Strength, or `neutral` / `unresolved`)
- Day Master band: weak / moderate / strong
- Useful God context only when upstream Useful God is present
- usability: contextual, never good/bad
- structured expression codes (1–3 positive, 0–2 risk) with presentation mapping
- trace `TR-P7-TG-{id}`, evidence IDs, categorical confidence

Identity alone never selects meaning. MC-01 Damage / Rescue are not inferred.

---

## MC-01 dependency handling

PARTIAL.

MC-01 remains unbound. The Ten Gods engine still runs on available BaZi / Strength / Pattern / Useful God facts.

Fields that require MC-01 stay unresolved / empty:

- `damage_ids` / `rescue_ids` empty
- `pattern_context` unresolved when Pattern does not name the deity
- diagnostics Ten Gods = **PARTIAL**
- customer condition: “Chưa gắn Mệnh Cục”

The engine does not simulate MC-01, elect Pattern, change Grade, or create Damage / Rescue / Useful God.

---

## Structured results

`TenGodInterpretationResult` (one per deity) and `TenGodInterpretationCollection` (all 10).

Engine stores codes/enums only. Collection `state` is `partially_resolved` while MC-01 is unbound. Absent deities are explicit `presence_state = absent`, not omitted.

---

## Runtime binding

`CanonicalRuntimeResult.interpretation.ten_gods.natal`

`InterpretationSection.status` follows the Ten God collection. Shen Sha, Evidence Priority, domains, temporal, optimization, and narrative remain not_evaluated / not_implemented.

Full Pack 07 contract stays internal (`pack07_context` stripped from public Analyze JSON).

Customer-safe projection only:

`data.ten_gods.detailed` — names, status/role labels, short expression phrases. No traces, no raw IDs, no JSON dump.

---

## Developer diagnostics

Mechanism: `GET` / `POST /api/v1/dev/pack07/diagnostics` (dev-only, production 404).

Live POST after Analyze (CASE Nguyễn Tiến Sơn):

| Field | Status |
| --- | --- |
| Contracts | PASS |
| Contexts | PASS |
| Validators | PASS |
| MC-01 Reference | NOT_BOUND |
| Ten Gods | PARTIAL |
| Shen Sha | NOT_IMPLEMENTED |
| Evidence Priority | NOT_IMPLEMENTED |
| Domains | NOT_EVALUATED |
| Luck | NOT_IMPLEMENTED |
| Temporal | NOT_EVALUATED |
| Optimization | NOT_EVALUATED |
| Narrative | NOT_EVALUATED |
| Runtime Contract | PASS |
| overall_status | PASS |

Artifact: `implementation/pack_07/P7-IMP-04_diagnostics.json`

---

## UI integration

Existing THẬP THẦN card on `/result` (`TenGodsCard`).

Preserved:

- Lộ rõ pillar placements (canonical identity)
- Tàng Can supporting names
- Bát Tự pillar Thập Thần row (unchanged identity facts)

Replaced / bypassed when Pack 07 `detailed` is present:

- dictionary commercial cards (`tenGodsCommercialAssets`)
- combination “Mô hình tạo giá trị” (`tenGodsCombinationAssets`)

Those dictionary surfaces remain as fallback when `detailed` is absent, so older fixtures still bind.

New: compact 10-chip grid “Luận giải chi tiết” + one-at-a-time expand (role, 1–3 positives, 0–2 risks, conditions). Unresolved uses “Chưa đủ dữ liệu để kết luận chi tiết”.

---

## Visual layout

Compact chip grid, not ten prose walls. No raw JSON, no trace IDs, no duplicate dictionary + Pack 07 interpretation. Identity lists stay below the detailed grid.

---

## Build

PASS (`python tools/build.py`)

Portal result bundle: `npm run build:result` PASS.

---

## Type Check

PASS — Pack 07 scoped mypy, 35 files, no issues.

---

## Tests

Pack 07 (`tests/detailed_interpretation`): **41 passed**, 0 failed.

Existing Ten Gods engine (`tests/ten_gods_engine`): **62 passed**.

Regression (Analyze / portal / history / PDF / DOCX): **22 passed**.

Unrelated failures not repaired.

---

## Runtime

| Endpoint | Result |
| --- | --- |
| `GET /api/v1/health` | 200 |
| `POST /api/v1/analyze` | 200; pipeline unchanged; `pack07_context` absent; `ten_gods.detailed` has 10 items, `partially_resolved` |
| `/result` | 200; THẬP THẦN shows Pack 07 detailed grid |
| `/history` | 200 |
| `POST /api/v1/dev/pack07/diagnostics` | 200; Ten Gods PARTIAL |

---

## Screenshots

- `implementation/pack_07/screenshots/p7_imp_04_result_overview.png`
- `implementation/pack_07/screenshots/p7_imp_04_ten_gods_desktop.png`
- `implementation/pack_07/screenshots/p7_imp_04_ten_gods_expanded.png`
- `implementation/pack_07/screenshots/p7_imp_04_ten_gods_mobile.png`
- Diagnostics: `implementation/pack_07/P7-IMP-04_diagnostics.json`

---

## PDF

PASS (regression). Pack 07 Ten Gods detailed is **intentionally not** forced into PDF.

---

## DOCX

PASS (regression). Pack 07 Ten Gods detailed is **intentionally not** forced into DOCX.

---

## History

PASS. `pack07_context` is not persisted. History tests unchanged. `ten_gods.detailed` is an additive Analyze field only.

---

## System consistency

PASS.

CASE-0001 / Nguyễn Tiến Sơn:

- Bát Tự Thập Thần: Năm Thất Sát, Tháng Kiếp Tài, Ngày Nhật Chủ, Giờ Thiên Ấn
- Pack 07 Lộ rõ matches those labels
- Detailed grid uses the same canonical names; no second identity, no `thien_quan`

---

## Business logic introduced

TEN GODS INTERPRETATION ONLY

---

## Files changed

Added:

- `engines/detailed_interpretation_engine/ten_gods/` (`constants`, `models`, `facts`, `evaluate`, `engine`, `presentation`, `__init__`)
- `tests/detailed_interpretation/test_p7_imp_04_ten_gods.py`
- `applications/customer_portal/scripts/capture_p7_imp_04_live.py`
- `implementation/pack_07/P7-IMP-04_diagnostics.json`
- screenshots listed above
- `implementation/pack_07/P7-IMP-04_RUNTIME_REPORT.md`

Modified:

- `engines/detailed_interpretation_engine/enums.py`
- `engines/detailed_interpretation_engine/constants.py`
- `engines/detailed_interpretation_engine/evidence.py`
- `engines/detailed_interpretation_engine/schema_registry.py`
- `engines/detailed_interpretation_engine/validators.py`
- `engines/detailed_interpretation_engine/diagnostics.py`
- `engines/detailed_interpretation_engine/engine.py`
- `engines/detailed_interpretation_engine/service.py`
- `engines/detailed_interpretation_engine/models.py`
- `engines/detailed_interpretation_engine/__init__.py`
- `applications/api/services/orchestrator.py`
- `applications/customer_portal/src/models/dto.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/types.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/tenGodsAdapter.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/TenGodsCard.tsx`
- `applications/customer_portal/src/screens/commercial_dashboard/tenGodsFixture.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/commercial-dashboard.css`

Frozen knowledge documents: not modified.

---

## Known limitations

- MC-01 unbound → Ten Gods diagnostics PARTIAL; Damage/Rescue never attached.
- `structurally_dominant` only if upstream dominance IDs are published; public `ten_gods` payload does not currently include dominance.
- Combinations, ecosystem, Shen Sha, domains, luck, optimization, narrative remain unimplemented.
- PDF/DOCX do not include Pack 07 detailed Ten Gods (intentional).
- Expression copy is a small presentation map, not DI-19 Narrative Composer.
- Role labels use the ticket’s Primary / Support / Pressure / Neutral set.

---

## Next

Do not assume P7-IMP-05.

Wait for Product Owner review.

STOP.
