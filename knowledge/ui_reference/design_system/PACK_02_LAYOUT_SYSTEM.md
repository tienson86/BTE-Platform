# PACK_02_LAYOUT_SYSTEM.md

Version: 1.0
Status: OFFICIAL
Owner: BTE UI Architecture
Depends on:
- PACK_01_DESIGN_PRINCIPLES.md

---

# 1. Purpose

This document defines the official layout system for the BTE Platform.

The layout system ensures that every screen across the platform follows a consistent structure, spacing rhythm, alignment strategy, and responsive behavior.

This specification applies to:

- BTE Portal
- Analysis Console
- Admin Portal
- Report Viewer
- Future Mobile Applications

---

# 2. Layout Philosophy

The layout is responsible for organizing information, not decorating it.

A user should immediately understand:

- where they are
- what they are looking at
- what deserves attention
- what action comes next

The layout must remain visually stable regardless of data size.

---

# 3. Global Page Structure

Every page follows the same hierarchy.

```
+-------------------------------------------------------+
| Header                                                |
+------------------+------------------------------------+
| Sidebar          |                                    |
|                  |                                    |
|                  | Main Content                       |
|                  |                                    |
|                  |                                    |
+------------------+------------------------------------+
```

Hierarchy

```
Application

↓

Page

↓

Section

↓

Grid

↓

Card

↓

Component

↓

Content
```

---

# 4. Maximum Content Width

Desktop

```
max-width: 1600px
```

Ultra Wide

```
max-width: 1800px
```

Content must remain centered.

Never stretch endlessly.

---

# 5. Grid System

Desktop

12-column Grid

Tablet

8-column Grid

Mobile

4-column Grid

Standard gap

```
24px
```

Never use arbitrary column counts.

---

# 6. Page Padding

Desktop

```
32px
```

Tablet

```
24px
```

Mobile

```
16px
```

Padding must be consistent.

---

# 7. Spacing System

Official spacing scale

```
4
8
12
16
24
32
40
48
64
80
96
```

No custom spacing values.

---

# 8. Vertical Rhythm

Sections

```
32px
```

Rows

```
24px
```

Cards

```
24px
```

Inside Card

```
16px
```

Component Gap

```
12px
```

---

# 9. Card Layout

Cards are the fundamental layout unit.

Each card has:

Header

↓

Body

↓

Footer (optional)

Never mix multiple unrelated purposes in one card.

---

# 10. Card Width

Small

25%

Medium

50%

Large

75%

Full

100%

Do not create arbitrary widths.

---

# 11. Card Height Strategy

Cards belong to predefined height classes.

Example

XS

160px

S

240px

M

320px

L

420px

XL

560px

Never allow content to define card height.

---

# 12. Equal Height Rule

Cards inside the same row should use the same height class.

Incorrect

```
200
420
310
```

Correct

```
320
320
320
```

---

# 13. Section Structure

Every section contains:

Section Title

↓

Section Description (optional)

↓

Grid

↓

Cards

---

# 14. Sidebar Layout

Sidebar width

```
240px
```

Collapsed

```
72px
```

Sticky

Yes

Scrollable

Independent

---

# 15. Header Layout

Height

```
72px
```

Contains

Logo

Navigation

Search

Notification

User Menu

Header never scrolls horizontally.

---

# 16. Content Area

Main content should scroll.

Sidebar remains fixed.

Header remains fixed.

---

# 17. Alignment Rules

Text

Left aligned

Numbers

Right aligned

Badges

Centered vertically

Buttons

Aligned consistently

---

# 18. Responsive Breakpoints

Mobile

<640px

Tablet

640–1023px

Desktop

1024–1439px

Wide

1440px+

Ultra Wide

1800px+

---

# 19. Responsive Behavior

Cards wrap automatically.

Never scale typography dramatically.

Avoid horizontal scrolling.

Overflow belongs inside components.

---

# 20. White Space Rules

Whitespace improves comprehension.

Minimum distance

Between sections

32px

Between cards

24px

Inside cards

16px

Never remove whitespace to fit more data.

---

# 21. Scroll Strategy

Preferred

Page scroll

Allowed

Internal card scroll

Avoid

Nested scrolling

Never

Horizontal scrolling

---

# 22. Sticky Components

Sticky

Sidebar

Header

Optional

Action Toolbar

Filters

Never

Individual content cards

---

# 23. Empty State Layout

Every empty state contains

Icon

↓

Title

↓

Description

↓

Primary Action

Never leave blank containers.

---

# 24. Loading Layout

Skeletons must occupy the final layout.

Loading must never change card dimensions.

Avoid layout shifts.

---

# 25. Error Layout

Every error card contains

Status

↓

Reason

↓

Recovery Action

↓

Retry Button

---

# 26. Dashboard Rules

Dashboard pages should prioritize

Overview

↓

Key Metrics

↓

Analysis

↓

Details

↓

History

Never display detailed reports before summaries.

---

# 27. Result Page Rules

Result pages always follow

Summary

↓

Key Findings

↓

Analysis

↓

Charts

↓

Recommendations

↓

Detailed Interpretation

↓

Appendix

---

# 28. Layout Anti-Patterns

Never

❌ Stretch cards because of long text

❌ Unequal spacing

❌ Floating elements

❌ Random widths

❌ Nested grids inside nested grids

❌ Cards without titles

❌ Horizontal scrolling

❌ Layout jumping

---

# 29. Relationship with Other Specifications

This document defines layout only.

Component appearance

↓

PACK_03_COMPONENT_STANDARD.md

Dynamic content behavior

↓

PACK_04_UI_PRESENTATION_STANDARD.md

---

# 30. Acceptance Criteria

A layout complies if

✓ Grid is consistent

✓ Spacing follows official scale

✓ Cards align correctly

✓ Equal-height rows

✓ Stable scrolling

✓ Responsive across breakpoints

✓ No layout shift

✓ White space preserved

✓ Content remains readable

✓ Future modules can be inserted without redesign

---

END OF DOCUMENT