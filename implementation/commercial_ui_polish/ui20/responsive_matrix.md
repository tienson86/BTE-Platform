# UI-20 Responsive matrix

| Viewport | Width | Intent | Notes |
|----------|-------|--------|-------|
| Mobile S | 390 | Decision layout | UI-18 order 1–9, evidence collapsed, thumb bar, overflow-x clip |
| Mobile M | 430 | Same as 390 | Single column |
| Tablet | 768 / 834 / 1024 | Intermediate | Action promoted (`order: 16`). Identity 2×2. Evidence still open |
| Desktop | 1280 / 1440 | Analysis layout | UI-14 order 10 / 20 / 21. Max width 1440 |
| Ultra-wide | 1920 | Same composition | Dashboard stays centered at 1440. Not stretched |

Safe area: thumb bar `bottom` includes `env(safe-area-inset-bottom)`.
