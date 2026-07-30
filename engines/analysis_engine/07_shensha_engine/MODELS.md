# ShenSha Engine Domain Models

**Module:** `engines/analysis_engine/07_shensha_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the official domain model specification for the ShenSha Engine.

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
ShenShaEvaluationContext
        │
        ▼
CalculationReferenceSet
LookupEvaluation
MappingEvaluation
AuspiciousShenShaSet
InauspiciousShenShaSet
InteractionAnalysis
CompatibilityAnalysis
ExceptionAnalysis
        │
        ▼
PriorityResolution
ConflictResolution
ConfidenceEvaluation
        │
        ▼
ShenShaResult
```

No dedicated ShenShaInput wrapper is defined. Shared AnalysisContext is used directly.

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

ShenSha Engine must not redefine or mutate these models.

---

# 6. ShenShaEvaluationContext

Request-scoped internal working context. Not part of public API.

---

# 7. CalculationReferenceSet

Represents derived lookup keys from chart anchors per calculation reference knowledge.

---

# 8. LookupEvaluation / MappingEvaluation

Represent deterministic lookup and mapping outcomes for ShenSha detection.

---

# 9. AuspiciousShenShaSet / InauspiciousShenShaSet

Represent detected ShenSha identities classified by polarity.

---

# 10. InteractionAnalysis / CompatibilityAnalysis / ExceptionAnalysis

Represent evaluated interaction, compatibility, and exception outcomes.

---

# 11. PriorityResolution / ConflictResolution

Represent deterministic resolution of competing ShenSha outcomes.

---

# 12. ConfidenceEvaluation

Represents confidence score/class and contribution evidence.

---

# 13. ShenShaResult

Public immutable output model.

Shall include at minimum:

- detected ShenSha identities and polarity classes
- interaction outcomes
- compatibility outcomes
- exception overrides / suppressions where applicable
- priority / conflict resolution summary
- confidence
- matched KnowledgeReferences / RuleEvidence
- diagnostics / execution metadata slots aligned with shared Analysis Engine models

Exact field-level schema remains backward compatible within V1.x once published.

---

# 14. Ownership

All ShenSha-specific models above are owned by ShenSha Engine unless marked external.

---

# 15. Acceptance Criteria

Domain models are accepted when overview, external reads, internal intermediates, and ShenShaResult contract are complete.
