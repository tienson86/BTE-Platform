# G1-11 — CÂN XƯƠNG HEADER INTEGRATION REPORT

Date: 2026-08-30  
Status: **PASS** (live `http://localhost:8081/result`)

---

## 1. STATUS

PASS.

The Identity Header is four regions: Định danh | Tứ Trụ | Cân Xương | Thông tin kỹ thuật.

For live case 24/09/1966 04:15 male Hà Nội:

- Tứ Trụ is unchanged: Bính Ngọ Đoài · Đinh Dậu Đoài · Bính Tuất Chấn · Canh Dần Cấn
- Cân Xương is a summary card, not four dash rows
- Header Cân Xương matches canonical runtime `analysis.can_xuong`
- Technical metadata stays on one line per field; analysis UUID uses ellipsis

Product Owner did not supply an expected bone-weight number. Live UI was compared to the engine output for this chart, not to a guessed sample such as “4 lượng 7 chỉ”.

---

## 2. Existing Cân Xương engine/data audit

No production Cân Xương algorithm existed.

| Surface | Finding |
|---|---|
| Engine | Missing. Identity copies `bone_weight` if present; pipeline never published it |
| Database | No `can_xuong` / `称骨` CSV |
| Orchestrator | `bone_weight=payload.get("bone_weight") or payload.get("can_xuong")` — always empty |
| S10 | Canonical Desktop preview card; `mapS10()` forced unavailable copy |
| Header | Four KV rows `Cân lượng — / Phân loại — / Đánh giá — / Tóm tắt —` |
| Report JS | `summary_builder.js` already looked for `data.can_xuong` |

S09 is Feng Shui. The detailed Cân Xương module is S10. Header “Xem chi tiết” targets `#sec-can-xuong` (S10 on Canonical Desktop; detail block on Commercial Dashboard `/result`).

No second algorithm was created on top of an existing one. This is the first CSV-driven engine.

---

## 3. Canonical data source

Yuan Tian Gang (袁天罡) lookup tables in `database/21_can_xuong/`:

| File | Role |
|---|---|
| `01_nam.csv` | 60 Hoa Giáp → chỉ |
| `02_thang.csv` | Lunar month 1–12 → chỉ |
| `03_ngay.csv` | Lunar day 1–30 → chỉ |
| `04_gio.csv` | Hour earthly branch → chỉ |
| `05_phan_loai.csv` | Total-chỉ bands → classification / rating / summary |
| `06_luan_giai.csv` | Exact total-chỉ → interpretation |
| `version.txt` | `G1-11` |

Frontend does not calculate weight. It copies `analysis.can_xuong`.

Inputs are published Calendar / BaZi values only:

- Year Hoa Giáp = `CalendarResult.year_can_chi` (G1-10B Tam Nguyên year)
- Lunar month / day = calendar lunar date
- Hour branch = `BaziChart.hour_pillar.branch`

Tam Nguyên periods, Cửu Vận, Cung Phi, Tứ Trụ routing, Strength, Pattern, Useful God, Ten Gods, ShenSha, Luck, Narrative were not modified.

---

## 4. New analysis contract

Public Analyze payload now includes:

```json
"can_xuong": {
  "total_weight": 51,
  "liang": 5,
  "chi": 1,
  "display_weight": "5 lượng 1 chỉ",
  "classification": "Thượng cách",
  "rating": "Khá",
  "summary": "Tài lộc khá · hậu vận thuận",
  "interpretation": "...",
  "source": "yuan_tian_gang_can_xuong",
  "version": "G1-11"
}
```

`identity.bone_weight` is a compatibility projection of the same object (`weight` = `display_weight`). Header and S10 both read `analysis.can_xuong` first.

Aliases `weight`, `total`, and `poem` are included so existing report presenters can copy the same payload.

---

## 5. Header binding

`adaptCanXuong` → `adaptIdentityHeader.foundation` → `IdentityFoundation`.

Precedence:

1. `analysis.can_xuong.display_weight` (and classification / summary / interpretation)
2. `identity.bone_weight` only for old payloads

Visual hierarchy:

- Micro-heading: CÂN XƯƠNG ĐOÁN MỆNH
- Large value: display_weight
- Pill: classification
- Max 2-line summary
- Subtle “Xem chi tiết” → `#sec-can-xuong`

Tứ Trụ (`FourPillars` / `TuTruPanel`) was not changed.

Desktop proportions: ~15% / 49% / 20% / 16% with separators.

---

## 6. Detailed section binding

Same canonical object.

- Commercial Dashboard `/result`: `CanXuongDetail` after the frozen card grid, `id="sec-can-xuong"`
- Canonical Desktop S10: `mapS10(data)` copies `can_xuong`; section `id="sec-can-xuong"`
- Workspace `BoneWeightPanel`: prefers `can_xuong.display_weight`

Header does not duplicate the full interpretation.

---

## 7. Empty state

If `can_xuong` is missing and identity bone_weight is empty:

- One line: **Chưa có dữ liệu Cân Xương**
- No `Cân lượng —` / `Phân loại —` / `Đánh giá —` / `Tóm tắt —`

Covered by frontend test B.

---

## 8. Technical metadata cleanup

Primary rows (nowrap + ellipsis):

Tam Nguyên · Cửu Vận · Cung Phi · Mệnh Quái · Nhóm Trạch · Tiết khí

Secondary, smaller:

- Mã phân tích — UUID truncated with ellipsis (`white-space: nowrap`)
- Ngày phân tích

Live computed style on the analysis id: `nowrap`.

---

## 9. Responsive behavior

| Width | Layout |
|---|---|
| Desktop | Identity \| Tứ Trụ \| Cân Xương \| Technical |
| ≤1199px | Identity + Tứ Trụ, then Cân Xương + Technical |
| ≤767px | One column A → B → C → D |

Dashboard card catalog (`DASHBOARD_CARDS`) is unchanged.

---

## 10. Live 1966 runtime values

Chart: 24/09/1966 04:15 male Hà Nội  
Origin: `http://localhost:8081/result`

Engine / HTTP / ResultStore / DOM (same values):

| Field | Value |
|---|---|
| year_ganzhi | Bính Ngọ (13 chỉ) |
| lunar_month | 8 (15 chỉ) |
| lunar_day | 10 (16 chỉ) |
| hour_branch | Dần (7 chỉ) |
| total_weight | 51 |
| display_weight | **5 lượng 1 chỉ** |
| classification | Thượng cách |
| rating | Khá |
| summary | Tài lộc khá · hậu vận thuận |
| version | G1-11 |

Tứ Trụ DOM (unchanged):

Năm BÍNH NGỌ THỦY ĐOÀI · Tháng ĐINH DẬU HỎA ĐOÀI · Ngày BÍNH TUẤT THỔ CHẤN · Giờ CANH DẦN MỘC CẤN

Technical: Trung Nguyên / 6 / Đoài / Đoài / Tây Tứ Trạch / Thu Phân

Bundle: `/static/dist/result.js?v=G1-11`

---

## 11. Frontend tests

`applications/customer_portal/tests/js/g1_11_can_xuong_header.test.tsx`

- A populated: weight, classification, summary visible; no four dash rows
- B empty: “Chưa có dữ liệu Cân Xương”; no four dash rows

Result: **2 passed**

G1-10C Tứ Trụ tests still pass (2).

Unrelated remaining frontend failures (G1-10D ResultStore version gate on fixtures that omit `calendar_rule_version`):

- `result_workspace_binding.test.tsx` (2)
- `ui03_commercial_dashboard.test.tsx` G15 (1)

Those tests were not edited (testing rules). They are not Cân Xương header regressions.

---

## 12. Backend tests

`pytest tests/can_xuong tests/identity -q`

**26 passed**

Includes:

- Year Bính Ngọ lookup = 13 chỉ
- Display split 47 → “4 lượng 7 chỉ”
- Identity copies `display_weight`
- Orchestrator Analyze 1966 publishes `can_xuong` matching the engine

---

## 13. Screenshot evidence

Live viewport ~1648×928 at `http://localhost:8081/result`:

| File | Content |
|---|---|
| `implementation/ui/G1_11_localhost_result_header.png` | First viewport: four-region header + Tứ Trụ dominant |
| `implementation/ui/G1_11_localhost_header_card.png` | Header card only |
| `implementation/ui/G1_11_localhost_can_xuong_detail.png` | `#sec-can-xuong` detail (same canonical values) |

PASS visual checks:

- Tứ Trụ remains the dominant header block
- Cân Xương is its own block (large weight + badge + 1-line summary)
- Technical column readable; UUID ellipsized; no character-by-character wrap
- No overlapping text
- Header height stayed compact (~202px)

---

## 14. Files changed

**New**

- `database/21_can_xuong/01_nam.csv`
- `database/21_can_xuong/02_thang.csv`
- `database/21_can_xuong/03_ngay.csv`
- `database/21_can_xuong/04_gio.csv`
- `database/21_can_xuong/05_phan_loai.csv`
- `database/21_can_xuong/06_luan_giai.csv`
- `database/21_can_xuong/version.txt`
- `engines/can_xuong_engine/` (`__init__.py`, `engine.py`, `calculator.py`, `loader.py`, `models.py`, `exceptions.py`)
- `tests/can_xuong/test_g1_11_can_xuong_engine.py`
- `applications/customer_portal/src/adapters/canonicalCanXuong.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/CanXuongDetail.tsx`
- `applications/customer_portal/tests/js/g1_11_can_xuong_header.test.tsx`
- `implementation/ui/G1_11_CAN_XUONG_HEADER_INTEGRATION_REPORT.md`
- Live screenshots listed in §13

**Modified**

- `applications/api/services/orchestrator.py` — attach `can_xuong` after BaZi (soft-fail)
- `engines/identity/assemble.py` — copy `display_weight` onto `identity.bone_weight`
- `applications/customer_portal/src/screens/commercial_dashboard/adapter.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/types.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/IdentityRegions.tsx`
- `applications/customer_portal/src/screens/commercial_dashboard/CommercialDashboardPage.tsx`
- `applications/customer_portal/src/screens/commercial_dashboard/commercial-dashboard.css`
- `applications/customer_portal/src/screens/commercial_dashboard/canXuongAdapter.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/index.ts`
- `applications/customer_portal/src/screens/canonical_desktop/sections/S10BoneWeightFortune.tsx`
- `applications/customer_portal/src/adapters/canonicalDesktopAdapter.ts`
- `applications/customer_portal/src/adapters/index.ts`
- `applications/customer_portal/src/features/result_workspace/adapter/baziWorkspaceAdapter.ts`
- `applications/customer_portal/src/models/dto.ts`
- `applications/customer_portal/src/models/index.ts`
- `applications/customer_portal/templates/result_desktop.html` — `?v=G1-11`
- `applications/customer_portal/templates/_layout.html` — `?v=G1-11`

G1-11 stops here.
