# Project Readiness Report

| Item | Value |
|------|-------|
| Document | PROJECT_READINESS_REPORT.md |
| Project | BTE Platform V1.0 |
| Assessment Type | Project Readiness (READ-ONLY synthesis) |
| Sources | `ARCHITECTURE_COMPLIANCE_REPORT.md`, `KNOWLEDGE_COMPLIANCE_REPORT.md`, `PIPELINE_RUNTIME_REPORT.md` |
| Supporting | `ARCHITECTURE_TRACE_REPORT.md` |
| Date | 2026-07-28 |
| Constraints | No code, no patch — report only |

---

## Executive Summary

BTE Platform V1.0 has a **working production API pipeline** (Calendar → BaZi → Pattern → Score → Interpretation → Report → Narrative) and substantial engine/module test coverage, but it is **contract-divergent** from the written Stages 0–12 architecture. Knowledge assets are large on disk while production mainly consumes `05_rule_database`. Runtime platform services (Context Registry, Version Manager, stage metrics) are thin.

| Dimension | Score | Classification |
|-----------|------:|----------------|
| Architecture | **55%** | PARTIALLY READY |
| Knowledge | **42%** | NOT READY (freeze) / PARTIALLY READY (ops) |
| Pipeline | **48%** | PARTIALLY READY |
| Testing | **62%** | PARTIALLY READY |
| Documentation | **78%** | MOSTLY READY |
| Runtime (ops services) | **35%** | NOT READY |
| **Overall** | **~52%** | **PARTIALLY READY** |

### Overall Verdict

**PARTIALLY READY**

| Gate | Verdict |
|------|---------|
| Demo / internal E2E use | **MOSTLY READY** (operational) |
| Architecture Freeze | **NOT READY** (Critical N-01…N-04 open) |
| Knowledge Freeze (full checklist) | **NOT READY** |
| Production commercial freeze | **PARTIALLY READY** — usable with known debt; not freeze-grade |

Freeze requires either remediating Critical/High items **or** ADR-waiving the collapsed V1 runtime against the written contracts.

---

## Scorecard

| Score Axis | Value | Basis |
|------------|------:|-------|
| **Architecture** | **55%** | Architecture Compliance overall / architecture score |
| **Knowledge** | **42%** | Knowledge Health Score |
| **Pipeline** | **48%** | Pipeline Runtime Health (aligned with Arch pipeline 52%) |
| **Testing** | **62%** | Module/golden/API phase tests strong; no `tests/architecture/` |
| **Documentation** | **78%** | `PIPELINE_ARCHITECTURE` + `SYSTEM_DATA_FLOW` + audit reports complete |
| **Overall** | **52%** | Weighted blend (Arch 25%, Pipeline 20%, Knowledge 20%, Testing 15%, Docs 10%, Runtime 10%) |

### Classification Legend

| Label | Score band | Meaning |
|-------|------------|---------|
| READY | ≥ 85% | Freeze-grade; residual Low only |
| MOSTLY READY | 70–84% | Ship with tracked Medium debt |
| PARTIALLY READY | 45–69% | Usable; Critical/High blockers remain |
| NOT READY | < 45% | Do not freeze / do not claim complete |

---

## Architecture Readiness

| Item | Detail |
|------|--------|
| **Score** | **55%** |
| **Classification** | **PARTIALLY READY** |
| **Freeze** | **NOT READY** for Architecture Freeze |

### Strengths

- Core engines exist with coarse single-responsibility (Calendar, BaZi, Pattern detect, Score calculate, Report render).
- Production orchestrator forward order is usable.
- Architecture contracts are written and audited.

### Gaps

- Stages 5 / 7–9 / 12 collapsed (N-01).
- RuleContext mutated by Score (N-02); built inside Pattern (N-03).
- Dual / divergent orchestrators (N-04).
- Builder computes business facts; hardcoded maps; API BaZi enrichment (N-05…N-08).
- Missing contract context types (N-09).

### Readiness statement

Architecture is **operationally understandable** but **not freeze-aligned**. Treat as contract-divergent until Critical items cleared or ADR-ratified.

---

## Knowledge Readiness

| Item | Detail |
|------|--------|
| **Score** | **42%** |
| **Classification** | **NOT READY** (full Knowledge Freeze) / **PARTIALLY READY** (rule-DB ops) |
| **Executable root** | `engines/interpretation_engine/knowledge/` |
| **Governance root** | `knowledge/` (docs only) |

### Strengths

- Large `05_rule_database` (~2,526 disk records; ~495 matchable) drives production Interpretation.
- Schemas exist for sentence library / report templates.
- Governance docs under `knowledge/docs/`.

### Gaps

- Checklist mismatch: missing `04_sentence_library`, `07_examples`, `08_metadata` as named modules.
- Phrase / dictionary / terminology / templates / sentences largely unused on production Orchestrator path.
- ~22% rule match utilization in samples; 104 duplicate rule IDs; broken `na_yin.json`.
- Priority KB (`08_priority_rules`) bypassed; PriorityRuleLoader fails on multi-JSON when used.
- No global knowledge version stamp.

### Readiness statement

Do **not** claim full Knowledge module compliance. Freeze only governance + rule-DB schema intent after Priority strategy ADR; keep dead-asset policy explicit.

---

## Pipeline Readiness

| Item | Detail |
|------|--------|
| **Score** | **48%** |
| **Classification** | **PARTIALLY READY** |
| **E2E runnable** | Yes (production `OrchestratorService`) |

### Stage coverage (contract 0–12)

| Status | Stages |
|--------|--------|
| Present | 1 Calendar, 2 BaZi, 4 Pattern, 6 Score, 10 Interpretation, 11 Report |
| Partial / side | 3 Feng Shui |
| Collapsed / skipped | 0, 5, 7, 8, 9, 12 |
| Extra | `narrative` |

### Strengths

- Production path completes analyze end-to-end.
- Partial-stage early stop works.
- Report production path is render-oriented.

### Gaps

- Not Stages 0–12 identity.
- Integration orchestrator runs Score before Pattern.
- Hidden deps: RC-in-Pattern, KB-in-Interpretation, `bazi_truth`, Feng merged into calendar view.

---

## Runtime Readiness

| Item | Detail |
|------|--------|
| **Score** | **35%** (services) / **~48%** (overall runtime health) |
| **Classification** | **NOT READY** (platform runtime services) / **PARTIALLY READY** (execution) |

| Service | Status |
|---------|--------|
| Pipeline Orchestrator | Partial (works; not singular) |
| Context Registry | Missing |
| Logging | Partial (HTTP; not stage-structured) |
| Metrics | Partial (HTTP only) |
| Cache Manager | Fragmented per-engine |
| Configuration Manager | Partial (per-app settings) |
| Health Check | Liveness only (not readiness) |
| Version Manager | Missing / stub |

### Readiness statement

Safe for controlled internal runs. Not ready for production ops maturity (SLO stage metrics, readiness probes, version gates, context immutability enforcement).

---

## Testing Readiness

| Item | Detail |
|------|--------|
| **Score** | **62%** |
| **Classification** | **PARTIALLY READY** |

### Strengths

- Broad module tests (`tests/bazi`, `tests/calendar`, `tests/report`, engine suites).
- Golden Dataset present.
- API phase unification tests (`applications/api/tests/test_phase*.py`).
- Production readiness API test file exists.

### Gaps

- No `tests/architecture/` for stage order, ownership, immutability (N-16).
- Tests do not enforce Stages 0–12 contracts.
- Knowledge utilization / Priority KB not guarded by architecture tests.
- Dual orchestrator divergence not blocked by CI contract tests.

### Readiness statement

Good **behavioral regression** posture; weak **architecture-compliance** posture. Suitable to protect engine outputs; insufficient to freeze architecture.

---

## Documentation Readiness

| Item | Detail |
|------|--------|
| **Score** | **78%** |
| **Classification** | **MOSTLY READY** |

### Strengths

- `docs/architecture/PIPELINE_ARCHITECTURE.md` and `SYSTEM_DATA_FLOW.md` are comprehensive contracts.
- Audit pack complete: Architecture Compliance, Trace, Knowledge Compliance, Pipeline Runtime.
- Knowledge governance docs exist under `knowledge/docs/`.

### Gaps

- Contracts describe a stricter system than runtime implements (doc–code drift).
- No ADR pack yet ratifying collapsed V1 vs full Stages 0–12.
- Root `knowledge/` vs engine knowledge split needs a single “where is SSOT?” index for newcomers.

### Readiness statement

Documentation is **ahead of** runtime alignment. Highest-leverage doc work is ADR freeze decisions, not more descriptive prose.

---

## Production Readiness

| Item | Detail |
|------|--------|
| **Classification** | **PARTIALLY READY** |
| **Commercial V1 freeze** | **NOT READY** without Critical remediation or ADR waiver |

| Concern | Status |
|---------|--------|
| E2E analyze API | Works |
| Portal / delivery | Implicit JSON delivery; no Stage 12 service |
| Data correctness producers | Improved recently; ownership still mixed |
| Knowledge commercial depth | Rule DB only; templates/sentences idle |
| Ops (metrics/health/version) | Thin |
| Single pipeline SSOT | Production yes; legacy paths remain |

**Production guidance:** Ship only as **controlled V1 beta** with explicit known-limitations list. Do not market “full Stages 0–12 Knowledge Platform” until High items and Priority strategy are closed.

---

## Issue Register

### Critical Issues

| ID | Issue | Source |
|----|-------|--------|
| C1 | Collapsed Stages 5 / 7–9 / 12 — not first-class | Arch N-01, Runtime |
| C2 | Score mutates published RuleContext | Arch N-02, Runtime |
| C3 | RuleContext constructed inside Pattern Engine | Arch N-03, Runtime |
| C4 | Dual / divergent orchestrators (Score↔Pattern order diverge) | Arch N-04, Runtime |

### High Priority Issues

| ID | Issue | Source |
|----|-------|--------|
| H1 | RuleContext Builder computes business facts (useful_god, temperature, strength, shensha) | Arch N-05 |
| H2 | Hardcoded signal maps / thresholds vs Database-first | Arch N-06 |
| H3 | Interpretation embeds Knowledge load / match / priority | Arch N-07, Runtime |
| H4 | API `bazi_truth` enrichment + chart sync | Arch N-08 |
| H5 | Missing / mismatched runtime context types | Arch N-09 |
| H6 | Priority Knowledge bypass (`for_matched_rules`; 08 KB unused / loader fragile) | Arch N-10, Knowledge |
| H7 | Knowledge checklist mismatch + dead libraries on production path | Knowledge |
| H8 | Broken `02_dictionary/na_yin.json`; 104 duplicate rule IDs | Knowledge |
| H9 | Context Registry missing; Version Manager missing | Runtime |

### Medium Priority Issues

| ID | Issue | Source |
|----|-------|--------|
| M1 | Stage 0 Input Validation not a pipeline stage | Arch N-11 |
| M2 | Feng Shui not first-class Stage 3 | Arch N-12 |
| M3 | Legacy ReportBuilder scoring path | Arch N-13 |
| M4 | `strength.level` dual write | Arch N-14 |
| M5 | No `tests/architecture/` suite | Arch N-16, Testing |
| M6 | Low rule match utilization (~22%); many no-condition assets | Knowledge |
| M7 | Templates / sentences unused on production Report | Knowledge |
| M8 | HTTP-only metrics/logging; no stage SLOs | Runtime |
| M9 | Readiness health ≠ liveness | Runtime |

### Low Priority Issues

| ID | Issue | Source |
|----|-------|--------|
| L1 | Calendar `can_chi` enriched from BaZi in orchestrator view | Arch N-15 |
| L2 | Extra `narrative` stage vs contract Stages 0–12 naming | Runtime |
| L3 | Root `knowledge/` empty of executable modules (docs-only) — confusing entrypoint | Knowledge |
| L4 | Scattered `__version__` constants without compatibility matrix | Runtime |

---

## Roadmap

Assumes 1–2 engineers familiar with the codebase; minimal-change / backward-compatible posture; ADR when choosing waive vs remediating.

### Sprint 1 — Freeze blockers (ownership & mutation)

**Goal:** Clear Critical path or ADR-waive with explicit V1 stage map.

| Work | Outcome |
|------|---------|
| ADR: Collapsed V1 vs full Stages 0–12 | Decision record |
| Single orchestrator SSOT (deprecate or align Integration Score→Pattern) | One execution order |
| Extract Stage 5 RuleContext publish from Pattern (or ADR Pattern-hosts-RC) | Ownership clarity |
| Stop in-place RuleContext mutation by Score (compose Score slice / ScoreContext) | Immutability |
| Module tests for Pattern / Score / orchestrator order | Safety net |

**Exit:** C1–C4 resolved **or** formally waived; production path documented as V1 stage map.

### Sprint 2 — Knowledge layer honesty

**Goal:** Make Knowledge/Priority production contract truthful.

| Work | Outcome |
|------|---------|
| Priority strategy ADR (wire 08 KB vs adopt MatchedRuleResolver as V1) | H6 closed |
| Fix PriorityRuleLoader multi-JSON **if** wiring 08 | Loader usable |
| Fix `na_yin.json`; dedupe policy for rule IDs | Asset integrity |
| Dead-asset policy (phrase/templates/sentences: wire / defer / archive) | H7 closed |
| Knowledge version stamp | Traceability |
| Optional: begin extract Stages 7–9 from Interpretation (thin wrappers OK) | Align toward N-07 |

**Exit:** Knowledge Freeze for **rule DB + Priority strategy**; checklist gaps documented.

### Sprint 3 — Producer purity & API boundary

**Goal:** Reduce High ownership bleed.

| Work | Outcome |
|------|---------|
| Move Builder-computed facts to owning engines (useful_god / temperature / strength) | H1 |
| Relocate API BaZi enrichment into Bazi Engine (API serializes only) | H4 |
| Quarantine legacy ReportBuilder scoring | M3 |
| Feng Shui as optional named stage / FengShuiContext | M2 |
| Stage 0 input validation stub | M1 |
| Begin named context types (wrappers OK for BC) | H5 |

**Exit:** High ownership issues largely closed; Builder closer to transport-only.

### Sprint 4 — Runtime services & architecture tests

**Goal:** Ops + compliance gates.

| Work | Outcome |
|------|---------|
| `tests/architecture/` — order, no RC mutation, single orchestrator | M5 |
| Context Registry (minimal) | H9 |
| Stage logging + stage duration metrics | M8 |
| Readiness health (engines + knowledge load smoke) | M9 |
| Version Manager smoke gate | H9 |
| Delivery Stage 12 thin adapter (document narrative placement) | C1 residual |
| Database-first signal map migration plan (incremental) | H2 start |

**Exit:** Architecture Freeze candidate **if** Sprint 1–3 exits met; Runtime MOSTLY READY for beta ops.

---

## Estimates

### Remaining work (scope)

| Bucket | Scope |
|--------|-------|
| Critical (C1–C4) | Stage identity + RC ownership + orchestrator SSOT |
| High (H1–H9) | Producer purity, Knowledge/Priority honesty, contexts, runtime registry/version |
| Medium (M1–M9) | Stage 0/3, legacy report, tests/architecture, utilization, ops signals |
| Low (L1–L4) | View cleanup, naming, docs index |

### Approximate implementation effort

| Phase | Effort (eng-weeks) | Notes |
|-------|-------------------:|-------|
| Sprint 1 | 2–3 | Highest design risk; keep wrappers for BC |
| Sprint 2 | 2–3 | Priority ADR may shrink code work |
| Sprint 3 | 3–4 | Touches Builder / Bazi / API — careful BC |
| Sprint 4 | 2–3 | Mostly additive services + tests |
| **Total to Architecture Freeze candidate** | **9–13 eng-weeks** | Assuming ADR choices that avoid full rewrite |
| Full Stages 0–12 + DB-first maps + full KB utilization | **+8–16 eng-weeks** | Stretch / V1.1–V1.2 |

*Estimates assume no Golden Dataset / snapshot edits; prefer source fixes + wrappers.*

### Architecture risk

| Risk | Level | Note |
|------|-------|------|
| Doc–runtime divergence continues | **High** | Freeze without ADR = false confidence |
| Dual orchestrator wrong-order bugs | **High** | Integration path Score before Pattern |
| RC mutation subtle match bugs | **High** | Interpretation depends on mutated facts |
| Priority KB vs resolver mismatch | **Medium–High** | Commercial rule conflict policy unclear |
| Dead KB marketed as live | **Medium** | Templates/sentences unused |
| Large Stage 7–9 extract break Interpretation | **Medium** | Needs wrappers / phased extract |

**Overall architecture risk: HIGH** until Sprint 1 exit.

### Technical debt

| Debt class | Severity | Examples |
|------------|----------|----------|
| Structural | High | Collapsed stages; Pattern owns RC; Interpretation owns Knowledge |
| Contract | High | Missing context types; MutableMapping RuleContext |
| Knowledge | High | Dead libraries; checklist mismatch; Priority bypass |
| Dual paths | High | Three orchestrators / pipelines |
| Ops | Medium | No Context Registry / Version Manager / stage metrics |
| Legacy | Medium | ReportBuilder scoring; Style loaders |
| Data quality | Medium | Dup rule IDs; broken na_yin.json |
| Test gap | Medium | No architecture compliance suite |

**Technical debt posture: HIGH** — manageable if ADRs freeze V1 scope; dangerous if treated as already-aligned.

---

## Decision Gates

| Question | Answer |
|----------|--------|
| Ready for internal demo? | **MOSTLY READY** |
| Ready for Architecture Freeze? | **NOT READY** (unless ADR waives C1–C4) |
| Ready for Knowledge Freeze (full)? | **NOT READY** |
| Ready for limited production beta? | **PARTIALLY READY** (with limitations list) |
| Ready for commercial “full platform” claim? | **NOT READY** |

### Recommended next action

1. Leadership ADR: **Remediate** vs **Ratify collapsed V1**.  
2. Execute Sprint 1 either way (SSOT orchestrator + immutability still valuable under waiver).  
3. Do **not** expand Report Binding onto unused template/sentence layers until Knowledge policy is frozen.

---

## Source Report Index

| Report | Path | Key score |
|--------|------|-----------|
| Architecture Compliance | `docs/reports/ARCHITECTURE_COMPLIANCE_REPORT.md` | Overall 58% / Arch 55% — PARTIALLY READY |
| Architecture Trace | `docs/reports/ARCHITECTURE_TRACE_REPORT.md` | N-01…N-16 locations |
| Knowledge Compliance | `docs/reports/KNOWLEDGE_COMPLIANCE_REPORT.md` | Knowledge Health 42% |
| Pipeline Runtime | `docs/reports/PIPELINE_RUNTIME_REPORT.md` | Pipeline 48% / Runtime services 35% |

---

**END OF REPORT** — No code modified. No patches applied.
