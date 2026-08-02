# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 04 — IMPLEMENTATION SPECIFICATION
# 10_CODING_CONVENTIONS.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : HIGH

Related Documents

- 00_IMPLEMENTATION_PRINCIPLES.md
- 01_FOLDER_STRUCTURE.md
- 02_COMPONENT_ARCHITECTURE.md
- 03_DATA_BINDING.md

==============================================================================
1. PURPOSE
==============================================================================

This document defines

the canonical coding conventions

for Commercial UI V3.

Coding conventions

exist to ensure

consistency,

readability,

maintainability,

and

architectural integrity.

These conventions

apply to

all frontend source code.

==============================================================================

2. DESIGN GOALS
==============================================================================

Coding conventions provide

• Consistent code

• Predictable structure

• Easy reviews

• Easy onboarding

• Long-term maintainability

• Architecture preservation

==============================================================================

3. CODING PHILOSOPHY
==============================================================================

Readable

↓

Predictable

↓

Maintainable

↓

Optimized

Never

the opposite.

Code

is written

for people first,

computers second.

==============================================================================

4. GENERAL PRINCIPLES
==============================================================================

Every source file

must have

one responsibility.

Every function

must have

one purpose.

Every component

must have

one owner.

==============================================================================

5. FILE ORGANIZATION
==============================================================================

One file

↓

One primary export.

Avoid

multiple unrelated exports.

File length

should remain

reasonable.

Large files

must be

split

by responsibility.

==============================================================================

6. NAMING CONVENTIONS
==============================================================================

Components

PascalCase

Example

ExecutiveHero

--------------------------------------------------

Hooks

camelCase

Example

useExecutiveSummary

--------------------------------------------------

Variables

camelCase

--------------------------------------------------

Constants

UPPER_SNAKE_CASE

--------------------------------------------------

Types

PascalCase

--------------------------------------------------

CSS Variables

kebab-case

==============================================================================

7. IMPORT ORDER
==============================================================================

Imports

must follow

this order

Framework

↓

Third-party

↓

Application

↓

Business Components

↓

Shared Components

↓

Base Components

↓

Styles

Relative imports

must remain

minimal.

==============================================================================

8. EXPORT RULES
==============================================================================

Prefer

named exports.

Default exports

are discouraged

except

documented entry points.

==============================================================================

9. COMPONENT RULES
==============================================================================

Components

must remain

small,

focused,

and

predictable.

Business Components

must consume

View Models only.

==============================================================================

10. FUNCTION RULES
==============================================================================

Functions

should be

short.

Avoid

deep nesting.

Prefer

early return.

Avoid

side effects.

==============================================================================

11. STATE RULES
==============================================================================

State

must remain

local

unless

shared state

is required.

Derived state

must not

duplicate

source state.

==============================================================================

12. PROP RULES
==============================================================================

Props

must be

explicit.

Avoid

generic

data

objects.

Prefer

typed properties.

==============================================================================

13. TYPESCRIPT RULES
==============================================================================

Prefer

explicit types.

Avoid

implicit any.

Interfaces

must describe

business meaning,

not implementation details.

==============================================================================

14. COMMENTS
==============================================================================

Comments

must explain

Why,

not

What.

Remove

obsolete comments.

Avoid

commented-out code.

==============================================================================

15. ERROR HANDLING
==============================================================================

Errors

must be

handled explicitly.

Never

ignore exceptions.

Never

silently fail.

==============================================================================

16. ASYNC CODE
==============================================================================

Async code

must be

predictable.

Avoid

nested promises.

Prefer

async / await.

==============================================================================

17. STYLING RULES
==============================================================================

Components

must consume

Design Tokens.

Inline styles

are forbidden

except

documented exceptions.

==============================================================================

18. ACCESSIBILITY
==============================================================================

Accessibility

must be

implemented

during coding.

Never

postponed.

==============================================================================

19. TESTABILITY
==============================================================================

Code

must be

easy to test.

Avoid

hidden dependencies.

Avoid

global mutations.

==============================================================================

20. FORBIDDEN PRACTICES
==============================================================================

Commercial UI V3

must never

✗ Hardcode business values.

✗ Duplicate logic.

✗ Parse payload in Components.

✗ Mix presentation and business logic.

✗ Create God Components.

✗ Create God Hooks.

✗ Use magic numbers.

✗ Leave dead code.

✗ Leave TODO before release.

==============================================================================

21. CODE REVIEW CHECKLIST
==============================================================================

Every Pull Request

must verify

Architecture

↓

Naming

↓

Binding

↓

Styling

↓

Accessibility

↓

Performance

↓

Tests

↓

Specification Compliance

==============================================================================

22. TRACEABILITY
==============================================================================

Every source file

must be traceable

to

one

Specification.

Every component

must map

to

one Screen Specification.

Every style

must map

to

one Design Token.

==============================================================================

23. QUALITY METRICS
==============================================================================

Code

should exhibit

High cohesion

Low coupling

Clear ownership

Predictable dependencies

Minimal duplication

==============================================================================

24. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Naming conventions followed.

✓ Imports ordered.

✓ Small components.

✓ Explicit typing.

✓ Testable code.

✓ Architecture preserved.

✓ Specification traceable.

FAIL

✗ Mixed responsibilities.

✗ Circular imports.

✗ Dead code.

✗ Hidden dependencies.

✗ Hardcoded values.

✗ Specification violations.

==============================================================================

25. IMPLEMENTATION NOTES
==============================================================================

This specification defines

Coding Style

Naming

Structure

Review Standards

Quality Expectations

It does NOT define

language syntax,

framework APIs,

or formatter configuration.

==============================================================================

26. FUTURE EXTENSIONS
==============================================================================

Commercial UI V3

may support

Automated Style Enforcement

Architecture Linting

Specification-aware Reviews

AI-assisted Refactoring

provided

the coding conventions

remain unchanged.

==============================================================================

27. FREEZE
==============================================================================

After approval,

Coding Conventions

become

the canonical

frontend coding standard

for Commercial UI V3.

Every implementation

must comply

before

code review

and

production release.

# ============================================================================
# END OF DOCUMENT
# ============================================================================