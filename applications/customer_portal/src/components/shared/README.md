# Shared Component Library (WP-0003)

Reusable presentation patterns composed from frozen Base Components.
No business meaning. No API calls. Token-driven.

## Inventory (Pack 06)

SectionHeader, SectionDivider, SectionContainer, SectionSurface,
MetricRow, MetricGroup, MetricCard, LabelValueRow,
StatusBadge, ConfidenceBadge, EvidenceRow, EvidenceList,
PropertyGrid, PropertyItem, KeyValueGrid, KeyValueRow,
HighlightBox, InformationBox, WarningBox, SuccessBox, InsightBox, Callout,
ReadingProgress, StickyReadingRail, ScrollSpy,
CollapsePanel, Accordion, TabPanel, Timeline, TimelineItem,
EmptyState, UnavailableState, LoadingState, ErrorState,
SearchBar, FilterBar, Toolbar, FooterNote,
GlossaryEntry, CitationRow, ReferenceBlock, TagGroup, ChipGroup,
SkeletonSection, SkeletonMetric, SkeletonParagraph.

## Usage

```ts
import { SectionHeader, MetricCard, Callout } from "@bte/commercial-ui-v3";
```

## Rules

- Compose Base Components only.
- Presentation data via props/callbacks.
- No business logic, engines, or screens.
- Public imports via barrel only.
