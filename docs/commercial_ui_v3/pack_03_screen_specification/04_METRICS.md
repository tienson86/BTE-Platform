# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 03 — SCREEN SPECIFICATION
# 04_METRICS.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Owner : Product Architecture

Related Documents

- Pack 01 Product Vision
- Pack 02 Design System
- 00_SCREEN_SPEC_STANDARD.md

==============================================================================
1. BUSINESS GOAL
==============================================================================

Metrics provides

visual confirmation

for the analytical conclusions.

It is not a dashboard.

It is not a statistics page.

It helps users understand

the overall balance

of the BaZi chart

through a small number
of meaningful indicators.

Charts support understanding.

They never replace explanation.

==============================================================================

2. USER GOAL
==============================================================================

Users want to know

• Is my chart balanced?

• Is my Day Master strong or weak?

• Which Five Elements dominate?

• Which Ten Gods stand out?

Users should not need

to interpret raw charts.

==============================================================================

3. READING GOAL
==============================================================================

After reading this section

users should understand

✓ Overall Balance

✓ Day Master Strength

✓ Five Elements Distribution

✓ Ten Gods Distribution

without reading
detailed analysis.

==============================================================================

4. SUCCESS CRITERIA
==============================================================================

Metrics succeeds only when

users correctly explain

the overall condition

of their chart

within

30–60 seconds.

==============================================================================

5. USER QUESTIONS ANSWERED
==============================================================================

Q1

Is my chart balanced?

↓

Overall Balance

--------------------------------------------------

Q2

How strong is my Day Master?

↓

Strength Gauge

--------------------------------------------------

Q3

Which element dominates?

↓

Five Elements

--------------------------------------------------

Q4

Which Ten Gods dominate?

↓

Ten Gods Distribution

==============================================================================

6. INFORMATION PRIORITY
==============================================================================

Priority 0

Insight Summary

--------------------------------------------------

Priority 1

Strength Gauge

--------------------------------------------------

Priority 2

Five Elements

--------------------------------------------------

Priority 3

Ten Gods

--------------------------------------------------

Priority 4

Supporting Metrics

Charts never become

Priority 0.

==============================================================================

7. EXPECTED READING TIME
==============================================================================

30–60 seconds

The section supports

quick understanding,

not detailed research.

==============================================================================

8. ASCII LAYOUT
==============================================================================

+------------------------------------------------------------------+

VISUAL ANALYTICS

--------------------------------------------------------------------

Insight Summary

--------------------------------------------------------------------

Strength Gauge

--------------------------------------------------------------------

Five Elements Distribution

--------------------------------------------------------------------

Ten Gods Distribution

--------------------------------------------------------------------

Supporting Metrics

+------------------------------------------------------------------+

==============================================================================

9. COMPONENT TREE
==============================================================================

MetricsWorkspace

├── InsightSummary

├── StrengthGauge

├── ElementDistribution

├── TenGodDistribution

└── SupportingMetrics

==============================================================================

10. GRID MAPPING
==============================================================================

Desktop

Single Reading Column

Charts centered.

Tablet

Single Reading Column

Charts scale down.

Mobile

Single Reading Column

Charts stacked vertically.

==============================================================================

11. SPACING MAPPING
==============================================================================

Uses only

Spacing Tokens

space.chapter

↓

space.section

↓

space.block

==============================================================================

12. TYPOGRAPHY ROLES
==============================================================================

Insight

↓

Chart Title

↓

Chart Description

↓

Supporting Text

↓

Metadata

==============================================================================

13. COLOR INTENT
==============================================================================

Semantic Tokens only.

Never encode meaning

using color alone.

Every chart

must have text support.

==============================================================================

14. SURFACE ROLE
==============================================================================

One Reading Surface.

Charts belong

inside

the report.

They are not

independent widgets.

==============================================================================

15. MOTION INTENT
==============================================================================

Guide

↓

Reveal

↓

Focus

Charts never animate

for decoration.

==============================================================================

16. INTERACTION RULES
==============================================================================

Hover

Optional tooltip.

Keyboard

Accessible.

Touch

Accessible.

No interaction

required

to understand charts.

==============================================================================

17. BINDING CONTRACT
==============================================================================

Consumes only

report.metrics

analysis.strength

analysis.elements

analysis.ten_gods

Presentation only.

No calculations.

No derived metrics.

==============================================================================

18. DATA DEPENDENCIES
==============================================================================

Required

Strength

Five Elements

Ten Gods

Optional

Supporting Metrics

Confidence

==============================================================================

19. LOADING STATE
==============================================================================

Display

Chart Skeletons

Maintain

layout stability.

==============================================================================

20. EMPTY STATE
==============================================================================

Display

"No metrics available."

Provide

Retry

or

Return to Analysis.

==============================================================================

21. UNAVAILABLE STATE
==============================================================================

Unavailable metrics

display

Unavailable

Never display

null

undefined

or fabricated charts.

==============================================================================

22. ERROR STATE
==============================================================================

Display

Friendly explanation.

Retry action.

Diagnostic identifier.

==============================================================================

23. RESPONSIVE BEHAVIOUR
==============================================================================

Desktop

Charts centered.

Tablet

Charts scaled.

Mobile

Charts stacked vertically.

Reading hierarchy

never changes.

==============================================================================

24. ACCESSIBILITY
==============================================================================

Every chart

must provide

Text Alternative

ARIA Labels

Keyboard Access

High Contrast

Screen Reader Support

Reduced Motion

==============================================================================

25. PERFORMANCE BUDGET
==============================================================================

Render

<100 ms

SVG only.

No external chart library.

No layout shift.

==============================================================================

26. COGNITIVE OUTCOME
==============================================================================

After reading

users should know

• Whether the chart is balanced.

• Whether the Day Master is strong or weak.

• Which elements dominate.

• Which Ten Gods dominate.

Users should never need

to interpret

the chart by themselves.

==============================================================================

27. ANTI-PATTERNS
==============================================================================

Commercial UI V3 must never

✗ Display charts before insight.

✗ Show more than four primary charts.

✗ Create dashboard layouts.

✗ Use decorative charts.

✗ Require users to decode colors.

✗ Replace explanations with graphics.

Charts support understanding.

They never become

the primary content.

==============================================================================

28. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Insight appears before charts.

✓ Charts reinforce conclusions.

✓ Users understand balance quickly.

✓ Charts remain secondary.

✓ Reading completes

within one minute.

FAIL

✗ Dashboard appearance.

✗ Too many charts.

✗ Charts dominate text.

✗ Users must interpret charts manually.

==============================================================================

29. FUTURE EXTENSIONS
==============================================================================

May support

Trend Comparison

Luck Cycle Overlay

Historical Metrics

Interactive Filtering

without changing

Business Goal

Reading Goal

Binding Contract

or Information Priority.

==============================================================================

30. IMPLEMENTATION NOTES
==============================================================================

This specification defines

Reading Experience

Visual Hierarchy

Binding

States

Acceptance

It does NOT define

HTML

CSS

React

Vue

Chart implementation.

==============================================================================

31. FREEZE
==============================================================================

After approval

Metrics becomes

the canonical

Visual Analytics layer

of Commercial UI V3.

All implementations

must preserve

Business Goal

Reading Goal

Information Priority

Insight-first hierarchy

and Binding Contract.

# ============================================================================
# END OF DOCUMENT
# ============================================================================