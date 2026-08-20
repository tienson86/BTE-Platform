# PAT-R1 — Special / Follow Pattern Qualification Audit

**Date:** 2026-08-20  
**Scope:** Phase 1 audit only. No repair. No Strength / Useful God / Hỷ-Kỵ / Golden / G1-FINAL change.  
**Primary case:** Ngô Đắc Dũng — Ất Sửu / Ất Dậu / Canh Thân / Canh Thìn · Nhật chủ Canh Kim.  
**Production sources:** `database/14_pattern/*.csv`, `database/13_useful_god/06_special_rules.csv`, `engines/pattern_engine`, `engines/useful_god_engine`.  
**Knowledge sources (not production matcher unless noted):** `knowledge/rule_database/04_pattern_rules/`, `knowledge/interpretation/domains/pattern/`, `database/05_phan_tich/04_cach_cuc/pha_cach.csv`.

**Live reconstruct used only to overlay authentic Strength:** civil datetime `1985-09-18 08:00` (Asia/Ho_Chi_Minh, male) produces the canonical pillars. This is a calendar reconstruction, not a biographical claim.

---

## Final status

**PAT-R1: MIXED SPECIAL-PATTERN DEFECT — REVIEW REQUIRED**

Defect class for Dũng: **E. MIXED DEFECT**

Giá Sắc on Dũng is an exact match of production rule `spe_gs_01`. That rule is LEVEL 1 and does not inspect visible Wealth, hidden Output, Officer/Killings, Strength class, or roots. Canonical project knowledge does **not** explicitly allow visible Wealth on Giá Sắc. Broader phá/tạp/broken knowledge exists and is **not** loaded by the production Pattern Engine.

---

## 1. Special / follow inventory

Production Pattern Engine loads only:

| File | Loaded into matcher? |
|------|----------------------|
| `01_main_pattern.csv` | Yes |
| `02_special_pattern.csv` | Yes |
| `03_follow_pattern.csv` | Yes |
| `04_combination_pattern.csv` | Yes |
| `05_priority_rules.csv` | **No** — metadata only (`PatternLoader.METADATA_FILES`) |
| `06_pattern_conditions.csv` | **No** — reference library |
| `07_pattern_examples.csv` | **No** |

`knowledge/rule_database/04_pattern_rules/pattern_rules.json` families `pseudo_follow`, `broken_pattern`, `mixed_pattern`, `exceptional_pattern` are **not** loaded. `SpecialPatternCalculator` / `CombinationCalculator` are leftover helpers and are **not** on the `PatternCalculator` decision path. CSV matcher is SSOT.

Empty cell below means **the production rule does not contain that predicate**. Missing conditions were not inferred.

### 1.1 Special (chuyên)

| Pattern | Token | Rule ID | Priority | Strength | Root | Support | Opposing prohibition | Visible-stem | Hidden-stem | Combination | UG consumer | Override ordinary Pattern? |
|---------|-------|---------|----------|----------|------|---------|----------------------|--------------|-------------|-------------|----------------------------|----------------------------|
| Khúc Trực | `khuc_truc` | `spe_kc_01` | 95 | — | — | — | `officer_elements == []` (visible Quan/Sát family) | DM element Mộc; month-branch element Mộc | — | — | `spc_004` | Yes |
| Viêm Thượng | `viem_thuong` | `spe_vt_01` | 95 | — | — | — | `officer_elements == []` | DM Hỏa; month Hỏa | — | — | `spc_004` | Yes |
| Nhuận Hạ | `nhuan_ha` | `spe_nh_01` | 95 | — | — | — | `officer_elements == []` | DM Thủy; month Thủy | — | — | `spc_004` | Yes |
| Giá Sắc | `gia_sac` | `spe_gs_01` | 95 | — | — | — | `output_elements == []` (visible Thực/Thương) | DM Kim; month Kim | — | — | `spc_004` | Yes |
| Giá Vượng | `jia_wang` | `spe_jw_01` | 93 | — | — | — | `officer_elements == []` | DM Thổ; month Thổ | — | — | **none** (`jia_wang` not in `spc_004`) | Yes (Pattern only) |

`officer_elements` / `output_elements` are built in `engines/pattern_engine/utils/context_builder.py` from **visible** `ten_gods_list` (BaZi heavenly stems; Nhật Chủ stripped). Hidden stems are stored on context but **are not** members of those two lists.

### 1.2 Follow (`fol_*`)

CSV rows are loose presence checks. Publication is gated in code by `FollowPatternCalculator.detect()` + `follow_token_eligible()` (G1-X01).

| Pattern | Token | Rule ID | CSV priority | CSV Strength | CSV Root | CSV Support | CSV opposing | CSV visible | CSV hidden | Combination | UG consumer | Override ordinary? |
|---------|-------|---------|--------------|--------------|----------|-------------|--------------|-------------|------------|-------------|----------------|--------------------|
| Tòng Vượng | `tong_vuong` | `fol_tv_01` | 90 | — | — | — | `ten_gods_list` not_contains Chính Quan / Thất Sát / Chính Tài / Thiên Tài | visible list only | — | — | **none** | Yes if published |
| Tòng Tài | `tong_tai` | `fol_ttai_01` | 90 | — | — | — | contains Chính Tài | visible list | — | — | `spc_001` | Yes if published |
| Tòng Sát | `tong_sat` | `fol_tsat_01` | 90 | — | — | — | contains Thất Sát | visible list | — | — | `spc_003` | Yes if published |
| Tòng Quan | `tong_quan` | `fol_tquan_01` | 90 | — | — | — | contains Chính Quan | visible list | — | — | `spc_002` | Yes if published |
| Tòng Nhi | `tong_nhi` | `fol_tnhi_01` | 90 | — | — | — | contains Thực Thần | visible list | — | — | **none** | Yes if published |
| Tòng Ấn | `tong_an` | `fol_tan_01` | 90 | — | — | — | contains Chính Ấn | visible list | — | — | **none** | Yes if published |

**Code gates (not in CSV):**

| Token family | Required Strength | Detector extra |
|--------------|-------------------|----------------|
| `tong_tai` `tong_quan` `tong_sat` `tong_nhi` `tong_an` | `weak` only | support (Tỷ/Kiếp + Ấn) / total ≤ 0.25; dominant opposing family ≥ 2 or ≥ 50% of non-support |
| `tong_vuong` | `strong` only | support / total ≥ 0.70 |
| any follow | `balanced` never | — |

Detector counts ten-god **families** from visible `ten_gods` plus year/month/hour stems plus **hidden stems**. CSV `ten_gods_list` remains visible-only. Strength-engine **root evidence is not read**.

There is **no** production token `chuyen_vuong` / Chuyên Vượng as a separate class. Tòng Vượng is `tong_vuong`. Giá Vượng is `jia_wang`.

### 1.3 Combination (`com_*`)

These can beat a single Lệnh-Tháng main Pattern. They are **not** Useful God `spc_*` tokens.

| Pattern | Token | Rule ID | Priority | Strength | Root | Support | Opposing | Visible | Hidden | Combination | UG consumer | Override ordinary Pattern? |
|---------|-------|---------|----------|----------|------|---------|----------|---------|--------|-------------|----------------------------|----------------------------|
| Quan Ấn | `quan_an` | `com_qan_01` | 85 | — | — | — | — | contains Chính Quan + Chính Ấn | — | two-god | none | Yes |
| Sát Ấn | `sat_an` | `com_san_01` | 85 | — | — | — | — | contains Thất Sát + Chính Ấn | — | two-god | none | Yes |
| Thực Thần sinh Tài | `thuc_than_sinh_tai` | `com_tttai_01` | 82 | — | — | — | — | month lệnh = Thực Thần + contains Chính Tài | — | month+list | none | Yes |
| Thương Quan phối Ấn | `thuong_quan_phoi_an` | `com_thuq_an_01` | 83 | — | — | — | — | month lệnh = Thương Quan + contains Chính Ấn | — | month+list | none | Yes |
| Tài Quan Song Mỹ | `tai_quan_song_my` | `com_taiqs_01` | 86 | — | — | — | — | contains Chính Tài + Chính Quan | — | two-god | none | Yes |

### 1.4 Other special/follow structures

| Item | Production? |
|------|-------------|
| `fol_*` | Six rows above |
| `spe_*` | Five rows above |
| `com_*` that override ordinary Pattern | Five rows above |
| Pattern tokens consumed by `spc_*` | `tong_tai`, `tong_quan`, `tong_sat`, `khuc_truc`, `viem_thuong`, `nhuan_ha`, `gia_sac` |
| `tong_nhi` `tong_an` `tong_vuong` `jia_wang` | Published by Pattern; **no** UG special row |
| Pseudo-follow / broken / mixed / exceptional in `pattern_rules.json` | Knowledge only |
| `database/05_phan_tich/04_cach_cuc/pha_cach.csv` | Knowledge / legacy analysis only |

---

## 2. Pattern → Useful God override map

`database/13_useful_god/06_special_rules.csv` plus `05_priority_rules.csv` group map.

Group priority **special = 100** (`pri_001`). Strength group = 80. Flow group = 60. Season/temperature are climate-only after UG-R2 (not Overall).

Winner sort key: `(group_priority, score, rule_priority)`.

| Pattern token | UG special rule | Rule priority | Group priority | Candidate | Hỷ | Kỵ | Overturns `str_003`/`str_004`/`str_005`? |
|---------------|-----------------|---------------|----------------|-----------|----|----|------------------------------------------|
| `tong_tai` | `spc_001` | 95 | 100 | Chính Tài | Chính Tài, Thiên Tài | Chính Ấn, Thiên Ấn | Yes |
| `tong_quan` | `spc_002` | 95 | 100 | Chính Quan | Chính Quan, Thất Sát | Tỷ Kiên, Kiếp Tài | Yes |
| `tong_sat` | `spc_003` | 95 | 100 | Thất Sát | Thất Sát, Chính Quan | Tỷ Kiên, Kiếp Tài | Yes |
| `khuc_truc` | `spc_004` | 92 | 100 | Thiên Ấn | Thiên Ấn, Chính Ấn | Chính Tài, Thiên Tài | Yes |
| `viem_thuong` | `spc_004` | 92 | 100 | Thiên Ấn | Thiên Ấn, Chính Ấn | Chính Tài, Thiên Tài | Yes |
| `nhuan_ha` | `spc_004` | 92 | 100 | Thiên Ấn | Thiên Ấn, Chính Ấn | Chính Tài, Thiên Tài | Yes |
| `gia_sac` | `spc_004` | 92 | 100 | Thiên Ấn | Thiên Ấn, Chính Ấn | Chính Tài, Thiên Tài | Yes |
| `jia_wang` | **unreachable** | — | — | — | — | — | No (Pattern can still win) |
| `tong_vuong` `tong_nhi` `tong_an` | none | — | — | — | — | — | No UG special override |
| `sat_an` `quan_an` and other `com_*` | none | — | — | — | — | — | Pattern only |

No other `spc_*` production row exists. No equivalent of `spc_004` for `jia_wang`.

Ordinary Overall (for comparison):

| Rule | Group | Group prio | Rule prio | Trigger | Token |
|------|-------|------------|-----------|---------|-------|
| `str_003` | strength | 80 | 82 | strong + officer contains Chính Quan | Chính Quan |
| `str_004` | strength | 80 | 76 | strong | Thực Thần |
| `str_005` | strength | 80 | 70 | balanced | Chính Tài |
| `flo_*` | flow | 60 | 74 | unique-max element_distribution (G1-06) | stem |

`spc_004` at group 100 always beats `str_003` (80/82) and `str_004` (80/76) and all flow.

---

## 3. Ngô Đắc Dũng — complete Pattern candidate trace

**Chart:** Ất Sửu / Ất Dậu / Canh Thân / Canh Thìn  
**Visible ten gods:** Chính Tài / Chính Tài / Nhật Chủ / Tỷ Kiên  
**Lệnh tháng:** Dậu main stem Tân → `month_branch_ten_god` = **Kiếp Tài**  
**Strength overlay:** 1.00 / `strong` (live reconstruct and stated BTE agree)  
**Follow detector:** `None`

Every enabled production rule, before winner selection:

| Rule ID | Pattern | Matched? | Evidence | Priority | Reject / discard reason |
|---------|---------|----------|----------|----------|-------------------------|
| `pat_fallback` | `chinh_quan` | Yes (empty conditions) | vacuously | 1 | `fallback_superseded` |
| `pat_cq_01` | `chinh_quan` | No | lệnh ≠ Chính Quan (is Kiếp Tài) | 80 | `conditions_not_met` |
| `pat_ts_01` | `that_sat` | No | lệnh ≠ Thất Sát | 80 | `conditions_not_met` |
| `pat_ct_01` | `chinh_tai` | No | lệnh ≠ Chính Tài | 75 | `conditions_not_met` |
| `pat_tt_01` | `thien_tai` | No | lệnh ≠ Thiên Tài | 75 | `conditions_not_met` |
| `pat_tht_01` | `thuc_than` | No | lệnh ≠ Thực Thần | 70 | `conditions_not_met` |
| `pat_thuq_01` | `thuong_quan` | No | lệnh ≠ Thương Quan | 70 | `conditions_not_met` |
| `pat_ca_01` | `chinh_an` | No | lệnh ≠ Chính Ấn | 72 | `conditions_not_met` |
| `pat_ta_01` | `thien_an` | No | lệnh ≠ Thiên Ấn | 72 | `conditions_not_met` |
| `pat_tyk_01` | `ty_kien` | No | lệnh ≠ Tỷ Kiên | 60 | `conditions_not_met` |
| `pat_ktai_01` | `kiep_tai` | **Yes** | lệnh = Kiếp Tài | 60 | survives as secondary |
| `spe_kc_01` | `khuc_truc` | No | DM ≠ Mộc | 95 | `conditions_not_met` |
| `spe_vt_01` | `viem_thuong` | No | DM ≠ Hỏa | 95 | `conditions_not_met` |
| `spe_nh_01` | `nhuan_ha` | No | DM ≠ Thủy | 95 | `conditions_not_met` |
| `spe_gs_01` | `gia_sac` | **Yes** | DM Kim + month Kim + `output_elements == []` | 95 | **winner** |
| `spe_jw_01` | `jia_wang` | No | DM ≠ Thổ | 93 | `conditions_not_met` |
| `fol_tv_01` | `tong_vuong` | No | `ten_gods_list` contains Chính Tài | 90 | `conditions_not_met` |
| `fol_ttai_01` | `tong_tai` | Yes (CSV) | contains Chính Tài | 90 | `follow_strength_incompatible` (strong) |
| `fol_tsat_01` | `tong_sat` | No | no visible Thất Sát | 90 | `conditions_not_met` |
| `fol_tquan_01` | `tong_quan` | No | no visible Chính Quan | 90 | `conditions_not_met` |
| `fol_tnhi_01` | `tong_nhi` | No | no visible Thực Thần | 90 | `conditions_not_met` |
| `fol_tan_01` | `tong_an` | No | no visible Chính Ấn | 90 | `conditions_not_met` |
| `com_qan_01` | `quan_an` | No | no Chính Quan | 85 | `conditions_not_met` |
| `com_san_01` | `sat_an` | No | no Thất Sát | 85 | `conditions_not_met` |
| `com_tttai_01` | `thuc_than_sinh_tai` | No | lệnh ≠ Thực Thần | 82 | `conditions_not_met` |
| `com_thuq_an_01` | `thuong_quan_phoi_an` | No | lệnh ≠ Thương Quan | 83 | `conditions_not_met` |
| `com_taiqs_01` | `tai_quan_song_my` | No | no Chính Quan | 86 | `conditions_not_met` |

**Published:** `gia_sac` / `spe_gs_01` / priority 95.  
**Validated peers:** `kiep_tai`, `gia_sac`.  
**Display:** `Giá Sắc cách — Nhật chủ Kim sinh tháng Kim không bị tiết` (`PATTERN_LABELS` has no `gia_sac` key; CSV description is used).

---

## 4. Why Giá Sắc matches — exact qualification

Production predicates of `spe_gs_01` (CSV + `pattern_rules.json` PAT-000015, identical):

1. `day_master_element == Kim`
2. `month_branch_element == Kim` (Dậu main stem Tân → Kim)
3. `output_elements == []`

### A–K for Dũng

| # | Question | In `spe_gs_01`? | Dũng actual |
|---|----------|-----------------|-------------|
| A | Exact predicates | the three above | all true |
| B | Day Master = Kim? | **Yes** | Canh → Kim |
| C | Month branch = Kim? | **Yes** (element of lệnh stem, not “branch name is Kim”) | Dậu → Tân → Kim |
| D | Strength = strong? | **No** | 1.00 strong (unused by this rule) |
| E | Dominant Metal ratio? | **No** | G1-05 stated Kim7; PatternContext stem+hidden count Kim5 (different field; unused by `spe_gs_01`) |
| F | Root count? | **No** | Day branch Thân contains Canh (peer/root-like); not inspected |
| G | Visible Wealth? | **No** | Ất / Ất = Chính Tài twice |
| H | Visible Officer/Killings? | **No** | none visible; `officer_elements == []` is **not** a Giá Sắc predicate |
| I | Output / Water? | Only **visible** `output_elements == []` | visible none; hidden Nhâm = Thực Thần, Quý = Thương Quan |
| J | Resource / Earth? | **No** | visible none; hidden Kỷ = Chính Ấn, Mậu = Thiên Ấn |
| K | Opposing / tiết / phá? | Only empty **visible** output | hidden tiết present; visible Wealth present; neither invalidates |

`gia_sac` is **not** the officer-empty sibling rule. Officer emptiness is required for Khúc Trực / Viêm Thượng / Nhuận Hạ / Giá Vượng, not Giá Sắc.

---

## 5. Two visible Ất Chính Tài

Year stem Ất = Chính Tài. Month stem Ất = Chính Tài. Hidden Ất in Thìn = Chính Tài.

`spe_gs_01` does **not** read `wealth_elements`, `ten_gods_list` for Tài, or hidden Ất.

Canonical Giá Sắc knowledge (`gia_sac.json`, `PATTERN_TAXONOMY.md`, `spe_gs_01` description) says: Kim DM + Kim month + **không bị tiết** / **no output**. It does **not** say visible Wealth is allowed.

**SPECIAL-PATTERN QUALIFICATION GAP: VISIBLE WEALTH NOT CONSIDERED**

The two visible Ất stems therefore cannot invalidate Giá Sắc in production, because they are never inspected.

`06_pattern_conditions.csv` contains `cond_no_ct` / `cond_no_tt` (category `special`). Those conditions are used by `fol_tv_01` (Tòng Vượng), **not** by `spe_gs_01`. Wiring them onto Giá Sắc would be a new rule, not a currently attached predicate.

---

## 6. Output / Water

G1-01 for Canh:

| Stem | Ten God |
|------|---------|
| Nhâm | Thực Thần |
| Quý | Thương Quan |

| Location | Stem | Ten God | Inspected by `spe_gs_01`? |
|----------|------|---------|---------------------------|
| Visible stems | none | — | `output_elements == []` **true** |
| Hidden Sửu | Quý | Thương Quan | **No** |
| Hidden Thân | Nhâm | Thực Thần | **No** |
| Hidden Thìn | Quý | Thương Quan | **No** |

Hidden Output is ignored by construction of `output_elements`. Documented: **hidden Output is ignored**.

If “không bị tiết” were taken as a hidden-inclusive structural claim, implementation would miss it. Production operationalizes tiết as **visible** `output_elements` only.

---

## 7. Hỏa = 0 vs Officer/Killings

G1-05 (frozen, stated): Hỏa = 0.

Giá Sắc **does not check** Officer/Killings. Absence of Hỏa / Quan / Sát is:

**not checked** (irrelevant to `spe_gs_01`).

It is not a required predicate, not recorded as favorable evidence, and not used as a break.

This audit does **not** treat Hỏa=0 as a reason to set Dụng = Hỏa.

---

## 8. Giá Sắc semantic / token

| Token | Display / title | Element | Rule |
|-------|-----------------|---------|------|
| `gia_sac` | Giá Sắc cách — chuyên **Kim** | Kim | `spe_gs_01` |
| `jia_wang` | Giá Vượng cách — chuyên **Thổ** | Thổ | `spe_jw_01` |
| `tong_vuong` | Tòng Vượng | follow Tỷ/Ấn | `fol_tv_01` |

BTE uses **A**: Giá Sắc is the Metal specialized structure.

Not B (generic strong Metal label). Not C (generic chuyên-vượng). Five chuyên tokens are distinct in CSV, taxonomy, and interpretation JSON.

Display gap: `engines/pattern_engine/labels.py` `PATTERN_LABELS` omits `gia_sac` / `jia_wang` / the other chuyên codes, so UI falls back to the CSV description string. Meaning still says Giá Sắc, not Giá Vượng. **Not** a token conflation.

`SpecialPatternCalculator.SPECIAL_PATTERNS` mixes Vietnamese chuyên names with “Tòng Vượng” / “Tòng Cường” and is unused by the matcher. Dead list; not the published SSOT.

---

## 9. Five specialized structures

| Element | Day Master | Canonical specialized pattern | Token | Rule | Qualification (production) |
|---------|------------|-------------------------------|-------|------|----------------------------|
| Mộc | Mộc | Khúc Trực | `khuc_truc` | `spe_kc_01` | month Mộc + visible officer empty |
| Hỏa | Hỏa | Viêm Thượng | `viem_thuong` | `spe_vt_01` | month Hỏa + visible officer empty |
| Thủy | Thủy | Nhuận Hạ | `nhuan_ha` | `spe_nh_01` | month Thủy + visible officer empty |
| Kim | Kim | Giá Sắc | `gia_sac` | `spe_gs_01` | month Kim + visible **output** empty |
| Thổ | Thổ | Giá Vượng | `jia_wang` | `spe_jw_01` | month Thổ + visible officer empty |

No extra specialized structures were added. Metal is the only sibling that uses output-empty instead of officer-empty. That difference is in the CSV text (“không bị tiết” vs “không bị khắc”), not a silent rename.

`jia_wang` is **not** consumed by `spc_004`. Names are not reused incorrectly. UG wiring is asymmetric.

---

## 10. Strength compatibility (G1-X01)

G1-X01 still holds on the follow path.

| Type | Required Strength (code) | CSV Strength | Can strong publish “extremely weak follow”? | Can weak publish “specialized strong”? |
|------|--------------------------|--------------|---------------------------------------------|----------------------------------------|
| Tòng Tài / Quan / Sát / Nhi / Ấn | `weak` only | none | **No** (`follow_strength_incompatible`) | N/A |
| Tòng Vượng | `strong` only | none | N/A (this is the strong-follow) | **No** |
| Balanced + any `fol_*` | never | none | No | No |
| Giá Sắc / other `spe_*` | **none** | none | N/A | **Yes, CSV allows it** — not observed in the 12 special UG winners |

Dũng: `fol_ttai_01` matched CSV and was rejected `follow_strength_incompatible`. Strong did not publish Tòng Tài.

Invariant “strong cannot publish extremely-weak follow”: **holds**.

Invariant “weak cannot publish specialized-strong unless documented”: **not documented** for `spe_*`. Production would publish Giá Sắc on a weak Kim-in-Kim-month chart with empty visible output. 101-case special UG winners did not include a weak chuyên.

---

## 11. Root / support compatibility

### Weak-follow

CSV: no root predicate.

Detector: support_ratio from ten-god families (visible + hidden). Not Strength-engine roots (`root_*`).

If support_ratio > 0.25, weak-follow returns `None`. Resource and Peer **can** invalidate follow **only through that ratio**, not via a named root-count or “meaningful Day Master root” field.

**Report:** weak-follow does **not** inspect canonical Strength root evidence. Hidden Ấn/Tỷ can still leave ratio ≤ 0.25 (see case_0021 false-positive screen).

### Specialized strong (`spe_*`)

No root, no support, no Peer/Resource invalidation.

Dũng hidden roots/support (Thân Canh, Mậu/Kỷ Ấn, hour Tỷ Kiên) are irrelevant to `spe_gs_01`.

---

## 12. Opposing-element / break-condition coverage

| Concept | Where it exists | Production Pattern identification | Class |
|---------|-----------------|-----------------------------------|-------|
| phá cách | `database/05_phan_tich/04_cach_cuc/pha_cach.csv`; interpretation examples | not loaded | **KNOWLEDGE-ONLY** |
| broken_officer_clash, broken_wealth_drain, broken_seal_break, broken_output_block, broken_season_mismatch | `pattern_rules.json` PAT-000035–039 | not loaded | **KNOWLEDGE-ONLY** |
| Pattern Evaluation `pattern_quality=broken` | `knowledge/packages/pattern/evaluation` | evaluates **published** Pattern; “Không nhận diện lại cách” | **KNOWLEDGE-ONLY** (quality, not ID) |
| Penetration / thành-phá | `engines/pattern_engine/evidence.py` | evidence only; “V1.0 does not change primary pattern” | **IMPLEMENTED** as evidence, **ABSENT** as qualifier |
| tạp khí | no production Pattern rule / token | — | **ABSENT** |
| opposing element (chuyên) | sibling `officer_elements == []`; Giá Sắc uses `output_elements == []` | visible-only | **IMPLEMENTED** (narrow) |
| Wealth breaking chuyên | not on `spe_gs_01` | — | **ABSENT** (production); condition library has no-Tài for Tòng Vượng only |
| Officer breaking Giá Sắc | not on `spe_gs_01` | — | **ABSENT** |
| Output breaking Giá Sắc | visible `output_elements == []` | hidden ignored | **IMPLEMENTED** visible-only |
| Resource contamination | not on `spe_*` | — | **ABSENT** |
| mixed structure as ID | `com_*` are extra Pattern classes | loaded | **IMPLEMENTED** as combination Pattern, not as chuyên-break |

---

## 13. Qualification depth

| Rule | Level | Why |
|------|-------|-----|
| `spe_gs_01` and other `spe_*` | **LEVEL 1** | element pair + one empty visible family list. No Strength, roots, or phá |
| `fol_*` CSV alone | **LEVEL 1** | contains / not_contains on visible list |
| `fol_*` after G1-X01 + detector | **LEVEL 2** | Strength class + support-ratio structure. Not LEVEL 3 (no canonical roots, no opposing-element phá for follow beyond family counts) |
| `com_*` | **LEVEL 1–2** | two visible ten-god tokens and/or month lệnh |
| Knowledge broken_* | would be LEVEL 2 if loaded | not production |
| Full phá/tạp/visible-hidden chuyên | **LEVEL 4** | **not implemented** |

---

## 14. Dũng fallback Pattern (counterfactual only)

If `gia_sac` / `spe_gs_01` were rejected, the remaining validated production candidate is:

**`kiep_tai` / `pat_ktai_01` / Dương Nhẫn — Lệnh tháng Kiếp Tài** (priority 60).

`pat_fallback` remains superseded. Follow stays unpublished (`tong_tai` strength-incompatible). No combination match.

**Downstream Useful God without publishing the counterfactual:**

With `special_pattern` unset, Overall candidates on this chart are:

| Rule | Group prio | Candidate |
|------|------------|-----------|
| `str_004` | 80 | Thủy · Nhâm · Thực Thần |
| `flo_003` | 60 | Hỏa · Đinh · Chính Quan |

Winner would be **`str_004` Thủy · Nhâm · Thực Thần**. `str_003` does not match (no Chính Quan, visible or hidden). `flo_003` cannot beat Strength.

Special Pattern is what moves Overall from **Thủy/Thực Thần** to **Thổ/Thiên Ấn**. It does **not** move Overall to Hỏa. Hỏa appears as:

- flow `flo_003` (Overall-ineligible vs Strength/special)
- climate `sea_004` Đinh — “Thu kim vượng cần hỏa tôi luyện” (Điều hậu, not Overall)

---

## 15. Why Thổ / Mậu wins Useful God

```
gia_sac
  → PatternResult.pattern = "gia_sac"
  → UsefulGodContext.special_pattern = "gia_sac"   (_SPECIAL_CODES)
  → spc_004 matches  special_pattern in {khuc_truc, viem_thuong, nhuan_ha, gia_sac}
  → useful_god token = Thiên Ấn
  → G1-01 Canh + Thiên Ấn → Mậu / Thổ
```

Dũng Overall candidates (live):

| Rule | Group | Group prio | Rule prio | Score | Display |
|------|-------|------------|-----------|-------|---------|
| `spc_004` | special | **100** | 92 | 0.90 | Thổ · Mậu · Thiên Ấn **winner** |
| `str_004` | strength | 80 | 76 | 0.77 | Thủy · Nhâm · Thực Thần |
| `flo_003` | flow | 60 | 74 | 0.76 | Hỏa · Đinh · Chính Quan |
| `str_003` | strength | 80 | 82 | — | **not matched** (no Chính Quan) |

Special group priority is **100** (`pri_001`). Rule priority on the winning row is **92**, not 100. Group 100 is what overturns `str_003`/`str_004`.

Matched UG rules on Dũng: `str_004`, `sea_004`, `tmp_003`, `flo_003`, `spc_004`. Climate winner `sea_004` does not become Overall (UG-R2).

---

## 16. Special Pattern Hỷ / Kỵ (HK-R1 dependency)

Published:

| Role | Tokens | G1-01 for Canh |
|------|--------|----------------|
| Dụng | Thiên Ấn | Thổ · Mậu · Thiên Ấn |
| Hỷ | Thiên Ấn, Chính Ấn | Thổ · Mậu + Thổ · Kỷ |
| Kỵ | Chính Tài, Thiên Tài | Mộc · Ất + Mộc · Giáp |

These lists are copied **directly** from the `spc_004` winner row (`favorable_gods` / `unfavorable_gods` in `06_special_rules.csv`) via `UsefulGodEngine._parse_json_list(overall.get(...))`. No separate HK calculator.

**HK-R1 dependency:** Hỷ/Kỵ of a chuyên winner are the Ấn/Tài pair on `spc_004`, not climate Fire, not flow Đinh, and not reference Hỷ Mộc+Thủy / Kỵ Kim+Thổ.

No HK repair in this audit.

---

## 17. 101-case special winners (12)

Same 12 Overall special winners as UG-R3 / UG-R3F (`spc_004` 8 + `spc_001` 3 + `spc_003` 1). Recomputed live 2026-08-20. Golden files were not edited.

| Case | Chart | Strength | Pattern | Pattern rule | UG special | Candidate | Qualification evidence |
|------|-------|----------|---------|--------------|------------|-----------|------------------------|
| case_0015 | Tân Sửu / Giáp Ngọ / Đinh Sửu / Canh Tý | 1.00 strong | `viem_thuong` | `spe_vt_01` | `spc_004` | Mộc · Ất · Thiên Ấn | DM Hỏa + month Ngọ Hỏa + visible officer empty. Visible Wealth: Thiên Tài + Chính Tài. Visible Ấn: Chính Ấn. |
| case_0021 | Tân Sửu / Canh Tý / Đinh Dậu / Nhâm Dần | 0.08 weak | `tong_tai` | `fol_ttai_01` | `spc_001` | Kim · Canh · Chính Tài | Detector `tong_tai`; visible Thiên Tài + Chính Tài + Chính Quan; lệnh Thất Sát. Hidden includes Tân=Chính Ấn, Giáp=Kiếp Tài, Bính=Tỷ Kiên. |
| case_0022 | Nhâm Dần / Nhâm Dần / Ất Dậu / Kỷ Mão | 1.00 strong | `khuc_truc` | `spe_kc_01` | `spc_004` | Thủy · Quý · Thiên Ấn | DM Mộc + month Dần Mộc + visible officer empty. Visible: two Chính Ấn + Thiên Tài. |
| case_0032 | Quý Mão / Giáp Dần / Giáp Ngọ / Quý Dậu | 1.00 strong | `khuc_truc` | `spe_kc_01` | `spc_004` | Thủy · Nhâm · Thiên Ấn | DM Mộc + month Dần Mộc + visible officer empty. Visible: Tỷ Kiên + two Chính Ấn. No visible Wealth/Output/Officer. |
| case_0057 | Ất Tỵ / Ất Dậu / Canh Ngọ / Bính Tuất | 0.95 strong | `gia_sac` | `spe_gs_01` | `spc_004` | Thổ · Mậu · Thiên Ấn | DM Kim + month Dậu Kim + visible output empty. **Visible: two Chính Tài + Thất Sát (hour Bính).** |
| case_0059 | Ất Tỵ / Đinh Hợi / Nhâm Tuất / Canh Tuất | 1.00 strong | `nhuan_ha` | `spe_nh_01` | `spc_004` | Kim · Canh · Thiên Ấn | DM Thủy + month Hợi Thủy + visible officer empty. Visible: Thương Quan + Chính Tài + Thiên Ấn. |
| case_0073 | Đinh Mùi / Giáp Thìn / Nhâm Tuất / Đinh Mùi | 0.13 weak | `tong_tai` | `fol_ttai_01` | `spc_001` | Hỏa · Đinh · Chính Tài | Detector `tong_tai`; visible two Chính Tài + Thực Thần; lệnh Thất Sát. |
| case_0077 | Đinh Mùi / Kỷ Dậu / Canh Dần / Ất Dậu | 1.00 strong | `gia_sac` | `spe_gs_01` | `spc_004` | Thổ · Mậu · Thiên Ấn | DM Kim + month Dậu Kim + visible output empty. **Visible: Chính Quan + Chính Ấn + Chính Tài.** Combination `quan_an` / `tai_quan_song_my` also validated; special still wins. |
| case_0084 | Mậu Thân / Đinh Tỵ / Bính Tý / Kỷ Hợi | 1.00 strong | `viem_thuong` | `spe_vt_01` | `spc_004` | Mộc · Giáp · Thiên Ấn | DM Hỏa + month Tỵ Hỏa + visible officer empty. Visible: Thực Thần + Kiếp Tài + Thương Quan. |
| case_0087 | Mậu Thân / Tân Dậu / Tân Sửu / Canh Dần | 1.00 strong | `gia_sac` | `spe_gs_01` | `spc_004` | Thổ · Kỷ · Thiên Ấn | DM Kim + month Dậu Kim + visible output empty. Visible: Chính Ấn + Tỷ Kiên + Kiếp Tài. Detector `tong_vuong` also validated; special wins. Hidden includes Giáp/Bính. |
| case_0093 | Kỷ Dậu / Kỷ Tỵ / Quý Tỵ / Mậu Ngọ | 0.02 weak | `tong_sat` | `fol_tsat_01` | `spc_003` | Thổ · Kỷ · Thất Sát | Detector `tong_sat`; visible two Thất Sát + Chính Quan. Hidden includes Tân/Canh Ấn. |
| case_0095 | Kỷ Dậu / Canh Ngọ / Giáp Tuất / Kỷ Tỵ | 0.16 weak | `tong_tai` | `fol_ttai_01` | `spc_001` | Thổ · Kỷ · Chính Tài | Detector `tong_tai`; visible two Chính Tài + Thất Sát; lệnh Thương Quan. |

`spc_002` (Tòng Quan): **0 / 101**.

---

## 18. False-positive screen (12)

Flag only. Not declared wrong.

| Case | Visible opposing / mix | Roots / Peer / Resource | Flag |
|------|------------------------|-------------------------|------|
| 0015 Viêm Thượng | visible Wealth (Thiên Tài + Chính Tài) + Chính Ấn | Sửu Thổ hidden; year Tân Tài | **permissive chuyên:** officer-empty ignores Wealth/Ấn |
| 0021 Tòng Tài | visible Quan + double Tài; hidden Ấn + Tỷ/Kiếp | weak 0.08; hidden support present | **permissive follow:** hidden Resource/Peer did not block ratio |
| 0022 Khúc Trực | visible Thiên Tài + double Ấn | Dần peer-season; Dậu Kim hidden | **permissive chuyên:** Wealth + Ấn ignored |
| 0032 Khúc Trực | clean visible Tỷ + Ấn | strong peer month | closer to a “same-element month” chart; still LEVEL 1 |
| 0057 Giá Sắc | **two visible Chính Tài + visible Thất Sát** | Canh in Tỵ; hour Bính Sát | **high:** same Metal-month hole as Dũng, plus Sát |
| 0059 Nhuận Hạ | visible Thương Quan + Chính Tài + Thiên Ấn | Hợi has Nhâm | **permissive:** Output+Wealth+Ấn all visible; officer-empty still passes |
| 0073 Tòng Tài | visible Output + double Tài; lệnh Sát | hidden Ấn/Quý | follow vs Sát lệnh tension; detector chose Tài |
| 0077 Giá Sắc | **visible Chính Quan + Chính Ấn + Chính Tài** | Dần Giáp/Bính/Mậu | **highest chuyên false-positive risk in 101** |
| 0084 Viêm Thượng | visible Thực + Thương + Kiếp | Tỵ Bính peer | **permissive:** Output ignored because sibling checks officer not output |
| 0087 Giá Sắc | no visible Wealth/Officer/Output; Peer+Ấn | detector tong_vuong | structurally cleaner Giá Sắc; hidden Giáp/Bính uninspected |
| 0093 Tòng Sát | visible Quan+Sát wall; hidden Ấn | 0.02 weak | follow vs hidden Ấn; ratio still allowed |
| 0095 Tòng Tài | visible Sát + double Tài | weak 0.16 | Sát present; detector still Tài |

Dũng belongs with **0057 / 0077**: Metal month + empty visible Output + **visible Wealth**, hidden Output present.

---

## 19. Reference vs BTE (after production trace)

Reference (not an oracle): Canh cực vượng · Kim dominant · Hỏa absent · Dụng Hỏa · Hỷ Mộc+Thủy (conditional) · Kỵ Kim+Thổ.

Production: Canh strong 1.00 · Giá Sắc · Dụng Thổ/Ấn · Kỵ Mộc/Tài · climate layer wants Fire.

**Reference theory:** ordinary strong-Metal balancing / control. Missing Fire is the control (Chế) the chart lacks, so Dụng is Hỏa. Wealth/Output are usable as Hỷ under that path. Resource/Peer/Metal are Kỵ.

**BTE theory:** specialized-follow-strength path.

1. Identify chuyên Kim (`spe_gs_01` LEVEL 1).
2. `spc_004` group 100 forces Overall = Thiên Ấn (support), mapped to Mậu Thổ.
3. Hỷ/Kỵ copy that Ấn/Tài row.
4. Fire is **not** Overall. It is climate `sea_004` / temperature “need warm” / ineligible flow `flo_003`.

The two theories are different engines, not a failed lookup of the same rule. This audit does **not** choose a winner.

---

## 20. Defect classification (Dũng)

**E. MIXED DEFECT**

| Piece | Class |
|-------|-------|
| Matcher vs `spe_gs_01` CSV | correct — Giá Sắc **does** match the written rule |
| Visible Wealth on chuyên Kim | **B** — qualification too permissive; knowledge does not allow it and does not forbid it; PO gap flag stands |
| Hidden Output ignored | **C vs knowledge-prose “không bị tiết”** / **by-design vs field `output_elements`** |
| Officer/Hỏa not checked | by-design of `spe_gs_01`; siblings check officer; **B** if chuyên family was meant to share “không bị khắc” |
| Strength not required for `spe_*` | **B** relative to “chuyên vượng” language; not a G1-X01 regression |
| phá/tạp/broken | **C** vs `PATTERN_DECISION_TREE` Phase 2; **KNOWLEDGE-ONLY** vs production CSV |
| Token `gia_sac` vs `jia_wang` | **not D** — meanings are distinct |
| `PATTERN_LABELS` missing chuyên keys | display gap, not token conflation |
| `jia_wang` not in `spc_004` | known UG wiring omission; out of Giá Sắc ID but part of special-family map |

Not **A** (qualification confirmed as theoretically adequate).  
Not **D** alone.

---

## 21. Minimum V1.0 repair recommendation

**Do not implement in Phase 1.**

Authoring a new “visible Wealth / hidden Output / Officer breaks Giá Sắc” predicate is **new theory** → **V1.1** unless Product Owner writes it into `database/14_pattern`.

Canonical knowledge that **is** already attached to Giá Sắc is only `spe_gs_01`. Aligning code to a richer classical chuyên Kim is not an implementation-only fix.

**Unsafe publication risk is real:** Dũng, case_0057, and case_0077 all publish `gia_sac` → `spc_004` (group 100) and overturn ordinary `str_003`/`str_004`. case_0077 even has visible Chính Quan, which would otherwise be the strong-control Overall path after UG-R3F.

**Conservative V1.0 option (recommended for freeze discussion, not coded here):**

> DO NOT publish / override Overall from an under-qualified special Pattern.  
> Fallback to the ordinary canonical Pattern (`kiep_tai` on Dũng) rather than invent new chuyên qualification.

That is a **publication-policy** change (stop `spc_004` / stop `spe_*` winning when qualification depth is LEVEL 1 and visible opposing gods exist), not a new five-element theory, and not “force Dũng → Hỏa”.

G1-X01 follow Strength gates: **keep**.  
`jia_wang` → `spc_004`: still new theory; do not wire in V1.0 under this audit.  
Hỷ/Kỵ: HK-R1.  
Golden: do not update.

---

## 22. Files / tests

Audit only. Production code, CSV, tests, Golden: **unchanged**.

Helper used for live traces then discarded: `_tmp_pat_r1_dump.py`.

---

**PAT-R1: MIXED SPECIAL-PATTERN DEFECT — REVIEW REQUIRED**

STOP. No repair. No G1-FINAL.
