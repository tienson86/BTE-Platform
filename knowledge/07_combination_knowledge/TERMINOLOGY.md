# Combination Knowledge Terminology

**Module:** Combination Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Terminology Specification)

---

# 1. Purpose

This document defines canonical terminology for Combination knowledge.

Shared fundamental terms are referenced from Fundamental Knowledge and are not redefined here.

---

# 2. Term Contract

Every term shall include:

| Field | Requirement |
|-------|-------------|
| term_id | Stable unique identity |
| canonical_term | Canonical label |
| definition | Precise meaning in Combination domain |
| scope | Combination Knowledge scope |
| aliases | Alternate labels |
| relationships | Related terms / fundamental references |
| language | Locale |
| version | Module-aligned version |

---

# 3. Core Relation Terms

## Heavenly Stem Combination

Definition: Declared pairing among Heavenly Stems that forms a combination class under stated conditions.

Scope: Heavenly Stem Combination.

Aliases: Thiên Can Hợp, Stem Combination.

Relationships: related to Transformation; references Fundamental Heavenly Stems.

## Earthly Branch Combination

Definition: Declared pairing, triad, or group among Earthly Branches that forms a combination class under stated conditions.

Scope: Earthly Branch Combination.

Aliases: Địa Chi Hợp, Branch Combination.

Relationships: related to Transformation; references Fundamental Earthly Branches.

## Clash

Definition: Opposing relation class between declared stems or branches that produces clash outcomes.

Scope: Clash.

Aliases: Xung, Conflict Clash.

Relationships: distinct from Harm, Punishment, and Destruction.

## Harm

Definition: Harmful relation class between declared branch pairs under stated conditions.

Scope: Harm.

Aliases: Hại, Branch Harm.

Relationships: distinct from Clash, Punishment, and Destruction.

## Punishment

Definition: Punishment relation class among declared branches, including self-punishment and mutual punishment subclasses.

Scope: Punishment.

Aliases: Hình, Branch Punishment.

Relationships: distinct from Clash, Harm, and Destruction.

## Destruction

Definition: Destruction relation class between declared branch pairs under stated conditions.

Scope: Destruction.

Aliases: Phá, Branch Destruction.

Relationships: distinct from Clash, Harm, and Punishment.

## Hidden Combination

Definition: Combination arising from Hidden Stem interactions within Earthly Branches.

Scope: Hidden Combination.

Aliases: Tàng Can Hợp, Concealed Combination.

Relationships: references Fundamental Hidden Stems; related to Heavenly Stem Combination.

## Transformation

Definition: Elemental transformation outcome of a combination when declared success conditions are met.

Scope: Transformation.

Aliases: Hóa, Combination Transformation.

Relationships: related to Heavenly Stem Combination and Earthly Branch Combination; references Fundamental Wu Xing.

---

# 4. Resolution Terms

## Priority Resolution

Definition: Ordering concepts used when multiple Combination outcomes compete.

Scope: Priority Resolution.

Aliases: Combination Priority Concepts.

Relationships: related to Conflict Resolution.

## Conflict Resolution

Definition: Policies for resolving mutually incompatible Combination outcomes.

Scope: Conflict Resolution.

Aliases: Combination Conflict Concepts.

Relationships: related to Priority Resolution and Decision Tables.

## Formula Concepts

Definition: Declarative formula models used for Combination intensity, transformation, and confidence.

Scope: Formula Concepts.

Aliases: Combination Formula Models.

Relationships: related to Formula Library.

## Mapping Tables

Definition: Deterministic source-to-target lookup tables for Combination pairs, groups, and outcomes.

Scope: Mapping Tables.

Aliases: Combination Mapping Assets.

Relationships: related to Rule Assets and Terminology.

---

# 5. Additional Required Term Families

Terminology shall also cover:

- Decision Table class names
- Reference Table class names
- Evaluation Dimension names
- transformation success / failure labels used by Combination Engine outputs

---

# 6. Non-Redefinition Rule

Stem, Branch, Wu Xing, and Hidden Stem taxonomies remain owned by Fundamental Knowledge.

Combination Terminology may specialize Combination-usage labels but must reference Fundamental identities.

---

# 7. Acceptance Criteria

Terminology is accepted when all mandatory Combination terms include definition, scope, aliases, and relationships, and remain consistent with Fundamental Knowledge.
