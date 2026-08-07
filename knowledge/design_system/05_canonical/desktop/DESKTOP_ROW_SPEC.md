# DESKTOP_ROW_SPEC.md

> BTE Design System
>
> Desktop Row Specification
>
> Version: V2.0
>
> Status: CANONICAL
>
> This document defines the visual rhythm and row behavior of the Desktop Result Page.
>
> This specification supersedes all previous Equal Height rules.

---

# 1. Purpose

This document defines how rows behave visually.

It standardizes:

- Row grouping
- Reading rhythm
- Visual balance
- Card hierarchy
- Vertical alignment
- Natural height
- White space

This specification is mandatory.

---

# 2. Design Philosophy

The Desktop Result Page is a professional dashboard.

It is NOT a spreadsheet.

It is NOT a table.

It is NOT a masonry layout.

It is NOT a collection of equally sized cards.

The objective is:

Visual Rhythm

instead of

Equal Height.

The page should feel balanced,

not mechanically aligned.

---

# 3. Canonical Rows

The page consists of four independent rows.

--------------------------------------------------

ROW 1

S00

--------------------------------------------------

ROW 2

S01

S02

S09

--------------------------------------------------

ROW 3

S03

S04

S05

S10

--------------------------------------------------

ROW 4

S06

S07

S08

S11

--------------------------------------------------

Rows never merge.

Rows never overlap.

Rows never auto-pack.

---

# 4. Row Integrity

Each row is an independent visual block.

Cards belonging to one row

must remain inside that row.

Cards from different rows

must never interleave.

Example

Correct

Row 3

S03 S04 S05 S10

↓

Row 4

S06 S07 S08 S11

Incorrect

S03

↓

S06

↓

S04

↓

S07

This behavior is forbidden.

---

# 5. Natural Height

Cards should use the height naturally required by their content.

Do NOT artificially stretch cards.

Do NOT insert empty space simply to match neighboring cards.

Card height should be content-driven.

---

# 6. Visual Rhythm

Cards inside the same row

do NOT need identical height.

Instead,

they should create a visually balanced composition.

Example

Correct

S03

██████████

S04

████

S05

███

S10

█████

Incorrect

██████████

██████████

██████████

██████████

The first example is preferred.

---

# 7. Card Hierarchy

Some cards intentionally carry more information.

These cards are expected to be taller.

Primary Cards

• S03

• S08

• S11

Secondary Cards

• S01

• S02

• S09

Summary Cards

• S04

• S05

• S06

• S07

• S10

Summary cards should remain compact.

Do not enlarge them unnecessarily.

---

# 8. Vertical Alignment

Cards align at the top.

Top edges must align.

Bottom edges do NOT need to align.

Visual consistency is more important than geometric symmetry.

---

# 9. White Space

Whitespace belongs between rows,

not inside cards.

Large empty areas inside cards should be avoided.

Natural card proportions are preferred.

---

# 10. Implementation Strategy

The page should be implemented as

four independent row containers.

Each row owns its own Grid.

Example

ResultPage

↓

Row01Grid

↓

Row02Grid

↓

Row03Grid

↓

Row04Grid

Each row uses CSS Grid internally.

The page itself is not a Grid.

---

# 11. CSS Recommendation

Page

display: flex;

flex-direction: column;

gap: 24px;

--------------------------------

Each Row

display: grid;

--------------------------------

Cards

align-self: start;

height: auto;

Do NOT use

height: 100%

unless explicitly required.

---

# 12. Forbidden Behaviors

The following are prohibited.

❌ Masonry Layout

❌ Pinterest Layout

❌ CSS Columns

❌ Auto Packing

❌ Dense Packing

❌ Equal Height by default

❌ Artificial stretching

❌ Empty cards

❌ Placeholder spacing

❌ Stretching cards simply to fill rows

---

# 13. Canonical Layout Goal

The target is visual balance.

NOT geometric equality.

Developers should compare the implementation against

CANONICAL_PORTAL_UI_DESKTOP_V2

rather than attempting to make every card the same height.

The canonical image has higher priority than mechanical layout rules.

---

# 14. Source of Truth

If implementation differs from

CANONICAL_PORTAL_UI_DESKTOP_V2

the implementation must be updated.

The Canonical UI image always has higher priority than assumptions.

---

END OF DOCUMENT