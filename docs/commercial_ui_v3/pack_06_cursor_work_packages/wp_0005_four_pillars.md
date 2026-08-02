# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 06 — CURSOR WORK PACKAGE
# WP-0005 — FOUR PILLARS
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : CRITICAL

Work Package ID

WP-0005

Estimated Scope

Four Pillars Screen

Owner

Product Architecture

Executor

Cursor

==============================================================================
1. OBJECTIVE
==============================================================================

Implement

the Four Pillars Screen

according to

Commercial UI V3.

This screen

is the canonical

BaZi Chart Presentation.

It must present

the complete

Four Pillars

clearly,

accurately,

and

professionally,

while preserving

Commercial Report

reading experience.

==============================================================================
2. BUSINESS GOAL
==============================================================================

Present

the complete

BaZi Chart

as the

primary reference

for all

subsequent analysis.

The user

must understand

the chart structure

before reading

any interpretation.

==============================================================================

3. REQUIRED SPECIFICATIONS
==============================================================================

Cursor MUST read

Pack 01

02_INFORMATION_ARCHITECTURE.md

03_READING_JOURNEY.md

04_PAGE_LAYOUT.md

05_VISUAL_HIERARCHY.md

Pack 02

All Design System

Pack 03

02_FOUR_PILLARS.md

09_RESPONSIVE_LAYOUTS.md

Pack 03.5

01_DESKTOP_WIREFRAMES.md

02_TABLET_WIREFRAMES.md

03_MOBILE_WIREFRAMES.md

04_DEVICE_BEHAVIOR_MATRIX.md

05_READING_FLOW_VALIDATION.md

Pack 04

All Implementation Specifications

WP-0001

WP-0002

WP-0003

==============================================================================

4. SCOPE
==============================================================================

IN SCOPE

Four Pillars Header

↓

Chart Grid

↓

Year Pillar

↓

Month Pillar

↓

Day Pillar

↓

Hour Pillar

↓

Hidden Stems

↓

Ten Gods Labels

↓

Na Yin

↓

Life Stage

↓

Chart Metadata

↓

Section Transition

OUT OF SCOPE

Executive Insight

Metrics

Explainable Analysis

Consultation Report

Appendix

Navigation

==============================================================================

5. COMPONENTS TO IMPLEMENT
==============================================================================

Business Components

FourPillarsChart

PillarColumn

PillarHeader

HeavenlyStemCell

EarthlyBranchCell

HiddenStemGroup

NaYinPanel

LifeStagePanel

ChartMetadata

ChartLegend

Shared Components

SectionHeader

PropertyGrid

PropertyItem

LabelValueRow

StatusBadge

InformationBox

Callout

Divider

Base Components

Consume only

WP-0002 components.

==============================================================================

6. LAYOUT REQUIREMENTS
==============================================================================

The screen

must follow

Commercial Report Layout V3.

Reading order

Section Title

↓

Chart Overview

↓

Four Pillars Grid

↓

Hidden Stems

↓

Metadata

↓

Legend

↓

Section Transition

The chart

must remain

the visual focus.

Supporting information

must not

compete

with the chart.

==============================================================================

7. VISUAL REQUIREMENTS
==============================================================================

The Four Pillars Grid

must appear

balanced,

symmetrical,

and

easy to scan.

All four pillars

must receive

equal visual weight.

The Day Pillar

may receive

subtle emphasis,

but

must not

dominate

the layout.

Borders

must be minimal.

Whitespace

defines

structure.

==============================================================================

8. DATA BINDING
==============================================================================

Components

must consume

Four Pillars

View Models only.

Forbidden

Raw Payload

Business Calculation

Rule Execution

Engine Invocation

==============================================================================

9. STATE SUPPORT
==============================================================================

Every Business Component

must support

Loading

↓

Ready

↓

Empty

↓

Unavailable

↓

Error

according to

Presentation State Contract.

==============================================================================

10. ACCESSIBILITY
==============================================================================

Verify

Semantic Headings

↓

Keyboard Navigation

↓

Logical Reading Order

↓

Screen Reader Labels

↓

Contrast

↓

Reduced Motion

All chart values

must have

accessible text.

==============================================================================

11. RESPONSIVE
==============================================================================

Desktop

Four-column layout

↓

Tablet

Adaptive layout

↓

Mobile

Single reading flow

Reading order

must remain

identical

on every device.

==============================================================================

12. PERFORMANCE
==============================================================================

Render

the chart

before

secondary metadata.

No unnecessary

animations.

No layout shift.

No delayed chart rendering.

==============================================================================

13. STYLING
==============================================================================

Consume only

Design Tokens.

Forbidden

Hardcoded spacing

Hardcoded colors

Hardcoded typography

Hardcoded borders

Hardcoded shadows

==============================================================================

14. VISUAL VALIDATION
==============================================================================

Verify

Chart symmetry

↓

Column alignment

↓

Typography hierarchy

↓

Spacing rhythm

↓

Surface hierarchy

↓

Dark Theme

↓

Light Theme

==============================================================================

15. TESTING
==============================================================================

Execute

Build

↓

Lint

↓

Component Tests

↓

Binding Tests

↓

Accessibility Tests

↓

Responsive Tests

↓

Performance Tests

↓

Visual Regression

==============================================================================

16. DELIVERABLES
==============================================================================

Four Pillars Screen

↓

Business Components

↓

Styles

↓

Tests

↓

Documentation

↓

Visual Comparison

==============================================================================

17. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Four Pillars Grid matches Pack 03.

✓ Reading order preserved.

✓ Day Pillar emphasis is subtle.

✓ Hidden Stems displayed correctly.

✓ Metadata clearly separated.

✓ Design Tokens only.

✓ Binding unchanged.

✓ Accessibility PASS.

✓ Responsive PASS.

✓ Performance PASS.

✓ Tests PASS.

FAIL

✗ Dashboard appearance.

✗ Uneven pillar alignment.

✗ Excessive borders.

✗ Hardcoded styling.

✗ Payload parsing.

✗ Business logic inside Components.

==============================================================================

18. ROLLBACK
==============================================================================

Rollback

must restore

the previous

Four Pillars Screen

without

affecting

Executive Summary

or

subsequent screens.

==============================================================================

19. REQUIRED OUTPUT
==============================================================================

Cursor must provide

Implementation Summary

↓

Files Changed

↓

Business Components Created

↓

Visual Comparison

↓

Binding Validation

↓

Accessibility Report

↓

Performance Report

↓

Acceptance Checklist

==============================================================================

20. REVIEW CHECKLIST
==============================================================================

Architecture

□ PASS

Chart Layout

□ PASS

Reading Journey

□ PASS

Design Tokens

□ PASS

Binding

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

21. EXECUTION PROMPT
==============================================================================

Implement

WP-0005 only.

Implement

Four Pillars Screen only.

Consume

Shared Components

from WP-0003.

Do not implement

Executive Insight

Metrics

Explainable Analysis

Consultation Report

Appendix

Navigation

Do not modify

Backend

Bindings

Business Logic

Database

Analysis Engine

Return

1.

Files Changed

2.

Business Components Created

3.

Visual Comparison

4.

Binding Validation

5.

Accessibility Validation

6.

Performance Validation

7.

Acceptance Checklist

==============================================================================

22. REFERENCE SCREENSHOT CONTRACT (RSC)
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

No layout deviation

is permitted

without

Product Architecture approval.

==============================================================================

23. FREEZE
==============================================================================

After approval,

WP-0005

becomes

Frozen.

The Four Pillars Screen

becomes

the canonical

BaZi Chart presentation

for Commercial UI V3.

No redesign

is permitted

after Freeze.

# ============================================================================
# END OF DOCUMENT
# ============================================================================