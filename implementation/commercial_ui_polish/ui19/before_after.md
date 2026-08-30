# UI-19 Before / After — CASE-0001

Source: Narrative V2 Presentation only. No Narrative, Runtime, Presentation, Export, or adapter edits.

Before: UI-18 layout with almost no interaction motion (skeleton pulse + Five Elements bar width).

After: The same CASE-0001 words and hierarchy, with restrained state feedback.

## What changed

| Area | Before | After |
|------|--------|-------|
| Page load | All cards appear at once | Priority, insight, lead reveal (max 3) |
| Hover | Instant color in places | 120ms background / border on controls |
| Focus | Ring, no duration | Fast ring (`--motion-fast`) |
| Mobile disclosure | `display: none` jump | max-height + opacity 200ms |
| Thumb bar | Static fixed bar | Enter 320ms + safe-area |
| Luck current | Static highlight | One-shot opacity settle |
| Reduced motion | Token durations → 0ms | Also kill keyframes, smooth scroll |
| Print | Static | Still static (`animation/transition: none`) |
| Hierarchy | UI-14 / UI-18 | Unchanged |
| Copy | Presentation | Unchanged |

## Screenshot index

| File | Viewport | Subject |
|------|----------|---------|
| `01_hero_initial.png` | 1440 | Hero after reveal |
| `02_action_hover_focus.png` | 1440 | Action control hover/focus |
| `03_interpretation_collapsed.png` | 390 | Lead on, zones collapsed |
| `04_interpretation_expanded.png` | 390 | Zones open |
| `05_luck_current.png` | 1440 | Current cycle emphasis |
| `06_mobile_hero.png` | 390 | Mobile hero |
| `07_mobile_thumb_navigation.png` | 390 | Thumb bar |
| `08_mobile_evidence_collapsed.png` | 390 | Five Elements collapsed |
