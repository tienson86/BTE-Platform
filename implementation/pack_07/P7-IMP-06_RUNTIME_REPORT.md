# P7-IMP-06 RUNTIME REPORT

**Task:** P7-IMP-06 — Shen Sha Secondary Evidence & Ecosystem — live vertical slice  
**Date:** 2026-09-05  
**Status:** PASS

---

## Status

PASS

---

## Upstream Shen Sha source

Exact owner: **`engines.bazi_engine.shensha`** (`ShenShaService` + `catalog.py`).

Published on Analyze as `data.bazi.shensha_matches` (canonical `id`, `canonical_name`, occurrences). Pack 07 consumes those matches only. It does not recalculate star existence. Vietnamese/Chinese names are presentation aliases, not second IDs.

V1 detector catalog: `tian_yi`, `wen_chang`, `lu_shen`, `hong_luan`, `tian_xi`, `hua_gai`, `yang_ren`, `tian_de`, `yue_de`. Freeze extras (`guo_yin`, `hoc_duong`, `thai_cuc`, `ham_tri`, `giai_than`, `khong_vong`, `co_than`, `qua_tu`) stay dormant until the detector publishes them.

---

## Individual Shen Sha interpretation

DI-05 secondary-evidence layer. Each detected star is gated and may only strengthen / qualify / warn / remain unresolved. It never creates domain classification, Pattern, Grade, Integrity, Useful God, Wealth/Career profiles, or Ten Gods Driver.

Customer copy is short and deterministic. Dictionary paragraphs from `approvedShenShaMeaning` are bypassed when Pack 07 projection is present.

---

## Dependency gating

Every interpreted star declares `supported_domains`, `required_dependencies`, `dependency_state`, `modifier_state`, `confidence_modifier`, conditions, warnings, evidence/trace.

States used:

- dependency: `satisfied | partial | blocked | unresolved | not_available`
- modifier: `applied | weak_support | qualified | warning | blocked | inactive | unresolved`

Confidence modification is categorical (`strengthen / qualify / warn / no_effect / blocked`). No invented numeric deltas.

MC-01 still `NOT_BOUND`. Required MC-01 domains that are unpublished stay `unresolved`. Stars are not promoted to applied structural modifiers.

---

## CASE-0001 detected Shen Sha

Fresh Analyze (Nguyễn Tiến Sơn, 21/01/1987 04:30, male, Hà Nội):

- Thiên Ất Quý Nhân (`tian_yi`) — Trụ Tháng
- Hồng Loan (`hong_luan`) — Trụ Tháng
- Thiên Đức Quý Nhân (`tian_de`) — Trụ Ngày
- Nguyệt Đức Quý Nhân (`yue_de`) — Trụ Ngày

Not hard-coded. Copied from live `bazi.shensha_matches`.

---

## Applied / blocked / unresolved modifiers

- Applied: none
- Blocked: none
- Unresolved: Thiên Ất Quý Nhân, Hồng Loan, Thiên Đức Quý Nhân, Nguyệt Đức Quý Nhân

All four remain secondary signals. No quý nhân / marriage / authority promotion.

---

## Shen Sha Ecosystem

- Active clusters: none
- Conditional clusters: none
- Blocked clusters: none as applied groups (families without usable members stay inactive / unresolved)
- Dominant cluster: **unresolved** (`Chưa đủ dữ liệu`)
- Supporting cluster: none
- Risk cluster: inactive (no canonical risk stars detected on this chart)

Twelve families exist in architecture. Only meaningful active / conditional / warning clusters would render as rows. CASE-0001 correctly shows the compact Hệ Thần Sát summary instead of a catalog list.

---

## MC-01 dependency handling

PARTIAL

MC-01 is `NOT_BOUND`. Domain-dependent stars and clusters stay unresolved / not applied. Dominant cluster is left unresolved rather than guessed.

---

## Runtime binding

`CanonicalRuntimeResult.interpretation.shen_sha.individual`  
`CanonicalRuntimeResult.interpretation.shen_sha.ecosystem`

No second root. Public Analyze additive projection only: `data.bazi.shen_sha.{individual,ecosystem}`. `pack07_context` stays internal.

---

## Developer diagnostics

After CASE-0001 Analyze:

| Layer | Status |
| --- | --- |
| Contracts | PASS |
| Contexts | PASS |
| Validators | PASS |
| Ten Gods | PARTIAL |
| Ten God Combination | PARTIAL |
| Ten Gods Ecosystem | PARTIAL |
| Shen Sha | PARTIAL |
| Shen Sha Ecosystem | PARTIAL |
| Evidence Priority | NOT_IMPLEMENTED |
| Domains | NOT_EVALUATED |
| Luck | NOT_IMPLEMENTED |
| Temporal | NOT_EVALUATED |
| Optimization | NOT_EVALUATED |
| Narrative | NOT_EVALUATED |
| Runtime Contract | PASS |
| MC-01 | NOT_BOUND |
| Overall | PASS |

Empty-shell GET diagnostics still reports Shen Sha `NOT_IMPLEMENTED` when no detection is bound.

---

## UI integration

Existing THẦN SÁT card only. No second top-level section.

Old behavior (no Pack 07 projection): canonical matches + approved dictionary line, grouped only when payload already carries categories.

New behavior (Pack 07 present): keep detected names and pillar facts; replace dictionary prose with compact state chips (`Hỗ trợ / Điều kiện / Cảnh báo / Chưa đủ dữ liệu`) and one-at-a-time expand; add compact **Hệ Thần Sát**. Supporting note unchanged: Thần Sát is auxiliary and does not decide the whole chart.

---

## Visual layout

Compact 2×2 star rows on desktop, stacked on mobile. Ecosystem is a four-cell summary. No dictionary wall, no raw IDs, no traces, no debug text, no duplicate old/new interpretation, no overflow in captured viewports.

Cluster-detail screenshot matches the ecosystem summary on CASE-0001 because no prominent cluster exists to expand.

---

## Build

PASS — `python tools/build.py` (version 1.0.0, compileall applications/tools/engines).  
Portal result bundle rebuilt by live capture (`npm run build:result`).

---

## Type Check

PASS — Pack 07 scoped mypy:

`python -m mypy --explicit-package-bases --follow-imports=skip engines/detailed_interpretation_engine applications/api/contracts/pack07_runtime.py applications/api/routes/pack07_dev.py`

54 source files, no issues.

---

## Tests

| Suite | Result |
| --- | --- |
| `tests/detailed_interpretation` | **92 passed** |
| P7-IMP-06 unit/cluster/negative/metamorphic | **28 passed** |
| Existing Shen Sha + Ten Gods engine + portal UI-09 Python | **123 passed** (includes overlapping IMP-06) |
| Analyze / Portal / History / PDF / DOCX | **33 passed** |
| Vitest UI-09 / UI-09R / UI-15 | **47 passed**, 1 remaining unrelated (`S20 ResultStore / routing boot`, expected `current` vs `empty`; not Shen Sha rendering) |

No test files other than `tests/detailed_interpretation/test_p7_imp_06_shen_sha.py` were edited. Unrelated failures were not repaired.

---

## Runtime

| Endpoint | Result |
| --- | --- |
| `/api/v1/health` | 200 `ok` |
| `POST /api/v1/analyze` | 200, pipeline `calendar → bazi → pattern → score → interpretation → report → narrative`, no `pack07_context` leak |
| `/result` | live THẦN SÁT Pack 07 card |
| `/history` | 200 |
| `GET /api/v1/dev/pack07/diagnostics` | 200 empty-shell |
| `POST /api/v1/dev/pack07/diagnostics` | 200 CASE-0001 states above |

---

## Screenshots

- `implementation/pack_07/screenshots/p7_imp_06_result_overview.png`
- `implementation/pack_07/screenshots/p7_imp_06_shen_sha_desktop.png`
- `implementation/pack_07/screenshots/p7_imp_06_shen_sha_expanded.png`
- `implementation/pack_07/screenshots/p7_imp_06_shen_sha_ecosystem.png`
- `implementation/pack_07/screenshots/p7_imp_06_cluster_expanded.png`
- `implementation/pack_07/screenshots/p7_imp_06_shen_sha_mobile.png`
- `implementation/pack_07/P7-IMP-06_diagnostics.json`

---

## PDF

PASS / intentionally unchanged. Pack 07 Shen Sha is not in export.

---

## DOCX

PASS / intentionally unchanged. Pack 07 Shen Sha is not in export.

---

## History

PASS / intentionally unchanged. No persistence schema change.

---

## System consistency

PASS

Canonical detector IDs = Pack 07 `shen_sha_id` = customer labels (`Thiên Ất Quý Nhân`, `Hồng Loan`, `Thiên Đức Quý Nhân`, `Nguyệt Đức Quý Nhân`). No second detection truth.

---

## Business logic introduced

SHEN SHA SECONDARY EVIDENCE + ECOSYSTEM ONLY

---

## Files changed

Engine / runtime:

- `engines/detailed_interpretation_engine/shen_sha/__init__.py`
- `engines/detailed_interpretation_engine/shen_sha/constants.py`
- `engines/detailed_interpretation_engine/shen_sha/models.py`
- `engines/detailed_interpretation_engine/shen_sha/facts.py`
- `engines/detailed_interpretation_engine/shen_sha/evaluate.py`
- `engines/detailed_interpretation_engine/shen_sha/clusters.py`
- `engines/detailed_interpretation_engine/shen_sha/presentation.py`
- `engines/detailed_interpretation_engine/shen_sha/engine.py`
- `engines/detailed_interpretation_engine/constants.py`
- `engines/detailed_interpretation_engine/enums.py`
- `engines/detailed_interpretation_engine/evidence.py`
- `engines/detailed_interpretation_engine/schema_registry.py`
- `engines/detailed_interpretation_engine/validators.py`
- `engines/detailed_interpretation_engine/diagnostics.py`
- `engines/detailed_interpretation_engine/models.py`
- `engines/detailed_interpretation_engine/__init__.py`
- `applications/api/services/orchestrator.py`

Customer UI (existing THẦN SÁT):

- `applications/customer_portal/src/models/dto.ts`
- `applications/customer_portal/src/models/index.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/types.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/shenShaAdapter.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/ShenShaCard.tsx`
- `applications/customer_portal/src/screens/commercial_dashboard/shenShaFixture.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/commercial-dashboard.css`

Tests / proof:

- `tests/detailed_interpretation/test_p7_imp_06_shen_sha.py`
- `applications/customer_portal/scripts/capture_p7_imp_06_live.py`
- `implementation/pack_07/P7-IMP-06_RUNTIME_REPORT.md`
- `implementation/pack_07/P7-IMP-06_diagnostics.json`
- `implementation/pack_07/screenshots/p7_imp_06_*.png`

No frozen design documents were changed.

---

## Known limitations

- Live CASE-0001 cannot apply modifiers or activate clusters until MC-01 / domain profiles are bound.
- Stars not published by `bazi_engine.shensha` are not invented (`guo_yin`, `khong_vong`, …).
- Pack 07 Shen Sha remains out of PDF / DOCX until canonical export integration.
- Cluster expand on CASE-0001 has no prominent cluster row; the screenshot is the ecosystem summary.
- One pre-existing Vitest (`UI-09 S20 ResultStore boot`) still fails and was not repaired.

---

## Next

STOP and wait for Product Owner review.
