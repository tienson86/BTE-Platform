# P7-IMP-11 LUCK INTERACTION RUNTIME REPORT

**Task:** P7-IMP-11 — Luck Interaction Engine — live vertical slice  
**Date:** 2026-09-05  
**Status:** PASS

Live CASE-0001: Nguyễn Tiến Sơn, male, 21/01/1987 04:30, Hà Nội.

Activation → Interaction → Life Situation. Interaction consumes natal DomainGraph, Luck Activation, Evidence Priority, and MC-01 refs. It does not recalculate Đại Vận and does not rewrite natal Domain or Luck Activation.

Annual / Monthly / Daily / Hourly Temporal Activation, Life Optimization, and Narrative Composer were not implemented.

---

## Status

PASS

Luck Interaction Engine publishes a separate temporal projection onto `CanonicalRuntimeResult.temporal.luck_interaction`. Schema: `bte.detailed_interpretation.luck_interaction.v1`. Ruleset: `bte.detailed_interpretation.luck_interaction.rules.v1`.

---

## Current Luck cycle

Canonical LuckEngine current cycle, reused from P7-IMP-10. Not recalculated.

- Pillar: **Ất Tỵ**
- Stem / branch: Ất / Tỵ
- Time window: **2022–2031**
- Age window: 35–44
- Index: 3
- Cycle id: `dai_van:3:ẤtTỵ`

Live activation consumed (unchanged by interaction):

| Domain | Natal | Activation |
| --- | --- | --- |
| Authority | conditional | overloaded |
| Career | conditional | overloaded |
| Wealth | fragmented | conditional |
| Relationship | fragmented | dormant |
| Legacy | conditional | conditional |
| Vitality | conditional | dormant |

---

## Interaction Graph

DI-10 graph: activated domain ↔ activated domain. Nodes are the current Luck Activation domain ids. Edges require evidence and a natal DomainGraph relation. No luck-cycle → domain edges (those remain DI-09).

Live CASE-0001 evidenced edges:

| Source | Relation | Target | Finding type |
| --- | --- | --- | --- |
| authority | supports | career | support |
| career | depends_on | vitality | resource_shift |
| career | stresses | vitality | stress_transfer |
| career | conflicts | wealth | conflict |

Career → Vitality pressure exists only because natal DomainGraph already has `vitality supports career`. It is not an automatic Career High → Vitality stress rule.

---

## Life Situation

`resource_pressure` / **Áp lực tăng trưởng**

`temporality=window_bound`. Descriptive of this luck window. Not fate and not a new natal Domain state.

---

## Interaction Driver

`career` / **Sự nghiệp**

Activated domain with the strongest downstream effect this window. Distinct from Pattern Driver, Ten Gods Driver, natal Domain Driver (`hybrid` / `mixed` / `communication` / `resilience`), and Activation Driver (`temporal_wealth`).

---

## Interaction Bottleneck

`vitality` / **Sức bền**

Graph limiter: Career overload depends on / stresses Vitality capacity. Does not rewrite natal bottleneck text.

---

## Support interactions

- Authority → Career, `support`, high. Natal edge `authority:supports:career`. Opportunity: Quyền hạn hỗ trợ Sự nghiệp.

---

## Conflict interactions

- Career → Wealth, `conflict`, high. Natal edge `career:conflicts:wealth`. Both activations kept. No averaging.

No Wealth ↔ Relationship conflict: natal DomainGraph has no such edge.

---

## Trade-offs

None on this chart. Career and Wealth are both engaged/loud, so the natal conflict stays a conflict rather than a directional trade-off.

---

## Stress transfers

- Career → Vitality, `stress_transfer`, high. Evidence: natal `vitality supports career` plus Career overloaded. Condition: Áp lực nghề nghiệp cần kiểm soát sức bền biểu đạt. Not a diagnosis.

---

## Blocked expressions

None on this chart. No loud-source / quiet-target pair on a natal support edge produced `blocked_expression`.

---

## Highest opportunity

Authority supports Career — **Quyền hạn hỗ trợ Sự nghiệp**.

---

## Highest risk

Career stress transfer onto Vitality — **Sự nghiệp chuyển áp lực sang Sức bền**.

---

## Natal immutability

PASS

Snapshot of MC-01, Evidence Priority, natal Domains, Ten Gods, Shen Sha before Interaction equals after Interaction. Domain state / driver / bottleneck unchanged.

---

## Luck Activation immutability

PASS

`luck_activation` object identity is preserved through `bind_luck_interaction`. Cycle id, time window, and per-domain activation states remain identical.

---

## Runtime binding

`CanonicalRuntimeResult.temporal.luck_interaction`

Customer compact stamp: `payload["luck"]["interaction"]` on the existing Đại Vận object. Interaction fields are not written onto natal DomainResult or LuckActivationResult.

---

## Developer diagnostics

Live CASE-0001 `POST /api/v1/dev/pack07/diagnostics`:

| Layer | Status |
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
| Temporal | NOT_EVALUATED |
| Optimization | NOT_EVALUATED |
| Narrative | NOT_EVALUATED |
| Runtime Contract | PASS |
| Overall | PASS |

Empty `GET /api/v1/dev/pack07/diagnostics`: Luck Interaction `NOT_IMPLEMENTED`.

---

## UI integration

Existing Đại Vận `LuckCard`. Below **Kích hoạt vận hiện tại**:

**TƯƠNG TÁC VẬN HIỆN TẠI** (`data-luck-section="interaction"`)

Compact: Life Situation, main interaction driver, bottleneck, top opportunity, top trade-off/risk. Graph edges stay behind **Chi tiết tương tác**. Expanded pair shows Domain A ↔ Domain B, type, short explanation, optional condition. No raw IDs. No event language.

---

## Build

PASS — `python tools/build.py` (version 1.0.0, compileall applications/tools/engines)

---

## Type Check

PASS — Pack 07 scoped mypy:

`python -m mypy --explicit-package-bases --follow-imports=skip engines/detailed_interpretation_engine applications/api/contracts/pack07_runtime.py applications/api/routes/pack07_dev.py`

94 files, no issues.

---

## Tests

| Suite | Result |
| --- | --- |
| `tests/detailed_interpretation` | **181 passed** |
| P7-IMP-11 luck interaction | **17 passed** (included above) |
| Luck engine + PDF + DOCX + History | **38 passed** (`test_luck_contract`, `test_g1_08_dayun`, `test_pdf_renderer`, `test_docx_renderer`, G2-05 history snapshot + portal history) |
| Portal UI-10 / UI-10R Vitest | **50 passed, 1 failed** — pre-existing ResultStore boot L25 (`expected current vs empty`). Not caused by this ticket. Not repaired. |

Negatives proved: Authority strong ≠ Career support without natal edge; Career overloaded ≠ Vitality stress after removing `vitality supports career`; Wealth active ≠ Relationship conflict; Life Situation ≠ natal state; Interaction Driver ≠ Domain Driver; Interaction Bottleneck ≠ natal bottleneck rewrite.

Metamorphics proved: remove one activation → dependent edges disappear; change Domain A → unrelated C/D unchanged; remove natal support edge → related support disappears; change interaction → Luck Activation identical.

No Golden Dataset / snapshot / expected-output edits. No asserts removed.

---

## Runtime

| Endpoint | Result |
| --- | --- |
| `GET /api/v1/health` | 200 |
| `POST /api/v1/analyze` | 200; current cycle Ất Tỵ 2022–2031; `data.luck.activation` six items; `data.luck.interaction` compact Life Situation / driver / bottleneck / opportunity / risk; no `TR-P7-` / `E-DI-` leak |
| `/result` | 200; Đại Vận + Luck Activation + Luck Interaction |
| `/history` | 200; no persistence change |
| `GET /api/v1/dev/pack07/diagnostics` | 200; Luck Interaction `NOT_IMPLEMENTED` on empty shell |
| `POST /api/v1/dev/pack07/diagnostics` | 200; Luck Interaction `PASS`; Luck `PASS`; Domains `PASS` |

Proof dump: `implementation/pack_07/P7-IMP-11_diagnostics.json`

---

## Screenshots

| Shot | Path |
| --- | --- |
| /result overview | `implementation/pack_07/screenshots/p7_imp_11_result_overview.png` |
| Current Đại Vận | `implementation/pack_07/screenshots/p7_imp_11_luck_current.png` |
| Luck Activation summary | `implementation/pack_07/screenshots/p7_imp_11_luck_activation.png` |
| Luck Interaction summary | `implementation/pack_07/screenshots/p7_imp_11_luck_interaction.png` |
| Expanded interaction edge | `implementation/pack_07/screenshots/p7_imp_11_luck_interaction_expanded.png` |
| Mobile Luck Interaction | `implementation/pack_07/screenshots/p7_imp_11_mobile_luck_interaction.png` |
| Diagnostics Luck Interaction PASS | `implementation/pack_07/screenshots/p7_imp_11_diagnostics.png` |

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

Natal Domains unchanged. Luck Activation unchanged. Interaction is a separate temporal projection. Conflict/trade-off would preserve both activations; this chart preserves Career vs Wealth conflict without averaging.

---

## Business logic introduced

LUCK INTERACTION ONLY

---

## Files changed

Engine / runtime:

- `engines/detailed_interpretation_engine/luck_interaction/__init__.py`
- `engines/detailed_interpretation_engine/luck_interaction/constants.py`
- `engines/detailed_interpretation_engine/luck_interaction/models.py`
- `engines/detailed_interpretation_engine/luck_interaction/facts.py`
- `engines/detailed_interpretation_engine/luck_interaction/labels.py`
- `engines/detailed_interpretation_engine/luck_interaction/evaluate.py`
- `engines/detailed_interpretation_engine/luck_interaction/graph.py`
- `engines/detailed_interpretation_engine/luck_interaction/presentation.py`
- `engines/detailed_interpretation_engine/luck_interaction/engine.py`
- `engines/detailed_interpretation_engine/luck_interaction/validation.py`
- `engines/detailed_interpretation_engine/constants.py`
- `engines/detailed_interpretation_engine/temporal.py`
- `engines/detailed_interpretation_engine/validators.py`
- `engines/detailed_interpretation_engine/diagnostics.py`
- `engines/detailed_interpretation_engine/__init__.py`
- `applications/api/services/orchestrator.py`

Customer UI:

- `applications/customer_portal/src/screens/commercial_dashboard/LuckCard.tsx`
- `applications/customer_portal/src/screens/commercial_dashboard/luckAdapter.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/luckFixture.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/types.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/commercial-dashboard.css`
- `applications/customer_portal/src/models/dto.ts`
- `applications/customer_portal/src/models/index.ts`

Tests / proof:

- `tests/detailed_interpretation/test_p7_imp_11_luck_interaction.py`
- `applications/customer_portal/scripts/capture_p7_imp_11_live.py`
- `implementation/pack_07/P7-IMP-11_RUNTIME_REPORT.md`
- `implementation/pack_07/P7-IMP-11_diagnostics.json`
- `implementation/pack_07/screenshots/p7_imp_11_*.png`

---

## Known limitations

- Interaction evaluates the current Đại Vận window only. It does not mint Annual / Monthly / Daily / Hourly activation.
- Support domains (academic, leadership, management, creative, learning) participate only when present and not blocked/unresolved in Luck Activation. CASE-0001 academic is dormant, so natal academic → career does not become a live support interaction.
- Customer PDF / DOCX / History / executive Luck section do not render Luck Interaction.
- Portal UI-10 L25 ResultStore boot failure is pre-existing and unrelated.
- Compact UI hides graph edges until **Chi tiết tương tác**. Mobile compact risk line can wrap.

---

## Next

STOP.

Do not implement Temporal Activation automatically.
