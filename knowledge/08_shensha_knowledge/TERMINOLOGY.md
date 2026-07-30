# ShenSha Knowledge Terminology

**Module:** ShenSha Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Terminology Specification)

---

# 1. Purpose

This document defines canonical terminology for ShenSha knowledge.

Shared fundamental terms are referenced from Fundamental Knowledge and are not redefined here.

---

# 2. Term Contract

Every term shall include:

| Field | Requirement |
|-------|-------------|
| term_id | Stable unique identity |
| canonical_term | Canonical label |
| definition | Precise meaning in ShenSha domain |
| scope | ShenSha Knowledge scope |
| aliases | Alternate labels |
| relationships | Related terms / fundamental references |
| language | Locale |
| version | Module-aligned version |

---

# 3. Core Polarity Terms

## Auspicious ShenSha

Definition: ShenSha identities classified as generally favorable under declared conditions.

Scope: Auspicious ShenSha.

Aliases: Cát Thần / Cát Sát, Beneficial ShenSha.

Relationships: opposite polarity class to Inauspicious ShenSha.

## Inauspicious ShenSha

Definition: ShenSha identities classified as generally unfavorable under declared conditions.

Scope: Inauspicious ShenSha.

Aliases: Hung Thần / Hung Sát, Adverse ShenSha.

Relationships: opposite polarity class to Auspicious ShenSha.

## ShenSha Identity

Definition: Stable analytical identity of an individual ShenSha entry.

Scope: ShenSha Definitions.

Aliases: Thần Sát Identity, Star Identity.

Relationships: belongs to Auspicious or Inauspicious polarity class as declared.

---

# 4. Detection and Structure Terms

## Calculation References

Definition: Declarative reference knowledge describing how chart anchors produce ShenSha lookup keys.

Scope: Calculation References.

Aliases: ShenSha Calculation Anchors.

Relationships: related to Lookup Tables; references Fundamental Stems and Branches.

## Lookup Tables

Definition: Compact deterministic tables mapping declared keys to ShenSha presence or identity outcomes.

Scope: Lookup Tables.

Aliases: ShenSha Lookup Assets.

Relationships: related to Calculation References and Mapping Tables.

## Mapping Tables

Definition: Deterministic source-to-target tables among anchors, identities, polarity, and interaction classes.

Scope: Mapping Tables.

Aliases: ShenSha Mapping Assets.

Relationships: related to Lookup Tables and Rule Assets.

## Priority Concepts

Definition: Ordering concepts used when multiple ShenSha outcomes compete.

Scope: Priority Concepts.

Aliases: ShenSha Priority Concepts.

Relationships: related to Interaction Rules and Exceptions.

## Interaction Rules

Definition: Declarative rules describing effects when multiple ShenSha identities co-occur.

Scope: Interaction Rules.

Aliases: ShenSha Interaction Concepts.

Relationships: related to Compatibility and Priority Concepts.

## Compatibility

Definition: Compatibility classes among ShenSha identities and with declared chart-structure classes.

Scope: Compatibility.

Aliases: ShenSha Compatibility Concepts.

Relationships: related to Interaction Rules.

## Exceptions

Definition: Conditions that override, suppress, or qualify default ShenSha outcomes.

Scope: Exceptions.

Aliases: ShenSha Exception Concepts.

Relationships: related to Priority Concepts and Decision Tables.

## Confidence Concepts

Definition: Declarative confidence classes for ShenSha determination knowledge quality.

Scope: Confidence Concepts.

Aliases: ShenSha Confidence.

Relationships: related to Formula Concepts.

---

# 5. Additional Required Term Families

Terminology shall also cover:

- Formula Concept names
- Decision Table class names
- Reference Table class names
- Evaluation Dimension names
- presence / polarity / exception labels used by ShenSha Engine outputs

---

# 6. Non-Redefinition Rule

Stem, Branch, Wu Xing, and Hidden Stem taxonomies remain owned by Fundamental Knowledge.

ShenSha Terminology may specialize ShenSha-usage labels but must reference Fundamental identities.

---

# 7. Acceptance Criteria

Terminology is accepted when all mandatory ShenSha terms include definition, scope, aliases, and relationships, and remain consistent with Fundamental Knowledge.
