# UI_IMPLEMENTATION_GUIDE.md

Version: 1.0
Status: OFFICIAL
Owner: BTE UI Architecture

Depends on

- 00_DESIGN_SYSTEM_INDEX.md
- PACK_01_DESIGN_PRINCIPLES.md
- PACK_02_LAYOUT_SYSTEM.md
- PACK_03_COMPONENT_STANDARD.md
- PACK_04_UI_PRESENTATION_STANDARD.md
- PACK_05_ACCESSIBILITY.md

---

# 1. Purpose

This document describes the official implementation workflow for every User Interface within the BTE Platform.

It explains how developers and Cursor should build UI while complying with the Design System.

This document is implementation-oriented.

The Design System defines WHAT.

This guide defines HOW.

---

# 2. Implementation Philosophy

Implementation should always prioritize

Consistency

↓

Reusability

↓

Maintainability

↓

Performance

↓

Visual Polish

Never sacrifice architecture for short-term convenience.

---

# 3. Official Development Workflow

Every UI feature follows the same workflow.

```

Requirement

↓

Architecture Review

↓

Design System Review

↓

Implementation

↓

Testing

↓

Compliance Validation

↓

Merge

↓

Release

```

Implementation must never skip Design System Review.

---

# 4. Before Writing Code

Before implementing any screen,

verify

✓ Design Principles

✓ Layout System

✓ Component Standard

✓ Presentation Standard

✓ Accessibility

Only after these checks may implementation begin.

---

# 5. Folder Structure

Recommended structure

```

src/

components/
layout/
pages/
presentation/
hooks/
providers/
constants/
types/
utils/
styles/

```

Avoid feature duplication.

---

# 6. Component Organization

Components should be organized by responsibility.

Example

```

components/

Card/

Button/

Badge/

Table/

Timeline/

Insight/

Recommendation/

```

Never organize by page.

---

# 7. Layout Organization

```

layout/

AppLayout

Sidebar

Header

ContentArea

Grid

Section

```

Layouts are shared across the application.

---

# 8. Presentation Layer

Presentation Layer contains

```

presentation/

adapters/

view_models/

formatters/

grouping/

sorting/

preview/

```

Business Engines never import React.

React never imports Business Engines.

---

# 9. ViewModel Rules

Components receive

ViewModels only.

Never pass raw Engine Models.

Never expose Business Models to UI.

---

# 10. Component Rules

Each component should

have one responsibility

accept typed props

remain reusable

remain stateless whenever possible

avoid side effects

---

# 11. State Management

Preferred hierarchy

Server State

↓

Presentation State

↓

UI State

↓

Component Local State

Business state should never exist inside components.

---

# 12. Styling Rules

Use only

Official spacing

Official typography

Official colors

Official radius

Official shadows

Never hardcode values.

---

# 13. Responsive Rules

Implement

Desktop first

↓

Tablet

↓

Mobile

Never implement Mobile separately.

Maintain identical information hierarchy.

---

# 14. Dynamic Content

Always use

Preview

↓

Expand

↓

Full Content

Never render unlimited paragraphs.

---

# 15. Loading

Loading uses

Skeleton

not

Spinner

whenever layout already exists.

---

# 16. Empty State

Every page supports

Empty

Loading

Error

Success

Never assume data always exists.

---

# 17. Error Handling

Display

Reason

↓

Recovery

↓

Retry

Never expose technical exceptions directly.

---

# 18. Performance

Avoid

unnecessary rendering

duplicate computation

deep component trees

large prop chains

Prefer memoization only when needed.

---

# 19. Accessibility

Every interactive element supports

Keyboard

Focus

Screen Reader

ARIA

Color Contrast

Accessibility is mandatory.

---

# 20. Code Review Checklist

Before merge verify

✓ Shared Layout

✓ Shared Components

✓ Shared Presentation

✓ Shared ViewModels

✓ Responsive

✓ Accessibility

✓ Stable Rendering

✓ No Business Logic

✓ No Duplicate Components

---

# 21. Cursor Workflow

Cursor should always

Read Specification

↓

Locate Existing Components

↓

Reuse Components

↓

Implement

↓

Run Tests

↓

Validate Design System

↓

Submit

Cursor should never create duplicate UI patterns.

---

# 22. Refactoring Rules

Refactoring should

reduce duplication

improve consistency

reuse shared components

preserve architecture

avoid unnecessary redesign

---

# 23. Creating New Components

Before creating a component

Check

PACK_03_COMPONENT_STANDARD

If similar component exists

Reuse it.

Only create new components when absolutely necessary.

New components must be documented.

---

# 24. Updating Existing Components

Changes must preserve

API compatibility

Visual consistency

Accessibility

Documentation

Breaking changes require Design System approval.

---

# 25. Pull Request Requirements

Every UI Pull Request includes

Purpose

Design System Reference

Screenshots

Responsive Verification

Accessibility Check

Performance Notes

Review Checklist

---

# 26. Implementation Anti-Patterns

Never

❌ Hardcode spacing

❌ Hardcode colors

❌ Duplicate components

❌ Mix business logic

❌ Read Engine Models

❌ Stretch layouts

❌ Render raw data

❌ Ignore responsive behavior

---

# 27. Compliance Workflow

Every implementation is validated against

PACK_01

↓

PACK_02

↓

PACK_03

↓

PACK_04

↓

PACK_05

Only compliant implementations may be merged.

---

# 28. Result Page UI V1.0 (Frozen)

Official Result Page implementation:

```
applications/customer_portal/src/screens/result/
```

Architecture (FROZEN)

```
ResultPage → Zones → Rows → Grid → Cards → ViewModels → Presentation Adapter
```

Zone reading order (FROZEN)

```
Context → Summary → Analysis → Visualization → Recommendation → Interpretation → Knowledge
```

Layout Patterns

| Pattern | Zone |
|---------|------|
| LP-001 | Summary |
| LP-003 | Analysis |
| LP-004 | Visualization |
| LP-005 | Recommendation |
| LP-006 | Interpretation |
| LP-007 | Knowledge |

Baselines

| Layer | Sprint |
|-------|--------|
| Architecture | A |
| Presentation | B |
| Quality | C |
| Release / Freeze | D |

Mandatory references

- PACK_01 … PACK_07
- RESULT_PAGE_LAYOUT_GALLERY.md
- UI_V1_FREEZE_CHECKLIST.md
- FINAL_UI_V1_RELEASE_REPORT.md

After UI V1.0 freeze, do not change zone order, row heights, grid contracts, or layout patterns without a new major Design System version.

---

# 29. Future Evolution

The implementation guide evolves together with the Design System.

Documentation must always be updated before implementation.

Implementation never defines standards.

The Design System defines standards.

---

END OF DOCUMENT