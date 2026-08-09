# Integration Layer Test Strategy

**Location**

```
knowledge/10_integration_layer/05_TESTING/01_TEST_STRATEGY.md
```

---

# Purpose

This document defines the official testing strategy for the BTE Integration Layer.

The objective is to verify that all architectural layers work together as one deterministic production pipeline.

Testing covers orchestration, integration, contracts, rendering and customer experience.

It does not replace unit testing inside individual engines.

---

# Status

Document Type

Testing Strategy

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE QA Architecture

---

# Testing Philosophy

The Integration Layer is tested from the perspective of a customer request.

Every successful test begins with

```
AnalyzeRequest
```

and ends with

```
ReportResponse
```

The test strategy validates the complete runtime experience.

---

# Testing Pyramid

```
                Human Review
                      ▲
              End-to-End Tests
                      ▲
           Integration Tests
                      ▲
          Contract Validation
                      ▲
              Unit Tests
```

Every level has a different responsibility.

---

# Testing Scope

Integration Layer testing covers

- Applications API
- Analyze Orchestrator
- Analyze Pipeline
- Report Builder
- Portal Binding
- ReportResponse Contract

Individual engine algorithms are outside the scope of this document.

---

# Testing Levels

The Integration Layer defines five testing levels.

```
Level 1

Unit

↓

Level 2

Contract

↓

Level 3

Integration

↓

Level 4

End-to-End

↓

Level 5

Commercial Validation
```

---

# Level 1 — Unit Tests

Purpose

Verify isolated components.

Examples

- Portal Adapter
- Section Builder
- Builder Validator
- Error Mapper

Target

100% deterministic.

---

# Level 2 — Contract Tests

Purpose

Verify compatibility with public contracts.

Validate

- ReportResponse Schema
- AnalyzeRequest Schema
- ErrorResponse Schema
- ViewModel Contract

Failure blocks release.

---

# Level 3 — Integration Tests

Purpose

Verify interaction between components.

Examples

```
Applications API

↓

Analyze Orchestrator

↓

Report Builder
```

and

```
Report Builder

↓

Portal Adapter
```

No mocks beyond engine boundaries.

---

# Level 4 — End-to-End Tests

Purpose

Validate the complete customer flow.

```
Customer

↓

Portal

↓

Applications API

↓

Pipeline

↓

ReportResponse

↓

Portal
```

Expected result

Customer receives a complete consulting report.

---

# Level 5 — Commercial Validation

Purpose

Verify commercial consulting quality.

Examples

- Reading order
- Recommendation quality
- Executive Summary
- Capability presentation
- Commercial wording
- Empty state behavior

Human review is mandatory before release.

---

# Test Categories

The following categories are mandatory.

```
Functional

Integration

Contract

Regression

Performance

Rendering

Accessibility

Commercial
```

---

# Functional Testing

Verify

- Analyze succeeds
- Report builds
- Recommendations appear
- Domain cards appear

---

# Contract Testing

Validate

```
report_response.schema.json
```

Every ReportResponse shall conform.

---

# Integration Testing

Verify

```
Calendar

↓

BaZi

↓

Analysis

↓

Interpretation

↓

Commercial

↓

Report Builder
```

No stage may be skipped.

---

# Portal Testing

Verify

- Component Mapping
- Data Binding
- Loading State
- Empty State
- State Machine

Portal never consumes engine models.

---

# Rendering Testing

Verify

- Component ordering
- Hidden sections
- Expandable cards
- Responsive layout

Rendering shall be deterministic.

---

# Regression Testing

Every release executes

- Golden Dataset
- Snapshot comparison
- Contract validation

No regression is permitted.

---

# Golden Dataset

Golden Cases validate

- Strong charts
- Weak charts
- Mixed charts
- Commercial capabilities
- Empty domains

Golden Dataset is the release baseline.

---

# Performance Testing

Measure

- Pipeline execution time
- Report Builder time
- Portal rendering time
- API latency

Performance goals are defined separately.

---

# Accessibility Testing

Verify

- Keyboard navigation
- Heading hierarchy
- Screen reader support
- Focus management

---

# Error Testing

Verify

- Invalid request
- Invalid birth date
- Engine failure
- Schema failure
- Portal recovery

No partial report shall be displayed.

---

# State Machine Testing

Validate every transition.

```
IDLE

↓

SUBMITTING

↓

PROCESSING

↓

RENDERING

↓

READY
```

Invalid transitions must fail.

---

# Empty State Testing

Verify

- Hidden cards
- Layout compaction
- No placeholder text
- Friendly customer experience

---

# Loading Testing

Verify

- Skeleton rendering
- Loading overlay
- Duplicate submit prevention
- Smooth transition

---

# Compatibility Testing

Verify

- API version compatibility
- ReportResponse compatibility
- Portal compatibility

Backward compatibility is mandatory.

---

# Test Environment

Minimum environments

```
Local

↓

Integration

↓

Release Candidate

↓

Production Validation
```

Each environment executes the same pipeline.

---

# Automation

The following tests shall be automated.

- Unit
- Contract
- Integration
- Regression
- Schema Validation

Commercial review remains manual.

---

# Success Criteria

A build is considered successful when

✓ Unit Tests pass

✓ Contract Tests pass

✓ Integration Tests pass

✓ End-to-End Tests pass

✓ Golden Dataset passes

✓ Portal Rendering passes

✓ Accessibility passes

✓ Commercial Validation passes

---

# Release Gates

Commercial V1 release requires

✓ Engineering PASS

✓ Contract PASS

✓ Golden Dataset PASS

✓ Integration PASS

✓ Portal PASS

✓ Human Consulting PASS

✓ Product Approval

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_REPORT_RESPONSE_SPEC.md | Output Contract |
| 02_REPORT_BUILDER | Assembly |
| 03_API_INTEGRATION | Runtime Pipeline |
| 04_PORTAL_BINDING | Presentation |
| 01_TEST_STRATEGY.md | Testing Strategy (this document) |

---

# Acceptance Criteria

The Integration Layer Test Strategy is accepted when

✓ All testing levels are defined

✓ Every architectural layer is covered

✓ Contracts are validated

✓ End-to-End testing is mandatory

✓ Golden Dataset is part of regression

✓ Commercial validation is included

✓ Human consulting review remains the final quality gate

---

# Official Status

Document

Integration Layer Test Strategy

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE QA Architecture