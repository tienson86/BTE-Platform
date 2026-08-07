# 01_DATA_MODEL.md

Version: 1.0

Status: CANONICAL

Pack: 05

Engine: Report Engine

---

# 1. Purpose

This document defines the canonical data model of the Report Engine.

The Report Engine exposes one canonical output model.

ReportResult

ReportResult is the Aggregate Root of the presentation domain.

Every UI renderer and exporter consumes this Aggregate.

---

# 2. Design Principles

ReportResult follows these principles.

- Immutable
- Strongly Typed
- Canonical
- Versioned
- Theme Independent
- Platform Independent
- Serializable
- Traceable

Presentation never changes business meaning.

---

# 3. Canonical Input

Input

InterpretationResult

Produced by

Interpretation Engine

InterpretationResult is immutable.

The Report Engine never modifies InterpretationResult.

---

# 4. Canonical Output

Output

ReportResult

ReportResult is immutable.

It becomes the single presentation source for every downstream renderer.

---

# 5. Aggregate Root

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

---

# 6. ReportMetadata

Metadata describing report generation.

| Field | Type | Description |
|--------|------|-------------|
| report_id | UUID | Unique report identifier |
| interpretation_id | UUID | Source InterpretationResult |
| version | string | Schema version |
| engine_version | string | Report Engine version |
| theme | string | Active theme |
| locale | string | Active locale |
| generated_at | datetime | Generation timestamp |
| duration_ms | number | Runtime duration |

---

# 7. Layout Tree

LayoutTree is the canonical presentation structure.

Hierarchy

Document

↓

Page

↓

Section

↓

Block

↓

Card

↓

Element

↓

Content

LayoutTree replaces HTML or PDF structures.

---

# 8. Page Model

Every Page contains

Page ID

Title

Blocks

Page Number

Metadata

Navigation

Pages remain immutable.

---

# 9. Section Model

Each section contains

Section ID

Title

Blocks

Visibility

Order

Metadata

Sections correspond to InterpretationResult sections.

---

# 10. Block Model

Blocks are reusable presentation units.

Examples

Card

Table

Chart

Timeline

Grid

Paragraph

Image

Separator

Every block has one responsibility.

---

# 11. Element Model

Elements are atomic visual components.

Examples

Heading

Text

Label

Value

Icon

Badge

Divider

Chart Axis

Table Cell

Elements are platform independent.

---

# 12. Content Model

Content references

Paragraph

Sentence

Fragment

Image

Chart Data

Table Data

Content never owns analytical logic.

---

# 13. Navigation Collection

Navigation contains

Menu

Bookmarks

Section Links

Page Links

TOC

Navigation improves user experience.

---

# 14. Theme Configuration

Theme defines

Typography

Spacing

Color Palette

Border Radius

Elevation

Icons

Dark Mode

Print Mode

Themes never change report content.

---

# 15. Asset Collection

Stores reusable assets.

Examples

Icons

SVG

Charts

Illustrations

Logos

Fonts

Assets are shared across render targets.

---

# 16. Export Collection

Defines supported outputs.

Desktop

Mobile

Tablet

PDF

HTML

DOCX

Markdown

JSON

Export metadata is centralized.

---

# 17. Trace Collection

Stores

Layout Trace

Theme Trace

Render Trace

Export Trace

Runtime Trace

Every presentation element is traceable.

---

# 18. Localization Model

Supports

Language

Locale

Typography

Formatting

Direction

Localization affects presentation only.

---

# 19. Serialization

Supported formats

JSON

YAML

MessagePack

Serialization preserves every Aggregate member.

---

# 20. Versioning

Major

Breaking schema changes.

Minor

Backward-compatible additions.

Patch

Bug fixes.

Backward compatibility is preserved.

---

# 21. Downstream Contract

The following consumers read

ReportResult

Desktop Renderer

Mobile Renderer

Tablet Renderer

PDF Exporter

Print Exporter

REST API

No consumer rebuilds report layout.

---

# 22. Aggregate Diagram

InterpretationResult

↓

Report Engine

↓

+-------------------------------------------+
|              ReportResult                 |
|-------------------------------------------|
| ReportMetadata                            |
| LayoutTree                                |
| PageCollection                            |
| NavigationCollection                      |
| ThemeConfiguration                        |
| AssetCollection                           |
| ExportCollection                          |
| TraceCollection                           |
+-------------------------------------------+

↓

Desktop / Mobile / PDF / Print

---

# 23. Source of Truth

ReportResult is the only presentation representation within the BTE Platform.

Every renderer consumes ReportResult.

No renderer rebuilds layout.

The Report Engine is the canonical presentation source.

---

END OF DOCUMENT