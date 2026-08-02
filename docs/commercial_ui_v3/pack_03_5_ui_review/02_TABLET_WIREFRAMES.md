# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 03.5 — UI REVIEW & WIREFRAMES
# 02_TABLET_WIREFRAMES.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Owner : Product Architecture

------------------------------------------------------------------------------

# 1. PURPOSE

This document defines the canonical Tablet Reading Blueprint
for Commercial UI V3.

Tablet is not a scaled Desktop.

Tablet is an independent reading experience.

The objective is to preserve the Reading Journey
while adapting to a narrower viewport
and touch interaction.

------------------------------------------------------------------------------

# 2. DESIGN OBJECTIVE

Tablet should feel like

reading a professional consultation report
on a high-quality notebook.

The report remains continuous.

Navigation becomes lighter.

Touch interaction becomes primary.

------------------------------------------------------------------------------

# 3. TARGET DEVICES

Reference Width

768–1279 px

Examples

• iPad Mini
• iPad Air
• iPad Pro (portrait)
• Android Tablets

Landscape and portrait
must both be supported.

------------------------------------------------------------------------------

# 4. PAGE STRUCTURE

Tablet page consists of

Top Navigation

↓

Collapsible Reading Rail

↓

Report Sheet

↓

Footer

The Report Sheet
remains the primary reading surface.

------------------------------------------------------------------------------

# 5. HIGH LEVEL WIREFRAME

┌──────────────────────────────────────────────────────┐
│                  Top Navigation                       │
├──────────────────────────────────────────────────────┤
│ ☰ Reading Outline                                    │
├──────────────────────────────────────────────────────┤
│                                                      │
│              Executive Hero                          │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│           Four Pillars Workspace                     │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│            Executive Insight                         │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│            Visual Analytics                          │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│          Explainable Analysis                        │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│         Consultation Report                          │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│         Knowledge Workspace                          │
│                                                      │
└──────────────────────────────────────────────────────┘

------------------------------------------------------------------------------

# 6. READING ORDER

The reading sequence is identical to Desktop.

1. Executive Hero

↓

2. Four Pillars

↓

3. Executive Insight

↓

4. Visual Analytics

↓

5. Explainable Analysis

↓

6. Consultation Report

↓

7. Knowledge Workspace

No section reordering is allowed.

------------------------------------------------------------------------------

# 7. READING RAIL

The Reading Rail
is hidden by default.

Users open it through

Outline Button (☰).

The rail overlays the report
without changing reading order.

It closes automatically
after navigation.

------------------------------------------------------------------------------

# 8. EXECUTIVE HERO

The Hero occupies
approximately one viewport.

Layout adapts to a single reading column.

Recommendation remains above metrics.

Metrics wrap gracefully
when width decreases.

------------------------------------------------------------------------------

# 9. FOUR PILLARS

The four pillars remain visible
as independent columns
when space allows.

If width is insufficient

2 × 2 layout is permitted.

Day Pillar
must remain visually dominant.

------------------------------------------------------------------------------

# 10. EXECUTIVE INSIGHT

Insight cards are removed.

Insights appear
as continuous reading sections.

Recommendations
remain visually highlighted.

------------------------------------------------------------------------------

# 11. VISUAL ANALYTICS

Charts shrink proportionally.

Text explanations
always precede charts.

Charts never require
horizontal scrolling.

------------------------------------------------------------------------------

# 12. EXPLAINABLE ANALYSIS

Analysis blocks stack vertically.

Expand / Collapse
uses touch-friendly controls.

Evidence and Rules
remain immediately below explanations.

------------------------------------------------------------------------------

# 13. CONSULTATION REPORT

Rendered as one continuous document.

Table of Contents
is collapsible.

Reading Progress
remains visible
at the top of the viewport.

------------------------------------------------------------------------------

# 14. KNOWLEDGE WORKSPACE

Knowledge appears
after the consultation report.

Each Knowledge Block
uses full width.

Evidence
and citations
remain readable
without zooming.

------------------------------------------------------------------------------

# 15. TOUCH INTERACTION

Primary interaction

Touch.

Rules

• Minimum comfortable touch targets.

• No hover dependency.

• Expand/collapse via tap.

• Swipe gestures are optional,
  never mandatory.

------------------------------------------------------------------------------

# 16. SCROLLING

Single vertical scroll only.

Horizontal scrolling
inside the report
is forbidden.

------------------------------------------------------------------------------

# 17. RESPONSIVE RULES

Desktop

↓

Tablet

Changes

• Reading Rail collapses.

• Margins reduce.

• Multi-column layouts may wrap.

• Reading width expands to fit.

Reading hierarchy
must remain unchanged.

------------------------------------------------------------------------------

# 18. VISUAL HIERARCHY

Hierarchy continues to rely on

Typography

↓

Whitespace

↓

Alignment

↓

Surface

↓

Color

↓

Border

↓

Shadow

Tablet introduces
no new visual hierarchy.

------------------------------------------------------------------------------

# 19. REVIEW CHECKLIST

Tablet layout passes review only if

✓ Reading order matches Desktop.

✓ No dashboard appearance.

✓ Reading Rail is collapsible.

✓ Touch interaction is natural.

✓ Four Pillars remain understandable.

✓ Charts remain secondary.

✓ Report feels continuous.

✓ No horizontal scrolling.

✓ Reading comfort is preserved.

------------------------------------------------------------------------------

# 20. IMPLEMENTATION NOTES

This specification defines

reading experience,

layout adaptation,

and touch behaviour.

It does not define

HTML,

CSS,

JavaScript,

or framework-specific implementation.

------------------------------------------------------------------------------

# 21. FREEZE

After approval,

this Tablet Reading Blueprint
becomes the canonical reference
for all tablet implementations.

Any deviation
requires updating
this specification first.

# ============================================================================
# END OF DOCUMENT
# ============================================================================