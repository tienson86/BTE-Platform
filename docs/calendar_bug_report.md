# Calendar Engine Bug Report — Lunar = Solar

**Date:** 2026-07-26  
**Severity:** Critical (user-facing incorrect birth calendar)  
**Status:** Root cause identified and fixed at data source

---

## 1. Bug location

**Primary source:** `engines/calendar_engine/engine.py` — `CalendarEngine.build()`

**Not caused by:**

- Orchestrator field overwrite (`applications/api/services/orchestrator.py`)
- Portal presenter mis-binding (`calendar.js` / `chart_info.js`) as primary cause
- Hard-coded solar→lunar mapping in Portal

**Symptom path:**

```text
CalendarEngine.build()
        │  (bug: LunarDate(year, month, day) = solar Y/M/D)
        ▼
orchestrator → payload["calendar"] = to_jsonable(calendar)
        │  (copies engine output as-is — correct)
        ▼
Portal calendar.js formatLunar(cal)
        │  (displays lunar.year/month/day)
        ▼
UI: Ngày âm == Ngày dương  (e.g. 21/01/1987)
```

---

## 2. Root cause

`CalendarEngine.build()` previously constructed lunar date by **copying solar year/month/day**:

```python
# BUG (historical)
LunarDate(year, month, day)  # same values as SolarDate
```

There was **no solar→lunar conversion**.  
Stub processors (`processor/lunar_converter.py`, unfinished `algorithms/jdn_to_lunar.py`) were not wired into the public `build()` API.

Therefore API JSON had:

```json
"solar": { "year": 1987, "month": 1, "day": 21 },
"lunar": { "year": 1987, "month": 1, "day": 21, "leap": false }
```

Portal correctly rendered whatever the engine returned — so Ngày âm looked identical to Ngày dương.

---

## 3. Impact

| Layer | Effect |
|-------|--------|
| Calendar Engine | Wrong lunar Y/M/D |
| API `/api/v1/analyze` | `data.calendar.lunar*` incorrect |
| Portal Result → Lịch Việt | Ngày âm = Ngày dương |
| Feng Shui Cung Phi | Uses lunar year when present — would use wrong year if lunar.year == solar.year (e.g. late-year dates near Tết boundary are especially wrong) |
| Report / Executive (lunar fields) | Same wrong values |

Does **not** change Bazi pillar logic that keys off solar datetime / solar terms (Bazi does not use this lunar stub for month commander).

---

## 4. Files changed (fix)

| File | Change |
|------|--------|
| `engines/calendar_engine/lunar/converter.py` | Hồ Ngọc Đức solar→lunar conversion (UTC+7) |
| `engines/calendar_engine/engine.py` | Call converter; expose flat `lunar_*`, `leap_month`, `solar_date`, `lunar_date` |
| `engines/calendar_engine/lunar/lunar.py` | Optional `year_can_chi` + `to_dict()` |
| `engines/calendar_engine/algorithms/jdn_to_lunar.py` | Delegate to converter |
| `applications/customer_portal/static/js/presenters/calendar.js` | VN format; bind `lunar_date` / lunar fields (display only) |
| `applications/customer_portal/static/js/presenters/chart_info.js` | Same binding/format |
| `applications/customer_portal/static/js/presenters/summary_builder.js` | Same binding/format |
| `tests/calendar/test_lunar_conversion.py` | Unit/conversion tests |
| `tests/calendar/test_lunar_regression.py` | Regression set (1987 / 1990 / 2000 / 2026) |

**Not changed for this bug:** Portal layout; no hard-coded lunar dates; no copying `solar_date` → `lunar_date` in presenters.

---

## 5. Verification (pipeline investigation 2026-07-26)

### 5.1 Calendar Engine output — `1987-01-21 04:30` Asia/Ho_Chi_Minh

| Field | Value |
|-------|--------|
| Solar | 1987-01-21 |
| Lunar Year / Month / Day | 1986 / 12 / 22 |
| Leap Month | false |
| Can Chi (năm âm) | Bính Dần |
| Tiết khí (engine approx.) | Vũ Thủy |
| `solar_date` | `21/01/1987` |
| `lunar_date` | `22/12/Bính Dần` |

### 5.2 API / Orchestrator

`payload["calendar"]` is a direct `to_jsonable(calendar)` — no overwrite of lunar fields.

Example excerpt:

```json
{
  "solar_date": "21/01/1987",
  "lunar_date": "22/12/Bính Dần",
  "lunar_year": 1986,
  "lunar_month": 12,
  "lunar_day": 22,
  "leap_month": false,
  "solar": { "year": 1987, "month": 1, "day": 21 },
  "lunar": {
    "year": 1986,
    "month": 12,
    "day": 22,
    "leap": false,
    "year_can_chi": "Bính Dần"
  }
}
```

### 5.3 Portal JSON / presenter

- If Network → Analyze shows lunar = solar → engine/API bug (historical).
- If Network shows lunar ≠ solar but UI still equal → presenter bug.
- **Current code:** JSON correct; `calendar.js` prefers `cal.lunar_date`, else `cal.lunar.*`.

**Note:** Result page reads `BtePortal.getLastResult()` (local storage). After deploying the engine fix, user must **re-run Analyze**; old cached payloads still contain the buggy lunar copy.

---

## 6. Fix summary

1. Implement real solar→lunar conversion (`lunar/converter.py`).
2. Wire conversion into `CalendarEngine.build()`.
3. Expose explicit API fields: `solar_date`, `lunar_date`, `lunar_year`, `lunar_month`, `lunar_day`, `leap_month`.
4. Keep Portal as display-only binding to those fields.

---

## 7. Tests executed

```bash
pytest tests/calendar -q
```

Includes:

- `test_lunar_conversion.py` — known cases (1987-01-21, Tết 2024, leap 2020, year edges)
- `test_lunar_regression.py` — prints Solar → Lunar for:
  - 1987-01-21
  - 1990-05-15
  - 2000-02-05
  - 2026-07-26

Regression expectations (UTC+7):

| Solar | Lunar |
|-------|--------|
| 21/01/1987 04:30 | 22/12/1986 (Bính Dần) |
| 15/05/1990 10:00 | 21/04/1990 (Canh Ngọ) |
| 05/02/2000 08:00 | 01/01/2000 (Canh Thìn) |
| 26/07/2026 12:00 | 13/06/2026 (Bính Ngọ) |

---

## 8. Conclusion

| Question | Answer |
|----------|--------|
| Where is the bug? | `CalendarEngine.build()` (historical stub) |
| Why? | Lunar was assigned solar Y/M/D — no conversion |
| Orchestrator wrong? | No — forwarded engine output correctly |
| Portal wrong? | No primary cause — displayed bad engine data |
| Fix? | Convert via Hồ Ngọc Đức algorithm at engine source |

**Do not** “fix” by assigning `lunar_date = solar_date` or hard-coding Portal labels.
