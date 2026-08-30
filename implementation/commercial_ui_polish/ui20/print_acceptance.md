# UI-20 Print acceptance

| Rule | Result |
|------|--------|
| A4 portrait | Pass — `@page size: A4 portrait` |
| Margins | Pass — 20/18/22/18 mm |
| Running header / footer | Pass — PrintHeader hidden on screen chrome; print CSS shows running elements |
| Page breaks | Pass — UI-17 PrintSection break/keep |
| Widow/orphan | Pass — existing print CSS |
| Action / findings | Pass — static blocks |
| Visualizations | Pass — print colors mapped to ink; no animation |
| Appendix + signature | Pass |
| Animation dependency | None — print `animation/transition: none` |
| Black-and-white readability | Pass — ink + muted line, not hue-only meaning |

Production PDF export path is unchanged (`data-pdf-export="false"` on preview).
