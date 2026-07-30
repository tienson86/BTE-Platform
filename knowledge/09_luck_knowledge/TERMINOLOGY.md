# Luck Knowledge Terminology

**Module:** Luck Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Terminology Specification)

---

# 1. Purpose

This document defines canonical terminology for Luck knowledge.

Shared fundamental terms are referenced from Fundamental Knowledge and are not redefined here.

---

# 2. Term Contract

Every term shall include:

| Field | Requirement |
|-------|-------------|
| term_id | Stable unique identity |
| canonical_term | Canonical label |
| definition | Precise meaning in Luck domain |
| scope | Luck Knowledge scope |
| aliases | Alternate labels |
| relationships | Related terms / fundamental / upstream references |
| language | Locale |
| version | Module-aligned version |

---

# 3. Core Luck Layer Terms

## Da Yun

Definition: Decade Luck layer governing approximately ten-year fortune periods.

Scope: Da Yun.

Aliases: Đại Vận, Decade Luck.

Relationships: parent layer relative to Liu Nian.

## Liu Nian

Definition: Annual Luck layer governing year-level fortune within a Da Yun context.

Scope: Liu Nian.

Aliases: Lưu Niên, Annual Luck.

Relationships: nested under Da Yun; parent relative to Liu Yue.

## Liu Yue

Definition: Monthly Luck layer governing month-level fortune within a Liu Nian context.

Scope: Liu Yue.

Aliases: Lưu Nguyệt, Monthly Luck.

Relationships: nested under Liu Nian; parent relative to Liu Ri.

## Liu Ri

Definition: Daily Luck layer governing day-level fortune within a Liu Yue context.

Scope: Liu Ri.

Aliases: Lưu Nhật, Daily Luck.

Relationships: nested under Liu Yue; parent relative to Liu Shi.

## Liu Shi

Definition: Hourly Luck layer governing hour-level fortune within a Liu Ri context.

Scope: Liu Shi.

Aliases: Lưu Thời, Hourly Luck.

Relationships: nested under Liu Ri; finest V1.0 luck layer.

---

# 4. Interaction and Timing Terms

## Luck Interaction

Definition: Interaction concepts between luck layers and natal chart / published natal analytical evidence.

Scope: Luck Interaction.

Aliases: Luck–Natal Interaction Concepts.

Relationships: related to all luck layers; references upstream natal classifications without redefining them.

## Timing Principles

Definition: Principles governing luck-layer activation windows, peaks, transitions, and overlaps.

Scope: Timing Principles.

Aliases: Luck Timing Concepts.

Relationships: related to Activation Rules.

## Activation Rules

Definition: Declarative conditions under which a luck-layer effect becomes active.

Scope: Activation Rules.

Aliases: Luck Activation Concepts.

Relationships: related to Timing Principles and Favorability Concepts.

## Favorability Concepts

Definition: Favorability classes assigned to luck-layer outcomes under declared conditions.

Scope: Favorability Concepts.

Aliases: Luck Favorability.

Relationships: related to Luck Interaction and Confidence Models.

## Confidence Models

Definition: Declarative confidence classes for Luck determination knowledge quality.

Scope: Confidence Models.

Aliases: Luck Confidence Concepts.

Relationships: related to Formula Concepts.

## Priority Concepts

Definition: Ordering concepts used when multiple luck-layer outcomes compete.

Scope: Priority Concepts.

Aliases: Luck Priority Concepts.

Relationships: related to Luck Interaction and Decision Tables.

## Reference Tables

Definition: Shared deterministic reference lookups used by Luck Knowledge.

Scope: Reference Tables.

Aliases: Luck Reference Assets.

Relationships: related to Mapping Tables and Rule Assets.

---

# 5. Additional Required Term Families

Terminology shall also cover:

- Formula Concept names
- Decision Table class names
- Mapping Table class names
- Evaluation Dimension names
- layer / activation / favorability labels used by Luck Engine outputs

---

# 6. Non-Redefinition Rule

Stem, Branch, Wu Xing, and sexagenary taxonomies remain owned by Fundamental Knowledge.

Natal analytical classification identities remain owned by their respective Knowledge Modules.

Luck Terminology may specialize Luck-usage labels but must reference upstream identities.

---

# 7. Acceptance Criteria

Terminology is accepted when all mandatory Luck terms include definition, scope, aliases, and relationships, and remain consistent with Fundamental and upstream natal Knowledge Modules.
