# UI-18 Mobile Layout

Mobile is a decision layout, not a resized desktop. Chrome lives in `mobile/mobileExperience.css` behind `data-mobile-experience="true"`.

## Breakpoints

| Viewport | Width | Grid | Hierarchy |
|----------|-------|------|-----------|
| Desktop | ≥1200 | 12 columns | UI-14 analysis order |
| Tablet | 768–1199 | 12 columns, large cards full width | Action promoted (`order: 16`) |
| Mobile | <768 | Single column | Decision order 1–9 |

## Scroll rhythm

Mobile grid gap is `--space-7` (48px) so one section is followed by whitespace, then the next section. Cards are not stacked flush.

## Hero

Overview `min-height: 70dvh`. Insight uses Display type. Top Priority is sticky while the hero is in view.

## Progressive disclosure

| Block | Mobile default |
|-------|----------------|
| Executive insight + conclusion | Open |
| Action (priority, actions, warnings, watch) | Open |
| Interpretation zones | Collapsed; lead visible |
| Five Elements, Pattern, BaZi, Ten Gods, ShenSha | Collapsed to title + thumb toggle |

Collapse is CSS `@media (max-width: 767px)` on `[data-mobile-body]`. jsdom and desktop still see the full DOM.

## Thumb zone

Primary expand/collapse uses `.bte-mobile-toggle` (`min-height: var(--touch-target-min)` = 44px). A lightweight sticky bar jumps to Action and Interpretation. Desktop card toggles stay for extra detail and are hidden on mobile.

## Loading / empty

Skeleton cards keep `data-mobile-order` so layout does not jump. Empty copy follows UI-13 (short customer line, no technical frame).

## Report preview (screen only)

`@media screen` reorders PrintSection wrappers with `:has([data-report-section])`. Print CSS is unchanged. Interpretation `.bte-er__detail` is hidden on small screens.
