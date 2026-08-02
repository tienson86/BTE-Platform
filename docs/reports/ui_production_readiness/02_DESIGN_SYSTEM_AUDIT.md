# 02 — Design System Audit

| Field | Value |
|-------|--------|
| **Sprint** | UI Sprint 07 |
| **Date** | 2026-08-02 |

---

## Prefix map (normative)

| Prefix | Tier | Role |
|--------|------|------|
| `.rpt-` | Chrome / Hero / shared | Shell, rail, tier head, hero |
| `.fp-` | Tier 2 | Four Pillars workspace |
| `.mx-` | Tier 3 | Metrics & charts workspace |
| `.ax-` | Tier 4 | Analysis blocks |
| `.idoc-` | Tier 5 | Interpretation document |
| `.kw-` | Tier 6 | Knowledge & Evidence |

---

## Elevation grammar (verified)

| Level | Surfaces |
|-------|----------|
| E0 | Page canvas |
| E2 | Pillar cols, metric panels, analysis blocks, large cards |
| E3 | Executive hero, Day pillar accent |
| Flat reading | Interpretation sections (by design) |
| Trace blocks | Knowledge border-top (not admin tiles) |

**Admin dashboard feel:** mitigated — one vertical stream, scarce accents, no equal KPI tile wall.

---

## Issues found → disposition

| Issue | Disposition |
|-------|-------------|
| Divergent miss colors | Unified shared miss recipe |
| Stream uncapped width | `.rpt-main` max 1100px |
| Hard-coded rem sizes | Mapped to `--text-*` for lead/prose/metric |
| Missing `--radius-md` | Added to `tokens.css` |
| Dead `formatRelation` / `metric` / `row` | Removed |
| Duplicate card recipes | Kept intentional per density grammar; no merge that would rewrite Tier modules |
| Legacy `.rpt-pillar*` CSS | Retained (compat); not used by live pillars |

---

## Component duplication

No duplicate *runtime* components across tiers. Shared chrome via `tierWrap`, icons, i18n. Tier modules remain one-responsibility composites.

---

## Theme compliance

Colors use `var(--ink)`, `--muted`, `--line`, `--primary`, `--panel`, `--bg-accent` with `color-mix` accents. No purple/indigo default theme drift introduced.
