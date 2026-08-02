# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 06 — CURSOR WORK PACKAGE
# WP-0009 — CONSULTATION REPORT
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : CRITICAL

Work Package ID

WP-0009

Estimated Scope

Commercial Consultation Report

Owner

Product Architecture

Executor

Cursor

==============================================================================
1. OBJECTIVE
==============================================================================

Implement

the Commercial Consultation Report

according to

Commercial UI V3.

This Work Package

assembles

all previous Business Screens

into

one continuous,

professional,

consulting document.

The final experience

must resemble

a premium advisory report,

not

a collection

of dashboards.

==============================================================================

2. BUSINESS GOAL
==============================================================================

Deliver

a complete,

commercial-grade,

consultation report

that users

can read,

understand,

share,

and trust.

The report

must present

analysis

as

one coherent narrative.

==============================================================================

3. REQUIRED SPECIFICATIONS
==============================================================================

Cursor MUST read

Pack 01

All Product Architecture

Pack 02

All Design System

Pack 03

06_CONSULTATION_REPORT.md

Pack 03.5

All UX Validation

Pack 04

All Implementation Specifications

WP-0001

↓

WP-0008

==============================================================================

4. SCOPE
==============================================================================

IN SCOPE

Commercial Report Container

↓

Table of Contents

↓

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

Reading Progress

↓

Section Transitions

↓

Report Footer

↓

Print Layout

↓

PDF-ready Presentation

OUT OF SCOPE

Appendix

Navigation Screen

==============================================================================

5. COMPONENTS TO IMPLEMENT
==============================================================================

Business Components

ConsultationReport

ReportContainer

ReportHeader

ReportSection

ReportFooter

ReportProgress

SectionTransition

TableOfContents

PrintHeader

PrintFooter

Shared Components

Consume only

approved Shared Components

from

WP-0003.

Business Components

Consume only

approved Business Components

from

WP-0004

↓

WP-0008.

==============================================================================

6. REPORT STRUCTURE
==============================================================================

The report

must follow

exactly

this order.

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

Report Closing

No section

may change

its position.

==============================================================================

7. READING EXPERIENCE
==============================================================================

The report

must support

continuous,

long-form reading.

The user

must never

feel

they are

moving

between

independent dashboards.

Every section

must transition

naturally

into

the next.

==============================================================================

8. REPORT LAYOUT
==============================================================================

Typography

defines

hierarchy.

Whitespace

defines

structure.

Surfaces

define

grouping.

Borders

must remain

minimal.

Cards

must be used

only

when

they improve

readability.

==============================================================================

9. DATA BINDING
==============================================================================

The Report

must consume

approved

View Models only.

The Report

must not

perform

Business Logic

Rule Evaluation

Knowledge Queries

Data Transformation

==============================================================================

10. STATE SUPPORT
==============================================================================

The Report

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

11. ACCESSIBILITY
==============================================================================

Verify

Semantic Headings

↓

Table of Contents Navigation

↓

Keyboard Navigation

↓

Logical Reading Order

↓

Screen Reader Support

↓

Contrast

↓

Reduced Motion

The report

must remain

fully readable

without

visual styling.

==============================================================================

12. RESPONSIVE
==============================================================================

Desktop

Premium Report

↓

Tablet

Adaptive Reading

↓

Mobile

Reading-first

single column

Reading order

must remain

identical

on every device.

==============================================================================

13. PERFORMANCE
==============================================================================

Render

Executive Summary

first.

Progressively render

lower sections.

Avoid

layout shift.

Avoid

blocking rendering.

Support

large reports

efficiently.

==============================================================================

14. STYLING
==============================================================================

Consume only

Design Tokens.

Forbidden

Hardcoded colors

Hardcoded spacing

Hardcoded typography

Hardcoded shadows

Hardcoded borders

==============================================================================

15. PRINT & PDF
==============================================================================

The report

must support

clean

Print Layout

↓

PDF Export Layout

↓

A4 Pagination

↓

Page Break Rules

↓

Print-safe Typography

No visual artifacts

are permitted.

==============================================================================

16. VISUAL VALIDATION
==============================================================================

Verify

Reading hierarchy

↓

Section rhythm

↓

Whitespace

↓

Typography

↓

Surface hierarchy

↓

Print layout

↓

Dark Theme

↓

Light Theme

==============================================================================

17. TESTING
==============================================================================

Execute

Build

↓

Lint

↓

Integration Tests

↓

Binding Tests

↓

Accessibility Tests

↓

Responsive Tests

↓

Performance Tests

↓

Print Validation

↓

Visual Regression

==============================================================================

18. DELIVERABLES
==============================================================================

Commercial Consultation Report

↓

Business Components

↓

Styles

↓

Print Styles

↓

Tests

↓

Documentation

↓

Visual Comparison

==============================================================================

19. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Reading Journey matches Pack 03.

✓ Continuous narrative preserved.

✓ Table of Contents functional.

✓ Print layout verified.

✓ PDF layout verified.

✓ Design Tokens only.

✓ Binding unchanged.

✓ Accessibility PASS.

✓ Responsive PASS.

✓ Performance PASS.

✓ Tests PASS.

FAIL

✗ Dashboard appearance.

✗ Broken narrative.

✗ Incorrect section order.

✗ Hardcoded styling.

✗ Business logic inside Components.

✗ Payload parsing.

==============================================================================

20. ROLLBACK
==============================================================================

Rollback

must restore

the previous

Consultation Report

without

affecting

Executive Summary,

Four Pillars,

Executive Insight,

Metrics,

or

Explainable Analysis.

==============================================================================

21. REQUIRED OUTPUT
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

Print Validation

↓

Binding Validation

↓

Accessibility Report

↓

Performance Report

↓

Acceptance Checklist

==============================================================================

22. REVIEW CHECKLIST
==============================================================================

Architecture

□ PASS

Report Structure

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

Print Layout

□ PASS

Testing

□ PASS

==============================================================================

23. EXECUTION PROMPT
==============================================================================

Implement

WP-0009 only.

Assemble

the Commercial Consultation Report

using

approved Business Components

from

WP-0004

↓

WP-0008.

Do not implement

Appendix

Navigation

Do not modify

Backend

Bindings

Business Logic

Database

Analysis Engine

Knowledge Base

Return

1.

Files Changed

2.

Business Components Used

3.

Visual Comparison

4.

Print Validation

5.

Accessibility Validation

6.

Performance Validation

7.

Acceptance Checklist

==============================================================================

24. COMMERCIAL REPORT CONTRACT (CRC)
==============================================================================

The report

must behave

as

one document.

Every section

must connect

to

the next

through

consistent

spacing,

typography,

and

section transitions.

No section

may appear

as

an isolated dashboard.

==============================================================================

25. REFERENCE SCREENSHOT CONTRACT (RSC)
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

26. FREEZE
==============================================================================

After approval,

WP-0009

becomes

Frozen.

The Commercial Consultation Report

becomes

the canonical

report presentation

for Commercial UI V3.

No redesign

is permitted

after Freeze.

# ============================================================================
# END OF DOCUMENT
# ============================================================================