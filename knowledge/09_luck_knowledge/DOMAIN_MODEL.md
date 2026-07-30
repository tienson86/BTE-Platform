# Luck Knowledge Domain Model

**Module:** Luck Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the logical entities of the Luck Knowledge domain.

These models describe knowledge content, not runtime objects.

---

# 2. Core Entities

```text
DaYunConcept
LiuNianConcept
LiuYueConcept
LiuRiConcept
LiuShiConcept
LuckLayer
LuckInteractionConcept
TimingPrincipleConcept
ActivationRuleConcept
FavorabilityConcept
ConfidenceConcept
PriorityConcept
FormulaConcept
DecisionConcept
ReferenceConcept
EvaluationDimension
KnowledgeReference
```

---

# 3. DaYunConcept

Represents Decade Luck (Đại Vận) knowledge, including sequence principles, directionality concepts, and decade-layer evaluation frames.

---

# 4. LiuNianConcept

Represents Annual Luck (Lưu Niên) knowledge and year-layer evaluation frames.

---

# 5. LiuYueConcept

Represents Monthly Luck (Lưu Nguyệt) knowledge and month-layer evaluation frames.

---

# 6. LiuRiConcept

Represents Daily Luck (Lưu Nhật) knowledge and day-layer evaluation frames.

---

# 7. LiuShiConcept

Represents Hourly Luck (Lưu Thời) knowledge and hour-layer evaluation frames.

---

# 8. LuckLayer

Represents the hierarchical luck layer class:

Da Yun → Liu Nian → Liu Yue → Liu Ri → Liu Shi

---

# 9. LuckInteractionConcept

Represents interaction knowledge between luck layers and natal chart structure / published natal analytical classifications.

Does not redefine natal analytical Knowledge Modules.

---

# 10. TimingPrincipleConcept

Represents timing principles that govern when luck layers activate, peak, transition, or overlap.

---

# 11. ActivationRuleConcept

Represents declarative activation conditions for luck-layer effects.

---

# 12. FavorabilityConcept

Represents favorability classes for luck-layer outcomes under declared conditions.

---

# 13. ConfidenceConcept

Represents declarative confidence classes and contribution metadata for Luck determination knowledge.

---

# 14. PriorityConcept

Represents priority classes for competing luck-layer outcomes.

---

# 15. FormulaConcept / DecisionConcept / ReferenceConcept

Represent formula, decision-table, and reference-table knowledge families used by this module.

---

# 16. EvaluationDimension

Represents analytical dimensions of Luck knowledge, including:

- Da Yun
- Liu Nian
- Liu Yue
- Liu Ri
- Liu Shi
- Luck Interaction
- Timing Principles
- Activation Rules
- Favorability Concepts
- Confidence Models
- Priority Concepts
- Reference Tables

---

# 17. KnowledgeReference

Stable reference model for explainability:

- module_id
- asset_id
- version
- category

---

# 18. Ownership

All domain entities above are owned by Luck Knowledge unless explicitly referenced from Fundamental or upstream natal analytical Knowledge Modules.
