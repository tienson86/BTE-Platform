# Portal Data Binding

**Location**

```
knowledge/10_integration_layer/04_PORTAL_BINDING/02_DATA_BINDING.md
```

---

# Purpose

This document defines the canonical data binding architecture between the ReportResponse contract and the Customer Portal.

The Portal never binds directly to engine outputs.

All rendering is driven by a canonical ViewModel created from the ReportResponse.

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

Portal data binding follows these principles.

- ReportResponse is the only external input
- Canonical ViewModel is the only UI model
- Components never perform business logic
- One-way data flow
- Immutable ViewModel
- Stateless rendering

---

# Data Binding Architecture

```
ReportResponse

        │

        ▼

Portal Adapter

        │

        ▼

Canonical ViewModel

        │

        ▼

UI Components

        │

        ▼

Rendered Customer Experience
```

---

# Data Flow

```
HTTP Response

↓

ReportResponse

↓

Portal Adapter

↓

ViewModel Factory

↓

Canonical ViewModel

↓

Component Props

↓

React Components

↓

Customer
```

No component accesses ReportResponse directly.

---

# Canonical ViewModel

The Portal operates entirely on one runtime object.

```
CanonicalViewModel
```

It represents the complete presentation state of the Result Page.

---

# ViewModel Structure

```
CanonicalViewModel

├── hero

├── executive

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

└── technical
```

Each property maps to one Portal section.

---

# Hero Binding

Source

```
customer

metadata
```

Produces

```
hero
```

Contains

- Customer Name
- Birth Information
- Report Date
- Report Title

---

# Executive Binding

Source

```
executive_summary
```

Produces

```
executive
```

Contains

- Headline
- Summary
- Conclusion
- Confidence

---

# Identity Binding

Source

```
identity
```

Produces

```
identity
```

Contains

- Title
- Description
- Dominant Traits

---

# Strength Binding

Source

```
strengths
```

Produces

```
strengths
```

Contains

- Ordered Strengths
- Supporting Explanation

---

# Weakness Binding

Source

```
weaknesses
```

Produces

```
weaknesses
```

Contains

- Risk
- Mitigation
- Opportunity

---

# Useful God Binding

Source

```
useful_god
```

Produces

```
usefulGod
```

Contains

- Element
- Practical Actions
- Reason

---

# Recommendation Binding

Source

```
recommendations
```

Produces

```
recommendations
```

Primary Recommendation

```
What

Why

How

When

Expected Outcome
```

Secondary recommendations remain collapsible.

---

# Domain Binding

Source

```
domains
```

Produces

```
domains
```

Possible entries

```
career

promotion

leadership

finance

marriage

business

health

education

children
```

Unavailable domains are omitted.

---

# Evidence Binding

Source

```
evidence
```

Produces

```
evidence
```

Evidence remains collapsed by default.

---

# Chart Binding

Source

```
charts
```

Produces

```
charts
```

Contains visualizations only.

---

# Knowledge Binding

Source

```
knowledge
```

Produces

```
knowledge
```

Contains

- References
- Sources
- Commercial Knowledge Units

---

# Technical Binding

Source

```
metadata

diagnostics
```

Produces

```
technical
```

Purpose

Developer information.

Hidden by default.

---

# Binding Rules

Every binding

- maps one source
- produces one ViewModel property
- performs no calculations
- performs no interpretation

---

# Adapter Responsibilities

The Portal Adapter shall

- map ReportResponse
- normalize optional values
- remove null values
- order collections
- hide unavailable sections
- create CanonicalViewModel

The Adapter never performs business logic.

---

# ViewModel Factory

The ViewModel Factory transforms

```
ReportResponse

↓

CanonicalViewModel
```

The Factory is deterministic.

No external services are invoked.

---

# Component Contract

Every component receives

```
Props

↓

ViewModel Section
```

Example

```
ExecutiveSection

↓

executive
```

No component accesses sibling data.

---

# One-Way Data Flow

```
ReportResponse

↓

Portal Adapter

↓

ViewModel

↓

React Props

↓

React Component

↓

Rendered HTML
```

Reverse data flow is prohibited.

---

# Empty State Policy

If a section contains no meaningful content

↓

Do not create ViewModel property

↓

Component is not rendered

Example

```
domains.finance

↓

missing

↓

Finance Card hidden
```

---

# Immutability

The CanonicalViewModel is immutable.

Components may read it.

Components may never modify it.

---

# Error Handling

Binding failures produce

```
BindingError
```

The affected section is omitted.

Remaining sections continue rendering.

The entire page shall not fail because one optional section cannot be bound.

---

# Performance

Binding shall

- allocate ViewModel once
- avoid repeated transformations
- avoid unnecessary copies

Target complexity

```
O(n)
```

where

```
n = number of ReportResponse sections
```

---

# Future Extensions

Future capabilities extend only

```
domains
```

No existing binding shall require modification.

Examples

```
Leadership

Business

Investment

Children

Education
```

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_COMPONENT_MAPPING.md | Component ownership |
| 02_DATA_BINDING.md | Data binding architecture (this document) |
| 03_VIEWMODEL.md | Canonical ViewModel specification |
| 04_RENDER_POLICY.md | Rendering rules |

---

# Acceptance Criteria

The data binding architecture is accepted when

✓ ReportResponse is the only external input

✓ CanonicalViewModel is the only UI model

✓ Components receive only ViewModel sections

✓ Binding performs no business logic

✓ Empty sections are omitted

✓ Binding is deterministic

✓ Binding is immutable

✓ Components never access engine models

---

# Official Status

Document

Portal Data Binding

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Architecture