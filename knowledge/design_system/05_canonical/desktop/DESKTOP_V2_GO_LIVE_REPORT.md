# DESKTOP_V2_GO_LIVE_REPORT.md

> BTE Customer Portal
>
> Status: **PRODUCTION**
>
> Date: 2026-08-07
>
> Sprint: `SPRINT_GO_LIVE_DESKTOP_V2`

---

## Verdict

**Canonical Desktop V2 is now the production Result UI.**

| Route | UI |
|-------|----|
| `/result` | PortalPage (Desktop V2) |
| `/result?preview=1` | Fixture preview mode |
| `/result?legacy=1` | Legacy presenters (escape hatch only) |

Birth Input (`/analyze`) → ResultStore → `/result` → Desktop V2.

---

## Screenshots

Captured from live portal (`http://127.0.0.1:8081/result?preview=1`).

| Viewport | File |
|----------|------|
| 1366×1000 | `applications/customer_portal/src/screens/canonical_desktop/polish/GO_LIVE_1366.png` |
| 1600×1000 | `applications/customer_portal/src/screens/canonical_desktop/polish/GO_LIVE_1600.png` |
| 1920×1000 | `applications/customer_portal/src/screens/canonical_desktop/polish/GO_LIVE_1920.png` |
| 1600 full-page preview | `applications/customer_portal/src/screens/canonical_desktop/polish/GO_LIVE_1600_preview.png` |
| Pre-freeze reference | `applications/customer_portal/src/screens/canonical_desktop/polish/BEFORE_desktop_v2.png` |

Viewport token check (automated): `--cd-content-w: 1600px`, sidebar `280px`, fluid `minmax(0,1fr)` main column — passes for 1366 / 1600 / 1920.

---

## Routing

```
GET /analyze
  → templates/analyze.html + static/js/analyze.js
  → POST /backend/api/v1/analyze
  → ResultStore.save({ input, data })
  → location.assign("/result")

GET /result
  → render_desktop_page("result_desktop.html")   # no legacy app-shell
  → #canonical-desktop-root
  → /static/dist/result.js  (Vite bundle)
  → resultApp → PortalPage

GET /result?legacy=1
  → legacy _layout + result_legacy.html + presenters
```

### Host changes

| File | Change |
|------|--------|
| `applications/customer_portal/app.py` | `/result` → Desktop V2; `?legacy=1` keeps old UI |
| `templates/result_desktop.html` | Full-bleed React host |
| `templates/result_legacy.html` | Former result body |
| `templates_util.py` | `render_desktop_page()` |
| `pages/result.py` | Template = `result_desktop.html` |
| `static/dist/result.js` + `result.css` | Production bundle |

---

## Runtime flow

```
ResultStore.loadForView()
        │
        ├─ has input + data  → adaptAnalysisToCanonicalDesktop(data)
        │                      → PortalPage initialData (engine-live)
        │                      → NO second analyze call
        │
        ├─ has input only    → PortalPage request
        │                      → AnalyzeService.getCanonicalDesktopViewModel
        │                      → POST /analyze → adapter
        │
        └─ no request        → fixture preview (dashboard-preview)
                               (?preview=1 forces this)
```

Provider path:

```
PortalPage
  → useCanonicalDesktopResult
  → CanonicalDesktopProvider
  → S00–S11 + PortalChrome  (Provider only — no mockData imports)
```

Modes:

| Mode | Condition | `data-mode` |
|------|-----------|-------------|
| Preview | no request | `dashboard-preview` |
| Production | request or adapted `initialData` | `engine-live` |

---

## Verification

| Check | Result |
|-------|--------|
| Sections/shell/rows import mockData | **None** (guard test) |
| `/result` serves Desktop mount | **200** + `#canonical-desktop-root` |
| `/static/dist/result.js` | **200** |
| Legacy not on default `/result` | **Pass** (`reportHost` absent) |
| `/result?legacy=1` | **200** with legacy host |
| Unit tests (desktop + adapter + boot + viewports + no-mock) | **Pass** |
| Refresh / navigate | Bundle is static; ResultStore survives same-tab refresh |

### Tests run

```
vitest:
  canonical_desktop.test.tsx
  canonical_desktop_adapter.test.tsx
  result_app_boot.test.ts
  canonical_desktop_no_mock_imports.test.ts
  canonical_desktop_viewports.test.ts
```

### Build

```
cd applications/customer_portal
npm run build:result
```

---

## Remaining known issues

| ID | Issue | Severity |
|----|-------|----------|
| GL-01 | S10 bone-weight still fixture (no engine) | Medium |
| GL-02 | Interpretation → S08/S11 list mapping is heuristic | Medium |
| GL-03 | Feng Shui bullets partially derived from calendar fields | Low |
| GL-04 | Visual polish backlog still open (see `DESKTOP_V2_VISUAL_POLISH_BACKLOG.md`) | Low |
| GL-05 | Deploy must run `npm run build:result` (or ship `static/dist`) | Ops |
| GL-06 | Double chrome avoided via blank desktop layout; other portal pages still use legacy shell | Info |

---

## Production declaration

Desktop V2 is the **Production UI** for Result.

- No redesign in this sprint
- No visual polish in this sprint
- Legacy Result is no longer the default runtime path

---

END
