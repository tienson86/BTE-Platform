# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 06 — CURSOR WORK PACKAGE
# WP-0011 — NAVIGATION
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : HIGH

Work Package ID

WP-0011

Estimated Scope

Reading Navigation System

Owner

Product Architecture

Executor

Cursor

==============================================================================
1. OBJECTIVE
==============================================================================

Implement

the Commercial UI V3

Reading Navigation System.

Navigation

must support

long-form reading,

not

dashboard interaction.

Users

must always know

where they are,

what they are reading,

and

what comes next.

==============================================================================

2. BUSINESS GOAL
==============================================================================

Provide

an intuitive

reading-oriented

navigation system

that improves

orientation,

discoverability,

and

reading efficiency

without

interrupting

the consultation experience.

==============================================================================

3. REQUIRED SPECIFICATIONS
==============================================================================

Cursor MUST read

Pack 01

All Product Architecture

Pack 02

All Design System

Pack 03

08_NAVIGATION.md

09_RESPONSIVE_LAYOUTS.md

Pack 03.5

04_DEVICE_BEHAVIOR_MATRIX.md

05_READING_FLOW_VALIDATION.md

Pack 04

All Implementation Specifications

WP-0001

↓

WP-0010

==============================================================================

4. SCOPE
==============================================================================

IN SCOPE

Reading Rail

↓

Table of Contents

↓

Scroll Spy

↓

Reading Progress

↓

Current Section Indicator

↓

Jump Navigation

↓

Back To Top

↓

Section Anchors

↓

Reading Breadcrumb

↓

Print Navigation

OUT OF SCOPE

Business Screens

Business Components

Sidebar Menus

Application Routing

==============================================================================

5. COMPONENTS TO IMPLEMENT
==============================================================================

Business Components

ReadingNavigation

ReadingRail

TableOfContents

ScrollSpy

ReadingProgress

CurrentSection

JumpNavigator

AnchorNavigation

BackToTop

ReadingBreadcrumb

PrintNavigator

Shared Components

SectionHeader

Divider

PropertyItem

StatusBadge

Callout

InformationBox

Base Components

Consume only

WP-0002 components.

==============================================================================

6. NAVIGATION MODEL
==============================================================================

Navigation

must follow

the reading journey.

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

Navigation

must never

reorder

the report.

==============================================================================

7. READING EXPERIENCE
==============================================================================

Navigation

must remain

secondary

to

content.

Users

must always

focus on

the report,

not

the navigation.

Navigation

must quietly

support

reading.

==============================================================================

8. BEHAVIOR REQUIREMENTS
==============================================================================

Reading Rail

must

highlight

the active section.

Scroll Spy

must

follow

the reading position.

Table of Contents

must support

direct navigation

to

approved sections.

Back To Top

must appear

only when useful.

==============================================================================

9. DATA BINDING
==============================================================================

Navigation

must consume

Navigation View Models only.

Forbidden

Business Logic

Payload Parsing

Rule Evaluation

Knowledge Query

==============================================================================

10. STATE SUPPORT
==============================================================================

Navigation

must support

Loading

↓

Ready

↓

Unavailable

↓

Error

according to

Presentation State Contract.

==============================================================================

11. ACCESSIBILITY
==============================================================================

Verify

Semantic Navigation

↓

Keyboard Navigation

↓

Skip Links

↓

Focus Order

↓

Screen Reader Labels

↓

Current Section Announcement

↓

Reduced Motion

==============================================================================

12. RESPONSIVE
==============================================================================

Desktop

Persistent Reading Rail

↓

Tablet

Collapsible Reading Rail

↓

Mobile

Compact Reading Navigator

Reading order

must remain

identical

across

all devices.

==============================================================================

13. PERFORMANCE
==============================================================================

Navigation

must remain

lightweight.

Scroll tracking

must not

degrade

scroll performance.

Avoid

continuous

layout recalculation.

==============================================================================

14. STYLING
==============================================================================

Consume only

Design Tokens.

Forbidden

Hardcoded spacing

Hardcoded colors

Hardcoded typography

Hardcoded shadows

==============================================================================

15. VISUAL VALIDATION
==============================================================================

Verify

Navigation hierarchy

↓

Reading Rail

↓

Scroll Progress

↓

Current Section

↓

Dark Theme

↓

Light Theme

==============================================================================

16. TESTING
==============================================================================

Execute

Build

↓

Lint

↓

Component Tests

↓

Accessibility Tests

↓

Responsive Tests

↓

Performance Tests

↓

Visual Regression

==============================================================================

17. DELIVERABLES
==============================================================================

Reading Navigation System

↓

Navigation Components

↓

Styles

↓

Tests

↓

Documentation

↓

Visual Comparison

==============================================================================

18. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Reading Journey preserved.

✓ Reading Rail functional.

✓ Scroll Spy accurate.

✓ Table of Contents synchronized.

✓ Current Section highlighted.

✓ Design Tokens only.

✓ Accessibility PASS.

✓ Responsive PASS.

✓ Performance PASS.

✓ Tests PASS.

FAIL

✗ Dashboard navigation.

✗ Business logic in Navigation.

✗ Hardcoded styling.

✗ Incorrect reading order.

✗ Scroll lag.

==============================================================================

19. ROLLBACK
==============================================================================

Rollback

must restore

the previous

Navigation System

without

affecting

Business Screens

or

Consultation Report.

==============================================================================

20. REQUIRED OUTPUT
==============================================================================

Cursor must provide

Implementation Summary

↓

Files Changed

↓

Navigation Components Created

↓

Visual Comparison

↓

Accessibility Report

↓

Performance Report

↓

Acceptance Checklist

==============================================================================

21. REVIEW CHECKLIST
==============================================================================

Architecture

□ PASS

Reading Navigation

□ PASS

Scroll Behaviour

□ PASS

Design Tokens

□ PASS

Accessibility

□ PASS

Responsive

□ PASS

Performance

□ PASS

Testing

□ PASS

==============================================================================

22. EXECUTION PROMPT
==============================================================================

Implement

WP-0011 only.

Implement

Reading Navigation only.

Consume

approved

Business Components

and

Shared Components.

Do not modify

Business Logic

Bindings

Backend

Database

Analysis Engine

Knowledge Base

Application Routing

Return

1.

Files Changed

2.

Navigation Components Created

3.

Visual Comparison

4.

Accessibility Validation

5.

Performance Validation

6.

Acceptance Checklist

==============================================================================

23. READING NAVIGATION CONTRACT (RNC)
==============================================================================

Navigation

exists

to support

reading.

Every navigation action

must help

the user

locate,

continue,

or

return

within

the report.

Navigation

must never

compete

with

the report content.

==============================================================================

24. REFERENCE SCREENSHOT CONTRACT (RSC)
==============================================================================

The implementation

must be validated

against

Approved Desktop Wireframe

↓

Approved Tablet Wireframe

↓

Approved Mobile Wireframe

↓

Pack 03 Screen Specification

↓

Commercial UI V3 Visual Hierarchy

↓

Commercial Report Layout V3

No layout deviation

is permitted

without

Product Architecture approval.

==============================================================================

25. FREEZE
==============================================================================

After approval,

WP-0011

becomes

Frozen.

The Reading Navigation System

becomes

the canonical

navigation model

for Commercial UI V3.

No redesign

is permitted

after Freeze.

# ============================================================================
# END OF DOCUMENT
# ============================================================================