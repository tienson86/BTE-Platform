# PACK_01_DESIGN_PRINCIPLES.md

Version: 1.0
Status: OFFICIAL
Owner: BTE UI Architecture
Scope: Entire BTE Platform

---

# 1. Purpose

This document defines the fundamental design philosophy of the BTE Platform.

It serves as the highest-level UI specification that governs all user interfaces across:

- BTE Portal
- Analysis Console
- Administration Portal
- Report Viewer
- Future Mobile Applications

No UI implementation may violate these principles.

---

# 2. Design Philosophy

BTE is not a generic dashboard.

It is a professional metaphysics analysis platform that presents complex analytical knowledge through a modern, calm, trustworthy interface.

The UI must reduce cognitive load rather than increase it.

The interface should guide users to understand analysis instead of overwhelming them with data.

Core philosophy:

> Clarity over Density.

> Understanding over Decoration.

> Information over Animation.

> Calmness over Excitement.

---

# 3. Design Goals

The UI must always achieve the following objectives.

## 3.1 Readability

Information must be easy to read.

Typography always has higher priority than decoration.

---

## 3.2 Predictability

Users should immediately understand:

- where information is located
- what is important
- what action comes next

---

## 3.3 Consistency

The same information must always appear using the same visual language.

Example:

Analysis Score

must always use identical colors,
identical badge styles,
identical spacing,
identical typography.

---

## 3.4 Simplicity

Every screen should contain only information that helps decision making.

Avoid unnecessary visual complexity.

---

## 3.5 Professionalism

The visual language should resemble

professional financial software

rather than

marketing websites.

---

# 4. Design Principles

The following principles are mandatory.

---

## Principle 1

UI controls Data.

Never allow data to control UI.

Dynamic content must adapt to layout.

Layout must never adapt to unlimited content.

---

## Principle 2

Hierarchy First.

The user must instantly recognize

Primary

Secondary

Supporting

information.

---

## Principle 3

Whitespace is Information.

Empty space improves readability.

Whitespace is never considered wasted space.

---

## Principle 4

Cards are Independent.

Each card is an independent information block.

One card must never affect another card's layout.

---

## Principle 5

Visual Rhythm.

Spacing should follow a consistent rhythm.

The user should visually "scan" the interface naturally.

---

## Principle 6

One Purpose per Card.

Each card should answer only one question.

Bad:

One card containing

summary

score

warning

analysis

history

recommendation

Good:

Separate cards.

---

## Principle 7

Progressive Disclosure.

Show only essential information first.

Advanced information is revealed only when requested.

---

## Principle 8

Preview before Detail.

Every large content block must have

Preview

↓

Read More

↓

Full Detail

Never render everything immediately.

---

## Principle 9

Stable Layout.

Loading data must not move the interface.

The page should remain visually stable.

---

## Principle 10

Design for Long-Term Growth.

Every screen must support

future modules

without redesign.

---

# 5. Information Hierarchy

Information priority:

Level 1

Critical

Example

Overall Score

Destiny Direction

Strength

Useful God

---

Level 2

Important

Charts

Ten Gods

Elements

Pattern

---

Level 3

Supporting

Notes

Definitions

References

Metadata

---

# 6. Visual Language

The UI should communicate

calm

confidence

clarity

professionalism

Avoid:

flashy colors

heavy shadows

excessive gradients

unnecessary animations

---

# 7. Color Philosophy

Colors communicate meaning.

Never use colors only for decoration.

Red

Warning

Weakness

Fire

Attention

Green

Positive

Healthy

Growth

Blue

Knowledge

Analysis

Information

Orange

Action

Recommendation

Purple

Special

Advanced

Grey

Neutral

Supporting information

---

# 8. Typography Philosophy

Typography is the primary communication tool.

Rules:

Headings emphasize hierarchy.

Body emphasizes readability.

Numbers emphasize comparison.

Never use typography for decoration.

---

# 9. Data Presentation Philosophy

The platform analyzes large amounts of information.

Therefore:

Summarize first.

Explain second.

Expand third.

Raw data is never shown before interpretation.

---

# 10. User Experience Principles

Every page should answer:

What is happening?

↓

Why does it matter?

↓

What should I do?

If a screen cannot answer these three questions,

it should be redesigned.

---

# 11. Scalability

The design system must support:

new engines

new report types

new cards

new charts

new analysis modules

without changing existing layouts.

---

# 12. Single Source of Truth

The following documents derive from this specification.

PACK_02_LAYOUT_SYSTEM.md

↓

PACK_03_COMPONENT_STANDARD.md

↓

PACK_04_UI_PRESENTATION_STANDARD.md

↓

Implementation

If conflicts occur,

this document has highest priority.

---

# 13. Non-Goals

This design system does NOT attempt to:

maximize visual effects

create artistic interfaces

imitate social media

prioritize decoration over usability

---

# 14. Acceptance Criteria

A design complies with this specification if:

✓ Information hierarchy is obvious.

✓ Layout remains stable.

✓ Dynamic content never breaks layout.

✓ Every card has a clear purpose.

✓ Typography remains readable.

✓ Whitespace is preserved.

✓ Colors communicate meaning.

✓ Users can scan information within seconds.

✓ The interface feels calm and professional.

✓ Future modules can be added without redesign.

---

END OF DOCUMENT