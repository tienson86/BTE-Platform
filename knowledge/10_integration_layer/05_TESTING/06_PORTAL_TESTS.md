# Portal Testing Framework

**Location**

```
knowledge/10_integration_layer/05_TESTING/06_PORTAL_TESTS.md
```

---

# Purpose

This document defines the canonical testing framework for the BTE Customer Portal.

Portal Testing verifies that the customer-facing consulting experience is rendered correctly from the canonical ReportResponse.

The objective is to validate presentation quality rather than analytical correctness.

Portal Testing is independent of engine implementation.

---

# Status

Document Type

Testing Architecture

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE QA + Product

---

# Philosophy

Portal Testing validates the customer experience.

It answers one question:

> Does the customer receive the intended consulting experience?

Portal Testing does not validate

- BaZi calculations
- Analysis rules
- Interpretation logic
- Knowledge rules

Those belong to lower testing layers.

---

# Portal Scope

Portal Testing covers

```
ReportResponse

↓

Portal Adapter

↓

Canonical ViewModel

↓

Visibility Policy

↓

React Components

↓

Rendered Portal
```

Everything after ReportResponse belongs to Portal Testing.

---

# Testing Layers

The Portal defines eight testing layers.

```
Component Mapping

↓

Data Binding

↓

Rendering

↓

Loading

↓

Empty State

↓

State Machine

↓

Accessibility

↓

Responsive Layout
```

---

# Layer 1 — Component Mapping

Purpose

Verify that every ReportResponse section maps to the correct Portal component.

Checks

- Hero
- Executive Summary
- Identity
- Recommendation
- Domains
- Evidence
- Charts
- Knowledge

Expected

Every section appears exactly once.

---

# Layer 2 — Data Binding

Purpose

Verify Canonical ViewModel creation.

Checks

```
ReportResponse

↓

Portal Adapter

↓

Canonical ViewModel
```

Validation

- Field mapping
- Null handling
- Optional values
- Hidden sections

---

# Layer 3 — Rendering

Purpose

Verify visual rendering.

Checks

- Component hierarchy
- Reading order
- Section ordering
- Expandable cards
- CTA placement

Rendering must be deterministic.

---

# Layer 4 — Loading

Purpose

Verify runtime loading experience.

Checks

- Loading Overlay
- Skeleton
- Disabled controls
- Transition timing
- Duplicate submit prevention

No blank screen is permitted.

---

# Layer 5 — Empty State

Purpose

Verify empty-state behavior.

Checks

- Hidden cards
- Layout compaction
- No placeholder text
- Friendly messaging
- Visibility Policy

No empty component shall be rendered.

---

# Layer 6 — Runtime State Machine

Purpose

Verify Portal runtime states.

States

```
IDLE

↓

SUBMITTING

↓

PROCESSING

↓

RENDERING

↓

READY

↓

ERROR
```

Checks

- Valid transitions
- Invalid transitions
- Error recovery
- Retry behavior

Exactly one runtime state shall be active.

---

# Layer 7 — Accessibility

Purpose

Verify WCAG-compatible behavior.

Checks

- Keyboard navigation
- Focus order
- Heading hierarchy
- Screen reader support
- ARIA attributes

Accessibility is mandatory.

---

# Layer 8 — Responsive Layout

Purpose

Verify layout across supported devices.

Viewports

```
Desktop

Tablet

Mobile
```

Checks

- Card stacking
- Typography
- Overflow
- CTA visibility
- Reading order

---

# Visual Validation

Visual testing verifies

- Layout consistency
- Card spacing
- Typography
- Icons
- Colors
- Expand/Collapse behavior

Snapshots may be used.

---

# ViewModel Validation

Verify

```
ReportResponse

↓

Portal Adapter

↓

Canonical ViewModel
```

Checks

- Visibility
- Ordering
- Optional fields
- Derived presentation values

No business logic is allowed.

---

# Visibility Policy Testing

Verify

```
Visible

Collapsed

Hidden
```

Examples

```
Career

↓

Visible

Finance

↓

Hidden

Knowledge

↓

Collapsed
```

---

# Error Presentation Testing

Verify

```
Pipeline Failure

↓

ErrorResponse

↓

Friendly Error Screen
```

Portal shall never display

- Stack traces
- Exception messages
- Python errors
- Internal object names

---

# Navigation Testing

Verify

- Anchor navigation
- Scroll behavior
- Expandable sections
- CTA actions

Navigation shall remain deterministic.

---

# Performance Testing

Measure

- Initial render
- ViewModel creation
- Re-render count
- Page interaction

Portal performance shall remain stable across releases.

---

# Regression Testing

Every Portal release executes

- Snapshot comparison
- Component mapping validation
- Responsive validation
- Accessibility validation

Unexpected UI changes require Product approval.

---

# Automation

Automated

- Component tests
- Rendering tests
- Snapshot tests
- Accessibility checks
- Responsive tests

Manual

- Consulting experience review
- Visual polish review
- Commercial UX approval

---

# Test Environments

Portal testing executes in

```
Local

↓

Integration

↓

Release Candidate

↓

Production Verification
```

---

# Success Criteria

Portal Testing passes when

✓ Component Mapping is correct

✓ ViewModel is correct

✓ Rendering matches design

✓ Loading behaves correctly

✓ Empty State behaves correctly

✓ State Machine is valid

✓ Accessibility passes

✓ Responsive layout passes

✓ Error presentation is customer-friendly

---

# Release Gates

Commercial Release requires

✓ Portal Testing PASS

✓ Snapshot PASS

✓ Accessibility PASS

✓ Responsive PASS

✓ Product UX Approval

---

# Future Extensions

Future Portal testing may include

- Dark Mode
- Localization
- Multi-language layouts
- Print layout
- Offline mode
- Progressive rendering

The testing architecture remains unchanged.

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_TEST_STRATEGY.md | Overall testing strategy |
| 02_GOLDEN_DATASET.md | Golden Dataset |
| 03_SNAPSHOT.md | Snapshot validation |
| 04_CONTRACT_VALIDATION.md | Contract validation |
| 05_INTEGRATION_TESTS.md | Integration testing |
| 06_PORTAL_TESTS.md | Portal testing framework (this document) |
| 07_RELEASE_VALIDATION.md | Release validation |

---

# Acceptance Criteria

The Portal Testing Framework is accepted when

✓ Every presentation layer is tested

✓ ReportResponse is the only Portal input

✓ Canonical ViewModel is validated

✓ Portal Runtime State Machine is verified

✓ Accessibility is enforced

✓ Responsive layout is verified

✓ Visual regressions are detected

✓ Commercial consulting experience is preserved

---

# Official Status

Document

Portal Testing Framework

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE QA + Product