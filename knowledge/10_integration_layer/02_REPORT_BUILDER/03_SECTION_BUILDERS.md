# Section Builders Architecture

**Location**

```
knowledge/10_integration_layer/02_REPORT_BUILDER/03_SECTION_BUILDERS.md
```

---

# Purpose

This document defines the canonical architecture of Section Builders within the Report Builder.

Section Builders are responsible for constructing individual sections of the canonical `ReportResponse`.

Each Section Builder owns one and only one section.

Section Builders never communicate directly with analytical engines.

All builders consume a shared `BuilderContext`.

---

# Status

Document Type

Architecture Specification

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Architecture

---

# Design Philosophy

The Report Builder follows the Composition Pattern.

```
Report Builder

↓

BuilderContext

↓

Section Builders

↓

ReportResponse
```

Every Builder has a single responsibility.

---

# BuilderContext

BuilderContext is the canonical runtime model of the Report Builder.

Every Section Builder receives exactly one input.

```
BuilderContext
```

BuilderContext contains references to:

```
AnalysisResult

InterpretationResult

CommercialKnowledgeBundle

Report Metadata

Runtime Configuration

Validation Context
```

Builders never receive engine objects individually.

---

# BuilderContext Diagram

```
BuilderContext

│

├── metadata

├── analysis

├── interpretation

├── commercial

├── runtime

├── validation

└── options
```

BuilderContext is immutable.

Builders must never modify it.

---

# Report Builder Composition

```
Report Builder

│

├── Metadata Builder

├── Customer Builder

├── Chart Builder

├── Executive Builder

├── Identity Builder

├── Strength Builder

├── Weakness Builder

├── UsefulGod Builder

├── Recommendation Builder

├── Domain Builder

├── Evidence Builder

├── Knowledge Builder

├── Appendix Builder

└── Diagnostics Builder
```

Each Builder owns exactly one ReportResponse section.

---

# Builder Interface

Every Section Builder follows the same logical contract.

Input

```
BuilderContext
```

Output

```
Section Object
```

Each Builder returns only its own section.

Builders never construct sibling sections.

---

# Metadata Builder

## Responsibility

Construct metadata.

Produces

```
metadata
```

Consumes

```
BuilderContext.metadata
```

Never accesses

- Analysis
- Knowledge

---

# Customer Builder

Produces

```
customer
```

Consumes

```
BuilderContext.analysis.input
```

---

# Chart Builder

Produces

```
chart
```

Consumes

```
BuilderContext.analysis.chart
```

Never calculates BaZi.

---

# Executive Builder

Produces

```
executive_summary
```

Consumes

- Interpretation
- Commercial Knowledge

Priority

Commercial wording takes precedence.

---

# Identity Builder

Produces

```
identity
```

Consumes

Commercial Knowledge.

---

# Strength Builder

Produces

```
strengths
```

Consumes

Analysis

Commercial Knowledge

---

# Weakness Builder

Produces

```
weaknesses
```

Consumes

Analysis

Commercial Knowledge

---

# UsefulGod Builder

Produces

```
useful_god
```

Consumes

Analysis

Commercial Knowledge

---

# Recommendation Builder

Produces

```
recommendations
```

Consumes

Interpretation

Commercial Knowledge

Produces

Primary Recommendation

Secondary Recommendations

Timeline

Expected Outcome

---

# Domain Builder

Produces

```
domains
```

Responsibilities

Build all commercial capability outputs.

Examples

```
career

finance

marriage

health

business

education

children

future capabilities
```

Domain Builder is extensible.

---

# Evidence Builder

Produces

```
evidence
```

Consumes

AnalysisResult only.

Never creates evidence.

---

# Knowledge Builder

Produces

```
knowledge
```

Consumes

CommercialKnowledgeBundle.

Never queries Knowledge Database.

---

# Appendix Builder

Produces

```
appendix
```

Optional section.

Contains supplementary information.

---

# Diagnostics Builder

Produces

```
diagnostics
```

Contains

Validation

Warnings

Builder statistics

Timing

Optional.

Not customer-facing.

---

# Builder Execution Model

```
BuilderContext

↓

Metadata Builder

↓

Customer Builder

↓

Chart Builder

↓

Executive Builder

↓

Identity Builder

↓

Strength Builder

↓

Weakness Builder

↓

UsefulGod Builder

↓

Recommendation Builder

↓

Domain Builder

↓

Evidence Builder

↓

Knowledge Builder

↓

Appendix Builder

↓

Diagnostics Builder
```

Independent builders may execute in parallel.

---

# Builder Dependencies

Allowed

```
BuilderContext

↓

Section Builder

↓

Section Object
```

Forbidden

```
Section Builder

↓

Analysis Engine

↓

Interpretation Engine

↓

Rule Database

↓

Knowledge Database

↓

Customer Portal
```

Builders depend only on BuilderContext.

---

# Builder Ordering

Mandatory order

```
Metadata

↓

Customer

↓

Chart

↓

Executive

↓

Identity

↓

Strength

↓

Weakness

↓

Useful God

↓

Recommendation

↓

Domains

↓

Evidence

↓

Knowledge

↓

Appendix

↓

Diagnostics
```

Ordering ensures deterministic assembly.

---

# Builder Validation

Each Builder validates

- required inputs
- required outputs
- traceability
- schema compliance

Validation failures stop assembly of that section.

---

# Builder Output

Every Builder produces one object only.

Example

Executive Builder

↓

```
executive_summary
```

Recommendation Builder

↓

```
recommendations
```

No Builder produces multiple top-level sections.

---

# Extensibility

New capabilities never modify existing Builders.

Instead

```
Domain Builder

↓

Leadership Module

↓

Leadership Section
```

or

```
Domain Builder

↓

Finance Module

↓

Finance Section
```

Builder architecture remains unchanged.

---

# Future Builders

Reserved

```
Leadership Builder

Finance Builder

Marriage Builder

Business Builder

Education Builder

Health Builder
```

These may extend Domain Builder or become independent builders if complexity requires.

---

# Builder Lifecycle

```
Receive BuilderContext

↓

Validate Input

↓

Assemble Section

↓

Normalize

↓

Validate Output

↓

Return Section
```

No Builder performs persistence.

No Builder performs rendering.

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_ARCHITECTURE.md | Report Builder overview |
| 02_PIPELINE.md | Assembly pipeline |
| 03_SECTION_BUILDERS.md | Builder responsibilities (this document) |
| 04_VALIDATION.md | Validation architecture |

---

# Acceptance Criteria

The Section Builder architecture is accepted when

✓ Every section has exactly one Builder

✓ Every Builder consumes BuilderContext only

✓ Builders are stateless

✓ Builders are deterministic

✓ Builders own one section only

✓ Builders never access engines directly

✓ Builders preserve traceability

✓ New capabilities can be added without changing existing Builders

---

# Official Status

Document

Section Builder Architecture

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Architecture