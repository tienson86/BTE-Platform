# Implementation Location

The Python implementation for stage **10 Report Generator** lives in:

```text
engines/analysis_engine/report_generator/
```

This directory's sibling (`10_report_generator/`) remains the architecture
documentation baseline (V1.0.0 Frozen).

## Public import

```python
from engines.analysis_engine.report_generator import (
    ReportGenerator,
    ReportAssemblyContext,
    FormatProfile,
    ReportGeneratorResult,
    ThemeManager,
    TemplateLoader,
)
```

## Public API

```text
ReportGenerator.assemble(context: ReportAssemblyContext) -> ReportGeneratorResult
```

`ReportEngine` is an alias of `ReportGenerator`.

## Template System (Sprint 2)

### Themes

- Classic
- Modern
- Professional
- Dark

Also retained: `default`, `compact` (backward compatible).

Resolved via `ThemeManager` / `ThemeRegistry`.

### Templates

`TemplateLoader` registers layout shells:

- `default`
- `classic` / `modern` / `professional` / `dark`
- `print`

### Renderers

- Component Renderer
- Section Renderer
- Table Renderer
- Chart Renderer

### Formats

- HTML
- PDF
- Markdown
- JSON
- Print (print-optimized HTML)

## Components

- Report Builder — assembles `StructuredReport`
- Section Builder — binds InterpretationResult sections
- Theme Manager — presentation tokens + catalog
- Template Loader — layout shells
- Serializers — HTML, Markdown, PDF, JSON, Print

## Behavior

Assembly and serialization only. No interpretation. No domain recomputation.
