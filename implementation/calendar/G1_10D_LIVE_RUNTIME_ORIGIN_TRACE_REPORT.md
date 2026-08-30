# G1-10D — Live origin / ResultStore / DOM trace

## 1. STATUS

**PASS** on `http://localhost:8081/result` after restarting the stale API process.

Live TỨ TRỤ Cung Phi:

```
Năm    BÍNH NGỌ   ĐOÀI
Tháng  ĐINH DẬU   ĐOÀI
Ngày   BÍNH TUẤT  CHẤN
Giờ    CANH DẦN   CẤN
```

Screenshot: `implementation/calendar/G1_10D_localhost_result_tutru.png`

Tam Nguyên periods, 60 Hoa Giáp data, personal Cung Phi formula, and Can Chi algorithms were not changed.

## 2. localhost origin state

Playwright Chromium at `http://localhost:8081` started empty (isolated profile).

After NEW Analyze 24/09/1966 04:15 male Hà Nội:

- `bte_last_result` written with `calendar_rule_version = G1-10C`
- Year Cung = Đoài (identity and BaZi)
- Month Cung = Đoài
- `bte_current_analysis_id` = `debc25e9-dbc2-4333-a32f-0bdf8b036128`

The Product Owner’s existing Chrome profile on this origin previously stored the **stale HTTP** payload (Khảm/Khảm, no `calendar_rule_version`). That payload was not dropped by the G1-10B gate (`missing version && missing routing` → treated as compatible). That gate is now tightened.

## 3. 127.0.0.1 origin state

`http://127.0.0.1:8081` is a **different origin**. Playwright’s 127.0.0.1 store was empty.

Both origins were previously able to keep independent `bte_last_result` copies. The live failure the Product Owner saw was not “wrong origin vs right origin”; **both** would save Khảm because the **API process** returned Khảm.

## 4. Process serving port 8081

**Before restart (stale):**

| Port | PID | Command | CWD |
| --- | --- | --- | --- |
| 8000 | 10952 | `.venv\Scripts\python.exe -m uvicorn applications.api.app:app --host 127.0.0.1 --port 8000` | current repo |
| 8081 | 1752 | `.venv\Scripts\python.exe -m uvicorn applications.customer_portal.app:app --host 127.0.0.1 --port 8081` | current repo |

Uvicorn was **not** `--reload`. Imported engines were the pre-G1-10A/B/C snapshot even though the working directory was this repository.

**After restart (current source):**

| Port | PID | Module |
| --- | --- | --- |
| 8000 | 1140 | `applications.api.app:app` |
| 8081 | 12200 | `applications.customer_portal.app:app` |

Host bind remains `127.0.0.1` (Windows still serves `http://localhost:8081`). Canonical **browser** origin for development is `http://localhost:8081`. Analyze uses a relative `/result` redirect, so it does not hop origins.

## 5. Bundle actually served

`/result` HTML loads:

- `/static/js/result_store.js?v=G1-10C`
- `/static/dist/result.js?v=G1-10C`

Filesystem `result.js` Last-Modified: 30 Aug 2026 04:30 UTC (G1-10C rebuild), then rebuilt again after the version-gate change.

Query `?v=G1-10C` prevents the browser from keeping an unversioned cached `result.js`.

## 6. Analyze HTTP Year/Month Cung

**Before restart** (`POST http://127.0.0.1:8081/backend/api/v1/analyze` and direct `:8000`):

```
calendar_rule_version = None
tam_nguyen = None
ganzhi_routing = None
year ident=Bính Ngọ/Khảm  bazi.cung_phi=None
month ident=Đinh Dậu/Khảm bazi.cung_phi=None
calendar.cung_phi (personal) = Đoài
```

**After restart:**

```
calendar_rule_version = G1-10C
tam_nguyen = Trung Nguyên
year ident=Đoài  bazi.cung_phi=Đoài  source_nguyen=Trung Nguyên
month ident=Đoài bazi.cung_phi=Đoài source_nguyen=Trung Nguyên
day ident=Chấn   bazi.cung_phi=Chấn  source_nguyen=Hạ Nguyên
hour ident=Cấn   bazi.cung_phi=Cấn   source_nguyen=Hạ Nguyên
```

## 7. ResultStore saved Year/Month Cung

After live Analyze on localhost:

```
year  ident=Đoài bazi=Đoài ver=G1-10C
month ident=Đoài bazi=Đoài ver=G1-10C
```

## 8. ResultStore loaded Year/Month Cung

Same object `loadCurrent()` used by `/result`. Loaded Cung = Đoài / Đoài.

## 9. Adapter Year/Month Cung

`adaptIdentityHeader` / `bindPillarCung`:

```
bazi.*_pillar.cung_phi
  → calendar.ganzhi_routing.*.cung_phi
  → identity ONLY if calendar_rule_version is not G1-10*
```

For G1-10C: Year=Đoài, Month=Đoài. Legacy identity fallback does not run.

## 10. Component Year/Month Cung

`FourPillars` → `TuTruPanel` props `year.cungPhi` / `month.cungPhi` = Đoài / Đoài.

## 11. DOM Year/Month Cung

`http://localhost:8081/result` `[data-testid=tu-tru-panel]`:

```
year:  Năm BÍNH NGỌ THỦY ĐOÀI
month: Tháng ĐINH DẬU HỎA ĐOÀI
day:   Ngày BÍNH TUẤT THỔ CHẤN
hour:  Giờ CANH DẦN MỘC CẤN
```

## 12. Exact source of previous KHẢM/KHẢM

```
FILE:       engines/date_selection/data/ha_nguyen_cung.csv
ROWS:       Bính Ngọ → Khảm ; Đinh Dậu → Khảm
FUNCTION:   pillar_contract(ganzhi) without tam_nguyen
            → trach_for_date_ganzhi → cung_for_date_ganzhi
PUBLISHED:  identity.four_pillars.year.cung_phi
            identity.four_pillars.month.cung_phi
SERVED BY:  stale uvicorn PID 10952 (no reload)
UI PATH:    adaptIdentityHeader bindPillar
            cungPhi: firstText(cell.cung_phi)   // pre-G1-10C bundle
            cell = identity.four_pillars.year|month
VALUE:      Khảm / Khảm
```

Personal `calendar.cung_phi` was already Đoài (1966 male digit-sum). The header did **not** use that field. It used Hạ Nguyên date-table palaces on identity cells.

## 13. Root cause classification A/B/C/D

**CASE A — HTTP RESPONSE IS WRONG** (proven before restart).

```
YEAR
HTTP:        Khảm
ResultStore: Khảm (copy of HTTP)
Adapter:     Khảm
Component:   Khảm
DOM:         Khảm
ROOT CAUSE:  live API process never loaded G1-10A/B/C; identity used Hạ Nguyên table
```

After restart the chain is Đoài at every step. Not B/C/D.

## 14. Fix applied

1. Stopped stale PID 10952 / 1752. Confirmed 8081 free. Started current API + portal from this repository.
2. Cache-bust `result.js` and `result_store.js` with `?v=G1-10C`.
3. G1-10C adapter: never use identity Cung when `calendar_rule_version` is G1-10*.
4. ResultStore: any current result **without** `calendar_rule_version === G1-10C` is dropped (covers unversioned Khảm payloads).

No Tam Nguyên / Ganzhi algorithm edits.

## 15. Cache/origin normalization

- Development browser URL: **`http://localhost:8081`**
- Analyze `window.location.assign("/result")` stays on the same origin
- Do not mix `localhost` and `127.0.0.1` in one session
- Unversioned `bte_last_result` is no longer treated as current

## 16. 1966 live verification

Sequence executed:

1. Kill 8000/8081
2. Start current uvicorn processes
3. Open `http://localhost:8081`
4. Clear current-result keys in the verification browser
5. Analyze 24/09/1966 04:15 male Hà Nội
6. Capture Analyze HTTP (Đoài/Đoài, G1-10C)
7. Open `/result`
8. Inspect `bte_last_result` (Đoài/Đoài)
9. Inspect TuTruPanel DOM (Đoài/Đoài)
10. Screenshot

**PASS.**

Re-analyze once in the Product Owner Chrome profile so that origin’s old unversioned store is replaced (or discarded by the new gate).

## 17. Homepage live verification

`#dsTuTru` after live `POST /backend/api/v1/date-selection/day` for 1966-09-24:

```
year Đoài / month Đoài / day Chấn / hour Cấn
DOM: Năm BÍNH NGỌ … ĐOÀI ; Tháng ĐINH DẬU … ĐOÀI
```

Screenshot: `implementation/calendar/G1_10D_localhost_homepage_tutru.png`

## 18. Screenshot evidence

- `implementation/calendar/G1_10D_localhost_result_tutru.png`
- `implementation/calendar/G1_10D_localhost_result_full.png`
- `implementation/calendar/G1_10D_localhost_homepage_tutru.png`

## 19. Tests

Live DOM is the acceptance gate. Module traces:

- Pre-restart HTTP dump: Khảm (CASE A)
- Post-restart HTTP + Playwright DOM: Đoài

No Tam Nguyên algorithm tests were altered.

## 20. Files changed

| File | Role |
| --- | --- |
| `applications/customer_portal/templates/result_desktop.html` | `?v=G1-10C` on result JS |
| `applications/customer_portal/templates/_layout.html` | `?v=G1-10C` on ResultStore |
| `applications/customer_portal/src/screens/commercial_dashboard/adapter.ts` | No G1-10* identity Cung fallback |
| `applications/customer_portal/static/js/result_store.js` | Drop unversioned current results |
| `applications/customer_portal/src/resultState/currentResult.ts` | Same gate |
| `applications/customer_portal/static/dist/result.js` | Rebuilt |

G1-10D stops here.
