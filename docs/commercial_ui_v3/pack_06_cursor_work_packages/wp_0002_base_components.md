# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 06 — CURSOR WORK PACKAGE
# WP-0002 — BASE COMPONENTS
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : CRITICAL

Work Package ID

WP-0002

Estimated Scope

Base UI Component Library

Owner

Product Architecture

Executor

Cursor

==============================================================================
1. OBJECTIVE
==============================================================================

Implement

the complete

Commercial UI V3

Base Component Library.

Base Components

are

atomic,

reusable,

presentation-only

building blocks.

Business meaning

must not exist

inside Base Components.

==============================================================================
2. BUSINESS GOAL
==============================================================================

Create

a reusable UI foundation

that can be consumed

by every

Shared Component

and

Business Component.

==============================================================================
3. SCOPE
==============================================================================

IN SCOPE

BaseButton

BaseIcon

BaseText

BaseHeading

BaseSurface

BaseDivider

BaseBadge

BaseChip

BaseTag

BaseAvatar

BaseSpinner

BaseSkeleton

BaseProgress

BaseTooltip

BaseLink

BaseInput

BaseTextarea

BaseSelect

BaseCheckbox

BaseRadio

BaseSwitch

BaseAlert

BaseCallout

BaseEmptyState

BaseErrorState

BaseUnavailableState

BaseLoadingState

BaseScrollArea

BaseContainer

BaseStack

BaseGrid

OUT OF SCOPE

Executive Summary

Four Pillars

Metrics

Analysis

Consultation Report

Navigation

Appendix

Business Components

Shared Components

==============================================================================
4. REQUIRED SPECIFICATIONS
==============================================================================

Cursor MUST read

Pack 02

00_VISUAL_LANGUAGE

01_DESIGN_TOKENS

02_GRID_SYSTEM

03_SPACING_SYSTEM

04_TYPOGRAPHY_SYSTEM

05_COLOR_SYSTEM

06_ELEVATION_AND_SURFACE

07_ICONOGRAPHY

08_MOTION_SYSTEM

09_COMPONENT_PRINCIPLES

Pack 04

02_COMPONENT_ARCHITECTURE

05_STATE_MANAGEMENT

06_STYLING_STRATEGY

07_ACCESSIBILITY_IMPLEMENTATION

10_CODING_CONVENTIONS

==============================================================================
5. ALLOWED FILES
==============================================================================

Cursor MAY modify

components/base/

styles/components/base/

tokens/

theme/

stories/base/

tests/base/

==============================================================================
6. FORBIDDEN FILES
==============================================================================

Cursor SHALL NOT modify

Business Components

Shared Components

Business Screens

Bindings

Adapters

Backend

API

Database

Analysis Engine

Knowledge Base

==============================================================================
7. IMPLEMENTATION TASKS
==============================================================================

Task 1

Create

Base Component folder structure.

----------------------------------

Task 2

Implement

visual primitives.

----------------------------------

Task 3

Implement

layout primitives.

----------------------------------

Task 4

Implement

feedback primitives.

----------------------------------

Task 5

Implement

form primitives.

----------------------------------

Task 6

Implement

loading primitives.

----------------------------------

Task 7

Implement

semantic state primitives.

----------------------------------

Task 8

Implement

responsive behaviour.

----------------------------------

Task 9

Implement

Dark Theme compatibility.

----------------------------------

Task 10

Implement

Accessibility support.

==============================================================================
8. COMPONENT REQUIREMENTS
==============================================================================

Every Base Component

must

have

Single Responsibility

↓

Token-driven Styling

↓

Accessibility Support

↓

Responsive Behaviour

↓

Dark Theme Support

↓

TypeScript Types

↓

Unit Tests

↓

Visual Tests

No component

may contain

Business Logic.

==============================================================================
9. STATE SUPPORT
==============================================================================

Where applicable

Base Components

must support

Default

Hover

Active

Focused

Disabled

Loading

Error

==============================================================================
10. ACCESSIBILITY
==============================================================================

Every Base Component

must support

Semantic HTML

↓

Keyboard Navigation

↓

Focus Ring

↓

ARIA

↓

Screen Readers

↓

Contrast Compliance

==============================================================================
11. RESPONSIVE
==============================================================================

Base Components

must adapt

to

Desktop

Tablet

Mobile

without

changing

their API.

==============================================================================
12. PERFORMANCE
==============================================================================

Base Components

must remain

lightweight.

No unnecessary

state.

No unnecessary

re-rendering.

No hidden

business calculations.

==============================================================================
13. API DESIGN
==============================================================================

Every Base Component

must expose

minimal,

predictable,

typed

props.

Avoid

generic

configuration objects.

==============================================================================
14. STYLING
==============================================================================

All styling

must consume

Design Tokens.

Forbidden

Hardcoded Colors

Hardcoded Typography

Hardcoded Radius

Hardcoded Shadow

Hardcoded Spacing

==============================================================================
15. TESTING
==============================================================================

Execute

Build

↓

Lint

↓

Unit Tests

↓

Accessibility Tests

↓

Responsive Tests

↓

Visual Regression

==============================================================================
16. VISUAL VALIDATION
==============================================================================

Verify

Typography

↓

Spacing

↓

States

↓

Icons

↓

Borders

↓

Elevation

↓

Theme Switching

==============================================================================
17. DELIVERABLES
==============================================================================

Base Component Library

↓

Stories

↓

Tests

↓

Documentation

↓

Type Definitions

==============================================================================
18. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Base Components implemented.

✓ Design Tokens used everywhere.

✓ Accessibility PASS.

✓ Responsive PASS.

✓ Theme PASS.

✓ Build PASS.

✓ Lint PASS.

✓ Tests PASS.

✓ No Business Logic.

FAIL

✗ Business behaviour exists.

✗ Hardcoded styling.

✗ Missing accessibility.

✗ Missing tests.

✗ Missing responsive support.

==============================================================================
19. ROLLBACK
==============================================================================

Rollback

must restore

previous

Base Component Library

without

changing

Foundation

or

Business UI.

==============================================================================
20. REQUIRED OUTPUT
==============================================================================

Cursor must provide

Implementation Summary

↓

Component List

↓

Files Changed

↓

Stories Created

↓

Tests Executed

↓

Accessibility Results

↓

Known Issues

↓

Rollback Notes

==============================================================================
21. REVIEW CHECKLIST
==============================================================================

Architecture

□ PASS

Design Tokens

□ PASS

Component API

□ PASS

Accessibility

□ PASS

Responsive

□ PASS

Performance

□ PASS

Testing

□ PASS

Documentation

□ PASS

==============================================================================
22. EXECUTION PROMPT
==============================================================================

Implement

WP-0002 only.

Create

Base Components only.

Do not implement

Shared Components.

Do not implement

Business Components.

Do not modify

Bindings,

Backend,

Business Logic,

or

Screen Layouts.

Return

1.

Files Changed

2.

Components Created

3.

Tests Executed

4.

Visual Validation

5.

Accessibility Validation

6.

Acceptance Checklist

==============================================================================
23. FREEZE
==============================================================================

After approval,

WP-0002

becomes

Frozen.

All subsequent

Work Packages

must consume

this Base Component Library.

No redesign

is permitted

after Freeze.

# ============================================================================
# END OF DOCUMENT
# ============================================================================