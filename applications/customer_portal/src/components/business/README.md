# Business Components — Executive Summary (WP-0004)

Presentation components for the Executive Summary screen.
Compose Shared Components only. Consume presentation ViewModels only.

## Inventory (Pack 06)

- ExecutiveHero
- RecommendationPanel
- ExecutiveOverview
- ExecutiveHighlights
- SummaryGlance
- HeroBackground
- HeroActions

## Rules

- No Base Component imports (Shared only).
- No analysis, scoring, API, or Knowledge Engine access.
- Support Loading / Ready / Empty / Unavailable / Error via presentation status.
- Public imports via barrel only.

## Usage

```ts
import {
  ExecutiveHero,
  RecommendationPanel,
  ExecutiveOverview,
  SummaryGlance,
  ExecutiveHighlights,
} from "@bte/commercial-ui-v3";
```
