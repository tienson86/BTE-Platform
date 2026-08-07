# PACK_07_RESULT_PAGE_BLUEPRINT.md

Version: 1.0

Status: OFFICIAL

Owner: BTE UI Architecture

Depends on

- PACK_01_DESIGN_PRINCIPLES.md
- PACK_02_LAYOUT_SYSTEM.md
- PACK_03_COMPONENT_STANDARD.md
- PACK_04_UI_PRESENTATION_STANDARD.md
- PACK_05_ACCESSIBILITY.md
- PACK_06_RESULT_PAGE_LAYOUT_STANDARD.md

---

# 1. Purpose

This document defines the official visual blueprint of the BTE Result Page.

Unlike PACK_06, which specifies screen architecture,

this document specifies the exact placement of rows, grids, cards, and visual regions.

The blueprint is the implementation reference for Cursor and Frontend Developers.

No Result Page should be implemented without following this blueprint.

---

# 2. Design Philosophy

The Result Page should feel like

an executive analytical report,

not

a dashboard.

Users should naturally read from

top

↓

summary

↓

analysis

↓

interpretation

↓

recommendation

↓

knowledge

without confusion.

---

# 3. Overall Screen Blueprint

```

┌──────────────────────────────────────────────────────────────┐
│ Header                                                       │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Context Row                                                  │
└──────────────────────────────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────┐
│              │              │              │
│ Executive    │ Core         │ Destiny      │
│ Summary      │ Indicators   │ Direction    │
│              │              │              │
└──────────────┴──────────────┴──────────────┘

┌──────────────┬──────────────┬──────────────┐
│              │              │              │
│ Five         │ Strength     │ Ten Gods     │
│ Elements     │ Analysis     │ Analysis     │
│              │              │              │
└──────────────┴──────────────┴──────────────┘

┌──────────────┬──────────────┐
│              │              │
│ Radar Chart  │ Timeline     │
│              │              │
└──────────────┴──────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Recommendation Zone                                          │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Interpretation Zone                                          │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Knowledge Zone                                               │
└──────────────────────────────────────────────────────────────┘

Footer

```

---

# 4. Reading Direction

```

Header

↓

Context

↓

Executive Summary

↓

Core Analysis

↓

Visualization

↓

Recommendation

↓

Interpretation

↓

Knowledge

↓

Footer

```

This order is mandatory.

Never change it.
---

# 5. Result Page Blueprint

The following blueprint represents the canonical layout of the Result Page.

Every implementation should preserve this composition.

```

┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER                                                                       │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ CONTEXT ROW                                                                  │
│ User • Birth • Chart • Report Status • Actions                              │
└──────────────────────────────────────────────────────────────────────────────┘


┌────────────────────┬────────────────────┬────────────────────┐
│ Executive Summary  │ Core Indicators    │ Destiny Direction  │
│                    │                    │                    │
│        M           │         M          │         M          │
└────────────────────┴────────────────────┴────────────────────┘


┌────────────────────┬────────────────────┬────────────────────┐
│ Five Elements      │ Strength           │ Ten Gods           │
│                    │                    │                    │
│        XL          │        XL          │        XL          │
└────────────────────┴────────────────────┴────────────────────┘


┌──────────────────────────────┬───────────────────────────────┐
│ Radar Chart                  │ Luck Timeline                │
│                              │                              │
│             XL               │             XL               │
└──────────────────────────────┴───────────────────────────────┘


┌──────────────────────────────────────────────────────────────┐
│ Recommendation Zone                                           │
│                                                              │
│                          L                                   │
└──────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────┐
│ Interpretation Zone                                           │
│                                                              │
│                     AUTO HEIGHT                              │
└──────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────┐
│ Knowledge Zone                                                │
│                                                              │
│                     AUTO HEIGHT                              │
└──────────────────────────────────────────────────────────────┘


Footer

```

---

# 6. Row Blueprint

Every row has predefined dimensions.

---

## Row 01

Context

```

┌──────────┬──────────┬──────────┬──────────┐

User

Birth

Report

Actions

```

Height

S

---

## Row 02

Executive Summary

```

┌──────────────┬──────────────┬──────────────┐

Summary

Indicators

Direction

```

Height

M

---

## Row 03

Analysis

```

┌──────────────┬──────────────┬──────────────┐

Five Elements

Strength

Ten Gods

```

Height

XL

---

## Row 04

Visualization

```

┌────────────────────┬────────────────────┐

Radar

Timeline

```

Height

XL

---

## Row 05

Recommendations

```

┌──────────────────────────────────────────┐

Recommendations

```

Height

L

---

## Row 06

Interpretation

```

┌──────────────────────────────────────────┐

Interpretation

```

AUTO HEIGHT

---

## Row 07

Knowledge

```

┌──────────────────────────────────────────┐

Knowledge

```

AUTO HEIGHT

---

# 7. Card Placement Matrix

The following table defines the official position of every card.

| Card | Zone | Row | Column Span | Height |
|------|------|-----|------------|---------|
| Executive Summary | Summary | 02 | 4 | M |
| Core Indicators | Summary | 02 | 4 | M |
| Destiny Direction | Summary | 02 | 4 | M |
| Five Elements | Analysis | 03 | 4 | XL |
| Strength | Analysis | 03 | 4 | XL |
| Ten Gods | Analysis | 03 | 4 | XL |
| Radar Chart | Visualization | 04 | 6 | XL |
| Timeline | Visualization | 04 | 6 | XL |
| Recommendation | Recommendation | 05 | 12 | L |
| Interpretation | Interpretation | 06 | 12 | AUTO |
| Knowledge | Knowledge | 07 | 12 | AUTO |

Cards may not be moved without updating this specification.

---

# 8. Card Relationship Map

The relationship between cards is predefined.

```

Executive Summary

│

├──────────────► Core Indicators

│

├──────────────► Destiny Direction

│

▼

Five Elements

│

├──────────────► Strength

│

├──────────────► Ten Gods

│

▼

Radar Chart

│

▼

Recommendations

│

▼

Interpretation

│

▼

Knowledge

```

Users should naturally follow this reading path.
---

# 9. Visual Balance Blueprint

Visual Balance ensures that every Result Page feels stable, harmonious, and professional regardless of content size.

Balance is determined by rows, proportions, whitespace, and visual weight rather than by the amount of data.

---

## 9.1 Visual Weight Principle

Every row should maintain balanced visual weight.

The eye should naturally move from left to right and from top to bottom.

No single card should visually dominate an entire row unless intentionally designed.

---

## 9.2 Equal Height Principle

Within the same row,

all fixed-height cards must have identical heights.

Correct

```

┌──────┬──────┬──────┐
│ 320  │ 320  │ 320  │
└──────┴──────┴──────┘

```

Incorrect

```

┌──────┬──────────────┬──────┐
│ 220  │     560      │ 300  │
└──────┴──────────────┴──────┘

```

Rows should appear visually stable.

---

## 9.3 Width Balance

Columns should distribute visual weight evenly.

Preferred

```

4 + 4 + 4

```

```

6 + 6

```

```

3 + 3 + 3 + 3

```

Avoid

```

2 + 8 + 2

```

unless required by the official blueprint.

---

## 9.4 Reading Balance

Users should spend similar reading time across cards within the same row.

Target reading time

Summary Cards

15–30 seconds

Analysis Cards

30–60 seconds

Visualization Cards

20–40 seconds

Recommendation Cards

30–60 seconds

Large differences indicate poor information balance.

---

## 9.5 Content Balance

Each card should contain similar content density.

Example

Correct

• Title

• Summary

• Metrics

• Preview

Incorrect

Card A

1 sentence

Card B

12 paragraphs

Large differences should be avoided.

---

## 9.6 Visual Rhythm

The Result Page should create a predictable rhythm.

Example

```

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

```

Users should feel guided through the page.

---

## 9.7 Balance Validation

Every Result Page should satisfy

✓ Equal-height rows

✓ Balanced card widths

✓ Consistent visual weight

✓ Stable alignment

✓ Predictable reading rhythm

✓ No isolated oversized card

---

# 10. White Space Blueprint

Whitespace is an intentional design element.

It separates information, improves readability, and reduces cognitive load.

Whitespace should never be considered wasted space.

---

## 10.1 Outer Margin

Desktop

32px

Tablet

24px

Mobile

16px

Outer margins remain consistent across all pages.

---

## 10.2 Row Spacing

Spacing between rows

32px

Large sections

40px

Major transitions

48px

Spacing should follow a consistent rhythm.

---

## 10.3 Card Spacing

Horizontal Gap

24px

Vertical Gap

24px

Cards should never touch each other.

---

## 10.4 Internal Padding

Every card uses

Top

24px

Bottom

24px

Left

24px

Right

24px

Compact cards may use 16px.

---

## 10.5 Title Spacing

Card Title

↓

16px

↓

Content

Section Title

↓

24px

↓

Grid

Spacing should reinforce hierarchy.

---

## 10.6 Paragraph Spacing

Paragraph

↓

12px

↓

Paragraph

Lists

↓

8px

↓

Item

Long text should breathe naturally.

---

## 10.7 Section Separation

Major screen sections should feel independent.

Example

```

Summary

====================

Analysis

====================

Visualization

====================

Recommendation

====================

Interpretation

```

Transitions should be immediately recognizable.

---

## 10.8 Empty Space Rules

Whitespace should increase

Readability

↓

Focus

↓

Scanning Speed

↓

Professional Appearance

Do not remove whitespace simply to display more information.

---

## 10.9 Dense Content Strategy

When content becomes too dense,

never reduce whitespace.

Instead

Split Cards

↓

Split Rows

↓

Create Expandable Sections

↓

Create Additional Pages

Whitespace should always be preserved.

---

## 10.10 White Space Validation

Every Result Page should satisfy

✓ Consistent outer margins

✓ Equal row spacing

✓ Equal card spacing

✓ Consistent internal padding

✓ Comfortable reading rhythm

✓ No crowded sections

✓ No excessive empty areas

✓ Balanced visual composition

---

END OF BLUEPRINT