# Luck Engine Domain Models

**Module:** `engines/analysis_engine/08_luck_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the official domain model specification for the Luck Engine.

---

# 2. Design Principles

- Immutable by default
- Explicit ownership
- Strong typing
- Deterministic serialization
- Version compatibility
- Explainable analytical data
- No presentation concerns

---

# 3. Domain Model Overview

```text
AnalysisContext (Input)
        │
        │  reads upstream stage results
        │  accesses Knowledge SDK
        ▼
LuckEvaluationContext
        │
        ▼
DaYunAnalysis
LiuNianAnalysis
LiuYueAnalysis
LiuRiAnalysis
LiuShiAnalysis
LuckInteractionAnalysis
TimingAnalysis
ActivationAnalysis
FavorabilityAnalysis
        │
        ▼
PriorityResolution
ConflictResolution
ConfidenceEvaluation
        │
        ▼
LuckResult
```

No dedicated LuckInput wrapper is defined. Shared AnalysisContext is used directly.

---

# 4. AnalysisContext (External)

Owner: Analysis Engine orchestrator / Analysis Runtime

Provides chart facts, upstream stage results, and knowledge session references as supplied by Runtime.

Mutability: immutable input for the stage.

---

# 5. Upstream Result Models (External)

| Model | Owner |
|-------|-------|
| StrengthResult | Strength Engine |
| TemperatureResult | Temperature Engine |
| PatternResult | Pattern Engine |
| UsefulGodResult | Useful God Engine |
| TenGodsResult | Ten Gods Engine |
| CombinationResult | Combination Engine |
| ShenShaResult | ShenSha Engine |

Luck Engine must not redefine or mutate these models.

---

# 6. LuckEvaluationContext

Request-scoped internal working context. Not part of public API.

---

# 7. Layer Analysis Models

Represent evaluated outcomes for each luck layer:

- DaYunAnalysis
- LiuNianAnalysis
- LiuYueAnalysis
- LiuRiAnalysis
- LiuShiAnalysis

---

# 8. LuckInteractionAnalysis / TimingAnalysis / ActivationAnalysis

Represent interaction, timing window, and activation outcomes.

---

# 9. FavorabilityAnalysis

Represents favorability classes assigned to luck-layer outcomes.

---

# 10. PriorityResolution / ConflictResolution

Represent deterministic resolution of competing Luck outcomes.

---

# 11. ConfidenceEvaluation

Represents confidence score/class and contribution evidence.

---

# 12. LuckResult

Public immutable output model.

Shall include at minimum:

- Da Yun outcomes
- Liu Nian outcomes
- Liu Yue outcomes
- Liu Ri outcomes
- Liu Shi outcomes
- luck interaction summary
- timing / activation summary
- favorability outcomes
- priority / conflict resolution summary
- confidence
- matched KnowledgeReferences / RuleEvidence
- diagnostics / execution metadata slots aligned with shared Analysis Engine models

Exact field-level schema remains backward compatible within V1.x once published.

---

# 13. Ownership

All Luck-specific models above are owned by Luck Engine unless marked external.

---

# 14. Acceptance Criteria

Domain models are accepted when overview, external reads, layer models, and LuckResult contract are complete.
