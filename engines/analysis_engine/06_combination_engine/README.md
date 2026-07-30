# Combination Engine

| Field | Value |
|-------|-------|
| Module Path | `engines/analysis_engine/06_combination_engine` |
| Module Type | Analysis Engine Stage |
| Stage Order | 06 — Sixth analytical stage |
| Document Type | Architecture Baseline |
| Version | 1.0.0 |
| Status | Frozen |

---

# 1. Purpose

The Combination Engine evaluates natal chart structural relations: Heavenly Stem Combination, Earthly Branch Combination, Clash, Harm, Punishment, Destruction, Hidden Combination, and Transformation.

It is the sixth analytical stage of the Analysis Engine pipeline. Its purpose is to produce a single, deterministic, explainable Combination judgment that all downstream analytical stages may consume without re-deriving Combination logic.

The engine answers one question only:

> Which combination, clash, harm, punishment, destruction, hidden combination, and transformation relations are active in this natal chart, and how are conflicts resolved?

It does not recompute Strength, Temperature, Pattern, Useful God, or Ten Gods, and it does not generate narrative interpretation or reports.

---

# 2. Responsibilities

1. Accept validated AnalysisContext.
2. Read published `StrengthResult`, `TemperatureResult`, `PatternResult`, `UsefulGodResult`, and `TenGodsResult` from AnalysisContext.
3. Access Combination Knowledge exclusively through Knowledge SDK.
4. Evaluate Heavenly Stem Combinations.
5. Evaluate Earthly Branch Combinations.
6. Evaluate Clash, Harm, Punishment, and Destruction.
7. Evaluate Hidden Combination.
8. Evaluate Transformation success/failure and result classes.
9. Resolve priority and conflicts among competing outcomes.
10. Compute Combination confidence where declared.
11. Record KnowledgeReferences, rejected alternatives, diagnostics, and execution metadata.
12. Publish immutable `CombinationResult`.

---

# 3. Scope

In scope:

- Heavenly Stem Combination
- Earthly Branch Combination
- Clash
- Harm
- Punishment
- Destruction
- Hidden Combination
- Transformation
- Priority / Conflict Resolution
- Confidence and explainability artifacts
- Publication of `CombinationResult`

---

# 4. Out of Scope

| Concern | Owning Stage |
|---------|--------------|
| Strength recomputation | Strength Engine |
| Temperature recomputation | Temperature Engine |
| Pattern recomputation | Pattern Engine |
| Useful God recomputation | Useful God Engine |
| Ten Gods recomputation | Ten Gods Engine |
| ShenSha detection | ShenSha Engine |
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
| Combination Knowledge | Knowledge SDK (frozen KnowledgeSession) |

Upstream results are never accepted as separate function parameters.

---

# 6. Output

```text
CombinationResult
```

---

# 7. Public API

```text
CombinationEngine.evaluate(context: AnalysisContext) -> CombinationResult
```

---

# 8. Position in Pipeline

```text
Ten Gods Engine
        │
        ▼
Combination Engine          ← this module
        │
        ▼
ShenSha Engine
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
