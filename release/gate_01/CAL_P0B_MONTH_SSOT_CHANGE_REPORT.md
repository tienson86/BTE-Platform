# CAL-P0B — Month Pillar SSOT Change

| Field | Value |
|-------|-------|
| **Gate** | CAL-P0B |
| **Date** | 2026-08-20 |
| **Standard** | `BTE-MONTH-PILLAR-LUNAR-V1.0` |
| **Product Owner** | Final V1.0 override — lunar-month Four Pillars month |
| **Golden Dataset** | **not** bulk-migrated |

---

## 1. Decision

The DESIGN_LOCKED sentence:

> Tháng Tử Bình không dùng tháng âm lịch. Dùng tiết khí.

is **UNFROZEN and SUPERSEDED** for Four Pillars month construction.

New SSOT:

1. Gregorian birth → canonical lunar date (`CalendarEngine` / `solar_to_lunar`).
2. Lunar month number → month branch (tháng 1=Dần … 12=Sửu). Leap months keep the same number, therefore the same branch.
3. Month stem = existing Ngũ Hổ Độn (`year stem` + lunar month index). Year stem still changes at **Lập Xuân**.
4. `SolarTermEngine` is **kept**. `get_bazi_month()` is **not** used to build the Four Pillars month.
5. Solar terms still serve season / climate / Điều hậu / Luck **jie timing**.

---

## 2. Implementation

| Item | Location |
|------|----------|
| Canonical mapper | `engines/calendar_engine/month_pillar.py` (`lunar_month_to_branch`, `MONTH_PILLAR_STANDARD`) |
| Four Pillars construction | `engines/bazi_engine/engine.py` — lunar month + `_month_stem`; prefers `CalendarResult.lunar_month` when the calendar object is passed |
| Solar-term month (subsystem) | `SolarTermEngine.get_bazi_month` remains; docstring states it is **not** Four Pillars |
| Luck 流月 / start-age jie | still `get_bazi_month` / 12 Tiết (timing contract unchanged) |
| Algorithm doc | `database/01_du_lieu_goc/09_calendar/00_cau_hinh/03_thuat_toan.md` §6 |
| Workflow doc | `engines/calendar_engine/thuat_toan.md` bước 06–07 |

Portal does not calculate month. It binds `data.bazi.month_pillar`.

No Strength weights or class thresholds were changed.

---

## 3. Why Hưng was Bính Thân and is now Đinh Dậu

| Step | 12 Tiết (old) | Lunar month (new) |
|------|----------------|-------------------|
| Lunar date | 01/08/1981 (already correct) | 01/08/1981 |
| Month index | 7 (Lập Thu → Bạch Lộ) | **8** |
| Branch | Thân | **Dậu** |
| Year stem Tân → Ngũ Hổ Độn | Canh + 6 = **Bính** | Canh + 7 = **Đinh** |
| Pillar | Bính Thân | **Đinh Dậu** |

Year / Day / Hour unchanged: Tân Dậu / Kỷ Mão / Bính Dần.

---

## 4. Four-case regression

| Case | Solar | Lunar | Old month | New month | Full Four Pillars | Status |
|------|-------|-------|-----------|-----------|-------------------|--------|
| Nguyễn Tiến Sơn | 21/01/1987 | 22/12/1986 | Tân Sửu | Tân Sửu | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần | PASS |
| Lương Ngọc Huỳnh | 24/09/1966 | 10/08/1966 | Đinh Dậu | Đinh Dậu | Bính Ngọ / Đinh Dậu / Bính Tuất / Canh Dần | PASS |
| Đặng Thị Dung | 22/05/1982 | 29/04/1982 | Ất Tỵ | Ất Tỵ | Nhâm Tuất / Ất Tỵ / Ất Tỵ / Tân Tỵ | PASS |
| Đoàn Quang Hưng | 29/08/1981 | 01/08/1981 | Bính Thân | **Đinh Dậu** | Tân Dậu / Đinh Dậu / Kỷ Mão / Bính Dần | PASS |

---

## 5. Đoàn Quang Hưng downstream (do not force weak)

Strength engine ran on the corrected chart. No threshold/weight retune.

| Layer | Before (Bính Thân) | After (Đinh Dậu) |
|-------|--------------------|------------------|
| Four Pillars | Tân Dậu / Bính Thân / Kỷ Mão / Bính Dần | Tân Dậu / **Đinh Dậu** / Kỷ Mão / Bính Dần |
| Month Ten God vs Kỷ (G1-01) | Chính Ấn (Bính) | **Thiên Ấn** (Đinh) |
| Visible Ten Gods | Thực Thần · Chính Ấn · Nhật Chủ · Chính Ấn | Thực Thần · **Thiên Ấn** · Nhật Chủ · Chính Ấn |
| Strength | **0.71 / strong** (raw 21, Thân vượng) | **0.61 / balanced** (raw 11, Trung hòa) |
| Strength evidence | Hưu +10 · căn 2 chi +22 · Ấn +10/+5 · tiết −8/−8/−10 | Hưu +10 · căn 1 chi +12 · Ấn +10/+5 · tiết −8/−8/−10 |
| Pattern | `thuong_quan_phoi_an` / Thương Quan phối Ấn (Thân · Canh = Thương Quan) | `thuc_than` / **Thực Thần** (Dậu · Tân = Thực Thần, `pat_tht_01`) |
| Temperature | cool / **Lương** / Cần ôn ấm · month Thân · autumn | cool / **Lương** / Cần ôn ấm · month **Dậu** · autumn (`cli_004`) |
| Five Elements | Mộc4 · Hỏa3 · Thổ3 · Kim5 · Thủy1 | Mộc4 · Hỏa3 · **Thổ2** · Kim5 · **Thủy0** |
| Useful God | Hỏa · Đinh · Thiên Ấn (`sea_004`) | **Hỏa · Đinh · Thiên Ấn** (`sea_004`) — still wins |
| ShenSha | (live names not frozen in CAL-P0) | Văn Xương · Thiên Đức Quý Nhân |
| Luck | reverse from **Bính Thân** → first **Ất Mùi** (age 7); then current Nhâm Thìn | reverse from **Đinh Dậu** → first **Bính Thân** (age 7); current **Quý Tỵ**. Jie start-age still 7 (Lập Thu timing unchanged) |
| Score (composite, not Điểm thân) | not used as freeze | total **53.95** grade **D+** |
| Calendar `bazi_can_chi.month` | Bính Thân | **Đinh Dậu** |

**0.71 strong → 0.61 balanced.** Not weak. Root dropped 2-chi (+22) to 1-chi (+12) because Thân’s Canh Kim root is gone; Dậu still supplies Tân Kim.

Customer-facing climate label is still internal `cool` → **Lương** (presentation localization to **Khí mát** was not part of this SSOT patch).

---

## 6. 22 Golden conflicts

See `release/gate_01/CAL_P0B_22_CASE_REVIEW.md`.

Expected Golden outputs were **not** rewritten. Product Owner reviews the new lunar-month pillars against *Can Chi Thông Luận*.

---

## 7. Tests

| Suite | Result |
|-------|--------|
| `pytest tests/bazi -q` | **45 passed** (6 subtests) |
| New | `tests/bazi/test_cal_p0b_lunar_month_pillar.py` |
| `pytest tests/calendar -q` | included in combined run — passed |
| `pytest tests/strength -q` | **1 failed** (see below) |

`tests/bazi/test_bazi_calendar_regression.py`: one historical row `2000-02-04` expected month **Mậu Dần** (12 Tiết / Lập Xuân day). Lunar is `29/12/1999` → **Kỷ Sửu**. Expected month updated to the new SSOT. Lunar tuple was already month 12.

**Remaining failure (not skipped):**

`tests/strength/test_g1_02r_strength_correctness.py::test_weak_fixture_ex002_profile`

Birth `1960-07-01 12:00` lunar `08/06/1960`:

- Old 12 Tiết month: **Ngọ** → Strength `month_status=Tử`
- New lunar month: **Quý Mùi** → `month_status=Tướng`

The fixture is no longer a 12-Tiết “Tử / weak” profile. Strength weights were not changed. Test was not rewritten (user: do not modify tests unless requested; this fixture was not a requested four-case). Product Owner may replace the weak fixture later.

---

## 8. Live `/analyze`

API restarted from this repo (`127.0.0.1:8000`). Fresh `POST /api/v1/analyze`, not `bte_last_result`.

| Case | Lunar | Live Four Pillars | Strength |
|------|-------|-------------------|----------|
| Đoàn Quang Hưng | 01/08/1981 | **Tân Dậu / Đinh Dậu / Kỷ Mão / Bính Dần** | 0.61 balanced |
| Nguyễn Tiến Sơn | 22/12/1986 | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần | 0.87 strong |
| Lương Ngọc Huỳnh | 10/08/1966 | Bính Ngọ / Đinh Dậu / Bính Tuất / Canh Dần | 0.64 balanced |
| Đặng Thị Dung | 29/04/1982 | Nhâm Tuất / Ất Tỵ / Ất Tỵ / Tân Tỵ | 0.24 weak |

Portal rebuild not required (no independent month calculation).

---

## Completion

**CAL-P0B MONTH SSOT CHANGED — 22 CASES AWAIT PRODUCT OWNER REVIEW**
