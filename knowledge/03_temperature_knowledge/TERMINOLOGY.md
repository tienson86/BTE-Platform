# Temperature Knowledge Terminology

**Module:** Temperature Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Terminology Specification)

---

# 1. Purpose

This document defines canonical terminology for Temperature / Climate knowledge.

Shared fundamental terms are referenced from Fundamental Knowledge and are not redefined here.

---

# 2. Term Contract

Every term shall include:

| Field | Requirement |
|-------|-------------|
| term_id | Stable unique identity |
| canonical_term | Canonical label |
| definition | Precise meaning in temperature domain |
| scope | Temperature Knowledge scope |
| aliases | Alternate labels |
| relationships | Related terms / fundamental references |
| language | Locale |
| version | Module-aligned version |

---

# 3. Core Climate Classifications

## Hàn (Cold)

Definition: Climate state dominated by cold characteristics.

Scope: Thermal polarity classification.

Aliases: Cold, Cold Climate.

Relationships: opposite polarity relative to Nhiệt; may relate to Lương as adjacent cooler class.

## Nhiệt (Hot)

Definition: Climate state dominated by hot characteristics.

Scope: Thermal polarity classification.

Aliases: Hot, Hot Climate.

Relationships: opposite polarity relative to Hàn; may relate to Ôn as adjacent warmer class.

## Ôn (Warm)

Definition: Moderately warm climate adjustment class.

Scope: Warm / Cool Adjustment.

Aliases: Warm, Warming.

Relationships: related to Nhiệt; used in warm adjustment principles.

## Lương (Cool)

Definition: Moderately cool climate adjustment class.

Scope: Warm / Cool Adjustment.

Aliases: Cool, Cooling.

Relationships: related to Hàn; used in cool adjustment principles.

## Táo (Dry)

Definition: Climate state dominated by dryness.

Scope: Dryness / Humidity classification.

Aliases: Dry, Dryness.

Relationships: opposite relative to Thấp.

## Thấp (Humid)

Definition: Climate state dominated by humidity / dampness.

Scope: Dryness / Humidity classification.

Aliases: Humid, Damp, Humidity.

Relationships: opposite relative to Táo.

## Điều Hòa (Balanced Climate)

Definition: Climate state judged as balanced / in equilibrium.

Scope: Climate Balance.

Aliases: Balanced, Climate Equilibrium.

Relationships: opposite relative to climate imbalance states.

---

# 4. Seasonal and Monthly Concepts

## Seasonal Temperature

Definition: Temperature characteristic derived from seasonal command frame.

Scope: Seasonal Temperature dimension.

Aliases: Season Climate, Seasonal Thermal State.

Relationships: related to Fundamental Season Definitions.

## Seasonal Energy

Definition: Seasonal energetic quality affecting climate evaluation.

Scope: Seasonal Energy dimension.

Aliases: Season Qi, Seasonal Force.

Relationships: related to Seasonal Temperature and Month Climate Characteristics.

## Month Climate Characteristics

Definition: Month-specific climate profile used in temperature evaluation knowledge.

Scope: Month Climate Characteristics dimension.

Aliases: Monthly Climate, Month Qi Profile.

Relationships: related to Earthly Branch month associations from Fundamental Knowledge.

---

# 5. Adjustment and Exception Concepts

## Adjustment Principle

Definition: Declarative principle describing how climate imbalance should be adjusted in knowledge terms.

Scope: Adjustment Principles dimension.

Aliases: Climate Adjustment Rule Concept, Remedial Climate Principle.

Relationships: related to Warm / Cool Adjustment and Climate Balance.

## Temperature Exception

Definition: Exceptional climate case that overrides or specializes standard classification knowledge.

Scope: Temperature Exceptions dimension.

Aliases: Climate Special Case, Thermal Exception.

Relationships: related to Priority Concepts and Special Exception handling.

---

# 6. Additional Required Term Families

Terminology shall also cover:

- Climate Category classes
- Climate Balance imbalance classes
- Weight Model class names
- Confidence Level classes
- Priority Concept classes
- Evaluation Dimension names
- Environmental support / climate adjustment requirement labels used by Temperature Engine outputs

---

# 7. Non-Redefinition Rule

Season Definitions, Climate Definitions, Wu Xing, Stems, and Branches remain owned by Fundamental Knowledge.

Temperature Terminology may specialize climate-usage labels but must reference fundamental identities.

---

# 8. Acceptance Criteria

Terminology is accepted when all mandatory climate terms include definition, scope, aliases, and relationships, and remain consistent with Fundamental Knowledge.
