# Portal Empty State Specification

**Location**

```
knowledge/10_integration_layer/04_PORTAL_BINDING/04_EMPTY_STATE.md
```

---

# Purpose

This document defines the canonical empty-state behavior of the BTE Customer Portal.

An empty state occurs when a ReportResponse section contains no meaningful customer-facing information.

The Portal shall present a complete consulting experience without exposing incomplete or placeholder content.

---

# Status

Document Type

UX / Runtime Specification

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Product

---

# Design Principles

Empty-state behavior follows these principles.

- No empty cards
- No placeholder text
- No technical messages
- Graceful degradation
- Preserve reading flow
- Maintain visual balance

---

# Empty State Philosophy

The absence of information is not an error.

It is a presentation decision.

The Portal determines whether a section should be:

- Rendered
- Collapsed
- Hidden
- Replaced by a friendly explanation

---

# Empty State Decision Flow

```
ReportResponse Section

        │

        ▼

Contains meaningful content?

        │

 ┌──────┴───────┐

 │              │

YES            NO

 │              │

 ▼              ▼

Render      Empty Policy

                │

      ┌─────────┼──────────┐

      ▼         ▼          ▼

 Hide      Collapse     Friendly Message
```

---

# Empty State Categories

The Portal recognizes four categories.

```
FULL

PARTIAL

EMPTY

NOT_APPLICABLE
```

---

# Category — FULL

Definition

The section contains complete customer-facing information.

Behavior

Render normally.

---

# Category — PARTIAL

Definition

The section contains useful information but is incomplete.

Behavior

Render available content.

Hide missing elements.

Do not display placeholders.

---

# Category — EMPTY

Definition

The section contains no meaningful information.

Behavior

Hide the section entirely.

Do not reserve layout space.

---

# Category — NOT_APPLICABLE

Definition

The capability does not apply to the current report.

Example

```
domains.business
```

for a report without Business capability.

Behavior

Hide silently.

---

# Section Policies

## Hero

Never empty.

Mandatory.

---

## Executive Summary

Mandatory.

Pipeline fails if missing.

---

## Identity

Mandatory.

Pipeline fails if missing.

---

## Recommendation

Mandatory.

Pipeline fails if missing.

---

## Strengths

If empty

↓

Hide component.

---

## Weaknesses

If empty

↓

Hide component.

---

## Useful God

If unavailable

↓

Hide component.

---

## Domains

Each domain is evaluated independently.

Example

```
Career

FULL

↓

Render

Finance

EMPTY

↓

Hide

Marriage

NOT_APPLICABLE

↓

Hide
```

---

## Evidence

If no evidence exists

↓

Hide expandable section.

---

## Charts

If visualization unavailable

↓

Hide chart component.

No empty graph container.

---

## Knowledge

If references unavailable

↓

Hide knowledge panel.

---

## Appendix

Optional.

Hidden if empty.

---

## Diagnostics

Never shown to customers.

---

# Empty Card Policy

The Portal shall never render

```
┌────────────────────────────┐

(No data available)

└────────────────────────────┘
```

Instead

↓

Hide component.

---

# Friendly Messages

Friendly explanations are permitted only when

- Customer action is required
- Future capability is expected
- Manual review is needed

Examples

Allowed

```
Thông tin này hiện chưa áp dụng cho báo cáo của bạn.
```

Not Allowed

```
null

N/A

No Data

Undefined

TODO
```

---

# Layout Behavior

When a section is hidden

↓

Adjacent sections move upward.

No visual gaps remain.

---

# Component Responsibility

Each component receives

```
ViewModel Section
```

If the ViewModel section is absent

↓

Component is not rendered.

Components never inspect ReportResponse directly.

---

# ViewModel Rules

The Portal Adapter determines emptiness.

React components do not.

```
ReportResponse

↓

Portal Adapter

↓

CanonicalViewModel

↓

React
```

---

# Accessibility

Hidden sections

- must not receive keyboard focus
- must not appear in screen reader navigation
- must not reserve semantic headings

---

# Animation

Hidden components

↓

Fade out or never mount.

Avoid abrupt layout jumps.

---

# Performance

The Portal shall

- avoid rendering empty components
- avoid unnecessary DOM nodes
- reduce layout complexity

---

# Future Extensions

Future capabilities

```
Leadership

Finance

Marriage

Education

Business
```

follow the same empty-state rules.

No capability defines custom empty behavior.

---

# Relationship to Loading

Loading and Empty State are distinct.

```
Loading

↓

Waiting for data

Empty

↓

Data received but no meaningful content
```

They must never be confused.

---

# Relationship to Error State

Error

↓

Request failed.

Empty

↓

Request succeeded.

The Portal shall clearly distinguish these experiences.

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_COMPONENT_MAPPING.md | Component ownership |
| 02_DATA_BINDING.md | Data binding |
| 03_LOADING_STATE.md | Loading UX |
| 04_EMPTY_STATE.md | Empty-state behavior (this document) |
| 05_RENDER_POLICY.md | Rendering rules |

---

# Acceptance Criteria

The Empty State specification is accepted when

✓ No empty cards are rendered

✓ Empty sections do not occupy layout space

✓ Mandatory sections cannot be empty

✓ Optional sections hide gracefully

✓ Components never display placeholder text

✓ ViewModel determines visibility

✓ Reading flow remains uninterrupted

✓ Accessibility is preserved

---

# Official Status

Document

Portal Empty State Specification

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Product