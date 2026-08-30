# UI-16 Before / After

## Before

The production customer path after analysis is the Commercial Dashboard (`/result`). Export remains `/reports` (existing PDF HTML). There was no editorial consulting-report layout.

A stacked dashboard print would have repeated card chrome, dashboard grid, and Level 3 analysis competing with the executive message.

## After

`/report-preview` is an internal HTML report surface:

- Editorial sections instead of a dashboard grid
- Serif for cover, insight, and consulting narrative
- Sans for data, labels, tables, metadata
- UI-15 visualization kinds reused without Dashboard DOM (`bte-cdash`)
- Frozen Narrative V2 Presentation copied unchanged
- Production `/reports` PDF path not switched

## CASE-0001

Render uses live/frozen production Narrative V2 Presentation after Birth Input → ResultStore. No hardcoded consulting copy in the report module.
