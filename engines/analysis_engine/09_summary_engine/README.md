# Summary Engine

| Field | Value |
|-------|-------|
| Module Path | `engines/analysis_engine/09_summary_engine` |
| Module Type | Analysis Engine Stage |
| Stage Order | 09 — Ninth and final analytical stage |
| Document Type | Architecture Baseline |
| Version | 1.0.0 |
| Status | Frozen |

---

# 1. Purpose

The Summary Engine consolidates all published analytical stage results into a unified cross-stage summary.

It is the ninth and final analytical stage of the Analysis Engine pipeline. Its purpose is to produce a single, deterministic, explainable `SummaryResult` that completes `AnalysisResult` for downstream Interpretation and Report engines.

The engine answers one question only:

> What is the consolidated analytical picture of this natal chart across all completed analysis stages?

It does not recompute Strength, Temperature, Pattern, Useful God, Ten Gods, Combination, ShenSha, or Luck, and it does not generate narrative interpretation or reports.

---

# 2. Responsibilities

1. Accept validated AnalysisContext containing all upstream stage results.
2. Read published results for Strength, Temperature, Pattern, Useful God, Ten Gods, Combination, ShenSha, and Luck.
3. Validate completeness and cross-stage consistency.
4. Aggregate domain summaries without altering upstream semantics.
5. Consolidate confidence and explainability evidence across stages.
6. Record aggregation diagnostics and execution metadata.
7. Publish immutable `SummaryResult`.
8. Enable `AnalysisResult` finalization by the Analysis Runtime orchestrator.

---

# 3. Scope

In scope:

- Aggregation of StrengthResult
- Aggregation of TemperatureResult
- Aggregation of PatternResult
- Aggregation of UsefulGodResult
- Aggregation of TenGodsResult
- Aggregation of CombinationResult
- Aggregation of ShenShaResult
- Aggregation of LuckResult
- Cross-stage consistency validation
- Consolidated confidence summary
- Consolidated evidence / KnowledgeReference index
- Publication of `SummaryResult`

---

# 4. Out of Scope

| Concern | Owning Stage |
|---------|--------------|
| Strength recomputation | Strength Engine |
| Temperature recomputation | Temperature Engine |
| Pattern recomputation | Pattern Engine |
| Useful God recomputation | Useful God Engine |
| Ten Gods recomputation | Ten Gods Engine |
| Combination recomputation | Combination Engine |
| ShenSha recomputation | ShenSha Engine |
| Luck recomputation | Luck Engine |
| Natural-language interpretation | Interpretation Engine |
| Report rendering | Report Engine |
| Domain knowledge rule execution | Upstream stage engines |

---

# 5. Inputs

| Input | Source |
|-------|--------|
| AnalysisContext | Analysis Runtime / Orchestrator |
| StrengthResult | `AnalysisContext.strength_result` |
| TemperatureResult | `AnalysisContext.temperature_result` |
| PatternResult | `AnalysisContext.pattern_result` |
| UsefulGodResult | `AnalysisContext.useful_god_result` |
| TenGodsResult | `AnalysisContext.ten_gods_result` |
| CombinationResult | `AnalysisContext.combination_result` |
| ShenShaResult | `AnalysisContext.shensha_result` |
| LuckResult | `AnalysisContext.luck_result` |

Upstream results are never accepted as separate function parameters.

---

# 6. Output

```text
SummaryResult
```

---

# 7. Public API

```text
SummaryEngine.evaluate(context: AnalysisContext) -> SummaryResult
```

---

# 8. Position in Pipeline

```text
Luck Engine
        │
        ▼
Summary Engine              ← this module
        │
        ▼
AnalysisResult
        │
        ▼
Interpretation Engine
```

---

# 9. Design Principles

- Single responsibility (consolidation only)
- Deterministic
- Stateless
- No upstream recomputation
- Non-destructive aggregation
- Explainability preservation
- Immutable results
- Fail-closed validation

---

# 10. Version

| Item | Value |
|------|-------|
| Module Version | 1.0.0 |
| Status | Frozen |

Breaking semantic changes require a major version increment.

---

## Architecture Coexistence

This directory is part of the **legacy stage documentation/engine tree**.

Canonical architecture skeleton packages live at the Analysis Engine root (`models/`, `pipeline/`, `analyzers/`, `registry/`, `validation/`, …).

See `engines/analysis_engine/README.md` and `ANALYSIS_ENGINE_AUDIT.md`.
