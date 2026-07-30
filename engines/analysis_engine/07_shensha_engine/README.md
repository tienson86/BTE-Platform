# ShenSha Engine

| Field | Value |
|-------|-------|
| Module Path | `engines/analysis_engine/07_shensha_engine` |
| Module Type | Analysis Engine Stage |
| Stage Order | 07 — Seventh analytical stage |
| Document Type | Architecture Baseline |
| Version | 1.0.0 |
| Status | Frozen |

---

# 1. Purpose

The ShenSha Engine detects and evaluates ShenSha (Thần Sát / 神煞) in the natal chart: auspicious and inauspicious stars, their presence, interactions, compatibility, and exceptions.

It is the seventh analytical stage of the Analysis Engine pipeline. Its purpose is to produce a single, deterministic, explainable ShenSha judgment that all downstream analytical stages may consume without re-deriving ShenSha logic.

The engine answers one question only:

> Which ShenSha are present in this natal chart, how do they interact, and what is their analytical classification?

It does not recompute Strength, Temperature, Pattern, Useful God, Ten Gods, or Combination, and it does not generate narrative interpretation or reports.

---

# 2. Responsibilities

1. Accept validated AnalysisContext.
2. Read published upstream stage results from AnalysisContext.
3. Access ShenSha Knowledge exclusively through Knowledge SDK.
4. Evaluate ShenSha presence using calculation references and lookup tables.
5. Classify Auspicious and Inauspicious ShenSha.
6. Evaluate interaction rules among co-present ShenSha.
7. Evaluate compatibility classes.
8. Apply exception overrides and suppressions.
9. Resolve priority and conflicts among competing outcomes.
10. Compute ShenSha confidence where declared.
11. Record KnowledgeReferences, rejected alternatives, diagnostics, and execution metadata.
12. Publish immutable `ShenShaResult`.

---

# 3. Scope

In scope:

- Auspicious ShenSha
- Inauspicious ShenSha
- Calculation References
- Lookup Tables
- Mapping Tables
- Priority Concepts
- Interaction Rules
- Compatibility
- Exceptions
- Confidence Concepts
- Publication of `ShenShaResult`

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
| Luck evaluation | Luck Engine |
| Summary / Interpretation / Report | Downstream engines |
| Direct Knowledge Module / Registry / Loader access | Forbidden — Knowledge SDK only |

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
| ShenSha Knowledge | Knowledge SDK (frozen KnowledgeSession) |

Upstream results are never accepted as separate function parameters.

---

# 6. Output

```text
ShenShaResult
```

---

# 7. Public API

```text
ShenShaEngine.evaluate(context: AnalysisContext) -> ShenShaResult
```

---

# 8. Position in Pipeline

```text
Combination Engine
        │
        ▼
ShenSha Engine              ← this module
        │
        ▼
Luck Engine
```

---

# 9. Design Principles

- Single responsibility
- Deterministic
- Stateless
- SDK-only knowledge access
- No upstream recomputation
- Explainable evidence
- Immutable results
- Fail-closed validation

---

# 10. Version

| Item | Value |
|------|-------|
| Module Version | 1.0.0 |
| Status | Frozen |

Breaking semantic changes require a major version increment.
