# Pattern Context Validation

**Date:** 2026-07-29  
**Version:** PatternContext V2  
**Source:** `engines/pattern_engine/context.py` + `utils/context_builder.py`

---

## I. Field Reference

### A. Basic Pillars

| Field | Source | Type | Example | Used by Rule |
|---|---|---|---|---|
| `year_pillar` | `bazi_chart.year_pillar` | `str \| None` | `"Bính Dần"` | — |
| `month_pillar` | `bazi_chart.month_pillar` | `str \| None` | `"Tân Sửu"` | — |
| `day_pillar` | `bazi_chart.day_pillar` | `str \| None` | `"Canh Ngọ"` | — |
| `hour_pillar` | `bazi_chart.hour_pillar` | `str \| None` | `"Mậu Dần"` | — |

### B. Nhật Chủ

| Field | Source | Type | Example | Used by Rule |
|---|---|---|---|---|
| `day_master` | `bazi_chart.day_master` | `str \| None` | `"Canh"` | — |
| `day_master_element` | `STEM_META[day_master][0]` | `str \| None` | `"Kim"` | `spe_kc_01`, `spe_vt_01`, `spe_nh_01`, `spe_gs_01`, `spe_jw_01` |
| `day_master_yin_yang` | `STEM_META[day_master][1]` | `str \| None` | `"Dương"` | (future) |

### C. Month Branch Metadata

| Field | Source | Type | Example | Used by Rule |
|---|---|---|---|---|
| `month_stem` | `bazi_chart.month_pillar.stem` | `str \| None` | `"Tân"` | — |
| `month_branch` | `bazi_chart.month_pillar.branch` | `str \| None` | `"Sửu"` | — |
| `month_branch_element` | `STEM_META[branch_main_stem][0]` | `str \| None` | `"Thổ"` | `spe_kc_01`, `spe_vt_01`, `spe_nh_01`, `spe_gs_01`, `spe_jw_01` |
| `month_stem_ten_god` | `ten_god_name(dm, month_stem)` | `str \| None` | `"Kiếp Tài"` | (future) |
| `month_branch_ten_god` | `ten_god_name(dm, branch_main_stem)` | `str \| None` | `"Chính Ấn"` | All main pattern rules `pat_*` |

### D. Per-Pillar Hidden Stems

| Field | Source | Type | Example | Used by Rule |
|---|---|---|---|---|
| `month_hidden_stems` | `_BRANCH_HIDDEN[month_branch]` | `list[str]` | `["Kỷ", "Quý", "Tân"]` | (future) |
| `year_hidden_stems` | `_BRANCH_HIDDEN[year_branch]` | `list[str]` | `["Giáp", "Bính", "Mậu"]` | (future) |
| `day_hidden_stems` | `_BRANCH_HIDDEN[day_branch]` | `list[str]` | `["Đinh", "Kỷ"]` | (future) |
| `hour_hidden_stems` | `_BRANCH_HIDDEN[hour_branch]` | `list[str]` | `["Giáp", "Bính", "Mậu"]` | (future) |
| `month_hidden_elements` | derived from `month_hidden_stems` | `list[str]` | `["Thổ", "Thủy", "Kim"]` | (future) |

### E. Flat Collections

| Field | Source | Type | Example | Used by Rule |
|---|---|---|---|---|
| `ten_gods` | `{"list": bazi.ten_gods}` | `dict` | `{"list": ["Thất Sát", ...]}` | (legacy) |
| `ten_gods_list` | filtered `bazi.ten_gods` | `list[str]` | `["Thất Sát", "Kiếp Tài"]` | `fol_*`, `com_*` |
| `hidden_stems_flat` | `bazi.hidden_stems` or recomputed | `list[str]` | `["Giáp", "Bính", "Mậu", ...]` | (future) |

### F. Element Distribution

| Field | Source | Type | Example | Used by Rule |
|---|---|---|---|---|
| `element_distribution` | count elements in all stems | `dict[str, int]` | `{"Mộc": 3, "Kim": 2}` | (future) |

### G. Season / Climate

| Field | Source | Type | Example | Used by Rule |
|---|---|---|---|---|
| `season` | `_BRANCH_SEASON[month_branch]` | `str \| None` | `"winter"` | (legacy `spe_*` v1) |
| `season_phase` | `_BRANCH_SEASON_PHASE[month_branch]` | `str \| None` | `"late_winter"` | (future) |
| `temperature_type` | `_BRANCH_TEMPERATURE[month_branch]` | `str \| None` | `"cold"` | (future) |

### H. Ten-God Family Lists

| Field | Source | Type | Example | Used by Rule |
|---|---|---|---|---|
| `support_elements` | Tỷ Kiên + Ấn in `ten_gods_list` | `list[str]` | `["Chính Ấn"]` | (future) |
| `drain_elements` | Thực/Thương + Tài in `ten_gods_list` | `list[str]` | `["Thực Thần", "Chính Tài"]` | (future) |
| `control_elements` | Quan/Sát in `ten_gods_list` | `list[str]` | `["Thất Sát"]` | — |
| `resource_elements` | Ấn in `ten_gods_list` | `list[str]` | `["Chính Ấn"]` | (future) |
| `wealth_elements` | Tài in `ten_gods_list` | `list[str]` | `["Chính Tài"]` | (future) |
| `officer_elements` | Quan + Sát in `ten_gods_list` | `list[str]` | `["Thất Sát"]` | `spe_kc_01`, `spe_vt_01`, `spe_nh_01`, `spe_jw_01` |
| `output_elements` | Thực/Thương in `ten_gods_list` | `list[str]` | `["Thực Thần"]` | `spe_gs_01` |
| `companion_elements` | Tỷ Kiên + Kiếp Tài in `ten_gods_list` | `list[str]` | `["Kiếp Tài"]` | (future) |

### I. Strength (future)

| Field | Source | Type | Example | Used by Rule |
|---|---|---|---|---|
| `strength_level` | Score Engine (not yet populated) | `str \| None` | `"weak"` | (future) |
| `strength_score` | Score Engine | `float` | `0.3` | (future) |

---

## II. Rule Coverage Matrix

| Rule ID | Pattern | Required Fields | All Fields Present? |
|---|---|---|---|
| `pat_cq_01` | chinh_quan | `month_branch_ten_god` | ✅ |
| `pat_ts_01` | that_sat | `month_branch_ten_god` | ✅ |
| `pat_ct_01` | chinh_tai | `month_branch_ten_god` | ✅ |
| `pat_tt_01` | thien_tai | `month_branch_ten_god` | ✅ |
| `pat_tht_01` | thuc_than | `month_branch_ten_god` | ✅ |
| `pat_thuq_01` | thuong_quan | `month_branch_ten_god` | ✅ |
| `pat_ca_01` | chinh_an | `month_branch_ten_god` | ✅ |
| `pat_ta_01` | thien_an | `month_branch_ten_god` | ✅ |
| `pat_tyk_01` | ty_kien | `month_branch_ten_god` | ✅ |
| `pat_ktai_01` | kiep_tai | `month_branch_ten_god` | ✅ |
| `spe_kc_01` | khuc_truc | `day_master_element`, `month_branch_element`, `officer_elements` | ✅ |
| `spe_vt_01` | viem_thuong | `day_master_element`, `month_branch_element`, `officer_elements` | ✅ |
| `spe_nh_01` | nhuan_ha | `day_master_element`, `month_branch_element`, `officer_elements` | ✅ |
| `spe_gs_01` | gia_sac | `day_master_element`, `month_branch_element`, `output_elements` | ✅ |
| `spe_jw_01` | jia_wang | `day_master_element`, `month_branch_element`, `officer_elements` | ✅ |
| `fol_tv_01` | tong_vuong | `ten_gods_list` | ✅ |
| `fol_ttai_01` | tong_tai | `ten_gods_list` | ✅ |
| `fol_tsat_01` | tong_sat | `ten_gods_list` | ✅ |
| `fol_tquan_01` | tong_quan | `ten_gods_list` | ✅ |
| `fol_tnhi_01` | tong_nhi | `ten_gods_list` | ✅ |
| `fol_tan_01` | tong_an | `ten_gods_list` | ✅ |
| `com_qan_01` | quan_an | `ten_gods_list` | ✅ |
| `com_san_01` | sat_an | `ten_gods_list` | ✅ |
| `com_tttai_01` | thuc_than_sinh_tai | `month_branch_ten_god`, `ten_gods_list` | ✅ |
| `com_thuq_an_01` | thuong_quan_phoi_an | `month_branch_ten_god`, `ten_gods_list` | ✅ |
| `com_taiqs_01` | tai_quan_song_my | `ten_gods_list` | ✅ |

**Coverage: 26/26 rules have all required fields = 100%**

---

## III. Field Coverage % (Populated in 100-chart test)

| Field | Populated Count | % | Notes |
|---|---|---|---|
| `day_master` | 100/100 | 100% | Always set |
| `day_master_element` | 100/100 | 100% | All 10 stems in STEM_META |
| `month_branch_ten_god` | 100/100 | 100% | All 12 branches covered |
| `month_branch_element` | 100/100 | 100% | All 12 branches covered |
| `ten_gods_list` | 100/100 | 100% | Always has values |
| `officer_elements` | varies | — | Only when Quan/Sát present |
| `season` | 100/100 | 100% | All 12 branches covered |
| `strength_level` | 0/100 | 0% | ⚠️ Not populated yet — Score Engine runs after Pattern |

---

## IV. Regression Distribution — 100 Charts (After V2)

| Category | Patterns | Count | % |
|---|---|---|---|
| **Main** | chinh_quan, that_sat, chinh_tai, thien_tai, thuc_than, thuong_quan, chinh_an, thien_an, ty_kien, kiep_tai | 61 | 61% |
| **Follow** | tong_vuong, tong_tai, tong_sat, tong_quan, tong_nhi | 18 | 18% |
| **Combination** | sat_an, quan_an, thuong_quan_phoi_an, tai_quan_song_my | 13 | 13% |
| **Special** | nhuan_ha, khuc_truc, viem_thuong, gia_sac, jia_wang | 8 | 8% |

### vs Before (50 charts, V1)

| Category | V1 (%) | V2 (%) | Change |
|---|---|---|---|
| Main | 24% | 61% | +37% ✅ |
| Follow | 16% | 18% | +2% ✅ |
| Combination | 18% | 13% | -5% ✅ |
| Special | 52% | 8% | **-44%** ✅ |

**Special patterns went from 52% → 8% after adding `day_master_element` + `month_branch_element` conditions.**

---

## V. Acceptance Criteria Check

| Criterion | Result |
|---|---|
| Special Pattern không vượt quá mức hợp lý | ✅ 8% (was 52%) |
| Không còn over-match do thiếu context | ✅ |
| Không hard-code điều kiện trong Engine | ✅ Toàn bộ trong CSV |
| Mọi điều kiện nằm trong Rule Database | ✅ |
| 7/7 unit tests pass | ✅ |
| 24 distinct patterns (100 charts) | ✅ |
| No pattern > 50% | ✅ max 11% (chinh_an) |

---

## VI. Known Gaps (Next Iteration)

| # | Gap | Field Needed | Status |
|---|---|---|---|
| 1 | Special cách chưa xét toàn lá số (chỉ xét DM + tháng) | `element_distribution` | ⏳ |
| 2 | `strength_level` chưa được populate | Score Engine kết quả | ⏳ |
| 3 | Follow Cách cần xét tỷ lệ ngũ hành (không chỉ list) | `element_distribution` | ⏳ |
| 4 | Tòng Nhi nên xét cả Thương Quan | Cập nhật `fol_tnhi_01` | ⏳ |
| 5 | Hóa Cách chưa có rules | Cần thêm `02_special_pattern.csv` | ⏳ |

---

*Generated: 2026-07-29 | PatternContext V2 | 100 charts*
