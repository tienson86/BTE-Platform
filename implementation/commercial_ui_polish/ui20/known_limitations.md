# UI-20 Known accepted limitations

- Identity header still uses pre-token px density from UI-03 geometry. Not redesigned in UI-20.
- Card radius `--cdash-radius: 14px` is between `--bte-radius-12` and `--bte-radius-16`. Left as frozen dashboard chrome.
- Pattern arrow uses 1.5px hairline. Not a new scale.
- Skeleton → live content is a remount; no cross-fade architecture.
- Evidence is not lazy-mounted; it is collapsed below the fold on mobile.
- Sticky Top Priority has no stuck-state shadow (would need observers).
- `/report-preview` is the HTML preview. Production PDF remains the existing export contract.
- CASE-0002 was reviewed from the existing editorial HTML export, not re-run through a new engine fixture.
- Portal app shell (logo, menu, theme) sits above the dashboard and is outside Commercial UI V2 freeze of the result surface.
