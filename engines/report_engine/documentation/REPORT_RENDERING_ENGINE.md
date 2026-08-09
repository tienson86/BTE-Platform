# Report Rendering Engine

Version: 1.0.0  
Engine ID: `report_rendering_engine`  
Sprint: RE-3  
Status: Released  
Foundation: v1.0.0 (frozen)

This document is the canonical architecture for Rendering & Export.

RE-3 transforms `CanonicalReportLayout` into in-memory `CanonicalReportArtifact` values.

RE-3 does **not** perform Analysis, Decision, Luck, Interpretation, or Layout logic.

RE-3 does **not** write the filesystem, persist storage, or print.

RE-1 Report Foundation and RE-2 Layout Engine are unchanged.

---

## Render lifecycle

```
CanonicalReportLayout (RE-2)
        ↓
Rendering Context
        ↓
Render Model
        ↓
Asset Embedder (references only)
        ↓
Export Manager → selected renderer
        ↓
CanonicalReportArtifact
```

`ReportRenderingEngine.run()` never raises to API callers.

---

## Render model

Logical projection of layout:

- pages
- blocks
- assets (embed refs)
- styles (theme identifiers)
- metadata

No business rules. No CSS stylesheets.

---

## Artifact model

`CanonicalReportArtifact` is the only official RE-3 output:

- `artifact_id`
- `renderer`
- `mime_type`
- `content`
- `metadata`
- `assets`
- `render_trace`
- `render_audit`
- `render_diagnostics`
- `render_version`

Content is an in-memory deterministic string. PDF/DOCX envelopes are mime-typed memory objects, not filesystem writers.

---

## Renderer registry

| renderer_id | mime_type | enabled |
|---|---|---|
| pdf | application/pdf | yes |
| docx | WordprocessingML | yes |
| html | text/html | yes |
| markdown | text/markdown | yes |
| json | application/json | yes |
| xlsx | SpreadsheetML | no |
| pptx | PresentationML | no |

---

## Export manager

Selects an enabled renderer and returns `RenderArtifact`.

No persistence. No storage. No printing.

---

## Future RX-1 integration

RX-1 Canonical Report Pipeline may orchestrate:

RE-1 Context → RE-2 Layout → RE-3 Rendering

RX-1 must consume `CanonicalReportArtifact` only. RE-3 must not call pipelines.

---

## Compliance

- Deterministic, version-aware, plugin-ready
- Additive only
- Ready for RX-1 Canonical Report Pipeline
