# Temperature Knowledge Domain Model

**Module:** Temperature Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the logical entities of the Temperature Knowledge domain.

These models describe knowledge content, not runtime objects.

---

# 2. Core Entities

```text
ClimateFactor
ClimateEvidence
ClimateWeight
SeasonTemperatureCategory
ClimateCategory
ThermalPolarity
HumidityClass
SeasonalEnergyClass
MonthClimateProfile
ClimateBalanceState
AdjustmentPrinciple
TemperatureException
ConfidenceLevel
EvaluationDimension
PriorityConcept
KnowledgeReference
```

---

# 3. ClimateFactor

Represents one contributing factor in temperature / climate evaluation.

Contains:

- factor_id
- dimension
- category
- polarity of contribution
- related evidence schema
- terminology references

---

# 4. ClimateEvidence

Represents required evidence descriptors for a factor or rule.

Contains:

- evidence_id
- required chart facts
- upstream knowledge references
- explainability fields

---

# 5. ClimateWeight

Represents declarative weight profiles for climate dimensions.

---

# 6. SeasonTemperatureCategory

Represents seasonal temperature classes used by Seasonal Temperature knowledge.

---

# 7. ClimateCategory

Represents broad climate classification frames.

---

# 8. ThermalPolarity

Represents cold / hot / warm / cool classification concepts.

---

# 9. HumidityClass

Represents dryness and humidity classification concepts.

---

# 10. SeasonalEnergyClass

Represents seasonal energy characteristics relevant to climate balance.

---

# 11. MonthClimateProfile

Represents month-level climate characteristic definitions.

---

# 12. ClimateBalanceState

Represents equilibrium / imbalance states for climate evaluation knowledge.

---

# 13. AdjustmentPrinciple

Represents declarative adjustment principles for restoring climate balance.

---

# 14. TemperatureException

Represents exceptional climate cases, override conditions, and evidence requirements.

---

# 15. ConfidenceLevel

Represents declarative confidence classes and contribution metadata.

---

# 16. EvaluationDimension

Represents analytical dimensions of temperature knowledge, including:

- Seasonal Temperature
- Climate Categories
- Cold and Hot Classification
- Warm and Cool Adjustment
- Dryness and Humidity
- Seasonal Energy
- Month Climate Characteristics
- Climate Balance
- Temperature Exceptions
- Adjustment Principles

---

# 17. PriorityConcept

Represents priority classes used when multiple climate knowledge outcomes compete.

---

# 18. KnowledgeReference

Stable reference model for explainability:

- module_id
- asset_id
- version
- category

---

# 19. Ownership

All domain entities above are owned by Temperature Knowledge unless explicitly referenced from Fundamental Knowledge.
