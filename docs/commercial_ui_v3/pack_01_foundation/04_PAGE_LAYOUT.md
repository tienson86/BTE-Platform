# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# 04_PAGE_LAYOUT.md
# ============================================================================
#
# Version : 1.0.0
# Status  : FOUNDATION (Freeze Candidate)
# Owner   : Product Architecture
#
# This document defines the ONLY accepted page layout
# for the BaZi Consultation Report.
#
# It specifies:
#
# • Overall page composition
# • Reading width
# • Grid system
# • Section ordering
# • Section spacing
# • Visual rhythm
# • Responsive layout
#
# No implementation may modify this layout.
#
# ============================================================================

# 1. PURPOSE

This document defines the physical structure
of every BaZi consultation report.

It answers:

Where is information placed?

NOT

How information is calculated.

NOT

How components are implemented.

------------------------------------------------------------------------------

# 2. LAYOUT PHILOSOPHY

Commercial UI V3 uses

ONE CONTINUOUS REPORT.

Never:

Dashboard

↓

Dashboard

↓

Dashboard

↓

Dashboard

The report is one document.

Scrolling equals reading.

------------------------------------------------------------------------------

# 3. GLOBAL STRUCTURE

Desktop

┌─────────────────────────────────────────────────────────────────────────┐

                    Top Navigation

───────────────────────────────────────────────────────────────────────────

┌──────┐ ┌──────────────────────────────────────────────────────────────┐

 Rail   │                                                        │

        │                REPORT SHEET                           │

        │                                                      │

        │ Hero                                                 │

        │                                                      │

        │ Four Pillars                                         │

        │                                                      │

        │ Executive Insight                                    │

        │                                                      │

        │ Explainable Analysis                                 │

        │                                                      │

        │ Consultation Report                                  │

        │                                                      │

        │ Appendix                                             │

        │                                                      │

└──────┘ └──────────────────────────────────────────────────────┘

└─────────────────────────────────────────────────────────────────────────┘

Only ONE report sheet exists.

------------------------------------------------------------------------------

# 4. PAGE COMPOSITION

Background

↓

Application Frame

↓

Report Sheet

↓

Sections

↓

Content

Never create visual competition
between these layers.

------------------------------------------------------------------------------

# 5. REPORT SHEET

The report sheet is the primary object.

Everything belongs inside it.

No floating dashboards.

No independent panels.

No competing containers.

The report behaves like

one premium document.

------------------------------------------------------------------------------

# 6. PAGE WIDTH

Desktop

Maximum content width

1360 px

Reading width

760 px

Wide content

up to 1080 px

Charts

may temporarily expand.

Text

must remain readable.

------------------------------------------------------------------------------

# 7. GRID SYSTEM

Desktop

12 Columns

Outer Margin

48 px

Column Gap

24 px

Reading Column

center aligned.

Never left-heavy.

------------------------------------------------------------------------------

# 8. PAGE RHYTHM

Major Sections

120 px

Subsections

64 px

Component Groups

40 px

Paragraph Groups

24 px

Paragraphs

16 px

Captions

8 px

Whitespace is intentional.

Never compress.

------------------------------------------------------------------------------

# 9. SECTION ORDER

The order is fixed.

1

Executive Summary

↓

2

BaZi Chart

↓

3

Executive Insight

↓

4

Explainable Analysis

↓

5

Consultation Report

↓

6

Appendix

Nothing may interrupt
this sequence.

------------------------------------------------------------------------------

# 10. EXECUTIVE SUMMARY

Viewport Target

100%

The entire Hero
must be visible
without scrolling
on standard desktop screens.

Contains:

Identity

↓

Overall Verdict

↓

First Recommendation

↓

Key Metrics

Maximum reading time

5 seconds.

------------------------------------------------------------------------------

# 11. FOUR PILLARS

Immediately follows Hero.

Acts as

the visual identity
of the report.

Centered.

Balanced.

No excessive metadata.

Secondary information

collapsed by default.

------------------------------------------------------------------------------

# 12. EXECUTIVE INSIGHT

Position

Immediately below
the Four Pillars.

Purpose

Summarize

Strengths

Weaknesses

Opportunities

Risks

Recommendations

Maximum

one screen.

------------------------------------------------------------------------------

# 13. EXPLAINABLE ANALYSIS

Longest structured section.

Every analysis block follows:

Title

↓

Conclusion

↓

Explanation

↓

Evidence

↓

Rule

↓

Confidence

↓

Reference

Blocks stack vertically.

Never create masonry layouts.

------------------------------------------------------------------------------

# 14. CONSULTATION REPORT

Single-column reading.

Book-like measure.

No dashboard cards.

No split reading.

Long-form paragraphs.

Comfortable typography.

------------------------------------------------------------------------------

# 15. APPENDIX

Lowest visual priority.

Functions as

supporting material.

Readers may skip it.

No primary conclusions
may exist only here.

------------------------------------------------------------------------------

# 16. RAIL NAVIGATION

Purpose

Orientation.

NOT

Navigation dominance.

Width

72 px

Icons always visible.

Labels appear
on hover
or expanded mode.

Must never compete
with report content.

------------------------------------------------------------------------------

# 17. SECTION TRANSITIONS

Transitions rely on:

Whitespace

↓

Typography

↓

Hairline Divider

Never use:

Heavy borders.

Colored separators.

Large cards.

Artificial containers.

------------------------------------------------------------------------------

# 18. VISUAL BALANCE

Every viewport
must have

one visual anchor.

Everything else
supports it.

Avoid

multiple focal points.

------------------------------------------------------------------------------

# 19. RESPONSIVE BEHAVIOR

Desktop

12-column grid.

Laptop

12-column grid
with reduced margins.

Tablet

8-column grid.

Mobile

Single-column reading.

Reading sequence

must remain identical.

------------------------------------------------------------------------------

# 20. SCROLL EXPERIENCE

Scrolling should feel like:

Reading chapters
of one report.

Not

jumping
between applications.

Each section

introduces one new concept.

------------------------------------------------------------------------------

# 21. IMPLEMENTATION RULES

Frontend implementation

shall NOT

change:

Section order.

Reading width.

Page rhythm.

Report sheet concept.

Visual hierarchy.

Only styling tokens
may vary.

------------------------------------------------------------------------------

# 22. ACCEPTANCE

Page Layout passes only when:

✓ Users perceive one report.

✓ No dashboard feeling remains.

✓ Reading rhythm is smooth.

✓ Whitespace guides attention.

✓ Navigation remains secondary.

✓ Every section feels connected.

------------------------------------------------------------------------------

# 23. FREEZE

After approval,

Page Layout

becomes immutable.

Any future redesign

must preserve

the layout architecture
defined here.

# ============================================================================
# END OF DOCUMENT
# ============================================================================