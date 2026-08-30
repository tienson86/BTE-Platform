# UI-15 Visualization Matrix

Approved visualizations from `knowledge/ui_system/13_INFORMATION_VISUALIZATION.md`. One card, one visual message. Input remains Narrative V2 Presentation / canonical chart copy. No new calculations.

| Card | Kind | `data-viz` | Spec | Not used |
|------|------|------------|------|----------|
| Five Elements | Horizontal Balance Bars | `balance-bars` | Mộc → Hỏa → Thổ → Kim → Thủy, labels + counts + hành color | Pie, Radar |
| Luck | Timeline | `timeline` | LTR, current highlighted, khởi vận / 10 đại vận / hiện tại / tiếp theo | Table-only |
| Pattern | Formation Flow | `formation-flow` | Step → step flow of published formation | Narrative rewrite |
| BaZi | Structure | `structure` | Thiên Can ↓ Địa Chi ↓ Tàng Can ↓ Thập Thần ↓ Trường Sinh | Summary table only |
| Ten Gods | Relationship | `relationship` | Lộ Can ↓ Tàng Can ↓ Quan hệ | Ranking, scores |
| ShenSha | Grouped chips | `grouped-chips` | Tag / chip / grouped list | Points, charts |

Overview, Interpretation, and Action stay UI-14 hierarchy. They are not chart surfaces.

## Color

Hành fills consume UI-13 tokens (classification, paired with labels):

| Hành | Token |
|------|-------|
| Mộc | `--feedback-success` |
| Hỏa | `--feedback-danger` |
| Thổ | `--feedback-warning` |
| Kim | `--bte-color-secondary-500` |
| Thủy | `--feedback-info` |

Color is never the only signal. Status tokens are not used as tốt/xấu.

## Responsive

| Viewport | Behavior |
|----------|----------|
| Desktop | Full visualization |
| Tablet | Ten Gods relationship stacks; Luck timeline remains LTR |
| Mobile | Pattern flow vertical; Luck timeline vertical; ShenSha chips full width; BaZi internal scroll |

No page-level horizontal scroll. Chart overflow stays inside the card.
