# G1-08 — Luck / Đại vận Repair Report

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-08 Phase 2 |
| **Date** | 2026-08-20 |
| **Product decision** | **Option A** — V1.0 year-level precision. No exact giao vận datetime. |
| **Canonical production** | `LuckEngine` + `DefaultDayunProvider` → `shape_luck_payload` |
| **Status** | FINAL FREEZE READY |

No Calendar formula change. No BaZi pillar change. No Strength / Temperature / Pattern / Useful God / ShenSha change. No Deep Luck interpretation (cát/hung, tài vận, Dụng/Hỷ/Kỵ). Exact datetime moved to **LUCK-PRECISION-V1.1**.

---

## 1. Product Owner precision decision

V1.0 locks **year-level** semantics:

- 12 Tiết calendar **dates** (not timestamps);
- birth hour/minute unused for khởi vận;
- `start_age = max(1, round(days / 3))` integer;
- current cycle by `current_year - birth_year` (not birthday, not giao vận datetime);
- `start_date` remains empty.

Option B (exact solar-term timestamps and giao vận datetime) is **not** implemented.

---

## 2. Canonical direction formula

Locked in `dayun_forward`:

```text
is_male(gender) == is_yang(year_stem)  →  Thuận / forward
otherwise                             →  Nghịch / reverse
```

| Group | Result |
|-------|--------|
| Dương Nam | Thuận |
| Âm Nữ | Thuận |
| Âm Nam | Nghịch |
| Dương Nữ | Nghịch |

Polarity = Niên can via `STEM_META`. Nhật can is not used.

---

## 3. Jie method

Start age uses **12 month-start Tiết** (`SolarTermEngine._MONTH_START_TERM_INDEX`). Trung khí is not used.

- Thuận → nearest later Jie (`term_date > birth_date`)
- Nghịch → nearest earlier Jie (`term_date < birth_date`)
- Birth **on** a Jie civil day: that Jie is skipped (V1.0 has no hour-level order)

CASE-0001: Lập Xuân **1987-02-04**, 14 calendar days.

---

## 4. Start-age formula

Unchanged:

```text
start_age = max(1, int(round(days / 3.0)))
```

CASE-0001: `round(14 / 3) = 5`.

---

## 5. CASE-0001 complete trace

Input: Nam, 1987-01-21 04:30, Asia/Bangkok.

| Step | Result |
|------|--------|
| Niên can | Bính = Dương |
| Direction | Nam + Dương → **Thuận** |
| Jie | Lập Xuân 1987-02-04 |
| Delta | 14 calendar days (04:30 unused) |
| Start age | **5** |
| Month pillar | Tân Sửu |
| First cycle | **Nhâm Dần** 1992–2001 ages 5–14 |
| Current (year-age 39 in 2026) | **Ất Tỵ · 2022–2031 · 35–44** |

---

## 6. Full cycle sequence

| i | GanZhi | Years | Ages |
|---|--------|-------|------|
| 0 | Nhâm Dần | 1992–2001 | 5–14 |
| 1 | Quý Mão | 2002–2011 | 15–24 |
| 2 | Giáp Thìn | 2012–2021 | 25–34 |
| 3 | Ất Tỵ | 2022–2031 | 35–44 |
| 4 | Bính Ngọ | 2032–2041 | 45–54 |
| 5 | Đinh Mùi | 2042–2051 | 55–64 |
| 6 | Mậu Thân | 2052–2061 | 65–74 |
| 7 | Kỷ Dậu | 2062–2071 | 75–84 |
| 8 | Canh Tuất | 2072–2081 | 85–94 |
| 9 | Tân Hợi | 2082–2091 | 95–104 |

Engine = API = Golden sequence. Renderers copy these fields.

---

## 7. Gender validation repair

Audit: `extract_birth_parts` used `gender or "male"`.

Now: `normalize_luck_gender` accepts API/Feng Shui aliases (`male`/`nam`/`m`/`1`, `female`/`nữ`/`nu`/`f`, …). Missing or invalid raises `LuckContextError` (`gender_required` / `unsupported_gender`). `LuckEngine.build` does not swallow that error into a male default; Dayun is omitted and `reason` is published.

**Addendum (presentation + Analyze gate):**

- Internal contract stays `male` / `female`.
- Customer-facing display is **Nam** / **Nữ** (`gender_display_label` / Portal `genderDisplay`).
- `POST /analyze` and any stage at/after Luck call `require_canonical_gender` → `ValidationAPIError` 422. Missing/invalid gender never defaults to male and never computes Đại vận as Nam.
- Portal Birth Input requires Nam/Nữ; `draftToAnalyzeRequest` returns null without canonical gender.

CASE-0001: internal `male`; customer **Giới tính: Nam**; luck **Nam + Bính Dương → Thuận**.

BaZi still stores `gender=None` without failing calendar-only stages.

---

## 8. Same-Jie-day semantics

V1.0 cannot know before/after on the same civil day. Implementation: equality is neither `<` nor `>`. Metadata `same_day_jie_skipped` records the skipped Jie. Forward then uses the next later Jie; reverse the previous earlier Jie. Tested for Lập Xuân 1987-02-04.

---

## 9. Report warning repair

`FULL_LUCK_CYCLES_GAP_NOTE` is emitted **only** when `luck.cycles` is empty. When cycles exist, Report/HTML/PDF/DOCX render the table plus:

- Đại vận hiện tại (canonical `current_cycle`)
- Chiều vận
- Tuổi khởi vận
- Căn cứ
- Phương pháp V1.0

No “cycles not provided” lie. No exact giao vận date claimed (`start_date` still unused).

Can/Chi elements: `Ất · Mộc` / `Tỵ · Hỏa` from `STEM_META` / `BRANCH_META` (Vietnamese projection of G1-05 `BRANCH_ELEMENT`).

---

## 10. Cross-surface verification

| Surface | Sequence | Start age | Direction | Current |
|---------|----------|-----------|-----------|---------|
| Engine | 10 cycles | 5 | forward / Thuận | Ất Tỵ 2022–2031 (year-age) |
| Orchestrator / API | copy | copy | copy + `direction_label` | `current_cycle` |
| Golden | same cycles | 5 | forward | not snapshotted (year-dependent; stripped in normalize) |
| Report / PDF / DOCX | copy | 5 | Thuận | copy of API current |
| Portal S01 | copy | separate “Tuổi khởi vận” row | “Chiều vận” | `formatLuckCurrent(data.luck.current_cycle)` |

Portal does not recompute `currentYear >= startYear`.

---

## 11. Tests

| File | Coverage |
|------|----------|
| `tests/luck_engine/test_g1_08_dayun.py` | 4-group direction, gender aliases/missing/invalid, start-age, same-Jie-day, JiaZi wrap, first cycle ±1, boundaries, CASE-0001, Orchestrator |
| `tests/report_engine/test_g1_08_luck_binding.py` | gap note, evidence, elements, HTML/DOCX, API=Report |
| Golden snapshot | luck_cycles sequence + presentation fields `evidence` / `method_note` / `precision` |

Module run: `python -m pytest tests/luck_engine tests/report_engine/test_g1_08_luck_binding.py tests/report_engine/test_case_0001_report_input.py -q` → **PASS**. Portal `vitest run tests/js/g1_08_gender_display.test.ts` → **PASS**.

Out of G1-08 (not repaired): Huỳnh foundation temperature label / score grade; `test_five_elements_adapter_uses_element_values` wood=None.

---

## 12. V1.1 precision backlog

**ID:** `LUCK-PRECISION-V1.1`  
**Blocking V1.0:** no

Scope:

- solar-term exact timestamp;
- timezone-aware Jie boundaries;
- birth hour/minute in delta;
- fractional day delta;
- years/months/days start age;
- exact giao vận datetime;
- exact current-cycle transition (birthday or datetime).

---

## Files changed

- `engines/luck_engine/providers/_common.py` — gender validation, Jie metadata, V1.0 constants
- `engines/luck_engine/providers/dayun.py` — evidence metadata, `branch_element`
- `engines/luck_engine/engine.py` — do not swallow `LuckContextError`
- `engines/luck_engine/models/periods.py` — `branch_element`
- `engines/bazi_engine/ten_god.py` — `BRANCH_META` + `branch_element()`
- `applications/api/services/luck_truth.py` — evidence, elements, precision
- `engines/report_engine/contracts/report_input_v1.py`
- `engines/report_engine/adapters/report_input_v1_adapter.py`
- `engines/report_engine/rendering/report_sections_v1.py`
- Portal adapters / DTO / full report view model / Birth Input
- `applications/api/services/gender_truth.py`
- `applications/api/routes/_helpers.py`
- Golden luck_cycles presentation fields only
- G1-08 tests

---

G1-08 STATUS: FINAL FREEZE READY
