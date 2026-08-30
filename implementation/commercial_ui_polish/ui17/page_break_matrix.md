# UI-17 Page Break Matrix

| Block | Rule |
|-------|------|
| Cover | Always page 1. `page-break-after: always`. Keep together. |
| Identity | Flows after cover. |
| Executive Summary | New page (`break-before`). Insight callout kept together. |
| Chart Snapshot | Keep together. Visualizations not split. |
| Key Findings | Keep together. Cards not split. |
| Interpretation | New page. `consulting_flow` and each zone `break-inside: avoid`. |
| Action Plan | New page. Top Priority callout and action items not split. |
| Luck | Keep together. Timeline not split. |
| Supporting Analysis | Flow. Each viz block `break-inside: avoid`. |
| Appendix | New section (`break-before`). Signature kept together. |

Widow / orphan: headings `break-after: avoid`; `orphans: 3`; `widows: 3`.
