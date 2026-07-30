# Strength Knowledge Domain Model

**Module:** Strength Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the logical entities of the Strength Knowledge domain.

These models describe knowledge content, not runtime objects.

---

# 2. Core Entities

```text
StrengthFactor
StrengthEvidence
StrengthWeight
SeasonCategory
GrowthStage
RootType
SupportType
RestrictionType
InfluenceType
ConfidenceLevel
EvaluationDimension
SpecialException
PriorityConcept
KnowledgeReference
```

---

# 3. StrengthFactor

Represents one contributing factor in Day Master strength evaluation.

Contains:

- factor_id
- dimension
- category
- polarity of contribution
- related evidence schema
- terminology references

---

# 4. StrengthEvidence

Represents required evidence descriptors for a factor or rule.

Contains:

- evidence_id
- required chart facts
- upstream knowledge references
- explainability fields

---

# 5. StrengthWeight

Represents declarative weight profiles.

Contains:

- weight_id
- dimension
- weight profile
- applicability conditions
- version

---

# 6. SeasonCategory

Represents seasonal strength categories used by De Ling and seasonal influence knowledge.

---

# 7. GrowthStage

Represents Trường Sinh cycle stages as used by strength evaluation knowledge.

References Fundamental Knowledge stage identities; does not redefine them.

---

# 8. RootType

Represents rooting classifications such as Tong Gen / Thông Căn and related root depth classes.

---

# 9. SupportType

Represents support classifications from stems, hidden stems, and five-element generation.

---

# 10. RestrictionType

Represents restriction / draining / controlling classifications.

---

# 11. InfluenceType

Represents structural influence classes:

- Combination Influence
- Clash Influence
- Harm Influence
- Punishment Influence
- Void Influence
- Temperature Adjustment Influence

These are strength-domain influence definitions.

Ownership of general combination taxonomies remains with Fundamental / Combination Knowledge as applicable; this module defines strength-specific influence usage.

---

# 12. ConfidenceLevel

Represents declarative confidence classes and contribution metadata for strength evaluation knowledge.

---

# 13. EvaluationDimension

Represents analytical dimensions of strength knowledge, including:

- Seasonal Strength
- Monthly Branch Influence
- Heavenly Stem Support
- Hidden Stem Support
- Root Strength
- Five Element Support
- Five Element Restriction
- Growth Stage
- De Ling / De Di / De Shi
- Special Exceptions
- Temperature Adjustment Influence

---

# 14. SpecialException

Represents exceptional strength cases defined by knowledge, including override conditions and evidence requirements.

---

# 15. PriorityConcept

Represents priority classes used when multiple strength knowledge outcomes compete.

---

# 16. KnowledgeReference

Stable reference model for explainability:

- module_id
- asset_id
- version
- category

---

# 17. Ownership

All domain entities above are owned by Strength Knowledge unless explicitly referenced from Fundamental Knowledge.
