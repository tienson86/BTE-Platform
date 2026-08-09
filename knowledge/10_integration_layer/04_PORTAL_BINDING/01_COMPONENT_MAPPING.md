# Portal Component Mapping

**Location**

```
knowledge/10_integration_layer/04_PORTAL_BINDING/01_COMPONENT_MAPPING.md
```

---

# Purpose

This document defines the canonical mapping between the ReportResponse contract and Customer Portal components.

The Customer Portal is a presentation layer only.

It consumes the canonical `ReportResponse` and renders a commercial consulting experience.

The Portal shall never access engine models directly.

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

# Design Principles

Portal Binding follows these principles.

- ReportResponse Only
- No Engine Models
- One-way Binding
- Presentation Only
- Stateless Rendering
- Component Isolation
- Backward Compatible

---

# Architecture

```
Customer Portal

        │

        ▼

Portal Adapter

        │

        ▼

Canonical ViewModel

        │

        ▼

React Components

        │

        ▼

Customer
```

The Portal never consumes AnalysisResult, InterpretationResult or BuilderContext.

---

# Binding Pipeline

```
ReportResponse

↓

Portal Adapter

↓

Canonical ViewModel

↓

Component Mapping

↓

React Components

↓

Rendered Result Page
```

---

# Mapping Overview

| ReportResponse Section | Portal Component |
|------------------------|------------------|
| metadata | Technical Information |
| customer | Customer Header |
| chart | BaZi Chart Card |
| executive_summary | Executive Summary Card |
| identity | Identity Card |
| strengths | Strength Card |
| weaknesses | Weakness Card |
| useful_god | Useful God Card |
| recommendations | Recommendation Card |
| domains.career | Career Assessment Card |
| domains.finance | Finance Assessment Card |
| domains.marriage | Marriage Assessment Card |
| domains.health | Health Assessment Card |
| evidence | Evidence Card |
| charts | Visualization Card |
| knowledge | Knowledge Reference Card |
| appendix | Appendix Panel |
| diagnostics | Hidden (Developer Only) |

---

# Result Page Layout

```
Hero

↓

Executive Summary

↓

Identity

↓

Career Assessment

↓

Primary Recommendation

↓

Strengths

↓

Weaknesses

↓

Useful God

↓

Other Domain Cards

↓

Evidence

↓

Charts

↓

Knowledge References

↓

Appendix
```

This is the canonical customer reading order.

---

# Hero Component

Consumes

```
customer

metadata
```

Displays

- Customer Name
- Birth Information
- Report Date

Technical identifiers remain collapsed.

---

# Executive Summary Component

Consumes

```
executive_summary
```

Displays

- Headline
- Summary
- Key Conclusion

Maximum visual priority.

---

# Identity Component

Consumes

```
identity
```

Displays

- Identity Title
- Description
- Dominant Traits

Commercial language only.

---

# Recommendation Component

Consumes

```
recommendations
```

Displays

Primary Recommendation

Structured as

```
What

Why

How

When

Expected Outcome
```

Secondary recommendations remain collapsible.

---

# Domain Components

Consumes

```
domains
```

Examples

```
Career

Promotion

Leadership

Finance

Marriage

Business

Health
```

Each domain renders independently.

Unavailable domains are hidden.

---

# Strength Component

Consumes

```
strengths
```

Displays

- Strength
- Supporting explanation

---

# Weakness Component

Consumes

```
weaknesses
```

Displays

- Risk
- Mitigation
- Opportunity

Commercial wording only.

---

# Useful God Component

Consumes

```
useful_god
```

Displays

- Element
- Practical Actions
- Explanation

---

# Evidence Component

Consumes

```
evidence
```

Purpose

Provide supporting evidence.

Hidden by default.

Expandable.

---

# Charts Component

Consumes

```
charts
```

Purpose

Visual explanation only.

Not primary reading.

---

# Knowledge Component

Consumes

```
knowledge
```

Purpose

Reference material.

Not part of the executive consultation.

---

# Hidden Components

Never shown to customers

```
diagnostics
```

Reserved for

- Debugging
- QA
- Internal Validation

---

# Empty State Policy

If a section is empty

↓

Hide component.

No empty placeholder cards.

Examples

```
domains.health

↓

Not Available

↓

Hidden
```

---

# Component Independence

Each Portal component renders independently.

Example

```
Identity

↓

No dependency on

↓

Strength Component
```

Component failures must not affect siblings.

---

# ViewModel

Portal components consume only

```
Canonical ViewModel
```

The ViewModel is created by the Portal Adapter.

Components never read ReportResponse directly.

---

# Adapter Responsibilities

Portal Adapter

- Read ReportResponse
- Normalize optional values
- Create ViewModel
- Hide empty sections
- Preserve ordering

The Adapter performs no business logic.

---

# Forbidden Dependencies

Portal components shall never access

```
AnalysisResult

InterpretationResult

CommercialKnowledgeBundle

BuilderContext

AnalyzeContext

Knowledge Database

Rule Database
```

Only the ViewModel may be consumed.

---

# Rendering Rules

Rendering must be

- Deterministic
- Stateless
- Idempotent

The same ReportResponse always produces the same UI.

---

# Extension Strategy

Future capabilities extend only

```
domains
```

New React components may be added without modifying existing bindings.

Examples

```
Leadership Card

Business Card

Education Card

Children Card
```

---

# Accessibility

Portal components shall

- Support keyboard navigation
- Preserve heading hierarchy
- Maintain semantic HTML
- Support screen readers

Accessibility is independent of ReportResponse.

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_REPORT_RESPONSE_SPEC.md | Canonical output contract |
| 02_REPORT_BUILDER/* | Report assembly |
| 03_API_INTEGRATION/* | API orchestration |
| 01_COMPONENT_MAPPING.md | Portal binding (this document) |

---

# Acceptance Criteria

The Portal Binding is accepted when

✓ Portal consumes only ReportResponse

✓ Portal Adapter creates Canonical ViewModel

✓ Components never access engine models

✓ Empty sections are hidden

✓ Reading order is standardized

✓ Components are independent

✓ Rendering is deterministic

✓ Future domains require no architectural changes

---

# Official Status

Document

Portal Component Mapping

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Architecture