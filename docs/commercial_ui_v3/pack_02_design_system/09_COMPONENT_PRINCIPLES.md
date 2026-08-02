# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 02 — DESIGN SYSTEM
# 09_COMPONENT_PRINCIPLES.md
# ============================================================================
#
# Version : 1.0.0
# Status  : Foundation (Freeze Candidate)
# Owner   : Product Architecture
#
# This document defines the ONLY accepted Component Principles
# for Commercial UI V3.
#
# It does NOT define individual components.
#
# It defines how components are created.
#
# ============================================================================

# 1. PURPOSE

Commercial UI V3 does not build interfaces
from components.

Commercial UI V3 builds components
from Design System primitives.

Components are outputs.

Never inputs.

------------------------------------------------------------------------------

# 2. DESIGN PHILOSOPHY

Every component exists
for one purpose only:

Helping users understand
their BaZi consultation.

Components never exist

for decoration,

for showcasing technology,

or

for filling space.

------------------------------------------------------------------------------

# 3. COMPONENT HIERARCHY

Commercial UI V3 defines
four component layers.

Layer 1

Primitive

↓

Layer 2

Composite

↓

Layer 3

Business

↓

Layer 4

Screen

Only lower layers
may depend
on higher layers.

Never reverse.

------------------------------------------------------------------------------

# 4. PRIMITIVE COMPONENTS

Primitive Components
are generic UI building blocks.

Examples

Typography

Divider

Icon

Badge

Label

Button

Input

Tooltip

Spinner

These components
contain no business knowledge.

------------------------------------------------------------------------------

# 5. COMPOSITE COMPONENTS

Composite Components
combine primitives.

Examples

Metric Row

Callout

Section Header

Evidence Row

Reading Progress

Search Field

Accordion

These components
still contain
no BaZi knowledge.

------------------------------------------------------------------------------

# 6. BUSINESS COMPONENTS

Business Components
represent domain concepts.

Examples

Executive Hero

Four Pillars

Element Distribution

Strength Gauge

Analysis Block

Interpretation Chapter

Knowledge Block

Business Components
consume business payloads.

------------------------------------------------------------------------------

# 7. SCREEN COMPONENTS

Screens assemble

Business Components

into complete reading experiences.

Examples

Result Report

Knowledge Workspace

Discussion

Print Report

Screen Components
never duplicate business logic.

------------------------------------------------------------------------------

# 8. COMPONENT COMPOSITION

Every Component
must be composed from

Visual Language

↓

Design Tokens

↓

Grid

↓

Spacing

↓

Typography

↓

Color

↓

Surface

↓

Motion

↓

Primitive Components

↓

Composite Components

↓

Business Components

No layer
may be skipped.

------------------------------------------------------------------------------

# 9. SINGLE RESPONSIBILITY

Every component
must answer
one question only.

Examples

Executive Hero

"What is my chart?"

--------------------------------------------------

Analysis Block

"Why?"

--------------------------------------------------

Knowledge Block

"What is the evidence?"

If a component
answers multiple questions,

split it.

------------------------------------------------------------------------------

# 10. COMPONENT CONTRACT

Every Component
must define

Purpose

↓

Inputs

↓

Outputs

↓

States

↓

Accessibility

↓

Dependencies

↓

Design Tokens

No component
may exist
without a contract.

------------------------------------------------------------------------------

# 11. COMPONENT STATES

Every component
must support

Default

↓

Loading

↓

Unavailable

↓

Empty

↓

Error

↓

Disabled (if applicable)

Missing data
must never break layout.

------------------------------------------------------------------------------

# 12. COMPONENT BINDING

Business Components
consume

Binding Index

only.

They never calculate
business values.

They never infer
missing values.

Presentation only.

------------------------------------------------------------------------------

# 13. COMPONENT REUSE

Every component
must be reusable.

Duplicate implementations
are forbidden.

Variation
is achieved by

configuration,

never duplication.

------------------------------------------------------------------------------

# 14. COMPONENT ACCESSIBILITY

Every component
must support

Keyboard navigation.

Screen readers.

Visible focus.

Semantic HTML.

Accessible labels.

Accessibility
is mandatory.

------------------------------------------------------------------------------

# 15. COMPONENT PERFORMANCE

Components
must remain

Lightweight.

Lazy-load
where appropriate.

Avoid unnecessary
re-rendering.

Motion
must not reduce performance.

------------------------------------------------------------------------------

# 16. COMPONENT TOKENS

Components
consume only

Semantic Tokens.

Examples

Typography Tokens

Spacing Tokens

Color Tokens

Surface Tokens

Motion Tokens

Grid Tokens

Components
must never
hardcode visual values.

------------------------------------------------------------------------------

# 17. IMPLEMENTATION RULES

Frontend SHALL NOT

Invent components.

Merge unrelated responsibilities.

Duplicate business logic.

Embed API logic.

Embed calculation logic.

Embed Rule Engine logic.

Components
render only.

------------------------------------------------------------------------------

# 18. COMPONENT ANTI-PATTERNS

Commercial UI V3
must never contain

God Components.

Massive Components.

Nested Cards.

Deep Component Trees.

Business Logic
inside UI.

Random Visual Styles.

Components
must remain predictable.

------------------------------------------------------------------------------

# 19. COMPONENT LIFECYCLE

Design System

↓

Primitive

↓

Composite

↓

Business

↓

Screen

↓

Application

Every component
follows this lifecycle.

------------------------------------------------------------------------------

# 20. COMPONENT GOVERNANCE

Every new component
requires

Business justification.

Design review.

Accessibility review.

Token compliance.

Reuse evaluation.

Only then
may it enter
the Design System.

------------------------------------------------------------------------------

# 21. ACCEPTANCE CRITERIA

Component Principles
pass only when

✓ Every component
has one responsibility.

✓ Every component
consumes Design Tokens.

✓ No business logic
exists inside UI.

✓ Components
remain reusable.

✓ Screens
assemble components
instead of reinventing them.

------------------------------------------------------------------------------

# 22. FREEZE

After approval,

Component Principles
become immutable.

Every future component
must comply
with this specification.

No implementation
may bypass
the Design System.

# ============================================================================
# END OF DOCUMENT
# ============================================================================