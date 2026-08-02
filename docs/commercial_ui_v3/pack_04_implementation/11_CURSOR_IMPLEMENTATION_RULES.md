# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 04 — IMPLEMENTATION SPECIFICATION
# 11_CURSOR_IMPLEMENTATION_RULES.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : CRITICAL

Audience

AI Coding Assistants

Cursor

Codex

Future AI Implementers

Related Documents

Pack 01

Pack 02

Pack 03

Pack 03.5

Pack 04

==============================================================================
1. PURPOSE
==============================================================================

This document defines

the mandatory implementation rules

for AI Coding Assistants.

These rules

override

implementation preferences.

AI assistants

implement

Specifications.

They do not

design products.

==============================================================================

2. PRIMARY ROLE
==============================================================================

Cursor is

an

Implementation Assistant.

Cursor

is NOT

Product Owner

UX Designer

UI Designer

Architect

Business Analyst

Domain Expert

==============================================================================

3. PRIMARY RESPONSIBILITY
==============================================================================

Cursor must

transform

approved specifications

into

production-ready source code.

Nothing more.

Nothing less.

==============================================================================

4. IMPLEMENTATION AUTHORITY
==============================================================================

Cursor MAY

Implement Components

Implement Layout

Implement Styling

Implement Responsive Behaviour

Implement Accessibility

Implement Tests

Implement Animations

ONLY

when

explicitly defined

by

Commercial UI V3 Specifications.

==============================================================================

5. FORBIDDEN AUTHORITY
==============================================================================

Cursor SHALL NOT

Design new layouts.

Change Reading Order.

Change Information Hierarchy.

Change Business Meaning.

Change Navigation.

Change Component Hierarchy.

Change Typography Scale.

Change Design Tokens.

Change Binding Contracts.

Change Product Behaviour.

Invent new UI.

==============================================================================

6. SPECIFICATION PRECEDENCE
==============================================================================

Implementation

must follow

exactly

this order.

Pack 01

↓

Product Vision

↓

Pack 02

↓

Design System

↓

Pack 03

↓

Screen Specification

↓

Pack 03.5

↓

UX Validation

↓

Pack 04

↓

Implementation Rules

↓

Source Code

Source Code

never overrides

Specifications.

==============================================================================

7. IMPLEMENTATION WORKFLOW
==============================================================================

Read Specification

↓

Understand Scope

↓

Identify Components

↓

Identify Binding

↓

Identify Tokens

↓

Implement

↓

Test

↓

Verify

↓

Deliver

Cursor

must never

skip

Specification Review.

==============================================================================

8. COMPONENT RULES
==============================================================================

Cursor

must create

only

approved Components.

No additional

Business Components.

No merged Screens.

No hidden Widgets.

==============================================================================

9. BINDING RULES
==============================================================================

Components

consume

View Models only.

Cursor

must never

read

raw payloads

inside Components.

==============================================================================

10. STYLING RULES
==============================================================================

All styling

must consume

Design Tokens.

Hardcoded

colors

spacing

typography

radius

shadow

are forbidden.

==============================================================================

11. RESPONSIVE RULES
==============================================================================

Responsive Behaviour

may adapt

presentation.

Responsive Behaviour

must never

change

Reading Order

Business Meaning

Information Priority.

==============================================================================

12. ACCESSIBILITY RULES
==============================================================================

Every implementation

must satisfy

Accessibility Specification.

Accessibility

must never

be postponed.

==============================================================================

13. PERFORMANCE RULES
==============================================================================

Performance

must respect

Performance Guidelines.

Cursor

must never

introduce

expensive rendering

without justification.

==============================================================================

14. STATE RULES
==============================================================================

Only

approved states

may exist.

Loading

Ready

Empty

Unavailable

Error

No additional

presentation states.

==============================================================================

15. TESTING RULES
==============================================================================

Every implementation

must include

required tests.

Implementation

without tests

is incomplete.

==============================================================================

16. CHANGE MANAGEMENT
==============================================================================

If

Specifications

and

existing implementation

conflict,

Cursor

must preserve

Specifications.

Cursor

must report

the conflict.

Cursor

must not

silently redesign.

==============================================================================

17. UNKNOWN REQUIREMENTS
==============================================================================

If

a requirement

is not documented,

Cursor

must

STOP.

Cursor

must request

clarification.

Cursor

must never

guess.

==============================================================================

18. REVIEW CHECKLIST
==============================================================================

Before completion,

Cursor

must verify

Reading Order

↓

Hierarchy

↓

Binding

↓

Components

↓

Design Tokens

↓

Accessibility

↓

Performance

↓

Testing

==============================================================================

19. REQUIRED OUTPUT
==============================================================================

Every implementation

must provide

Summary

↓

Files Changed

↓

Specification References

↓

Tests Executed

↓

Known Limitations

↓

Next Steps

==============================================================================

20. TRACEABILITY
==============================================================================

Every source file

must reference

its governing

Specification.

Every Pull Request

must identify

affected

Specifications.

==============================================================================

21. FORBIDDEN PRACTICES
==============================================================================

Cursor

must never

✗ Guess missing UI.

✗ Invent business logic.

✗ Merge unrelated components.

✗ Rename architecture layers.

✗ Ignore Blueprint.

✗ Ignore Binding Contracts.

✗ Change Information Architecture.

✗ Hide implementation assumptions.

==============================================================================

22. IMPLEMENTATION QUALITY LEVELS
==============================================================================

IQ-1

Compiles

--------------------------------------------------

IQ-2

Tests Pass

--------------------------------------------------

IQ-3

Specification Compliant

--------------------------------------------------

IQ-4

Architecturally Correct

--------------------------------------------------

IQ-5

Commercial UI V3 Certified

Target Level

IQ-5

==============================================================================

23. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Blueprint preserved.

✓ Reading Journey preserved.

✓ Component Architecture preserved.

✓ Binding preserved.

✓ Design Tokens preserved.

✓ Accessibility preserved.

✓ Performance preserved.

✓ Tests executed.

✓ Specification references included.

FAIL

✗ Design decisions by Cursor.

✗ Missing specification references.

✗ Changed hierarchy.

✗ Changed navigation.

✗ Changed reading order.

✗ Hardcoded UI.

✗ Unapproved components.

==============================================================================

24. IMPLEMENTATION NOTES
==============================================================================

This document defines

the operating rules

for AI Coding Assistants.

It does NOT define

Product Vision,

Design,

Business Logic,

or

Architecture.

==============================================================================

25. FINAL DECLARATION
==============================================================================

Commercial UI V3

is

Specification Driven.

Cursor

exists

to implement

approved specifications.

Cursor

does not

reinterpret

Specifications.

==============================================================================

26. FREEZE
==============================================================================

After approval,

this document

becomes

the canonical

AI implementation policy

for Commercial UI V3.

Every AI-assisted implementation

must comply

before

code review,

QA,

and

production release.

# ============================================================================
# END OF DOCUMENT
# ============================================================================