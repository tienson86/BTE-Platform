# BTE Integration Audit — Bazi Data Flow Verification

**Priority:** BLOCKER  
**Date:** 2026-07-27  
**Case:** 21/01/1987 04:30 Nam  
**Scope:** Data-flow only (no Can Chi / Calendar formula changes)

---

## Verdict

| Layer | Value | Status |
|-------|-------|--------|
| Expected | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần | Reference |
| Engine `BaziEngine.build()` | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần | MATCH |
| API `/api/v1/analyze` JSON | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần | MATCH |
| Portal UI (before fix) | Could show Đinh Mão / Tân Dần / Bính Thìn / Canh Dần | MISMATCH |
| Portal UI (after fix) | Re-fetches live analyze before render | MATCH path |

**Mismatch location (root cause):** Portal Result page rendered **cached browser storage JSON**, not a live Engine call.

Wrong year pillar `Đinh Mão` is exactly `GanzhiAlgorithm.year(1987)` — Gregorian 1987 **without** Lập Xuân. That is the **pre-rewrite** algorithm output, not the current facade.

---

## Full pipeline trace

```
Portal /analyze (vanilla JS — NOT React)
  applications/customer_portal/static/js/analyze.js  → readInput() / runAnalyze()
        ↓ POST /backend/api/v1/analyze
Portal proxy
  applications/customer_portal/app.py  → backend_proxy()  (~L99)
        ↓ httpx → BTE_API_BASE_URL (default http://127.0.0.1:8000)
Applications API
  applications/api/routes/v1.py  → analyze_endpoint()
  applications/api/routes/_helpers.py  → attach_presentation_metadata()
  applications/api/services/orchestrator.py  → OrchestratorService._run()
        ↓ calendar_engine.build(...)
        ↓ bazi_engine.build(calendar, gender=...)   ← engines/bazi_engine/engine.py
        ↓ _shape_bazi() → payload["bazi"]
JSON Response envelope { success, data: { calendar, bazi, ... } }
        ↓
analyze.js → BtePortal.saveLastResult({ input, data })
        ↓ sessionStorage + localStorage keys:
            bte_last_result / bte_history
            (legacy read still possible: bte_portal_last_result)
        ↓ redirect /result
result.js → ResultStore.loadForView()  ← USED TO RENDER CACHE ONLY
        ↓ presenters/bazi.js / calendar.js  (display only)
Final UI
```

There is **no React app** in this repo for the customer portal (`*.tsx` / `*.jsx` = 0). UI is FastAPI templates + static JS.

---

## Checklist answers

### 1. Does API really call `engines/bazi_engine/engine.py`?

**YES.**

- Import: `applications/api/services/orchestrator.py` L13  
- Instance: `OrchestratorService.__init__` → `self.bazi_engine = BaziEngine()` (~L231)  
- Call: `_run()` → `self.bazi_engine.build(calendar, gender=gender)` (~L503)  
- Live inspect: `inspect.getfile(BaziEngine)` → `...\engines\bazi_engine\engine.py`  
- Response fingerprint added: `data.bazi_source.contract = "li_chun_jdn_v1"`

### 2. Alternate / legacy / mock engines?

| Symbol | Exists? | On production Portal path? |
|--------|---------|----------------------------|
| `engines.bazi_engine.engine.BaziEngine` | YES — active | YES |
| `engines/bazi_engine/pillars/pillar_builder.py` (`PillarBuilder`) | YES — package leftover | NO (not imported by orchestrator) |
| `PillarService` / `pillar_service` | YES | NO |
| `BaziCalculator` | NO | — |
| `FakeEngine` / `MockEngine` / `sampleResult` / `demoData` | NO in portal JS | — |
| Legacy stack `api/services/pipeline_service.py` | YES, also imports same `BaziEngine` | Portal uses `applications.api`, not `api/` |
| Portal `ResultStore` browser cache | YES | **WAS the stale UI source** |

### 3. Project search highlights

| Term | Finding |
|------|---------|
| `Đinh Mão` / `Bính Thìn` | Database nạp âm / JDN tables only — not hardcoded UI chart |
| `Bính Dần` / `Tân Sửu` / `Canh Ngọ` / `Mậu Dần` | Regression tests + live Engine/API output |
| `toordinal` | `engines/calendar_engine/julian/julian.py` (current JDN helpers) |
| `build_pillars` | Not found as live API entry |
| `xem-tu-tru` | Not found |
| `BaziEngine` | All live imports point at `engines.bazi_engine.engine` |
| `sampleResult` / `mockResult` / `defaultData` / `demoData` | Not used by Portal Result render |

### 4. Response JSON vs UI

**Live API (TestClient POST `/api/v1/analyze`):**

```text
year_pillar  Bính Dần
month_pillar Tân Sửu
day_pillar   Canh Ngọ
hour_pillar  Mậu Dần
calendar.*_can_chi  same four pillars
```

If UI still showed `Đinh Mão…`, **API was not the source of that paint** — cached `bte_last_result` / `bte_portal_last_result` / history view was.

### 5–6. Cache / React defaults

- Portal persists analyze payloads in **sessionStorage + localStorage** (`result_store.js`).  
- Result page previously **never re-called** the API; it only painted stored JSON.  
- No React `sampleResult` / `mockResult` / `defaultData`.  
- Legacy key `bte_portal_last_result` remained readable → old sessions could keep wrong pillars forever.

---

## Mismatch report (exact)

| Field | Value |
|-------|-------|
| Current UI Value (stale) | Đinh Mão / Tân Dần / Bính Thìn / Canh Dần |
| API Value (live) | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần |
| Engine Value (live) | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần |
| Expected Value | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần |
| Mismatch Location | Portal presentation of **cached** analyze payload |
| Exact File | `applications/customer_portal/static/js/result.js` |
| Exact Function | `boot()` (pre-fix: render `ResultStore.loadForView()` without refresh) |
| Exact Line (pre-fix) | ~L49–L110: load storage → `show(stage)` with `data[stage]` |
| Contributing File | `applications/customer_portal/static/js/result_store.js` |
| Contributing Function | `load()` / `loadForView()` reading `bte_last_result` + legacy `bte_portal_last_result` |
| Why wrong pillars | Cached output of old year rule: solar year 1987 → `Đinh Mão` |

---

## Fix applied (data-flow only)

1. **`result.js`** — before render, always `POST /api/v1/analyze` with stored birth `input`; refuse to paint cached engine JSON if refresh fails.  
2. **`result_store.js`** — purge legacy last-result key on `save()`; expose `peekView()` so refresh updates the correct slot.  
3. **`orchestrator.py`** — attach `bazi_source` fingerprint proving which facade built the chart.

**Not changed:** Can Chi formulas, Calendar Engine algorithms, Golden Dataset.

---

## Operator checklist

1. Restart API: `uvicorn applications.api.app:app --port 8000`  
2. Restart Portal: `uvicorn applications.customer_portal.app:app --port 8081`  
3. Hard-refresh browser (Ctrl+F5) so new `result.js` loads.  
4. Open `/result` (or re-run Analyze for 21/01/1987 04:30 Nam).  
5. Confirm Bát Tự + Lịch Việt Can Chi = Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần.  
6. Optional: DevTools → Application → clear `bte_*` keys once.

Ensure Portal `BTE_API_BASE_URL` points at the **current** Applications API, not an old process.
