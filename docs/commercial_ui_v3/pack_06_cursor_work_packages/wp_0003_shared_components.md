# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 06 — CURSOR WORK PACKAGE
# WP-0003 — SHARED COMPONENTS
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : CRITICAL

Work Package ID

WP-0003

Estimated Scope

Shared Component Library

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

Shared Component Library.

Shared Components

compose

Base Components

into

reusable,

business-independent

presentation modules.

Shared Components

must not

contain

Business Logic.

==============================================================================
2. BUSINESS GOAL
==============================================================================

Create

a reusable

presentation layer

shared

across

every Business Screen

in Commercial UI V3.

==============================================================================
3. SCOPE
==============================================================================

IN SCOPE

SectionHeader

SectionDivider

SectionContainer

SectionSurface

MetricRow

MetricGroup

MetricCard

LabelValueRow

StatusBadge

ConfidenceBadge

EvidenceRow

EvidenceList

PropertyGrid

PropertyItem

KeyValueGrid

KeyValueRow

HighlightBox

InformationBox

WarningBox

SuccessBox

InsightBox

Callout

ReadingProgress

StickyReadingRail

ScrollSpy

CollapsePanel

Accordion

TabPanel

Timeline

TimelineItem

EmptyState

UnavailableState

LoadingState

ErrorState

SearchBar

FilterBar

Toolbar

FooterNote

GlossaryEntry

CitationRow

ReferenceBlock

TagGroup

ChipGroup

SkeletonSection

SkeletonMetric

SkeletonParagraph

OUT OF SCOPE

Executive Summary

Four Pillars

Executive Insight

Metrics

Analysis

Consultation Report

Appendix

Business Components

==============================================================================
4. REQUIRED SPECIFICATIONS
==============================================================================

Cursor MUST read

Pack 02

00_VISUAL_LANGUAGE

01_DESIGN_TOKENS

09_COMPONENT_PRINCIPLES

Pack 03

All Screen Specifications

(for context only)

Pack 04

02_COMPONENT_ARCHITECTURE

05_STATE_MANAGEMENT

06_STYLING_STRATEGY

07_ACCESSIBILITY_IMPLEMENTATION

10_CODING_CONVENTIONS

WP-0001

WP-0002

==============================================================================
5. ALLOWED FILES
==============================================================================

Cursor MAY modify

components/shared/

styles/components/shared/

stories/shared/

tests/shared/

==============================================================================
6. FORBIDDEN FILES
==============================================================================

Cursor SHALL NOT modify

Business Components

Business Screens

Binding Layer

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

Shared Component structure.

----------------------------------

Task 2

Implement

Section components.

----------------------------------

Task 3

Implement

Information components.

----------------------------------

Task 4

Implement

Evidence components.

----------------------------------

Task 5

Implement

Navigation helpers.

----------------------------------

Task 6

Implement

Reading helpers.

----------------------------------

Task 7

Implement

State components.

----------------------------------

Task 8

Implement

Skeleton library.

----------------------------------

Task 9

Implement

Documentation.

----------------------------------

Task 10

Implement

Testing.

==============================================================================
8. COMPONENT RULES
==============================================================================

Shared Components

must

compose

Base Components only.

Shared Components

must never

consume

Business Models

Business Rules

Business Services

Business Calculations.

==============================================================================
9. DATA RULES
==============================================================================

Shared Components

receive

Presentation Props only.

Forbidden

Raw Payload

API Response

Domain Objects

Business Entities

==============================================================================
10. STATE SUPPORT
==============================================================================

Every applicable

Shared Component

must support

Loading

Ready

Empty

Unavailable

Error

according to

PSC

(Presentation State Contract).

==============================================================================
11. ACCESSIBILITY
==============================================================================

Every Shared Component

must support

Semantic HTML

↓

Keyboard Navigation

↓

Focus Management

↓

ARIA

↓

Screen Readers

↓

Reduced Motion

↓

Contrast Compliance

==============================================================================
12. RESPONSIVE
==============================================================================

Shared Components

must support

Desktop

Tablet

Mobile

without

changing

their public API.

==============================================================================
13. PERFORMANCE
==============================================================================

Shared Components

must remain

lightweight.

Avoid

nested rendering.

Avoid

deep component trees.

Avoid

unnecessary state.

==============================================================================
14. STYLING
==============================================================================

All Shared Components

must consume

Base Components

↓

Design Tokens

↓

Theme Tokens

Hardcoded styling

is forbidden.

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

Accessibility Tests

↓

Responsive Tests

↓

Visual Regression

↓

Snapshot Tests

==============================================================================
16. VISUAL VALIDATION
==============================================================================

Verify

Spacing

↓

Typography

↓

Hierarchy

↓

Elevation

↓

Borders

↓

States

↓

Dark Theme

↓

Light Theme

==============================================================================
17. DELIVERABLES
==============================================================================

Shared Component Library

↓

Documentation

↓

Stories

↓

Tests

↓

Usage Examples

==============================================================================
18. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Shared Components implemented.

✓ Base Components reused.

✓ No Business Logic.

✓ Design Tokens used.

✓ Accessibility PASS.

✓ Responsive PASS.

✓ Theme PASS.

✓ Tests PASS.

FAIL

✗ Business behaviour.

✗ Business calculations.

✗ Payload parsing.

✗ Hardcoded styling.

✗ Duplicate Base Components.

==============================================================================
19. ROLLBACK
==============================================================================

Rollback

must restore

previous

Shared Component Library

without

affecting

Foundation

or

Business Components.

==============================================================================
20. REQUIRED OUTPUT
==============================================================================

Cursor must provide

Implementation Summary

↓

Shared Components Created

↓

Files Changed

↓

Stories Added

↓

Tests Executed

↓

Accessibility Report

↓

Known Issues

↓

Rollback Notes

==============================================================================
21. REVIEW CHECKLIST
==============================================================================

Architecture

□ PASS

Composition

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

Documentation

□ PASS

==============================================================================
22. EXECUTION PROMPT
==============================================================================

Implement

WP-0003 only.

Create

Shared Components only.

Consume

Base Components.

Do not create

Business Components.

Do not modify

Business Screens,

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

Stories Added

4.

Tests Executed

5.

Accessibility Validation

6.

Acceptance Checklist

==============================================================================
23. FREEZE
==============================================================================

After approval,

WP-0003

becomes

Frozen.

All Business Components

must consume

the Shared Component Library.

Direct composition

from Base Components

inside Business Components

is prohibited

unless

explicitly approved

by Product Architecture.

# ============================================================================
# END OF DOCUMENT
# ============================================================================