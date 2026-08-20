# G1-09 — Live Runtime Trace & Canonical Routing Audit

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-09 Phase 1 |
| **Date** | 2026-08-20 |
| **Mode** | TRACE ONLY — no restart, no rebuild, no code repair |
| **Status** | **G1-09 ROOT CAUSE IDENTIFIED** |

Phase 1 did not modify engines, adapters, Golden, snapshots, cache, or running processes.

---

## 1. User-visible symptom

Product Owner ran CASE-0001 on the live product and exported:

`C:\Users\MG\Downloads\nguyen-tien-son_2082026_V1.pdf`

- Created: **2026-08-20 10:09:23** (2 minutes before this audit started)
- Size: **487,824 bytes**, PDF 1.7
- Same size class as yesterday’s print export `nguyen-tien-son_19-8-2026.pdf` (488,158 bytes at 2026-08-19 10:37)
- Not the Report V1 Playwright filename (`BTE_CASE-0001_Nguyen_Tien_Son_Report_V1_0.pdf`)
- Stream content is Chrome print vectors (drawing operators), not Report V1 tagged HTML text

Live UI/PDF still shows the **pre–Gate-1 commercial picture**: Dụng = Thực Thần, duplicated Thần sát names, Điều hậu wrong climate, English `male`, name-only Thập thần, score **51.25 / D+** available on the payload that the old UI binds.

Meanwhile Cursor tests G1-01 → G1-08 PASS because they instantiate engines in a **new Python process** that reads current workspace files. The Product Owner browser does **not** use that process.

---

## 2. Frozen Truth markers (G1-01 → G1-08)

| Gate | Frozen expected (CASE-0001) |
|------|-----------------------------|
| G1-01 | Structured visible + hidden Ten Gods; same-stem hidden = Tỷ Kiên; day stem only = Nhật Chủ |
| G1-02 | `strength_score=0.87`, class `strong`, label `Thân vượng`, confidence `1.0`. Not `45.0` / `51.25` / `D+` as Điểm thân |
| G1-03 | `Chính Ấn`, rule `pat_ca_01`, main qi `Kỷ` |
| G1-04 | month Sửu, winter, climate cold, Điều hậu `Hàn · Cần ôn ấm`, `temperature_score≈0.72` = imbalance intensity |
| G1-05 | Title **Phân bố Ngũ hành**; counts Mộc 4 / Hỏa 5 / Thổ 6 / Kim 3 / Thủy 1; total 19 |
| G1-06 | Dụng `Hỏa · Bính · Thất Sát`, winner `sea_001`; not `Thực Thần` |
| G1-07 | Canonical aliases; no double Thiên Ất / Thiên Đức / Nguyệt Đức; Hồng Loan & Thiên Hỷ independent |
| G1-08 | Internal `male`; customer **Nam**; Thuận; start age 5; current **Ất Tỵ 2022–2031** |

---

## 3. Live backend PID / path / version

Product Owner Analyze goes here:

```text
Browser http://127.0.0.1:8081/analyze
  → POST /backend/api/v1/analyze   (portal proxy)
    → http://127.0.0.1:8000/api/v1/analyze
```

Confirmed by posting CASE-0001 to both URLs. Portal `/healthz` reports `api_base_url=http://127.0.0.1:8000`.

| Item | Evidence |
|------|----------|
| Listen | `127.0.0.1:8000` owned by **PID 4548** |
| Command | `.venv\Scripts\python.exe -m uvicorn applications.api.app:app --host 127.0.0.1 --port 8000 --log-level info` |
| **No `--reload`** | Process never picked up file changes after start |
| Sibling worker | PID **4728**, same command, `.venv` python.exe |
| Executable | Venv trampoline → `C:\Python314\python.exe` |
| Interpreter | Python 3.14 + repo `.venv` |
| Working tree | `C:\Users\MG\Documents\GitHub\BTE-Platform\BTE-Platform` |
| Start time | **2026-08-19 21:12:29** |
| Uptime at audit | ~13 hours |
| Environment | `BTE_API_BASE_URL` default `http://127.0.0.1:8000`; no second API on 8000 |
| `GET /version` | `api_version=1.0.0`, `schema_version=1.0.0`, `minimum_engine_version=1.0.0` (static contract; **not** a git fingerprint) |
| `GET /api/v1/version` | **404** (version is `/version`, not under `/api/v1`) |
| `GET /api/v1/health` | `{"status":"ok","service":"bte-applications-api","version":"1.0.0"}` |

Also running (not Analyze):

| PID | Port | App | Start |
|-----|------|-----|-------|
| 620 / 1444 | 8080 | `applications.web_admin.app` | 2026-08-19 21:12:31 |
| 10476 / 9420 | 8081 | `applications.customer_portal.app` | 2026-08-19 21:12:32 |

No Vite/Node dev server. No other listen on 5173/5177.

**Answer: Product Owner `/analyze` hits uvicorn PID 4548 on 127.0.0.1:8000, started 2026-08-19 21:12:29, no reload.**

---

## 4. Live frontend path / build / hash

| Item | Evidence |
|------|----------|
| App | FastAPI Customer Portal `http://127.0.0.1:8081` |
| Analyze UI | Jinja `templates/analyze.html` + `static/js/analyze.js` (**2026-08-02**) |
| Result UI | `templates/result_desktop.html` → `/static/dist/result.js` |
| Report composer | `templates/reports.html` → `/static/dist/report.js` + `static/js/reports.js` |
| Dev vs prod | **Production static build**, not Vite HMR |
| `result.js` mtime | **2026-08-14 00:33:13** |
| `report.js` mtime | **2026-08-14 00:33:13** (151-byte re-export of chunk) |
| SHA-256 `result.js` | `99DDF264EC61B8705BA0517600FE0CE38556BE7A2389D63B67B1A09CA3A8EE6C` |
| Current source | `src/adapters/*`, `fullReportViewModel.ts`, `genderDisplay.ts` edited **2026-08-20 09:54–10:00** |
| Dist contains `Phân bố Ngũ hành` | **No** (`Ngũ hành` appears 5× in `result.js`) |
| Dist gender helper | Aug 14 composer: `gender: customer.gender \|\| input.gender` → **leaks `male`** |
| Service worker | **None** in portal |

**Answer: Browser is running the 2026-08-14 bundle, not the Cursor source that just passed G1-08 tests.**

---

## 5. Live Analyze endpoint

| Item | Value |
|------|--------|
| User URL | `http://127.0.0.1:8081/analyze` |
| JS client | `static/js/api.js` → `fetch("/backend" + path)` |
| Proxied URL | `http://127.0.0.1:8000/api/v1/analyze` |
| Handler | `applications.api.routes.v1.analyze_endpoint` → `OrchestratorService.analyze` |
| Probe request id | `g1-09-live-case-0001` (direct) and `g1-09-portal-proxy` (via 8081) |
| Status | **200 Analyze OK** |
| Default form timezone | `Asia/Ho_Chi_Minh` (CASE-0001 frozen uses `Asia/Bangkok`; both UTC+7) |
| Gender control | `<select>` still includes **unspecified** (`value=""`) on live Jinja form |

Replay payload:

```json
{
  "year": 1987, "month": 1, "day": 21, "hour": 4, "minute": 30,
  "gender": "male", "timezone": "Asia/Bangkok",
  "full_name": "Nguyễn Tiến Sơn", "birth_place": "Hà Tây, Việt Nam"
}
```

---

## 6. CASE-0001 live API vs Frozen vs fresh workspace interpreter

Fresh column = **new** `OrchestratorService().analyze(...)` in a separate Python process started 2026-08-20 10:17, reading current workspace files. Live column = HTTP to PID 4548 (in-memory modules from 2026-08-19 21:12).

| Field | Frozen expected | Live API (PID 4548) | Fresh workspace process | PASS/FAIL live |
|---|---|---|---|---|
| gender internal | `male` | `customer.gender=male`, no `gender_label` | `male` + `gender_label=Nam` | FAIL display contract |
| gender display source | Nam | missing `gender_label`; UI would show `male` | Nam | FAIL |
| strength.score | 0.87 | **0.87** | 0.87 | PASS |
| strength.class | strong | `strength_level=strong`, reasoning `Thân vượng`, confidence `1.0` | same | PASS |
| score.total / grade (wrong semantic) | must not be Điểm thân | **`total_score=51.25`, `strength_score=45.0`, `grade=D+`** | `total_score=0.0`, `grade=""` | FAIL if UI binds `score` |
| temperature.climate | cold | **`temperature_level=hot`**, reasoning `Nhiệt khí nặng` | `cold` / `Hàn`, Sửu, winter, `Cần ôn ấm` | FAIL |
| temperature.dieu_hau | Cần ôn ấm | not published as Hàn/ôn ấm | `balancing_need_label=Cần ôn ấm` | FAIL |
| temperature_score | 0.72 imbalance | 0.7166… | 0.7166… `score_semantic=imbalance_intensity` | numeric PASS; semantic FAIL on live |
| pattern | Chính Ấn | `cach_cuc=Chính Ấn` | Chính Ấn | PASS name |
| pattern rule / main qi | `pat_ca_01` / Kỷ | **no `winning_rule_id`, no `month_main_qi`** | `pat_ca_01`, `month_main_qi=Kỷ` | FAIL extras |
| five_elements.counts | 4/5/6/3/1 | **4/5/6/3/1** | 4/5/6/3/1 | PASS counts |
| five_elements.status | must not drive Mạnh/Yếu | `EXCESS` on all four + Thủy `PRESENT` | (workspace adapter suppresses that) | RISK on old UI |
| useful_god | Hỏa · Bính · Thất Sát / `sea_001` | **`Thực Thần`** (`str_004`…) | `Hỏa · Bính · Thất Sát`, `sea_001` | FAIL |
| ten_gods | structured visible/hidden | **name-only** `visible: [Thất Sát, Kiếp Tài, Nhật Chủ, Thiên Ấn]`; `hidden` = stem names | structured objects + hidden ten-god names | FAIL |
| shensha | canonicalized | **8-name duplicates**: Thiên Ất + Thiên Ất Quý Nhân, Thiên Đức + Thiên Đức Quý Nhân, Nguyệt Đức + Nguyệt Đức Quý Nhân | 4 names: Thiên Ất Quý Nhân, Hồng Loan, Thiên Đức Quý Nhân, Nguyệt Đức Quý Nhân | FAIL |
| luck.current | Ất Tỵ 2022–2031 | **Ất Tỵ 2022–2031**, start_age **5**, direction `forward` | same + `direction_label=Thuận`, evidence `Nam · Niên can Bính Dương · Thuận` | numeric PASS; G1-08 presentation FAIL |
| luck.gender_label | Nam | `null` | Nam | FAIL |

Live and portal-proxy responses matched (`useful_god=Thực Thần`). The proxy is not a second backend.

---

## 7. Orchestrator call stack (live)

```text
POST /api/v1/analyze
  applications.api.routes.v1.analyze_endpoint
    OrchestratorService.analyze  → stage alias "analyze" → "delivery"
      CalendarEngine → BaziEngine → Pattern → Score → Luck → Interpretation → Report → Narrative
    attach_presentation_metadata  (live: gender only, no gender_label)
```

Live in-memory code is the import set from **21:12:29 19 Aug**. G1 commits after that start:

| Time | Commit | Topic |
|------|--------|--------|
| 19 Aug 21:12:29 | — | **API process start** |
| 19 Aug 21:15 | `29203ae9` | G1-01 audit doc |
| 19 Aug 21:50 | `6a1a842a` | Ten Gods facts / shaping |
| 19 Aug 22:29 | `9e0c4b82` | StrengthView fields |
| 19 Aug 22:43–23:47 | G1-03 | Pattern canonical context |
| 19 Aug 23:58–20 Aug 00:13 | G1-05 | Five elements adapter |
| 20 Aug 00:24 | G1-06 | Useful God audit/docs |
| 20 Aug 08:19–09:22 | G1-07 | ShenSha canonical |
| 20 Aug 10:16 | `113b473a` | Luck evidence metadata (HEAD during audit) |

`--reload` was **not** used. Changing `.py` on disk does not update PID 4548.

Not a wrong-installed wheel: `sys.path` of this venv starts at the repo root; `applications` resolves to `...\BTE-Platform\applications\__init__.py`. The process path is the Cursor workspace. The defect is **stale import cache**, not a second checkout.

---

## 8. Engine module files

Live process does not expose `module.__file__`. Bound path is the workspace (command line + venv sys.path). Content in memory ≠ current files.

Workspace files the **fresh** interpreter loaded (what a restart would get):

| Concern | `__file__` |
|---------|------------|
| Ten Gods | `engines\ten_gods_engine\__init__.py` |
| Strength | `engines\strength_engine\engine.py` + `applications\api\services\strength_truth.py` |
| Pattern | `engines\pattern_engine\engine.py` + `applications\api\services\pattern_truth.py` |
| Temperature | `applications\api\services\temperature_truth.py` |
| Five elements | API five-elements truth (counts already 4/5/6/3/1 on live) |
| Useful God | `applications\api\services\useful_god_truth.py` |
| ShenSha | bazi/shensha path used by G1-07 commits after start |
| Luck | `engines\luck_engine\engine.py`, `providers\dayun.py`, `providers\_common.py`, `applications\api\services\luck_truth.py`, `gender_truth.py` |

Proof live is not those current files: HTTP `useful_god=Thực Thần` vs disk `useful_display=Hỏa · Bính · Thất Sát`.

---

## 9. ResultStore comparison

ResultStore is **browser-only**:

- `sessionStorage` / `localStorage` keys: `bte_last_result`, `bte_history`, `bte_view_result`, `bte_current_analysis_id`
- Owner: `static/js/result_store.js` (mtime 2026-08-14)
- Write path: `analyze.js` `BtePortal.saveLastResult({ input, data })` then `location.assign("/result")`

There is **no server ResultStore**. Phase 1 cannot dump the Product Owner’s Chrome profile without touching their browser DB (not done).

Inference (high):

- Store copies the Analyze `data` object as-is.
- A run against PID 4548 therefore stores **live API truth** (Thực Thần, hot, duplicate shensha, `gender=male`, `score.grade=D+`).
- Our probe request ids were **not** written into their browser; their 10:09 PDF used whatever `bte_last_result` they produced on the same stale API.

Mismatch class: ResultStore ≈ live API. It is **not** a second older payload source unless they opened History (`?from=history`) or `?preview=1` (fixture).

---

## 10. `/result` comparison

```text
GET /result
  result_desktop.html
    result_store.js  → load bte_last_result
    /static/dist/result.js  (2026-08-14)
      resolveResultBoot → adaptAnalysisToCanonicalDesktop (old)
```

| Field | ResultStore (inferred = live API) | Adapter VM (Aug 14 bundle) | Rendered UI |
|-------|-----------------------------------|----------------------------|-------------|
| gender | `male` | `text(customer.gender)` → **male** | English leak |
| strength | 0.87 / strong / Thân vượng | current source maps canonical 0.87; **dist still can bind `score` 51.25 / D+** | mixed; D+ is on live `score` |
| Điều hậu | temperature `hot` | old adapter / missing climate labels | not `Hàn · Cần ôn ấm` |
| Five Elements | counts 4/5/6/3/1 | dist title **not** `Phân bố Ngũ hành` | title `Ngũ hành` risk; counts likely OK |
| Useful God | Thực Thần | copies `useful_god` | **Thực Thần** |
| ShenSha | 8 duplicated names | `bazi.shensha` array | old 8-name list |
| Luck | Ất Tỵ 2022–2031, age 5 | copies cycles | timeline OK; missing Nam/Thuận evidence line |

`?preview=1` would render **mock** Canonical Desktop (bundle still contains mock S06/S10). Default `/result` after Analyze uses store, not preview.

---

## 11. Report builder trace

Live report is **not** `build_presented_report` / Report V1 HTML/PDF exporter.

| Path | What runs |
|------|-----------|
| API `data.report` | Legacy dict `{title, markdown, html, section_count}` — HTML starts `<h1>Bản luận Bát tự</h1>` |
| `/reports` print/download | `reports.js` `composeHtmlDocument` → prefers `window.BteFullReport` from **`/static/dist/report.js` (14 Aug)** over `data.report.html` |
| Fallback | `BtePresenters.composeExecutiveReport` + legacy `report.html` if composer missing |
| Report V1 `HtmlReportV1Renderer` / Playwright | **Not** invoked by portal print |

So structured Analyze exists, but customer Report/PDF uses **Aug 14 Full Report composer + ResultStore**, or Chrome print of Canonical Desktop. Legacy `data.report.html` remains on the payload and is the fallback.

---

## 12. PDF source trace

File: `C:\Users\MG\Downloads\nguyen-tien-son_2082026_V1.pdf`

| Item | Evidence |
|------|----------|
| Timestamp | 2026-08-20 **10:09:23** |
| Generator | Chrome print-to-PDF (PDF 1.7, Flate vector `cm`/`c`/`f` operators; no Unicode report strings) |
| Not | Playwright `PdfExporterV1` (those CASE-0001 files are ~3.5MB under `knowledge/report_v1_validation` / editorial exports, dated 16 Aug) |
| Portal actions that call `window.print()` | Canonical Desktop `#xuat` / header (`PortalChrome.tsx`); `/reports` `printReport()` |
| Pre-PDF HTML | Either printed `/result` DOM (old `result.js`) or `/reports` HTML from old `report.js` + ResultStore |
| HTML-before-PDF | **Already old** (stale API + stale bundle) |
| PDF vs HTML | Same generation path; not a stale PDF cache of a correct HTML |

Filename `nguyen-tien-son_2082026_V1.pdf` is the Product Owner’s Save-as name (date 20/8/2026 + V1), not `build_export_filename()`.

---

## 13. DOCX

Customer Portal download path emits **HTML** (`safeFilename(name)+".html"`), not DOCX. No live DOCX was found next to the 10:09 PDF. API `POST /api/v1/report` still returns legacy markdown/html, not Report V1 DOCX export.

**N/A for this Product Owner export.** PDF and DOCX are not a paired V1 export.

---

## 14. Analysis ID consistency

| Surface | ID |
|---------|----|
| Audit direct Analyze | `g1-09-live-case-0001` (header `X-Request-ID`) |
| Audit portal proxy | `g1-09-portal-proxy` |
| Product Owner PDF | no analysis id in extractable text; store uses last Analyze `request_id` |
| ResultStore | client-generated / echoed `request_id`; not a server session |

PO’s PDF and their `/result` share whatever id was in `bte_last_result` at 10:09. Audit probes did **not** overwrite that (server has no store).

---

## 15. Cache / build / process audit

| Check | Result |
|-------|--------|
| Browser service worker | None |
| Vite dist on disk | **Old (14 Aug)** — this is the served asset, not a CDN cache |
| Reverse proxy | Portal FastAPI proxy only; no nginx in process list |
| Backend restart | **None since 19 Aug 21:12** |
| Multiple uvicorn on 8000 | **One listener (PID 4548)** |
| `--reload` | **Off** |
| Global pip package overlay | Repo-root `sys.path` first; no separate installed BTE engine distro observed |
| Stale `.pyc` | Irrelevant while process holds old modules in RAM |

---

## 16. Multiple repo / worktree audit

| Question | Evidence |
|----------|----------|
| Cursor workspace | `C:\Users\MG\Documents\GitHub\BTE-Platform\BTE-Platform` |
| Backend cwd/module root | Same path |
| Frontend files served | Same path `applications\customer_portal\static\dist` |
| `git worktree list` | Single worktree |
| Other `BTE-Platform` copies serving ports | **None** |

Not a wrong-checkout problem. Same tree, **old process + old dist**.

---

## 17. Version fingerprint

| Fingerprint | Live runtime | Workspace now |
|-------------|--------------|---------------|
| Git HEAD | unknown to process (started before today’s commits) | `113b473a` `release/v1.0-final` (2026-08-20 10:16) |
| Branch | n/a | `release/v1.0-final` |
| Backend start | 2026-08-19 21:12:29 | — |
| Frontend bundle | 2026-08-14 00:33:13 / SHA-256 `99DDF264…A8EE6C` | source newer; dist **not rebuilt** |
| `GET /version` | `1.0.0` / `1.0.0` / `1.0.0` | same constants — **useless as Gate fingerprint** |
| Engine versions in Analyze | `*_source` layer names only, no git hash | — |

---

## 18. Exact root cause(s)

### A. Backend stale runtime — **HIGH**

Uvicorn without reload, started **before every G1-01…G1-08 code commit**. Live HTTP still returns G1-06 winner `Thực Thần`, G1-04 `hot`, G1-07 duplicate shensha, G1-01 name-only ten gods, no G1-08 `gender_label`.

A new Python `OrchestratorService` on the **same files** returns Frozen Useful God / temperature / ShenSha / Ten Gods / Nam.

### C. Frontend stale build — **HIGH**

`static/dist/result.js` + `report.js` dated **2026-08-14**. Cursor G1 UI/source was never compiled into what `:8081` serves. Dist omits `Phân bố Ngũ hành` and maps gender from raw `male`.

### D. Adapter / field routing — **HIGH** (on the live bundle)

Aug 14 Full Report / Desktop adapters:

- echo `customer.gender` (`male`)
- can label score as `total_score / grade` → **51.25 / D+**
- Ten Gods from `visible` string list
- ShenSha from raw `bazi.shensha`
- Useful God from `useful_god` string (`Thực Thần`)

Current unbuilt source already localizes Nam and binds canonical strength 0.87 — **not what the browser runs**.

### E. Report / PDF legacy path — **HIGH**

PO PDF is **Chrome print** of `/result` or `/reports`, not Report V1 Playwright. Pre-PDF HTML is already the old composer + stale Analyze payload.

### G. Mixed runtime — **HIGH**

Some Frozen numbers already exist on the old process (0.87, Chính Ấn, 4/5/6/3/1, Ất Tỵ 5). That makes the product look “half updated” and hides that G1-04/06/07/01/08 presentation never loaded.

### Not B

Same repo, same venv, same ports.

### Not a nameless “cache issue”

No service worker. The files on disk that FastAPI serves **are** the 14 Aug build. The API process **is** the 19 Aug 21:12 import set.

---

## 19. Blocker conditions

| # | Condition | Blocker? |
|---|-----------|----------|
| 1 | Live API ≠ Frozen Truth | **YES** |
| 2 | Loaded module path ≠ workspace | Path same; **memory stale** (treat as 1) |
| 3 | Frontend bundle old | **YES** (14 Aug) |
| 4 | ResultStore ≠ API | Inferred **equal to live API** (also old) |
| 5 | `/result` ≠ store | **YES** extra distortion from old `result.js` |
| 6 | Report ≠ `/result` | **YES** if print uses `/reports` composer; both old |
| 7 | PDF ≠ report HTML | PDF **is** print of that HTML/DOM; both old |
| 8 | Analysis id changes across surfaces | Not proven for PO session; audit probes used distinct `X-Request-ID` |
| 9 | Legacy payload override | **YES** `data.report.html` still legacy; composer/dist override when present |
| 10 | Multiple copies unclear | **NO** — one worktree |
| 11 | Browser ≠ Cursor test server | **YES** — PO hits PID 4548; pytest uses a **new** TestClient/process |

---

## 20. Minimal repair plan (Phase 2 — do not execute now)

1. **Restart** `applications.api.app` uvicorn on 8000 (same command is fine; must load current modules). Do not change engine formulas.
2. **Rebuild** portal: `applications/customer_portal` Vite production `result.js` / `report.js` from current `src/`.
3. Restart portal 8081 only if it caches open file handles (usually static files are read per request; rebuild is the required step).
4. Product Owner: hard refresh, **new Analyze** CASE-0001 (Nam, 21/01/1987 04:30), then `/result` and print/PDF again.
5. Re-trace the §6 table against live HTTP after restart. Expect `useful_display=Hỏa · Bính · Thất Sát`, temperature `Hàn · Cần ôn ấm`, `gender_label=Nam`, structured ten gods, canonical shensha.

Do **not** in Phase 2 (unless a new mismatch remains after restart+rebuild): edit G1-01…G1-08 engines, Golden, snapshots, or “fix” tests.

---

## 21. Files / processes / builds that would need change

| Need change | What |
|-------------|------|
| Process | Restart PID 4548 (and typically 4728) API uvicorn |
| Build | Rebuild `applications/customer_portal/static/dist/*` |
| Browser | New Analyze so `bte_last_result` is the new payload; normal refresh |
| Optional | Restart portal 8081; remove Jinja “unspecified” gender **only if** still present after rebuild (live `analyze.html` still has it — presentation bug, separate from engine freeze) |

---

## 22. What does NOT need change

- Calendar / pillar math for CASE-0001 (live already Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần)
- Luck JiaZi sequence / start age 5 / Ất Tỵ 2022–2031 (already on live API)
- Strength 0.87 / strong (already on live API)
- Five-element counts 4/5/6/3/1 (already on live API)
- Frozen Golden Dataset / snapshots
- G1-01…G1-08 engine repairs already on disk (they work in a **new** interpreter)
- Inventing a second backend or another git clone

---

## 23. Output status

**G1-09 ROOT CAUSE IDENTIFIED**

Live product is old because:

1. Analyze is served by a **13-hour-old uvicorn without reload**, started before G1-01–G1-08 code landed; and
2. `/result` and PDF print use a **6-day-old Vite bundle** (`static/dist` 2026-08-14).

Tests PASS because they never talk to PID 4548 or `result.js`.

STOP. No restart, rebuild, cache clear, adapter edit, report edit, engine edit, Golden edit, or deploy in this phase.
