# DESKTOP_GRID_SPEC.md

> BTE Design System
>
> Desktop Grid Specification
>
> Version: V1.0
>
> Status: CANONICAL
>
> This document defines the official Desktop Grid System for the BTE Platform.
>
> Every Desktop screen MUST follow this specification.

---

# 1. Purpose

This document defines the desktop layout grid.

It standardizes:

- Container width
- Grid columns
- Margins
- Gutters
- Section spacing
- Card spacing
- Alignment
- Responsive limits

This document applies to:

- Portal
- Analysis Console
- Admin Console

Future desktop applications should reuse this grid whenever possible.

---

# 2. Design Philosophy

The Desktop UI follows a predictable dashboard layout.

The grid must:

- Provide visual stability.
- Keep related information aligned.
- Support future expansion.
- Minimize layout shifts.
- Maintain consistency across all BTE products.

The grid is not content-dependent.

Content must adapt to the grid.

The grid must never adapt to content.

---

# 3. Viewport

Reference Resolution

1920 × 1080

Minimum Supported Width

1600 px

Maximum Design Width

1920 px

Centered Layout

Yes

Horizontal Scroll

Never

Vertical Scroll

Allowed

---

# 4. Container

Container Width

1600 px

Container Alignment

Centered

Maximum Width

1600 px

Minimum Width

1600 px

Padding Left

32 px

Padding Right

32 px

Top Margin

24 px

Bottom Margin

24 px

---

# 5. Grid System

Grid Type

CSS Grid

Columns

12

Column Width

Flexible

Column Gap (Gutter)

24 px

Row Gap

24 px

Grid Flow

Row

Auto Placement

Disabled

Masonry Layout

Forbidden

Auto Packing

Forbidden

---

# 6. Column Distribution

Columns are equally distributed.

Example

|1|2|3|4|5|6|7|8|9|10|11|12|

Every section occupies predefined columns.

Column spans are defined in:

DESKTOP_LAYOUT_SPEC.md

---

# 7. Row Rules

Rows are logical groups.

Each row represents one information layer.

Rows must never collapse.

Rows must never merge.

Cards from one row must not move into another row.

Example

Row 1

S00

------------------

Row 2

S01

S02

S09

------------------

Row 3

S03

S04

S05

S10

------------------

Row 4

S06

S07

S08

S11

---

# 8. Spacing Rules

Outer Margin

32 px

Section Gap

24 px

Card Padding

24 px

Internal Component Gap

16 px

Heading → Content

16 px

Content → Footer

24 px

Button Gap

16 px

List Item Gap

8 px

Paragraph Gap

12 px

---

# 9. Card Rules

Border Radius

16 px

Border

1 px

Shadow

Design Token Shadow-02

Background

Surface

Overflow

Hidden

Cards must align with the grid.

Cards must never overlap.

---

# 10. Alignment Rules

Section titles align left.

Card headers align left.

Action buttons align right unless defined otherwise.

Icons align with text baseline.

Progress bars align with labels.

Cards inside the same row align to the same top edge.

---

# 11. White Space

White space is intentional.

Developers must not remove white space to fit more content.

Avoid visual crowding.

Breathing room improves readability.

---

# 12. Expansion Rules

If a section grows in future versions:

Preferred order

Increase height

↓

Increase internal scrolling (if appropriate)

↓

Move to next major version

Do NOT change grid spans without updating:

DESKTOP_LAYOUT_SPEC.md

---

# 13. Forbidden Behaviors

The following are prohibited.

❌ Masonry Grid

❌ CSS Columns Layout

❌ Pinterest Style

❌ Auto Packing

❌ Dynamic Reordering

❌ Variable Gutters

❌ Nested Independent Grids without approval

❌ Negative Margins

❌ Absolute Positioning for layout

❌ Overlapping Cards

❌ Uneven Outer Margins

---

# 14. CSS Recommendation

Recommended implementation

display: grid

grid-template-columns: repeat(12, 1fr);

gap: 24px;

max-width: 1600px;

margin: 0 auto;

Developers may adapt implementation details,

but visual output must remain identical.

---

# 15. Future Compatibility

Tablet

Uses independent specification.

Mobile

Uses independent specification.

Desktop Grid must not change because of responsive requirements.

---

# 16. Source of Truth

This document defines the official Desktop Grid.

If implementation differs,

this document has higher priority.

Implementation must be updated.

---

END OF DOCUMENT