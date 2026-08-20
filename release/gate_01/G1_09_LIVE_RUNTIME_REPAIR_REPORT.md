# G1-09 — Live Runtime Canonical Repair Report

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-09 Phase 2 |
| **Date** | 2026-08-20 |
| **Mode** | Runtime process + frontend build + canonical live routing |
| **Status** | **G1-09 LIVE RUNTIME REPAIR: PASS** |

Engines, Golden, snapshots, and G1-01 → G1-08 algorithms were not modified.

One presentation-routing change was required so `/result` paints G1-04 Điều hậu that already existed on the adapter ViewModel and Full Report: `applications/customer_portal/src/adapters/canonicalDesktopAdapter.ts` (S02 indicators).

---

## 1. Stale backend stopped

| Item | Evidence |
|------|----------|
| Listen before stop | `127.0.0.1:8000` → **PID 4548** (child of 4728) |
| Command | `.venv\Scripts\python.exe -m uvicorn applications.api.app:app --host 127.0.0.1 --port 8000 --log-level info` |
| Start | 2026-08-19 21:12:29 |
| Stopped | **PID 4548** then parent **PID 4728** (same uvicorn tree) |
| After stop | Port 8000 **FREE** |
| Left running | Admin PID 620/1444 on 8080; Portal PID 10476/9420 on 8081 |

Unrelated Python processes were not killed.

---

## 2. New backend PID / path

| Item | Value |
|------|-------|
| Shell wrapper | PID **9824** |
| Venv parent | PID **4680** (`.venv\Scripts\python.exe`) |
| **Listen PID** | **1380** on `127.0.0.1:8000` |
| Executable | `"C:\Users\MG\Documents\GitHub\BTE-Platform\BTE-Platform\.venv\Scripts\python.exe"` (trampoline → `C:\Python314\python.exe`) |
| Command | `-m uvicorn applications.api.app:app --host 127.0.0.1 --port 8000 --log-level info` |
| cwd | `C:\Users\MG\Documents\GitHub\BTE-Platform\BTE-Platform` |
| Start | **2026-08-20 10:31:38** |
| `--reload` | **Off** (canonical command; modules loaded at start from current tree) |
| Git HEAD at start | `113b473ac25d3df68dd69551eb5f5c65ab32b859` (`release/v1.0-final`) |

Not global Python. Not a second checkout.

---

## 3. Backend smoke test

Loaded module `__file__` (same venv + cwd as uvicorn):

| Concern | Path |
|---------|------|
| Ten Gods | `...\engines\ten_gods_engine\__init__.py` |
| Strength | `...\engines\strength_engine\engine.py` + `applications\api\services\strength_truth.py` |
| Pattern | `...\engines\pattern_engine\engine.py` + `applications\api\services\pattern_truth.py` |
| Temperature | `...\applications\api\services\temperature_truth.py` |
| Useful God | `...\applications\api\services\useful_god_truth.py` |
| ShenSha | `...\engines\bazi_engine\shensha\service.py` |
| Luck | `...\engines\luck_engine\engine.py` + `applications\api\services\luck_truth.py` |
| Orchestrator | `...\applications\api\services\orchestrator.py` |

All under current workspace. Smoke CASE-0001 was sent through the Product Owner path:

`POST http://127.0.0.1:8081/backend/api/v1/analyze`  
Header: `X-Request-ID: g1-09-p2-smoke-case-0001`  
Status: **200**

Frozen markers on that live API payload: **PASS** (see §8). Frontend rebuild started only after this smoke passed.

---

## 4. Frontend build command

```text
cd applications/customer_portal
npm install --no-fund --no-audit
npm run build:result
```

Canonical script: `vite build --mode production` → `static/dist/result.js` + `report.js` + chunks.

Second `npm run build:result` after S02 climate routing so `/result` paints Điều hậu.

Portal PID 10476 was **not** restarted. `StaticFiles` reads disk per request; HTTP hash matched the new file.

---

## 5. Old vs new bundle timestamp / hash

| File | Old (14 Aug) | New (20 Aug) |
|------|----------------|--------------|
| `result.js` | 295392 B · 2026-08-14 00:33:13 · SHA256 `99DDF264…A8EE6C` | **294020 B · 2026-08-20 10:43:02 · SHA256 `8FB91898CADB53AEA4875760087CAD489D0838EA7367724189FA53C594291D91`** |
| `report.js` | 151 B · 2026-08-14 00:33:13 · SHA256 `06EBACD8…9CE35C` | **151 B · 2026-08-20 10:34:43 · SHA256 `1E97B3168033ECFDC1CEC63B0B272A3EE0830FBC62037564CF7525835B16F265`** |
| report chunk | `fullReportViewModel-BPBFcK5B.js` | **`fullReportViewModel-Dl6gd0lq.js`** SHA256 `9406577246AADC8423410D3DD58D110F1F10628E0E6B77D3104F0EBB54581E19` |

Old hashed chunk `fullReportViewModel-BPBFcK5B.js` now **HTTP 404**.

`result.js` contains `Phân bố Ngũ hành` (was absent on 14 Aug bundle).

---

## 6. Served-bundle verification

`GET http://127.0.0.1:8081/static/dist/result.js` with `Cache-Control: no-cache`:

- HTTP body SHA256 = disk SHA256 `8FB91898…291D91`
- `Last-Modified: Thu, 20 Aug 2026 03:43:02 GMT` (UTC)
- No `Cache-Control` header (ETag/Last-Modified only). New ETag ⇒ browsers with the old `result.js` receive 200, not a stale 304 of the 14 Aug file.
- No service worker on the portal.

**Browser is served the new bundle.** Product Owner should still hard-refresh once so any memory-cached 14 Aug `result.js` is dropped.

---

## 7. New CASE-0001 analysis ID

Live Birth Input UI (`http://127.0.0.1:8081/analyze`), not a TestClient:

| Field | Value |
|-------|-------|
| Name | Nguyễn Tiến Sơn |
| Place | Hà Tây, Việt Nam |
| Birth | 21/01/1987 04:30 |
| Gender select | `male` (customer display Nam) |
| Timezone | Asia/Bangkok |
| Analyze URL | `POST http://127.0.0.1:8081/backend/api/v1/analyze` → `127.0.0.1:8000` |
| **Analysis ID** | **`bte-1987-1-21-4-30-1787197461334`** |
| ResultStore key | `bte_current_analysis_id` (same id) |
| `/result` DOM | `data-analysis-id="bte-1987-1-21-4-30-1787197461334"` |
| Report composer | same id (`Mã phân tích …`) |
| Timestamp | 2026-08-20 10:44 (store `saved_at` / UI run) |

Old `bte_last_result` was cleared in the verification session before Analyze. History did not override current.

---

## 8. Live API frozen-truth comparison

| Marker | Expected | Live API (via 8081) | PASS/FAIL |
|--------|----------|---------------------|-----------|
| Gender internal | `male` | `customer.gender=male` | PASS |
| Gender display | Nam | `customer.gender_label=Nam` | PASS |
| Strength score | 0.87 | `strength_score=0.87` | PASS |
| Strength class | strong / Thân vượng | `strength_level=strong`, reasoning `Thân vượng` | PASS |
| Pattern | Chính Ấn | `cach_cuc=Chính Ấn`, `winning_rule_id=pat_ca_01`, main qi `Kỷ` | PASS |
| Climate | cold | `climate_state=cold`, label `Hàn` | PASS |
| Điều hậu | Cần ôn ấm | `balancing_need_label=Cần ôn ấm` | PASS |
| Five Elements | 4/5/6/3/1 | wood 4 / fire 5 / earth 6 / metal 3 / water 1, total 19 | PASS |
| Useful God | Hỏa · Bính · Thất Sát / `sea_001` | `useful_display=Hỏa · Bính · Thất Sát`, `winning_rule_id=sea_001` | PASS |
| ShenSha | canonical, no alias doubles | Thiên Ất Quý Nhân, Hồng Loan, Thiên Đức Quý Nhân, Nguyệt Đức Quý Nhân | PASS |
| Luck | Ất Tỵ 2022–2031, start 5 | `gan_zhi=Ất Tỵ`, years 2022–2031, `start_age=5`, `direction_label=Thuận` | PASS |

---

## 9. `/result` comparison

Live page after new Analyze + new `result.js`:

| Marker | `/result` |
|--------|-----------|
| Giới tính | **Nam** (no English `male`) |
| Strength | **Thân vượng** **0.87** (not 51.25 / D+ as Điểm thân) |
| Pattern | **Chính Ấn** |
| Điều hậu | **Hàn** · **Cần ôn ấm** in CHỈ SỐ CỐT LÕI |
| Five Elements | Title **Phân bố Ngũ hành**; Mộc 4 · Hỏa 5 · Thổ 6 · Kim 3 · Thủy 1 |
| Useful God | **Hỏa · Bính · Thất Sát** (not `Dụng thần: Thực Thần`) |
| ShenSha | Four canonical names only; aliases not double-published |
| Luck | Visualization: **Hiện tại · Ất Tỵ 2022–2031**, **Tuổi khởi Đại vận: 5** |

Ten Gods: lộ can Thất Sát / Kiếp Tài / Nhật Chủ / Thiên Ấn; tàng can kept as structured hidden lines (Giáp · Mộc · Thiên Tài, …).

---

## 10. Report comparison

`/reports` → select current analysis → `#previewHtml` uses `BteFullReport.build` / `render` from **`fullReportViewModel-Dl6gd0lq.js`**.

Same analysis ID as `/result`. Not a previous History payload.

All Frozen markers present, including:

- Giới tính **Nam**
- Điểm thân **0.87**
- Trạng thái khí hậu **Hàn** / Nhu cầu điều hòa **Cần ôn ấm**
- Dụng thần **Hỏa · Bính · Thất Sát**
- Đại vận hiện tại **Ất Tỵ 2022–2031**, Thuận, tuổi khởi **5**
- ShenSha canonical list

Cover line also shows **Điểm tổng `55.05 / D+`** (Score Engine composite — see §13). That is not Điểm thân.

---

## 11. PDF comparison

Two export classes (not the same path):

| Path | What it is | Artifact |
|------|------------|----------|
| **Chrome-print PDF** | Chromium `page.pdf()` of `/result` (same `window.print()` family the Product Owner used) | `release/gate_01/G1_09_CASE0001_result_chrome_print.pdf` (417,122 B, 2026-08-20 10:44:25, Skia/PDF, Creator Chromium) |
| **Full Report print PDF** | Chromium print of composed Full Report HTML | `release/gate_01/G1_09_CASE0001_full_report_print.pdf` (81,566 B, 2026-08-20 10:44:29, title `Báo cáo Bát Tự — Nguyễn Tiến Sơn`) |
| **Report V1 Playwright** | `PdfExporterV1` / `BTE_CASE-0001_…_Report_V1_0.pdf` | **Not** invoked by Customer Portal Xuất |

PO’s old file `nguyen-tien-son_2082026_V1.pdf` was Chrome print of the **old** `/result`. New result print is the same generator class, new DOM.

Pre-PDF HTML/DOM for both new files contained every Frozen marker in §17. Skia PDFs do not expose those Unicode strings as extractable text (same as the 10:09 PO file). **Defect is not “PDF cache of a correct HTML”.** HTML-before-PDF is new.

---

## 12. Narrative stale-data check

Full Report luận giải (live composer, same analysis):

- **Not** `Dụng thần được chọn: Thực Thần`
- **Is** `Dụng thần được chọn: Bính`
- Supporting: `Mùa đông hàn cần hỏa` · `Bính: Mùa đông hàn cần hỏa`

Narrative copy still names the stem **Bính** rather than the rich triple `Hỏa · Bính · Thất Sát`. That is Deep Narrative wording, not a stale Useful God winner. Deep Narrative content was not edited.

---

## 13. Score result

| Semantic | Live value |
|----------|------------|
| Điểm thân (G1-02) | **0.87** / strong / Thân vượng |
| Score Engine `total_score` / `grade` | **55.05 / D+** |
| `score.strength_score` (legacy composite component) | 45.0 |
| `useful_god_score` | 30.0 (changed vs old 51.25 total after G1-06 winner `sea_001`) |

Old PDF **51.25 / D+** must not be restored. `/result` Điểm thân card binds **0.87**, not 55.05. Report labels 55.05 as **Điểm tổng**.

---

## 14. Analysis-ID consistency

For run `bte-1987-1-21-4-30-1787197461334`:

```text
Analyze UI
  → ResultStore bte_last_result / bte_current_analysis_id
    → /result data-analysis-id
      → /reports BteFullReport.analysisId
        → Full Report footer “Mã phân tích”
          → print PDFs of those pages
```

Same ID on every surface. Client-generated `bte-…` id (ResultStore), not API `X-Request-ID`.

---

## 15. Remaining mismatches

| Item | Status |
|------|--------|
| Stale uvicorn 19 Aug 21:12 | **Fixed** (now PID 1380, 20 Aug 10:31) |
| Stale `static/dist` 14 Aug | **Fixed** |
| `/result` missing Điều hậu in PACK_07 body | **Fixed** by routing G1-04 labels onto S02 indicators (already on Full Report / s01 VM) |
| Jinja `/analyze` still has “unspecified” gender option | Unchanged; CASE-0001 used Nam. Not an engine issue. |
| Customer DOCX download | Still HTML download on `/reports`; no live DOCX path |
| Report V1 Playwright PDF | Still not the portal Xuất path |
| Portal/Admin processes from 19 Aug 21:12 | Still running; they only proxy/serve files. New API is PID 1380. |
| Product Owner Chrome tab | Must hard-refresh and **run Analyze again** so `bte_last_result` is this payload, not the 10:09 stale store |

Nothing in this list is “live API still Frozen-FAIL.”

---

## 16. Exact commands executed

```text
# Confirm stale listener
Get-NetTCPConnection -LocalPort 8000 -State Listen
Get-CimInstance Win32_Process -Filter "ProcessId=4548 OR ProcessId=4728"

# Stop only API uvicorn tree
Stop-Process -Id 4548 -Force
Stop-Process -Id 4728 -Force

# Start from current workspace .venv
cd C:\Users\MG\Documents\GitHub\BTE-Platform\BTE-Platform
.\.venv\Scripts\python.exe -m uvicorn applications.api.app:app --host 127.0.0.1 --port 8000 --log-level info

# Smoke (after health 200)
POST http://127.0.0.1:8081/backend/api/v1/analyze
  {year:1987,month:1,day:21,hour:4,minute:30,gender:"male",timezone:"Asia/Bangkok",
   full_name:"Nguyễn Tiến Sơn",birth_place:"Hà Tây, Việt Nam"}

# Frontend
cd applications\customer_portal
npm install --no-fund --no-audit
npm run build:result
# second build after S02 climate routing
npm run build:result

# Verify served asset
GET http://127.0.0.1:8081/static/dist/result.js
```

Playwright then filled `/analyze` (same fields), opened `/result` and `/reports`, printed PDFs under `release/gate_01/`.

---

## Runtime fingerprint (after repair)

### Backend

- PID listen: **1380** (parent 4680, wrapper 9824)
- cwd: `C:\Users\MG\Documents\GitHub\BTE-Platform\BTE-Platform`
- Python: `.venv\Scripts\python.exe`
- Start: 2026-08-20 10:31:38
- git HEAD: `113b473ac25d3df68dd69551eb5f5c65ab32b859`

### Frontend

- Build: Vite production 2026-08-20 10:43:02
- `result.js` SHA256 `8FB91898CADB53AEA4875760087CAD489D0838EA7367724189FA53C594291D91`
- `report.js` SHA256 `1E97B3168033ECFDC1CEC63B0B272A3EE0830FBC62037564CF7525835B16F265`
- Chunk `fullReportViewModel-Dl6gd0lq.js`

### CASE

- Analysis ID: `bte-1987-1-21-4-30-1787197461334`
- Request time: 2026-08-20 ~10:44 local

---

## Acceptance test — Frozen Truth table

| Marker | Expected | Live API | /result | Report | PDF (pre-PDF HTML) |
|---|---|---|---|---|---|
| Gender | Nam customer | PASS | PASS | PASS | PASS |
| Strength | 0.87 strong | PASS | PASS | PASS | PASS |
| Pattern | Chính Ấn | PASS | PASS | PASS | PASS |
| Climate | cold | PASS | PASS (Hàn) | PASS | PASS |
| Điều hậu | Cần ôn ấm | PASS | PASS | PASS | PASS |
| Five Elements | 4/5/6/3/1 | PASS | PASS | PASS | PASS |
| Useful God | Hỏa/Bính/Thất Sát | PASS | PASS | PASS | PASS |
| ShenSha | canonical | PASS | PASS | PASS | PASS |
| Luck | Ất Tỵ 2022–2031 | PASS | PASS | PASS | PASS |

PDF cells are pre-PDF HTML of the Chromium print path (extractable PDF text is empty, same as PO’s old Skia files).

---

## Files changed (this phase)

| File | Why |
|------|-----|
| *(process)* | Stopped PID 4548/4728; started PID 1380 |
| `applications/customer_portal/static/dist/*` | Vite rebuild |
| `applications/customer_portal/src/adapters/canonicalDesktopAdapter.ts` | Route G1-04 Hàn / Cần ôn ấm onto visible `/result` S02 indicators |
| `release/gate_01/G1_09_LIVE_RUNTIME_REPAIR_REPORT.md` | This report |
| `release/gate_01/G1_09_CASE0001_*.pdf` | New print artifacts |

**Did not change:** Ten Gods / Strength / Pattern / Temperature / Five Elements / Useful God / ShenSha / Luck engines, Golden, snapshots, G1-01…G1-08 tests.

---

## Product Owner next step

1. Hard refresh `http://127.0.0.1:8081/analyze` (Ctrl+F5).
2. Run CASE-0001 again (do not open History).
3. Confirm `/result` and Print → PDF.

Do not start G1-FINAL. Do not start Gate 2.

---

**G1-09 LIVE RUNTIME REPAIR: PASS**
