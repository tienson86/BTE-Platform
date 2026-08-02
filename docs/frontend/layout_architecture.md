# BTE Frontend — Layout Architecture

**Sprint:** UI Sprint 01  
**Status:** Foundation

## Goal

One App Layout contract for all BTE React surfaces (and CSS-equivalent for portal).

## Structure

```text
AppLayout
├── Sidebar      (nav rail)
├── Header       (brand / actions / theme)
├── Content      (primary scroll region)
├── InspectorPanel (optional detail rail)
└── Footer
```

CSS grid areas: `sidebar | header | content | inspector | footer`.

## Responsive

| Breakpoint | Behavior |
|------------|----------|
| Desktop ≥1280 | Full grid + optional inspector |
| Laptop ≤1100 | Sidebar/inspector off-canvas (`data-open`) |
| Tablet ≤900 | Compact content padding |

## Components

| Component | Responsibility |
|-----------|----------------|
| `AppLayout` | Grid shell; `showInspector` flag |
| `Sidebar` | Nav items / brand slot (memoized) |
| `Header` | Left/right slots |
| `Content` | Main landmark |
| `InspectorPanel` | Contextual detail |
| `Footer` | Meta / legal |

## UX rules

- Skip-link remains app responsibility (consoles already have one).
- Do not put business logic in layout primitives.
- Page content uses `PageHeader` + `SectionHeader` for hierarchy.

## Future

Wire consoles’ existing `AppShell` to compose these primitives without changing page IA in Sprint 01.
