# Report Builder Validation Framework

**Location**

```
knowledge/10_integration_layer/02_REPORT_BUILDER/04_VALIDATION.md
```

---

# Purpose

This document defines the canonical validation architecture of the Report Builder.

Validation is the final quality gate before a `ReportResponse` is released to any customer-facing application.

Every generated report must pass this validation framework.

No report may bypass validation.

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

# Validation Philosophy

Validation is separated into multiple independent layers.

Each layer validates one concern only.

```
Input

↓

Input Validation

↓

Section Validation

↓

Cross Validation

↓

Contract Validation

↓

Business Validation

↓

Publish
```

---

# Validation Layers

The Report Builder validation consists of six layers.

```
Layer 1

Input Validation

↓

Layer 2

Section Validation

↓

Layer 3

Cross Section Validation

↓

Layer 4

Contract Validation

↓

Layer 5

Business Validation

↓

Layer 6

Release Validation
```

Every layer must pass.

---

# Layer 1 — Input Validation

## Purpose

Validate BuilderContext before assembly begins.

---

## Validate

- AnalysisResult exists
- InterpretationResult exists
- CommercialKnowledgeBundle exists
- Metadata exists
- Version compatibility
- BuilderContext integrity

---

## Failure

Pipeline stops immediately.

---

# Layer 2 — Section Validation

Each Section Builder validates its own output.

Examples

Executive Builder validates

```
executive_summary
```

Recommendation Builder validates

```
recommendations
```

Identity Builder validates

```
identity
```

Every Builder owns its own validation.

---

## Required Checks

- Required fields
- Empty values
- Invalid types
- Invalid references
- Duplicate values
- Traceability

---

# Layer 3 — Cross Section Validation

Purpose

Ensure consistency between sections.

Examples

Executive Summary references Identity.

Recommendations reference Useful God.

Career recommendations reference Career domain.

Evidence exists.

Knowledge references exist.

---

## Validation Rules

No orphan references.

No duplicated recommendations.

No conflicting identities.

No duplicated evidence.

No duplicated knowledge units.

---

# Layer 4 — Contract Validation

Purpose

Validate against

```
report_response.schema.json
```

Checks

- Required properties
- Data types
- Optional fields
- Version compatibility
- JSON Schema compliance

---

# Layer 5 — Business Validation

Purpose

Validate commercial quality.

Checks include

- Executive Summary exists.
- Identity exists.
- Primary Recommendation exists.
- At least one actionable recommendation exists.
- No technical wording exposed.
- No duplicate commercial wording.
- No contradictory recommendations.
- Commercial language only.
- No placeholder text.
- No unresolved template variables.

---

# Layer 6 — Release Validation

Purpose

Ensure the report is suitable for customer delivery.

Validation includes

- Golden Dataset compatibility
- Snapshot compatibility
- Portal rendering compatibility
- PDF compatibility
- API compatibility

---

# Validation Pipeline

```
BuilderContext

↓

Input Validation

↓

Section Validation

↓

Cross Validation

↓

Schema Validation

↓

Business Validation

↓

Release Validation

↓

ReportResponse
```

---

# Validation Severity

Validation issues are classified into four levels.

## INFO

Informational only.

Does not affect publication.

Examples

Unused optional section.

Missing appendix.

---

## WARNING

Quality issue.

Publication allowed.

Examples

Missing optional knowledge.

No chart visualization.

---

## ERROR

Contract violation.

Publication rejected.

Examples

Missing executive summary.

Missing recommendation.

Missing customer.

Schema mismatch.

---

## CRITICAL

System integrity failure.

Pipeline stops immediately.

Examples

BuilderContext invalid.

AnalysisResult missing.

InterpretationResult missing.

Contract version mismatch.

---

# Validation Ownership

| Validation Layer | Owner |
|------------------|-------|
| Input | Report Builder |
| Section | Section Builder |
| Cross Section | Report Builder |
| Contract | Schema Validator |
| Business | Commercial Validator |
| Release | Integration Layer |

---

# Validation Result

Every validation produces

```
ValidationResult

├── status

├── severity

├── errors

├── warnings

├── statistics

└── execution_time
```

---

# Validation Status

Possible values

```
PASS

WARNING

FAILED

CRITICAL
```

---

# Failure Strategy

## PASS

Continue.

---

## WARNING

Continue.

Record warnings.

---

## FAILED

Reject ReportResponse.

Return ValidationError.

---

## CRITICAL

Abort pipeline immediately.

Return SystemError.

---

# Validation Rules

Every ReportResponse must satisfy

✓ metadata

✓ customer

✓ chart

✓ executive_summary

✓ identity

✓ recommendations

✓ schema

✓ traceability

✓ commercial wording

✓ no unresolved placeholders

✓ no duplicate recommendations

✓ no duplicate knowledge units

✓ no orphan references

---

# Validation Metrics

Validation records

- execution time
- number of warnings
- number of errors
- sections validated
- schema version
- report version

Metrics are internal only.

---

# Extensibility

Future validation modules may include

```
Leadership Validation

Finance Validation

Marriage Validation

Business Validation

Health Validation

AI Quality Validation
```

Core validation architecture remains unchanged.

---

# Relationship to Testing

Validation is runtime.

Testing is development-time.

Validation does not replace tests.

Tests verify implementation.

Validation verifies runtime output.

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_ARCHITECTURE.md | Builder architecture |
| 02_PIPELINE.md | Assembly pipeline |
| 03_SECTION_BUILDERS.md | Section Builders |
| 04_VALIDATION.md | Validation framework (this document) |

---

# Acceptance Criteria

The validation framework is accepted when

✓ All validation layers are defined

✓ Every Section Builder validates its own output

✓ JSON Schema validation is mandatory

✓ Business validation exists

✓ Release validation exists

✓ ValidationResult is standardized

✓ Severity model is standardized

✓ Pipeline rejects invalid reports

✓ Commercial quality is enforced

---

# Official Status

Document

Validation Framework

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Architecture