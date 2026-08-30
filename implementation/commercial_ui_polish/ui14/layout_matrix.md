# UI-14 Layout Matrix

Visual System V2 applied to Commercial Dashboard. Frozen UI-03 `data-span` and DOM order are unchanged. Visual placement uses CSS `order` and `grid-column`.

## Page chrome

| Surface | Visual level | Card type | DOM position | Visual order |
|---------|--------------|-----------|--------------|--------------|
| Page title | 4 | — | First | 1 |
| Identity Header | 4 | Status | After title | 2 |
| Canonical grid | 1–3 | — | After identity | 3 |
| Cân Xương detail | 4 | Reference | Last | 4 |

## Grid cards

| Card | `data-span` | Visual level | Card type | CSS order | Desktop visual span |
|------|-------------|--------------|-----------|-----------|---------------------|
| Overview | 4 | 1 | Hero | 10 | Full width (`1 / -1`) |
| Interpretation | 12 | 2 | Analysis | 20 | 12 |
| Action Plan | 12 | 2 | Analysis | 21 | 12 |
| BaZi | 8 | 3 | Analysis | 30 | 8 |
| Five Elements | 4 | 3 | Analysis | 31 | 4 |
| Ten Gods | 4 | 3 | Analysis | 32 | 4 |
| Pattern | 4 | 3 | Analysis | 33 | 4 |
| ShenSha | 6 | 3 | Analysis | 34 | 6 |
| Luck | 6 | 3 | Analysis | 35 | 6 |

Semantic DOM order remains:

`overview → bazi → five-elements → ten-gods → pattern → shensha → luck → interpretation → action-plan`

## Breakpoints

| Viewport | Width | Grid | Hierarchy |
|----------|-------|------|-----------|
| Desktop | ≥1200 | 12 columns | Hero full width, then L2, then L3 pairs |
| Tablet | 768–1199 | 12 columns, large cards full width | Hero / Interpretation / Action / BaZi / Luck full width |
| Mobile | <768 | Single column | Same visual order, one card per row |

## Spacing (UI-13)

| Context | Token | Value |
|---------|-------|-------|
| Desktop page padding | `--space-6` | 32px |
| Tablet page padding | `--space-5` | 24px |
| Mobile page padding | `--space-4` | 16px |
| Between cards | `--space-5` | 24px |
| Inside analysis cards | `--space-4` | 16px |
| Hero padding | `--space-6` | 32px |
| L2 card padding | `--space-5` | 24px |
