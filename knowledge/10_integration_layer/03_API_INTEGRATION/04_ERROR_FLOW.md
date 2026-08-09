# Analyze Pipeline Error Flow

**Location**

```
knowledge/10_integration_layer/03_API_INTEGRATION/04_ERROR_FLOW.md
```

---

# Purpose

This document defines the canonical error handling flow of the BTE Analyze Pipeline.

Its purpose is to ensure every failure is handled consistently, predictably and safely.

Errors shall never leak internal implementation details.

Customers shall always receive a standardized ErrorResponse.

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

# Design Principles

The error architecture follows these principles.

- Fail Fast
- Fail Safe
- Deterministic
- No Partial Report
- Standardized ErrorResponse
- Full Traceability
- Engine Isolation

---

# High-Level Error Flow

```
Customer Request

↓

Applications API

↓

Analyze Pipeline

↓

Failure ?

↓

YES

↓

Error Mapper

↓

ErrorResponse

↓

Customer Portal

↓

Customer
```

No engine returns HTTP responses directly.

Applications API owns every customer-facing error.

---

# Error Ownership

| Component | Responsibility |
|------------|----------------|
| Customer Portal | Display Error |
| Applications API | Error Mapping |
| Analyze Orchestrator | Pipeline Termination |
| Engines | Raise Domain Errors |
| Report Builder | Raise Validation Errors |
| Validator | Raise Contract Errors |

---

# Error Categories

The platform defines six error categories.

```
Request Errors

↓

Calendar Errors

↓

BaZi Errors

↓

Analysis Errors

↓

Interpretation Errors

↓

Integration Errors
```

---

# Request Errors

Origin

Applications API

Examples

- Missing birth date
- Invalid time
- Invalid location
- Invalid calendar type

Result

```
400 Bad Request
```

Pipeline never starts.

---

# Calendar Errors

Origin

Calendar Engine

Examples

- Unsupported timezone
- Invalid calendar conversion
- JieQi unavailable

Result

```
422 Unprocessable Entity
```

Pipeline terminates.

---

# BaZi Errors

Origin

BaZi Engine

Examples

- Pillar generation failure
- Invalid chart
- Hidden stem failure

Result

```
422 Unprocessable Entity
```

Pipeline terminates.

---

# Analysis Errors

Origin

Analysis Engine

Examples

- Pattern failure
- Evidence failure
- Score failure

Result

```
500 Internal Server Error
```

Pipeline terminates.

---

# Interpretation Errors

Origin

Interpretation Engine

Examples

- Rule evaluation failure
- Sentence generation failure
- Narrative failure

Result

```
500 Internal Server Error
```

Pipeline terminates.

---

# Commercial Knowledge Errors

Origin

Commercial Knowledge

Examples

- Unknown capability
- Missing Knowledge Unit
- Bundle construction failure

Result

```
500 Internal Server Error
```

Pipeline terminates.

---

# Report Builder Errors

Origin

Report Builder

Examples

- Section Builder failure
- Merge failure
- BuilderContext invalid

Result

```
500 Internal Server Error
```

Pipeline terminates.

---

# Contract Validation Errors

Origin

Schema Validator

Examples

- Missing required field
- Invalid JSON Schema
- Traceability failure
- Version mismatch

Result

```
500 Internal Server Error
```

No invalid ReportResponse may be returned.

---

# Error Pipeline

```
Engine

↓

Raise Error

↓

Analyze Orchestrator

↓

Pipeline Stop

↓

Error Mapper

↓

Standard ErrorResponse

↓

Applications API

↓

Portal
```

---

# ErrorResponse

Every failure returns

```
ErrorResponse

├── code
├── category
├── message
├── request_id
├── timestamp
├── retryable
└── correlation_id
```

No stack traces.

No internal object names.

No implementation details.

---

# Error Severity

```
INFO

↓

WARNING

↓

ERROR

↓

CRITICAL
```

---

## INFO

Logging only.

Pipeline continues.

---

## WARNING

Non-blocking issue.

Pipeline continues.

---

## ERROR

Pipeline terminates.

Customer receives ErrorResponse.

---

## CRITICAL

Immediate termination.

System diagnostics recorded.

---

# Retry Policy

| Category | Retry |
|-----------|-------|
| Request | No |
| Calendar | No |
| BaZi | No |
| Analysis | No |
| Interpretation | No |
| Commercial Knowledge | No |
| Report Builder | No |
| Infrastructure | Yes |

Business errors are never retried automatically.

Infrastructure failures may be retried.

---

# Error Mapping

| Internal Error | HTTP |
|----------------|------|
| RequestError | 400 |
| CalendarError | 422 |
| BaZiError | 422 |
| AnalysisError | 500 |
| InterpretationError | 500 |
| KnowledgeError | 500 |
| BuilderError | 500 |
| ValidationError | 500 |

---

# Error Lifecycle

```
Error Detected

↓

Classify

↓

Record

↓

Stop Pipeline

↓

Map

↓

Generate ErrorResponse

↓

Return HTTP Response
```

---

# Logging

Every error records

```
request_id

pipeline_stage

engine

error_code

severity

timestamp

execution_time
```

Logs are internal.

Customers never see them.

---

# Traceability

Every ErrorResponse must be traceable to

```
Request

↓

AnalyzeContext

↓

Pipeline Stage

↓

Component

↓

Error Code
```

---

# Customer Experience

The Customer Portal shall

- display friendly messages
- hide technical details
- preserve request_id
- allow retry if appropriate

The Portal must never display

- stack traces
- Python exceptions
- engine names
- file paths

---

# Forbidden Behaviour

The platform shall never

- return partial ReportResponse
- ignore schema failures
- expose internal exceptions
- continue after critical failure
- mix ReportResponse with ErrorResponse

---

# Future Extensions

Reserved

```
Retry Manager

Circuit Breaker

Observability

Distributed Tracing

Incident Reporting
```

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_ANALYZE_PIPELINE.md | Runtime pipeline |
| 02_ENDPOINTS.md | Public API |
| 03_SEQUENCE_DIAGRAM.md | Runtime interaction |
| 04_ERROR_FLOW.md | Error architecture |
| 05_VERSION_NEGOTIATION.md | Version compatibility |

---

# Acceptance Criteria

The Error Flow is accepted when

✓ Every failure has one owner

✓ Every error maps to one HTTP response

✓ Pipeline always terminates safely

✓ ErrorResponse is standardized

✓ No internal implementation leaks

✓ Portal never receives partial reports

✓ Errors are traceable

✓ Logging is standardized

---

# Official Status

Document

Analyze Pipeline Error Flow

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Architecture