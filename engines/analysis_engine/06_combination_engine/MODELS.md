# Combination Engine Domain Models

**Module:** `engines/analysis_engine/06_combination_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the official domain model specification for the Combination Engine.

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
        │  reads ten_gods_result
        │  accesses Knowledge SDK
        ▼
CombinationEvaluationContext
        │
        ▼
StemCombinationAnalysis
BranchCombinationAnalysis
ClashAnalysis
HarmAnalysis
PunishmentAnalysis
DestructionAnalysis
HiddenCombinationAnalysis
TransformationAnalysis
        │
        ▼
PriorityResolution
ConflictResolution
ConfidenceEvaluation
        │
        ▼
CombinationResult
```

No dedicated CombinationInput wrapper is defined. Shared AnalysisContext is used directly.

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

Combination Engine must not redefine or mutate these models.

---

# 6. CombinationEvaluationContext

Request-scoped internal working context. Not part of public API.

---

# 7. Relation Analysis Models

Represent evaluated outcomes for:

- Heavenly Stem Combination
- Earthly Branch Combination
- Clash
- Harm
- Punishment
- Destruction
- Hidden Combination
- Transformation

---

# 8. PriorityResolution / ConflictResolution

Represent deterministic resolution of competing Combination outcomes.

---

# 9. ConfidenceEvaluation

Represents confidence score/class and contribution evidence.

---

# 10. CombinationResult

Public immutable output model.

Shall include at minimum:

- detected combination / clash / harm / punishment / destruction / hidden combination outcomes
- transformation outcomes
- priority / conflict resolution summary
- confidence
- matched KnowledgeReferences / RuleEvidence
- diagnostics / execution metadata slots aligned with shared Analysis Engine models

Exact field-level schema remains backward compatible within V1.x once published.

---

# 11. Ownership

All Combination-specific models above are owned by Combination Engine unless marked external.

---

# 12. Acceptance Criteria

Domain models are accepted when overview, external reads, internal intermediates, and CombinationResult contract are complete.
