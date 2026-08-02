# UI Commercial Polish V1 — Handover Report

**Surface:** Customer Portal only (`applications/customer_portal/`)  
**Scope:** Presentation-only (Jinja + vanilla JS + CSS). No Backend / API / Engine / Database changes.  
**Date:** 2026-08-02

---

## 1. Summary

Commercial design-system polish for the Customer Portal: Linear/Stripe-like tokens, app shell, extensible result module registry, cardized result presenters, Knowledge Expert 3-pane Discussion UX (consumes existing `POST /api/v1/discussion`), and aligned secondary pages. React consoles deferred.

## 2. Files changed

### Modified
- `applications/customer_portal/static/css/portal.css` — `@import` hub
- `applications/customer_portal/static/i18n/vi.json` — analyze sections + discussion expert strings
- `applications/customer_portal/static/js/analyze.js` — field validation + loading skeleton
- `applications/customer_portal/static/js/dashboard.js` — metric/empty helpers
- `applications/customer_portal/static/js/history.js` — empty state + card list items
- `applications/customer_portal/static/js/profile.js` — empty state
- `applications/customer_portal/static/js/result.js` — registry-driven tabs + expert bind
- `applications/customer_portal/static/js/presenters/bazi.js` — collapsible section cards
- `applications/customer_portal/static/js/presenters/score.js` — collapsible section cards
- `applications/customer_portal/static/js/presenters/interpretation.js` — section cards + empty
- `applications/customer_portal/static/js/presenters/discussion.js` — 3-pane Knowledge Expert
- `applications/customer_portal/templates/_layout.html` — enterprise header, skip-link, UI scripts
- `applications/customer_portal/templates/analyze.html` — grouped form sections
- `applications/customer_portal/templates/result.html` — empty `#stageTabs`
- `applications/customer_portal/templates/history.html` / `login.html` / `profile.html`

### New
- `applications/customer_portal/static/css/tokens.css`
- `applications/customer_portal/static/css/base.css`
- `applications/customer_portal/static/css/components.css`
- `applications/customer_portal/static/css/layout.css`
- `applications/customer_portal/static/css/pages.css`
- `applications/customer_portal/static/css/domain.css`
- `applications/customer_portal/static/js/ui/components.js`
- `applications/customer_portal/static/js/ui/module_registry.js`
- `applications/customer_portal/static/js/ui/shell.js`
- `applications/customer_portal/tests/js/ui_commercial_preview_build.js`
- `docs/reports/ui_commercial_preview/` (generated HTML)
- `docs/reports/ui_commercial_polish_v1_report.md` (this file)

### Removed
- None (legacy styles migrated into `domain.css`; `portal.css` retained as import hub).

## 3. New / removed components

| Component | Role |
|-----------|------|
| `BteUI.metricCard` / `sectionCard` / `emptyState` / `errorPanel` / `statusBadge` / `bindCollapsible` | Shared presentational builders |
| `BteModules` registry | Extensible result stages (+ disabled luck/shensha stubs) |
| `BteShell` | Theme toggle + toast host |
| `bindDiscussionExpert` | Wires 3-pane chat to existing discussion API |

No React components. No npm toolchain added.

## 4. Design system summary

- **Tokens:** Primary blue, slate neutrals, success/warn/danger/info, type scale, spacing, radius, shadow, z-index; light/dark via `[data-theme]`.
- **Layers:** `tokens` → `base` → `components` → `layout` → `pages` → `domain`.
- **Shell:** Brand header, nav, theme toggle, skip-link, flash/toast, content max-width.
- **Responsive:** Desktop / laptop / tablet breakpoints only (no mobile-first work).

## 5. UI / UX improvements

- Dashboard: metric cards, empty recent state, health badges (client/store/health only).
- Analyze: grouped Personal / Place / Date / Time / Gender / Calendar sections; visible field errors; submit skeleton.
- Result: registry-driven tabs; Bazi / Score / Interpretation as collapsible section cards with honest empty states.
- Discussion: conversation / answer / sources+confidence panes; narrative kept as fallback `<details>`.
- History / Login / Profile / Reports: aligned with design-system panels and empty states.

## 6. Performance notes

- No new network calls except Discussion Expert asking via existing `/backend/api/v1/discussion`.
- CSS split via `@import` (acceptable without bundler); domain presenter CSS retained for visual continuity.
- Collapsible sections reduce initial scroll density without changing data binding.

## 7. Before / after previews

| | Path |
|--|------|
| **Before** | [`docs/reports/ui_v2_preview/index.html`](ui_v2_preview/index.html) |
| **After** | [`docs/reports/ui_commercial_preview/index.html`](ui_commercial_preview/index.html) |

Tabs: basic, calendar, bazi, score, interpretation, discussion.

Regenerate after:  
`node applications/customer_portal/tests/js/ui_commercial_preview_build.js`

## 8. Test results

| Check | Result |
|-------|--------|
| `python -m pytest applications/customer_portal/tests -q` | **18 passed**, 1 warning (Starlette/httpx deprecation) |
| Lint / Typecheck | **N/A** (portal has no ESLint/tsc pipeline) |
| Preview build | OK — wrote `docs/reports/ui_commercial_preview/` |

Remaining failures: **none** in portal module.

## 9. Freeze confirmations

| Area | Diff |
|------|------|
| `engines/` | **none** |
| `database/` | **none** |
| `applications/api/` | **none** |
| ResultStore key contracts | unchanged |
| `_layout.html` script order | `result_store.js` before `api.js` preserved |
| Golden / snapshot / expected | not modified |

Discussion UI **consumes** existing `POST /api/v1/discussion` only; no API schema or route edits.

## 10. Risks / follow-ups

- Disabled registry stubs (`luck_cycle`, `shensha`) await real payload fields — do not fabricate UI data.
- React consoles (`analysis_console`, `knowledge_console`, `validation_console`) remain for a later sprint.
- Optional: add portal ESLint later if requested; not required for this ship.
- Separate product gate: pre-existing `applications/api/tests` phase3–6 failures are **out of scope** for this presentation sprint.
