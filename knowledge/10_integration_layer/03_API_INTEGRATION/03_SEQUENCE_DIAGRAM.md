# Analyze Pipeline Sequence Diagram

**Location**

```
knowledge/10_integration_layer/03_API_INTEGRATION/03_SEQUENCE_DIAGRAM.md
```

---

# Purpose

This document defines the official interaction sequence of the BTE Analyze Pipeline.

It describes how requests travel between the Customer Portal, Applications API, analytical engines, the Integration Layer, and the final customer response.

This sequence is the canonical runtime interaction of Commercial V1.

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

# Sequence Principles

The Analyze Pipeline follows these principles.

- Single Request
- Single Orchestrator
- Public APIs only
- No Engine-to-Engine coupling
- Deterministic execution
- Fail Fast
- One ReportResponse

---

# Runtime Participants

```
Customer

↓

Customer Portal

↓

Applications API

↓

Analyze Orchestrator

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

Schema Validator

↓

Customer Portal
```

---

# Canonical Sequence

```
Customer
    │
    │ Submit Birth Information
    ▼

Customer Portal
    │
    │ POST /api/v1/analyze
    ▼

Applications API
    │
    │ Create AnalyzeContext
    ▼

Analyze Orchestrator
    │
    │ Validate Request
    ▼

Calendar Engine
    │
    │ CalendarResult
    ▼

BaZi Engine
    │
    │ BaZiChart
    ▼

Analysis Engine
    │
    │ AnalysisResult
    ▼

Interpretation Engine
    │
    │ InterpretationResult
    ▼

Commercial Knowledge
    │
    │ CommercialKnowledgeBundle
    ▼

Report Builder
    │
    │ ReportResponse
    ▼

Schema Validator
    │
    │ ValidationResult
    ▼

Applications API
    │
    │ HTTP 200
    ▼

Customer Portal
    │
    ▼

Customer
```

---

# Detailed Runtime Sequence

## Step 1

Customer submits analysis.

Output

```
AnalyzeRequest
```

---

## Step 2

Customer Portal sends

```
POST /api/v1/analyze
```

to Applications API.

---

## Step 3

Applications API

Creates

```
AnalyzeContext
```

Stores

- Request
- Runtime Options
- Request Metadata

---

## Step 4

Analyze Orchestrator validates request.

Checks

- Birth Date
- Birth Time
- Location
- Calendar Type

Failure

```
400 Bad Request
```

---

## Step 5

Analyze Orchestrator invokes

```
Calendar Engine
```

Receives

```
CalendarResult
```

---

## Step 6

Analyze Orchestrator invokes

```
BaZi Engine
```

Receives

```
BaZiChart
```

---

## Step 7

Analyze Orchestrator invokes

```
Analysis Engine
```

Receives

```
AnalysisResult
```

---

## Step 8

Analyze Orchestrator invokes

```
Interpretation Engine
```

Receives

```
InterpretationResult
```

---

## Step 9

Analyze Orchestrator invokes

```
Commercial Knowledge
```

Receives

```
CommercialKnowledgeBundle
```

---

## Step 10

Analyze Orchestrator invokes

```
Report Builder
```

Input

- AnalysisResult
- InterpretationResult
- CommercialKnowledgeBundle

Output

```
ReportResponse
```

---

## Step 11

Applications API invokes

```
Schema Validator
```

Validation

- JSON Schema
- Required Sections
- Traceability
- Version

Failure

```
500 Internal Server Error
```

---

## Step 12

Applications API returns

```
HTTP 200

ReportResponse
```

to Customer Portal.

---

# AnalyzeContext Evolution

```
AnalyzeContext

├── Request
│
├── CalendarResult
│
├── BaZiChart
│
├── AnalysisResult
│
├── InterpretationResult
│
├── CommercialKnowledgeBundle
│
├── ReportResponse
│
└── Diagnostics
```

Each stage enriches AnalyzeContext.

No stage mutates previous outputs.

---

# Interaction Ownership

| Participant | Responsibility |
|-------------|----------------|
| Customer | Submit birth information |
| Customer Portal | UI + HTTP client |
| Applications API | Public API |
| Analyze Orchestrator | Runtime orchestration |
| Calendar Engine | Calendar calculation |
| BaZi Engine | Chart generation |
| Analysis Engine | Analytical evidence |
| Interpretation Engine | Narrative generation |
| Commercial Knowledge | Commercial enhancement |
| Report Builder | Canonical ReportResponse |
| Schema Validator | Final validation |

---

# Forbidden Interactions

The following interactions are prohibited.

```
Customer Portal

↓

Analysis Engine
```

---

```
Customer Portal

↓

Commercial Knowledge
```

---

```
Report Builder

↓

Rule Database
```

---

```
Interpretation Engine

↓

Customer Portal
```

---

```
Analysis Engine

↓

Portal
```

All interactions must pass through the Analyze Orchestrator.

---

# Failure Sequence

```
Request Validation

↓

400

STOP
```

---

```
Calendar Failure

↓

422

STOP
```

---

```
Analysis Failure

↓

500

STOP
```

---

```
Interpretation Failure

↓

500

STOP
```

---

```
Commercial Knowledge Failure

↓

500

STOP
```

---

```
Report Builder Failure

↓

500

STOP
```

---

```
Schema Validation Failure

↓

500

STOP
```

---

# Timing Order

Execution order is fixed.

```
Validation

↓

Calendar

↓

BaZi

↓

Analysis

↓

Interpretation

↓

Commercial Knowledge

↓

Report Builder

↓

Schema Validation

↓

Response
```

No stage may be skipped.

---

# Runtime Guarantees

The sequence guarantees

✓ One AnalyzeContext

✓ One Orchestrator

✓ One Report Builder

✓ One ReportResponse

✓ One Customer Response

✓ No Engine Coupling

✓ Deterministic execution

✓ Traceable processing

---

# Future Extensions

The following participants may be added in future releases.

```
AI Rewrite Service

Notification Service

Audit Service

Observability Service

Plugin Runtime
```

New participants must be inserted through the Analyze Orchestrator.

No participant may bypass orchestration.

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_ANALYZE_PIPELINE.md | Pipeline stages |
| 02_ENDPOINTS.md | Public API |
| 03_SEQUENCE_DIAGRAM.md | Runtime interaction sequence (this document) |
| 04_ERROR_HANDLING.md | Failure strategy |
| 05_VERSION_NEGOTIATION.md | API compatibility |

---

# Acceptance Criteria

The sequence is accepted when

✓ Every interaction is defined

✓ Every participant has one responsibility

✓ AnalyzeContext is created once

✓ Applications API is the only public entry point

✓ Engines never communicate directly

✓ Report Builder is invoked once

✓ ReportResponse is validated before publication

✓ Portal receives only ReportResponse

---

# Official Status

Document

Analyze Pipeline Sequence Diagram

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Architecture