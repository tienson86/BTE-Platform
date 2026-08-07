# VISUAL_TRANSFORMATION_GUIDE.md

Version: 1.0

Status: OFFICIAL

Owner: BTE UI Architecture

Priority: CRITICAL

Depends On

- VISUAL_LANGUAGE_SYSTEM.md
- VISUAL_REFERENCE_GALLERY.md
- PACK_07_RESULT_PAGE_BLUEPRINT.md

---

# Purpose

This document defines the official transformation strategy for upgrading the BTE user interface from the current implementation to the Visual Language V2.

Unlike the Design System,

which specifies rules,

and the Visual Reference Gallery,

which provides examples,

this guide defines the concrete transformation steps that Cursor and developers must follow.

The objective is not to redesign the application.

The objective is to improve visual quality while preserving architecture.

---

# Transformation Principles

Architecture remains unchanged.

Layout remains unchanged.

Business logic remains unchanged.

Presentation hierarchy remains unchanged.

Only visual presentation should evolve.

The transformation must preserve

Zones

Rows

Layout Patterns

Reading Flow

Responsive Behaviour

Accessibility

---

# Transformation Workflow

Current UI

↓

Identify Visual Issues

↓

Select Transformation Pattern

↓

Apply Visual Language

↓

Compare with Visual Reference

↓

Validate

↓

Approve

---

# Transformation Rule 01

## Reduce Visual Noise

Problem

Every component attempts to attract attention.

Symptoms

Many borders

Many shadows

Many colors

Many badges

Many buttons

Transformation

Reduce decorative elements.

Increase whitespace.

Use typography to create hierarchy.

Expected Result

Calm

Readable

Professional

---

# Transformation Rule 02

## Reduce Nested Containers

Problem

Cards contain cards which contain additional cards.

Before

Card

↓

Sub Card

↓

Sub Card

↓

Content

After

Card

↓

Content Groups

↓

Content

Rule

Prefer one visual container.

Separate internal sections using spacing.

---

# Transformation Rule 03

## Simplify Borders

Problem

Every component has a border.

Transformation

Replace borders with

Whitespace

↓

Background contrast

↓

Typography

↓

Border (last resort)

Expected Result

Cleaner interface

Reduced cognitive load

---

# Transformation Rule 04

## Increase Information Hierarchy

Problem

Everything has equal importance.

Transformation

Primary

Executive Summary

↓

Secondary

Analysis

↓

Tertiary

Knowledge

Only one primary visual focus is allowed per major section.

---

# Transformation Rule 05

## Improve Card Composition

Before

Title

Metric

Action

Paragraph

Badge

Random order

After

Title

↓

Summary

↓

Metric

↓

Action

↓

Expand

Rule

Every card follows the same reading sequence.

---

# Transformation Rule 06

## Reduce Action Density

Problem

Every card contains multiple buttons.

Transformation

One Primary Action

↓

Secondary Actions

↓

Text Links

Expected Result

Users immediately understand what action is most important.

---

# Transformation Rule 07

## Improve Typography

Before

Random sizes

Random weights

Random spacing

After

Typography Scale

H1

↓

H2

↓

H3

↓

Body

↓

Caption

Typography replaces decorative styling.

---

# Transformation Rule 08

## Improve White Space

Problem

Content feels compressed.

Transformation

Increase spacing between

Sections

Rows

Cards

Paragraphs

Lists

Whitespace should improve readability rather than reduce information density.

---

# Transformation Rule 09

## Reduce Information Density

Problem

Users receive too much information at once.

Transformation

Preview

↓

Expand

↓

Detail

Avoid displaying long interpretations immediately.

---

# Transformation Rule 10

## Improve Visual Weight

Problem

Every card competes equally for attention.

Transformation

One dominant card

↓

Supporting cards

↓

Reference cards

Visual emphasis should follow analytical importance.

---

# Transformation Rule 11

## Simplify Color Usage

Problem

Too many accent colors.

Transformation

Primary Accent

↓

Semantic Colors

↓

Neutral Colors

Decorative colors should be removed.

---

# Transformation Rule 12

## Simplify Icons

Problem

Icons appear everywhere.

Transformation

Use icons only where they reinforce understanding.

Icons should never replace text.

---

# Transformation Rule 13

## Improve Recommendation Presentation

Before

Long recommendation paragraphs.

After

Priority

↓

Action

↓

Reason

↓

Benefit

↓

Expand

Recommendations should be actionable.

---

# Transformation Rule 14

## Improve Interpretation

Before

Continuous text blocks.

After

Observation

↓

Explanation

↓

Impact

↓

Suggestion

Long-form reading should be comfortable.

---

# Transformation Rule 15

## Improve Knowledge Presentation

Before

Knowledge mixed with interpretation.

After

Definition

↓

Theory

↓

Reference

↓

Appendix

Educational content should remain secondary.

---

# Transformation Rule 16

## Enterprise Report Style

The final interface should resemble

Professional Consulting Software

Executive Report

Enterprise Analysis Platform

Avoid

Consumer applications

Marketing websites

Widget dashboards

---

# Transformation Matrix

| Current State | Transformation | Expected Result |
|---------------|---------------|----------------|
| Too many borders | Remove internal borders | Cleaner layout |
| Dense cards | Increase whitespace | Better readability |
| Equal visual weight | Introduce hierarchy | Better focus |
| Long paragraphs | Preview + Expand | Easier reading |
| Multiple CTA buttons | Single Primary CTA | Clear interaction |
| Random typography | Typography Scale | Consistent hierarchy |
| Decorative colors | Semantic colors only | Professional appearance |
| Nested cards | Flat composition | Reduced complexity |
| Uneven emphasis | Primary → Secondary → Tertiary | Better scanning |
| Dashboard feeling | Executive Report style | Enterprise quality |

---

# Cursor Transformation Rules

Cursor MUST

Identify visual issues before editing.

Preserve architecture.

Preserve layout.

Preserve reading flow.

Apply only approved transformation rules.

Validate against

VISUAL_LANGUAGE_SYSTEM

↓

VISUAL_REFERENCE_GALLERY

↓

Transformation Matrix

Cursor MUST NOT

Redesign architecture.

Move cards between Zones.

Invent new visual styles.

Invent spacing.

Invent typography hierarchy.

Invent color hierarchy.

Introduce decorative UI.

---

# Acceptance Criteria

The transformation is complete only when

✓ Architecture unchanged.

✓ Layout unchanged.

✓ Visual quality improved.

✓ Cognitive load reduced.

✓ Reading speed improved.

✓ Visual hierarchy strengthened.

✓ Professional appearance achieved.

✓ Enterprise report style preserved.

---

# Definition of Done

A transformed screen is considered complete only when

✓ Visual Language applied.

✓ Visual Reference matched.

✓ Transformation Rules followed.

✓ No regression introduced.

✓ Product Owner approves visual quality.

END OF DOCUMENT