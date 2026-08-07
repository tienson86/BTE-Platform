# VISUAL_REFERENCE_GALLERY.md

Version: 1.0

Status: OFFICIAL

Owner: BTE UI Architecture

Priority: HIGH

Depends On

- VISUAL_LANGUAGE_SYSTEM.md

---

# Purpose

This document provides visual reference patterns for the BTE Platform.

Unlike the Design System,

which defines rules,

this document demonstrates how those rules should look in practice.

Each visual pattern contains

- Good Example
- Bad Example
- Reason
- Usage

Cursor should imitate the approved visual examples rather than invent new visual styles.

---

# Pattern 01 — Executive Summary

Purpose

Present the most important conclusions at the top of the page.

GOOD

┌────────────┬────────────┬────────────┐
│ Executive  │ Indicators │ Direction  │
│ Summary    │            │            │
└────────────┴────────────┴────────────┘

✓ Equal width

✓ Equal height

✓ Balanced whitespace

✓ One primary visual focus

BAD

┌──────────┬────────────────────┬───────┐
│ Small    │      Huge Card     │ Tiny  │
└──────────┴────────────────────┴───────┘

✗ Uneven proportions

✗ Visual imbalance

✗ Competing attention

---

# Pattern 02 — Card Composition

GOOD

┌────────────────────────────┐
│ Title                      │
│                            │
│ Summary                    │
│                            │
│ Metric                     │
│                            │
│ Action                     │
└────────────────────────────┘

✓ Predictable reading order

✓ Comfortable spacing

BAD

┌────────────────────────────┐
│TitleMetricActionSummaryText│
└────────────────────────────┘

✗ Crowded

✗ Difficult to scan

---

# Pattern 03 — Border Strategy

GOOD

┌────────────────────────────┐
│                            │
│   Content                  │
│                            │
└────────────────────────────┘

Whitespace separates content.

BAD

┌────────────────────────────┐
│┌──────────────────────────┐│
││┌────────────────────────┐││
│││Content                 │││
││└────────────────────────┘││
│└──────────────────────────┘│
└────────────────────────────┘

✗ Borders inside borders

✗ Excessive visual noise

---

# Pattern 04 — Typography Hierarchy

GOOD

Page Title

↓

Section

↓

Card Title

↓

Body

↓

Caption

✓ Easy to scan

✓ Strong hierarchy

BAD

Page Title

Body

Caption

Title

Body

Caption

✗ Random reading flow

---

# Pattern 05 — White Space

GOOD

┌────────────────────────────┐

      Title

      Summary

      Metric

      Action

└────────────────────────────┘

✓ Comfortable

✓ Balanced

BAD

┌────────────────────────────┐
│TitleSummaryMetricAction    │
└────────────────────────────┘

✗ Dense

✗ Stressful

---

# Pattern 06 — Information Density

GOOD

Preview

↓

Expand

↓

Detail

Users progressively discover information.

BAD

20 paragraphs immediately visible.

✗ Cognitive overload

---

# Pattern 07 — Recommendation

GOOD

Priority

↓

Action

↓

Reason

↓

Benefit

↓

Expand

✓ Executive reading

BAD

Long essay

↓

Recommendation hidden

✗ No actionable guidance

---

# Pattern 08 — Interpretation

GOOD

Observation

↓

Explanation

↓

Impact

↓

Suggestion

✓ Structured narrative

BAD

One uninterrupted wall of text.

✗ Poor readability

---

# Pattern 09 — Knowledge

GOOD

Definition

↓

Theory

↓

Reference

↓

Appendix

✓ Educational progression

BAD

Random knowledge blocks.

✗ No learning hierarchy

---

# Pattern 10 — Button Hierarchy

GOOD

[ Primary ]

Secondary

Text Link

✓ One clear action

BAD

[Primary]

[Primary]

[Primary]

[Primary]

✗ Competing actions

---

# Pattern 11 — Visual Weight

GOOD

██████████

Executive Summary

██████

Analysis

███

Knowledge

✓ Clear visual hierarchy

BAD

████████

████████

████████

████████

Everything has equal emphasis.

✗ No focus

---

# Pattern 12 — Dashboard vs Executive Report

Dashboard

┌──┬──┬──┬──┐
│K │K │K │K │
├──┼──┼──┼──┤
│C │C │C │C │
└──┴──┴──┴──┘

Executive Report

Summary

↓

Analysis

↓

Visualization

↓

Recommendation

↓

Interpretation

↓

Knowledge

BTE should always resemble an Executive Report.

---

# Pattern 13 — Before vs After

BEFORE

Many borders

Many cards

Many colors

Many buttons

Visual noise

AFTER

Clear hierarchy

Balanced spacing

Minimal borders

Single primary action

Professional appearance

---

# Cursor Visual Rules

Before modifying any screen

Cursor MUST

1.

Identify the content type.

↓

2.

Select the official Layout Pattern.

↓

3.

Apply the Visual Language.

↓

4.

Compare against this Gallery.

↓

5.

Render.

Cursor MUST NOT

Invent visual styles.

Invent spacing.

Invent border styles.

Invent button hierarchy.

Invent typography hierarchy.

Invent visual weight.

---

# Visual Approval Checklist

Before a screen is approved

✓ Professional

✓ Balanced

✓ Readable

✓ Minimal

✓ Analytical

✓ Premium

✓ Consistent

If any item fails,

the screen should return to the design stage.

END OF DOCUMENT