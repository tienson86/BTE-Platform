# Pattern Knowledge Domain Model

**Module:** Pattern Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the logical entities of the Pattern Knowledge domain.

These models describe knowledge content, not runtime objects.

---

# 2. Core Entities

```text
PatternIdentity
PatternCategory
PatternCondition
PatternCandidate
PatternEvidence
PatternCompatibility
PatternException
PatternPriority
PatternConfidence
DecisionConcept
EvaluationDimension
FormulaConcept
ValidationConcept
KnowledgeReference
```

---

# 3. PatternIdentity

Represents one canonical Pattern (Ge Ju) identity.

Contains:

- pattern_id
- display term references
- category
- eligibility descriptors
- metadata

---

# 4. PatternCategory

Represents pattern family classification:

- Standard Patterns
- Special Patterns
- Follow Patterns
- Transformation Patterns
- Mixed / Exceptional extensions where declared

---

# 5. PatternCondition

Represents declarative conditions required for pattern eligibility or confirmation.

---

# 6. PatternCandidate

Represents a knowledge-level candidate descriptor before runtime resolution.

---

# 7. PatternEvidence

Represents required evidence descriptors for pattern matching and explainability.

---

# 8. PatternCompatibility

Represents compatibility and mutual-exclusion relationships among patterns.

---

# 9. PatternException

Represents exceptional pattern cases, overrides, and specialized eligibility.

---

# 10. PatternPriority

Represents priority classes used when multiple pattern candidates compete.

---

# 11. PatternConfidence

Represents declarative confidence classes and contribution metadata.

---

# 12. DecisionConcept

Represents decision concepts used by Decision Tables for pattern determination knowledge.

---

# 13. EvaluationDimension

Represents analytical dimensions of pattern knowledge, including:

- Standard Patterns
- Special Patterns
- Follow Patterns
- Transformation Patterns
- Pattern Conditions
- Pattern Priority
- Pattern Compatibility
- Pattern Exceptions
- Pattern Confidence

---

# 14. FormulaConcept

Represents conceptual formula families used by pattern confidence / ranking knowledge.

---

# 15. ValidationConcept

Represents validation coverage concepts for pattern knowledge completeness and consistency.

---

# 16. KnowledgeReference

Stable reference model for explainability:

- module_id
- asset_id
- version
- category

---

# 17. Ownership

All domain entities above are owned by Pattern Knowledge unless explicitly referenced from Fundamental Knowledge.
