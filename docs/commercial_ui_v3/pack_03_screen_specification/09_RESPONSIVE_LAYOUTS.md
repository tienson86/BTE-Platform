# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 03 — SCREEN SPECIFICATION
# 09_RESPONSIVE_LAYOUTS.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Owner : Product Architecture

Related Documents

- Pack 01 Product Vision
- Pack 02 Design System
- 00_SCREEN_SPEC_STANDARD.md
- Pack 03.5 / 04_DEVICE_BEHAVIOR_MATRIX.md
- Pack 03.5 / 05_READING_FLOW_VALIDATION.md

==============================================================================
1. BUSINESS GOAL
==============================================================================

Responsive Layouts ensure

Commercial UI V3

delivers

one consistent reading experience

across

Desktop,

Tablet,

and

Mobile.

Responsive design

is not

about resizing components.

It is about preserving

meaning,

reading flow,

and

information hierarchy.

==============================================================================

2. DESIGN PHILOSOPHY
==============================================================================

One Product

↓

One Reading Journey

↓

Many Presentations

Presentation adapts.

Meaning never changes.

==============================================================================

3. USER GOAL
==============================================================================

Users expect

the same report

regardless

of device.

Changing devices

must never require

learning

a different interface.

==============================================================================

4. READING GOAL
==============================================================================

Users should experience

the same sequence

the same hierarchy

and

the same conclusions

on every device.

==============================================================================

5. RESPONSIVE PRINCIPLES
==============================================================================

Responsive adaptation

may change

Grid

Spacing

Margins

Typography Scale

Navigation Style

Component Density

Surface Width

Responsive adaptation

must never change

Business Goal

Reading Order

Information Priority

Binding Contract

Document Structure

==============================================================================

6. BREAKPOINT STRATEGY
==============================================================================

Desktop

≥ 1280 px

--------------------------------------------------

Tablet

768–1279 px

--------------------------------------------------

Mobile

360–767 px

--------------------------------------------------

Smaller devices

are supported

using the Mobile layout.

==============================================================================

7. PAGE ADAPTATION
==============================================================================

Desktop

Reading Rail

+

Centered Report

--------------------------------------------------

Tablet

Drawer Navigation

+

Centered Report

--------------------------------------------------

Mobile

Drawer Navigation

+

Full Width Report

==============================================================================

8. SECTION ADAPTATION
==============================================================================

Executive Summary

Desktop

Wide Hero

Tablet

Single Column

Mobile

Single Column

--------------------------------------------------

Four Pillars

Desktop

4 Columns

Tablet

4 Columns or 2×2

Mobile

Vertical Stack

--------------------------------------------------

Executive Insight

Single Reading Column

on every device.

--------------------------------------------------

Metrics

Desktop

Charts centered.

Tablet

Charts scaled.

Mobile

Charts stacked vertically.

--------------------------------------------------

Explainable Analysis

Always

Single Reading Column.

--------------------------------------------------

Consultation Report

Always

Document Reading.

--------------------------------------------------

Appendix

Always

Document Reading.

==============================================================================

9. GRID ADAPTATION
==============================================================================

Desktop

12-column grid

--------------------------------------------------

Tablet

8-column grid

--------------------------------------------------

Mobile

4-column grid

Grid changes

must not alter

reading order.

==============================================================================

10. SPACING ADAPTATION
==============================================================================

Desktop

Generous spacing

--------------------------------------------------

Tablet

Moderate spacing

--------------------------------------------------

Mobile

Compact spacing

Reading rhythm

must remain identical.

==============================================================================

11. TYPOGRAPHY ADAPTATION
==============================================================================

Desktop

100%

--------------------------------------------------

Tablet

95%

--------------------------------------------------

Mobile

90%

Typography hierarchy

never changes.

==============================================================================

12. NAVIGATION ADAPTATION
==============================================================================

Desktop

Sticky Reading Rail

--------------------------------------------------

Tablet

Drawer

--------------------------------------------------

Mobile

Drawer

Navigation hierarchy

never changes.

==============================================================================

13. COMPONENT ADAPTATION
==============================================================================

Components may

Resize

Wrap

Collapse

Expand

Reorder internally

Components must never

change

semantic meaning

or

information priority.

==============================================================================

14. CHART ADAPTATION
==============================================================================

Charts may

Resize

Simplify labels

Reduce padding

Charts must never

hide

primary information.

==============================================================================

15. TABLE ADAPTATION
==============================================================================

Large tables

may become

stacked sections.

Horizontal scrolling

inside

the report

is forbidden.

==============================================================================

16. SCROLL BEHAVIOUR
==============================================================================

Every device

uses

one vertical scroll.

Nested scrolling

is prohibited.

==============================================================================

17. ORIENTATION
==============================================================================

Portrait

Primary

Landscape

Supported

No separate

landscape design

is required.

==============================================================================

18. PERFORMANCE TARGETS
==============================================================================

Desktop

60 FPS

--------------------------------------------------

Tablet

60 FPS

--------------------------------------------------

Mobile

60 FPS

Responsive adaptation

must not introduce

layout instability.

==============================================================================

19. ACCESSIBILITY
==============================================================================

Every layout

must support

Keyboard

(where applicable)

↓

Screen Readers

↓

High Contrast

↓

Reduced Motion

↓

Visible Focus

Accessibility

must never regress

on smaller devices.

==============================================================================

20. RESPONSIVE STATES
==============================================================================

Supported

Loading

↓

Empty

↓

Unavailable

↓

Error

↓

Normal

State behaviour

must remain

identical

across devices.

==============================================================================

21. BINDING CONTRACT
==============================================================================

Responsive Layouts

consume only

viewport information

and

layout tokens.

Responsive logic

must never

modify

business data,

analysis,

or

knowledge payloads.

==============================================================================

22. COGNITIVE OUTCOME
==============================================================================

Users should

switch devices

without

relearning

the report.

Understanding

must remain

consistent.

==============================================================================

23. ANTI-PATTERNS
==============================================================================

Commercial UI V3 must never

✗ Hide chapters
on Mobile.

✗ Reorder report sections.

✗ Replace reading
with dashboards.

✗ Introduce horizontal scrolling.

✗ Remove explanations.

✗ Change Business Logic.

✗ Change Binding.

==============================================================================

24. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Reading Journey
identical across devices.

✓ Reading Order preserved.

✓ Information Priority preserved.

✓ Navigation adapts naturally.

✓ Charts remain secondary.

✓ Reading comfort maintained.

✓ No horizontal scrolling.

FAIL

✗ Different report structures.

✗ Missing sections.

✗ Different business meaning.

✗ Device-specific interpretation.

✗ Dashboard-only mobile layout.

==============================================================================

25. RESPONSIVE QUALITY LEVELS
==============================================================================

Level 1

Layout adapts.

--------------------------------------------------

Level 2

Navigation adapts.

--------------------------------------------------

Level 3

Components adapt.

--------------------------------------------------

Level 4

Performance preserved.

--------------------------------------------------

Level 5

Reading Experience preserved.

Commercial UI V3

targets

Level 5.

==============================================================================

26. IMPLEMENTATION NOTES
==============================================================================

This specification defines

Responsive Behaviour

Layout Adaptation

Reading Preservation

State Behaviour

Acceptance Rules

It does NOT define

CSS Media Queries

Framework APIs

React implementation

Tailwind configuration.

==============================================================================

27. FREEZE
==============================================================================

After approval

Responsive Layouts

become

the canonical

cross-device layout specification

for Commercial UI V3.

Every implementation

must preserve

Business Goal

Reading Journey

Information Priority

Binding Contract

Document Structure

and

Reading Experience

across all supported devices.

# ============================================================================
# END OF DOCUMENT
# ============================================================================