# UI-19 Motion audit

Every animation below has a customer purpose. Unlisted motion is not part of UI-19.

| Component | Trigger | Duration | Purpose | Reduced motion |
|-----------|---------|----------|---------|----------------|
| Overview Top Priority | Page load | `--motion-slow` 320ms | Orient: this is the decision | Instant (animation none) |
| Overview insight | Page load, delay `--motion-fast` | 320ms | Orient: main insight | Instant |
| Interpretation lead | Page load | 320ms | Orient: consulting_flow | Instant |
| Buttons / links / thumb bar | Hover (fine pointer) | `--motion-fast` 120ms | Confirm the control is actionable | Instant color/border |
| Buttons / links | `:focus-visible` | 120ms | Keyboard focus is visible | Instant ring |
| Interpretation extra / closing | Desktop expand mount | `--motion-normal` 200ms | Confirm more narrative opened | Instant |
| Ten Gods hidden / distribution | Desktop expand mount | 200ms | Confirm detail opened | Instant |
| Mobile evidence / interpretation body | `aria-expanded` / `data-mobile-open` | expand 200ms, fade 200ms | Height+opacity instead of a jump | Instant max-height |
| Luck current badge | Load | 200ms | Mark current vs other cycles | Instant |
| Five Elements bars | Width from 0 (existing UI-15) | 200ms | One-time quantity reveal | Transition none |
| Mobile thumb bar | First paint on small screens | 320ms | Bar arrived; does not cover by jump | Instant |
| Skeleton rows | Loading (existing UI-14) | 320ms pulse | Calm placeholder | Animation none |
| In-page anchors | Thumb bar / hash links | Browser smooth scroll | Orientation to Action / Interpretation | `scroll-behavior: auto` |
| Print / preview print | Print media | none | Static archive | n/a |

No unexplained animations.
