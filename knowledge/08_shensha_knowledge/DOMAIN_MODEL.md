# ShenSha Knowledge Domain Model

**Module:** ShenSha Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the logical entities of the ShenSha Knowledge domain.

These models describe knowledge content, not runtime objects.

---

# 2. Core Entities

```text
AuspiciousShenShaConcept
InauspiciousShenShaConcept
ShenShaIdentity
CalculationReferenceConcept
LookupTableConcept
MappingConcept
PriorityConcept
InteractionRuleConcept
CompatibilityConcept
ExceptionConcept
ConfidenceConcept
FormulaConcept
DecisionConcept
ReferenceConcept
EvaluationDimension
KnowledgeReference
```

---

# 3. AuspiciousShenShaConcept

Represents Auspicious ShenSha (cát thần / cát sát class) definitions, detection references, and quality knowledge.

---

# 4. InauspiciousShenShaConcept

Represents Inauspicious ShenSha (hung thần / hung sát class) definitions, detection references, and quality knowledge.

---

# 5. ShenShaIdentity

Represents a stable analytical identity for an individual ShenSha entry, including polarity class and category tags.

---

# 6. CalculationReferenceConcept

Represents declarative calculation reference knowledge used to determine ShenSha presence from chart anchors (for example Year / Month / Day / Hour stem-branch anchors as locale-defined).

Does not implement calculation code.

---

# 7. LookupTableConcept

Represents compact lookup knowledge for ShenSha detection by declared anchors and keys.

---

# 8. MappingConcept

Represents source-to-target mapping knowledge among anchors, ShenSha identities, polarity classes, and interaction classes.

---

# 9. PriorityConcept

Represents priority classes for competing ShenSha outcomes.

---

# 10. InteractionRuleConcept

Represents declarative interaction knowledge among co-present ShenSha identities.

---

# 11. CompatibilityConcept

Represents compatibility classes among ShenSha identities and with declared chart-structure classes where applicable.

---

# 12. ExceptionConcept

Represents exception conditions that override, suppress, or qualify default ShenSha outcomes.

---

# 13. ConfidenceConcept

Represents declarative confidence classes and contribution metadata for ShenSha determination knowledge.

---

# 14. FormulaConcept / DecisionConcept / ReferenceConcept

Represent formula, decision-table, and reference-table knowledge families used by this module.

---

# 15. EvaluationDimension

Represents analytical dimensions of ShenSha knowledge, including:

- Auspicious ShenSha
- Inauspicious ShenSha
- Calculation References
- Lookup Tables
- Mapping Tables
- Priority Concepts
- Interaction Rules
- Compatibility
- Exceptions
- Confidence Concepts

---

# 16. KnowledgeReference

Stable reference model for explainability:

- module_id
- asset_id
- version
- category

---

# 17. Ownership

All domain entities above are owned by ShenSha Knowledge unless explicitly referenced from Fundamental Knowledge.
