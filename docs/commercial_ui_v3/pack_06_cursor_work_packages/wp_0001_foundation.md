# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 06 — CURSOR WORK PACKAGE
# WP-0001 — FOUNDATION
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : CRITICAL

Work Package ID

WP-0001

Estimated Scope

Foundation Only

Owner

Product Architecture

Executor

Cursor

==============================================================================
1. OBJECTIVE
==============================================================================

Implement

the Commercial UI V3

presentation foundation.

This Work Package

builds

the infrastructure

required

for every subsequent

Work Package.

No Business Screen

is implemented

in this package.

==============================================================================
2. BUSINESS GOAL
==============================================================================

Prepare

a stable,

scalable,

maintainable

presentation foundation

without

changing

Business Logic.

==============================================================================
3. SCOPE
==============================================================================

IN SCOPE

• Global Layout Infrastructure

• Theme Infrastructure

• Design Token Integration

• Global Typography

• Grid System

• Spacing System

• CSS Variables

• Surface System

• Layout Utilities

OUT OF SCOPE

Executive Summary

Four Pillars

Metrics

Analysis

Navigation

Consultation Report

Appendix

Any Business Component

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

Pack 04

00_IMPLEMENTATION_PRINCIPLES

06_STYLING_STRATEGY

10_CODING_CONVENTIONS

==============================================================================
5. ALLOWED FILES
==============================================================================

Cursor MAY modify

styles/

theme/

tokens/

layout/

utilities/

shared styling infrastructure

global CSS

theme configuration

layout helpers

==============================================================================
6. FORBIDDEN FILES
==============================================================================

Cursor SHALL NOT modify

Business Components

Executive Summary

Four Pillars

Metrics

Analysis

Navigation

Appendix

Binding Layer

Backend

API

Engine

Database

Knowledge Base

==============================================================================
7. IMPLEMENTATION TASKS
==============================================================================

Task 1

Create

Design Token Infrastructure.

----------------------------------

Task 2

Implement

CSS Variables.

----------------------------------

Task 3

Implement

Typography System.

----------------------------------

Task 4

Implement

Spacing Scale.

----------------------------------

Task 5

Implement

Grid Infrastructure.

----------------------------------

Task 6

Implement

Surface Styles.

----------------------------------

Task 7

Implement

Theme Infrastructure.

----------------------------------

Task 8

Implement

Layout Utilities.

==============================================================================
8. DELIVERABLES
==============================================================================

Commercial UI Foundation

↓

Global Theme

↓

Token System

↓

Typography

↓

Spacing

↓

Grid

↓

Utilities

==============================================================================
9. BINDING RULES
==============================================================================

No Binding

changes

are allowed.

View Models

must remain

unchanged.

==============================================================================
10. COMPONENT RULES
==============================================================================

No Business Components.

No Shared Components.

No Screen Components.

Foundation only.

==============================================================================
11. ACCESSIBILITY
==============================================================================

Verify

Root Typography

↓

Focus Styles

↓

Contrast Tokens

↓

Reduced Motion Support

==============================================================================
12. PERFORMANCE
==============================================================================

Foundation

must

introduce

minimal

runtime overhead.

No unnecessary

rendering logic.

==============================================================================
13. RESPONSIVE
==============================================================================

Implement

responsive foundations

only.

No responsive

screen behaviour.

==============================================================================
14. TESTS
==============================================================================

Execute

Build

↓

Lint

↓

Foundation Tests

↓

Theme Tests

↓

Token Validation

==============================================================================
15. VISUAL VALIDATION
==============================================================================

Verify

Typography Scale

↓

Spacing Scale

↓

Grid

↓

Colors

↓

Elevation

↓

Dark Theme

↓

Light Theme

==============================================================================
16. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Tokens implemented.

✓ Typography implemented.

✓ Grid implemented.

✓ Spacing implemented.

✓ Themes implemented.

✓ Build PASS.

✓ Lint PASS.

✓ No Business UI modified.

FAIL

✗ Business Components changed.

✗ Binding modified.

✗ Hardcoded values.

✗ Missing Design Tokens.

==============================================================================
17. ROLLBACK
==============================================================================

Rollback

must restore

previous

presentation foundation

without

affecting

Business Logic.

==============================================================================
18. REQUIRED OUTPUT
==============================================================================

Cursor must provide

Implementation Summary

↓

Files Changed

↓

Token Summary

↓

Theme Summary

↓

Tests Executed

↓

Known Issues

↓

Rollback Notes

==============================================================================
19. REVIEW CHECKLIST
==============================================================================

Architecture

□ PASS

Design Tokens

□ PASS

Typography

□ PASS

Spacing

□ PASS

Grid

□ PASS

Theme

□ PASS

Accessibility

□ PASS

Performance

□ PASS

Testing

□ PASS

==============================================================================
20. FREEZE
==============================================================================

After approval

WP-0001

becomes

Frozen.

Subsequent Work Packages

must consume

this Foundation.

No redesign

is permitted

after Freeze.

# ============================================================================
# END OF DOCUMENT
# ============================================================================