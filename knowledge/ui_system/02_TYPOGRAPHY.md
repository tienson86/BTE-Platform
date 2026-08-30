# 02_TYPOGRAPHY.md

Version: 2.0  
Status: DESIGN FOUNDATION  
Sprint: UI-13

Depends On

- VISUAL_LANGUAGE_SYSTEM.md §9
- PACK_01_DESIGN_PRINCIPLES.md §8
- PACK_03_COMPONENT_STANDARD.md §18

Do not invent a type scale. Roles below map Visual Language levels to Commercial UI V2 names.

---

# 1. Philosophy

Typography is the primary hierarchy tool.

Weight before color.

Spacing before borders.

Hierarchy before emphasis.

Never enlarge type merely to attract attention.

---

# 2. Families

| Role | Token | Stack |
|------|-------|-------|
| Display / Hero | `--font-family-display` | Source Serif 4, Iowan Old Style, Palatino, Georgia, serif |
| Body | `--font-family-body` | Source Sans 3, Segoe UI, system-ui, sans-serif |
| Metric / code | `--font-family-mono` | Cascadia Code, SF Mono, Consolas, ui-monospace |

Hero numbers and page identity may use display serif. Analysis body uses sans-serif.

---

# 3. Official roles

| V2 role | Visual Language | Size | Weight | Line height | Use |
|---------|-----------------|------|--------|-------------|-----|
| Hero | Display | 40px | Bold | 110% | Executive numbers, page identity |
| Section | H2 | 24px | SemiBold | 120% | Section headings |
| Card Title | H3 | 20px | SemiBold | 120% | Card headers |
| Body | Body | 16px | Regular | 150–170% | Main reading |
| Caption | Caption | 14px | Regular | 140–150% | Supporting text |
| Label | Meta / Label | 12px | Medium | 140% | Field labels, meta |
| Metric | Display / Number | 40px or Card Title | Bold / SemiBold | 110–120% | Comparable figures |

Page title (H1, 32px Bold) remains the screen title. It is not a card role.

Group title (H4, 18px Medium) may appear inside a card body. It is not a competing Card Title.

---

# 4. Token aliases

| V2 role | CSS token |
|---------|-----------|
| Hero | `--font-size-display` / `--font-display` |
| Section | `--font-size-section` / `--font-section` |
| Card Title | `--font-size-subsection` (nearest official step to 20px / 1.125rem) |
| Body | `--font-size-body` / `--font-body` |
| Caption | `--font-size-caption` / `--font-caption` |
| Label | `--font-size-metadata` / `--font-metadata` |
| Metric | `--font-size-display` for hero metrics; Card Title size for in-card metrics |

Weights: `--font-weight-regular` 400, `--font-weight-medium` 500, `--font-weight-semibold` 600, `--font-weight-bold` 700.

---

# 5. Reading rules

- Line length 45–75 characters for interpretation.
- Numbers use tabular alignment where compared.
- Do not mix more than one display size in a single card.
- Vietnamese customer copy uses Body, never Label, for narrative sentences.

---

END
