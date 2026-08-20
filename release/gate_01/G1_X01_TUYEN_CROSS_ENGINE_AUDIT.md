# G1-X01 — Cross-Engine Consistency Audit

**Case:** Vũ Thị Thanh Tuyền  
**Birth used:** 1984-07-13 21:01 female, Asia/Ho_Chi_Minh · lunar **15/06/1984**  
**Canonical chart (live):** Giáp Tý / Tân Mùi / Mậu Thân / Quý Hợi  
**Day Master:** Mậu Thổ  

| Field | Live |
|-------|------|
| Strength | **0.66 / strong** (raw 16) |
| Pattern | `tong_tai` / **Tòng Tài cách — Nhật chủ cực nhược theo Tài** (`fol_ttai_01`) |
| Useful God | **Thủy · Nhâm · Thiên Tài** (`sea_002`) |
| Temperature | `hot` / Nhiệt / Cần làm mát |
| G1-05 structural FE | Mộc3 · Hỏa1 · Thổ4 · Kim3 · Thủy6 (customer occurrence model) |

Phase 1 only. **No repair implemented.** Reference report is not an oracle.

---

## 1. Strength ledger

Context: `month_status=Đắc lệnh` (Mùi Thổ = DM Thổ). `root_level=Thông căn 2 chi` (Mùi **Kỷ** 本气 + Thân **Mậu** 余气). Visible thập thần: Giáp Thất Sát · Tân Thương Quan · Quý Chính Tài. No visible 印 / Tỷ.

| Category | Rule | Evidence | Points |
|----------|------|----------|-------:|
| Season | `sea_001` | Mùi Thổ = Nhật chủ Thổ → Đắc lệnh | +35 |
| Root | `root_002` | 2 chi Thổ | +22 |
| Resource | — | `resource_elements=[]` (Đinh 印 in Mùi is hidden) | 0 |
| Peer | — | `companion_elements=[]` (Kỷ/Mậu 比劫 hidden only) | 0 |
| Drain | `flw_001` | Thân Kim bản khí = output | −8 |
| Drain named | `flw_003` | visible Tân Thương Quan | −5 |
| Drain volume | `flw_005` | `drain_count=3` | −10 |
| Wealth | — | Quý Chính Tài is wealth; `drain_type` already output so `flw_002` off | 0 |
| Officer | `ctl_001`+`ctl_006` | year Giáp Thất Sát (type + named) | −10 −8 |
| Special | — | none | 0 |
| **Raw** | | 35+22−8−5−10−10−8 | **16** |
| **Normalized** | | (16+50)/100 | **0.66** |
| **Class** | `>= 0.65` | | **strong** |

**Why 0.66:** Đắc lệnh **+35** and 2-chi root **+22** (57) beat officer+output **−41**. Hidden 印/比劫 do not enter support. This is 月令+通根 arithmetic, not “Thổ có nền” as a separate rule — but it is the same idea: Earth sits in Earth month with Earth in Mùi/Thân.

---

## 2. Pattern trace

### CSV follow rule that won

| Item | Value |
|------|-------|
| Rule ID | `fol_ttai_01` |
| File | `database/14_pattern/03_follow_pattern.csv` |
| Pattern code | `tong_tai` |
| Priority / score | 90 / 86 |
| Conditions | **`ten_gods_list` contains `Chính Tài` only** |
| Evidence | hour **Quý** = Chính Tài (visible `ten_gods_list`) |
| Strength requirement | **none** |
| Wealth requirement | contains Chính Tài (presence, not count, not 月令 Tài) |
| Root prohibition | **none** |
| Resource prohibition | **none** |

`database/14_pattern/` has **zero** `strength_level` conditions on any follow row (`fol_tv_01`, `fol_ttai_01`, `fol_tsat_01`, `fol_tquan_01`, `fol_tnhi_01`, `fol_tan_01`).

### Detector that *enables* follow CSV rows

`FollowPatternCalculator.detect` (`engines/pattern_engine/calculators/follow_pattern.py`):

- Counts ten-god **families from visible list + stems again + all hidden stems** (this chart: 15 labels; wealth=5, support same+resource=3, ratio **0.20 < 0.25**).
- Treats that ratio as “cực nhược” and returns **Tòng Tài** (dominant opposing family = wealth).
- **Does not read `StrengthResult`, `strength_level`, or `strength_score`.**

`PatternContext.strength_level` is **copied** (`strong`) and published on the result (`than_vuong_nhuoc=Thân vượng`) but **not used** in follow validation except being present on the object.

Validation (`_validation_failure`): a `follow_override` row is kept if `follow_type` is set and maps to the same `tong_*` code. `fol_ttai_01` kept; `fol_tsat_01` rejected `follow_type_mismatch`.

Other candidates this chart: `pat_ktai_01` (月令 Kiếp Tài — Mùi Kỷ), `fol_tsat_01` (contains Thất Sát). Winner `fol_ttai_01` (priority 90) over Kiếp Tài.

### Does Tòng Tài inspect canonical StrengthResult?

**NO.**

**CROSS-ENGINE BLOCKER.**

---

## 3. Pattern invariant — is strong + Tòng Tài allowed?

**Yes, current architecture permits it.** Same `PatternResult` currently holds:

- `than_vuong_nhuoc` = **Thân vượng** (from Strength)
- `cach_cuc` = **Tòng Tài cách — Nhật chủ cực nhược theo Tài**
- `tong_cach` = Tòng Tài
- `follow_type` = Tòng Tài

Why:

1. Strength and Pattern use **different weakness proxies** (score vs hidden-inclusive 十神 ratio).
2. Follow CSV does not constrain `strength_level`.
3. Priority prefers follow override (90) over 月令 Kiếp Tài once `detect()` returns Tòng Tài.

This is not “both engines independently correct so the pair is consistent.” The **customer labels contradict**.

---

## 4. Five Elements vs Useful God

| Model | Counts | Role |
|-------|--------|------|
| G1-05 structural (stem + branch bản khí + hidden occurrence) | **Mộc3 Hỏa1 Thổ4 Kim3 Thủy6** | occurrence display only |
| Pattern/UG `element_distribution` (visible+hidden stems in strength/pattern builder) | Mộc3 Hỏa1 Thổ3 Kim2 Thủy4 | `flo_*` matching |

Useful God **does not** treat Thủy6 as “strength.”

Matched UG flow rule `flo_004`: `element_distribution contains Thủy` → token **Mậu** (“Thủy quá thịnh cần thổ chế”). Group **flow**, priority 60 — **loses**.

Winner `sea_002` conditions: `season==summer` AND `temperature_type==hot` → **Nhâm**. No water-count field.

---

## 5. Useful God candidates (all)

UG `follow_pattern` on context = **`Tòng Tài`** (Vietnamese `follow_type` string).

Special `spc_001` wants `follow_pattern == tong_tai`. **Does not match.** Tòng Tài override never enters the candidate list.

| Rule | Group | Pri | Token | Stem | Element | Ten God | Match reason |
|------|-------|----:|-------|------|---------|---------|--------------|
| `str_004` | strength | 76 | Thực Thần | Canh | Kim | Thực Thần | `strength_level==strong` — thân vượng cần tiết |
| `sea_002` | season | 88 | Nhâm | Nhâm | Thủy | Thiên Tài | summer + hot — hạ nhiệt cần thủy |
| `tmp_002` | temperature | 86 | Quý | Quý | Thủy | Chính Tài | `temperature_type==hot` — nhuận hạ |
| `flo_004` | flow | 74 | Mậu | Mậu | Thổ | Tỷ Kiên | dist contains Thủy — thủy thịnh cần thổ |

Winner: **`sea_002`** because group priority **season 90 > strength 80 > temperature 70 > flow 60**.

**Nhâm wins from season/climate (điều hậu), not from Tòng Tài, not from Thủy6, not from Strength tiết khí.**

Enrichment: Nhâm vs Mậu = **Thiên Tài / Thủy** (G1-01). Display `Thủy · Nhâm · Thiên Tài`.

Hỷ/Kỵ from that row: favor Nhâm/Quý/Canh; avoid Bính/Đinh. **Not** the reference Mộc / Thủy-conditional / Kỵ Thổ-Hỏa set.

---

## 6. Reconciliation truth table

| Engine | Says | Assumes |
|--------|------|---------|
| **Strength** | 0.66 **strong** / Thân vượng | 月令 Earth + 2 Earth roots outweigh 克/tiết |
| **Pattern** | **Tòng Tài** / Nhật chủ **cực nhược** theo Tài | 十神 family ratio (hidden-heavy) + `contains Chính Tài`; **ignores Strength** |
| **Temperature** | **hot** / Nhiệt / Cần làm mát | Mùi summer heat (`cli_001`) |
| **Useful God** | **Nhâm thủy** (điều hậu hạ nhiệt) | `follow_pattern` is **not** `tong_tai`, so no Tài-follow override; season+hot beats `str_004` Thực Thần |

**Semantic contradictions (same chart, same payload):**

1. **Thân vượng** vs **cực nhược theo Tài**.
2. Pattern **Tòng Tài** vs UG **not** `spc_001` Chính Tài — wiring: `Tòng Tài` ≠ `tong_tai`.
3. Strength-strong UG path (`str_004` tiết Kim) exists but **loses to** summer-water `sea_002`.
4. G1-05 **Thủy6** vs UG flow that would **control** water (`flo_004` Mậu) — unused; winner **adds** water.

---

## 7. Tòng / follow safety (no repair)

| Pattern | Detector | CSV condition | Strength gate? |
|---------|----------|---------------|----------------|
| Tòng Tài | support_ratio ≤ 0.25, wealth dominant | `contains Chính Tài` | **No** |
| Tòng Sát | same, killing dominant | `contains Thất Sát` | **No** |
| Tòng Quan | officer dominant | `contains Chính Quan` | **No** |
| Tòng Nhi | output dominant | `contains Thực Thần` | **No** |
| Tòng Ấn | (only if support_ratio already ≤ 0.25 — rare with 印 in support) | `contains Chính Ấn` | **No** |
| Tòng Vượng | support_ratio ≥ 0.70 | **not_contains** Quan/Sát/Tài | **No** |

None require `strength_level == weak` (or forbid `strong`).  
`FollowPatternCalculator` never reads StrengthResult.  
This chart is the live proof: **strong + Tòng Tài**.

---

## 8. Mộc vs Thủy (after traces)

| | Old reference | BTE live |
|--|---------------|----------|
| Useful God | **Mộc** | **Thủy / Nhâm / Thiên Tài** |
| Hỷ | Thủy có điều kiện | Nhâm, Quý, Canh (from `sea_002`) |
| Kỵ | Thổ / Hỏa | Bính, Đinh |

**Why BTE chooses Thủy:** Mùi = summer + `temperature_type=hot` → `sea_002` Nhâm. Highest matching **group** is season. Tòng Tài special never matched. Structural Thủy6 did not pick the winner.

**Why a Mộc reference can exist (conceptual, not imported):** for Mậu, Mộc is Quan/Sát (year Giáp already 克). Some 调候/扶抑 books drain or control a “hot Earth in late summer” via Wood, or use Wood as 用神 when treating the chart as weak/follow. That is a **different assumption set** (weak/tòng vs BTE strong+heat).

Do not adopt the old report as winner. The contradiction to fix first is **strong vs cực nhược** and **Tòng Tài vs season Nhâm**, not Mộc vs Thủy as a taste choice.

---

## 9. Decision

**A. CROSS-ENGINE DEFECT PROVEN — REPAIR REQUIRED**

Not “two valid theory models sitting quietly side by side.” The product publishes **Thân vượng** and **Nhật chủ cực nhược** together, and Pattern’s Tòng Tài **does not consume** Strength.

### Proposed minimal invariant (do **not** implement until Product Owner review)

1. **Follow safety (Pattern):** reject `fol_*` / `FollowPatternCalculator` follow labels when canonical `strength_level == strong` (PO may also exclude `balanced`). Optionally require `weak` for Tòng Tài/Quan/Sát/Nhi. Tòng Vượng should require `strong`, not a separate 十神-only ratio.
2. **Token SSOT (Useful God):** when copying `follow_type`, map `Tòng Tài` → `tong_tai` (same table Pattern already has). Then `spc_001` can actually fire **if** follow remains the pattern.
3. **Do not** retune Strength to 0.66→weak to make Tòng Tài true. Strength ledger is internally consistent.
4. **Do not** pick Mộc from the reference PDF.

PO must choose whether Tòng Tài is allowed only when Strength is weak, or Strength should be ignored (then stop printing “cực nhược” next to Thân vượng).

---

## Completion

**G1-X01: CROSS-ENGINE DEFECT PROVEN — REPAIR REQUIRED (not implemented)**

No G1-FINAL.
