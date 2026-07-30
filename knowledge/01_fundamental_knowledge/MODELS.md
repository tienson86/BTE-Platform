# Fundamental Knowledge Models

**Module:** Fundamental Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the canonical models published by Fundamental Knowledge.

---

# 2. Design Principles

Models shall be:

- Immutable after publication
- Strongly typed
- Versioned
- Referencable by stable IDs
- Free of analytical business rules
- Storage-agnostic

---

# 3. Core Models

```text
Polarity
Element
HeavenlyStem
EarthlyBranch
HiddenStemComposition
ChangShengStage
NaYinEntry
TenGodRelation
ElementRelation
StemRelation
BranchRelation
SeasonDefinition
ClimateDefinition
Term
```

---

# 4. Polarity

Represents Yin / Yang.

Contains:

- polarity_id
- code
- term references
- metadata

---

# 5. Element

Represents one Wu Xing element.

Contains:

- element_id
- code
- polarity affinities where applicable
- term references

---

# 6. HeavenlyStem

Represents one Heavenly Stem.

Contains:

- stem_id
- code
- polarity_id
- element_id
- order index
- term references

---

# 7. EarthlyBranch

Represents one Earthly Branch.

Contains:

- branch_id
- code
- polarity_id
- element_id
- season associations
- order index
- term references

---

# 8. HiddenStemComposition

Represents hidden stems within a branch.

Contains:

- branch_id
- hidden stem members
- role class (principal / residual)
- order

---

# 9. ChangShengStage

Represents one Chang Sheng stage.

Contains:

- stage_id
- code
- order index
- term references

---

# 10. NaYinEntry

Represents one Na Yin pairing.

Contains:

- pair identity
- stem-branch pair
- na_yin identity
- element affiliation
- term references

---

# 11. TenGodRelation

Represents canonical Day Master → target stem relationship class.

Contains:

- relation_id
- day_master stem class
- target stem class
- ten_god class
- term references

No quality score fields.

---

# 12. ElementRelation

Represents canonical element-to-element relation.

Contains:

- source element
- target element
- relation class
- term references

---

# 13. StemRelation / BranchRelation

Represent canonical stem-stem and branch-branch relation classes.

Contain:

- source
- target
- relation class
- term references

---

# 14. SeasonDefinition / ClimateDefinition

Represent shared seasonal and climate definition frames.

Contain:

- definition_id
- code
- associated branches / solar-term frames as applicable
- term references

No scoring thresholds.

---

# 15. Term

Represents a terminology entry.

Contains:

- term_id
- canonical term
- aliases
- language
- scope
- definition

---

# 16. Ownership

All models above are owned by Fundamental Knowledge.

Downstream modules reference them; they do not mutate them.
