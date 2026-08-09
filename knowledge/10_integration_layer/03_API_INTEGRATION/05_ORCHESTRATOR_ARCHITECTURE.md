# Analyze Orchestrator Architecture

**Location**

```
knowledge/10_integration_layer/03_API_INTEGRATION/05_ORCHESTRATOR_ARCHITECTURE.md
```

---

# Purpose

This document defines the canonical architecture of the Analyze Orchestrator.

The Analyze Orchestrator is responsible for coordinating the execution of the complete BTE analysis pipeline.

It is the only component allowed to invoke analytical engines during runtime.

The Applications API delegates orchestration to this component.

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

The Analyze Orchestrator is

- Stateless
- Deterministic
- Pipeline-driven
- Context-oriented
- Fail Fast
- Engine-independent

The Orchestrator coordinates execution.

It never performs analysis.

It never performs interpretation.

It never builds reports.

---

# Position in Architecture

```
Customer Portal

        │

        ▼

Applications API

        │

        ▼

==============================
Analyze Orchestrator
==============================

        │

        ▼

Calendar Engine

BaZi Engine

Analysis Engine

Interpretation Engine

Commercial Knowledge

Report Builder

        │

        ▼

ReportResponse
```

Applications API owns HTTP.

Analyze Orchestrator owns execution.

---

# Responsibilities

The Analyze Orchestrator is responsible for

- Creating AnalyzeContext
- Executing pipeline stages
- Managing runtime state
- Handling failures
- Preserving traceability
- Returning ReportResponse

---

# Non-Responsibilities

The Analyze Orchestrator shall never

- Calculate BaZi
- Match Rules
- Retrieve Knowledge
- Build Narratives
- Render UI
- Persist data
- Perform business decisions

---

# Runtime Model

The Orchestrator creates

```
AnalyzeContext
```

AnalyzeContext is the only mutable runtime object.

All engine outputs are immutable.

---

# AnalyzeContext

```
AnalyzeContext

├── request
├── metadata
├── runtime
├── calendar
├── chart
├── analysis
├── interpretation
├── commercial
├── report
├── diagnostics
├── timings
└── state
```

Every stage enriches AnalyzeContext.

No stage overwrites previous results.

---

# Pipeline State Machine

```
INITIALIZED

↓

VALIDATING_REQUEST

↓

CALENDAR

↓

BAZI

↓

ANALYSIS

↓

INTERPRETATION

↓

COMMERCIAL

↓

REPORT_BUILD

↓

VALIDATION

↓

COMPLETED
```

Failure transitions

```
ANY STATE

↓

FAILED
```

---

# Execution Flow

```
Receive Request

↓

Create AnalyzeContext

↓

Validate Request

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

Report Builder

↓

Schema Validation

↓

Return ReportResponse
```

---

# Internal Components

```
Analyze Orchestrator

│

├── Context Manager

├── Stage Executor

├── State Machine

├── Error Coordinator

├── Validation Coordinator

├── Diagnostics Collector

└── Result Publisher
```

Each component has a single responsibility.

---

# Context Manager

Responsibilities

- Create AnalyzeContext
- Append runtime objects
- Preserve immutability
- Destroy context after completion

---

# Stage Executor

Responsibilities

Execute stages sequentially.

Allowed stages

```
Calendar

BaZi

Analysis

Interpretation

Commercial

Report Builder
```

Stages execute through public engine interfaces only.

---

# State Machine

Tracks current execution state.

Allowed transitions

```
INITIALIZED

↓

VALIDATING_REQUEST

↓

CALENDAR

↓

BAZI

↓

ANALYSIS

↓

INTERPRETATION

↓

COMMERCIAL

↓

REPORT_BUILD

↓

VALIDATION

↓

COMPLETED
```

Illegal transitions are rejected.

---

# Error Coordinator

Responsibilities

- Capture engine failures
- Stop pipeline
- Build ErrorResponse
- Record diagnostics

Errors never propagate directly to Applications API.

---

# Validation Coordinator

Responsibilities

Coordinate

- Request Validation
- Schema Validation
- Business Validation
- Release Validation

Validation remains independent from orchestration.

---

# Diagnostics Collector

Collects

```
Execution Time

Stage Timing

Warnings

Errors

Version

Traceability
```

Diagnostics are internal only.

---

# Result Publisher

Responsible for

```
ReportResponse

↓

Applications API
```

The publisher never modifies ReportResponse.

---

# Engine Invocation Rules

Allowed

```
Orchestrator

↓

Calendar Engine
```

```
Orchestrator

↓

Analysis Engine
```

Forbidden

```
Analysis Engine

↓

Interpretation Engine
```

```
Commercial Knowledge

↓

Portal
```

Only the Orchestrator coordinates engines.

---

# Parallel Execution

Commercial V1

Sequential execution only.

Future versions may parallelize

- Charts
- Knowledge
- Diagnostics

Core analytical stages remain sequential.

---

# Retry Policy

Business stages

No retry.

Infrastructure failures

Retry supported by future infrastructure layer.

Commercial V1 performs no automatic retries.

---

# Timeout Policy

Every stage may define

```
Maximum Execution Time
```

Timeout causes

```
FAILED
```

No partial report is returned.

---

# Cancellation Policy

If request is cancelled

↓

Stop current stage

↓

Release AnalyzeContext

↓

Discard runtime objects

↓

Return cancellation response

---

# Traceability

AnalyzeContext preserves

```
Request

↓

Calendar

↓

Chart

↓

Analysis

↓

Interpretation

↓

Commercial

↓

Report
```

Every runtime object remains traceable.

---

# Observability

Future observability hooks

```
Metrics

Tracing

Logging

Health

Performance
```

shall integrate through the Orchestrator.

No engine shall implement observability independently.

---

# Extension Points

Future integrations

```
AI Rewrite

Plugin Runtime

Streaming Output

Audit Trail

Observability

Workflow Engine
```

must attach to the Orchestrator.

Existing engines remain unchanged.

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_ANALYZE_PIPELINE.md | Pipeline stages |
| 02_ENDPOINTS.md | Public API |
| 03_SEQUENCE_DIAGRAM.md | Component interaction |
| 03A_RUNTIME_SEQUENCE.md | Runtime object lifecycle |
| 04_ERROR_FLOW.md | Failure handling |
| 05_ORCHESTRATOR_ARCHITECTURE.md | Orchestrator architecture (this document) |

---

# Acceptance Criteria

The Analyze Orchestrator architecture is accepted when

✓ Applications API contains no business logic

✓ AnalyzeContext is the only orchestration context

✓ Engine outputs are immutable

✓ Only the Orchestrator invokes engines

✓ State transitions are defined

✓ Errors terminate safely

✓ ReportResponse is the only successful output

✓ Runtime objects are destroyed after completion

✓ The architecture supports future capabilities without changing engine contracts

---

# Official Status

Document

Analyze Orchestrator Architecture

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Architecture