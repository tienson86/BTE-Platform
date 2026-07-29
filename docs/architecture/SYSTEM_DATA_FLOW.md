# SYSTEM_DATA_FLOW.md

---

# Part 1 — Foundation

## 1. Document Information

| Item | Value |
|------|-------|
| Document | SYSTEM_DATA_FLOW.md |
| Project | BTE Platform |
| Version | 1.0 |
| Status | Architecture Contract |
| Owner | BTE Platform Architecture |
| Scope | Entire Platform |
| Last Updated | TBD |

---

## 2. Purpose

This document defines the official end-to-end data flow of the BTE Platform.

It serves as the single architectural reference describing how data is produced, transformed, transferred, consumed, and rendered across all platform modules.

This document is an Architecture Contract rather than an implementation document.

If implementation differs from this document, the implementation should be reviewed and corrected unless an approved architectural change has been made.

---

## 3. Design Principles

### 3.1 Single Source of Truth (SSOT)

Each business field must have exactly one official producer.

A field may have multiple consumers but must never have multiple authoritative producers.

Example:

- `dung_than` → Producer: Pattern Engine
- `strength.level` → Producer: Score Engine
- `solar_term` → Producer: Calendar Engine

---

### 3.2 One-Way Data Flow

Data always flows forward.

Input

↓

Calendar

↓

Bazi

↓

Pattern

↓

RuleContext

↓

Score

↓

Knowledge Matching

↓

Priority Resolution

↓

Interpretation

↓

Report

↓

Portal

Backward modification of upstream data is prohibited except through explicitly defined synchronization mechanisms.

---

### 3.3 Engine Responsibility

Each Engine owns one responsibility only.

Examples:

Calendar Engine

Responsible for:

- Calendar conversion
- Solar term
- Can Chi calculation

Not responsible for:

- Pattern
- Useful God
- Interpretation

Pattern Engine

Responsible for:

- Pattern detection
- Useful God
- Follow Pattern
- Temperature state

Not responsible for:

- Report rendering
- HTML
- Narrative generation

---

### 3.4 Immutable Pipeline Contract

Once data leaves an Engine, downstream Engines must treat it as immutable.

Derived fields shall be added through dedicated output models rather than modifying upstream source objects.

---

### 3.5 Separation of Concerns

The platform is divided into five logical layers:

1. Input Layer
2. Calculation Layer
3. Knowledge Layer
4. Interpretation Layer
5. Presentation Layer

Each layer communicates only through defined contracts.

No Presentation component may directly perform business calculations.

No Knowledge component may directly render user interfaces.

---

## 4. Overall Architecture

The BTE Platform consists of multiple independent Engines connected through a single forward-only processing pipeline.

Each Engine produces a well-defined output model.

Each downstream Engine consumes only published outputs.

Direct cross-layer access is prohibited unless explicitly documented.

The Rule Database is considered passive knowledge.

Business decisions are made by Engines, not by the database itself.

---

End of Part 1
---

# Part 2 — High-Level Data Flow

## 5. High-Level Data Flow

The BTE Platform follows a single forward-only processing pipeline.

Each Engine receives a well-defined input model, performs one business responsibility, and produces a standardized output model for downstream Engines.

No Engine may directly modify data owned by an upstream Engine.

---

### 5.1 Overall Processing Pipeline

```text
User Input
    │
    ▼
Input Layer
    │
    ▼
Calendar Engine
    │
    ▼
Bazi Engine
    │
    ▼
Feng Shui Engine (Optional)
    │
    ▼
Pattern Engine
    │
    ▼
RuleContext Builder
    │
    ▼
Score Engine
    │
    ▼
Knowledge Loader
    │
    ▼
Rule Matcher
    │
    ▼
Priority Resolution
    │
    ▼
Interpretation Engine
    │
    ▼
Report Engine
    │
    ▼
Portal / API / Export
```

---

### 5.2 Layer Responsibilities

| Layer | Responsibility |
|--------|----------------|
| Input Layer | Receive and validate user input |
| Calendar Engine | Calendar conversion and Solar Term calculation |
| Bazi Engine | Build Four Pillars and core BaZi data |
| Feng Shui Engine | Produce Feng Shui related calculations (optional pipeline) |
| Pattern Engine | Determine Strength, Pattern, Useful God, Follow Pattern and related business fields |
| RuleContext Builder | Consolidate runtime business context |
| Score Engine | Produce standardized scoring results |
| Knowledge Layer | Load and organize runtime knowledge |
| Rule Matching Layer | Match rules against RuleContext |
| Priority Resolution | Resolve rule conflicts |
| Interpretation Layer | Generate structured interpretation |
| Report Layer | Render report output |
| Portal Layer | Present results to end users or APIs |

---

### 5.3 Forward-Only Rule

The processing pipeline is strictly forward-only.

Allowed:

Input → Calendar → Bazi → Pattern → RuleContext → Score → Knowledge → Interpretation → Report

Not Allowed:

- Report modifying Pattern
- Interpretation modifying Calendar
- Knowledge modifying Bazi
- Portal modifying RuleContext

---

### 5.4 Engine Independence

Each Engine is independently testable.

Each Engine shall expose:

- Input Model
- Output Model
- Public Interface
- Error Contract

An Engine must not depend on the internal implementation details of downstream Engines.

---

### 5.5 Data Contract

Every transition between two Engines shall use a documented data contract.

The contract defines:

- Required fields
- Optional fields
- Field ownership
- Validation rules
- Version compatibility

No downstream Engine may assume undocumented fields.

---

### 5.6 Pipeline Guarantees

The platform guarantees that:

- Calendar data is finalized before BaZi calculation.
- BaZi data is finalized before Pattern analysis.
- Pattern analysis is finalized before Rule Matching.
- Rule Matching is finalized before Interpretation.
- Interpretation is finalized before Report generation.

This execution order is mandatory and must not be bypassed.

---

End of Part 2
---

# Part 3 — Engine Data Ownership

## 6. Engine Ownership Principles

Each Engine owns a well-defined business domain.

Ownership includes:

- Producing business data
- Maintaining data consistency
- Publishing standardized output
- Guaranteeing output validity

An Engine shall never overwrite fields owned by another Engine.

---

## 6.1 Input Layer

### Responsibility

Receive raw user input and normalize request data.

### Input

- User Request
- Birth Information
- Configuration
- Runtime Options

### Output

- InputRequest

### Producer

- Portal
- API
- CLI

### Consumer

- Calendar Engine

### Owns

- Request metadata
- Input validation status
- User timezone
- Calendar type
- Runtime configuration

---

## 6.2 Calendar Engine

### Responsibility

Convert raw calendar information into standardized calendar data.

### Input

InputRequest

### Output

CalendarContext

### Producer

Calendar Engine

### Consumer

- Bazi Engine
- Feng Shui Engine

### SSOT Fields

Calendar Engine is the only authoritative producer of:

- Gregorian Date
- Lunar Date
- Julian Day
- Solar Term
- Solar Term Index
- Year Stem Branch
- Month Stem Branch
- Day Stem Branch
- Hour Stem Branch
- Leap Month
- Calendar Metadata

No downstream Engine may modify these fields.

---

## 6.3 Bazi Engine

### Responsibility

Construct complete Four Pillars and all derived BaZi structures.

### Input

CalendarContext

### Output

BaziContext

### Consumer

- Pattern Engine
- Score Engine
- Interpretation Engine

### SSOT Fields

Only Bazi Engine owns:

- Four Pillars
- Heavenly Stems
- Earthly Branches
- Hidden Stems
- Ten Gods
- Twelve Growth Stages
- Na Yin
- Five Element Distribution
- Pillar Relationships
- Branch Combinations
- Branch Clashes
- Stem Combinations

---

## 6.4 Feng Shui Engine

### Responsibility

Produce Feng Shui related calculations independent of BaZi interpretation.

### Input

CalendarContext

### Output

FengShuiContext

### Consumer

- Report
- Portal
- API

### SSOT Fields

- Flying Star
- Nine Palace
- Eight Mansions
- Trigram
- Direction
- House Gua
- Person Gua
- Feng Shui Metadata

This Engine is optional and does not participate in the BaZi interpretation pipeline.

---

## 6.5 Pattern Engine

### Responsibility

Determine the complete business pattern of the BaZi chart.

This Engine represents the business intelligence core of the platform.

### Input

BaziContext

### Output

PatternContext

### Consumer

- RuleContext Builder
- Score Engine
- Interpretation Engine

### SSOT Fields

Only Pattern Engine owns:

- Strength Type
- Pattern
- Follow Pattern
- Tong Cach
- Useful God (Dung Than)
- Favorable Gods (Hy Than)
- Unfavorable Gods (Ky Than)
- Temperature Status
- Special Structures
- Combination Summary
- Pattern Metadata

No other Engine may calculate or overwrite these fields.

---

## 6.6 RuleContext Builder

### Responsibility

Merge all upstream runtime information into one unified business context.

### Input

- CalendarContext
- BaziContext
- PatternContext

### Output

RuleContext

### Consumer

- Knowledge Loader
- Rule Matcher
- Priority Engine

### Owns

RuleContext does not create business facts.

It only consolidates existing data.

RuleContext is therefore a transport model rather than a business model.

---

## 6.7 Score Engine

### Responsibility

Calculate standardized scoring values.

### Input

- BaziContext
- PatternContext

### Output

ScoreContext

### Consumer

- Interpretation Engine
- Report Engine

### SSOT Fields

Only Score Engine owns:

- Overall Score
- Strength Score
- Pattern Score
- Useful God Score
- Combination Score
- Temperature Score
- Luck Score
- Final Weighted Score

Score values are immutable after publication.

---

End of Part 3
---

# Part 4 — Knowledge & Presentation Layer Ownership

## 6.8 Knowledge Loader

### Responsibility

Load runtime knowledge from the Knowledge Base into memory.

The Knowledge Loader is responsible only for loading and organizing knowledge.

It shall never evaluate business logic or perform rule matching.

### Input

- RuleContext
- Knowledge Repository

### Output

KnowledgeContext

### Consumer

- Rule Matcher

### Owns

Knowledge Loader owns:

- Loaded Rule Sets
- Rule Index
- Rule Metadata
- Rule Cache
- Runtime Knowledge Snapshot

### Architectural Constraints

Knowledge Loader shall not:

- Modify RuleContext
- Evaluate rule conditions
- Resolve rule conflicts
- Generate interpretations

---

## 6.9 Rule Matcher

### Responsibility

Evaluate RuleContext against loaded runtime knowledge.

The Rule Matcher determines which rules are applicable for the current chart.

### Input

- RuleContext
- KnowledgeContext

### Output

MatchedRuleSet

### Consumer

- Priority Resolution Engine

### SSOT Fields

Only Rule Matcher owns:

- Matched Rules
- Rule Match Result
- Match Score
- Match Metadata
- Triggered Conditions

### Architectural Constraints

Rule Matcher shall not:

- Resolve rule conflicts
- Generate interpretation
- Render sentences
- Modify business data

---

## 6.10 Priority Resolution Engine

### Responsibility

Resolve conflicts between matched rules according to the Priority Rule Database.

The output of this Engine represents the final executable rule set.

### Input

MatchedRuleSet

### Output

ResolvedRuleSet

### Consumer

- Interpretation Engine

### SSOT Fields

Only Priority Resolution owns:

- Winning Rules
- Suppressed Rules
- Conflict Resolution Result
- Rule Priority Decision
- Resolution Metadata

### Architectural Constraints

Priority Resolution shall never:

- Recalculate business facts
- Modify PatternContext
- Modify ScoreContext
- Modify RuleContext

---

## 6.11 Interpretation Engine

### Responsibility

Transform structured business data into structured interpretations.

Interpretation Engine consumes runtime data and selected rules to produce domain interpretations.

It is not responsible for formatting or presentation.

### Input

- RuleContext
- PatternContext
- ScoreContext
- ResolvedRuleSet

### Output

InterpretationResult

### Consumer

- Report Engine
- API
- Portal

### SSOT Fields

Only Interpretation Engine owns:

- Interpretation Sections
- Interpretation Paragraphs
- Interpretation Metadata
- Structured Conclusions
- Interpretation Confidence

### Architectural Constraints

Interpretation Engine shall not:

- Calculate BaZi
- Calculate Scores
- Evaluate Rules
- Render HTML
- Generate PDF

---

## 6.12 Report Engine

### Responsibility

Render structured interpretation into user-facing outputs.

Report Engine is responsible only for presentation.

### Input

- InterpretationResult
- Report Template
- Theme Configuration

### Output

ReportDocument

### Consumer

- Portal
- API
- Export Service

### SSOT Fields

Only Report Engine owns:

- HTML Output
- PDF Output
- DOCX Output
- Print Layout
- Report Metadata

### Architectural Constraints

Report Engine shall never:

- Calculate business data
- Modify InterpretationResult
- Execute Knowledge Rules
- Resolve Priorities

---

## 6.13 Portal Layer

### Responsibility

Deliver reports and runtime services to end users.

Portal represents the presentation entry point of the platform.

### Input

- ReportDocument
- API Response
- Runtime Status

### Output

- Web UI
- Mobile UI
- REST API
- Export Download

### Owns

Portal owns:

- Session State
- User Interaction
- Display Preferences
- Authentication Context

### Architectural Constraints

Portal shall never:

- Execute business rules
- Perform BaZi calculations
- Generate interpretation
- Modify runtime data

---

## 6.14 End-to-End Ownership Summary

The ownership of business data across the platform is summarized below.

| Engine | Owns Business Data | Owns Presentation | Owns Runtime Logic |
|---------|-------------------|-------------------|--------------------|
| Input Layer | No | No | No |
| Calendar Engine | Yes | No | Yes |
| Bazi Engine | Yes | No | Yes |
| Feng Shui Engine | Yes | No | Yes |
| Pattern Engine | Yes | No | Yes |
| RuleContext Builder | No (Transport Only) | No | No |
| Score Engine | Yes | No | Yes |
| Knowledge Loader | No | No | Yes (Knowledge Loading Only) |
| Rule Matcher | Yes (Match Result) | No | Yes |
| Priority Resolution | Yes (Resolution Result) | No | Yes |
| Interpretation Engine | Yes (Interpretation) | No | Yes |
| Report Engine | No | Yes | No |
| Portal Layer | No | Yes | No |

---

## 6.15 Layer Isolation Rules

The following dependencies are mandatory:

- Calendar Engine shall not depend on Pattern Engine.
- Bazi Engine shall not depend on Interpretation Engine.
- Pattern Engine shall not depend on Report Engine.
- Rule Matcher shall not depend on Portal.
- Report Engine shall not depend on Knowledge Repository.
- Portal shall not call internal Engines directly.

Communication between layers shall occur only through published contracts.

---

End of Part 4
---

# Part 5 — Data Governance

## 7. Data Governance Overview

The BTE Platform follows a strict data governance model.

Every business field shall have:

- One authoritative producer (SSOT)
- Zero or more consumers
- A defined lifecycle
- A validation rule
- A version compatibility policy

Business fields are not allowed to exist without ownership.

---

# 7.1 Single Source of Truth (SSOT)

Each runtime field has exactly one authoritative producer.

Only the producer Engine may:

- Create the field
- Modify the field
- Correct the field
- Publish updates

All downstream Engines shall treat the field as read-only.

Example

Calendar Engine

↓

solar_term

↓

Read Only

↓

Bazi Engine

↓

Pattern Engine

↓

Interpretation Engine

---

# 7.2 Data Ownership Levels

Every runtime field belongs to one of four ownership levels.

| Level | Meaning |
|--------|---------|
| Level 1 | Raw Source Data |
| Level 2 | Calculated Business Data |
| Level 3 | Runtime Context |
| Level 4 | Presentation Data |

---

## Level 1

Produced by

- Input Layer
- Calendar Engine

Examples

- birth_date
- birth_time
- longitude
- latitude
- timezone
- lunar_date
- solar_term

---

## Level 2

Produced by

Business Engines.

Examples

- pillars
- hidden_stems
- ten_gods
- pattern
- useful_god
- favorable_god
- unfavorable_god
- shensha
- score

---

## Level 3

Produced by

Runtime Engines.

Examples

- RuleContext
- MatchedRuleSet
- ResolvedRuleSet
- RuntimeMetadata

---

## Level 4

Produced by

Presentation Layer.

Examples

- HTML
- PDF
- Markdown
- API Response
- Export

---

# 7.3 Read / Write Rules

Each Engine has one of three permissions.

| Permission | Meaning |
|------------|---------|
| Read | May consume data |
| Write | May produce owned data |
| None | No access |

Example

Pattern Engine

CalendarContext

Read

PatternContext

Write

ScoreContext

None

---

# 7.4 Immutable Runtime Fields

The following fields become immutable after publication.

CalendarContext

- lunar_date
- solar_term
- julian_day

BaziContext

- pillars
- hidden_stems
- ten_gods

PatternContext

- pattern
- follow_pattern
- useful_god
- favorable_god
- unfavorable_god

ScoreContext

- overall_score
- strength_score
- pattern_score

InterpretationResult

Entire object.

---

# 7.5 Synchronization Rules

Synchronization is allowed only between officially defined contexts.

Allowed

CalendarContext

↓

BaziContext

↓

PatternContext

↓

RuleContext

↓

ScoreContext

↓

InterpretationResult

Not Allowed

InterpretationResult

↓

PatternContext

ReportDocument

↓

RuleContext

Portal

↓

CalendarContext

---

# 7.6 Runtime Validation

Before an Engine publishes its output:

Validation must verify

Required Fields

Business Consistency

Data Type

Version Compatibility

Null Safety

Runtime Integrity

Publishing shall fail if validation fails.

---

# 7.7 Data Versioning

Each published context shall include

Context Version

Schema Version

Engine Version

Timestamp

Producer

Checksum (optional)

This allows backward compatibility between Engine versions.

---

# 7.8 Data Compatibility

Minor Version

May add optional fields.

Major Version

May change schema.

Breaking changes require

Migration Rules

Compatibility Layer

Documentation Update

Architecture Approval

---

# 7.9 Runtime Audit Requirements

Every published context shall be auditable.

Audit information includes

Producer Engine

Publish Time

Execution Duration

Validation Result

Pipeline Stage

Rule Count

Score Summary

Architecture Version

---

# 7.10 Architecture Compliance Rules

The following are considered Architecture Violations.

Multiple producers for one field.

Downstream Engine modifying upstream data.

Report Layer calculating business logic.

Knowledge Layer rendering HTML.

Portal bypassing Engine APIs.

Rule Matcher modifying RuleContext.

Priority Engine recalculating Pattern.

Any violation shall be treated as an implementation defect.

---

# 7.11 Governance Principles

The platform follows these governance principles.

Single Source of Truth

Forward-only Pipeline

Immutable Published Data

Layer Isolation

Explicit Ownership

Contract-first Development

Architecture before Implementation

Documentation drives Code

Code shall conform to Architecture.

Architecture shall not be changed to fit temporary implementation.

---

End of Part 5
---

# Part 6 — Architecture Contract & Compliance

## 8. Producer → Consumer Matrix

The following matrix defines the official ownership and consumption of all runtime contexts.

| Context | Producer | Primary Consumers |
|----------|----------|-------------------|
| InputRequest | Input Layer | Calendar Engine |
| CalendarContext | Calendar Engine | Bazi Engine, Feng Shui Engine |
| BaziContext | Bazi Engine | Pattern Engine, Score Engine |
| FengShuiContext | Feng Shui Engine | Report Engine, Portal |
| PatternContext | Pattern Engine | RuleContext Builder, Score Engine, Interpretation Engine |
| RuleContext | RuleContext Builder | Knowledge Loader, Rule Matcher |
| KnowledgeContext | Knowledge Loader | Rule Matcher |
| MatchedRuleSet | Rule Matcher | Priority Resolution |
| ResolvedRuleSet | Priority Resolution | Interpretation Engine |
| ScoreContext | Score Engine | Interpretation Engine, Report Engine |
| InterpretationResult | Interpretation Engine | Report Engine |
| ReportDocument | Report Engine | Portal, API, Export |

---

## 8.1 Runtime Pipeline Contract

The official execution sequence is fixed.

```text
Input
    │
    ▼
Calendar
    │
    ▼
Bazi
    │
    ▼
Feng Shui (Optional)
    │
    ▼
Pattern
    │
    ▼
RuleContext
    │
    ▼
Score
    │
    ▼
Knowledge Loader
    │
    ▼
Rule Matcher
    │
    ▼
Priority Resolution
    │
    ▼
Interpretation
    │
    ▼
Report
    │
    ▼
Portal
```

This execution order is mandatory.

No Engine may skip or reorder pipeline stages.

---

# 8.2 Pipeline Invariants

The following architectural rules are permanent.

Invariant 1

Calendar data shall always exist before BaZi calculation.

Invariant 2

BaZi shall always be finalized before Pattern analysis.

Invariant 3

Pattern shall always be finalized before Rule Matching.

Invariant 4

Rule Matching shall always complete before Priority Resolution.

Invariant 5

Priority Resolution shall always complete before Interpretation.

Invariant 6

Interpretation shall always complete before Report rendering.

Invariant 7

Report generation shall never change business data.

Invariant 8

Portal shall never execute business logic.

---

# 8.3 Runtime Dependency Rules

Each Engine depends only on upstream published contracts.

Allowed

Calendar

↓

Bazi

↓

Pattern

↓

Interpretation

Not Allowed

Interpretation

↓

Calendar

Report

↓

Pattern

Portal

↓

Knowledge

Knowledge

↓

Calendar

---

# 8.4 Engine Failure Strategy

If an Engine fails,

the pipeline shall stop immediately.

No downstream Engine may execute using incomplete upstream data.

Failure example

Calendar Failure

↓

Stop Pipeline

↓

Return Validation Error

↓

No BaZi Calculation

↓

No Interpretation

Partial execution is prohibited unless explicitly supported.

---

# 8.5 Validation Gates

Each Engine must complete validation before publishing output.

Validation includes

Schema Validation

Business Validation

Null Validation

Dependency Validation

Ownership Validation

Version Validation

Only validated outputs may enter the next pipeline stage.

---

# 8.6 Extension Rules

Future Engines shall be inserted without breaking existing contracts.

Allowed future modules include

Luck Engine

Shensha Engine

AI Rewrite Engine

Recommendation Engine

Prediction Engine

Learning Engine

Analytics Engine

Mobile API

Plugin System

Each new Engine must define

Input

Output

Ownership

Producer

Consumer

Validation

Version

No Engine may be inserted by bypassing the architecture contract.

---

# 8.7 Architecture Compliance Checklist

Every Pull Request shall satisfy the following checklist.

□ No multiple producers

□ No backward dependency

□ No business logic inside Report

□ No business logic inside Portal

□ No undocumented runtime fields

□ No direct Engine-to-Engine mutation

□ All outputs validated

□ SSOT preserved

□ Public contracts unchanged

□ Tests updated

Failure of any item shall block merge approval.

---

# 8.8 Architecture Review Process

Changes to the architecture shall follow this workflow.

Architecture Proposal

↓

Architecture Review

↓

Architecture Approval

↓

Documentation Update

↓

Implementation

↓

Testing

↓

Architecture Audit

↓

Release

Implementation shall never precede Architecture Approval.

---

# 8.9 Definition of Done (Architecture)

A feature is considered architecturally complete only when all of the following conditions are satisfied.

- Architecture documentation updated.
- Producer and Consumer defined.
- SSOT identified.
- Runtime contract documented.
- Validation implemented.
- Unit tests passed.
- Integration tests passed.
- Architecture audit passed.
- Documentation synchronized.
- Release notes updated.

---

# 8.10 Final Statement

This document is the authoritative architectural specification for the BTE Platform runtime pipeline.

All Engines, services, APIs, reports, plugins, and future modules shall conform to the contracts defined herein.

Whenever implementation differs from this specification, the implementation shall be reviewed and corrected, unless an approved architectural revision has superseded this document.

This document serves as the foundation for:

- Pipeline implementation
- Engine development
- Knowledge integration
- Runtime validation
- Architecture auditing
- Continuous integration
- Future platform evolution

---

End of Part 6

End of SYSTEM_DATA_FLOW.md Version 1.0
---

# Part 7 — Architecture Decision Records (ADR) & Runtime Compliance

## 9. Architecture Decision Records (ADR)

This section records the major architectural decisions of the BTE Platform.

These decisions are considered permanent unless superseded by an approved Architecture Revision.

---

## ADR-001

### Title

Forward-Only Runtime Pipeline

### Status

Accepted

### Decision

All business processing shall follow a forward-only execution pipeline.

```
Input
→ Calendar
→ Bazi
→ Pattern
→ RuleContext
→ Score
→ Knowledge
→ Rule Matching
→ Priority
→ Interpretation
→ Report
→ Portal
```

### Reason

- Predictable execution
- Easy debugging
- Deterministic results
- Simplified testing

---

## ADR-002

### Title

Single Source of Truth (SSOT)

### Status

Accepted

### Decision

Every business field has exactly one authoritative producer.

Example

```
solar_term

Producer

Calendar Engine

Consumers

Bazi
Pattern
Interpretation
Report
```

Multiple producers are prohibited.

---

## ADR-003

### Title

Contract-First Development

### Status

Accepted

### Decision

Architecture documentation shall be completed before implementation.

Implementation follows contracts.

Documentation does not follow implementation.

---

## ADR-004

### Title

Knowledge Base is Passive

### Status

Accepted

### Decision

Knowledge Base stores knowledge only.

It never executes business logic.

Business decisions are made only by Engines.

---

## ADR-005

### Title

Interpretation is Structured Data

### Status

Accepted

Interpretation Engine produces structured interpretation objects.

Rendering is delegated to Report Engine.

---

## ADR-006

### Title

Presentation Layer is Logic-Free

### Status

Accepted

Portal

API

Report

must never execute business calculations.

---

# 10. Runtime Compliance

Every Engine shall satisfy the following requirements.

## Input Compliance

□ Validate schema

□ Validate required fields

□ Validate ownership

---

## Output Compliance

□ Publish standardized context

□ Include metadata

□ Pass validation

---

## Runtime Compliance

□ No hidden side effects

□ No undocumented fields

□ No circular dependency

□ No mutable upstream context

□ No duplicate producer

---

# 11. Architecture Quality Gates

Every release shall pass these gates.

Gate 1

Architecture Validation

↓

Gate 2

Pipeline Validation

↓

Gate 3

Knowledge Validation

↓

Gate 4

Integration Tests

↓

Gate 5

Regression Tests

↓

Gate 6

Architecture Audit

↓

Release

Release shall be blocked if any gate fails.

---

# 12. Future Architecture Governance

Future architectural changes require:

- Architecture Proposal
- Technical Review
- Documentation Update
- Implementation
- Automated Audit
- Approval

Architecture changes shall never be introduced directly through source code.

---

# 13. Document Status

Document Name

SYSTEM_DATA_FLOW.md

Status

Architecture Contract

Version

1.0

Authority

BTE Platform Architecture

Applicable Scope

Entire Platform

This document shall remain the authoritative runtime architecture specification until replaced by a newer approved version.

---

End of Part 7
