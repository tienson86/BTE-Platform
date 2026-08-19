# G1-01 — Ten Gods Repair Report

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-01 Phase 2 |
| **Date** | 2026-08-19 |
| **Canonical production** | `engines/ten_gods_engine` → `engines.bazi_engine.ten_god.ten_god_name` |
| **Not used in production** | `engines/analysis_engine/ten_gods_engine` |
| **Status** | FINAL FREEZE READY |

No new Ten Gods engine. No Strength / Temperature / Pattern / Useful God / Deep Interpretation work.

---

## 1. Four Fire×Wood conflicts (initial)

Conflict was CSV polarity inverted versus actual stem yin/yang. Algorithm and `STEM_META` already matched `quy_tac.md`.

| Pair | Algorithm | STEM_META | CSV (before) | Canonical expected | Reason |
|------|-----------|-----------|--------------|--------------------|--------|
| Bính×Giáp | Thiên Ấn | Hỏa Dương × Mộc Dương; Cùng; Đối tượng sinh | Khác + Chính Ấn | **Thiên Ấn** | Wood generates Fire; same polarity → Thiên Ấn |
| Bính×Ất | Chính Ấn | Hỏa Dương × Mộc Âm; Khác; Đối tượng sinh | Cùng + Thiên Ấn | **Chính Ấn** | Wood generates Fire; different polarity → Chính Ấn |
| Đinh×Giáp | Chính Ấn | Hỏa Âm × Mộc Dương; Khác; Đối tượng sinh | Cùng + Thiên Ấn | **Chính Ấn** | Wood generates Fire; different polarity → Chính Ấn |
| Đinh×Ất | Thiên Ấn | Hỏa Âm × Mộc Âm; Cùng; Đối tượng sinh | Khác + Chính Ấn | **Thiên Ấn** | Wood generates Fire; same polarity → Thiên Ấn |

Wrong source: **CSV only**. Algorithm, `STEM_META`, and `quy_tac.md` were already correct.

---

## 2. Canonical truth applied

CSV rows TT021, TT022, TT031, TT032 in `database/02_quan_he/thap_than/du_lieu.csv` were corrected to the table above.

---

## 3. Files / sources actually changed

### Data

- `database/02_quan_he/thap_than/du_lieu.csv` — 4 Fire×Wood rows

### Mapping evidence (no new calculator)

- `engines/bazi_engine/ten_god.py` — helpers for element / polarity / relation
- `engines/ten_gods_engine/models.py` — additive evidence fields on visible/hidden entries
- `engines/ten_gods_engine/calculator.py` — copy evidence from `stem_mapping_facts`; pass pillar + visibility into mapper
- `engines/ten_gods_engine/mapper.py` — Nhật Chủ only for Day Pillar heavenly stem; same stem elsewhere is Tỷ Kiên

### Canonical public binding (copy, do not recalculate)

- `applications/api/services/ten_gods_truth.py` — `shape_ten_gods_payload`
- `applications/api/models/analysis_result.py` — `ten_gods_result`
- `applications/api/services/orchestrator.py` — one `TenGodsEngine.calculate`; reuse for narrative
- `applications/production/engine_runner.py` — attach result to analysis + report source
- `engines/report_engine/adapters/report_input_v1_adapter.py`
- `engines/report_engine/contracts/report_input_v1.py` — entries kept off snapshot JSON
- `engines/report_engine/rendering/report_sections_v1.py` — Lộ / Tàng + pillar provenance
- `applications/production/orchestrator.py` — cover summary splits Lộ / Tàng

### Portal (display only)

- `applications/customer_portal/src/adapters/tenGodsDisplay.ts`
- `applications/customer_portal/src/adapters/baziResultAdapter.ts`
- `applications/customer_portal/src/adapters/canonicalDesktopAdapter.ts`
- `applications/customer_portal/src/models/dto.ts`
- `applications/customer_portal/src/resultState/currentResult.ts`
- `applications/customer_portal/src/report/fullReportViewModel.ts`
- `applications/customer_portal/src/screens/bazi/*` (pillars + Ten Gods split)
- `applications/customer_portal/src/screens/canonical_desktop/sections/S03FourPillars.tsx`
- `applications/customer_portal/src/screens/canonical_desktop/sections/S06TenGods.tsx`
- `applications/customer_portal/static/js/presenters/bazi.js`
- `applications/customer_portal/static/js/presenters/discussion.js`
- `applications/customer_portal/static/js/presenters/summary_builder.js`
- `applications/customer_portal/static/i18n/vi.json`

### Tests added

- `tests/ten_gods_engine/test_mapping_matrix.py`
- `tests/ten_gods_engine/test_g1_01_golden_case.py`
- `tests/ten_gods_engine/test_g1_01a_day_master_role.py`
- `tests/report_engine/test_g1_01_ten_gods_presentation.py`
- `tests/ten_gods_engine/test_core_ten_gods.py` — same-stem relationship is Tỷ Kiên; Nhật Chủ only with `pillar="day"`

---

## 4. 100-mapping test

`tests/ten_gods_engine/test_mapping_matrix.py`

Oracle is independent of `ten_god_name`: STEM identity + generate/control + Chính/Thiên from `quy_tac.md`.

Asserts for every Day Master × stem: element, polarity, relationship, Ten God — against algorithm, `stem_mapping_facts`, and CSV.

Result: **100/100 PASS** (`tests/ten_gods_engine/test_mapping_matrix.py`).

---

## 5. Golden CASE

Chart: Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần. Day Master: Canh.

**Visible 4/4**

| Pillar | Stem | Ten God |
|--------|------|---------|
| year | Bính | Thất Sát |
| month | Tân | Kiếp Tài |
| day | Canh | Nhật Chủ |
| hour | Mậu | Thiên Ấn |

**Hidden 11/11**

| Pillar | Branch | Stem | Ten God |
|--------|--------|------|---------|
| year | Dần | Giáp | Thiên Tài |
| year | Dần | Bính | Thất Sát |
| year | Dần | Mậu | Thiên Ấn |
| month | Sửu | Kỷ | Chính Ấn |
| month | Sửu | Quý | Thương Quan |
| month | Sửu | Tân | Kiếp Tài |
| day | Ngọ | Đinh | Chính Quan |
| day | Ngọ | Kỷ | Chính Ấn |
| hour | Dần | Giáp | Thiên Tài |
| hour | Dần | Bính | Thất Sát |
| hour | Dần | Mậu | Thiên Ấn |

Public payload keeps hidden as mapped Ten God occurrences (not a tàng-can name list).

---

## 6. Portal

`/result` consumes `data.ten_gods` from `TenGodsEngine` via `shape_ten_gods_payload`.

- Tứ trụ: stem as `Bính · Hỏa`, Ten God on the pillar, tàng can as `Giáp · Mộc · Thiên Tài`.
- Summary splits **Lộ can** vs **Tàng can**.
- Note: `Xác định theo quan hệ Ngũ hành và âm dương với Nhật chủ.`
- No Ten God math in JS/TS. No Deep Interpretation.

---

## 7. Report / PDF / DOCX

HTML, PDF, and DOCX share `build_presented_report`.

- Section 05 splits Lộ can / Tàng can and prints hidden lines with stem · element · Ten God.
- Pillar Ẩn can uses canonical hidden entries, not a stem-name-only list.
- ReportInputV1 JSON `ten_gods.hidden` remains the compact stem list so the CASE-0001 snapshot stays stable. Presentation reads `hidden_entries`.

---

## 8. Code / data changed

See §3. Canonical production engine was not replaced.

---

## 9. Regression tests

Executed (module only):

```text
pytest tests/ten_gods_engine \
       tests/report_engine/test_g1_01_ten_gods_presentation.py \
       tests/report_engine/test_case_0001_report_input.py \
       tests/production/test_p1_calendar_data_recovery.py::test_ten_gods_customer_model_not_score -q
→ 67 passed
```

Includes 100-mapping, Golden CASE visible 4/4 + hidden 11/11, G1-01A same-stem role (10 Day Masters), Report presentation, CASE-0001 snapshot.

---

## 10. Remaining issues

- Compact ReportInputV1 JSON `ten_gods.hidden` still lists tàng-can **names**. This is a **NON-BLOCKING** V1.1 compatibility/technical-debt field. Canonical presentation source is `hidden_entries` / `TenGodsResult.hidden`. Snapshot kept.
- `engines/analysis_engine/ten_gods_engine` remains unused in production, as required.

G1-01A closed the same-stem overlay: hidden/year/month/hour same as Day Master → **Tỷ Kiên**. Only Day Pillar heavenly stem → **Nhật Chủ**.

G1-01 STATUS: FINAL FREEZE READY
