# Report Layout Engine

Version: 1.0.0  
Engine ID: `report_layout_engine`  
Sprint: RE-2  
Status: Released  
Foundation: v1.0.0 (frozen)

This document is the canonical architecture for Layout & Theme Composition.

RE-2 transforms `CanonicalInterpretationResult` into `CanonicalReportLayout`.

RE-2 does **not** render reports and does **not** export PDF, DOCX, HTML, Markdown, or any presentation format.

RE-1 Report Foundation is unchanged. Legacy Report Engine renderers are unchanged.

---

## Layout lifecycle

```
CanonicalReportContext (RE-1)
        +
CanonicalInterpretationResult (IX-1)
        ↓
Document Builder
        ↓
Section Builder
        ↓
Block Builder
        ↓
Theme Resolver
        ↓
Layout Resolver
        ↓
Asset Resolver
        ↓
TOC Builder
        ↓
CanonicalReportLayout
```

`ReportLayoutEngine.run()` never raises to API callers.

---

## Theme model

Identifiers only:

| Field | Default |
|---|---|
| `theme_id` | `bte.report.theme.v1` |
| `palette_id` | `bte.report.palette.foundation.v1` |
| `spacing_id` | `bte.report.spacing.foundation.v1` |
| `typography_id` | `bte.report.typography.foundation.v1` |
| `icon_set_id` | `bte.report.icons.foundation.v1` |

No CSS. No stylesheets.

---

## Layout model

Logical metadata only:

- page hierarchy
- block order
- column metadata
- page-break markers
- keep-together groups
- widows/orphans integers

No pagination rendering.

---

## Block model

Supported types:

`text` · `table` · `chart_placeholder` · `image_placeholder` · `divider` · `list` · `quote` · `reference` · `note` · `warning`

Blocks store type, source refs, and asset ids. No formatted bodies.

---

## Asset model

Kinds: `image` · `logo` · `chart` · `icon` · `attachment`

References only. No binary loading.

---

## TOC model

Hierarchy of layout sections. No page numbers. No hyperlinks.

---

## CanonicalReportLayout

The only official RE-2 output:

- `document`
- `sections`
- `blocks`
- `theme`
- `layout`
- `assets`
- `toc`
- `metadata`
- `layout_trace`
- `layout_audit`
- `layout_diagnostics`
- `layout_version`

---

## Future Renderer integration

RE-3 may consume `CanonicalReportLayout` only.

When enabled:

1. Bind theme identifiers to a renderer.
2. Materialize placeholders.
3. Export through a separate export engine.

RE-2 must not call a renderer.

---

## Compliance

- Deterministic, version-aware, plugin-ready
- Additive only
- Ready for RE-3 Rendering & Export Engine
