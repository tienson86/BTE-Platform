# UG-R3F — 101-case regression (live recompute)

**Date:** 2026-08-20  
**Input set:** `tests/golden_dataset/inputs` (n=101). **Golden expected files were not edited.**  
**Pipeline:** Calendar → BaZi → Strength → Temperature overlay → Pattern → Useful God (production builders).  
**Before:** same path with Pattern-visible `officer_elements` only (pre-repair matcher input).  
**After:** Useful God context includes canonical hidden Chính Quan.

---

## Overall winner groups (unchanged architecture)

| Group | Before | After | Role |
|-------|------:|------:|------|
| `strength` | 89 | 89 | Overall Dụng thần |
| `special` | 12 | 12 | Overall Dụng thần (follow/chuyên) |
| `season` | 0 | **0** | climate-only (UG-R2) |
| `temperature` | 0 | **0** | climate-only (UG-R2) |
| `flow` | 0 | **0** | structural candidate; never beats Strength |
| incomplete | 0 | **0** | |

Climate recommendations still: season **82**, temperature **19**, none **0**.

---

## Exact Overall winner-rule distribution

| Rule | Before | After | Delta | Layer |
|------|------:|------:|------:|-------|
| `str_003` | 15 | **40** | +25 | overall / strong Chính Quan |
| `str_004` | 29 | **4** | −25 | overall / strong drain fallback |
| `str_005` | 29 | 29 | 0 | overall / balanced |
| `str_002` | 15 | 15 | 0 | overall / weak Ấn fallback |
| `str_001` | 1 | 1 | 0 | overall / weak Chính Ấn |
| `spc_004` | 8 | 8 | 0 | overall / special Ấn |
| `spc_001` | 3 | 3 | 0 | overall / Tòng Tài |
| `spc_003` | 1 | 1 | 0 | overall / Tòng Sát |

**Changed due to hidden Chính Quan:** **25** (all `str_004` → `str_003`).  
**Changed due to `spc_004` / `jia_wang` wiring:** **0** (not wired).  
**Incomplete:** **0**.  
**Failures:** **0**.  
**Duplicate `str_003` publications:** **0**.

The 25 changed IDs:

`case_0001`, `case_0004`, `case_0005`, `case_0011`, `case_0014`, `case_0019`, `case_0026`, `case_0027`, `case_0029`, `case_0035`, `case_0037`, `case_0041`, `case_0045`, `case_0047`, `case_0049`, `case_0051`, `case_0054`, `case_0067`, `case_0070`, `case_0072`, `case_0074`, `case_0076`, `case_0092`, `case_0097`, `case_0101`.

---

## Chính Quan visibility classes

Canonical G1-01: visible heavenly stems + hidden stems from `database/09_hidden_stems` / Pattern hidden lists, mapped with `ten_god_name`. Nhật Chủ excluded.

| Class | Definition | n |
|-------|------------|--:|
| A | visible Chính Quan only | 11 |
| B | hidden-only Chính Quan | 47 |
| C | visible + hidden | 22 |
| D | no Chính Quan | 21 |
| **Total** | | **101** |

### `str_003` candidate counts (publication, not winners)

| Class | Before | After | Notes |
|-------|------:|------:|-------|
| A visible | 6 | 6 | 5 of 11 are not strong / already special-override; no new rows |
| B hidden-only | 0 | **29** | +29 eligibility; 25 win Overall; 4 lose to `spc_004` (92 > 82) |
| C visible+hidden | 10 | **10** | hidden support did **not** duplicate `Chính Quan` or `str_003` |
| D none | 0 | 0 | Thất Sát-only stays unmatched, as designed |

Before: 16 charts published `str_003` (15 won; 1 lost to special).  
After: 45 charts published `str_003` (40 won; 5 lost to `spc_004`).

### Remaining `str_004` (4)

Strong charts with **no** Chính Quan (visible or hidden). Thất Sát does not unlock `str_003`.

| Case | Visibility | Pattern | Display |
|------|------------|---------|---------|
| case_0003 | D none | `chinh_tai` | Thủy · Nhâm · Thực Thần |
| case_0007 | D none (`Thất Sát` only) | `thuc_than_sinh_tai` | Thổ · Kỷ · Thực Thần |
| case_0064 | D none (`Thất Sát` only) | `sat_an` | Kim · Tân · Thực Thần |
| case_0088 | D none | `jia_wang` | Kim · Tân · Thực Thần |

`case_0088` is the live illustration of the **unwired** `jia_wang` / `spc_004` decision.

---

## `jia_wang` cases (3)

| Case | Before | After | Visibility | Note |
|------|--------|-------|------------|------|
| case_0004 | `str_004` | `str_003` | hidden CQ | change is hidden Quan, not `spc_004` |
| case_0014 | `str_004` | `str_003` | hidden CQ | same |
| case_0088 | `str_004` | `str_004` | none | `special_pattern=jia_wang` still does not match `spc_004` |

---

## Flow limitation (unchanged)

Flow `contains` on `element_distribution` remains **unique-max**, not key presence (G1-06).

| Metric | Count |
|--------|------:|
| Charts generating a `flo_*` Overall candidate | 42 |
| Flow Overall winners | **0** |

Group priority 60 never beats Strength 80 or Special 100. **V1.0: Flow is non-competitive.** Do not change this in UG-R3F.

---

## Climate (UG-R2 invariant)

| Climate rule prefix | Count |
|---------------------|------:|
| `sea_*` | 82 |
| `tmp_*` | 19 |

Zero climate Overall winners. Điều hậu ≠ Overall Dụng thần.
