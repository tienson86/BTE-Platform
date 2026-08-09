# BTE Platform System Flow

**Location**

```
knowledge/10_integration_layer/00_SYSTEM_FLOW.md
```

---

# Purpose

This document defines the official end-to-end processing flow of the BTE Platform.

It describes how a customer's birth information travels through every engine until it becomes a commercial consulting report.

This document is the canonical reference for all integration work.

---

# Design Principles

The platform follows a strict one-direction pipeline.

```
Input

↓

Calculation

↓

Analysis

↓

Interpretation

↓

Integration

↓

Presentation

↓

Delivery
```

Every stage has a single responsibility.

No stage may bypass another stage.

---

# High-Level Architecture

```
                Customer
                    │
                    ▼
          Birth Information
                    │
                    ▼
          Input Validation
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
        Integration Layer
                    │
                    ▼
         ReportResponse
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
 Customer Portal         PDF Export
          │                   │
          └─────────┬─────────┘
                    ▼
                 Customer
```

---

# Phase 1 — Customer Input

## Purpose

Collect customer birth information.

## Input

- Name
- Gender
- Date of Birth
- Time of Birth
- Birth Location
- Calendar Type

## Output

Validated Birth Input

---

# Phase 2 — Calendar Engine

## Purpose

Convert customer birth information into calendar data.

## Responsibilities

- Solar Calendar
- Lunar Calendar
- Julian Date
- JieQi
- Time Zone
- Day Boundary

## Output

Calendar Result

---

# Phase 3 — BaZi Engine

## Purpose

Generate the complete BaZi chart.

## Responsibilities

- Four Pillars
- Heavenly Stems
- Earthly Branches
- Hidden Stems
- Ten Gods
- Five Elements
- Twelve Growth Phases

## Output

BaZi Chart

---

# Phase 4 — Analysis Engine

## Purpose

Perform deterministic chart analysis.

## Responsibilities

- Strength Analysis
- Seasonal Analysis
- Temperature Analysis
- Pattern Detection
- Combination Detection
- Clash Detection
- Useful God Analysis
- Structure Analysis
- Evidence Collection
- Score Calculation

## Output

AnalysisResult

---

# Phase 5 — Interpretation Engine

## Purpose

Convert analytical facts into explainable interpretations.

## Responsibilities

- Rule Matching
- Priority Resolution
- Knowledge Matching
- Sentence Selection
- Placeholder Binding
- Narrative Preparation

## Output

InterpretationResult

---

# Phase 6 — Commercial Knowledge

## Purpose

Enhance Interpretation using approved Commercial Knowledge Units.

## Responsibilities

- Retrieve Knowledge Units
- Validate Allow List
- Resolve Scenarios
- Build Commercial Bundle

## Output

CommercialKnowledgeBundle

---

# Phase 7 — Report Builder (Integration Layer)

## Purpose

Assemble all analytical outputs into one canonical product response.

## Inputs

- AnalysisResult
- InterpretationResult
- CommercialKnowledgeBundle

## Responsibilities

- Merge
- Normalize
- Validate
- Build Sections
- Remove Duplicates
- Apply Ordering
- Validate Contract

## Output

ReportResponse

---

# Phase 8 — Applications API

## Purpose

Expose ReportResponse to product applications.

## Responsibilities

- Receive Request
- Execute Pipeline
- Handle Errors
- Return ReportResponse

## Output

REST Response

---

# Phase 9 — Presentation Layer

## Purpose

Present ReportResponse to end users.

## Consumers

### Customer Portal

- Desktop
- Mobile

### Report Engine

- PDF
- Printable Report

### Future Clients

- Mobile App
- Third-party APIs

Presentation consumes ReportResponse only.

---

# Phase 10 — Persistence

## Purpose

Persist customer results.

## Responsibilities

- History
- Audit
- Version
- Report Archive

Persistence never modifies ReportResponse.

---

# Official Processing Pipeline

```
Customer

↓

Birth Input

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

Customer Portal

↓

Customer
```

---

# Layer Responsibilities

| Layer | Responsibility |
|---------|----------------|
| Calendar | Calendar calculation |
| BaZi | Chart construction |
| Analysis | Analytical facts |
| Interpretation | Human-readable meaning |
| Commercial Knowledge | Consulting enhancement |
| Integration | Assemble ReportResponse |
| Portal | Presentation |
| Report | PDF / Export |

---

# Dependency Rules

Allowed

```
Portal

↓

API

↓

Integration

↓

Interpretation

↓

Analysis

↓

BaZi

↓

Calendar
```

Forbidden

- Portal → Analysis
- Portal → Knowledge
- Portal → Rule Database
- Report Builder → Calculation
- Integration → Rule Matching

---

# Error Flow

```
Validation Error

↓

Return ErrorResponse

↓

Stop Pipeline
```

```
Analysis Failure

↓

Stop Interpretation

↓

Return ErrorResponse
```

```
Interpretation Failure

↓

Skip Report Builder

↓

Return ErrorResponse
```

```
Report Validation Failure

↓

Reject ReportResponse

↓

Return Validation Error
```

---

# Architectural Guarantees

The BTE Platform guarantees:

- Single processing pipeline
- Deterministic output
- Immutable contracts
- Engine independence
- Presentation independence
- Backward compatibility
- Traceable evidence
- Explainable interpretation

---

# Success Criteria

The system flow is considered complete when:

✓ Every engine exposes a public API

✓ Integration Layer produces ReportResponse

✓ Customer Portal consumes ReportResponse only

✓ No mock data exists in production

✓ All Golden Dataset tests pass

✓ Commercial Knowledge is traceable

✓ ReportResponse validates successfully

✓ Portal renders without transformation logic

---

# Official Status

Document Type

Architecture Specification

Status

Approved for Integration Layer

Commercial Version

RC1

Owner

BTE Architecture