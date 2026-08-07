# RESULT_PAGE_REFACTOR_TASK.md

Version: 1.0

Status: OFFICIAL

Owner: BTE UI Architecture

Priority: CRITICAL

Estimated Effort: Large Refactor

---

# Purpose

This document defines the official execution plan for refactoring the BTE Result Page.

The objective is not to improve CSS.

The objective is to rebuild the Result Page according to the official BTE Design System.

The implementation must comply with

- PACK_01_DESIGN_PRINCIPLES
- PACK_02_LAYOUT_SYSTEM
- PACK_03_COMPONENT_STANDARD
- PACK_04_UI_PRESENTATION_STANDARD
- PACK_05_ACCESSIBILITY
- PACK_06_RESULT_PAGE_LAYOUT_STANDARD
- PACK_07_RESULT_PAGE_BLUEPRINT
- RESULT_PAGE_LAYOUT_GALLERY

No implementation may bypass these specifications.

---

# Sprint Objective

Rebuild the entire Result Page using the official architecture.

Target outcome

Stable

Consistent

Professional

Scalable

Responsive

Maintainable

---

# Overall Workflow

Read Design System

↓

Read Blueprint

↓

Read Layout Gallery

↓

Execute Tasks

↓

Run Tests

↓

Validate

↓

Merge

---

# Phase 01

Architecture Extraction

Goal

Separate Screen Architecture from Presentation.

Tasks

□ Create ResultPage component

□ Create Zone components

□ Create Row components

□ Remove direct Card rendering

□ Remove layout logic from ResultPage

Deliverables

ResultPage

SummaryZone

AnalysisZone

VisualizationZone

RecommendationZone

InterpretationZone

KnowledgeZone

Acceptance

✓ Zone architecture completed

---

# Phase 02

Summary Zone

Reference

LP-001

Tasks

□ Executive Summary

□ Core Indicators

□ Destiny Direction

□ Equal Height

□ Responsive

Acceptance

✓ Summary follows official blueprint

---

# Phase 03

Analysis Zone

Reference

LP-003

Tasks

□ Five Elements

□ Strength

□ Ten Gods

□ Pattern

□ Luck

Acceptance

✓ Three-column analysis layout

✓ Equal height

---

# Phase 04

Visualization Zone

Reference

LP-004

Tasks

□ Radar

□ Timeline

□ Distribution

□ Charts

Acceptance

✓ Fixed height

✓ Text summaries

---

# Phase 05

Recommendation Zone

Reference

LP-005

Tasks

□ Recommendation Card

□ Priority

□ Action

□ Benefit

□ Expand

Acceptance

✓ Recommendations prioritised

---

# Phase 06

Interpretation Zone

Reference

LP-006

Tasks

□ Preview

□ Expand

□ Collapse

□ Reading layout

Acceptance

✓ Reading flow preserved

---

# Phase 07

Knowledge Zone

Reference

LP-007

Tasks

□ Terminology

□ References

□ Theory

□ Appendix

Acceptance

✓ Knowledge isolated from interpretation

---

# Phase 08

Presentation Layer

Tasks

□ ViewModels

□ Presentation Adapter

□ Preview Builder

□ Display Model

□ Formatting

Acceptance

✓ UI consumes ViewModels only

---

# Phase 09

Layout Validation

Tasks

□ Equal Heights

□ Row Alignment

□ White Space

□ Visual Rhythm

□ Grid Validation

Acceptance

✓ Matches Blueprint

---

# Phase 10

Responsive

Tasks

□ Desktop

□ Tablet

□ Mobile

Acceptance

✓ Reading order unchanged

---

# Phase 11

Accessibility

Tasks

□ Keyboard

□ Focus

□ Contrast

□ Screen Reader

Acceptance

✓ PACK_05 compliant

---

# Phase 12

Performance

Tasks

□ Remove unnecessary renders

□ Memoize where needed

□ Lazy rendering

□ Skeleton

Acceptance

✓ Stable rendering

---

# Phase 13

Code Quality

Tasks

□ Remove duplicated components

□ Remove duplicated CSS

□ Remove hardcoded spacing

□ Remove hardcoded colors

Acceptance

✓ Design Tokens only

---

# Phase 14

Visual Polish

Tasks

□ Alignment

□ Spacing

□ Typography

□ White Space

□ Balance

Acceptance

✓ Professional appearance

---

# Phase 15

Regression Testing

Tasks

□ Desktop screenshots

□ Tablet screenshots

□ Mobile screenshots

□ Dynamic content

□ Empty state

□ Loading

□ Error

Acceptance

✓ No regressions

---

# Phase 16

Final Compliance Review

Validate against

□ PACK_01

□ PACK_02

□ PACK_03

□ PACK_04

□ PACK_05

□ PACK_06

□ PACK_07

□ Layout Gallery

Acceptance

✓ All Packs PASS

---

# Cursor Rules

Cursor MUST

✓ Follow Blueprint

✓ Follow Layout Gallery

✓ Reuse Components

✓ Preserve Reading Flow

✓ Preserve Equal Heights

✓ Preserve White Space

✓ Preserve Responsive Behaviour

✓ Preserve Accessibility

---

# Cursor MUST NOT

✗ Invent Layout

✗ Invent Grid

✗ Invent Row

✗ Invent Card Position

✗ Stretch Cards

✗ Break Reading Order

✗ Render Engine Models

✗ Mix Business Logic into UI

✗ Duplicate Components

✗ Hardcode Values

---

# Deliverables

The Sprint is complete only when

✓ Result Page follows PACK_06.

✓ Result Page follows PACK_07.

✓ Layout Gallery patterns are applied.

✓ Dynamic content no longer breaks layout.

✓ Equal-height rows implemented.

✓ Reading flow preserved.

✓ Accessibility validated.

✓ Responsive validated.

✓ Visual balance achieved.

✓ Professional appearance achieved.

---

# Definition of Done

The Result Page shall be considered complete only when

✓ All tasks are PASS.

✓ All acceptance criteria are PASS.

✓ All Design System Packs are PASS.

✓ Screenshots approved.

✓ Build PASS.

✓ TypeScript PASS.

✓ Tests PASS.

✓ Visual Review PASS.

END OF DOCUMENT