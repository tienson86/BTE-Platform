# Architecture Compliance Report

| Item | Value |
|------|-------|
| Document | ARCHITECTURE_COMPLIANCE_REPORT.md |
| Project | BTE Platform V1.0 |
| Audit Type | Architecture Compliance (READ-ONLY) |
| Contracts | `docs/architecture/SYSTEM_DATA_FLOW.md`, `docs/architecture/PIPELINE_ARCHITECTURE.md` |
| Production Path | `applications/api/services/orchestrator.py` |
| Date | 2026-07-28 |
| Auditor Role | Architecture Auditor |

**Constraints honored:** No source modifications, no patches, no refactors, no commits.

---

## Executive Summary

The production API path implements a **collapsed** version of the documented Stages 0–12 pipeline. Core calculation engines (Calendar, BaZi, Pattern, Score, Interpretation, Report) exist and execute forward in a usable order, but several architecture contracts are violated: stage isolation, immutable contexts, single producer ownership, and knowledge-layer separation.

| Score | Value | Meaning |
|-------|------:|---------|
| **Overall Compliance** | **58%** | Partial — runnable but not contract-aligned |
| **Architecture Score** | **55%** | Layer/stage contracts partially met |
| **Pipeline Score** | **52%** | Stages collapsed; dual orchestrators |
| **Knowledge Score** | **48%** | Loader/matcher exist; Priority KB bypass; hardcoded maps |
| **Runtime Score** | **45%** | Runtime services mostly missing/fragmented |
| **Report Score** | **70%** | Production render path clean; legacy scoring residual |

### Verdict (preview)

**PARTIALLY READY** for Architecture Freeze.

Freeze is **not** recommended until Critical/High violations on stage identity, RuleContext ownership, and RuleContext mutation are resolved or formally waived by ADR.

---

## Fully Compliant

Modules / behaviors that align with architecture contracts on the **production** path:

| Module | Why compliant |
|--------|----------------|
| **Calendar Engine** (`engines/calendar_engine`) | Produces calendar data only; does not interpret or render |
| **Feng Shui Engine** (side branch) | Optional; does not alter BaZi / Pattern / Score business pipeline |
| **Pattern CSV loader** (`database/14_pattern`) | Does not load Interpretation Knowledge `05_rule_database` |
| **Production Report path** (`ReportEngine.render_from_analysis`) | Renders from `AnalysisResult.interpretation`; no rule matching |
| **Portal presenters (intent)** | Documented as presentation-only; do not call engines |
| **Orchestrator intent** | Applications layer coordinates Public APIs; no embedded BaZi math |
| **Forward calculation chain (high level)** | Calendar → BaZi → Pattern → Score → Interpretation → Report |
| **Interpretation production RuleContext path** | When `is_rule_context`, does not rebuild RuleContext |
| **KnowledgeRuleLoader constraints (partial)** | Loads/organizes rules; does not resolve priority conflicts itself |
| **Rule Matcher constraints (partial)** | Matches conditions; does not render HTML/PDF |

---

## Partial Compliance

| Module | Status | Why partial |
|--------|--------|-------------|
| **OrchestratorService** | Partial | Works as SSOT for API, but `PIPELINE_ORDER` omits Stages 0, 3, 5, 7–9, 12 as first-class stages |
| **Pattern Engine** | Partial | Detects pattern; also **hosts** RuleContext build + enrich (Stage 5 bleed) |
| **RuleContext Builder** (`rule_contract`) | Partial | Exists as library, but **computes** useful_god / temperature / strength heuristics (not transport-only) |
| **Score Engine** | Partial | Scores correctly, but **mutates** shared RuleContext after publication |
| **Interpretation Engine** | Partial | Consumes RuleContext; also **embeds** Knowledge load + Match + Priority (Stages 7–9) |
| **Priority path** | Partial | `MatchedRuleResolver` runs; `08_priority_rules` PriorityRuleLoader / PR* pipeline not production-wired |
| **Bazi Engine** | Partial | Owns pillars/hidden/ten_gods/shensha; API `bazi_truth` re-enriches and syncs chart |
| **Report Engine** | Partial | Production render OK; legacy `report_builder` still calls scoring |
| **API layer** | Partial | Delivers AnalysisResult; also enriches BaZi (nap_am, truong_sinh) and shapes calendar |
| **Logging / Metrics / Health** | Partial | Middleware / monitoring / health routes exist; not stage-level Runtime Services |
| **Cache** | Partial | Per-engine caches; no platform Cache Manager |
| **Config** | Partial | Per-app/engine config; no unified Configuration Manager |

---

## Non-Compliant

### N-01 — Collapsed Stages 5 / 7–9 / 12

| Field | Detail |
|-------|--------|
| **Architecture Rule** | PIPELINE_ARCHITECTURE §8–9: Stages 0–12 execute as distinct sequential stages; Knowledge = Stages 7–9; RuleContext = Stage 5; Delivery = Stage 12 |
| **Current Implementation** | `PIPELINE_ORDER = calendar → bazi → pattern → score → interpretation → report → narrative`. RuleContext built inside Pattern. Knowledge/Matcher/Priority inside `InterpretationEngine.run()`. Delivery = API JSON return |
| **Expected Implementation** | Explicit Stage 5 RuleContext Builder; Stages 7–9 publish KnowledgeContext / MatchedRuleSet / ResolvedRuleSet; Stage 12 Delivery service |
| **Severity** | **Critical** |

---

### N-02 — Score mutates published RuleContext

| Field | Detail |
|-------|--------|
| **Architecture Rule** | PIPELINE_ARCHITECTURE §4.3 Immutable Runtime Context; SYSTEM_DATA_FLOW §3.4; Score owns ScoreContext only |
| **Current Implementation** | `ScoreEngine.append_score_to_rule_context()` writes `rule_context["score"]`, overwrites `strength.level`, rewrites `facts` (orchestrator after Score) |
| **Expected Implementation** | Publish immutable `ScoreContext` / `ScoreResult`; Interpretation consumes Score + RuleContext without mutating RuleContext; strength.level owned solely by Score output model |
| **Severity** | **Critical** |

---

### N-03 — RuleContext constructed by Pattern Engine

| Field | Detail |
|-------|--------|
| **Architecture Rule** | SYSTEM_DATA_FLOW §6.6; PIPELINE Stage 5: Only RuleContext Builder publishes RuleContext |
| **Current Implementation** | `PatternEngine.calculate` → `rule_context_bridge.build_rule_context` → `RuleContextBuilder.build` |
| **Expected Implementation** | Dedicated Stage 5 service/engine publishes RuleContext after PatternResult; Pattern does not own RuleContext publication |
| **Severity** | **Critical** |

---

### N-04 — Dual / divergent orchestrators

| Field | Detail |
|-------|--------|
| **Architecture Rule** | PIPELINE_ARCHITECTURE §3 / §13: all entry points converge to the same pipeline |
| **Current Implementation** | Production: `applications/api/services/orchestrator.py`. Legacy: `engines/integration/orchestrator.py` runs **Score before Pattern**. Legacy: `api/services/pipeline_service.py` / `engines/base/pipeline.py` alternate bag |
| **Expected Implementation** | Single canonical orchestrator; legacy paths deprecated or adapted to same stage order |
| **Severity** | **Critical** |

---

### N-05 — RuleContext Builder computes business facts

| Field | Detail |
|-------|--------|
| **Architecture Rule** | SYSTEM_DATA_FLOW §6.6: RuleContext consolidates only; does not create business facts. Pattern owns Useful God / Temperature (§6.5 / §3.3) |
| **Current Implementation** | `RuleContextBuilder` derives `useful_god` (incl. hy/ky), `temperature.status`, strength heuristics, shensha fallback detection, many `facts.*` |
| **Expected Implementation** | Upstream engines produce those SSOT fields; Builder maps/copies into RuleContext only |
| **Severity** | **High** |

---

### N-06 — Hardcoded knowledge / signal maps

| Field | Detail |
|-------|--------|
| **Architecture Rule** | Database / Knowledge as passive SSOT; Engines decide using loaded knowledge (SYSTEM_DATA_FLOW §4; workspace Database-first rules) |
| **Current Implementation** | `engines/rule_contract/signal_maps.py` (ten gods, shensha, PATTERN_USEFUL_GOD); thresholds in builder/score; follow heuristics in `FollowPatternCalculator`; duplicated HIDDEN in `bazi_engine/engine.py` |
| **Expected Implementation** | Load maps/rules from Knowledge / Database loaders; no parallel hard-coded rule tables for SSOT decisions |
| **Severity** | **High** |

---

### N-07 — Interpretation embeds Knowledge Matching

| Field | Detail |
|-------|--------|
| **Architecture Rule** | SYSTEM_DATA_FLOW §6.11: Interpretation shall not Evaluate Rules. Stages 7–9 are Knowledge Layer |
| **Current Implementation** | `InterpretationEngine.run` loads rules, matches, scores, applies priority, then builds interpretation |
| **Expected Implementation** | Interpretation consumes `ResolvedRuleSet` (+ contexts); matching/priority are upstream stages |
| **Severity** | **High** |

---

### N-08 — API BaZi enrichment / chart sync

| Field | Detail |
|-------|--------|
| **Architecture Rule** | Portal/API MUST NOT execute business logic; Bazi Engine is SSOT for chart structures |
| **Current Implementation** | `applications/api/services/bazi_truth.py` loads CSV, computes ten_god/nap_am/truong_sinh; `sync_chart_from_view` mutates `BaziChart` |
| **Expected Implementation** | Enrichment inside Bazi Engine (or dedicated BaZi enrich producer); API only serializes |
| **Severity** | **High** |

---

### N-09 — Missing / mismatched runtime context types

| Field | Detail |
|-------|--------|
| **Architecture Rule** | Contract-first contexts: InputRequestContext, CalendarContext, BaziContext, KnowledgeContext, MatchedRuleSet, ResolvedRuleSet, ReportDocument, etc. |
| **Current Implementation** | Production uses `CalendarResult`, `BaziChart`, plain `dict` RuleContext, lists for matched/resolved rules, `ReportResult` / portal dicts. Several documented types absent |
| **Expected Implementation** | Named context contracts published per stage |
| **Severity** | **High** |

---

### N-10 — Priority Knowledge bypass on production path

| Field | Detail |
|-------|--------|
| **Architecture Rule** | Stage 9 Priority Resolution uses Priority Rule Database |
| **Current Implementation** | `PriorityService.for_matched_rules()` — section/confidence resolver, **no** `08_priority_rules` load. `PriorityRuleLoader` fails on multi-JSON `priority_rules.json` when used |
| **Expected Implementation** | Priority Engine loads/validates 08 KB and resolves conflicts accordingly |
| **Severity** | **High** |

---

### N-11 — Stage 0 Input Validation not a pipeline stage

| Field | Detail |
|-------|--------|
| **Architecture Rule** | Stage 0 validates/normalizes InputRequest before Calendar |
| **Current Implementation** | Implicit datetime checks inside engines; no published InputRequestContext stage in orchestrator |
| **Expected Implementation** | Explicit validation stage with fail-fast contract |
| **Severity** | **Medium** |

---

### N-12 — Feng Shui not a first-class Stage 3

| Field | Detail |
|-------|--------|
| **Architecture Rule** | Stage 3 optional Feng Shui publishes FengShuiContext |
| **Current Implementation** | Always attempted after BaZi; not in `PIPELINE_ORDER`; merged into calendar payload via `_shape_calendar` |
| **Expected Implementation** | Optional Stage 3 with dedicated published context |
| **Severity** | **Medium** |

---

### N-13 — Legacy Report scoring path

| Field | Detail |
|-------|--------|
| **Architecture Rule** | Report Engine shall never calculate business data |
| **Current Implementation** | `engines/report_engine/report_builder.py` calls `self.scoring.calculate(...)` (legacy path) |
| **Expected Implementation** | Remove/quarantine; production-only render |
| **Severity** | **Medium** |

---

### N-14 — strength.level dual write

| Field | Detail |
|-------|--------|
| **Architecture Rule** | SSOT: strength.level → Score Engine |
| **Current Implementation** | Initial heuristic in RuleContextBuilder at Pattern time; later overwritten by Score append |
| **Expected Implementation** | Single Score producer; no pre-Score authoritative level in RuleContext |
| **Severity** | **Medium** |

---

### N-15 — Calendar can_chi enriched from BaZi in orchestrator

| Field | Detail |
|-------|--------|
| **Architecture Rule** | Calendar owns Year/Month/Day/Hour Stem Branch (SYSTEM_DATA_FLOW §6.2); one-way flow |
| **Current Implementation** | Orchestrator `_shape_calendar` copies pillar can_chi from BaZi into calendar view |
| **Expected Implementation** | Calendar owns can_chi, or view layer clearly marks BaZi-owned fields without mutating Calendar SSOT |
| **Severity** | **Low** |

---

### N-16 — No architecture test suite

| Field | Detail |
|-------|--------|
| **Architecture Rule** | Contract-first + pipeline determinism; tests should guard stage order/ownership |
| **Current Implementation** | No `tests/architecture/`; pipeline/golden/report/API phase tests exist but do not enforce Stages 0–12 contracts |
| **Expected Implementation** | Architecture compliance tests (order, immutability, single producer) |
| **Severity** | **Medium** |

---

## Missing Components

Documented in PIPELINE_ARCHITECTURE / SYSTEM_DATA_FLOW but **not implemented** as first-class runtime components:

| Component | Architecture reference | Status |
|-----------|------------------------|--------|
| Stage 0 Input Validation service | PIPELINE § Stage 0 | NOT IMPLEMENTED (as stage) |
| Stage 5 RuleContext Builder (orchestrated stage) | PIPELINE Stage 5 | Library exists; **not** orchestrated stage |
| Stage 7 Knowledge Loading (orchestrated) | PIPELINE Stage 7 | Embedded inside Interpretation |
| Stage 8 Rule Matching (orchestrated) | PIPELINE Stage 8 | Embedded inside Interpretation |
| Stage 9 Priority Resolution (KB-backed) | PIPELINE Stage 9 | Partial resolver only |
| Stage 12 Delivery Pipeline | PIPELINE Stage 12 | NOT IMPLEMENTED |
| InputRequestContext | Context contracts | NOT IMPLEMENTED |
| KnowledgeContext type | Context contracts | NOT IMPLEMENTED |
| MatchedRuleSet / ResolvedRuleSet types | Context contracts | NOT IMPLEMENTED |
| FengShuiContext type | Context contracts | NOT IMPLEMENTED (`GuaResult` used) |
| ReportDocument type | Context contracts | NOT IMPLEMENTED (`ReportResult` / portal dict) |
| Context Manager | Runtime Service Summary §58 | NOT IMPLEMENTED |
| Logging Service (stage-level) | §58 | NOT IMPLEMENTED (HTTP middleware only) |
| Metrics Service (stage/rule metrics) | §58 | NOT IMPLEMENTED (HTTP metrics partial) |
| Cache Manager (platform) | §58 | NOT IMPLEMENTED (fragmented) |
| Version Manager | §58 | NOT IMPLEMENTED |
| Configuration Manager (unified) | §58 | NOT IMPLEMENTED (fragmented) |
| Health Check Service (engine/KB readiness) | §58 | PARTIAL (storage/config health) |
| `tests/architecture` | Governance / compliance | NOT IMPLEMENTED |

> Per audit instructions: missing postponed services are marked **NOT IMPLEMENTED**, not automatically treated as product bugs if intentionally deferred — but they remain **architecture gaps** relative to the written contract.

---

## Dead Code

| Category | Items |
|----------|-------|
| **Unused / divergent orchestrators** | `engines/integration/orchestrator.py` (Score→Pattern order); `api/services/pipeline_service.py` + `engines/base/pipeline.py` legacy bag |
| **Unused Priority KB path (production)** | `PriorityRuleLoader` / full `08_priority_rules` PR* pipeline not used by `for_matched_rules()` |
| **Unused context names** | Documented `CalendarContext` / `BaziContext` / `ScoreContext` types exist in models but production prefers `CalendarResult` / `BaziChart` / `ScoreResult` |
| **Unused Knowledge assets (runtime)** | Labels/examples JSON skipped; many no-condition JSON files; `follow_pattern_actions.json` with no action executor (see Knowledge Usage Audit) |
| **Legacy report scoring** | `report_engine/report_builder.py` scoring call path |
| **Alternate interpretation pipelines** | Deprecated/stub paths noted in `InterpretationEngine` module docstring (`pipeline.InterpretationPipeline`, stub builders) |
| **Legacy Pattern calculators** | Partially unused stubs historically; follow detect now wired — retain audit of unused combination/special paths as needed |

---

## Recommendations

Recommendations only — **no implementation**.

1. **Declare Architecture Freeze blockers**  
   Treat N-01, N-02, N-03, N-04 as freeze blockers unless waived by ADR.

2. **Publish an ADR for collapsed stages**  
   If Stages 5/7–9 remain inside Pattern/Interpretation for V1, document the approved merge and update PIPELINE_ARCHITECTURE — or split stages to match the contract.

3. **Stop mutating RuleContext after Pattern publication**  
   Score should publish ScoreResult only; sync strength into a Score-owned slice consumed by Interpretation without rewriting Pattern-era RuleContext facts in place.

4. **Make RuleContext Builder transport-only**  
   Move useful_god / temperature / strength / shensha detection to owning engines (Pattern / Score / BaZi) per SYSTEM_DATA_FLOW ownership tables.

5. **Retire or quarantine divergent orchestrators**  
   Integration and legacy API pipelines must not remain callable with different stage order.

6. **Align runtime type names with contracts**  
   Introduce or alias InputRequestContext, KnowledgeContext, MatchedRuleSet, ResolvedRuleSet, ReportDocument — or revise architecture docs to match production names.

7. **Wire or formally defer Priority KB**  
   Either fix PriorityRuleLoader multi-JSON and use Stage 9 KB resolution, or document MatchedRuleResolver as the V1 Priority contract.

8. **Move API BaZi enrichment into BaZi Engine**  
   Keep API as serializer of BaziView only.

9. **Add architecture tests**  
   Stage order, immutability of published contexts, single orchestrator entry, Report no-scoring invariant.

10. **Do not start Report/Portal structural binding** until ownership/immutability ADRs are accepted — binding on unstable producers amplifies debt.

---

## Final Assessment

| Question | Answer |
|----------|--------|
| Matches Stages 0–12 as written? | **No** (collapsed) |
| Single producer / immutable contexts? | **No** (RuleContext mutation + dual producers) |
| Knowledge layer isolated? | **Partial** |
| Report render-only (production)? | **Mostly yes** |
| Runtime services complete? | **No** |
| Ready for Architecture Freeze? | **PARTIALLY READY** |

### Freeze recommendation

**PARTIALLY READY**

The platform has a working forward pipeline and several engines that respect single-responsibility at a coarse level. It is **not READY** for a strict Architecture Freeze against the current written contracts without either:

- (A) remediating Critical/High non-compliance items, or  
- (B) amending the Architecture Contracts via ADR to ratify the collapsed V1 runtime.

Until (A) or (B) is completed, treat the architecture as **contract-divergent but operationally usable**.

---

## Appendix A — Production Stage Mapping

| Doc Stage | Production reality |
|-----------|-------------------|
| 0 Input Validation | Implicit / engine-level |
| 1 Calendar | `CalendarEngine.build` |
| 2 BaZi | `BaziEngine.build` + API `bazi_truth` enrich |
| 3 Feng Shui | Side call; not in `PIPELINE_ORDER` |
| 4 Pattern | `PatternEngine.calculate` |
| 5 RuleContext | Inside Pattern (`rule_context_bridge`) |
| 6 Score | `ScoreEngine.calculate` + **mutates RC** |
| 7 Knowledge | Inside `InterpretationEngine.run` |
| 8 Matcher | Inside `InterpretationEngine.run` |
| 9 Priority | `MatchedRuleResolver` inside Interpretation |
| 10 Interpretation | Same `run()` after priority |
| 11 Report | `ReportEngine.render_from_analysis` |
| 12 Delivery | API response / Portal consume JSON |

---

## Appendix B — Producer Ownership Snapshot (SSOT vs Actual)

| Field / Context | Contract Producer | Actual Producer | Compliant? |
|-----------------|-------------------|-----------------|------------|
| CalendarResult / solar_term | Calendar Engine | Calendar Engine | Yes |
| Four Pillars | BaZi Engine | BaZi Engine | Yes |
| shensha list | BaZi Engine | BaZi Engine (+ RC fallback) | Partial |
| Pattern / tong_cach | Pattern Engine | Pattern Engine | Yes |
| dung_than / hy / ky | Pattern Engine | Pattern view ← RuleContextBuilder | Partial |
| temperature.status | Pattern Engine (doc) | RuleContextBuilder | No |
| RuleContext | RuleContext Builder (Stage 5) | Pattern Engine call site | No |
| Score totals | Score Engine | Score Engine | Yes |
| strength.level | Score Engine | Builder then Score mutate | No |
| KnowledgeContext | Knowledge Loader | Implicit list in Interpretation | Partial |
| MatchedRuleSet | Rule Matcher | Inside Interpretation | Partial |
| ResolvedRuleSet | Priority Engine | MatchedRuleResolver | Partial |
| InterpretationResult | Interpretation Engine | Interpretation Engine | Yes |
| ReportDocument | Report Engine | ReportResult / portal dict | Partial |

---

## Appendix C — Test Landscape

| Area | Location | Architecture coverage |
|------|----------|----------------------|
| Pipeline / integration | `tests/integration/`, `tests/test_pipeline.py` | Behavioral; not Stages 0–12 contract |
| Golden Dataset | `tests/golden_dataset/` | Output fidelity |
| Report | `tests/report/` | Engine/template |
| API phases | `applications/api/tests/test_phase*.py` | Unified truth slices |
| Architecture suite | — | **Missing** |

---

*End of Architecture Compliance Report*  
*READ-ONLY audit — no source code was modified.*
