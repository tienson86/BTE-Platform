# P7-IMP-14 NARRATIVE COMPOSER RUNTIME REPORT

**Task:** P7-IMP-14 — Narrative Composer Engine — live customer narrative  
**Date:** 2026-09-05  
**Case:** CASE-0001 · Nguyễn Tiến Sơn · male · 21/01/1987 04:30 · Hà Nội

Composer consumes Pack 07 truth. It does not create natal, luck, interaction, temporal, optimization, Ten Gods, Shen Sha, or MC-01 truth. Export and History persistence were not implemented.

---

## Status

PASS

## Narrative Graph

`NarrativeGraph` is bound on `CanonicalRuntimeResult.narrative` (`NarrativeSection.graph` + `NarrativeResult`).

Nodes used: `executive_summary`, `strength`, `risk`, `opportunity`, `domain_section`, `temporal`, `action`, `closing_summary`.

Edges used: `supports`, `explains`, `qualifies`, `contrasts`, `expands`, `summarizes`.

Career and Vitality domain nodes are linked with `contrasts` so opportunity and overload stay both visible.

Schema: `bte.detailed_interpretation.composer.v1`.  
Ruleset: `bte.detailed_interpretation.composer.rules.v1`.

Customer stamp: `payload["detailed_narrative"]` from `present_narrative_customer`. ReportEngine `payload["narrative"]` is not overwritten.

---

## Executive Summary

6–10 sentences from MC-01 identity plus P0/P1 Evidence Priority labels and the Optimization top action.

Live orchestrator CASE-0001:

Lá số này thuộc mệnh cục Chính Ấn, hạng B. Tính toàn vẹn cấu trúc hiện Hỗn hợp. Trọng tâm hiện tại là Thiên Tài. Trọng tâm hiện tại là Ấn quá vượng kìm biểu đạt. Trọng tâm hiện tại là Tạo tài yếu. Trọng tâm hiện tại là Tỷ Kiếp đoạt Tài. Trọng tâm hiện tại là Học thuật · Khởi nghiệp · Quản trị. Trọng tâm hiện tại là Tích lũy khá. Ưu tiên hành động: Giữ kỷ luật vốn.

Pattern/grade/integrity appear once in the identity sentences. They are not repeated as Top Strengths.

---

## Top Strengths

Consumed from Evidence Priority. Not a template list.

Live: Học thuật · Khởi nghiệp · Quản trị (P1 achievement).

---

## Top Risks

Consumed from Evidence Priority damage / wealth / leakage.

Live:

- Thiên Tài (P0 wealth bottleneck)
- Ấn quá vượng kìm biểu đạt (P1 damage)
- Tạo tài yếu (P1 wealth)
- Tài vận: rò rỉ Tạo tài (domain leakage)

---

## Top Opportunities

Consumed from Evidence Priority opportunity / wealth / career.

Live: Tích lũy khá (P1 wealth).

---

## Six Domains

All six published natal domains are present. Ranked Evidence Priority order first, remaining mains appended. No rerank.

| Domain | State | Driver / bottleneck / opportunity notes |
|---|---|---|
| Quyền hạn | Có điều kiện | Áp lực quyền hạn; uy tín chuyên môn |
| Tài vận | Phân mảnh | Bottleneck already named above; biến động tài cao; kỷ luật giữ tài |
| Sự nghiệp | Có điều kiện | Bottleneck already named; năng lực học thuật |
| Quan hệ | Phân mảnh | Khe hở giao tiếp |
| Di sản | Có điều kiện | Truyền tri thức |
| Sinh lực | Có điều kiện | Quá tải căng thẳng; kỷ luật phục hồi |

Career opportunity and Vitality overload remain both visible. No averaging.

---

## Luck Summary

- Đại vận hiện tại: 2022–2031
- Quan hệ / Sinh lực dormant in this window
- Quyền hạn hỗ trợ Sự nghiệp
- Sự nghiệp dồn nguồn lực / chuyển áp lực Sinh lực
- Sự nghiệp xung đột Tài vận
- Năm 2026 adjusts expression inside the luck window; natal background is unchanged
- Explicit non-event wording: not an event forecast

---

## Action Summary

Consumed only from `LifeOptimizationResult`. Live orchestrator Top 3 matches P7-IMP-13:

1. Giữ kỷ luật vốn — P0 wealth, natal long-term  
2. Kiểm soát khối lượng việc — P1 career, current year  
3. Phục hồi năng lực bền — P1 vitality, current luck cycle  

One extra long-term authority pressure action is appended because it is not already in Top 3. Duplicate recommended-action keys are not repeated.

---

## Closing Summary

Action-oriented. No new evidence.

Live: giữ thứ tự — xử lý nút thắt trước, rồi mở rộng — then the Top 3 titles.

---

## Runtime binding

`CanonicalRuntimeResult.narrative` is the single Pack 07 narrative root.

`interpret_and_bind_narrative` replaces only `runtime.narrative` and `context.narrative`. Domains, temporal, interpretation, and optimization object identity is unchanged.

---

## Diagnostics

Live POST `/api/v1/dev/pack07/diagnostics` CASE-0001:

| Layer | Status |
|---|---|
| Contracts | PASS |
| Contexts | PASS |
| Validators | PASS |
| MC-01 | PASS |
| Ten Gods / Combinations / Ecosystem | PASS |
| Shen Sha | PASS |
| Shen Sha ecosystem | PARTIAL (pre-existing; not owned by Composer) |
| Evidence Priority | PASS |
| Domains | PASS |
| Luck / Interaction / Temporal | PASS |
| Optimization | PASS |
| Narrative | PASS |
| Runtime | PASS |
| Overall | PASS |

Empty GET `/api/v1/dev/pack07/diagnostics`: Narrative `NOT_EVALUATED`.

---

## Build

PASS. `npm run build:result` succeeded inside the live capture.

## Type Check

PASS. Pack 07 scoped mypy: **120 source files**, no issues.

`python -m mypy --explicit-package-bases --follow-imports=skip engines/detailed_interpretation_engine applications/api/contracts/pack07_runtime.py applications/api/routes/pack07_dev.py`

Portal `tsc --noEmit` still reports pre-existing errors outside this ticket (`luckAdapter`, report view models, unused imports). Not repaired.

## Tests

| Suite | Result |
|---|---|
| `tests/detailed_interpretation` | **225 passed** |
| `test_p7_imp_14_narrative_composer.py` | **11 passed** |
| Portal vitest `p7_imp_14_narrative` + `ui11_interpretation` + `ui12_action_plan` | **42 passed** |
| PDF renderer/exporter | PASS / unchanged |
| DOCX renderer/exporter | PASS / unchanged |
| History snapshot + portal history | PASS / unchanged |

Negative tests: narrative does not mutate Pattern, Grade, Domain, or Action objects. Compact has no `TR-P7-` / `E-DI-` and no forbidden advice tokens.

Metamorphic: reverse Optimization top-priority order → narrative action text changes. Change Wealth bottleneck → domain narrative changes. Patch `WHO_TEMPLATE` only → domains/optimization truth unchanged.

## Runtime

- `GET /api/v1/health` — 200 ok
- `POST /api/v1/analyze` CASE-0001 — 200, `data.detailed_narrative` present, six domains, Top 3 actions
- `/result` — `data-int-composer=true` inside existing LUẬN GIẢI TỔNG THỂ card
- `/history` — 200, no persistence change
- `GET /api/v1/dev/pack07/diagnostics` — Narrative NOT_EVALUATED
- `POST /api/v1/dev/pack07/diagnostics` — Narrative PASS

## Screenshots

- `implementation/pack_07/screenshots/p7_imp_14_result_overview.png`
- `implementation/pack_07/screenshots/p7_imp_14_executive.png`
- `implementation/pack_07/screenshots/p7_imp_14_strength.png`
- `implementation/pack_07/screenshots/p7_imp_14_risk.png`
- `implementation/pack_07/screenshots/p7_imp_14_opportunity.png`
- `implementation/pack_07/screenshots/p7_imp_14_domains.png`
- `implementation/pack_07/screenshots/p7_imp_14_luck.png`
- `implementation/pack_07/screenshots/p7_imp_14_action.png`
- `implementation/pack_07/screenshots/p7_imp_14_closing.png`
- `implementation/pack_07/screenshots/p7_imp_14_mobile.png`
- `implementation/pack_07/screenshots/p7_imp_14_diagnostics.png`

Proof dump: `implementation/pack_07/P7-IMP-14_diagnostics.json`

## PDF

PASS / intentionally unchanged

## DOCX

PASS / intentionally unchanged

## History

PASS / intentionally unchanged

## System consistency

PASS

Evidence Priority P0/P1 → domain bottleneck/leakage → luck interaction → Optimization Top 3 → Narrative blocks. Composer does not rerank. Internal traces exist. Customer compact strips traces and IDs.

## Business logic introduced

NONE

Narrative composition and catalog wording only. No new analytical findings.

## Files changed

- `engines/detailed_interpretation_engine/narrative.py` (`NarrativeBlock`, `NarrativeResult.luck` / `blocks`)
- `engines/detailed_interpretation_engine/constants.py` (`NARRATIVE_COMPOSER_RULESET_VERSION`)
- `engines/detailed_interpretation_engine/narrative_composer/` (`__init__.py`, `constants.py`, `facts.py`, `labels.py`, `evaluate.py`, `presentation.py`, `engine.py`, `validation.py`)
- `engines/detailed_interpretation_engine/models.py` (`NarrativeBlock` export)
- `engines/detailed_interpretation_engine/diagnostics.py`
- `engines/detailed_interpretation_engine/validators.py`
- `applications/api/services/orchestrator.py`
- `applications/customer_portal/src/models/dto.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/types.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/narrativeComposerAdapter.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/InterpretationCard.tsx`
- `applications/customer_portal/src/screens/commercial_dashboard/CommercialDashboardPage.tsx`
- `applications/customer_portal/src/screens/commercial_dashboard/index.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/commercial-dashboard.css`
- `applications/customer_portal/scripts/capture_p7_imp_14_live.py`
- `applications/customer_portal/tests/js/p7_imp_14_narrative.test.tsx`
- `tests/detailed_interpretation/test_p7_imp_14_narrative_composer.py`
- `tests/detailed_interpretation/test_p7_imp_12_temporal_activation.py` (live Narrative diagnostic expected PASS)
- `tests/detailed_interpretation/test_p7_imp_13_life_optimization.py` (live Narrative diagnostic expected PASS)
- `implementation/pack_07/P7-IMP-14_RUNTIME_REPORT.md`
- `implementation/pack_07/P7-IMP-14_diagnostics.json`

## Known limitations

- `evaluate.py` is longer than the 500-line recommendation (680 lines).
- Strength list on this chart is thin because P0 identity findings are reserved for the executive sentences.
- Luck dormant states copy the Luck Activation label (`Ngủ`) without extra prose.
- Rebinding Composer from the public analyze payload can still diverge from the orchestrator compact (same IMP-13 public-payload caveat). Live orchestrator `detailed_narrative` is the customer source of truth.
- Shen Sha ecosystem remains PARTIAL on this case; Composer does not own that layer.
- Portal `tsc --noEmit` still has pre-existing errors outside this ticket.
- UI-10 L25 ResultStore empty/current remains pre-existing.

## Next

STOP.

Do not implement Export.  
Do not implement History persistence.  
Wait for Product Owner approval.
