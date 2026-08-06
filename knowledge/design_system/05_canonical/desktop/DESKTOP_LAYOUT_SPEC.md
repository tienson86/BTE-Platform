# DESKTOP_LAYOUT_SPEC.md

> BTE Design System
>
> Desktop Layout Specification
>
> Version: V1.0
>
> Status: CANONICAL
>
> This document defines the ONLY approved Desktop layout for the BTE Portal Result Page.
>
> This specification is mandatory for every implementation.
>
> UI Developers must NOT redesign, reinterpret, or optimize this layout.

---

# 1. Purpose

This document defines the physical layout of the Desktop Result Page.

It specifies:

- Section order
- Grid position
- Row structure
- Column span
- Reading flow
- Allowed behaviors
- Forbidden behaviors

This document does NOT define:

- Typography
- Colors
- Components
- Icons

Those are defined elsewhere.

---

# 2. Design Philosophy

The Result Page is a dashboard.

It is NOT a Masonry page.

It is NOT a Pinterest layout.

It is NOT an auto-flow layout.

Every section belongs to a predefined row.

Rows must remain visually aligned.

Reading order must follow top-to-bottom.

---

# 3. Reading Flow

Users should naturally read the page in the following order.

S00

↓

S01 → S02 → S09

↓

S03 → S04 → S05 → S10

↓

S06 → S07 → S08 → S11

This order MUST NOT change.

---

# 4. Desktop Grid

Viewport

1920 px

Container

1600 px

Grid

12 Columns

Outer Margin

32 px

Column Gap

24 px

Section Gap

24 px

Card Radius

16 px

---

# 5. Canonical Layout

############################################################

ROW 1

############################################################

Section

S00

Title

THÔNG TIN BỐI CẢNH

Grid

Columns 1–12

Width

Full

Height

Auto

Purpose

Context Header

############################################################

ROW 2

############################################################

S01

Columns 1–4

Purpose

Thông tin & Định hướng

-------------------------

S02

Columns 5–8

Purpose

Tổng quan & Hành động

-------------------------

S09

Columns 9–12

Purpose

Cung Phi / Quái Mệnh

Row 2 sections should appear balanced.

No Masonry.

############################################################

ROW 3

############################################################

S03

Columns 1–4

Purpose

Tứ Trụ

-------------------------

S04

Columns 5–8

Purpose

Cân bằng Ngũ hành

-------------------------

S05

Columns 9–10

Purpose

Sức mạnh Mệnh cục

-------------------------

S10

Columns 11–12

Purpose

Cân xương

IMPORTANT

All Row 3 sections belong to the SAME ROW.

DO NOT move S05 or S10 below S03.

DO NOT use Masonry.

DO NOT auto-pack cards.

############################################################

ROW 4

############################################################

S06

Columns 1–4

Purpose

Thập thần

-------------------------

S07

Columns 5–6

Purpose

Thần sát

-------------------------

S08

Columns 7–9

Purpose

Luận giải tổng hợp

-------------------------

S11

Columns 10–12

Purpose

Báo cáo tổng kết

IMPORTANT

All sections belong to Row 4.

No automatic positioning.

---

# 6. Section Priority

Highest

S03

S04

S08

Medium

S01

S02

S05

S06

S09

S10

Lower

S07

S11

Priority affects future expansion only.

It MUST NOT affect the canonical layout.

---

# 7. Height Rules

Rows are independent.

Sections inside one row may have different content heights.

However,

the visual top alignment MUST remain consistent.

Developers must NOT use Masonry layout.

Developers must NOT allow lower-row cards to move upward.

Rows must remain visually separated.

---

# 8. Forbidden Behaviors

The following are NOT allowed.

❌ Masonry Layout

❌ Pinterest Layout

❌ CSS auto packing

❌ Automatic row collapsing

❌ Auto balancing

❌ Reordering sections

❌ Moving S06 beside S03

❌ Moving S11 below S10

❌ Swapping S09 and S02

❌ Any layout optimization without approval

---

# 9. Mandatory Assets

S09

Must use approved Bagua asset.

Do NOT regenerate.

Do NOT redraw.

Use official SVG.

S03

Must use approved Four Pillars layout.

S04

Must use horizontal balance bars.

Radar chart is prohibited.

Pie chart is prohibited.

S06

Must use 10-card layout.

Summary layout is prohibited.

S11

Official title

BÁO CÁO TỔNG KẾT

Old title

PANEL HỌC TẬP

is deprecated.

---

# 10. Responsive

This document applies ONLY to Desktop.

Tablet has its own specification.

Mobile has its own specification.

Desktop rules must NOT be modified to accommodate smaller devices.

---

# 11. Source of Truth

This document is the canonical layout specification.

If implementation differs from this document,

this document takes precedence.

Implementation must be updated.

---

END OF DOCUMENT