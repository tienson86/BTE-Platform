# BTE Customer Portal — QA Report

**Audit date:** 2026-07-25
**Scope:** Customer Portal presentation layer only
**Constraints:** No Engine / API / Knowledge / Rule Database changes

---

## Summary

- Passed: **71**
- Warnings: **0**
- Bugs: **0**
- UX notes: **5**
- Accessibility notes: **5**
- Performance notes: **9**

### Coverage checked

- Dashboard
- Analyze
- Result presenters: Calendar, Bazi, Pattern, Score, Interpretation, Narrative
- Reports (search / filter / sort / preview / actions)
- History, Profile, Login
- Routes, static assets, dark mode CSS, print CSS, responsive breakpoints

---

## 1. Passed items

- Root redirects to /dashboard
- Route OK /dashboard
- Template exists dashboard.html
- Route OK /analyze
- Template exists analyze.html
- Route OK /result
- Template exists result.html
- Route OK /reports
- Template exists reports.html
- Route OK /history
- Template exists history.html
- Route OK /profile
- Template exists profile.html
- Route OK /login
- Template exists login.html
- Static asset OK /static/css/portal.css
- Static asset OK /static/js/analyze.js
- Static asset OK /static/js/api.js
- Static asset OK /static/js/dashboard.js
- Static asset OK /static/js/history.js
- Static asset OK /static/js/login.js
- Static asset OK /static/js/presenters/bazi.js
- Static asset OK /static/js/presenters/calendar.js
- Static asset OK /static/js/presenters/interpretation.js
- Static asset OK /static/js/presenters/narrative.js
- Static asset OK /static/js/presenters/pattern.js
- Static asset OK /static/js/presenters/score.js
- Static asset OK /static/js/profile.js
- Static asset OK /static/js/reports.js
- Static asset OK /static/js/result.js
- Presenter exists calendar.js
- Presenter exists bazi.js
- Presenter exists pattern.js
- Presenter exists score.js
- Presenter exists interpretation.js
- Presenter exists narrative.js
- Dark mode CSS tokens present
- Print stylesheet present
- Responsive breakpoints present
- Reports feature code present: Search
- Reports feature code present: Filter
- Reports feature code present: Sort
- Reports feature code present: Copy
- Reports feature code present: Download
- Reports feature code present: Print
- Narrative Copy/Print actions present
- Dashboard Quick Actions visible
- Analyze Run button visible
- Result stage tabs visible
- Report Center heading visible
- Dashboard renders at mobile viewport
- Analyze navigates to /result
- Result presenter renders: calendar
- Result presenter renders: bazi
- Result presenter renders: pattern
- Result presenter renders: score
- Result presenter renders: interpretation
- Result presenter renders: narrative
- Narrative Copy control present
- Narrative Print control present
- Narrative collapse/expand controls present
- Reports search control present
- Reports filter control present
- Reports sort control present
- Reports action toolbar present (or ready after selection)
- Reports Copy action visible after selection
- Reports Download action visible after selection
- Reports Print action visible after selection
- Dark scheme applied (body background=rgba(0, 0, 0, 0))
- No uncaught pageerrors during browser audit
- No application console.error (excluding resource load noise)

## 2. Warnings

- None

## 3. Bugs

- None found in this audit pass

## 4. UX improvements

- Result presenters hide raw JSON for Calendar–Narrative; other stages use cards/report UI
- Dashboard stats use local history (Average Score remains '--' without a stats API)
- Share on Reports is explicitly a placeholder
- PDF download only when API provides PDF URL — no client PDF generation
- Report Center lists local analyze history only (no remote report list API)
- Add explicit empty-state CTAs on Result when session has no analyze yet (beyond meta text)
- Consider persisting theme toggle (`data-theme`) in addition to `prefers-color-scheme`
- Reports table is hidden on narrow screens — ensure card list remains primary on mobile (already true)

## 5. Accessibility notes

- /dashboard has h1 (1)
- /analyze has h1 (1)
- /reports has h1 (1)
- Nav links are text anchors; consider skip-to-content link for keyboard users
- iframe report preview may need title already present — verify screen reader announcement

## 6. Performance observations

- healthz load 677 ms
- /dashboard DOMContentLoaded 286 ms
- /analyze DOMContentLoaded 819 ms
- /result DOMContentLoaded 131 ms
- /reports DOMContentLoaded 122 ms
- /history DOMContentLoaded 66 ms
- /profile DOMContentLoaded 43 ms
- /login DOMContentLoaded 46 ms
- Analyze→Result depends on API warm/cold; first analyze can exceed 1s

---

## Feature matrix

| Area | Status | Notes |
|------|--------|-------|
| Broken links | Checked | Nav + Quick Actions + static assets |
| Missing routes | Checked | All NAV_ITEMS + login + healthz |
| JavaScript errors | Checked | Playwright pageerror + console.error |
| Console warnings | Checked | Captured when present |
| Responsive | Checked | CSS breakpoints + mobile viewport smoke |
| Dark mode | Checked | CSS tokens + emulate dark scheme |
| Print | Checked | `@media print` + Narrative/Reports print actions |
| Copy | Checked | Narrative + Reports actions |
| Download | Checked | Reports download for HTML/MD when payload exists |
| Search / Filter / Sort | Checked | Report Center controls |

## Raw console (truncated)

```
(none)
```

## Verdict

**Portal QA: PASS with notes** — core flows and presentation layers work; warnings/UX/a11y items are non-blocking.
