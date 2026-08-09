# ReportResponse Schema Diagram

**Location**

```
knowledge/10_integration_layer/01_REPORT_CONTRACT/01A_REPORT_SCHEMA_DIAGRAM.md
```

---

# Purpose

This document provides the canonical structural diagram of the BTE `ReportResponse`.

Unlike the specification document, this file focuses on the overall architecture and relationships between sections.

It serves as the primary visual reference for:

- Integration Layer
- Applications API
- Customer Portal
- Report Engine
- Mobile Clients
- Future SDKs

---

# Status

Document Type

Architecture Diagram

Status

Frozen after Contract Approval

Commercial Version

RC1

Owner

BTE Architecture

---

# Canonical ReportResponse

```
ReportResponse
│
├── metadata
│
├── customer
│
├── chart
│
├── executive_summary
│
├── identity
│
├── strengths
│
├── weaknesses
│
├── useful_god
│
├── recommendations
│
├── domains
│   ├── career
│   ├── finance
│   ├── marriage
│   ├── health
│   ├── children
│   ├── education
│   ├── business
│   └── future_extensions
│
├── evidence
│
├── charts
│
├── knowledge
│
├── appendix
│
└── diagnostics
```

---

# ReportResponse Hierarchy

```
ReportResponse

├─────────────────────────────────────
│ Core Product Information
├─────────────────────────────────────

metadata

customer

chart

──────────────────────────────────────

Executive Layer

executive_summary

identity

recommendations

──────────────────────────────────────

Consultation Layer

strengths

weaknesses

useful_god

domains

──────────────────────────────────────

Evidence Layer

evidence

knowledge

──────────────────────────────────────

Presentation Layer

charts

appendix

──────────────────────────────────────

System Layer

diagnostics
```

---

# Section Ownership

| Section | Owner |
|----------|-------|
| metadata | Applications API |
| customer | Input Layer |
| chart | BaZi Engine |
| executive_summary | Interpretation Engine |
| identity | Commercial Knowledge |
| strengths | Analysis + Commercial Knowledge |
| weaknesses | Analysis + Commercial Knowledge |
| useful_god | Analysis + Commercial Knowledge |
| recommendations | Interpretation + Commercial Knowledge |
| domains | Commercial Knowledge |
| evidence | Analysis Engine |
| charts | Report Builder |
| knowledge | Commercial Knowledge |
| appendix | Report Builder |
| diagnostics | Integration Layer |

---

# Upstream Sources

```
Input
    │
    ▼
Customer

Calendar Engine
    │
    ▼
Chart

BaZi Engine
    │
    ▼
Chart

Analysis Engine
    │
    ▼
Evidence

Interpretation Engine
    │
    ▼
Executive Summary

Commercial Knowledge
    │
    ▼
Identity
Recommendations
Domains
```

---

# Integration Flow

```
AnalysisResult
        │
        │
        ▼

InterpretationResult
        │
        │
        ▼

CommercialKnowledgeBundle
        │
        │
        ▼

Report Builder
        │
        ▼

ReportResponse
```

---

# Downstream Consumers

```
ReportResponse
        │
        ├───────────────► Customer Portal
        │
        ├───────────────► PDF Export
        │
        ├───────────────► Mobile App
        │
        ├───────────────► Public API
        │
        └───────────────► Future SDK
```

No downstream consumer may access internal engine models.

---

# Traceability Model

Every commercial section preserves traceability.

```
Executive Summary

│

├── evidence_refs

├── interpretation_refs

├── knowledge_refs

└── rule_refs
```

The same applies to:

- Identity
- Recommendations
- Domain Sections

---

# Customer Reading Flow

```
Executive Summary

↓

Identity

↓

Strengths

↓

Weaknesses

↓

Useful God

↓

Career

↓

Finance

↓

Marriage

↓

Health

↓

Recommendations

↓

Evidence

↓

Charts

↓

Knowledge

↓

Appendix
```

This is the canonical commercial reading order.

---

# ReportResponse Dependency Graph

```
metadata

customer

chart

        │

        ▼

executive_summary

        │

        ▼

identity

        │

        ▼

recommendations

        │

        ▼

domains

        │

        ▼

evidence

        │

        ▼

charts

        │

        ▼

knowledge
```

Dependencies always flow downward.

Reverse dependencies are prohibited.

---

# Optional vs Required Sections

## Required

- metadata
- customer
- chart
- executive_summary
- identity
- recommendations

## Recommended

- strengths
- weaknesses
- useful_god
- evidence
- charts

## Optional

- appendix
- diagnostics

## Extensible

- domains

Future domain modules may extend this section without changing the top-level contract.

---

# Extension Points

The following sections support future growth without breaking compatibility.

```
domains

knowledge

charts

appendix

diagnostics
```

New domain capabilities (Career, Finance, Business, Health...) are added inside `domains`.

---

# ReportResponse Lifecycle

```
AnalysisResult

        +

InterpretationResult

        +

CommercialKnowledgeBundle

↓

Report Builder

↓

Validation

↓

ReportResponse

↓

Customer Portal

↓

Customer
```

---

# Architectural Guarantees

This schema guarantees:

- Single canonical contract
- Stable hierarchy
- Engine independence
- Presentation independence
- Commercial scalability
- Backward compatibility
- Evidence traceability

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| README.md | Integration Layer overview |
| 00_SYSTEM_FLOW.md | End-to-end processing pipeline |
| 00A_ARCHITECTURE_DECISIONS.md | Architecture rationale |
| 01_REPORT_RESPONSE_SPEC.md | Detailed contract specification |
| 01A_REPORT_SCHEMA_DIAGRAM.md | Structural overview (this document) |
| 02_FIELD_MAPPING.md | Field-to-source mapping |
| 03_VERSIONING.md | Contract evolution rules |

---

# Official Status

Document

Canonical Schema Diagram

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Architecture