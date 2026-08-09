# Integration Layer

**Location**

```
knowledge/10_integration_layer/
```

---

# Purpose

The Integration Layer is the official orchestration and integration boundary of the BTE Platform.

Its responsibility is to transform the outputs produced by analytical engines into a single canonical product response that can be consumed by customer-facing applications.

The Integration Layer is the only layer allowed to assemble the final ReportResponse.

All presentation layers must consume ReportResponse instead of directly accessing Analysis, Interpretation, or Knowledge engines.

---

# Scope

This package defines:

- Report Contract
- Report Builder
- API Integration
- Portal Binding
- Validation
- Error Handling
- Integration Testing
- Acceptance Rules

This package does **not** implement business logic.

---

# Architecture Position

```
                    Customer Portal
                           │
                           ▼
                    Applications API
                           │
                           ▼
                  Integration Layer
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
 Analysis Engine   Interpretation Engine   Report Engine
```

The Integration Layer sits between product applications and analytical engines.

---

# Design Principles

## One Pipeline

Only one official pipeline exists.

```
Analysis
      ↓
Interpretation
      ↓
Report Builder
      ↓
ReportResponse
```

No alternative assembly pipeline is allowed.

---

## One Report Contract

Customer applications consume only one contract.

```
ReportResponse
```

Applications must never directly consume:

- AnalysisResult
- InterpretationResult
- Engine Models

---

## No Business Logic

The Integration Layer never performs:

- BaZi calculation
- Rule matching
- Pattern recognition
- Score calculation
- Knowledge generation

Those responsibilities belong to analytical engines.

---

## No Rendering

The Integration Layer never:

- renders HTML
- generates UI
- controls layout
- formats typography

Rendering belongs to Portal and Report Presentation.

---

## No Persistence

The Integration Layer does not own:

- database
- storage
- caching
- history

Persistence belongs to application services.

---

## Immutable Contracts

Published ReportResponse fields must remain backward compatible.

Breaking changes require a new major version.

---

## Engine Independence

Integration depends only on public APIs.

No internal engine implementation may be accessed.

---

## Deterministic Output

The same input must always generate the same ReportResponse.

---

# Components

```
10_integration_layer/

README.md

00_SYSTEM_FLOW.md

01_REPORT_CONTRACT/

02_REPORT_BUILDER/

03_API_INTEGRATION/

04_PORTAL_BINDING/

05_TESTING/
```

---

# Data Contracts

Official contracts include:

- ReportResponse
- ValidationResult
- ErrorResponse

ReportResponse is the canonical customer-facing model.

---

# Processing Pipeline

```
Input

↓

Analysis Engine

↓

Interpretation Engine

↓

Report Builder

↓

ReportResponse

↓

Portal
```

---

# Responsibilities

The Integration Layer is responsible for:

- collecting engine outputs
- validating data
- assembling sections
- normalizing values
- building ReportResponse
- validating ReportResponse
- exposing product contracts

---

# Non-Responsibilities

The Integration Layer must never:

- calculate BaZi
- determine Useful God
- score charts
- generate interpretations
- create knowledge
- manage UI
- export PDF layouts

---

# Dependency Graph

```
Customer Portal
        │
        ▼
Applications API
        │
        ▼
Integration Layer
        │
 ┌──────┼────────┐
 ▼      ▼        ▼
Analysis
Interpretation
Report
```

Dependencies are strictly top-down.

Reverse dependencies are prohibited.

---

# Version Policy

Versioning follows Semantic Versioning.

```
Major

Breaking contract changes

Minor

New optional fields

Patch

Documentation
Validation
Bug fixes
```

---

# Directory Structure

```
10_integration_layer/

README.md

00_SYSTEM_FLOW.md

01_REPORT_CONTRACT/

02_REPORT_BUILDER/

03_API_INTEGRATION/

04_PORTAL_BINDING/

05_TESTING/
```

---

# Development Rules

Every implementation must satisfy:

- public API only
- immutable contracts
- deterministic output
- validation before output
- no duplicated mapping
- no business logic leakage

---

# Acceptance Criteria

The Integration Layer is accepted when:

✓ ReportResponse is frozen

✓ Report Builder implemented

✓ API returns ReportResponse

✓ Portal consumes ReportResponse

✓ No mock data remains

✓ Integration tests pass

✓ Golden Dataset passes

✓ Snapshot validation passes

✓ Commercial Portal renders successfully

---

# Official Status

Current Status

Architecture Specification

Implementation

Pending

Commercial Version

RC1

Owner

BTE Architecture
