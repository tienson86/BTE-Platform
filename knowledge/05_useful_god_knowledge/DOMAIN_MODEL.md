# Useful God Knowledge Domain Model

**Module:** Useful God Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the logical entities of the Useful God Knowledge domain.

These models describe knowledge content, not runtime objects.

---

# 2. Core Entities

```text
UsefulGodRole
YongShenConcept
XiShenConcept
JiShenConcept
ChouShenConcept
SeasonalSelectionConcept
StrengthDependencyConcept
TemperatureDependencyConcept
PatternDependencyConcept
UsefulGodCandidate
CandidateSelectionConcept
PriorityConcept
ConfidenceConcept
FormulaConcept
DecisionConcept
ReferenceConcept
EvaluationDimension
KnowledgeReference
```

---

# 3. UsefulGodRole

Represents the role class assigned to an elemental / stem-based balancing entity.

Roles include Yong Shen, Xi Shen, Ji Shen, and Chou Shen.

---

# 4. YongShenConcept

Represents Useful God (Dụng Thần) selection knowledge.

---

# 5. XiShenConcept

Represents Favorable God (Hỷ Thần) selection knowledge.

---

# 6. JiShenConcept

Represents Unfavorable God (Kỵ Thần) selection knowledge.

---

# 7. ChouShenConcept

Represents Idle / Neutral God (Cừu Thần / Nhàn Thần class as locale-defined) selection knowledge.

---

# 8. SeasonalSelectionConcept

Represents seasonal selection frames used when season command influences Useful God choice.

---

# 9. StrengthDependencyConcept

Represents how published strength classifications constrain or inform Useful God candidates.

Does not redefine Strength Knowledge.

---

# 10. TemperatureDependencyConcept

Represents how published climate classifications constrain or inform Useful God candidates.

Does not redefine Temperature Knowledge.

---

# 11. PatternDependencyConcept

Represents how published Pattern identities constrain or inform Useful God candidates.

Does not redefine Pattern Knowledge.

---

# 12. UsefulGodCandidate

Represents a knowledge-level candidate descriptor before runtime resolution.

---

# 13. CandidateSelectionConcept

Represents selection principles among primary, secondary, and alternative candidates.

---

# 14. PriorityConcept

Represents priority classes for competing Useful God outcomes.

---

# 15. ConfidenceConcept

Represents declarative confidence classes and contribution metadata.

---

# 16. FormulaConcept / DecisionConcept / ReferenceConcept

Represent formula, decision-table, and reference-table knowledge families used by this module.

---

# 17. EvaluationDimension

Represents analytical dimensions of Useful God knowledge, including:

- Yong Shen
- Xi Shen
- Ji Shen
- Chou Shen
- Seasonal Selection
- Strength Dependency
- Temperature Dependency
- Pattern Dependency
- Priority Rules
- Candidate Selection
- Confidence Concepts

---

# 18. KnowledgeReference

Stable reference model for explainability:

- module_id
- asset_id
- version
- category

---

# 19. Ownership

All domain entities above are owned by Useful God Knowledge unless explicitly referenced from Fundamental or upstream analytical Knowledge Modules.
