# Architecture Decisions (ADR)

**Location**

```
knowledge/10_integration_layer/00A_ARCHITECTURE_DECISIONS.md
```

---

# Purpose

This document records the official architectural decisions that govern the Integration Layer and the end-to-end processing pipeline of the BTE Platform.

Unlike architecture specifications that describe **how the system works**, this document explains **why the architecture is designed this way**.

Every major architectural decision must be documented here before implementation.

---

# Status

Document Type

Architecture Decision Record (ADR)

Status

Active

Commercial Version

RC1

Owner

BTE Architecture

---

# Decision Record Format

Each decision must contain:

- Decision ID
- Title
- Status
- Context
- Decision
- Consequences
- Alternatives Considered

---

# ADR-001

## Title

Customer applications consume ReportResponse only.

### Status

Accepted

---

### Context

Customer applications originally accessed multiple internal models such as:

- AnalysisResult
- InterpretationResult
- NarrativeResult

This created tight coupling between UI and analytical engines.

Any internal engine change required Portal updates.

---

### Decision

All customer-facing applications consume only:

```
ReportResponse
```

No application may directly consume internal engine models.

---

### Consequences

Positive

- Loose coupling
- Stable APIs
- Independent engine evolution
- Simplified Portal

Negative

- Integration Layer becomes mandatory

---

### Alternatives Considered

Portal consumes AnalysisResult directly.

Rejected.

Reason:

Presentation becomes tightly coupled to analysis implementation.

---

# ADR-002

## Title

Report Builder contains no business logic.

### Status

Accepted

---

### Context

Business rules belong to analytical engines.

Duplicating logic inside Report Builder introduces inconsistencies.

---

### Decision

Report Builder performs only:

- merge
- normalize
- ordering
- validation
- assembly

No analytical calculation is allowed.

---

### Consequences

Positive

Single source of truth.

Negative

Builder depends on complete upstream outputs.

---

### Alternatives Considered

Report Builder recalculates missing values.

Rejected.

---

# ADR-003

## Title

Commercial Knowledge precedes Report Builder.

### Status

Accepted

---

### Context

Commercial advice is generated from approved Knowledge Units.

Report Builder should assemble completed content rather than retrieve knowledge.

---

### Decision

Pipeline order:

```
Analysis

↓

Interpretation

↓

Commercial Knowledge

↓

Report Builder
```

---

### Consequences

Commercial content becomes deterministic.

---

### Alternatives Considered

Report Builder retrieves Knowledge Units.

Rejected.

Reason:

Violates separation of responsibilities.

---

# ADR-004

## Title

One official processing pipeline.

### Status

Accepted

---

### Context

Multiple pipelines create inconsistent customer experiences.

---

### Decision

Official pipeline:

```
Customer

↓

Calendar Engine

↓

BaZi Engine

↓

Analysis Engine

↓

Interpretation Engine

↓

Commercial Knowledge

↓

Integration Layer

↓

ReportResponse

↓

Presentation
```

No alternative production pipeline is allowed.

---

### Consequences

Deterministic processing.

---

### Alternatives Considered

Multiple product pipelines.

Rejected.

---

# ADR-005

## Title

Integration Layer owns orchestration only.

### Status

Accepted

---

### Context

Integration Layer sits between engines and applications.

Its purpose is orchestration rather than computation.

---

### Decision

Integration Layer may:

- validate
- assemble
- normalize
- expose contracts

Integration Layer may never:

- calculate BaZi
- analyze charts
- interpret rules
- generate knowledge

---

### Consequences

Clear architectural boundaries.

---

# ADR-006

## Title

Presentation Layer is engine-independent.

### Status

Accepted

---

### Context

Portal and PDF should evolve independently from analytical engines.

---

### Decision

Presentation depends only on:

```
ReportResponse
```

Presentation must never import:

- Analysis Engine
- Interpretation Engine
- Rule Database
- Commercial Knowledge

---

### Consequences

UI becomes stable.

---

# ADR-007

## Title

ReportResponse is the canonical product contract.

### Status

Accepted

---

### Context

Different output models increase integration complexity.

---

### Decision

The official customer-facing contract is:

```
ReportResponse
```

Future clients consume the same contract:

- Customer Portal
- Mobile App
- PDF
- Public APIs
- Third-party integrations

---

### Consequences

Single integration model.

---

# ADR-008

## Title

Backward compatibility is mandatory.

### Status

Accepted

---

### Context

Commercial customers require stable integrations.

---

### Decision

Published fields:

- must not be removed
- must not change type

New fields must be optional.

Breaking changes require a major version.

---

### Consequences

Long-term compatibility.

---

# ADR-009

## Title

Evidence traceability is mandatory.

### Status

Accepted

---

### Context

Every customer conclusion must be explainable.

---

### Decision

Every ReportResponse section must preserve traceability to:

- Analysis Evidence
- Interpretation
- Commercial Knowledge
- Rule References

No generated content may lose its origin.

---

### Consequences

Explainable consulting.

Auditable reports.

---

# ADR-010

## Title

Integration Layer is the final architectural boundary.

### Status

Accepted

---

### Context

Applications should never know internal engine topology.

---

### Decision

Applications communicate only with:

```
Applications API

↓

Integration Layer

↓

ReportResponse
```

Engine topology remains internal.

---

### Consequences

Future engine refactoring does not affect customers.

---

# Future Decisions

Reserved for:

- Streaming responses
- AI-assisted rewriting
- Multi-language output
- Mobile synchronization
- Public SDK
- Offline reports
- Plugin architecture

---

# Decision Lifecycle

```
Proposed

↓

Review

↓

Accepted

↓

Implemented

↓

Frozen

↓

Deprecated
```

Only **Accepted** decisions may enter implementation.

---

# Governance Rules

Every architectural change must:

- reference an ADR
- document the reason
- describe the impact
- preserve backward compatibility whenever possible

Implementation without an approved ADR is not permitted.

---

# Official Status

Architecture Decisions

Active

Implementation

Governed by this document

Commercial Version

RC1

Owner

BTE Architecture