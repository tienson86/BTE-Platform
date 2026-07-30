# Ten Gods Engine Domain Models

**Module:** `engines/analysis_engine/05_ten_gods_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the official domain model specification for the Ten Gods Engine.

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
        │  reads strength_result
        │  reads temperature_result
        │  reads pattern_result
        │  reads useful_god_result
        │  accesses Knowledge SDK
        ▼
TenGodsEvaluationContext
        │
        ▼
TenGodPresenceSet
RelationshipAnalysis
StrengthInteractionAnalysis
TemperatureInteractionAnalysis
PatternInteractionAnalysis
UsefulGodInteractionAnalysis
FavorabilityAnalysis
LifeAreaConceptAnalysis
        │
        ▼
PriorityResolution
ConflictResolution
ConfidenceEvaluation
        │
        ▼
TenGodsResult
```

No dedicated TenGodsInput wrapper is defined. Shared AnalysisContext is used directly.

---

# 4. AnalysisContext (External)

Owner: Analysis Engine orchestrator / Analysis Runtime

Provides:

- Calendar and BaZi chart facts
- `strength_result`
- `temperature_result`
- `pattern_result`
- `useful_god_result`
- runtime/knowledge session references as provided by Runtime

Mutability: immutable input for the stage.

---

# 5. Upstream Result Models (External)

Read-only evidence:

| Model | Owner |
|-------|-------|
| StrengthResult | Strength Engine |
| TemperatureResult | Temperature Engine |
| PatternResult | Pattern Engine |
| UsefulGodResult | Useful God Engine |

Ten Gods Engine must not redefine or mutate these models.

---

# 6. TenGodsEvaluationContext

Request-scoped internal working context assembling chart facts, upstream evidence, and knowledge handles.

Not part of public API.

---

# 7. TenGodPresenceSet

Represents detected Ten Gods identities and presence structure (for example Bi Jian, Jie Cai, Shi Shen, Shang Guan, Pian Cai, Zheng Cai, Qi Sha, Zheng Guan, Pian Yin, Zheng Yin as applicable).

---

# 8. RelationshipAnalysis

Represents evaluated relationship-model outcomes among Ten Gods.

---

# 9. Interaction Analyses

Represent interaction outcomes with published:

- strength classifications
- temperature / climate classifications
- pattern identities
- useful god roles

---

# 10. FavorabilityAnalysis

Represents favorability classes assigned to Ten Gods under declared conditions.

---

# 11. LifeAreaConceptAnalysis

Represents analytical concept tags for:

- personality
- career
- wealth
- marriage
- health

These are analytical frames, not narrative sentences.

---

# 12. PriorityResolution / ConflictResolution

Represent deterministic resolution of competing Ten Gods outcomes.

---

# 13. ConfidenceEvaluation

Represents confidence score/class and contribution evidence for the Ten Gods determination.

---

# 14. TenGodsResult

Public immutable output model.

Shall include at minimum:

- ten gods presence / structure summary
- relationship outcomes
- interaction summaries
- favorability outcomes
- life-area concept tags where applicable
- confidence
- matched KnowledgeReferences / RuleEvidence
- diagnostics / execution metadata slots aligned with shared Analysis Engine models

Exact field-level schema remains backward compatible within V1.x once published.

---

# 15. Ownership

All Ten Gods-specific models above are owned by Ten Gods Engine unless marked external.

---

# 16. Acceptance Criteria

Domain models are accepted when overview, external reads, internal intermediates, and TenGodsResult contract are complete.
