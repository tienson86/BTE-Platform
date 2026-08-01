# Luck Engine

| Field | Value |
|-------|-------|
| Module Path | `engines/analysis_engine/08_luck_engine` |
| Module Type | Analysis Engine Stage |
| Stage Order | 08 — Eighth analytical stage |
| Document Type | Architecture Baseline |
| Version | 1.0.0 |
| Status | Frozen |

---

# 1. Purpose

The Luck Engine evaluates natal chart fortune over time: Da Yun (Đại Vận), Liu Nian (Lưu Niên), Liu Yue (Lưu Nguyệt), Liu Ri (Lưu Nhật), and Liu Shi (Lưu Thời).

It is the eighth analytical stage of the Analysis Engine pipeline. Its purpose is to produce a single, deterministic, explainable Luck judgment that all downstream analytical stages may consume without re-deriving Luck logic.

The engine answers one question only:

> How do the luck layers interact with the natal chart over time, and what are their favorability and activation outcomes?

It does not recompute natal analytical domains, and it does not generate narrative interpretation or reports.

---

# 2. Responsibilities

1. Accept validated AnalysisContext.
2. Read published upstream stage results from AnalysisContext.
3. Access Luck Knowledge exclusively through Knowledge SDK.
4. Evaluate Da Yun sequence and decade-layer outcomes.
5. Evaluate Liu Nian year-layer outcomes.
6. Evaluate Liu Yue month-layer outcomes.
7. Evaluate Liu Ri day-layer outcomes.
8. Evaluate Liu Shi hour-layer outcomes.
9. Evaluate luck–natal interaction, timing principles, and activation rules.
10. Evaluate favorability and resolve priority/conflicts.
11. Compute Luck confidence where declared.
12. Record KnowledgeReferences, rejected alternatives, diagnostics, and execution metadata.
13. Publish immutable `LuckResult`.

---

# 3. Scope

In scope:

- Da Yun
- Liu Nian
- Liu Yue
- Liu Ri
- Liu Shi
- Luck Interaction
- Timing Principles
- Activation Rules
- Favorability Concepts
- Priority Concepts
- Confidence Concepts
- Publication of `LuckResult`

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
| Cross-stage analytical summary | Summary Engine |
| Interpretation / Report | Downstream engines |
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
| ShenShaResult | `AnalysisContext.shensha_result` |
| Luck Knowledge | Knowledge SDK (frozen KnowledgeSession) |

Upstream results are never accepted as separate function parameters.

---

# 6. Output

```text
LuckResult
```

---

# 7. Public API

```text
LuckEngine.evaluate(context: AnalysisContext) -> LuckResult
```

---

# 8. Position in Pipeline

```text
ShenSha Engine
        │
        ▼
Luck Engine                 ← this module
        │
        ▼
Summary Engine
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

---

## Architecture Coexistence

This directory is part of the **legacy stage documentation/engine tree**.

Canonical architecture skeleton packages live at the Analysis Engine root (`models/`, `pipeline/`, `analyzers/`, `registry/`, `validation/`, …).

See `engines/analysis_engine/README.md` and `ANALYSIS_ENGINE_AUDIT.md`.
