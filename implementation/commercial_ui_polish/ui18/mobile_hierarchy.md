# UI-18 Mobile Hierarchy

Visual priority only. Semantic DOM order stays the frozen UI-03 catalog:

`overview → bazi → five-elements → ten-gods → pattern → shensha → luck → interpretation → action-plan`

Desktop CSS order (UI-14) is unchanged: Overview 10 → Interpretation 20 → Action 21 → evidence 30–35.

## Decision hierarchy (mobile <768px)

| Visual step | Surface | Card | CSS `order` | Default disclosure |
|-------------|---------|------|-------------|--------------------|
| 1 Hero | Main insight | Overview | 1 | Expanded |
| 2 Top Priority | Sticky in hero | Overview | 1 | Visible |
| 3 Executive Summary | Conclusion | Overview | 1 | Expanded |
| 4 Action | Priority + actions | Action Plan | 2 | Expanded |
| 5 Interpretation | `consulting_flow` lead | Interpretation | 3 | Lead on; zones collapsed |
| 6 Current Luck | Present cycle | Luck | 4 | Visible |
| 7 Supporting Analysis | Ngũ Hành, Mệnh Cục | Five Elements, Pattern | 5–6 | Collapsed |
| 8 Evidence | Bát Tự, Thập Thần, Thần Sát | BaZi, Ten Gods, ShenSha | 7–9 | Collapsed |

Hero + Top Priority + Executive Summary share the Overview card. They occupy the first viewport together. Action is the next card.

## Tablet (768–1199)

Intermediate: Action moves to CSS `order: 16` (between Overview 10 and Interpretation 20). Evidence stays expanded. Desktop ≥1200 is untouched.

## Identity / metadata

On mobile, identity name stays. Foundation, status, pillars, Cân Xương detail, and Overview evidence badges hide. They remain in the DOM.
