# UI Sprint 01 — Handover

**Goal:** Design System & Layout Foundation (no screen redesign)  
**Date:** 2026-08-02

## 1. New components

See [component_catalog.md](component_catalog.md). Full set: Card, Panel, MetricCard, InfoCard, AnalysisCard, SectionHeader, Divider, StatusBadge, ProgressBar, Gauge, Toolbar, Sidebar, PageHeader, Tabs, Accordion, Collapse, Alert, Tooltip, Skeleton, Loading, EmptyState, ErrorState, QuickAction, FloatingAction, AppLayout, Header, Content, InspectorPanel, Footer.

## 2. Layout architecture

See [layout_architecture.md](layout_architecture.md).

## 3. Design System

Package `@bte/design-system` at `frontend/design_system/`. Docs: [design_system.md](design_system.md).

## 4. Theme

`[data-theme=light|dark]` / `.dark` with paired token sets.

## 5. Typography

H1–H3, Subtitle, Body, Caption, Metric, Label (`.bte-*` classes + CSS vars).

## 6. Spacing

`--bte-space-1` … `--bte-space-12` + stack/row utilities.

## 7. Color tokens

Primary, Secondary, Success, Warning, Danger, Info, Neutral, surfaces (bg/panel/card/line/ink/muted), light/dark.

## 8. Animation

Fade-in, expand, skeleton pulse, hover transitions; reduced-motion safe.

## 9–10. Build / Typecheck

```bash
cd frontend/design_system
npm install
npm run typecheck
npm run build
```

## 11. Freeze

No Backend / API / Engine / Database changes in this sprint.

## Adoption status

- Consoles declare `"@bte/design-system": "file:../../frontend/design_system"`.
- Bridge modules: `src/designSystem.ts` (re-export only).
- Screens **not** redesigned (Dashboard / Analysis / Report / Knowledge unchanged).
- Portal keeps existing CSS; tokens aligned to the same Linear/Stripe palette for future sync.
