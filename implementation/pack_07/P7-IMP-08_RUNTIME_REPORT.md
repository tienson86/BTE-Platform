# P7-IMP-08 RUNTIME REPORT

**Task:** P7-IMP-08 — Evidence Priority Engine — live vertical slice  
**Date:** 2026-09-05  
**Status:** PASS

---

## Status

PASS

Evidence Priority Engine ranks existing MC-01 and Pack 07 evidence only. No Domain Interpretation, Optimization, or Narrative Composer was implemented.

---

## Evidence sources

Consumed, not recalculated:

**MC-01**

- Pattern (`Chính Ấn`)
- Purity (`mixed` / Pha tạp)
- Pattern Strength (`moderate` / Vừa)
- Damage (`DMG-MC-001` `resource_overload`)
- Rescue (`RSC-MC-001` `output_releases_excess`)
- Integrity (`mixed` / Hỗn hợp)
- Grade (`B`)
- Achievement (academic, entrepreneurship, management)
- Wealth profile dimensions
- Career profile (academic_research, managerial, leadership_command)

**Pack 07**

- Ten Gods natal findings
- Ten God Combinations / chains
- Ten Gods Ecosystem (Driver / Bottleneck)
- Shen Sha individual stars
- Shen Sha Ecosystem (PARTIAL; unresolved clusters not promoted)

ScoreEngine grade is observed only (`D+`). It is never used as MC-01 Grade.

---

## Evidence Graph

`EvidenceGraph` is published on `EvidencePriorityResult.graph`.

CASE-0001 live shape:

- Nodes: Pattern, Integrity, Grade, Damage, Rescue, Achievement, Wealth, Career, Ten Gods, Combinations, Ecosystem Driver/Bottleneck, decorative Shen Sha
- Edges used: `depends_on`, `qualifies`, `damages`, `rescues`, `supports`, `strengthens`

Same-cause nodes merge (Pattern + DI-04 Driver `Chính Ấn` share `pattern.primary`). Duplicate semantic keys collapse while source refs and traces are preserved.

---

## P0 / P1 / P2

Fresh CASE-0001 (Nguyễn Tiến Sơn, male, 21/01/1987 04:30, Hà Nội):

**P0 Critical**

- Integrity — Hỗn hợp
- MC-01 Grade — B
- Pattern / Driver — Chính Ấn
- Bottleneck — Thiên Tài

**P1 Major**

- Damage — Ấn quá vượng kìm biểu đạt (`resource_overload`)
- Combination — Tỷ Kiếp đoạt Tài
- Achievement — Học thuật · Khởi nghiệp · Quản trị
- Wealth dimensions kept split (creation weak vs retention/accumulation not averaged)
- Career — Nghiên cứu học thuật · Quản lý · Lãnh đạo
- Combination — Tài → Quan → Ấn
- Combination — Sát → Ấn → Thân

**P2 Important**

- Secondary active chains (Thương Quan → Tài, Thân vượng dụng Quan/Tài/Thực Thương, Quan Sát hỗn tạp)
- Material Ten Gods other than the Pattern deity (Kiếp Tài, Thất Sát, Thiên Tài, Thiên Ấn)

Shen Sha stars on this chart are P5 decorative / unresolved. None are P0.

---

## Top Driver

Chính Ấn

Consumed from MC-01 Pattern + already-elected DI-04 Driver. No new chart Driver was elected here.

---

## Top Bottleneck

Thiên Tài

DI-04 bottleneck remains P0. It does not disappear because Pattern/Grade also occupy P0.

---

## Top Risk

Ấn quá vượng kìm biểu đạt

MC-01 Damage. Rescue remains a separate finding. Damage is not deleted.

---

## Top Opportunity

Học thuật · Khởi nghiệp · Quản trị

MC-01 Achievement drivers. Not a Domain engine result.

---

## Top Condition

Cần giữ toàn vẹn cấu trúc chính

Mapped from MC-01 expression condition (`integrity_must_hold`). Compact label only. No narrative.

---

## Grade semantic guard

| Object | Value | Owner |
| --- | --- | --- |
| MC-01 structural Grade | **B** | `MingJuDecisionEngine` / `pattern.structural_grade` |
| ScoreEngine customer grade | **D+** | `ScoreEngine` / `score.grade` |

These remain different semantic objects. Evidence Priority ranks Grade **B**. Changing ScoreEngine grade does not change P0 structural order. CASE-0001 public payload still publishes both, unmixed.

---

## Deduplication

- Pattern + DI-04 Driver of the same deity merge into one `pattern.primary` node.
- Duplicate `semantic_key` values merge; source refs, traces, and supporting evidence are unioned.
- Derived combination rows (`source_combination_id`) are not emitted as extra nodes.
- Individual Shen Sha members of a ranked cluster do not become a second cluster headline.

---

## Contradiction preservation

Not averaged:

- Damage + Rescue both remain (P1 damage, supporting/opportunity rescue).
- Wealth creation weakness is not blended with retention/accumulation.
- Career opportunity structures remain separate from risk chains (Tỷ Kiếp đoạt Tài).
- Removing Rescue keeps Damage and can raise residual risk rank within the same tier.

---

## Runtime binding

Path:

`CanonicalRuntimeResult.interpretation.evidence_priority`

Schema: `bte.detailed_interpretation.evidence_priority.v1`  
Ruleset: `bte.detailed_interpretation.evidence_priority.rules.v1`

No second root. Customer JSON publishes a labels-only `data.evidence_priority` compact summary (no finding IDs, no traces, no hashes).

---

## Developer diagnostics

POST `/api/v1/dev/pack07/diagnostics` on fresh CASE-0001:

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
| Domains | NOT_EVALUATED |
| Luck | NOT_IMPLEMENTED |
| Temporal | NOT_EVALUATED |
| Optimization | NOT_EVALUATED |
| Narrative | NOT_EVALUATED |
| Runtime Contract | PASS |
| Overall | PASS |

GET empty shell: Evidence Priority remains `NOT_IMPLEMENTED` (no evidence to rank).

---

## UI integration

Compact block **TRỌNG TÂM LÁ SỐ** inside the existing Overview card (`TỔNG QUAN LÁ SỐ`). No new page architecture. No duplicate Mệnh Cục or Ten Gods sections.

Customer labels only:

- Động lực chính — Chính Ấn
- Điểm nghẽn — Thiên Tài
- Rủi ro chính — Ấn quá vượng kìm biểu đạt
- Cơ hội chính — Học thuật · Khởi nghiệp · Quản trị
- Điều kiện phát huy — Cần giữ toàn vẹn cấu trúc chính

No raw IDs. No traces. No domain narrative.

---

## Build

PASS — `python tools/build.py` (version 1.0.0, compileall applications/tools/engines)

---

## Type Check

PASS — Pack 07 scoped mypy:

`python -m mypy --explicit-package-bases --follow-imports=skip engines/detailed_interpretation_engine applications/api/contracts/pack07_runtime.py applications/api/routes/pack07_dev.py`

64 source files, no issues.

---

## Tests

| Suite | Result |
| --- | --- |
| `tests/detailed_interpretation` | **123 passed** |
| P7-IMP-08 negatives / metamorphics / CASE-0001 | **15 passed** (included above) |
| MC-01 / Ten Gods / Analyze / History / PDF / DOCX / Portal pytest | **134 passed** |
| Portal UI-04 / G1-12 Vitest | **17 passed, 1 failed** — pre-existing ResultStore boot (`expected current vs empty`). Not caused by this ticket. Not repaired. |

Aligned `test_p7_imp_07_mc01_binding.py` diagnostics expectation: `evidence_priority` is now `PASS` after this layer exists. No Golden Dataset / snapshot / expected-output edits. No asserts removed.

---

## Runtime

| Endpoint | Result |
| --- | --- |
| `GET /api/v1/health` | 200 |
| `POST /api/v1/analyze` | 200; `evidence_priority` compact labels; `structural_grade=B`; `score.grade=D+`; no `mc01` / traces leaked |
| `/result` | 200; TRỌNG TÂM LÁ SỐ renders in Overview |
| `/history` | 200; no persistence change |
| `GET /api/v1/dev/pack07/diagnostics` | 200; Evidence Priority `NOT_IMPLEMENTED` on empty shell |
| `POST /api/v1/dev/pack07/diagnostics` | 200; Evidence Priority `PASS` |

---

## Screenshots

- `implementation/pack_07/screenshots/p7_imp_08_result_overview.png`
- `implementation/pack_07/screenshots/p7_imp_08_mingju.png`
- `implementation/pack_07/screenshots/p7_imp_08_evidence_priority.png`
- `implementation/pack_07/screenshots/p7_imp_08_ten_gods_ecosystem.png`
- `implementation/pack_07/screenshots/p7_imp_08_shen_sha_ecosystem.png`
- `implementation/pack_07/screenshots/p7_imp_08_mobile_evidence_priority.png`
- `implementation/pack_07/screenshots/p7_imp_08_diagnostics.png`

Proof dump: `implementation/pack_07/P7-IMP-08_diagnostics.json`

---

## PDF

PASS / intentionally unchanged

Canonical export projection does not yet include Evidence Priority. Existing PDF regression passed. Not forced into export.

---

## DOCX

PASS / intentionally unchanged

Same as PDF. Existing DOCX regression passed.

---

## History

PASS / intentionally unchanged

No persistence schema or snapshot-shape change.

---

## System consistency

PASS

- MC-01 structural evidence is primary (Pattern / Integrity / Grade / Driver / Bottleneck / Damage)
- ScoreEngine D+ is not used as MC-01 Grade B
- Shen Sha never becomes P0 (CASE-0001 stars stay P5; unresolved ecosystem is not dominant)
- Duplicates merge by semantic key
- Damage remains when Rescue exists
- Critical bottleneck (Thiên Tài) remains visible beside stronger P0 Pattern/Grade
- Runtime binding path is the frozen interpretation root
- Live compact summary renders

---

## Business logic introduced

EVIDENCE PRIORITY ONLY

Collect, merge, deduplicate, rank, and group existing canonical evidence. No Domain / Authority / Career / Wealth / Relationship / Legacy / Vitality / Luck / Temporal / Optimization / Narrative engines.

---

## Files changed

Engine

- `engines/detailed_interpretation_engine/evidence_priority/` (`engine.py`, `collect.py`, `merge.py`, `assemble.py`, `candidates.py`, `constants.py`, `labels.py`, `presentation.py`)
- `engines/detailed_interpretation_engine/evidence.py`
- `engines/detailed_interpretation_engine/validators.py`
- `engines/detailed_interpretation_engine/diagnostics.py`
- `engines/detailed_interpretation_engine/constants.py`
- `engines/detailed_interpretation_engine/models.py`
- `engines/detailed_interpretation_engine/__init__.py`

Runtime

- `applications/api/services/orchestrator.py`

UI

- `applications/customer_portal/src/screens/commercial_dashboard/OverviewCard.tsx`
- `applications/customer_portal/src/screens/commercial_dashboard/overviewAdapter.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/types.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/commercial-dashboard.css`
- `applications/customer_portal/src/screens/commercial_dashboard/overviewFixture.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/index.ts`
- `applications/customer_portal/src/adapters/narrativeV2DashboardAdapter.ts`
- `applications/customer_portal/src/resultState/narrativePresentationSelection.ts`
- `applications/customer_portal/src/models/dto.ts`
- `applications/customer_portal/src/models/index.ts`

Tests / proof

- `tests/detailed_interpretation/test_p7_imp_08_evidence_priority.py`
- `tests/detailed_interpretation/test_p7_imp_07_mc01_binding.py` (diagnostics status only)
- `applications/customer_portal/scripts/capture_p7_imp_08_live.py`
- `implementation/pack_07/P7-IMP-08_RUNTIME_REPORT.md`
- `implementation/pack_07/P7-IMP-08_diagnostics.json`
- `implementation/pack_07/screenshots/p7_imp_08_*.png`

---

## Known limitations

- Shen Sha Ecosystem remains PARTIAL on CASE-0001; unresolved clusters are accepted as non-blocking and are not promoted.
- Compact customer summary is five labels only. Full ranked graph stays internal on the runtime contract.
- Evidence Priority is not projected into PDF / DOCX / History.
- Public Analyze payload does not leak the internal finding graph (by design).
- Pre-existing Vitest ResultStore boot failure (`O15`) is unchanged.

---

## Next

STOP and wait for Product Owner review.

Do not implement Domain Interpretation.  
Do not implement Optimization.  
Do not implement Narrative.
