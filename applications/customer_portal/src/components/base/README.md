# Base Component Library (WP-0002)

Presentation-only primitives for Commercial UI V3.
No business meaning. Token-driven. Accessible.

## Inventory (Pack 06)

| Component | Responsibility |
|-----------|----------------|
| `BaseButton` | Actions |
| `BaseIcon` | Icon wrapper |
| `BaseText` | Body / caption text |
| `BaseHeading` | Semantic headings |
| `BaseSurface` | Surface hierarchy |
| `BaseDivider` | Hairline separator |
| `BaseBadge` | Status / meta badge |
| `BaseChip` | Compact chip |
| `BaseTag` | Category tag |
| `BaseAvatar` | Avatar / initials |
| `BaseSpinner` | Indeterminate loading |
| `BaseSkeleton` | Content placeholder |
| `BaseProgress` | Determinate progress |
| `BaseTooltip` | Hover / focus hint |
| `BaseLink` | Text link |
| `BaseInput` | Text field |
| `BaseTextarea` | Multiline field |
| `BaseSelect` | Select control |
| `BaseCheckbox` | Checkbox + label |
| `BaseRadio` | Radio + label |
| `BaseSwitch` | Switch + label |
| `BaseAlert` | Inline alert |
| `BaseCallout` | Annotation callout |
| `BaseEmptyState` | Empty content |
| `BaseErrorState` | Error content |
| `BaseUnavailableState` | Unavailable content |
| `BaseLoadingState` | Loading content |
| `BaseScrollArea` | Scroll region |
| `BaseContainer` | Max-width container |
| `BaseStack` | Vertical stack |
| `BaseGrid` | Responsive grid |

## Usage

```ts
import { BaseButton, BaseText, BaseStack } from "@bte/commercial-ui-v3";
```

Import styles once:

```ts
import "@bte/commercial-ui-v3/styles.css";
```

## Rules

- Consume Design Tokens only (`cui-base-*` classes).
- No business props, payloads, or engine calls.
- Prefer composition over configuration objects.
- Public imports via barrel only.

## Stories

Storybook is not a project standard for this package.
Use unit / interaction tests and this inventory as the component catalog.
