# Ten Gods Knowledge Domain Model

**Module:** Ten Gods Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the logical entities of the Ten Gods Knowledge domain.

These models describe knowledge content, not runtime objects.

---

# 2. Core Entities

```text
TenGodIdentity
RelationshipModel
StrengthInteractionConcept
PatternInteractionConcept
UsefulGodInteractionConcept
FavorabilityConcept
PersonalityConcept
CareerConcept
WealthConcept
MarriageConcept
HealthConcept
PriorityConcept
ConfidenceConcept
FormulaConcept
DecisionConcept
ReferenceConcept
EvaluationDimension
KnowledgeReference
```

---

# 3. TenGodIdentity

Represents analytical identity knowledge for each of the Ten Gods, including definition, polarity class, and production/control orientation relative to Day Master.

The ten identities are:

- Bi Jian (Friend)
- Jie Cai (Rob Wealth)
- Shi Shen (Eating God)
- Shang Guan (Hurting Officer)
- Pian Cai (Indirect Wealth)
- Zheng Cai (Direct Wealth)
- Qi Sha / Pian Guan (Seven Killings)
- Zheng Guan (Direct Officer)
- Pian Yin (Indirect Resource)
- Zheng Yin (Direct Resource)

Fundamental stem–branch Ten Gods relationship identities are referenced from Fundamental Knowledge and are not redefined here.

---

# 4. RelationshipModel

Represents declarative relationship models among Ten Gods identities, including mutual support, conflict, control, and structure-forming interactions used in Ten Gods Analysis.

---

# 5. StrengthInteractionConcept

Represents how published Day Master strength classifications interact with Ten Gods quality and favorability knowledge.

Does not redefine Strength Knowledge.

---

# 6. PatternInteractionConcept

Represents how published Pattern identities interact with Ten Gods structural and quality knowledge.

Does not redefine Pattern Knowledge.

---

# 7. UsefulGodInteractionConcept

Represents how published Useful God role assignments interact with Ten Gods favorability and quality knowledge.

Does not redefine Useful God Knowledge.

---

# 8. FavorabilityConcept

Represents favorability classes for Ten Gods under declared conditions (favorable, unfavorable, conditional, neutral).

---

# 9. PersonalityConcept

Represents personality-oriented interpretive knowledge frames associated with Ten Gods presence and quality.

---

# 10. CareerConcept

Represents career-oriented interpretive knowledge frames associated with Ten Gods presence and quality.

---

# 11. WealthConcept

Represents wealth-oriented interpretive knowledge frames associated with Ten Gods presence and quality.

---

# 12. MarriageConcept

Represents marriage / relationship-oriented interpretive knowledge frames associated with Ten Gods presence and quality.

---

# 13. HealthConcept

Represents health-oriented interpretive knowledge frames associated with Ten Gods presence and quality.

---

# 14. PriorityConcept

Represents priority classes for competing Ten Gods analytical outcomes.

---

# 15. ConfidenceConcept

Represents declarative confidence classes and contribution metadata for Ten Gods determination knowledge.

---

# 16. FormulaConcept / DecisionConcept / ReferenceConcept

Represent formula, decision-table, and reference-table knowledge families used by this module.

---

# 17. EvaluationDimension

Represents analytical dimensions of Ten Gods knowledge, including:

- Ten Gods Definitions
- Relationship Models
- Strength Interaction
- Pattern Interaction
- Useful God Interaction
- Favorability
- Personality Concepts
- Career Concepts
- Wealth Concepts
- Marriage Concepts
- Health Concepts
- Priority Concepts
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

All domain entities above are owned by Ten Gods Knowledge unless explicitly referenced from Fundamental or upstream analytical Knowledge Modules.
