# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 02 — DESIGN SYSTEM
# 02_GRID_SYSTEM.md
# ============================================================================
#
# Version : 1.0.0
# Status  : Foundation (Freeze Candidate)
# Owner   : Product Architecture
#
# This document defines the ONLY accepted Grid System
# for Commercial UI V3.
#
# ============================================================================

# 1. PURPOSE

The Grid System establishes the spatial structure of the
Commercial UI V3.

It guarantees:

• Consistent layouts

• Predictable alignment

• Reading comfort

• Responsive scalability

The Grid is invisible.

Users should never notice it.

They should only experience visual harmony.

------------------------------------------------------------------------------

# 2. DESIGN PHILOSOPHY

Commercial UI V3 uses

Reading-first Grid.

The grid exists to improve reading.

NOT

to maximize information density.

NOT

to display more widgets.

NOT

to imitate dashboards.

Whitespace is part of the Grid.

Margins are part of the Grid.

Alignment is part of the Grid.

------------------------------------------------------------------------------

# 3. GRID HIERARCHY

Grid consists of four layers.

Application Frame

↓

Report Sheet

↓

Content Grid

↓

Reading Column

Only the Reading Column
contains long-form text.

------------------------------------------------------------------------------

# 4. APPLICATION FRAME

Purpose

Application shell.

Contains

Navigation

Rail

Top bar

Footer

The Application Frame
must never compete
with the Report Sheet.

------------------------------------------------------------------------------

# 5. REPORT SHEET

The Report Sheet
is the primary visual object.

Everything users read
belongs to the Report Sheet.

Only ONE Report Sheet
exists per page.

Never split reports
into multiple independent containers.

------------------------------------------------------------------------------

# 6. CONTENT GRID

Desktop

12 Columns

Laptop

12 Columns

Tablet

8 Columns

Mobile

4 Columns

The grid supports layout.

The reader experiences content.

------------------------------------------------------------------------------

# 7. READING COLUMN

Reading width
is independent
from page width.

Long-form text
must never span
the entire monitor.

Optimal reading width

≈ 70–80 characters per line.

This rule has higher priority
than maximizing content width.

------------------------------------------------------------------------------

# 8. DESKTOP GRID

Viewport

≥ 1440 px

Content Grid

12 Columns

Outer Margin

48 px

Column Gap

24 px

Maximum Report Width

1360 px

Preferred Reading Width

760 px

Wide analytical sections

may expand

up to 1080 px.

------------------------------------------------------------------------------

# 9. LAPTOP GRID

Viewport

1280–1439 px

12 Columns

Outer Margin

32 px

Column Gap

20 px

Reading Width

680–720 px

Preserve
reading rhythm.

------------------------------------------------------------------------------

# 10. TABLET GRID

Viewport

768–1279 px

8 Columns

Outer Margin

24 px

Column Gap

16 px

Reading Width

100%

Side rail
becomes collapsible.

------------------------------------------------------------------------------

# 11. MOBILE GRID

Viewport

≤ 767 px

4 Columns

Outer Margin

16 px

Column Gap

12 px

Everything stacks vertically.

Reading order
must never change.

------------------------------------------------------------------------------

# 12. SECTION WIDTH RULES

Executive Summary

Medium Width

--------------------------------------------------

Four Pillars

Wide Width

--------------------------------------------------

Executive Insight

Reading Width

--------------------------------------------------

Explainable Analysis

Reading Width

--------------------------------------------------

Charts

Wide Width

--------------------------------------------------

Consultation Report

Reading Width

--------------------------------------------------

Appendix

Reading Width

Not every section
shares the same width.

------------------------------------------------------------------------------

# 13. HORIZONTAL ALIGNMENT

Every major chapter
shares the same alignment axis.

Titles

Body

Dividers

Callouts

must align consistently.

Avoid visual drift.

------------------------------------------------------------------------------

# 14. VERTICAL RHYTHM

Page Top

↓

Hero

120 px

↓

Section

96 px

↓

Block

48 px

↓

Paragraph

24 px

↓

Inline

8–16 px

Spacing
creates rhythm.

Grid
supports rhythm.

------------------------------------------------------------------------------

# 15. RESPONSIVE PRINCIPLES

Responsive design
does NOT mean

reordering content.

Responsive design
means

adapting width.

Reading sequence
never changes.

------------------------------------------------------------------------------

# 16. MULTI-COLUMN RULES

Commercial UI V3
uses multiple columns
only when comparison
improves understanding.

Examples

Four Pillars

Metrics

Comparison Tables

Everything else
returns to
single-column reading.

------------------------------------------------------------------------------

# 17. FORBIDDEN LAYOUTS

Do NOT create

Dashboard tiles.

Pinterest layouts.

Masonry grids.

Floating panels.

Independent scrolling regions.

Multiple reports
on one page.

------------------------------------------------------------------------------

# 18. GRID TOKENS

All Grid values
must reference
Design Tokens.

Examples

grid.desktop.columns

grid.desktop.margin

grid.desktop.gutter

grid.report.maxWidth

grid.reading.maxWidth

Raw values
must never appear
inside components.

------------------------------------------------------------------------------

# 19. IMPLEMENTATION RULES

Frontend SHALL NOT

Invent breakpoints.

Invent margins.

Invent gutters.

Invent widths.

Everything
must reference
Grid Tokens.

------------------------------------------------------------------------------

# 20. ACCEPTANCE CRITERIA

Grid System passes only when

✓ Layout feels balanced.

✓ Reading remains comfortable.

✓ Long paragraphs
never become too wide.

✓ Every section
aligns consistently.

✓ Responsive behavior
preserves reading flow.

✓ The report feels like
one continuous document.

------------------------------------------------------------------------------

# 21. FREEZE

After approval,

this Grid System
becomes immutable.

Future layouts
must consume
Grid Tokens only.

No component
may redefine
the Grid.

# ============================================================================
# END OF DOCUMENT
# ============================================================================