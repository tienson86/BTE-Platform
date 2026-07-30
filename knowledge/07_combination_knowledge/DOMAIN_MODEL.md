# Combination Knowledge Domain Model

**Module:** Combination Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the logical entities of the Combination Knowledge domain.

These models describe knowledge content, not runtime objects.

---

# 2. Core Entities

```text
HeavenlyStemCombinationConcept
EarthlyBranchCombinationConcept
ClashConcept
HarmConcept
PunishmentConcept
DestructionConcept
HiddenCombinationConcept
TransformationConcept
PriorityResolutionConcept
ConflictResolutionConcept
FormulaConcept
DecisionConcept
MappingConcept
ReferenceConcept
EvaluationDimension
KnowledgeReference
```

---

# 3. HeavenlyStemCombinationConcept

Represents Heavenly Stem combination (Thiên Can Hợp) knowledge, including pair identities, combination conditions, and related elemental outcomes where declared.

---

# 4. EarthlyBranchCombinationConcept

Represents Earthly Branch combination (Địa Chi Hợp) knowledge, including pair / triad / group combination classes and conditions.

---

# 5. ClashConcept

Represents Clash (Xung) knowledge between declared stem or branch pairs and structural positions.

---

# 6. HarmConcept

Represents Harm (Hại) knowledge between declared branch pairs and structural conditions.

---

# 7. PunishmentConcept

Represents Punishment (Hình) knowledge, including self-punishment, mutual punishment, and related classes.

---

# 8. DestructionConcept

Represents Destruction (Phá) knowledge between declared branch pairs and structural conditions.

---

# 9. HiddenCombinationConcept

Represents Hidden Combination knowledge arising from concealed stem interactions within branches.

---

# 10. TransformationConcept

Represents Transformation (Hóa) knowledge, including transformation success / failure conditions and resulting elemental class.

Does not redefine Fundamental Wu Xing identities.

---

# 11. PriorityResolutionConcept

Represents priority classes used when multiple combination / clash / harm / punishment / destruction / transformation outcomes compete.

---

# 12. ConflictResolutionConcept

Represents conflict-resolution policies when mutually incompatible Combination outcomes are triggered.

---

# 13. FormulaConcept / DecisionConcept / MappingConcept / ReferenceConcept

Represent formula, decision-table, mapping-table, and reference-table knowledge families used by this module.

---

# 14. EvaluationDimension

Represents analytical dimensions of Combination knowledge, including:

- Heavenly Stem Combination
- Earthly Branch Combination
- Clash
- Harm
- Punishment
- Destruction
- Hidden Combination
- Transformation
- Priority Resolution
- Conflict Resolution
- Formula Concepts
- Mapping Tables

---

# 15. KnowledgeReference

Stable reference model for explainability:

- module_id
- asset_id
- version
- category

---

# 16. Ownership

All domain entities above are owned by Combination Knowledge unless explicitly referenced from Fundamental Knowledge.
