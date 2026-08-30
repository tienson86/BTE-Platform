# UI-17 Before / After

## Before (UI-16)

HTML Executive Report Preview with basic `@page` A4 rules and some `break-inside: avoid`. No running header/footer, no print callout system, no archive signature, no Print Design System margin grid.

## After (UI-17)

Same report architecture and the same NarrativeV2Presentation copy.

Print adds:

- A4 grid with 20 / 18 / 22 / 18 mm margins
- Running header and footer
- Cover as dedicated page 1
- Major-section page starts (Executive, Interpretation, Action, Appendix)
- Print callouts only on Executive Summary and Top Priority
- Widow/orphan and block-integrity rules
- Archive signature on the last section
- Print typography in points
- Color used with labels so black-and-white remains readable

Production `/reports` PDF path is unchanged.
