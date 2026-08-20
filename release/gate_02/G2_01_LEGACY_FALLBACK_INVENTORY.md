# G2-01 — Legacy / fallback inventory

## Legacy routes & modules

| Path | Classification | Notes |
|------|----------------|-------|
| `GET /result?legacy=1` → `result_legacy.html` + `static/js/result.js` | **EXPLICIT LEGACY ONLY** | `loadForView()` = view **or** last (ignores `from=history`). Presenters may read `pattern.hy_than` / `useful_god` loosely. |
| `templates/result.html` | **DEAD** | Meta-refresh to `/result`. |
| `static/js/presenters/*` (`summary_builder`, `pattern`, `executive`, `discussion`) | **FALLBACK** on `/reports` if unstructured; **ACTIVE** on legacy result | Keys include `hy_than`, `favorable_god`, `xi_shen`. |
| `bte_portal_last_result` / `bte_portal_history` | **FALLBACK** (read) | ResultStore `load()` / `loadHistory()` still read these. Fresh `save()` deletes legacy last key. |
| React `PortalApp` + Result V2 + `portalDemoReport` | **EXPLICIT LEGACY ONLY** (not in `app.py`) | No analysis id → **demo** payload. In-memory session; refresh loses live result. |
| `BaZiResultScreen` | **DEAD** on production /result | Not mounted by `resultApp.tsx`. |
| `AnalyzeService.getCanonicalDesktopViewModel` re-POST | **FALLBACK** | Production boot passes `initialData` and `request: null`, so /result does **not** re-analyze. Would re-run engines if hook used with request only. |
| Score `wuxing_score` / `ten_god_score` | **DEAD** for Canonical Desktop | Adapters explicitly ignore. Fields still exist on DTO. |
| Report V1 PDF/DOCX | **ACTIVE** server ops | Not a Portal customer control. Different path from Print. |

## Fallback activation (high risk)

| Condition | Activates? After fresh Analyze? | Override structured truth? |
|-----------|--------------------------------|----------------------------|
| Empty ResultStore on `/result` | **Yes — mock Canonical Desktop fixture** (`previewFallback: true`) | Shows complete fake analysis, not empty gate |
| `?preview=1` | Yes | Fixture, not stored analysis |
| Missing `favorable_display` | S02 Hỷ → `pattern.hy_than` then `—` | Latent; Frozen payloads currently populate both |
| Missing `useful_display` | S02 Dụng → `useful.useful_god` then `pattern.dung_than` | Latent compact name |
| Unstructured history row on `/reports` | `report.html` / markdown | Yes if old HTML stored |
| `BteFullReport` script delayed | reports wait ~2s then may compose executive HTML | After Analyze, structured path still preferred once composer loads |
| No current last_result but `bte_view_result` exists | TS `resolveCurrentStoredResult` source=`legacy` **without** `from=history` | Can show leftover view as if current |
| PortalApp without session | demo report | Not production host |
| `useful_god_source.contract` mismatch | **Not detected** | Old bundle / old API can render silently |

## Dead vs canonical

Canonical customer result is **only** `/result` Desktop V2 + `/interpretation` (same template) + `/reports` structured composer + History `selectForView`.

Nothing else may be called canonical.
