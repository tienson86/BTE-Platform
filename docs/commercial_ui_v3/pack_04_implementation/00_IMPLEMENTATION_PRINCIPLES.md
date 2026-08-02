# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 04 — IMPLEMENTATION SPECIFICATION
# 00_IMPLEMENTATION_PRINCIPLES.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : CRITICAL

------------------------------------------------------------------------------

# PURPOSE

This document defines

the implementation constitution

of Commercial UI V3.

Every implementation decision

must comply

with these principles.

------------------------------------------------------------------------------

# PRINCIPLE 1

Specification First

Implementation follows

Specification.

Never the opposite.

------------------------------------------------------------------------------

# PRINCIPLE 2

Presentation Layer

must never

contain

Business Logic.

UI displays.

Engine calculates.

------------------------------------------------------------------------------

# PRINCIPLE 3

No Component

may perform

business inference.

Components

render only.

------------------------------------------------------------------------------

# PRINCIPLE 4

No Screen

may access

Rule Database

directly.

Only View Models

may be consumed.

------------------------------------------------------------------------------

# PRINCIPLE 5

No Component

may call

Analysis Engine

directly.

Data arrives

through

Binding Contracts.

------------------------------------------------------------------------------

# PRINCIPLE 6

No Component

may mutate

incoming payload.

Payload

is immutable.

------------------------------------------------------------------------------

# PRINCIPLE 7

Every Screen

owns

one responsibility.

Screen

must not

render

other screen logic.

------------------------------------------------------------------------------

# PRINCIPLE 8

Every Component

owns

one responsibility.

Avoid

multi-purpose components.

------------------------------------------------------------------------------

# PRINCIPLE 9

Every Component

must consume

one View Model.

Never

multiple unrelated payloads.

------------------------------------------------------------------------------

# PRINCIPLE 10

Reading Order

is immutable.

UI

must never

reorder sections.

------------------------------------------------------------------------------

# PRINCIPLE 11

Information Hierarchy

is immutable.

Presentation

may adapt.

Priority

never changes.

------------------------------------------------------------------------------

# PRINCIPLE 12

Binding Contract

is immutable.

UI

must never

derive

missing values.

------------------------------------------------------------------------------

# PRINCIPLE 13

Unavailable

means

Unavailable.

Never

guess.

Never

invent.

Never

rewrite.

------------------------------------------------------------------------------

# PRINCIPLE 14

Design Tokens

are

the only

visual source

of truth.

Hardcoded

spacing,

colors,

radius,

typography

are forbidden.

------------------------------------------------------------------------------

# PRINCIPLE 15

Every Style

must map

to

Design Tokens.

------------------------------------------------------------------------------

# PRINCIPLE 16

Every Screen

must be

Responsive

without

changing

Business Meaning.

------------------------------------------------------------------------------

# PRINCIPLE 17

Accessibility

is mandatory.

Never optional.

------------------------------------------------------------------------------

# PRINCIPLE 18

Performance

must be considered

during implementation,

not

after implementation.

------------------------------------------------------------------------------

# PRINCIPLE 19

Testing

is part

of implementation.

Implementation

without tests

is incomplete.

------------------------------------------------------------------------------

# PRINCIPLE 20

Cursor

is

an implementation assistant.

Cursor

must never

become

a product designer.

------------------------------------------------------------------------------

# PRINCIPLE 21

Allowed Changes

Cursor MAY

Implement Components

Implement CSS

Implement Layout

Implement Animation

Implement Accessibility

Implement Responsive Behaviour

Implement Tests

only

when explicitly defined

by the specifications.

------------------------------------------------------------------------------

# PRINCIPLE 22

Forbidden Changes

Cursor SHALL NOT

Change Reading Order

Change Information Hierarchy

Change Typography Scale

Change Grid System

Change Design Tokens

Change Business Components

Change Navigation

Change Binding Contracts

Change Screen Structure

Change Product Behaviour

without

an updated specification.

------------------------------------------------------------------------------

# PRINCIPLE 23

Implementation Flow

Specification

↓

View Model

↓

Binding

↓

Component

↓

Design Tokens

↓

Rendered UI

No shortcuts.

------------------------------------------------------------------------------

# PRINCIPLE 24

Review Order

Product Review

↓

Architecture Review

↓

Implementation Review

↓

QA Review

↓

Release

Implementation

must never

skip

earlier review stages.

------------------------------------------------------------------------------

# PRINCIPLE 25

Acceptance Rule

An implementation

is considered complete

only when

Business Goals

Reading Goals

Binding Contracts

Accessibility

Performance

Responsive Behaviour

Testing

all satisfy

their corresponding specifications.

------------------------------------------------------------------------------

# FINAL DECLARATION

Commercial UI V3

is

Specification Driven.

The implementation

exists

to realize

the specification,

not

to reinterpret it.

------------------------------------------------------------------------------

# FREEZE

This document

is the highest-priority

implementation rule

within Commercial UI V3.

Every subsequent document

in Pack 04

inherits

these principles.

# ============================================================================
# END OF DOCUMENT
# ============================================================================