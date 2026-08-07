# PACK_05_REPORT_ENGINE_ARCHITECTURE.md

Version: 1.0

Status: CANONICAL

Pack: 05

Engine: Report Engine

---

# 1. Purpose

The Report Engine transforms a canonical InterpretationResult into a presentation-ready ReportResult.

Its responsibility is presentation, rendering and export.

The Report Engine never performs analysis.

The Report Engine never generates interpretation.

The Report Engine is the final presentation layer of the BTE Platform.

---

# 2. Position in Architecture

BirthRequest

↓

Calendar Engine

↓

BirthContext

↓

BaZi Engine

↓

BaziChart

↓

Score Engine

↓

AnalysisResult

↓

Interpretation Engine

↓

InterpretationResult

↓

Report Engine

↓

ReportResult

↓

Desktop

Mobile

Tablet

PDF

Print

API

The Report Engine consumes InterpretationResult only.

---

# 3. Responsibilities

The Report Engine is responsible for

✓ Report Layout

✓ Page Construction

✓ Theme Application

✓ Rendering

✓ Asset Management

✓ Navigation

✓ Export

✓ ReportResult generation

The Report Engine is NOT responsible for

✗ Calendar calculation

✗ BaZi construction

✗ Rule execution

✗ Score calculation

✗ Interpretation generation

---

# 4. Report Philosophy

Reports present information.

They never modify information.

Every report is a visual representation of InterpretationResult.

Presentation never changes meaning.

---

# 5. Runtime Pipeline

InterpretationResult

↓

Report Layout Engine

↓

Theme Engine

↓

Render Engine

↓

Export Engine

↓

Report Builder

↓

Validation

↓

ReportResult

Every stage has one responsibility.

---

# 6. Canonical Aggregate

The Report Engine produces one Aggregate Root.

ReportResult

The Aggregate contains

ReportMetadata

LayoutTree

ThemeConfiguration

PageCollection

NavigationCollection

AssetCollection

ExportCollection

TraceCollection

---

# 7. Engine Components

The Report Engine consists of

Report Layout Engine

Theme Engine

Render Engine

Export Engine

Report Builder

Validation Engine

Each component has a single responsibility.

---

# 8. Runtime Characteristics

The Engine must be

- Deterministic

- Stateless

- Immutable

- Thread-safe

- Render-independent

Given the same InterpretationResult,

the same ReportResult must always be produced.

---

# 9. Public Contract

Input

InterpretationResult

Output

Result<ReportResult>

ReportResult is immutable.

---

# 10. Knowledge Dependency

The Report Engine depends on

Layout Templates

Theme Resources

Typography Resources

Icon Resources

Localization Resources

It never loads

Rule Database

Sentence Library

Template Library

Placeholder Library

---

# 11. Rendering Model

Rendering follows

InterpretationResult

↓

Layout Tree

↓

Theme

↓

Render Model

↓

Export Model

↓

ReportResult

Rendering never changes narrative.

---

# 12. Explainability

Every visual block keeps references to

Interpretation Section

Paragraph

Sentence

Trace

This supports visual traceability.

---

# 13. Multi-Platform Support

The Report Engine supports

Desktop

Tablet

Mobile

PDF

Print

JSON

Future render targets

Platform adaptation affects layout only.

---

# 14. Error Handling

Every execution returns

Result<ReportResult>

Possible outcomes

Success

↓

ReportResult

Failure

↓

Structured Error

Partial reports are never returned.

---

# 15. Performance Targets

Single Report

<100 ms

100 Reports

<2 seconds

1000 Reports

<15 seconds

Rendering must not require network access.

---

# 16. Documentation Structure

The Report Engine documentation consists of

PACK_05_REPORT_ENGINE_ARCHITECTURE.md

01_DATA_MODEL.md

02_RUNTIME_PIPELINE.md

03_PUBLIC_API.md

04_REPORT_LAYOUT_ENGINE.md

05_RENDER_ENGINE.md

06_EXPORT_ENGINE.md

07_THEME_ENGINE.md

08_VALIDATION_RULES.md

09_TEST_STRATEGY.md

10_ACCEPTANCE_CHECKLIST.md

---

# 17. Long-Term Vision

The Report Engine is the canonical presentation layer of the BTE Platform.

Future capabilities such as

- Interactive Reports
- AI Report Assistant
- Voice Reports
- Video Reports
- White-label Themes
- Customer Branding

must integrate without changing the public contract.

---

# 18. Source of Truth

ReportResult is the only presentation representation within the BTE Platform.

Every UI, PDF exporter and external consumer reads ReportResult.

No downstream component rebuilds report layout.

The Report Engine is the single source of truth for presentation output.

---

# 19. Design Principles

The Report Engine follows

Single Responsibility

↓

Presentation Only

↓

Immutable Output

↓

Reusable Components

↓

Theme Separation

↓

Platform Independence

Presentation logic is isolated from business logic.

---

# 20. Acceptance Criteria

The Report Engine architecture is complete when

✓ Runtime pipeline defined

✓ Aggregate Root defined

✓ Component boundaries defined

✓ Public API defined

✓ Rendering model defined

✓ Export model defined

✓ Multi-platform strategy defined

✓ Documentation approved

---

END OF DOCUMENT