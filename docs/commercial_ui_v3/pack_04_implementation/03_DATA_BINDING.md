# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 04 — IMPLEMENTATION SPECIFICATION
# 03_DATA_BINDING.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : CRITICAL

Related Documents

- 00_IMPLEMENTATION_PRINCIPLES.md
- 01_FOLDER_STRUCTURE.md
- 02_COMPONENT_ARCHITECTURE.md
- Pack 03 Screen Specifications

==============================================================================
1. PURPOSE
==============================================================================

This document defines

the canonical data binding architecture

for Commercial UI V3.

Data Binding separates

Business Data

from

Presentation.

UI components

never consume

raw payloads.

==============================================================================

2. DESIGN GOALS
==============================================================================

The Binding Layer provides

• Stable UI contracts

• Payload isolation

• Predictable rendering

• Easy testing

• Backend independence

==============================================================================

3. BINDING PHILOSOPHY
==============================================================================

Commercial UI V3

implements

One-way Data Flow.

Payload

↓

Adapter

↓

View Model

↓

Component

↓

Rendered UI

No shortcuts.

==============================================================================

4. CANONICAL DATA FLOW
==============================================================================

Analysis Engine

↓

API Response

↓

Binding Adapter

↓

View Model

↓

Business Component

↓

Shared Component

↓

Base Component

==============================================================================

5. RAW PAYLOAD
==============================================================================

Raw payload

belongs

to

Backend.

UI

must never

depend directly

on payload structure.

==============================================================================

6. ADAPTER LAYER
==============================================================================

Adapters transform

payload

into

stable View Models.

Responsibilities

• Mapping

• Formatting

• Normalization

• Default values

Adapters never

render UI.

==============================================================================

7. VIEW MODEL LAYER
==============================================================================

View Models

represent

UI-ready data.

They contain

only

presentation-ready values.

No backend structure

is exposed.

==============================================================================

8. COMPONENT LAYER
==============================================================================

Components consume

View Models only.

Components

must never

inspect

payload fields.

==============================================================================

9. BINDING OWNERSHIP
==============================================================================

Every Screen

owns

exactly one

Binding Adapter.

Every Business Component

consumes

exactly one

View Model.

==============================================================================

10. BINDING EXAMPLE
==============================================================================

Backend Payload

↓

report.summary

↓

ExecutiveSummaryAdapter

↓

ExecutiveSummaryViewModel

↓

ExecutiveHero

↓

Rendered UI

==============================================================================

11. VIEW MODEL CONTRACT
==============================================================================

Every View Model

must be

Complete

Immutable

Predictable

Presentation-oriented

Components

must never

modify

View Models.

==============================================================================

12. NORMALIZATION RULES
==============================================================================

Adapters normalize

Missing values

↓

Unavailable

Empty arrays

↓

Empty collections

Formatting

↓

Presentation format

Localization keys

↓

Localized text

==============================================================================

13. FORBIDDEN TRANSFORMATIONS
==============================================================================

Components

must never

• Parse payload

• Format dates

• Calculate metrics

• Infer conclusions

• Build recommendations

• Join business strings

These belong

to

Adapters

or

Backend.

==============================================================================

14. BINDING STATES
==============================================================================

Every View Model

supports

Loading

↓

Ready

↓

Unavailable

↓

Empty

↓

Error

State behavior

is identical

across all screens.

==============================================================================

15. REQUIRED VIEW MODELS
==============================================================================

ExecutiveSummaryViewModel

FourPillarsViewModel

ExecutiveInsightViewModel

MetricsViewModel

AnalysisViewModel

ConsultationReportViewModel

AppendixViewModel

NavigationViewModel

==============================================================================

16. OPTIONAL VIEW MODELS
==============================================================================

TooltipViewModel

ReferenceViewModel

EvidenceViewModel

CitationViewModel

GlossaryViewModel

ConfidenceViewModel

==============================================================================

17. FIELD OWNERSHIP
==============================================================================

Each UI field

must originate

from

exactly one

View Model property.

Multiple ownership

is forbidden.

==============================================================================

18. MISSING DATA
==============================================================================

Missing values

must become

Unavailable.

Never

null

undefined

NaN

empty strings

inside Components.

==============================================================================

19. LOCALIZATION
==============================================================================

Localization

occurs

before

rendering.

Components

consume

localized text.

Never

raw i18n keys.

==============================================================================

20. BINDING VALIDATION
==============================================================================

Adapters

must validate

Required fields

Optional fields

Data types

State consistency

Invalid payloads

must never

reach Components.

==============================================================================

21. ERROR HANDLING
==============================================================================

Binding errors

remain

inside

Binding Layer.

Components

receive

only

Error State View Models.

==============================================================================

22. PERFORMANCE
==============================================================================

Binding

executes

once

per payload.

Components

must not

repeat

transformations.

==============================================================================

23. TESTABILITY
==============================================================================

Every Adapter

must have

unit tests.

Every View Model

must have

contract tests.

Every Screen

must have

binding integration tests.

==============================================================================

24. TRACEABILITY
==============================================================================

Every View Model

must map

to

one Screen Specification.

Every field

must map

to

one Binding Contract.

Traceability

must be

bidirectional.

==============================================================================

25. DEPENDENCY RULES
==============================================================================

Allowed

Payload

↓

Adapter

↓

View Model

↓

Component

Forbidden

Component

↓

Payload

Component

↓

API

Component

↓

Rule Database

==============================================================================

26. ANTI-PATTERNS
==============================================================================

Commercial UI V3 must never

✗ Read payload inside Components.

✗ Parse JSON during rendering.

✗ Build business sentences.

✗ Perform calculations.

✗ Hide binding failures.

✗ Couple UI to backend models.

==============================================================================

27. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Components consume only View Models.

✓ One-way data flow.

✓ Stable Binding Contracts.

✓ Payload isolated.

✓ Missing data normalized.

✓ View Models immutable.

FAIL

✗ Components inspect payload.

✗ Backend changes break UI.

✗ Binding duplicated.

✗ Business logic inside Components.

==============================================================================

28. IMPLEMENTATION NOTES
==============================================================================

This specification defines

Binding Architecture

Adapters

View Models

Normalization

Validation

State Handling

It does NOT define

API implementation

Backend models

Database schemas

Business rules.

==============================================================================

29. FUTURE EXTENSIONS
==============================================================================

The Binding Layer

may support

Caching

Lazy Binding

Incremental Updates

Streaming View Models

Offline Synchronization

provided

the Binding Contract

remains unchanged.

==============================================================================

30. FREEZE
==============================================================================

After approval,

Data Binding

becomes

the canonical

presentation data architecture

for Commercial UI V3.

Every implementation

must preserve

One-way Data Flow

Binding Contracts

View Model isolation

Normalization

and

Presentation independence.

# ============================================================================
# END OF DOCUMENT
# ============================================================================