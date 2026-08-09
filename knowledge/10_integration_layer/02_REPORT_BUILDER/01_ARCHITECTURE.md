# Report Builder Architecture

**Location**

```
knowledge/10_integration_layer/02_REPORT_BUILDER/01_ARCHITECTURE.md
```

---

# Purpose

This document defines the official architecture of the Report Builder.

The Report Builder is the final assembly component of the BTE Platform.

Its responsibility is to transform validated analytical outputs into one canonical `ReportResponse`.

The Report Builder is **not** an analytical engine.

It never performs calculation, interpretation, or knowledge generation.

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

# Position in System Architecture

```
                Analysis Engine
                       │
                       ▼

          AnalysisResult
                       │

                       ▼

          Interpretation Engine
                       │
                       ▼

     InterpretationResult
                       │

                       ▼

     Commercial Knowledge
                       │
                       ▼

 CommercialKnowledgeBundle
                       │
                       ▼

=============================
     REPORT BUILDER
=============================

                       │
                       ▼

      Canonical ReportResponse

                       │
                       ▼

 Customer Portal
 PDF
 Mobile
 Public API
```

Report Builder is the final integration boundary before presentation.

---

# Mission

The Report Builder shall:

- Assemble
- Normalize
- Validate
- Organize
- Produce

It shall never:

- Calculate
- Analyze
- Interpret
- Match Rules
- Retrieve Knowledge
- Render UI

---

# Design Principles

## Single Responsibility

Report Builder performs assembly only.

Business logic belongs upstream.

---

## Deterministic

Given the same inputs:

```
AnalysisResult

+

InterpretationResult

+

CommercialKnowledgeBundle
```

the Builder must always produce the same ReportResponse.

---

## Stateless

The Builder stores no data.

No cache.

No persistence.

No history.

---

## Immutable Input

Inputs are read-only.

Builder never modifies upstream objects.

---

## Immutable Output Contract

Builder always produces the canonical ReportResponse.

No alternative response model exists.

---

## Composition over Calculation

Builder composes existing information.

Builder never creates new analysis.

---

# Inputs

## AnalysisResult

Provided by

Analysis Engine

Contains

- analytical evidence
- scores
- strengths
- weaknesses
- chart facts

---

## InterpretationResult

Provided by

Interpretation Engine

Contains

- executive summary
- interpretation
- recommendations
- explanations

---

## CommercialKnowledgeBundle

Provided by

Commercial Knowledge Layer

Contains

- identity
- consulting wording
- capability outputs
- domain guidance

---

# Output

Exactly one object.

```
ReportResponse
```

Defined by

```
01_REPORT_CONTRACT/
```

---

# Internal Architecture

```
                Report Builder
                        │

        ┌───────────────┼────────────────┐

        ▼               ▼                ▼

Input Validation   Section Builders   Output Validation

                        │

                        ▼

              ReportResponse
```

Builder orchestration is centralized.

Section construction is delegated.

---

# Section Builder Architecture

```
Report Builder
│
├── Metadata Builder
├── Customer Builder
├── Chart Builder
├── Executive Builder
├── Identity Builder
├── Strength Builder
├── Weakness Builder
├── UsefulGod Builder
├── Recommendation Builder
├── Domain Builder
├── Evidence Builder
├── Knowledge Builder
├── Appendix Builder
└── Diagnostics Builder
```

Each Builder owns exactly one section.

No shared ownership.

---

# Processing Responsibilities

## Input Validation

Validate

- required inputs
- schema
- version
- references

---

## Section Assembly

Each section builder receives only the data it requires.

Example

```
Executive Builder

↓

InterpretationResult

+

Commercial Bundle
```

---

## Normalization

Builder performs

- ordering
- deduplication
- formatting
- grouping

Builder never changes meaning.

---

## Traceability

Every generated section preserves

```
evidence_refs

interpretation_refs

knowledge_refs

rule_refs
```

Traceability is mandatory.

---

## Output Validation

Before publishing

ReportResponse must satisfy

- schema validation
- required fields
- section integrity
- traceability integrity

---

# Dependency Rules

Allowed

```
Report Builder

↓

AnalysisResult

↓

InterpretationResult

↓

CommercialKnowledgeBundle
```

Forbidden

```
Report Builder

↓

Rule Database

↓

Calendar Engine

↓

BaZi Engine

↓

Knowledge Database
```

---

# Data Flow

```
AnalysisResult

        │

        ▼

InterpretationResult

        │

        ▼

Commercial Bundle

        │

        ▼

Input Validation

        │

        ▼

Section Builders

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

# Error Handling

Input validation failure

↓

Stop

---

Section Builder failure

↓

Reject ReportResponse

---

Schema validation failure

↓

Reject output

---

Traceability failure

↓

Reject output

---

# Performance Goals

Report Builder should perform

- no database queries
- no heavy calculations
- no rule evaluation

Expected complexity

```
O(n)
```

where

```
n = total sections
```

---

# Extension Strategy

Future capabilities extend Builder by adding new Section Builders.

Example

```
Leadership Builder

Finance Builder

Business Builder

Marriage Builder
```

Existing Builders remain unchanged.

---

# Builder Lifecycle

```
Receive Inputs

↓

Validate

↓

Build Sections

↓

Merge

↓

Normalize

↓

Validate

↓

Return ReportResponse
```

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| README.md | Integration overview |
| 00_SYSTEM_FLOW.md | End-to-end flow |
| 00A_ARCHITECTURE_DECISIONS.md | Architecture rationale |
| 01_REPORT_RESPONSE_SPEC.md | Output contract |
| 02_FIELD_MAPPING.md | Data lineage |
| 03_VERSIONING.md | Contract evolution |
| 01_ARCHITECTURE.md | Report Builder architecture (this document) |

---

# Acceptance Criteria

The Report Builder architecture is accepted when

✓ Builder contains no business logic

✓ Every section has one owner

✓ Input validation exists

✓ Output validation exists

✓ ReportResponse is the only output

✓ Traceability is preserved

✓ Builder is stateless

✓ Builder depends only on public contracts

✓ Portal consumes ReportResponse without transformation

---

# Official Status

Architecture

Frozen Candidate

Implementation

Pending

Commercial Version

RC1

Owner

BTE Architecture