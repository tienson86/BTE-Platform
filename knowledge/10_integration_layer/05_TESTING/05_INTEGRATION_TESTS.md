# Integration Testing Framework

**Location**

```
knowledge/10_integration_layer/05_TESTING/05_INTEGRATION_TESTS.md
```

---

# Purpose

This document defines the canonical Integration Testing Framework of the BTE Platform.

Integration Testing validates that all architectural layers collaborate correctly through their public contracts.

The objective is to verify end-to-end orchestration without testing internal engine algorithms.

---

# Status

Document Type

Testing Architecture

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE QA Architecture

---

# Philosophy

Integration Testing validates collaboration.

It does not validate internal business rules.

Each component is assumed to have passed its own unit tests.

Integration Testing verifies that components communicate correctly through stable contracts.

---

# Testing Scope

The Integration Layer includes

```
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

Portal Adapter

↓

Customer Portal
```

Every interaction between adjacent components shall be verified.

---

# Integration Levels

The framework defines five levels.

```
Level 1

API Integration

↓

Level 2

Engine Integration

↓

Level 3

Report Integration

↓

Level 4

Portal Integration

↓

Level 5

End-to-End Integration
```

---

# Level 1 — API Integration

Purpose

Verify Applications API orchestration.

Checks

- Request accepted
- Request validation
- AnalyzeContext creation
- Pipeline invocation
- HTTP response generation

Expected Result

```
AnalyzeRequest

↓

ReportResponse
```

---

# Level 2 — Engine Integration

Purpose

Verify sequential engine execution.

Expected order

```
Calendar

↓

BaZi

↓

Analysis

↓

Interpretation

↓

Commercial Knowledge
```

Checks

- Correct execution order
- Public interface usage
- Context propagation
- Immutable outputs

---

# Level 3 — Report Integration

Purpose

Verify Report Builder integration.

Input

```
AnalysisResult

InterpretationResult

CommercialKnowledgeBundle
```

Output

```
ReportResponse
```

Checks

- BuilderContext creation
- Section Builder execution
- Validation
- Report assembly

---

# Level 4 — Portal Integration

Purpose

Verify Portal consumption of ReportResponse.

Pipeline

```
ReportResponse

↓

Portal Adapter

↓

Canonical ViewModel

↓

React Components
```

Checks

- Component mapping
- Data binding
- Visibility policy
- Empty-state handling
- Loading transition

---

# Level 5 — End-to-End Integration

Purpose

Validate the complete production flow.

```
Customer

↓

Customer Portal

↓

Applications API

↓

Analyze Pipeline

↓

Report Builder

↓

Portal

↓

Customer
```

The customer receives a complete consulting report.

---

# Integration Scenarios

The following scenarios are mandatory.

---

## Scenario 1

Valid analysis request.

Expected

PASS

---

## Scenario 2

Invalid request.

Expected

400 Bad Request

---

## Scenario 3

Calendar failure.

Expected

422

---

## Scenario 4

Engine failure.

Expected

500

---

## Scenario 5

Schema validation failure.

Expected

Pipeline stops.

---

## Scenario 6

Portal rendering.

Expected

Complete consulting page.

---

# Data Flow Validation

Verify runtime objects.

```
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

ReportResponse

↓

CanonicalViewModel
```

Each object shall be created exactly once.

---

# Control Flow Validation

Verify execution order.

```
Applications API

↓

Analyze Orchestrator

↓

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

↓

Portal Adapter
```

No stage may be skipped.

---

# Contract Validation

Every boundary validates

- Request contract
- Response contract
- Error contract

Contract failures terminate the pipeline.

---

# Runtime Validation

Verify

- AnalyzeContext lifecycle
- BuilderContext lifecycle
- PortalRuntimeContext lifecycle

All runtime contexts are destroyed after request completion.

---

# Error Integration

Every error path shall be tested.

```
Request Error

↓

400

Calendar Error

↓

422

Engine Error

↓

500

Validation Error

↓

500
```

No partial report is returned.

---

# Portal Validation

Verify

- Loading State
- Empty State
- Ready State
- Error State
- State Machine transitions

The Portal consumes only the Canonical ViewModel.

---

# Performance Validation

Measure

- API latency
- Pipeline duration
- Report Builder duration
- Portal render duration

Measurements are recorded for regression comparison.

---

# Regression Validation

Every integration test executes

- Golden Dataset
- Snapshot comparison
- Contract validation

Unexpected differences block release.

---

# Test Data

Integration tests shall use

- Golden Dataset
- Approved snapshots
- Canonical AnalyzeRequest examples

Synthetic data shall be clearly identified.

---

# Test Environments

Supported environments

```
Local

↓

Integration

↓

Release Candidate

↓

Production Verification
```

The same integration suite executes in every environment.

---

# Automation

The following tests are fully automated.

- API Integration
- Engine Integration
- Report Integration
- Portal Integration
- Contract Validation
- Snapshot Comparison

Human Consulting Review remains manual.

---

# Success Criteria

Integration Testing passes only when

✓ Every architectural layer executes

✓ Execution order is correct

✓ Public contracts remain valid

✓ ReportResponse is generated

✓ Portal renders correctly

✓ Runtime contexts are released

✓ No regression is detected

✓ Golden Dataset passes

---

# Release Gates

Commercial Release requires

✓ Integration PASS

✓ Contract PASS

✓ Snapshot PASS

✓ Golden Dataset PASS

✓ Human Consulting PASS

✓ Product Approval

---

# Future Extensions

Future integration testing may include

- Distributed deployment
- Parallel pipeline execution
- AI Rewrite integration
- Plugin Runtime
- Multi-language validation
- Multi-region deployment

The integration architecture remains unchanged.

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_TEST_STRATEGY.md | Overall testing strategy |
| 02_GOLDEN_DATASET.md | Golden Dataset |
| 03_SNAPSHOT.md | Snapshot framework |
| 04_CONTRACT_VALIDATION.md | Contract validation |
| 05_INTEGRATION_TESTS.md | Integration testing framework (this document) |
| 06_PORTAL_TESTS.md | Portal testing |

---

# Acceptance Criteria

The Integration Testing Framework is accepted when

✓ Every architectural layer is covered

✓ API orchestration is verified

✓ Engine interactions are verified

✓ Report Builder integration is verified

✓ Portal integration is verified

✓ Runtime lifecycle is validated

✓ Error paths are tested

✓ End-to-End flow is verified

---

# Official Status

Document

Integration Testing Framework

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE QA Architecture