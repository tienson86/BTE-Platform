# Temperature Engine Domain Models

**Module:** `engines/analysis_engine/02_temperature_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the official domain model specification for the Temperature Engine.

All data exchanged within the module shall conform to these model definitions.

No implementation may introduce incompatible domain objects without a major version change.

---

# 2. Design Principles

The domain model follows these principles:

- Immutable by default
- Explicit ownership
- Strong typing
- Deterministic serialization
- Version compatibility
- Explainable analytical data
- No presentation concerns
- No persistence concerns

---

# 3. Domain Model Overview

The Temperature Engine defines the following primary models:

```text
AnalysisContext (Input)

StrengthResult (Input)

        │

        ▼

TemperatureContext

        │

        ▼

SeasonTemperatureAnalysis

WarmColdAnalysis

DrynessAnalysis

HumidityAnalysis

EquilibriumAnalysis

EnvironmentalSupportAnalysis

AdjustmentAnalysis

        │

        ▼

TemperatureScore

        │

        ▼

ConfidenceEvaluation

        │

        ▼

TemperatureResult
```

---

# 4. AnalysisContext (External)

Owner:

- Bazi Engine / Analysis Engine orchestrator

Purpose:

Provides immutable analytical input.

Mutability:

Immutable

Lifecycle:

Created before Temperature Engine execution.

Modified:

Never.

---

# 5. StrengthResult (External)

Owner:

- Strength Engine

Purpose:

Provides published Day Master strength evidence required by Temperature Rules.

Mutability:

Immutable

Lifecycle:

Created by Strength Engine before Temperature Engine execution.

Modified:

Never by Temperature Engine.

---

# 6. TemperatureContext

Owner:

Temperature Engine

Purpose:

Internal normalized analytical context.

Contains:

- normalized chart references
- projected strength evidence
- cached calculations
- runtime configuration
- rule references

Mutability:

Immutable after creation.

---

# 7. SeasonTemperatureAnalysis

Represents seasonal temperature influence.

Contains:

- season
- temperature polarity
- weight
- score
- matched_rules
- evidence

---

# 8. WarmColdAnalysis

Represents warm / cold balance.

Contains:

- warm factors
- cold factors
- net balance
- score
- evidence

---

# 9. DrynessAnalysis

Represents dryness contribution.

Contains:

- dryness factors
- dryness weight
- dryness score
- evidence

---

# 10. HumidityAnalysis

Represents humidity contribution.

Contains:

- humidity factors
- humidity weight
- humidity score
- evidence

---

# 11. EquilibriumAnalysis

Represents climate equilibrium.

Contains:

- equilibrium state
- imbalance indicators
- equilibrium score
- evidence

---

# 12. EnvironmentalSupportAnalysis

Represents environmental support for climate.

Contains:

- supporting environmental factors
- opposing environmental factors
- support score
- evidence

---

# 13. AdjustmentAnalysis

Represents climate adjustment requirements.

Contains:

- adjustment_required
- adjustment indicators
- adjustment direction
- adjustment score
- evidence

---

# 14. TemperatureScore

Represents aggregated analytical scores.

Contains:

- seasonal temperature score
- warm / cold score
- dryness score
- humidity score
- equilibrium score
- environmental support score
- adjustment score
- weighted score
- normalized score

---

# 15. ConfidenceEvaluation

Represents confidence assessment.

Contains:

- confidence level
- confidence score
- coverage
- reasoning

---

# 16. TemperatureResult

Represents the final analytical result.

Contains:

- TemperatureScore
- ConfidenceEvaluation
- temperature_level
- adjustment indicators
- matched_rules
- reasoning
- execution metadata

Immutable.

Returned by the Public API.

---

# 17. Ownership Rules

Each model has exactly one owner.

Models shall never be modified by downstream engines.

Temperature Engine shall never modify StrengthResult.

---

# 18. Serialization

All models shall support deterministic serialization.

Serialization format shall remain version compatible within V1.x.

---

# 19. Validation

Every model shall define:

- required fields
- optional fields
- constraints
- invariant rules

Validation occurs before model publication.

---

# 20. Compatibility

The model hierarchy shall remain backward compatible throughout the V1.x lifecycle.

Breaking changes require V2.
