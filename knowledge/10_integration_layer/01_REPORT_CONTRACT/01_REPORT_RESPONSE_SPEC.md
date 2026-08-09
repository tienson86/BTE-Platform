# ReportResponse Specification

**Location**

```
knowledge/10_integration_layer/01_REPORT_CONTRACT/01_REPORT_RESPONSE_SPEC.md
```

---

# Purpose

This document defines the canonical ReportResponse contract of the BTE Platform.

ReportResponse is the only customer-facing response model produced by the Integration Layer.

All presentation layers, APIs and future clients must consume this contract.

No application is allowed to directly consume internal engine models.

---

# Status

Document Type

Architecture Specification

Status

Frozen after approval

Commercial Version

RC1

Owner

BTE Architecture

---

# Design Goals

ReportResponse is designed to satisfy the following principles.

- Stable
- Deterministic
- Explainable
- Traceable
- Presentation Independent
- Backward Compatible
- Commercial Ready

---

# Position in Architecture

```
AnalysisResult

        +

InterpretationResult

        +

CommercialKnowledgeBundle

        ↓

Report Builder

        ↓

ReportResponse

        ↓

Customer Portal
PDF
Mobile
API
```

---

# Contract Principles

## Single Canonical Contract

There is exactly one official customer-facing response.

```
ReportResponse
```

---

## Immutable

Published fields shall not be removed.

Published field types shall not change.

---

## Extendable

Future versions may add optional fields.

Breaking changes require Major Version.

---

## Traceable

Every customer-facing conclusion must preserve references to:

- analytical evidence
- interpretation
- commercial knowledge
- rule database

---

## Presentation Independent

ReportResponse contains information.

It never contains:

- HTML
- CSS
- UI Components
- Layout
- Typography

---

# Top-Level Structure

```
ReportResponse

├── metadata
├── customer
├── chart
├── executive_summary
├── identity
├── strengths
├── weaknesses
├── useful_god
├── recommendations
├── domains
├── evidence
├── charts
├── knowledge
├── appendix
└── diagnostics
```

---

# Section Specifications

---

# metadata

Purpose

System metadata.

Required

YES

Source

Applications API

Contains

- request_id
- report_version
- generated_at
- locale
- language

---

# customer

Purpose

Customer profile.

Required

YES

Contains

- full_name
- gender
- birth_information

Source

Input

---

# chart

Purpose

Canonical BaZi chart.

Required

YES

Source

BaZi Engine

Contains

- pillars
- hidden stems
- element distribution
- ten gods

---

# executive_summary

Purpose

Primary commercial conclusion.

Required

YES

Source

Interpretation Engine

Commercial Knowledge

Contains

- headline
- summary
- confidence
- evidence_refs

---

# identity

Purpose

Identity narrative.

Required

YES

Contains

- identity title
- consultant description
- dominant characteristics

---

# strengths

Purpose

Commercial strengths.

Source

Analysis

Commercial Knowledge

---

# weaknesses

Purpose

Commercial weaknesses.

Contains

- observations
- risks
- mitigation

---

# useful_god

Purpose

Useful God explanation.

Contains

- useful element
- why
- practical actions

---

# recommendations

Purpose

Action plan.

Contains

Primary Recommendation

Secondary Recommendations

Expected Outcomes

Timeline

Priority

---

# domains

Purpose

Domain-specific consulting.

Examples

Career

Finance

Marriage

Health

Business

Children

Education

Future domains are additive.

---

# evidence

Purpose

Supporting analytical evidence.

Contains

Evidence Units

Confidence

Priority

Traceability

---

# charts

Purpose

Visualization data.

Contains only data.

No rendering information.

---

# knowledge

Purpose

Commercial Knowledge references.

Contains

Knowledge Units

Categories

References

---

# appendix

Purpose

Supplementary information.

Optional.

---

# diagnostics

Purpose

Validation information.

Not customer-facing.

Optional.

---

# Traceability

Every commercial section shall expose

```
evidence_refs

interpretation_refs

knowledge_refs

rule_refs
```

No generated section may lose provenance.

---

# Validation Rules

A valid ReportResponse must satisfy:

✓ metadata exists

✓ customer exists

✓ chart exists

✓ executive_summary exists

✓ recommendations exists

✓ traceability preserved

✓ schema validation passes

---

# Versioning

Current Version

1.0.0

Future Changes

Optional fields only.

Breaking changes require Version 2.

---

# Consumers

Official consumers:

- Customer Portal
- Report Engine
- Mobile Application
- Public API
- Future SDK

No consumer may depend on internal engine models.

---

# Non-Goals

ReportResponse never contains:

- business logic
- calculation
- rules
- HTML
- UI Components
- rendering information

---

# Acceptance Criteria

The contract is accepted when:

✓ Every field has an owner

✓ Every field has a source

✓ Every field has a purpose

✓ Schema validation passes

✓ Portal renders exclusively from ReportResponse

✓ Mock data removed

✓ Golden Dataset compatible

✓ Backward compatibility guaranteed

---

# Official Status

Canonical Product Contract

Version

1.0.0

Status

Architecture Freeze Candidate

Owner

BTE Architecture