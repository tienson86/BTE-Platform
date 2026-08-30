# UI-20 Accessibility audit

| Check | Result |
|-------|--------|
| `:focus-visible` + `--focus-ring` | Pass — UI-14 + UI-19 |
| Keyboard expand (`aria-expanded`) | Pass — interpretation, evidence, luck, action extras |
| Touch targets ≥ 44px | Pass — `--touch-target-min` on buttons and thumb bar |
| Contrast | Pass — emerald accent on paper; print uses ink tokens |
| `prefers-reduced-motion` | Pass — tokens 0ms + keyframes disabled |
| Semantic headings | Pass — card `h2`, zone `h3` |
| Labels | Pass — Vietnamese region labels; empty uses approved copy |
| Color-independent meaning | Pass — luck "Hiện tại" text; priority badge + title |
| Reduced motion keeps function | Pass |

No accessibility regression introduced to freeze the visual system.
