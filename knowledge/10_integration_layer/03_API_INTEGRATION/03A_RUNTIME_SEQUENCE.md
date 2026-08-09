# Runtime Object Sequence

**Location**

```
knowledge/10_integration_layer/03_API_INTEGRATION/03A_RUNTIME_SEQUENCE.md
```

---

# Purpose

This document defines the runtime lifecycle of objects created during execution of the BTE Analyze Pipeline.

Unlike the Sequence Diagram, which describes interactions between components, this document describes the evolution of runtime data from request reception until the final `ReportResponse` is returned.

The Runtime Sequence is the canonical object lifecycle of Commercial V1.

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

# Runtime Philosophy

The Analyze Pipeline creates one canonical runtime context.

Every stage enriches that context.

No stage mutates completed results.

No runtime object survives after the request completes.

---

# Runtime Lifecycle Overview

```
HTTP Request

↓

AnalyzeRequest

↓

AnalyzeContext

↓

CalendarResult

↓

BaZiChart

↓

AnalysisResult

↓

InterpretationResult

↓

CommercialKnowledgeBundle

↓

BuilderContext

↓

SectionResults

↓

ValidationResult

↓

ReportResponse

↓

HTTP Response

↓

Destroy Runtime Objects
```

---

# Runtime Object Timeline

```
Request
│
├──────────────┐
│              │
▼              │
AnalyzeRequest │
│              │
├──────────────┘
│
▼
AnalyzeContext
│
├──────────────────────────────┐
│                              │
├── CalendarResult             │
│                              │
├── BaZiChart                  │
│                              │
├── AnalysisResult             │
│                              │
├── InterpretationResult       │
│                              │
├── CommercialKnowledgeBundle  │
│                              │
├── BuilderContext             │
│                              │
├── SectionResults             │
│                              │
├── ValidationResult           │
│                              │
└── ReportResponse             │
                               │
                               ▼
                      HTTP Response
```

AnalyzeContext is the parent runtime object.

---

# Stage 1 — AnalyzeRequest

Created by

Applications API

Contains

```
Customer

Birth Information

Runtime Options

Metadata
```

Lifetime

Until AnalyzeContext creation.

---

# Stage 2 — AnalyzeContext

Created by

Analyze Orchestrator

Purpose

Acts as the canonical runtime container.

Contains

```
request

runtime

calendar

chart

analysis

interpretation

commercial

report

diagnostics
```

Lifetime

Entire request lifecycle.

Destroyed after response.

---

# Stage 3 — CalendarResult

Created by

Calendar Engine

Stored in

```
AnalyzeContext.calendar
```

Immutable after creation.

---

# Stage 4 — BaZiChart

Created by

BaZi Engine

Stored in

```
AnalyzeContext.chart
```

Never recalculated.

---

# Stage 5 — AnalysisResult

Created by

Analysis Engine

Stored in

```
AnalyzeContext.analysis
```

Contains

- Evidence
- Scores
- Useful God
- Strength
- Weakness
- Patterns

Read-only after completion.

---

# Stage 6 — InterpretationResult

Created by

Interpretation Engine

Stored in

```
AnalyzeContext.interpretation
```

Contains

- Executive Summary
- Narrative
- Recommendations

Never modified by downstream components.

---

# Stage 7 — CommercialKnowledgeBundle

Created by

Commercial Knowledge Adapter

Stored in

```
AnalyzeContext.commercial
```

Contains

- Identity
- Capability Outputs
- Domain Recommendations
- Commercial Language

---

# Stage 8 — BuilderContext

Created by

Report Builder

Purpose

Expose a normalized runtime model for all Section Builders.

Contains references only.

```
BuilderContext

├── metadata
├── analysis
├── interpretation
├── commercial
├── runtime
├── validation
└── options
```

BuilderContext never owns data.

---

# Stage 9 — SectionResults

Created by

Section Builders

One object per section.

```
Executive Section

Identity Section

Recommendation Section

Evidence Section

Knowledge Section

...
```

Collected before merge.

---

# Stage 10 — ValidationResult

Created by

Validation Framework

Contains

```
status

severity

warnings

errors

execution_time

validator
```

If validation fails

↓

Pipeline terminates.

---

# Stage 11 — ReportResponse

Created by

Report Builder

Purpose

Canonical customer-facing contract.

Stored in

```
AnalyzeContext.report
```

Returned unchanged by Applications API.

---

# Runtime Ownership

| Runtime Object | Owner |
|----------------|-------|
| AnalyzeRequest | Applications API |
| AnalyzeContext | Analyze Orchestrator |
| CalendarResult | Calendar Engine |
| BaZiChart | BaZi Engine |
| AnalysisResult | Analysis Engine |
| InterpretationResult | Interpretation Engine |
| CommercialKnowledgeBundle | Commercial Knowledge |
| BuilderContext | Report Builder |
| SectionResult | Section Builder |
| ValidationResult | Validation Framework |
| ReportResponse | Report Builder |

---

# Runtime Relationships

```
AnalyzeRequest

↓

AnalyzeContext

├── CalendarResult

├── BaZiChart

├── AnalysisResult

├── InterpretationResult

├── CommercialKnowledgeBundle

↓

BuilderContext

↓

SectionResults

↓

ValidationResult

↓

ReportResponse
```

---

# Object Mutability

| Object | Mutable |
|----------|---------|
| AnalyzeRequest | NO |
| AnalyzeContext | YES (append only) |
| CalendarResult | NO |
| BaZiChart | NO |
| AnalysisResult | NO |
| InterpretationResult | NO |
| CommercialKnowledgeBundle | NO |
| BuilderContext | NO |
| SectionResult | NO |
| ValidationResult | NO |
| ReportResponse | NO |

AnalyzeContext is the only mutable orchestration object.

Mutation is append-only.

Existing values may never be modified.

---

# Object Lifetime

| Object | Lifetime |
|----------|----------|
| AnalyzeRequest | Request validation |
| AnalyzeContext | Entire request |
| CalendarResult | Entire request |
| BaZiChart | Entire request |
| AnalysisResult | Entire request |
| InterpretationResult | Entire request |
| CommercialKnowledgeBundle | Entire request |
| BuilderContext | Report Builder execution |
| SectionResult | Report Builder execution |
| ValidationResult | Validation stage |
| ReportResponse | Response serialization |

All runtime objects are destroyed after the HTTP response is sent.

---

# Memory Policy

Runtime objects

- never persisted
- never cached
- never shared
- never reused
- never exposed externally

Every request creates a new runtime graph.

---

# Runtime Guarantees

The Runtime Sequence guarantees

✓ One AnalyzeContext per request

✓ Immutable engine outputs

✓ Append-only orchestration

✓ Stateless execution

✓ Deterministic object lifecycle

✓ No shared runtime state

✓ One ReportResponse

---

# Future Runtime Extensions

Reserved runtime objects

```
AIRewriteResult

ObservabilityContext

PluginContext

StreamingContext

AuditContext

PerformanceMetrics
```

Future objects extend AnalyzeContext without changing existing runtime contracts.

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_ANALYZE_PIPELINE.md | Pipeline stages |
| 02_ENDPOINTS.md | Public API |
| 03_SEQUENCE_DIAGRAM.md | Component interaction |
| 03A_RUNTIME_SEQUENCE.md | Runtime object lifecycle (this document) |
| 04_ERROR_FLOW.md | Failure architecture |

---

# Acceptance Criteria

The Runtime Sequence is accepted when

✓ AnalyzeContext is the single orchestration object

✓ Every runtime object has one owner

✓ Engine outputs are immutable

✓ BuilderContext is created only inside Report Builder

✓ ReportResponse is the only public output

✓ Runtime objects are destroyed after request completion

✓ Runtime lifecycle is deterministic

---

# Official Status

Document

Runtime Object Sequence

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Architecture