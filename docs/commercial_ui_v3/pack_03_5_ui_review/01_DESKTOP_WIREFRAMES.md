# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 03.5 — UI REVIEW & WIREFRAMES
# 01_DESKTOP_WIREFRAMES.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Owner : Product Architecture

------------------------------------------------------------------------------

# 1. PURPOSE

This document defines the canonical Desktop Reading Blueprint
for Commercial UI V3.

It is not an implementation guide.

It is the visual contract that describes exactly
how users experience the report from top to bottom.

All desktop implementations must conform
to this blueprint.

------------------------------------------------------------------------------

# 2. DESIGN OBJECTIVE

The Desktop experience must feel like

a premium professional consultation report.

Not

a dashboard.

Not

an admin system.

Not

a collection of widgets.

The report is a continuous reading experience.

------------------------------------------------------------------------------

# 3. VIEWPORT

Target Resolution

1440 × 900

Reference Resolution

1920 × 1080

Minimum Supported

1280 × 720

The report must remain centered
and readable on all supported desktop sizes.

------------------------------------------------------------------------------

# 4. PAGE STRUCTURE

Desktop page consists of

Application Shell

↓

Left Reading Rail

↓

Report Sheet

↓

Appendix

↓

Footer

Only the Report Sheet
is considered primary content.

------------------------------------------------------------------------------

# 5. HIGH LEVEL WIREFRAME

┌────────────────────────────────────────────────────────────────────────────┐
│                          Top Navigation Bar                               │
├──────────────┬─────────────────────────────────────────────────────────────┤
│              │                                                             │
│ Reading Rail │                     Report Sheet                            │
│              │                                                             │
│ • Hero       │  ┌──────────────────────────────────────────────────────┐   │
│ • Pillars    │  │ Executive Hero                                      │   │
│ • Insight    │  └──────────────────────────────────────────────────────┘   │
│ • Analysis   │                                                             │
│ • Report     │  ┌──────────────────────────────────────────────────────┐   │
│ • Knowledge  │  │ Four Pillars Workspace                              │   │
│              │  └──────────────────────────────────────────────────────┘   │
│              │                                                             │
│              │  ┌──────────────────────────────────────────────────────┐   │
│              │  │ Executive Insight                                   │   │
│              │  └──────────────────────────────────────────────────────┘   │
│              │                                                             │
│              │  ┌──────────────────────────────────────────────────────┐   │
│              │  │ Visual Analytics                                    │   │
│              │  └──────────────────────────────────────────────────────┘   │
│              │                                                             │
│              │  ┌──────────────────────────────────────────────────────┐   │
│              │  │ Explainable Analysis                                │   │
│              │  └──────────────────────────────────────────────────────┘   │
│              │                                                             │
│              │  ┌──────────────────────────────────────────────────────┐   │
│              │  │ Consultation Report                                 │   │
│              │  └──────────────────────────────────────────────────────┘   │
│              │                                                             │
│              │  ┌──────────────────────────────────────────────────────┐   │
│              │  │ Knowledge Workspace                                 │   │
│              │  └──────────────────────────────────────────────────────┘   │
│              │                                                             │
├──────────────┴─────────────────────────────────────────────────────────────┤
│                              Footer                                       │
└────────────────────────────────────────────────────────────────────────────┘

------------------------------------------------------------------------------

# 6. READING ORDER

The desktop reading order is fixed.

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

The order must never change.

------------------------------------------------------------------------------

# 7. REPORT SHEET

The report is rendered as one continuous sheet.

Rules

• One visual document

• Continuous scrolling

• No nested page containers

• No competing surfaces

• No dashboard layout

The user should feel
they are reading one document.

------------------------------------------------------------------------------

# 8. READING RAIL

The left rail provides orientation only.

Contains

• Chapter list

• Reading progress

• Active section indicator

• Jump navigation

The rail never competes
with report content.

------------------------------------------------------------------------------

# 9. EXECUTIVE HERO

Viewport Goal

Within 5 seconds the user understands

• Who am I?

• Overall chart quality

• Primary recommendation

The Hero should occupy
approximately one viewport height
without unnecessary scrolling.

------------------------------------------------------------------------------

# 10. FOUR PILLARS

Presented as

four independent pillars.

Day Pillar
is visually emphasized.

No table layout.

Metadata remains secondary.

------------------------------------------------------------------------------

# 11. EXECUTIVE INSIGHT

This section answers

"What should I remember?"

Contains

• Strengths

• Weaknesses

• Opportunities

• Risks

• Key Recommendation

Insight is textual first.

------------------------------------------------------------------------------

# 12. VISUAL ANALYTICS

Charts support
the written insight.

Charts never become
the primary focus.

Preferred order

Metrics

↓

Gauge

↓

Five Elements

↓

Ten Gods

------------------------------------------------------------------------------

# 13. EXPLAINABLE ANALYSIS

Every analysis block follows

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

No essay-style dump.

------------------------------------------------------------------------------

# 14. CONSULTATION REPORT

Rendered as a document.

Contains

Table of Contents

↓

Executive Summary

↓

Chapters

↓

References

↓

Appendix

It should resemble
a printed consulting report.

------------------------------------------------------------------------------

# 15. KNOWLEDGE WORKSPACE

Knowledge appears
after the consultation report.

Structure

Insight

↓

Evidence

↓

Rule

↓

Classical Sources

↓

Confidence

↓

Related Topics

Knowledge validates
the report.

------------------------------------------------------------------------------

# 16. SCROLLING

Desktop uses

one continuous scroll.

Nested scrolling
is forbidden.

Each chapter begins
with generous whitespace.

------------------------------------------------------------------------------

# 17. VISUAL HIERARCHY

Hierarchy is established by

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

Shadow has the lowest priority.

------------------------------------------------------------------------------

# 18. REVIEW CHECKLIST

The desktop layout passes review only if

✓ Reads as one report

✓ No dashboard appearance

✓ One continuous paper

✓ Reading Rail remains secondary

✓ Hero answers key questions

✓ Sections follow reading order

✓ Charts support text

✓ Analysis explains decisions

✓ Knowledge validates conclusions

✓ Reading remains calm

------------------------------------------------------------------------------

# 19. IMPLEMENTATION NOTES

This document defines

layout,

sequence,

and reading flow.

It does not define

React,

CSS,

HTML,

or implementation details.

------------------------------------------------------------------------------

# 20. FREEZE

After approval,

this Desktop Reading Blueprint
becomes the canonical reference
for all desktop implementations.

No implementation may alter

reading order,

layout hierarchy,

or report structure
without updating this specification first.

# ============================================================================
# END OF DOCUMENT
# ============================================================================