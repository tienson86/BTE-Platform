# Analyze Pipeline

**Location**

```
knowledge/10_integration_layer/03_API_INTEGRATION/01_ANALYZE_PIPELINE.md
```

---

# Purpose

This document defines the official end-to-end Analyze Pipeline of the BTE Platform.

The Analyze Pipeline is the orchestration flow executed by the Applications API.

Its responsibility is to coordinate all analytical engines and produce one canonical `ReportResponse`.

No business logic is implemented inside the API.

The API acts only as the orchestrator.

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

The Analyze Pipeline follows these principles:

- One Request
- One Pipeline
- One ReportResponse
- Stateless
- Deterministic
- Engine Independence
- Fail Fast
- Validate Before Publish

---

# High-Level Flow

```
Customer Portal

        │

        ▼

POST /api/v1/analyze

        │

        ▼

Applications API

        │

        ▼

Analyze Pipeline

        │

        ▼

Calendar Engine

        │

        ▼

BaZi Engine

        │

        ▼

Analysis Engine

        │

        ▼

Interpretation Engine

        │

        ▼

Commercial Knowledge

        │

        ▼

Report Builder

        │

        ▼

ReportResponse

        │

        ▼

Customer Portal
```

---

# Pipeline Overview

```
Stage 1

Receive Request

↓

Stage 2

Validate Request

↓

Stage 3

Calendar Calculation

↓

Stage 4

BaZi Chart Construction

↓

Stage 5

Chart Analysis

↓

Stage 6

Interpretation

↓

Stage 7

Commercial Knowledge

↓

Stage 8

Report Builder

↓

Stage 9

Response Validation

↓

Stage 10

Return ReportResponse
```

---

# Stage 1 — Receive Request

## Purpose

Receive customer analysis request.

---

## Input

HTTP Request

Contains

- Customer Information
- Birth Date
- Birth Time
- Birth Location
- Calendar Type
- Runtime Options

---

## Output

AnalyzeRequest

---

# Stage 2 — Request Validation

## Purpose

Validate request before execution.

---

## Validate

- Required fields
- Date validity
- Time validity
- Time zone
- Birth location
- Supported calendar

---

## Failure

Return

```
400 Bad Request
```

Pipeline terminates.

---

# Stage 3 — Calendar Engine

## Purpose

Generate canonical calendar information.

---

## Output

CalendarResult

Contains

- Solar Calendar
- Lunar Calendar
- JieQi
- Julian Day
- Time Zone

---

# Stage 4 — BaZi Engine

## Purpose

Generate BaZi chart.

---

## Input

CalendarResult

---

## Output

BaZiChart

Contains

- Four Pillars
- Hidden Stems
- Ten Gods
- Five Elements

---

# Stage 5 — Analysis Engine

## Purpose

Produce deterministic chart analysis.

---

## Input

BaZiChart

---

## Output

AnalysisResult

Contains

- Strength
- Useful God
- Evidence
- Scores
- Patterns
- Relationships

---

# Stage 6 — Interpretation Engine

## Purpose

Transform analytical evidence into explanations.

---

## Input

AnalysisResult

---

## Output

InterpretationResult

Contains

- Executive Summary
- Narrative
- Recommendations
- Explanations

---

# Stage 7 — Commercial Knowledge

## Purpose

Enhance customer-facing consultation.

---

## Input

AnalysisResult

InterpretationResult

---

## Output

CommercialKnowledgeBundle

Contains

- Identity
- Capability Outputs
- Commercial Recommendations
- Domain Consultation

---

# Stage 8 — Report Builder

## Purpose

Assemble canonical ReportResponse.

---

## Input

AnalysisResult

InterpretationResult

CommercialKnowledgeBundle

---

## Output

ReportResponse

---

# Stage 9 — Response Validation

## Purpose

Validate ReportResponse.

---

## Validate

JSON Schema

Required sections

Traceability

Version compatibility

Commercial quality

---

## Failure

Return

```
500 Internal Server Error
```

No invalid ReportResponse shall be published.

---

# Stage 10 — Return Response

## Purpose

Return canonical response.

---

## Output

```
HTTP 200 OK

ReportResponse
```

No alternative response model is allowed.

---

# Runtime Context

The pipeline creates one runtime object.

```
AnalyzeContext
```

Contains

```
Request

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

ReportResponse
```

AnalyzeContext exists only during execution.

---

# Pipeline Diagram

```
Request

        │

        ▼

Validation

        │

        ▼

Calendar

        │

        ▼

BaZi

        │

        ▼

Analysis

        │

        ▼

Interpretation

        │

        ▼

Commercial Knowledge

        │

        ▼

Report Builder

        │

        ▼

Validation

        │

        ▼

ReportResponse
```

---

# Error Handling

Request Validation Failure

↓

400 Bad Request

---

Calendar Failure

↓

422 Unprocessable Entity

---

BaZi Failure

↓

422 Unprocessable Entity

---

Analysis Failure

↓

500 Internal Error

---

Interpretation Failure

↓

500 Internal Error

---

Commercial Knowledge Failure

↓

500 Internal Error

---

Report Builder Failure

↓

500 Internal Error

---

Schema Validation Failure

↓

500 Internal Error

---

# Pipeline Guarantees

The Analyze Pipeline guarantees

✓ One Request

✓ One AnalyzeContext

✓ One Pipeline

✓ One ReportResponse

✓ Stateless execution

✓ Deterministic output

✓ No business logic inside API

✓ Traceability preservation

---

# Performance Goals

The Analyze Pipeline shall

- execute sequential engine orchestration
- avoid duplicated calculations
- avoid repeated Knowledge retrieval
- avoid unnecessary object copies

The API performs orchestration only.

---

# Dependency Rules

Allowed

```
Applications API

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
```

Forbidden

```
Portal

↓

Analysis Engine

Portal

↓

Knowledge Database

API

↓

Rule Database
```

Applications API communicates only through public engine interfaces.

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 00_SYSTEM_FLOW.md | Platform processing flow |
| 01_REPORT_RESPONSE_SPEC.md | Canonical output contract |
| 02_REPORT_BUILDER/* | Report assembly |
| 01_ANALYZE_PIPELINE.md | API orchestration (this document) |

---

# Acceptance Criteria

The Analyze Pipeline is accepted when

✓ One AnalyzeContext is created

✓ Every engine exposes a public interface

✓ Applications API contains no business logic

✓ Report Builder produces ReportResponse

✓ ReportResponse passes validation

✓ Customer Portal consumes only ReportResponse

✓ The pipeline is deterministic

✓ Failures terminate safely

---

# Official Status

Document

Analyze Pipeline

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Architecture