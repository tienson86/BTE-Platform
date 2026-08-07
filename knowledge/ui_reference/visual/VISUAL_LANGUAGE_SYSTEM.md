# VISUAL_LANGUAGE_SYSTEM.md

Version: 2.0

Status: DRAFT

Owner: BTE UI Architecture

Priority: HIGH

Depends On

- PACK_01_DESIGN_PRINCIPLES
- PACK_02_LAYOUT_SYSTEM
- PACK_03_COMPONENT_STANDARD
- PACK_04_UI_PRESENTATION_STANDARD
- PACK_05_ACCESSIBILITY
- PACK_06_RESULT_PAGE_LAYOUT_STANDARD
- PACK_07_RESULT_PAGE_BLUEPRINT

---

# 1. Purpose

This document defines the official visual language of the BTE Platform.

Unlike the Design System,

which defines structure,

the Visual Language defines appearance.

It specifies how the interface should feel,

how information should be perceived,

and how visual hierarchy should guide user attention.

---

# 2. Design Philosophy

The BTE Platform is not a marketing website.

It is not a dashboard.

It is not a collection of widgets.

It is a professional analytical platform.

Every screen should resemble

an executive analytical report

used by professional consultants.

Users should immediately perceive

clarity

authority

precision

trust

professionalism

before reading any content.

---

# 3. Design Keywords

The visual identity of BTE should be described by the following keywords.

Professional

Calm

Elegant

Minimal

Structured

Readable

Trustworthy

Focused

Analytical

Premium

Avoid

Playful

Colorful

Noisy

Decorative

Crowded

Consumer-style

---

# 4. Visual Hierarchy

Every screen should present information in the following order.

Executive Summary

↓

Key Metrics

↓

Analysis

↓

Visualization

↓

Recommendations

↓

Interpretation

↓

Knowledge

The interface should naturally guide the user's eyes through this hierarchy.

---

# 5. Visual Principles

The interface should prioritize

Whitespace over borders.

Typography over decoration.

Hierarchy over quantity.

Grouping over separation.

Consistency over creativity.

Every visual decision should reduce cognitive load.
# 6. Visual Weight

Not all components should have equal visual importance.

Visual weight should be intentionally distributed.

Primary

Executive Summary

Critical Findings

Primary CTA

Secondary

Analysis Cards

Charts

Metrics

Tertiary

Knowledge

References

Metadata

Decorative elements should have minimal visual weight.

The user's attention should always be directed by hierarchy rather than by excessive color or decoration.
# 7. Border Strategy

Borders should not be used to separate every element.

Preferred order

Whitespace

↓

Typography

↓

Background contrast

↓

Border

Avoid nested bordered containers.

A region should normally have one visual boundary.

Items inside the region should rely on spacing rather than additional borders.

# 8. Surface Strategy

Every screen should use a limited number of visual surfaces.

Background

↓

Section

↓

Card

↓

Interactive Component

Different surfaces should be distinguishable primarily through spacing and subtle elevation rather than strong borders.
---

# 9. Typography Scale

Typography is the primary tool for establishing visual hierarchy.

The interface should communicate importance through size, weight, spacing, and rhythm rather than excessive color or decoration.

---

## 9.1 Typography Levels

| Level | Usage | Size | Weight |
|--------|------|------|--------|
| Display | Executive Numbers | 40px | Bold |
| H1 | Page Title | 32px | Bold |
| H2 | Section Title | 24px | SemiBold |
| H3 | Card Title | 20px | SemiBold |
| H4 | Group Title | 18px | Medium |
| Body | Main Content | 16px | Regular |
| Caption | Supporting Text | 14px | Regular |
| Meta | Auxiliary Information | 12px | Medium |

---

## 9.2 Reading Rhythm

Headings should create a predictable reading rhythm.

Example

Page Title

↓

Section

↓

Card

↓

Body

↓

Caption

Users should immediately understand the hierarchy without relying on color.

---

## 9.3 Line Length

Recommended

45–75 characters

Avoid extremely wide paragraphs.

Reading comfort takes priority over information density.

---

## 9.4 Line Height

Display

110%

Headings

120%

Body

150%

Caption

140%

Long-form interpretation should prioritize readability.

---

## 9.5 Typography Principles

Typography should replace unnecessary visual decoration.

Never increase font size merely to attract attention.

Use weight before color.

Use spacing before borders.

Use hierarchy before emphasis.
---

# 10. Color Hierarchy

Color communicates meaning.

It should never be used as decoration.

---

## 10.1 Color Roles

Primary

Brand Identity

Secondary

Navigation

Success

Positive Findings

Warning

Attention

Danger

Critical Issues

Neutral

Supporting Content

---

## 10.2 Accent Rule

Each screen should have

one primary accent.

Multiple competing accent colors should be avoided.

---

## 10.3 Visual Priority

Priority should follow

Typography

↓

Spacing

↓

Contrast

↓

Color

Color is the final layer of emphasis.

---

## 10.4 Information Colors

Positive

Green

Neutral

Gray

Negative

Red

Warning

Amber

Information

Blue

Do not invent additional semantic colors.

---

## 10.5 Background Colors

Background surfaces should remain subtle.

The background should support the content rather than compete with it.
---

# 11. Card Elevation

Elevation communicates grouping and hierarchy.

It should not be used excessively.

---

## 11.1 Elevation Levels

Level 0

Background

Level 1

Standard Cards

Level 2

Focused Cards

Level 3

Dialogs

Level 4

Overlays

---

## 11.2 Shadow Strategy

Prefer subtle elevation.

Avoid deep shadows.

The interface should feel calm and professional.

---

## 11.3 Active Cards

Focused cards may increase elevation slightly.

Never increase border thickness.

---

## 11.4 Hover

Hover should primarily affect

Elevation

Background

Shadow

Avoid dramatic animations.
---

# 12. Button Hierarchy

Buttons represent actions.

Not every action deserves equal visual attention.

---

## 12.1 Button Types

Primary

One per screen

Secondary

Supporting actions

Tertiary

Contextual actions

Text Button

Low-priority navigation

---

## 12.2 CTA Rule

Each major screen should have

one dominant CTA.

Multiple primary buttons reduce clarity.

---

## 12.3 Button Density

Avoid displaying multiple action buttons inside every card.

Use expandable menus when appropriate.

---

## 12.4 Visual Consistency

Button styles should remain consistent across the platform.

Never redesign buttons for individual pages.
---

# 13. Iconography

Icons reinforce meaning.

They do not replace text.

---

## 13.1 Icon Style

Use a single icon family throughout the platform.

Stroke weight

Corner radius

Optical balance

should remain consistent.

---

## 13.2 Icon Usage

Icons should precede labels.

Avoid standalone icons unless universally understood.

---

## 13.3 Color

Icons inherit semantic color.

Decorative colors are discouraged.

---

## 13.4 Density

Do not place icons beside every line of text.

Reserve icons for important visual anchors.
---

# 14. White Space Rhythm

Whitespace creates clarity.

It should follow a predictable rhythm.

---

## 14.1 Rhythm Scale

XS

8px

S

16px

M

24px

L

32px

XL

48px

XXL

64px

---

## 14.2 Usage

Card Padding

M

Section Gap

L

Major Zone Gap

XL

---

## 14.3 Rhythm Rule

Spacing should follow the predefined rhythm.

Avoid arbitrary values.

Consistency creates harmony.
---

# 15. Information Density

Information should feel concentrated,

not crowded.

---

## 15.1 Density Levels

Low

Executive Summary

Medium

Analysis

High

Knowledge

Very High

Appendix

---

## 15.2 Reading Principle

Users should consume information progressively.

Preview

↓

Expand

↓

Detail

Never overwhelm the user immediately.

---

## 15.3 Compression Strategy

When information grows,

Split

↓

Collapse

↓

Navigate

Never reduce readability.
---

# 16. Executive Report Style

The visual appearance should resemble

an executive consulting report.

Not

a dashboard.

---

## 16.1 Characteristics

Calm

Structured

Balanced

Readable

Minimal

Professional

---

## 16.2 Avoid

Flashy gradients

Heavy shadows

Decorative graphics

Rounded excess

Dense borders

Bright backgrounds

---

## 16.3 Desired Impression

Users should feel

Confidence

Authority

Precision

Trust
---

# 17. Anti-Patterns

The following patterns are prohibited.

---

## Layout

✗ Uneven card heights

✗ Misaligned rows

✗ Nested scrolling

✗ Arbitrary spacing

---

## Typography

✗ Excessive font sizes

✗ Too many weights

✗ Decorative fonts

---

## Color

✗ Competing accents

✗ Random semantic colors

✗ Saturated backgrounds

---

## Components

✗ Cards inside cards inside cards

✗ Multiple primary buttons

✗ Decorative icons

✗ Empty visual containers

---

## User Experience

✗ Information overload

✗ Long uninterrupted paragraphs

✗ Hidden primary actions

✗ Inconsistent reading flow
---

# 18. Visual QA Checklist

Before approving any screen,

verify the following.

---

## Visual Hierarchy

□ Clear primary focus

□ Clear secondary focus

□ Predictable reading order

---

## Typography

□ Correct hierarchy

□ Comfortable reading

□ Consistent rhythm

---

## Layout

□ Equal-height rows

□ Balanced spacing

□ Stable alignment

---

## Color

□ Correct semantic colors

□ Single dominant accent

□ Professional appearance

---

## Components

□ Consistent card style

□ Consistent button hierarchy

□ Consistent iconography

---

## Overall Impression

□ Calm

□ Professional

□ Premium

□ Analytical

□ Trustworthy

---

A screen should not be approved until every item above is satisfied.
