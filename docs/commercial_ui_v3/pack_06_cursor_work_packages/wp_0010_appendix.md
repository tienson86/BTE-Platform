# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 06 — CURSOR WORK PACKAGE
# WP-0010 — APPENDIX
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : HIGH

Work Package ID

WP-0010

Estimated Scope

Appendix Screen

Owner

Product Architecture

Executor

Cursor

==============================================================================
1. OBJECTIVE
==============================================================================

Implement

the Appendix Screen

according to

Commercial UI V3.

The Appendix

provides

reference materials,

terminology,

knowledge sources,

and

supporting information

without

interrupting

the main consultation report.

==============================================================================

2. BUSINESS GOAL
==============================================================================

Support

advanced users

who wish

to explore

the underlying

knowledge

behind

the consultation.

The Appendix

is optional.

The main report

must remain

complete

without it.

==============================================================================

3. REQUIRED SPECIFICATIONS
==============================================================================

Cursor MUST read

Pack 01

All Product Architecture

Pack 02

All Design System

Pack 03

07_APPENDIX.md

09_RESPONSIVE_LAYOUTS.md

Pack 03.5

All UX Validation

Pack 04

All Implementation Specifications

WP-0001

↓

WP-0009

==============================================================================

4. SCOPE
==============================================================================

IN SCOPE

Appendix Header

↓

Glossary

↓

Terminology

↓

Knowledge References

↓

Rule References

↓

Interpretation References

↓

Abbreviations

↓

Version Information

↓

Credits

↓

Section Transition

OUT OF SCOPE

Navigation Screen

==============================================================================

5. COMPONENTS TO IMPLEMENT
==============================================================================

Business Components

AppendixContainer

GlossarySection

TerminologySection

KnowledgeReferenceSection

RuleReferenceSection

CitationSection

VersionInformation

CreditsSection

AppendixSummary

Shared Components

SectionHeader

ReferenceBlock

CitationRow

PropertyGrid

PropertyItem

Callout

InformationBox

Accordion

CollapsePanel

TagGroup

ReadingProgress

Base Components

Consume only

WP-0002 components.

==============================================================================

6. LAYOUT REQUIREMENTS
==============================================================================

The Appendix

must follow

Commercial Report Layout V3.

Reading order

Appendix Header

↓

Glossary

↓

Terminology

↓

Knowledge References

↓

Rule References

↓

Credits

↓

Version Information

The Appendix

must feel

lightweight

and

secondary.

==============================================================================

7. READING EXPERIENCE
==============================================================================

Users

must be able

to

enter

and

leave

the Appendix

at any point.

The Appendix

must never

interrupt

the main report

or

change

the consultation narrative.

==============================================================================

8. KNOWLEDGE PRESENTATION
==============================================================================

Knowledge

must be presented

as

reference material.

Do not

repeat

consultation content.

Do not

duplicate

Executive Insight

or

Explainable Analysis.

==============================================================================

9. DATA BINDING
==============================================================================

Components

must consume

Appendix

View Models only.

Forbidden

Raw Payload

Rule Evaluation

Knowledge Query

Business Calculation

==============================================================================

10. STATE SUPPORT
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

11. ACCESSIBILITY
==============================================================================

Verify

Semantic Headings

↓

Keyboard Navigation

↓

Screen Reader Support

↓

Logical Reading Order

↓

Focus Order

↓

Contrast

↓

Reduced Motion

Accordion

must remain

fully accessible.

==============================================================================

12. RESPONSIVE
==============================================================================

Desktop

Reference layout

↓

Tablet

Stacked sections

↓

Mobile

Single-column reading

Reading order

must remain

identical

on every device.

==============================================================================

13. PERFORMANCE
==============================================================================

Lazy-load

large reference lists

when appropriate.

Avoid

loading

unused

reference sections.

Maintain

fast scrolling

throughout

the Appendix.

==============================================================================

14. STYLING
==============================================================================

Consume only

Design Tokens.

Forbidden

Hardcoded spacing

Hardcoded colors

Hardcoded typography

Hardcoded borders

==============================================================================

15. VISUAL VALIDATION
==============================================================================

Verify

Reference hierarchy

↓

Typography

↓

Whitespace

↓

Accordion behaviour

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

17. DELIVERABLES
==============================================================================

Appendix Screen

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

18. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Reading Journey preserved.

✓ Appendix remains secondary.

✓ Glossary readable.

✓ Rule References accessible.

✓ Design Tokens only.

✓ Binding unchanged.

✓ Accessibility PASS.

✓ Responsive PASS.

✓ Performance PASS.

✓ Tests PASS.

FAIL

✗ Appendix dominates report.

✗ Duplicate consultation content.

✗ Hardcoded styling.

✗ Payload parsing.

✗ Business logic inside Components.

==============================================================================

19. ROLLBACK
==============================================================================

Rollback

must restore

the previous

Appendix

without

affecting

Consultation Report

or

Navigation.

==============================================================================

20. REQUIRED OUTPUT
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

21. REVIEW CHECKLIST
==============================================================================

Architecture

□ PASS

Knowledge Hierarchy

□ PASS

Reference Structure

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

22. EXECUTION PROMPT
==============================================================================

Implement

WP-0010 only.

Implement

Appendix Screen only.

Consume

Shared Components

from WP-0003.

Do not modify

Consultation Report,

Navigation,

Backend,

Bindings,

Business Logic,

Database,

Analysis Engine,

or

Knowledge Base.

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

23. APPENDIX CONTRACT (AC)
==============================================================================

The Appendix

must function

as

a reference library.

It must

support

the consultation,

never

replace it.

Every reference

must be

optional,

traceable,

and

non-disruptive

to

the main reading journey.

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

No layout deviation

is permitted

without

Product Architecture approval.

==============================================================================

25. FREEZE
==============================================================================

After approval,

WP-0010

becomes

Frozen.

The Appendix

becomes

the canonical

knowledge reference interface

for Commercial UI V3.

No redesign

is permitted

after Freeze.

# ============================================================================
# END OF DOCUMENT
# ============================================================================