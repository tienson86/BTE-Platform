# Navigation Components (WP-0011)

Reading-oriented navigation for Commercial UI V3.
Compose Shared Components only. Consume NavigationViewModel only.

## Inventory (Pack 06)

- ReadingNavigation
- ReadingRail
- TableOfContents (public alias: `NavigationTableOfContents`)
- ScrollSpy (public alias: `NavigationScrollSpy`)
- ReadingProgress (public alias: `NavigationReadingProgress`)
- CurrentSection
- JumpNavigator
- AnchorNavigation
- BackToTop
- ReadingBreadcrumb
- PrintNavigator

## Rules

- No Base Component imports (Shared only).
- No frozen Business Screen / Business Component modifications.
- Progress, current section, and active states come from ViewModel only.
- No analysis, routing engines, or API calls.
- Public imports via barrel only.
