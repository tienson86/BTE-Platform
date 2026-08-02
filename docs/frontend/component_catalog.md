# BTE Frontend — Component Catalog

**Package:** `@bte/design-system`  
**Sprint:** UI Sprint 01

## Surfaces

| Component | Description |
|-----------|-------------|
| `Card` | Generic elevated surface |
| `Panel` | Larger page section panel |
| `MetricCard` | Label + metric value + optional hint |
| `InfoCard` | Title + body information block |
| `AnalysisCard` | Large analysis section (head/body) |
| `SectionHeader` | Title / subtitle / actions row |
| `Divider` | Horizontal rule |

## Status & meters

| Component | Description |
|-----------|-------------|
| `StatusBadge` | Tone: neutral/primary/success/warning/danger/info |
| `ProgressBar` | Linear progress (token color) |
| `Gauge` | Semi-circle SVG gauge 0–100 |

## Chrome

| Component | Description |
|-----------|-------------|
| `Toolbar` | Action cluster |
| `PageHeader` | H1 + subtitle + actions |
| `Tabs` | Controlled tablist |
| `Accordion` | Single expandable block |
| `Collapse` | Controlled/uncontrolled collapse |
| `Alert` | Inline status message |
| `Tooltip` | Hover/focus tip |
| `Skeleton` | Loading placeholder |
| `Loading` | Skeleton + label |
| `EmptyState` | Honest empty |
| `ErrorState` | Error panel |
| `QuickAction` | Compact CTA link |
| `FloatingAction` | FAB |

## Layout

| Component | Description |
|-----------|-------------|
| `AppLayout` | App shell grid |
| `Header` | Top bar slots |
| `Sidebar` | Nav rail (memo) |
| `Content` | Main |
| `InspectorPanel` | Side inspector |
| `Footer` | Footer |

## Performance notes

- `Sidebar` is wrapped in `React.memo`.
- Consumers should `React.lazy` route-level pages; import design-system at shell level once.
- Library build externalizes `react` / `react-dom` for split bundles.

## CSS entry

`@bte/design-system/styles.css` or granular `@bte/design-system/tokens.css`.
