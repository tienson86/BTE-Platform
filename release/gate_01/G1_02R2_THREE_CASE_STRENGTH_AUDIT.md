# G1-02R2 — Three-Case Strength Calculation Audit

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-02R2 Phase A forensic |
| **Date** | 2026-08-20 |
| **Scope** | Strength Engine calculation only. Thresholds not changed. |
| **Cases** | Nguyễn Tiến Sơn · Lương Ngọc Huỳnh · Đặng Thị Dung |
| **Normalization** | `(raw + 50) / 100`, clamp `[0, 1]` |
| **Class rules** | `strong >= 0.65` · `weak <= 0.35` · else `balanced` (`06_priority_rules.csv`) |

**Phase A only.** No Strength CSV scores, no class thresholds, and no case-targeted weights were changed.

**Phase B verdict:** no calculation defect proven. See §10.

---

## Frozen live numbers (engine, this repo)

| Case | Civil birth used | Pillars | Day Master | Raw | Normalized | Class |
|------|------------------|---------|------------|----:|-----------:|-------|
| Nguyễn Tiến Sơn | 1987-01-21 04:30 male | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần | Canh Kim | 37 | 0.87 | strong |
| Lương Ngọc Huỳnh | 1966-09-24 04:15 male | Bính Ngọ / Đinh Dậu / Bính Tuất / Canh Dần | Bính Hỏa | 14 | 0.64 | balanced |
| Đặng Thị Dung | 1982-05-22 09:30 female | Nhâm Tuất / Ất Tỵ / Ất Tỵ / Tân Tỵ | Ất Mộc | −26 | 0.24 | weak |

Score Engine composite is **not** Điểm thân. These numbers are Strength Engine `raw_total` / `strength_score`.

---

## 1. Full decomposition — Nguyễn Tiến Sơn

Chart: `Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần`  
Day Master: **Canh Kim**

Context:

| Field | Value |
|-------|-------|
| `month_status` | **Tướng** (Sửu Thổ sinh Kim) |
| `month_branch_ten_god` | **Chính Ấn** (Sửu bản khí Kỷ) |
| `season` / `season_phase` | winter / late_winter |
| `root_level` / `root_count` | Thông căn 1 chi / 1 |
| `support_type` | Đồng hành trợ thân (month **Tân** Kiếp Tài) |
| `control_type` | Bị Quan Sát khắc (year **Bính** Thất Sát) |
| `drain_type` | `None` |
| `output_branch_count` | 0 |
| `resource_elements` | `Thiên Ấn` (hour Mậu — **not** scored as named Chính Ấn) |
| `companion_elements` | `Kiếp Tài` |
| `officer_elements` | `Thất Sát` |
| `output_elements` / `wealth_elements` | empty |

Visible thập thần: year Thất Sát · month Kiếp Tài · hour Thiên Ấn.

Hidden by pillar:

| Pillar | Branch | Hidden (vs Canh) | Kim root? |
|--------|--------|------------------|-----------|
| Year | Dần | Giáp / Bính / Mậu | no |
| Month | Sửu | Kỷ Chính Ấn, Quý Thương Quan, **Tân Tỷ Kiên** | **yes (余气 Tân)** |
| Day | Ngọ | Đinh / Kỷ | no |
| Hour | Dần | Giáp / Bính / Mậu | no |

Residual Quý in Sửu is output-element Water but **not** branch bản khí (bản khí = Kỷ Thổ). G1-02R correctly excludes it from drain.

| Category | Evidence | Rule ID | Points | Unique evidence ID | Overlap |
|----------|----------|---------|-------:|--------------------|---------|
| Season / 月令 | Sửu Thổ sinh Canh → Tướng | `sea_002` | +25 | `month_branch:Sửu` + `month_el:Thổ→Kim` | shares Sửu 印令 with `spc_004` |
| Root | Sửu tàng **Tân** Kim | `root_003` | +12 | `hidden:month:Sửu:Tân` | 透/藏 pair with month Tân |
| Resource / Ấn (named) | hour Mậu Thiên Ấn in list | — | 0 | `visible:hour:Mậu` | no `contains Thiên Ấn` rule |
| Peer / Tỷ Kiếp | month Tân Kiếp Tài → `support_type` | `sup_001` | +8 | `visible:month:Tân` | 透 vs 藏 with root Tân |
| Output / Thực Thương | none visible; Quý residual only | — | 0 | `hidden:month:Sửu:Quý` | excluded from drain by design |
| Wealth / Tài | none | — | 0 | — | — |
| Officer / Killings | year Bính Thất Sát → type | `ctl_001` | −10 | `visible:year:Bính` | dual-dimension with `ctl_006` |
| Officer named | `officer_elements` contains Thất Sát | `ctl_006` | −8 | `visible:year:Bính` | same stem as `ctl_001` |
| Special seasonal | 月令 Chính Ấn + winter | `spc_004` | +10 | `month_main:Kỷ` + `season:winter` | 印令 theme with `sea_002` |
| Caps / volume | `flw_005` not reached | — | 0 | — | — |
| Combination | none | — | 0 | — | — |
| **Raw / norm / class** | `(37+50)/100` | — | **37 / 0.87 / strong** | — | — |

Matched: `sea_002`, `root_003`, `sup_001`, `ctl_001`, `ctl_006`, `spc_004`.

Evidence compact: `Tướng địa theo tháng +25 · Có căn khí +12 · Đồng hành trợ thân +8 · Bị Quan Sát khắc -10 · Có Thất Sát -8 · Ấn mùa lạnh +10`.

---

## 2. Full decomposition — Lương Ngọc Huỳnh

Chart: `Bính Ngọ / Đinh Dậu / Bính Tuất / Canh Dần`  
Day Master: **Bính Hỏa**

Context:

| Field | Value |
|-------|-------|
| `month_status` | **Tù** (Hỏa khắc Kim; Dậu Kim) |
| `month_branch_ten_god` | **Chính Tài** (Dậu bản khí Tân) |
| `season` / `season_phase` | autumn / mid_autumn |
| `root_level` / `root_count` | Thông căn 3 chi trở lên / **3** |
| `support_type` | Đồng hành trợ thân (year **Bính** Tỷ Kiên) |
| `control_type` | Bị Tài tinh hao (hour **Canh** Thiên Tài) |
| `drain_type` | Thực Thương tiết khí (Tuất Thổ bản khí) |
| `output_branch_count` | 1 (day Tuất) |
| `drain_count` | 2 (`wealth_count 1` + `output_branch_count 1`) |
| `resource_elements` | **[]** (Giáp Thiên Ấn in Dần is hidden only) |
| `companion_elements` | Tỷ Kiên, Kiếp Tài |
| `wealth_elements` | Thiên Tài |
| `output_elements` | [] (no visible Thực Thương) |

Trace requested by the gate:

| Object | Engine treatment | Scored? |
|--------|------------------|---------|
| Bính Nhật chủ | Day stem; not in thập thần lists | identity only |
| Bính lộ năm | Tỷ Kiên → `support_type` Đồng hành | `sup_001` +8 |
| Đinh lộ tháng | Kiếp Tài; companion list | **no extra named rule** (only `sup_007` wants Tỷ Kiên) |
| Ngọ | bản khí Đinh Hỏa → root pillar 1 | inside `root_001` +30 |
| Dần | tàng Bính Hỏa → root pillar 3; tàng Giáp Ấn **hidden** | root yes; Ấn **no** |
| Bính tàng (Dần) | same-element hidden → root | inside `root_001` |
| Hỏa support | 6 Hỏa in element_distribution; scored via root + peer type | yes, as root/peer not as a Fire blob |
| Dậu / Kim | 月令 Tù −10; 月令 Chính Tài | `sea_004` |
| Canh / Kim | hour Thiên Tài | `ctl_003` −6 + `flw_004` −5 |
| Tân tàng (Dậu, Tuất) | Kim hidden; not Fire root | wealth/season only |
| Thổ output/drain | Tuất bản khí Mậu = Hỏa sinh Thổ | `flw_001` −8 |
| mùa Dậu / Thu | `season=autumn`, status **囚 Tù** | `sea_004` −10 |

Root pillars (any hidden stem of Hỏa):

| Pillar | Branch | Hidden Fire | Quality in branch |
|--------|--------|-------------|-------------------|
| Year | Ngọ | Đinh | **本气** |
| Month | Dậu | none | — |
| Day | Tuất | Đinh | **余气** |
| Hour | Dần | Bính | **中气** |

| Category | Evidence | Rule ID | Points | Unique evidence ID | Overlap |
|----------|----------|---------|-------:|--------------------|---------|
| Season / 月令 | Dậu Kim; Hỏa khắc Kim → Tù | `sea_004` | −10 | `month_branch:Dậu` + `month_el:Kim` | — |
| Root | 3 chi Hỏa (Ngọ, Tuất, Dần) | `root_001` | +30 | `root_pillars:{Ngọ,Tuất,Dần}` | 通根 vs 透 Bính/Đinh |
| Resource / Ấn | Giáp in Dần hidden only | — | 0 | `hidden:hour:Dần:Giáp` | visible-list design |
| Peer / Tỷ Kiếp | year Bính Tỷ Kiên → type | `sup_001` | +8 | `visible:year:Bính` | with `sup_007` |
| Peer named | contains Tỷ Kiên | `sup_007` | +5 | `visible:year:Bính` | dual-dimension |
| Output / Drain | Tuất Thổ bản khí | `flw_001` | −8 | `branch:day:Tuất:Mậu` | G1-02R output-branch |
| Wealth drain named | hour Canh Thiên Tài | `flw_004` | −5 | `visible:hour:Canh` | with `ctl_003` |
| Officer / Killings | none | — | 0 | — | — |
| Control type | same Canh → Bị Tài tinh hao | `ctl_003` | −6 | `visible:hour:Canh` | type + named wealth |
| Special | 月令 is Tài, not Ấn; autumn would not fire `spc_004` without Chính Ấn | — | 0 | — | — |
| Caps | `drain_count=2` < 3 | — | 0 | — | `flw_005` not reached |
| **Raw / norm / class** | `(14+50)/100` | — | **14 / 0.64 / balanced** | — | — |

Matched: `sea_004`, `root_001`, `sup_001`, `sup_007`, `ctl_003`, `flw_001`, `flw_004`.

Evidence compact: `Tù khí theo tháng -10 · Căn khí rất mạnh +30 · Đồng hành trợ thân +8 · Có Tỷ Kiên +5 · Bị Tài tinh hao -6 · Thực Thương tiết khí -8 · Có Thiên Tài -5`.

Historical note: pre-G1-02R this chart used visible-wealth drain (`flw_002` −6) instead of output-branch `flw_001` −8, raw 16 / **0.66 strong**. The −2 raw is Fire→Earth symmetry with Dung Wood→Fire, not a new Huỳnh-specific penalty.

---

## 3. Full decomposition — Đặng Thị Dung

Chart: `Nhâm Tuất / Ất Tỵ / Ất Tỵ / Tân Tỵ`  
Day Master: **Ất Mộc**  
Weak control after G1-02R.

Context:

| Field | Value |
|-------|-------|
| `month_status` | **Hưu** (Mộc sinh Hỏa; Tỵ Hỏa) |
| `month_branch_ten_god` | Thương Quan (Tỵ bản khí Bính) |
| `season` / `season_phase` | summer / early_summer |
| `root_level` / `root_count` | Vô căn / 0 |
| `support_type` | Ấn tinh sinh thân (year **Nhâm** Chính Ấn) |
| `control_type` | Bị Quan Sát khắc (hour **Tân** Thất Sát) |
| `drain_type` | Thực Thương tiết khí |
| `output_branch_count` | **3** (Tỵ ×3) |
| `drain_count` | **3** |

Drain repair still connected: three Tỵ bản khí Bính / Thương Quan. Aggregation remains `flw_001` once (−8) + `flw_005` once (−10) because `drain_count >= 3`. **Not** 3 × −8.

| Category | Evidence | Rule ID | Points | Unique evidence ID | Overlap |
|----------|----------|---------|-------:|--------------------|---------|
| Season / 月令 | Tỵ Hỏa; Ất sinh Hỏa → Hưu | `sea_003` | +10 | `month_branch:Tỵ` | 休 vs drain on same 生 relation |
| Root | no Mộc in four branches | `root_005` | −20 | `root:none` | — |
| Resource type | year Nhâm Chính Ấn | `sup_002` | +10 | `visible:year:Nhâm` | with `sup_006` |
| Resource named | contains Chính Ấn | `sup_006` | +5 | `visible:year:Nhâm` | dual-dimension |
| Peer | month Ất Tỷ Kiên | `sup_007` | +5 | `visible:month:Ất` | independent |
| Output / Drain presence | Tỵ ×3 bản khí | `flw_001` | −8 | `branch:Tỵ×3:Bính` | with volume `flw_005` |
| Drain volume | `drain_count >= 3` | `flw_005` | −10 | `drain_count:3` | presence vs volume |
| Wealth drain | hidden Mậu only | — | 0 | residual | not in visible wealth |
| Officer type | hour Tân Thất Sát | `ctl_001` | −10 | `visible:hour:Tân` | with `ctl_006` |
| Killings named | contains Thất Sát | `ctl_006` | −8 | `visible:hour:Tân` | dual-dimension |
| Special | none | — | 0 | — | — |
| **Raw / norm / class** | `(−26+50)/100` | — | **−26 / 0.24 / weak** | — | — |

Matched: `sea_003`, `root_005`, `sup_002`, `sup_006`, `sup_007`, `ctl_001`, `ctl_006`, `flw_001`, `flw_005`.

Pre-G1-02R: drain omitted → raw −8 / **0.42 balanced**. Current 0.24 is the repaired drain, not a new G1-02R2 movement.

---

## 4. Normalized comparison (do not merge categories)

Component scores below are **raw points** (same units as CSV `score`). Normalized row is 0–1.

| Component | Sơn | Huỳnh | Dung |
|-----------|----:|------:|-----:|
| Season | +25 | −10 | +10 |
| Root | +12 | +30 | −20 |
| Resource | 0 | 0 | +15 (`sup_002`+`sup_006`) |
| Peer | +8 | +13 (`sup_001`+`sup_007`) | +5 (`sup_007`) |
| Output/Drain | 0 | −8 | −18 (`flw_001`+`flw_005`) |
| Wealth drain | 0 | −5 (`flw_004`) | 0 |
| Officer/Killings | −18 | 0 | −18 |
| Control-as-wealth (type) | 0 | −6 (`ctl_003`) | 0 |
| Special | +10 | 0 | 0 |
| Combination | 0 | 0 | 0 |
| **Raw** | **37** | **14** | **−26** |
| **Normalized** | **0.87** | **0.64** | **0.24** |
| **Class** | **strong** | **balanced** | **weak** |

Huỳnh support is listed split (peer +13) rather than one “support bucket” so the +5 Tỷ Kiên named star is visible. Engine `support_score` for Huỳnh is +0.13; Dung `support_score` is +0.20 (Ấn + peer).

---

## 5. The 23-point gap (Sơn 0.87 vs Huỳnh 0.64)

Normalized difference = `0.87 − 0.64 = 0.23` = **23 raw points / 100**.  
Raw difference = `37 − 14 = 23`.

| Component | Sơn | Huỳnh | Sơn − Huỳnh | Exact rules |
|-----------|----:|------:|------------:|-------------|
| Season | +25 | −10 | **+35** | `sea_002` Tướng vs `sea_004` Tù |
| Root | +12 | +30 | **−18** | `root_003` 1 chi vs `root_001` 3 chi |
| Support / peer | +8 | +13 | **−5** | `sup_001` vs `sup_001`+`sup_007` |
| Output drain | 0 | −8 | **+8** | none vs `flw_001` Tuất Thổ |
| Wealth named | 0 | −5 | **+5** | none vs `flw_004` Canh |
| Control | −18 | −6 | **−12** | officer dual −18 vs `ctl_003` −6 |
| Special | +10 | 0 | **+10** | `spc_004` vs none |
| **Total** | **37** | **14** | **23** | |

Check: `35 − 18 − 5 + 8 + 5 − 12 + 10 = 23`.

This is **not** “because seasons differ” as a slogan. Season is the **largest single term (+35)** and is then **offset** by Huỳnh’s much stronger root (−18 against Sơn) and by Sơn’s heavier officer control (−12 against Huỳnh) plus Sơn’s special +10. Drain/wealth on Huỳnh accounts for **+13** of Sơn’s lead (`flw_001`+`flw_004`).

One-sentence mechanism:

> Sơn is 月令 Tướng with light root and officer drag; Huỳnh is 月令 Tù with heavy Fire root and Fire→Earth plus Metal wealth drain. The net of those independent buckets is 23 raw points.

---

## 6. Sơn support stacking (`+25`, `+12`, `+8`, `+10`)

### A. Seasonal +25 — `sea_002`

| Item | Value |
|------|-------|
| Source | `database/12_strength/01_season_rules.csv` |
| Trigger | `month_status == Tướng` |
| Evidence | Month branch **Sửu**; bản khí **Kỷ / Thổ**; Thổ sinh Kim |
| Taxonomy | 旺相休囚死 → **相 Tướng** (month produces Day Master) |

### B. Root +12 — `root_003`

| Item | Value |
|------|-------|
| Trigger | `root_level == Thông căn 1 chi` |
| Branch | **Sửu** only |
| Hidden stem | **Tân** Kim (余气, not Sửu 本气) |
| Direct/indirect | Indirect 通根 (hidden same element). Not sitting on a Kim branch. |

### C. Peer/support +8 — `sup_001`

| Item | Value |
|------|-------|
| Trigger | `support_type == Đồng hành trợ thân` |
| Stem | Visible month **Tân** |
| Ten-god | Kiếp Tài (Tân vs Canh) |
| First-match | `_detect_support_type` returns peer before resource, so hour Mậu Thiên Ấn does **not** set Ấn type |

### D. Ấn mùa lạnh +10 — `spc_004`

See §7. Evidence is Sửu **Kỷ** Chính Ấn 月令 + winter, **not** hour Mậu and **not** root Tân.

### Independence verdict

These are **not four copies of one Thổ/Kim blob**. They are **two pairs**:

| Pair | Shared object | Distinct semantics |
|------|---------------|--------------------|
| `+25` and `+10` | Sửu **Kỷ** 印令 (Thổ sinh Kim) | 旺相 taxonomy vs special “Ấn in cold season” |
| `+12` and `+8` | **Tân** Kim | 通根 (藏) vs 透 (visible peer) |

Hour Mậu Thiên Ấn is a **third** 印 object and is **not** in the +10 / +25 / +8 / +12 stack as a scored resource star.

Classical 透 vs 通根 is treated as **legitimate multi-dimension**, same pattern as officer `ctl_001`+`ctl_006`.

`sea_002`+`spc_004` share 印令. Classified in §7 / §9.

---

## 7. Audit `Ấn mùa lạnh +10` (`spc_004`)

| Item | Value |
|------|-------|
| Rule ID | `spc_004` |
| File | `database/12_strength/07_special_rules.csv` |
| Score / target | +10 / `special` |
| Trigger | `month_branch_ten_god == Chính Ấn` **AND** `season in {winter, autumn}` |
| Month / season here | Sửu / **winter** (late_winter) |
| Required Resource | **月令** Chính Ấn (branch main stem vs Day Master), not “any Ấn in the chart” |
| Exact Resource evidence | Sửu bản khí **Kỷ** vs Canh = Chính Ấn |
| Already scored elsewhere? | Same Kỷ 印令 already implied by **Tướng** (`sea_002`), because 相 **is** “month produces DM” = 印 season for all five elements |
| Additive vs modifier | Additive special bucket. Does **not** multiply or replace `sea_002`. Priority 102 does **not** override class (`spc_*` class override requires priority ≥ 105) |

**Not** a re-score of:

- hour Mậu Thiên Ấn (different stem, Thiên Ấn, no named rule fired);
- root Tân / peer Tân (Kim 比劫, not 印).

**POTENTIAL DOUBLE COUNT (印令 theme):** `sea_002` and `spc_004` both reward the fact that 月令 is 印. `spc_004` adds an extra condition (cold/autumn season). Independent claimed semantics: “Ấn sinh thân mùa lạnh”. A Fire chart in 相 (spring Wood 月令) would get `sea_002` +25 **without** `spc_004`.

This is **not** proven identical-meaning duplicate scoring of one stem in two support rules. It is **related seasonal stacking**. Removing `spc_004` would move Sơn to raw 27 / **0.77 still strong**. That would not satisfy a Product Owner request to leave the strong class, and it would be Sơn-tuning.

**Decision:** mark potential 印令 overlap; **do not delete** the rule in this gate.

---

## 8. Why Huỳnh is 0.64 despite stacked Fire

Visible / hidden Fire is real. The engine **does** count it, mainly as **root +30**, not as a second Fire bonus:

| Fire object | Points |
|-------------|-------:|
| Year Bính 透 Tỷ Kiên | inside `sup_001` +8 and `sup_007` +5 |
| Month Đinh 透 Kiếp Tài | sets companion list only; **no extra CSV row** |
| Ngọ 本气 Đinh | root pillar |
| Tuất 余气 Đinh | root pillar |
| Dần 中气 Bính | root pillar |
| Dần 藏 Giáp Ấn | **0** (hidden; `resource_elements` is visible stems) |

Offsets:

| Drag | Points | Why |
|------|-------:|-----|
| Dậu 囚 | −10 | Hỏa khắc Kim 月令 |
| Tuất Thổ drain | −8 | Fire→Earth bản khí (G1-02R) |
| Canh Thiên Tài named | −5 | wealth list |
| Canh control type | −6 | `Bị Tài tinh hao` |

Net: `−10 + 30 + 13 − 8 − 5 − 6 = 14` → 0.64.

**Undercount?** Month Đinh is not given a second named-companion bonus. That is first-match `support_type` plus one `contains Tỷ Kiên` rule — the same model Sơn uses (one peer type, no `contains Kiếp Tài` rule). Hidden Ấn is unscored by design; counting it would **raise** Huỳnh and would be a forbidden case target.

**Overcount drain/wealth?** Dual `ctl_003`+`flw_004` on the same Canh is the frozen type+named pattern (mirror of Sơn `ctl_001`+`ctl_006`). `flw_001` on Tuất is required five-element symmetry with Dung’s Tỵ drain. `drain_count=2` does **not** fire the heavy cap `flw_005`.

**Verdict:** Huỳnh 0.64 is the arithmetic of Tù + strong root + peer + Fire→Earth + Metal wealth. Not a missing-support defect. Not a reason to change thresholds (`0.64` stays **balanced**; `0.65` is strong).

---

## 9. Root quality comparison

Engine rule: count **pillars** whose hidden stems include **any** stem of the Day Master element. Then map count → label (`02_root_rules.csv`). Per-pillar test is binary (has / has not). It does **not** weight 本气 vs 中气 vs 余气.

| | Sơn Canh | Huỳnh Bính | Dung Ất |
|--|----------|------------|---------|
| Root branch(es) | Sửu | Ngọ, Tuất, Dần | none |
| Hidden stem(s) used | Tân | Đinh, Đinh, Bính | — |
| Direct sitting? | No (day is Ngọ Hỏa) | Year sits Ngọ Hỏa **本气** | No |
| Indirect 通根 | Sửu 余气 Tân | Tuất 余气 + Dần 中气 | — |
| `root_count` | 1 | 3 | 0 |
| Label | Thông căn 1 chi | Thông căn 3 chi trở lên | Vô căn |
| Points | +12 `root_003` | +30 `root_001` | −20 `root_005` |

**Gap (not repaired):** CSV has count levels (0 / tàng-can / 1 / 2 / 3+) but **not** quality levels inside a branch. Sơn’s only root is 余气; Huỳnh mixes 本气+中气+余气 and still gets the same +30 as three 本气 would. Documented; **no root-model redesign** in this gate.

`root_004` Thông căn tàng can (+6) is the leftover path when the flat `hidden_stems` list has the element but no per-pillar hit — not used by these three charts.

---

## 10. Seasonal power comparison

Mapping (`_compute_month_status`): same element → 旺 Đắc lệnh; month sinh DM → 相 Tướng; DM sinh month → 休 Hưu; DM khắc month → 囚 Tù; month khắc DM → 死 Tử.

| | Sơn | Huỳnh | Dung |
|--|-----|-------|------|
| Month | Sửu Thổ | Dậu Kim | Tỵ Hỏa |
| Relation | Thổ sinh Kim | Hỏa khắc Kim | Mộc sinh Hỏa |
| State | **相 Tướng** | **囚 Tù** | **休 Hưu** |
| Points | +25 `sea_002` | −10 `sea_004` | +10 `sea_003` |
| Rule source | `01_season_rules.csv` | same | same |

Sơn Canh sinh Sửu is **not** Hưu: month element is Thổ (Kỷ), which **produces** Kim → Tướng. The Day Master does not “sit in the season it produces”; 月令 is the branch bản khí.

This seasonal pair (Tướng vs Tù) is **+35 raw** and is the largest term in the 23-point gap.

---

## 11. Drain / control symmetry (post G1-02R)

Drain type is set if (1) visible output stems exist, else (2) `output_branch_count > 0` (branch bản khí produced by DM), else (3) visible wealth.

| DM → produced | Case | Branch bản khí used? | Result |
|---------------|------|----------------------|--------|
| Ất Mộc → Hỏa | Dung | Tỵ ×3 Bính | `flw_001` + `flw_005` |
| Bính Hỏa → Thổ | Huỳnh | Tuất Mậu | `flw_001` (count 1, no `flw_005`) |
| Canh Kim → Thủy | Sơn | no Thủy branch; Quý in Sửu is residual | drain **None** (correct) |

Five-element smoke (constructed charts, not the three cases): each of Mộc→Hỏa, Hỏa→Thổ, Thổ→Kim, Kim→Thủy, Thủy→Mộc with one output branch sets `drain_type=Thực Thương tiết khí` and matches `flw_001`. See `tests/strength/test_g1_02r2_five_element_symmetry.py`.

G1-02R drain is **not** Wood-specific. Huỳnh’s Fire→Earth hit is the corresponding path, not a bug.

---

## 12. Duplicate evidence (all three cases)

Provenance key = stem occurrence / hidden stem / branch / month state.

### Legitimate multi-dimension

| Case | Rules | Shared object | Why kept |
|------|-------|---------------|----------|
| Sơn | `ctl_001` + `ctl_006` | year Bính Thất Sát | type vs named star (frozen G1-02 / G1-02R) |
| Sơn | `sup_001` + `root_003` | Tân 透 vs Tân 藏 | 透 vs 通根 |
| Huỳnh | `sup_001` + `sup_007` | year Bính Tỷ Kiên | type vs named star |
| Huỳnh | `ctl_003` + `flw_004` | hour Canh Thiên Tài | control type vs named wealth drain |
| Huỳnh | `root_001` + peer stems | Bính/Đinh vs Ngọ/Dần/Tuất Hỏa | 透 vs 通根 |
| Dung | `sup_002` + `sup_006` | year Nhâm Chính Ấn | type vs named star |
| Dung | `ctl_001` + `ctl_006` | hour Tân Thất Sát | same officer pattern as Sơn |
| Dung | `flw_001` + `flw_005` | Tỵ drain | presence vs volume (G1-02R intended) |
| Dung | `sea_003` + `flw_001` | Mộc sinh Hỏa | 休 月令 vs branch tiết — different buckets |

### Potential duplicate (not auto-removed)

| Case | Rules | Shared object | Class |
|------|-------|---------------|-------|
| Sơn | `sea_002` + `spc_004` | Sửu Kỷ 印令 | **POTENTIAL DOUBLE COUNT** of 印 season theme; extra cold-season predicate on `spc_004` |

Not every overlap is a bug. No overlap was proven as two CSV rows scoring the **same analytical sentence** on the **same dimension** without an independent predicate.

---

## 13. Thresholds (unchanged)

| Band | CSV | These cases |
|------|-----|-------------|
| weak | `strength_score <= 0.35` | Dung 0.24 |
| balanced | `> 0.35` and `< 0.65` | Huỳnh **0.64** |
| strong | `>= 0.65` | Sơn 0.87 |

Huỳnh remains balanced. Sơn remains strong. No threshold move.

---

## 14. Dung regression

| | Pre G1-02R | Post G1-02R / this audit |
|--|-----------:|-------------------------:|
| Raw | −8 | −26 |
| Normalized | 0.42 | 0.24 |
| Class | balanced | weak |

Movement is entirely `flw_001` (−8) + `flw_005` (−10) after connecting Tỵ bản khí. No G1-02R2 code change. Dung does **not** return to 0.42.

---

## 15. Defect / no-defect conclusion

Checked against Phase B repair triggers:

| Trigger | Proven? |
|---------|---------|
| Duplicate scoring (identical meaning, no independent predicate) | **No** (印令 stack marked potential only) |
| Missing support | **No** (Huỳnh Fire is in `root_001` + peer; hidden Ấn is visible-list design) |
| Missing drain | **No** (Dung Tỵ and Huỳnh Tuất connected; Sơn residual Quý excluded) |
| Asymmetric element handling | **No** (five-element output-branch drain fires `flw_001`) |
| Wrong season mapping | **No** (Tướng / Tù / Hưu match 生克) |
| Wrong root mapping | **No** for the count model; quality-within-branch is a **documented gap** |
| Aggregation / cap bug | **No** (`flw_001` once; `flw_005` only if count ≥ 3) |

Product Owner suspicion that Sơn is “too high” is explained by **Tướng +25**, **印 lạnh +10**, light root, and officer −18 — not by illegal repeated Thổ/Kim points that we are allowed to strip without redesign. Lowering Sơn to match that suspicion is **out of scope**.

Huỳnh 0.64 is explained by **Tù −10** and drain/wealth against a **+30 root**. Raising Huỳnh is **out of scope**.

**Phase B: no repair.** No `G1_02R2_STRENGTH_REPAIR_REPORT.md` / refreeze checklist.

---

## 16. Live `/analyze` (no engine repair)

No Strength code was changed in this gate, so the API was not restarted for a repair. Confirmation used the running process on `127.0.0.1:8000`:

`POST /api/v1/analyze` with the three civil births above.

| Case | Before | After | Class | Live `raw_total` |
|------|-------:|------:|-------|-----------------:|
| Sơn | 0.87 | 0.87 | strong | 37 |
| Huỳnh | 0.64 | 0.64 | balanced | 14 |
| Dung | 0.24 | 0.24 | weak | −26 |

HTTP `data.strength` matched the in-process engine. These are not pytest-only values.

---

## Completion

**G1-02R2: CURRENT STRENGTH CALCULATION CONFIRMED — NO REPAIR**
