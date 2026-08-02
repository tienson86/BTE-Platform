# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 03.5 — UI REVIEW & WIREFRAMES
# 03_MOBILE_WIREFRAMES.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Owner : Product Architecture

------------------------------------------------------------------------------

# 1. PURPOSE

This document defines the canonical Mobile Reading Blueprint
for Commercial UI V3.

Mobile is not a miniature Desktop.

Mobile is a focused consultation companion.

The objective is

Quick Understanding

↓

Comfortable Reading

↓

Immediate Recommendation

rather than deep analysis.

------------------------------------------------------------------------------

# 2. DESIGN OBJECTIVE

Mobile should answer
the user's most important questions
within one hand and one thumb.

The experience must feel

Fast

↓

Simple

↓

Comfortable

↓

Trustworthy

↓

Continuous

Users should never feel
they are using
a complicated analytical system.

------------------------------------------------------------------------------

# 3. TARGET DEVICES

Reference Width

360–480 px

Examples

• Android Phones

• iPhone SE

• iPhone 15

• Pixel Series

Portrait orientation
is the primary design target.

Landscape is supported
but not optimized.

------------------------------------------------------------------------------

# 4. PAGE STRUCTURE

Mobile page consists of

Top Navigation

↓

Reading Progress

↓

Continuous Report

↓

Bottom Safe Area

The report occupies
the full width
of the screen.

------------------------------------------------------------------------------

# 5. HIGH LEVEL WIREFRAME

┌──────────────────────────────┐
│        Top Navigation         │
├──────────────────────────────┤
│ Reading Progress             │
├──────────────────────────────┤
│                              │
│ Executive Hero               │
│                              │
├──────────────────────────────┤
│ Four Pillars                │
├──────────────────────────────┤
│ Executive Insight           │
├──────────────────────────────┤
│ Visual Analytics            │
├──────────────────────────────┤
│ Explainable Analysis        │
├──────────────────────────────┤
│ Consultation Report         │
├──────────────────────────────┤
│ Knowledge Workspace         │
├──────────────────────────────┤
│ Footer                      │
└──────────────────────────────┘

Only one
continuous scroll.

------------------------------------------------------------------------------

# 6. READING ORDER

Reading order
must remain identical
to Desktop and Tablet.

1.

Executive Hero

↓

2.

Four Pillars

↓

3.

Executive Insight

↓

4.

Visual Analytics

↓

5.

Explainable Analysis

↓

6.

Consultation Report

↓

7.

Knowledge Workspace

Never reorder sections.

------------------------------------------------------------------------------

# 7. NAVIGATION

Desktop Reading Rail

does not exist
on Mobile.

Navigation becomes

Outline Drawer

opened manually.

Users always return
to the same reading position.

------------------------------------------------------------------------------

# 8. EXECUTIVE HERO

Hero occupies
approximately
the first viewport.

Within five seconds
users understand

• Day Master

• Overall Verdict

• First Recommendation

Metrics
stack vertically.

Recommendation
always appears
above metrics.

------------------------------------------------------------------------------

# 9. FOUR PILLARS

The Four Pillars
are displayed
as four stacked cards.

Each pillar follows
the same structure.

Stem

↓

Branch

↓

Hidden Stems

↓

Ten Gods

↓

Life Stage

Day Pillar
remains highlighted.

------------------------------------------------------------------------------

# 10. EXECUTIVE INSIGHT

Rendered
as a reading section.

Order

Strengths

↓

Weaknesses

↓

Opportunities

↓

Risks

↓

Recommendation

No multi-column layout.

------------------------------------------------------------------------------

# 11. VISUAL ANALYTICS

Charts become supporting content.

Order

Insight

↓

Chart

↓

Explanation

Charts must fit
the viewport width.

No horizontal scrolling.

------------------------------------------------------------------------------

# 12. EXPLAINABLE ANALYSIS

Analysis Blocks
stack vertically.

Structure

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

Knowledge

Expand/Collapse
is touch optimized.

------------------------------------------------------------------------------

# 13. CONSULTATION REPORT

Rendered
as one document.

Table of Contents
becomes collapsible.

Reading Progress
stays visible
at the top.

Long paragraphs
maintain comfortable width.

------------------------------------------------------------------------------

# 14. KNOWLEDGE WORKSPACE

Knowledge appears
after the report.

Each Knowledge Block
uses the full width.

References

collapse by default.

Users may expand
for details.

------------------------------------------------------------------------------

# 15. TOUCH INTERACTION

Primary interaction

Tap.

Secondary interaction

Long Press (optional).

Hover
must never be required.

Touch targets
must remain comfortable.

------------------------------------------------------------------------------

# 16. SCROLLING

Only one
vertical scroll.

Nested scrolling
is forbidden.

Horizontal scrolling
inside report
is forbidden.

------------------------------------------------------------------------------

# 17. RESPONSIVE ADAPTATION

Desktop

↓

Tablet

↓

Mobile

Only presentation changes.

Business logic

never changes.

Reading order

never changes.

Information priority

never changes.

------------------------------------------------------------------------------

# 18. PERFORMANCE TARGET

Mobile prioritizes

Fast First Paint

↓

Fast Scroll

↓

Smooth Expand

↓

Stable Layout

Heavy sections
may lazy-load.

Content shifting
is forbidden.

------------------------------------------------------------------------------

# 19. ACCESSIBILITY

Support

Screen Readers

↓

Large Text

↓

High Contrast

↓

Reduced Motion

↓

Keyboard Navigation
(external keyboards)

Touch interaction
must remain accessible.

------------------------------------------------------------------------------

# 20. REVIEW CHECKLIST

Mobile layout passes only when

✓ One-hand reading is comfortable.

✓ Hero answers
the three key questions.

✓ Reading order
matches Desktop.

✓ No dashboard appearance.

✓ No horizontal scrolling.

✓ Charts remain secondary.

✓ Knowledge remains readable.

✓ Report feels continuous.

✓ Reading rhythm
is preserved.

------------------------------------------------------------------------------

# 21. IMPLEMENTATION NOTES

This document specifies

Reading Flow,

Layout,

Touch Behaviour,

Responsive Adaptation.

It does not specify

React,

HTML,

CSS,

JavaScript,

or framework implementation.

------------------------------------------------------------------------------

# 22. FREEZE

After approval,

this Mobile Reading Blueprint
becomes the canonical reference
for all mobile implementations.

All future mobile interfaces
must preserve

Reading Journey,

Information Priority,

and Business Goals

defined in this specification.

No implementation
may reinterpret
the mobile experience.

# ============================================================================
# END OF DOCUMENT
# ============================================================================