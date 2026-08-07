# 08_VALIDATION_RULES.md

Version: 1.0

Status: CANONICAL

Pack: 05

Engine: Report Engine

---

# 1. Purpose

This document defines the canonical validation rules of the Report Engine.

Validation ensures every ReportResult is

- Structurally complete
- Visually consistent
- Theme compliant
- Renderable
- Exportable
- Traceable
- Ready for publication

Report validation is the final quality gate of the BTE Platform.

---

# 2. Validation Philosophy

The Report Engine validates

presentation quality.

It never validates

- calendar calculations
- BaZi structures
- analytical conclusions
- narrative correctness

Those responsibilities belong to upstream Engines.

---

# 3. Validation Pipeline

PresentationContext

↓

Layout Validation

↓

Theme Validation

↓

Render Validation

↓

Asset Validation

↓

Navigation Validation

↓

Export Validation

↓

Trace Validation

↓

Aggregate Validation

↓

Result<ReportResult>

Every stage is mandatory.

---

# 4. Validation Categories

The Report Engine performs

Layout Validation

Theme Validation

Render Validation

Asset Validation

Navigation Validation

Export Validation

Localization Validation

Trace Validation

Aggregate Validation

Metadata Validation

---

# 5. Layout Validation

Validate

✓ Document structure

✓ Page hierarchy

✓ Section hierarchy

✓ Block hierarchy

✓ Card hierarchy

✓ Grid consistency

✓ Layout constraints

No orphan nodes are allowed.

---

# 6. Theme Validation

Validate

✓ Theme exists

✓ Theme version

✓ Design tokens

✓ Typography

✓ Color palette

✓ Responsive tokens

✓ Accessibility tokens

No invalid theme may be applied.

---

# 7. Render Validation

Validate

✓ RenderTree integrity

✓ Render nodes

✓ Containers

✓ Visual constraints

✓ Render metadata

✓ Responsive rendering

RenderTree must be complete.

---

# 8. Asset Validation

Validate

✓ Fonts

✓ Icons

✓ Images

✓ Charts

✓ SVG

✓ Embedded resources

No required asset may be missing.

---

# 9. Navigation Validation

Validate

✓ Table of contents

✓ Internal links

✓ Bookmarks

✓ Page references

✓ Section references

Navigation must remain consistent.

---

# 10. Export Validation

Validate

✓ PDF package

✓ DOCX package

✓ HTML package

✓ JSON package

✓ Print package

✓ Export metadata

Every enabled export target must be valid.

---

# 11. Localization Validation

Validate

✓ Language

✓ Locale

✓ Typography

✓ Number formatting

✓ Date formatting

✓ RTL/LTR compatibility

Localization never changes content.

---

# 12. Trace Validation

Validate

Layout Trace

Theme Trace

Render Trace

Export Trace

Runtime Trace

Every presentation element must remain traceable.

---

# 13. Aggregate Validation

Validate

ReportResult

Checks

✓ Metadata

✓ LayoutTree

✓ Pages

✓ Navigation

✓ Assets

✓ Theme

✓ Export Collection

✓ Trace Collection

No missing Aggregate members.

---

# 14. Metadata Validation

Validate

Engine Version

Theme Version

Layout Version

Render Version

Export Version

Execution Duration

Metadata is mandatory.

---

# 15. Consistency Validation

Verify

Page numbering

Section ordering

Grid consistency

Card hierarchy

Theme consistency

Navigation consistency

Presentation must be deterministic.

---

# 16. Accessibility Validation

Validate

✓ Heading hierarchy

✓ Reading order

✓ Contrast ratio

✓ Alternative text

✓ Keyboard navigation metadata

✓ Semantic structure

Accessibility is mandatory.

---

# 17. Error Handling

Possible errors

LayoutValidationError

ThemeValidationError

RenderValidationError

AssetValidationError

NavigationValidationError

ExportValidationError

AggregateValidationError

InternalError

Every error contains

- code

- stage

- component

- message

- trace_id

- timestamp

---

# 18. Warning Rules

Warnings allow execution.

Examples

Fallback font

Fallback icon

Deprecated theme

Optional image missing

Unsupported bookmark

Warnings never change report meaning.

---

# 19. Validation Result

Validation returns

Result<ReportResult>

Possible states

SUCCESS

WARNING

ERROR

Only SUCCESS and WARNING produce ReportResult.

---

# 20. Logging

Validation records

Stage

Duration

Warnings

Errors

Trace ID

Export Target

Theme

No personal data may appear in logs.

---

# 21. Acceptance Checklist

Report validation is complete when

✓ Layout Validation passed

✓ Theme Validation passed

✓ Render Validation passed

✓ Asset Validation passed

✓ Navigation Validation passed

✓ Export Validation passed

✓ Localization Validation passed

✓ Trace Validation passed

✓ Aggregate Validation passed

✓ Metadata Validation passed

✓ Structured Result returned

---

END OF DOCUMENT