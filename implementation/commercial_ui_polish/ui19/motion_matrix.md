# UI-19 Motion matrix

| Surface | Interaction | Motion | Duration | Purpose | Mobile | Reduced motion |
|---------|-------------|--------|----------|---------|--------|----------------|
| Hero / Overview | Initial reveal | Opacity + `translateY(var(--space-1))` | 320ms | Orient to insight | Yes, 3 elements max | Instant |
| Top Priority | Initial reveal | Same | 320ms | Decision first | Sticky; no extra loop | Instant |
| Interpretation lead | Initial reveal | Same | 320ms | consulting_flow visible | Lead stays; zones collapse | Instant |
| Action / buttons | Hover | Background / border | 120ms | Actionable feedback | No hover on coarse pointers | Instant |
| Action / buttons | Focus | Focus ring | 120ms | Keyboard path | Same | Instant ring |
| Interpretation / evidence | Expand | max-height + opacity | 200ms | State: closed → open | Primary disclosure | Instant open |
| Luck current | State | Opacity settle | 200ms | This cycle is now | Timeline still readable | Instant |
| Five Elements | Bar width | Width ease-out | 200ms | Quantity, once | Not looping | No width transition |
| Pattern / BaZi / Ten Gods / ShenSha | — | None decorative | — | Avoid noise | Evidence stays collapsed | n/a |
| Thumb bar | Enter | Reveal | 320ms | Navigation available | Safe-area inset | Instant |
| Thumb bar | Anchor | Smooth scroll | browser | Jump with orientation | Same hrefs | Auto scroll |
| Skeleton | Load | Opacity pulse | 320ms | Calm wait | Unchanged layout | Static bars |
| Report preview | Focus/hover | Ring / color | 120ms | Screen only | n/a | Instant |
| Print | — | None | — | Archive | n/a | n/a |
