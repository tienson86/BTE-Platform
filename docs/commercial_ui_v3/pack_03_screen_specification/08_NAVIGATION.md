# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 03 — SCREEN SPECIFICATION
# 08_NAVIGATION.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Owner : Product Architecture

Related Documents

- Pack 01 Product Vision
- Pack 02 Design System
- 00_SCREEN_SPEC_STANDARD.md
- 06_CONSULTATION_REPORT.md
- Pack 03.5 / 05_READING_FLOW_VALIDATION.md

==============================================================================
1. BUSINESS GOAL
==============================================================================

Navigation exists

to guide users

through a professional consultation report.

It is not

an application menu.

It is not

feature navigation.

Navigation supports

reading,

orientation,

and

progress.

==============================================================================

2. DESIGN PHILOSOPHY
==============================================================================

Commercial UI V3

contains

one report,

one reading journey,

and

one navigation system.

Users should always know

• Where they are

• What they have read

• What comes next

Navigation must reduce

cognitive load,

not increase it.

==============================================================================

3. USER GOAL
==============================================================================

Users want

• To understand where they are.

• To jump to a section quickly.

• To resume reading.

• To see reading progress.

• To avoid getting lost.

==============================================================================

4. READING GOAL
==============================================================================

Navigation should support

continuous reading.

Readers should never wonder

"What should I read next?"

==============================================================================

5. NAVIGATION MODEL
==============================================================================

Commercial UI V3 uses

Document Navigation.

The report is treated as

one continuous document.

Navigation follows

Reading Order,

not feature hierarchy.

==============================================================================

6. READING ORDER
==============================================================================

Navigation follows

Executive Summary

↓

Four Pillars

↓

Executive Insight

↓

Metrics

↓

Explainable Analysis

↓

Consultation Report

↓

Appendix

This order

must never change.

==============================================================================

7. NAVIGATION COMPONENTS
==============================================================================

Commercial UI V3 includes

Reading Rail

↓

Table of Contents

↓

Reading Progress

↓

Section Anchors

↓

Scroll Spy

↓

Jump Navigation

No additional

navigation systems

are allowed

inside the report.

==============================================================================

8. READING RAIL
==============================================================================

Desktop

Persistent

Sticky

Collapsed only

on small screens.

Tablet

Drawer

Mobile

Drawer

The Reading Rail

shows

current location

and

reading progress.

==============================================================================

9. TABLE OF CONTENTS
==============================================================================

The Table of Contents

is generated

from document headings.

Every major chapter

must appear.

Users may jump

to any chapter.

==============================================================================

10. READING PROGRESS
==============================================================================

Reading Progress

indicates

current position

inside

the report.

It should update

continuously

during scrolling.

Reading Progress

must never

replace

the Reading Rail.

==============================================================================

11. SCROLL SPY
==============================================================================

Scroll Spy

tracks

the active section.

Only one section

may be active

at a time.

The active state

must be

visually distinct

but unobtrusive.

==============================================================================

12. SECTION ANCHORS
==============================================================================

Every major section

must expose

a stable anchor.

Anchors support

• Navigation

• Deep linking

• Accessibility

• Future sharing

Anchor IDs

must remain stable

across releases.

==============================================================================

13. JUMP NAVIGATION
==============================================================================

Users may jump

to any major section.

Jumping

must preserve

reading context.

No modal navigation.

No page reload.

==============================================================================

14. SCROLL BEHAVIOUR
==============================================================================

Navigation uses

smooth scrolling

where supported.

Scrolling must

respect

fixed headers

and

reading offsets.

Horizontal scrolling

is forbidden.

==============================================================================

15. NAVIGATION STATES
==============================================================================

Supported states

Default

↓

Hover

↓

Focus

↓

Active

↓

Disabled

↓

Unavailable

Every state

must use

Design Tokens.

==============================================================================

16. GRID MAPPING
==============================================================================

Desktop

Reading Rail

+

Document

Tablet

Drawer

+

Document

Mobile

Drawer

+

Document

==============================================================================

17. BINDING CONTRACT
==============================================================================

Navigation consumes only

Document Structure

Section IDs

Reading Progress

Scroll Position

Navigation

must never

calculate business data.

==============================================================================

18. DATA DEPENDENCIES
==============================================================================

Required

Document Outline

Section IDs

Optional

Reading Progress

Bookmarks

User Preferences

==============================================================================

19. LOADING STATE
==============================================================================

Display

Navigation Skeleton

until

document structure

is available.

==============================================================================

20. EMPTY STATE
==============================================================================

If no document

exists

display

"No navigation available."

==============================================================================

21. ERROR STATE
==============================================================================

Display

Friendly explanation.

Retry.

Diagnostic identifier.

==============================================================================

22. RESPONSIVE BEHAVIOUR
==============================================================================

Desktop

Sticky Reading Rail.

Tablet

Slide-out Drawer.

Mobile

Slide-out Drawer.

Navigation hierarchy

never changes.

==============================================================================

23. ACCESSIBILITY
==============================================================================

Keyboard navigation.

Skip links.

Semantic landmarks.

ARIA navigation.

Visible focus.

Screen readers.

WCAG AA.

==============================================================================

24. PERFORMANCE BUDGET
==============================================================================

Navigation updates

must remain

under 16 ms

per scroll frame.

No layout shift.

No expensive

scroll handlers.

==============================================================================

25. COGNITIVE OUTCOME
==============================================================================

Users should always know

• Where they are.

• What they finished.

• What remains.

Navigation

should disappear

from conscious attention.

==============================================================================

26. ANTI-PATTERNS
==============================================================================

Commercial UI V3 must never

✗ Use tab navigation
for report sections.

✗ Hide the reading order.

✗ Require nested menus.

✗ Break the report
into unrelated pages.

✗ Interrupt reading
with dialogs.

✗ Use navigation
to expose implementation details.

==============================================================================

27. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Reading order is preserved.

✓ Reading Rail reflects
the active section.

✓ TOC jumps correctly.

✓ Scroll Spy is accurate.

✓ Reading Progress updates smoothly.

✓ Navigation feels invisible.

FAIL

✗ Users become lost.

✗ Multiple active sections.

✗ Reading order changes.

✗ Tabs replace document navigation.

✗ Navigation competes with content.

==============================================================================

28. FUTURE EXTENSIONS
==============================================================================

May support

Bookmarks

Personal Notes

Reading History

Chapter Completion

Collaborative Review

without changing

the navigation hierarchy

or

reading flow.

==============================================================================

29. IMPLEMENTATION NOTES
==============================================================================

This specification defines

Reading Navigation

Document Navigation

State Behaviour

Binding

Acceptance Rules

It does NOT define

HTML

CSS

React

Vue

Router implementation.

==============================================================================

30. FREEZE
==============================================================================

After approval

Navigation becomes

the canonical

Reading Navigation System

of Commercial UI V3.

Every implementation

must preserve

Reading Order

Document Structure

Navigation Hierarchy

Binding Contract

and

Continuous Reading Experience.

# ============================================================================
# END OF DOCUMENT
# ============================================================================