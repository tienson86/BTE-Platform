# UI-14 Visual Hierarchy

Dashboard is the customer's first consulting experience. Within three seconds the Overview hero answers "what matters."

## Four levels

### Level 1 — Hero

- Overview is the visual anchor.
- Largest type: `--font-family-display` + `--font-size-section` on insight.
- Most whitespace: 32px padding, 24px internal gap.
- Top Priority is a copy-only badge + title from `actionPlan.priority.title`.
- No nested analysis tables.

### Level 2 — Interpretation / Action

- Full-width analysis cards.
- Body type, 24px padding.
- Soft elevation. Secondary to the hero.

### Level 3 — Structure

- BaZi, Five Elements, Ten Gods, Pattern, Luck, ShenSha.
- Flat paper. Caption-weight titles.
- Charts keep existing geometry; only spacing changed.

### Level 4 — Metadata

- Identity Header, analysis id, dates, Cân Xương reference.
- Quiet type (`--text-secondary`), no competing shadow.

## Card system (UI-13)

| Type | Surfaces |
|------|----------|
| Hero | Overview |
| Analysis | Interpretation, Action, BaZi, Five Elements, Ten Gods, Pattern, Luck, ShenSha |
| Status | Identity Header |
| Reference | Cân Xương detail |

## Typography

| Role | Use |
|------|-----|
| Hero / Display | Overview insight |
| Section | Hero insight size token |
| Card Title | `--font-size-subsection` |
| Body | Interpretation / Action copy |
| Caption | Subtitles, supporting lines |
| Label | Badge and field labels |
| Metric | Identity weight, Pattern primary name |

## Color

Mapped `--cdash-*` aliases to Visual System V2:

- Accent `#059669` (`--accent-primary`)
- Paper `--surface-report-paper`
- Background `--surface-background`

No new palette. Five-element bar colors are unchanged (UI-15).

## Icons and badges

- Action markers are 16px outline discs, not emoji.
- Pattern flow uses a single stroke chevron.
- Badges share `--bte-radius-9999`, Label type, 4×8 padding.

## Empty / loading / a11y

- Empty copy uses Body + `--text-secondary`.
- Skeleton uses `--surface-section` pulse; disabled under `prefers-reduced-motion`.
- Focus: `--focus-ring`. Touch: `--touch-target-min` 44px.
