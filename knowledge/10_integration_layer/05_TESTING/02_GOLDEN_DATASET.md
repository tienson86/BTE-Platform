# Golden Dataset Framework

**Location**

```
knowledge/10_integration_layer/05_TESTING/02_GOLDEN_DATASET.md
```

---

# Purpose

This document defines the canonical Golden Dataset Framework of the BTE Platform.

The Golden Dataset is the official quality baseline used to validate every production release.

Every Commercial Release Candidate shall pass the Golden Dataset before entering Human Consulting Review.

The Golden Dataset is considered a product asset rather than a testing artifact.

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

The Golden Dataset represents real customer consultation scenarios.

It validates

- analytical correctness
- interpretation consistency
- commercial quality
- report integrity
- customer experience

The objective is not only to verify software correctness, but also consulting quality.

---

# Position in Release Pipeline

```
Developer

↓

Unit Tests

↓

Integration Tests

↓

Golden Dataset

↓

Commercial QA

↓

Human Consulting Review

↓

Product Approval

↓

Commercial Release
```

Every release candidate must pass the Golden Dataset.

---

# Golden Dataset Principles

The dataset shall be

- Deterministic
- Repeatable
- Traceable
- Versioned
- Immutable after release
- Representative of production usage

---

# Dataset Scope

The Golden Dataset validates the complete runtime pipeline.

```
AnalyzeRequest

↓

Applications API

↓

Analyze Pipeline

↓

Report Builder

↓

Portal Binding

↓

ReportResponse
```

The dataset never bypasses the public API.

---

# Dataset Structure

```
golden_dataset/

├── cases/
│
├── snapshots/
│
├── expected/
│
├── reports/
│
├── validators/
│
└── versions/
```

---

# Dataset Components

## Test Cases

Contain

```
AnalyzeRequest
```

Examples

- Birth Information
- Runtime Options
- Locale

---

## Expected Results

Contain

Expected

```
ReportResponse
```

or

Approved validation rules.

---

## Snapshots

Contain

Frozen customer-facing output.

Snapshots detect unintended presentation changes.

---

## Validation Rules

Contain

Acceptance rules for

- Contract
- Business
- Rendering
- Capability

---

## Reports

Generated automatically after execution.

Contain

- PASS
- FAIL
- Warnings
- Metrics

---

# Golden Case Categories

The Golden Dataset shall contain representative production scenarios.

---

## Category 1

Fundamental Charts

Examples

- Strong Day Master
- Weak Day Master
- Balanced Chart

---

## Category 2

Special Structures

Examples

- Follow Structure
- Special Pattern
- Combination Cases

---

## Category 3

Commercial Capabilities

Examples

- Career Selection
- Promotion Readiness
- Leadership
- Business Suitability
- Finance

---

## Category 4

Mixed Cases

Multiple capabilities triggered simultaneously.

---

## Category 5

Edge Cases

Examples

- Boundary solar terms
- Leap months
- Midnight transitions
- Invalid inputs

---

## Category 6

Regression Cases

Previously fixed production issues.

Regression cases shall never be removed.

---

# Golden Dataset Versioning

Every dataset has its own version.

Example

```
GD-1.0.0
```

Dataset versions are independent of

- API version
- Knowledge version
- Commercial version

---

# Dataset Lifecycle

```
Create

↓

Validate

↓

Approve

↓

Freeze

↓

Use in Releases

↓

Archive
```

Frozen datasets are immutable.

---

# Execution Flow

```
Load Case

↓

Execute Analyze Pipeline

↓

Generate ReportResponse

↓

Validate Contract

↓

Validate Commercial Rules

↓

Compare Snapshot

↓

Generate Report

↓

PASS / FAIL
```

---

# Validation Dimensions

Each Golden Case validates

| Dimension | Description |
|-----------|-------------|
| Contract | ReportResponse schema |
| Runtime | Pipeline execution |
| Capability | Correct capability activation |
| Narrative | Executive summary and recommendations |
| Presentation | Portal ViewModel |
| Regression | Snapshot consistency |

---

# Pass Criteria

A Golden Case passes only if

✓ Pipeline succeeds

✓ ReportResponse is valid

✓ Schema validation passes

✓ Capability activation matches expectation

✓ Commercial wording is valid

✓ Snapshot differences are approved

✓ No regression is detected

---

# Failure Categories

## Contract Failure

Schema mismatch.

Immediate failure.

---

## Runtime Failure

Pipeline execution failed.

Immediate failure.

---

## Capability Failure

Incorrect capability activation.

Immediate failure.

---

## Narrative Failure

Commercial recommendations incorrect.

Requires Product review.

---

## Presentation Failure

Unexpected customer-facing output.

Requires review before release.

---

## Regression Failure

Previously approved behavior changed.

Release blocked until resolved or approved.

---

# Snapshot Policy

Snapshots represent approved customer-facing output.

Rules

- Version controlled
- Human reviewed
- Immutable after release

Snapshots are updated only through Product approval.

---

# Dataset Metrics

Every execution records

- Total Cases
- Passed
- Failed
- Warnings
- Execution Time
- Contract Version
- Dataset Version

---

# Dataset Ownership

| Artifact | Owner |
|----------|-------|
| Cases | QA |
| Expected Results | Product |
| Snapshots | Product + Consulting |
| Validators | Engineering |
| Reports | QA Automation |

---

# Release Gates

Commercial Release requires

✓ 100% Golden Cases PASS

✓ No Critical Regression

✓ No Contract Failure

✓ Human Consulting Review PASS

---

# Future Expansion

Future releases may introduce

- Regional datasets
- Language-specific datasets
- Industry datasets
- AI-assisted datasets
- Customer anonymized production datasets

Existing dataset principles remain unchanged.

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_TEST_STRATEGY.md | Overall testing strategy |
| 02_GOLDEN_DATASET.md | Golden Dataset framework (this document) |
| 03_CONTRACT_TESTS.md | Contract validation |
| 04_INTEGRATION_TESTS.md | Integration testing |
| 09_RELEASE_VALIDATION.md | Release quality gates |

---

# Acceptance Criteria

The Golden Dataset Framework is accepted when

✓ Every production release executes the dataset

✓ Dataset is versioned independently

✓ Golden Cases are immutable after approval

✓ Snapshots are human approved

✓ Capability behavior is validated

✓ Commercial quality is verified

✓ Regression detection is mandatory

✓ Human Consulting Review uses Golden Dataset results

---

# Official Status

Document

Golden Dataset Framework

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE QA Architecture