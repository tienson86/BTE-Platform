# Ten Gods Engine

| Field | Value |
|-------|-------|
| Module Path | `engines/analysis_engine/05_ten_gods_engine` |
| Module Type | Analysis Engine Stage |
| Stage Order | 05 — Fifth analytical stage |
| Document Type | Architecture Baseline |
| Version | 1.0.0 |
| Status | Frozen |

---

# 1. Purpose

The Ten Gods Engine evaluates the natal chart's Ten Gods (Thập Thần / 十神) structure, quality, favorability, interactions, and life-area analytical frames.

It is the fifth analytical stage of the Analysis Engine pipeline. Its purpose is to produce a single, deterministic, explainable Ten Gods judgment that all downstream analytical stages may consume without re-deriving Ten Gods logic.

The engine answers one question only:

> How do the Ten Gods present, interact, and qualify in this natal chart under published upstream analytical evidence?

It does not answer questions of Day Master strength recomputation, climate recomputation, Pattern recomputation, Useful God recomputation, combination structure as a dedicated stage, narrative meaning, or report presentation.

---

# 2. Responsibilities

The Ten Gods Engine is solely responsible for:

1. Accepting a validated analytical context produced after Calendar and BaZi construction.
2. Reading published `StrengthResult` from `AnalysisContext.strength_result`.
3. Reading published `TemperatureResult` from `AnalysisContext.temperature_result`.
4. Reading published `PatternResult` from `AnalysisContext.pattern_result`.
5. Reading published `UsefulGodResult` from `AnalysisContext.useful_god_result`.
6. Accessing Ten Gods Knowledge exclusively through the Knowledge SDK.
7. Evaluating Ten Gods identities and presence structure.
8. Evaluating relationship models among Ten Gods.
9. Evaluating strength, pattern, and useful-god interactions.
10. Evaluating favorability.
11. Evaluating personality, career, wealth, marriage, and health analytical concept tags.
12. Resolving priority and conflicts among competing Ten Gods outcomes.
13. Computing Ten Gods confidence.
14. Recording matched knowledge references, rejected alternatives, analytical reasoning, diagnostics, and execution metadata.
15. Publishing an immutable `TenGodsResult` for downstream consumption.

---

# 3. Scope

V1.0 scope is limited to **natal Ten Gods analysis**.

In scope:

- Ten Gods identity and presence evaluation
- Relationship model evaluation
- Strength / Temperature / Pattern / Useful God interaction evaluation as Ten Gods inputs
- Favorability determination
- Personality, career, wealth, marriage, and health analytical concept frames
- Priority and conflict resolution
- Confidence computation
- Deterministic traceability artifacts
- Publication of `TenGodsResult` into the Analysis Engine pipeline and `AnalysisResult`

The engine operates exclusively on structural chart facts, published upstream stage results attached to AnalysisContext, and Ten Gods Knowledge accessed through Knowledge SDK.

---

# 4. Out of Scope

| Concern | Owning Stage |
|---------|--------------|
| Day Master strength recomputation | Strength Engine |
| Climate recomputation | Temperature Engine |
| Pattern / Ge Ju recomputation | Pattern Engine |
| Useful God recomputation | Useful God Engine |
| Combination / clash / harm / transformation as dedicated stage | Combination Engine |
| ShenSha detection | ShenSha Engine |
| Luck pillar generation | Luck Engine |
| Cross-stage analytical summary | Summary Engine |
| Natural-language interpretation | Interpretation Engine |
| Report rendering | Report Engine |
| Calendar conversion | Calendar Engine |
| Pillar construction | BaZi Engine |
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
| Ten Gods Knowledge | Knowledge SDK (frozen KnowledgeSession) |

Upstream results are never accepted as separate function parameters.

---

# 6. Output

```text
TenGodsResult
```

Immutable, explainable, and published into AnalysisContext / AnalysisResult for downstream stages.

---

# 7. Public API

```text
TenGodsEngine.evaluate(context: AnalysisContext) -> TenGodsResult
```

---

# 8. Position in Pipeline

```text
Useful God Engine
        │
        ▼
Ten Gods Engine          ← this module
        │
        ▼
Combination Engine
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
