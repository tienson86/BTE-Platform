# BTE User Flow Audit — Analyze → Result

**Priority:** BLOCKER  
**Date:** 2026-07-27  
**Scope:** Portal workflow only (no Engine / Calendar formula changes)

---

## Broken step (root cause)

```
Analyze Button
  ↓ POST /backend/api/v1/analyze   ✅ works
  ↓ Response { success, data }     ✅ ~12KB, pillars correct
  ↓ ResultStore.save(bte_last_result) ✅
  ↓ Navigate /result               ✅
  ↓ Result boot loadForView()      ✅ had data
  ↓ *** FORCED re-POST /api/v1/analyze ***   ❌ FAIL (proxy/auth/API)
  ↓ catch → paint result.empty     ❌ DATA LOST ON SCREEN
```

The previous “cache fix” made `/result` **always re-analyze**. When that second call failed, UI showed:

> Chưa có kết quả — hãy chọn Luận giải trước.

even though `bte_last_result` still held the successful Analyze payload.

**Exact files**
- Break introduced in: `applications/customer_portal/static/js/result.js` → `refreshLiveResult()` / `boot()` catch
- Store keys: `bte_last_result` (sessionStorage + localStorage)

---

## Correct workflow (restored)

```
Input Form (analyze.js readInput)
  ↓ Click "Luận giải"
  ↓ POST /backend/api/v1/analyze  (api.js → portal proxy → Applications API)
  ↓ Response.data = { calendar, bazi, … }
  ↓ ResultStore.save → key bte_last_result (+ history best-effort)
  ↓ verify ResultStore.load() has data
  ↓ location.assign("/result")
  ↓ result.js boot → ResultStore.loadForView()
  ↓ render presenters (NO second POST)
```

Checklist:

| # | Check | Result |
|---|--------|--------|
| 1 | Click calls POST `/api/v1/analyze` | YES (`analyze.js` L81) |
| 2 | API JSON | Live TestClient 200; pillars Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần |
| 3 | Storage | `ResultStore` → sessionStorage + localStorage `bte_last_result` (not cookie/DB) |
| 4 | Result reads | `ResultStore.loadForView()` → VIEW key or LAST key |
| 5 | Empty cause | Forced re-POST failure discarded on-screen store data |
| 6 | No auto POST on `/result` | Restored — render store only |
| 7 | Result ID / GET Result | Not used; client-side store only |

---

## Fixes

1. **`result.js`** — remove mandatory re-POST; render stored Analyze payload immediately.  
2. **`analyze.js`** — require `saveLastResult` success + `load()` verify before navigate.  
3. **`result_store.js`** — `save()` returns false if Web Storage write failed; history is best-effort.

---

## Proof

- Analyze payload size ~11.7KB (not quota).  
- Node store simulation: `save` → `loadForView` returns same four pillars.  
- Portal tests: `applications/customer_portal/tests` → 18 passed.  
- `result.js` contains no `/api/v1/analyze` call.
