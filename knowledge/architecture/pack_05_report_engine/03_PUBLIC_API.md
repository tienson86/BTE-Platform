# 03_PUBLIC_API.md

Version: 1.0

Status: CANONICAL

Pack: 05

Engine: Report Engine

---

# 1. Purpose

This document defines the canonical Public API of the Report Engine.

The Report Engine exposes one official service responsible for transforming a canonical InterpretationResult into a canonical ReportResult.

All layout, rendering and export logic remain internal.

---

# 2. API Philosophy

The Report Engine exposes one public service.

Consumers never execute

- Report Layout Engine
- Theme Engine
- Render Engine
- Export Engine
- Report Builder
- Validation Engine

directly.

Presentation logic is fully encapsulated inside the Report Engine.

---

# 3. Public Service

Canonical Service

ReportEngine

Responsibilities

- Validate input
- Execute presentation pipeline
- Produce ReportResult
- Return structured execution result

---

# 4. Public Entry Point

ReportEngine.run()

Input

InterpretationResult

↓

Output

Result<ReportResult>

This is the only supported public API.

---

# 5. Input Contract

Input Model

InterpretationResult

Produced only by

Interpretation Engine

Requirements

✓ Canonical

✓ Immutable

✓ Fully validated

The Report Engine never accepts

- HTML

- PDF

- React Components

- UI Models

- JSON Layout

Only canonical InterpretationResult.

---

# 6. Output Contract

Output

Result<ReportResult>

Possible states

Success

↓

ReportResult

Warning

↓

ReportResult + Warnings

Failure

↓

Structured Error

Partial reports are never returned.

---

# 7. Result Model

Result<T>

contains

success

value

warnings

error

metadata

trace

Result<T> is immutable.

Null is never returned.

---

# 8. Public Aggregate

ReportResult

contains

ReportMetadata

LayoutTree

PageCollection

NavigationCollection

ThemeConfiguration

AssetCollection

ExportCollection

TraceCollection

ReportResult is immutable.

---

# 9. Internal Components

The following components are private.

PresentationContextBuilder

ReportLayoutEngine

ThemeEngine

RenderEngine

ExportEngine

ReportBuilder

ValidationEngine

These components are implementation details.

They are never exposed outside the Report Engine.

---

# 10. Dependency Rules

Allowed

InterpretationResult

Layout Templates

Theme Resources

Typography Resources

Localization Resources

Asset Resources

Forbidden

Calendar Engine

BaZi Engine

Score Engine

Interpretation Engine internals

Rule Database

Desktop UI

Mobile UI

PDF Renderer

The Report Engine consumes only InterpretationResult and presentation resources.

---

# 11. Runtime Ownership

The Report Engine owns

- Layout Construction

- Theme Application

- Render Tree Construction

- Export Preparation

- Navigation Construction

- ReportResult generation

No downstream renderer rebuilds layout.

---

# 12. Error Model

Possible errors

ValidationError

LayoutError

ThemeError

RenderError

ExportError

AssetError

NavigationError

InternalError

Every error contains

- code

- stage

- component

- message

- timestamp

- engine_version

- trace_id

---

# 13. Warning Model

Warnings do not terminate execution.

Examples

Fallback Theme

Missing Optional Asset

Fallback Font

Deprecated Icon

Unsupported Export Target

Warnings are attached to Result<ReportResult>.

---

# 14. Traceability

Every execution produces

Presentation Trace

including

- Layout Trace

- Theme Trace

- Render Trace

- Export Trace

- Runtime Trace

Presentation Trace supports debugging and auditing.

---

# 15. Thread Safety

The Report Engine is

✓ Stateless

✓ Deterministic

✓ Thread-safe

✓ Immutable

Parallel execution is fully supported.

---

# 16. Performance

Target

Single Report

<100 ms

100 Reports

<2 seconds

1000 Reports

<15 seconds

No external network dependency.

---

# 17. Semantic Versioning

The Public API follows Semantic Versioning.

Major

Breaking API changes

Minor

Backward-compatible additions

Patch

Bug fixes

Breaking changes require Architecture Review.

---

# 18. Integration Example

InterpretationResult

↓

ReportEngine.run()

↓

Result<ReportResult>

↓

Desktop Renderer

↓

PDF Exporter

↓

REST API

The Report Engine never invokes downstream renderers.

---

# 19. Extension Rules

Future internal components may be added.

Examples

Interactive Renderer

Animation Engine

White-label Branding

Watermark Engine

Accessibility Adapter

Print Optimizer

Extensions remain internal.

The Public API remains unchanged.

---

# 20. API Stability

The Public API is considered stable when

Input remains

InterpretationResult

Output remains

Result<ReportResult>

Internal implementation may evolve without affecting consumers.

---

# 21. Acceptance Criteria

The Public API is complete when

✓ One public service

✓ One public entry point

✓ One canonical input

✓ One canonical output

✓ ReportResult Aggregate returned

✓ Internal components hidden

✓ Strong typing enforced

✓ Thread-safe

✓ Fully documented

---

END OF DOCUMENT