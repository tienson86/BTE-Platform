# Report Builder Pipeline

**Location**

```
knowledge/10_integration_layer/02_REPORT_BUILDER/02_PIPELINE.md
```

---

# Purpose

This document defines the canonical execution pipeline of the Report Builder.

The pipeline transforms validated upstream results into a single canonical `ReportResponse`.

The pipeline is deterministic, stateless, and validation-driven.

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

# Pipeline Philosophy

The Report Builder follows the same pipeline philosophy used throughout the BTE Platform.

```
Input

↓

Validate

↓

Assemble

↓

Normalize

↓

Validate

↓

Output
```

Every stage has one responsibility.

Every stage produces deterministic output.

---

# High-Level Pipeline

```
AnalysisResult

+

InterpretationResult

+

CommercialKnowledgeBundle

        │

        ▼

Stage 1

Input Validation

        ▼

Stage 2

Context Assembly

        ▼

Stage 3

Section Assembly

        ▼

Stage 4

Normalization

        ▼

Stage 5

Cross-Section Validation

        ▼

Stage 6

Contract Validation

        ▼

Stage 7

ReportResponse

        ▼

Portal
```

---

# Stage 1 — Input Validation

## Purpose

Validate all upstream inputs before assembly.

---

## Input

- AnalysisResult
- InterpretationResult
- CommercialKnowledgeBundle

---

## Validation

Check

- null
- schema
- version
- required sections
- traceability
- compatibility

---

## Output

Validated Builder Context

---

## Failure

Pipeline stops immediately.

No ReportResponse produced.

---

# Stage 2 — Context Assembly

## Purpose

Create a unified Builder Context.

Builder Context contains references to all upstream models.

No copying.

No modification.

---

## Responsibilities

Merge references to

- Analysis
- Interpretation
- Commercial Knowledge

Expose a single BuilderContext.

---

## Output

BuilderContext

---

# Stage 3 — Section Assembly

## Purpose

Build every ReportResponse section independently.

---

## Execution

```
BuilderContext

        │

        ▼

Metadata Builder

Customer Builder

Chart Builder

Executive Builder

Identity Builder

Strength Builder

Weakness Builder

UsefulGod Builder

Recommendation Builder

Domain Builder

Evidence Builder

Knowledge Builder

Appendix Builder

Diagnostics Builder
```

Each Builder owns exactly one section.

---

## Parallelism

Independent builders may execute in parallel.

Examples

```
Strength Builder

Weakness Builder

Knowledge Builder

Charts Builder
```

Sequential execution is required only when dependencies exist.

---

## Output

Partial Report Sections

---

# Stage 4 — Normalization

## Purpose

Normalize assembled sections.

---

## Responsibilities

- ordering
- deduplication
- sorting
- grouping
- formatting
- default values

---

## Never

- reinterpret
- calculate
- rewrite conclusions

---

## Output

Normalized Sections

---

# Stage 5 — Cross-Section Validation

## Purpose

Validate consistency between sections.

---

## Examples

Executive Summary references existing Identity.

Recommendations reference existing Useful God.

Evidence exists.

Domains reference valid knowledge.

---

## Validation Rules

No duplicated sections.

No orphan references.

No missing dependencies.

---

## Output

Validated Report Structure

---

# Stage 6 — Contract Validation

## Purpose

Validate the final ReportResponse.

---

## Validation

JSON Schema

Required fields

Version compatibility

Traceability

Section integrity

---

## Output

Canonical ReportResponse

---

## Failure

Reject output.

Return ValidationError.

---

# Stage 7 — Output

## Output

Exactly one object.

```
ReportResponse
```

No alternative model exists.

---

# Pipeline Diagram

```
Inputs

        │

        ▼

Input Validation

        │

        ▼

Builder Context

        │

        ▼

Section Builders

        │

        ▼

Section Collection

        │

        ▼

Normalization

        │

        ▼

Cross Validation

        │

        ▼

Contract Validation

        │

        ▼

ReportResponse
```

---

# Pipeline Responsibilities

| Stage | Responsibility |
|---------|----------------|
| Input Validation | Validate upstream inputs |
| Context Assembly | Create BuilderContext |
| Section Assembly | Build sections |
| Normalization | Normalize data |
| Cross Validation | Validate relationships |
| Contract Validation | Validate schema |
| Output | Return ReportResponse |

---

# Pipeline Data Flow

```
AnalysisResult

        │

        ▼

Builder Context

        │

        ▼

Executive Builder

        │

        ▼

Executive Section

──────────────────────────────

InterpretationResult

        │

        ▼

Recommendation Builder

        │

        ▼

Recommendation Section

──────────────────────────────

Commercial Bundle

        │

        ▼

Identity Builder

        │

        ▼

Identity Section

──────────────────────────────

All Sections

        │

        ▼

Merge

        │

        ▼

Normalize

        │

        ▼

Validate

        │

        ▼

ReportResponse
```

---

# Pipeline Constraints

The pipeline shall never

- access Rule Database
- access Knowledge Database
- calculate BaZi
- execute Rule Matching
- modify upstream objects
- render UI
- persist data

---

# Performance Goals

Pipeline complexity

```
O(n)
```

where

```
n = Report Sections
```

No database access.

No recursive processing.

No network calls.

---

# Error Handling

Input validation failure

↓

Stop

---

Section Builder failure

↓

Reject section

↓

Reject report

---

Normalization failure

↓

Reject report

---

Schema validation failure

↓

Reject report

---

Unexpected exception

↓

Return BuilderError

---

# Extensibility

New capabilities extend the pipeline by adding new Section Builders.

Example

```
Leadership Builder

Finance Builder

Business Builder

Marriage Builder
```

Pipeline stages remain unchanged.

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_ARCHITECTURE.md | Report Builder architecture |
| 02_PIPELINE.md | Execution pipeline (this document) |
| 03_SECTION_BUILDERS.md | Section Builder specifications |
| 04_VALIDATION.md | Validation architecture |

---

# Acceptance Criteria

Pipeline is accepted when

✓ Every stage has one responsibility

✓ BuilderContext exists

✓ Every section has one Builder

✓ Normalization separated from assembly

✓ Validation separated from assembly

✓ ReportResponse validated before output

✓ Pipeline deterministic

✓ Pipeline stateless

✓ Pipeline extensible

---

# Official Status

Pipeline

Architecture Freeze Candidate

Implementation

Pending

Commercial Version

RC1

Owner

BTE Architecture