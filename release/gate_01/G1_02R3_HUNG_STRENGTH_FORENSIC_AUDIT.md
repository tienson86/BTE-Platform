# G1-02R3 — Đoàn Quang Hưng Corrected-Chart Strength Forensic Audit

| Field | Value |
|-------|-------|
| **Gate** | G1-02R3 Phase A–J forensic |
| **Date** | 2026-08-20 |
| **Chart** | Tân Dậu / Đinh Dậu / Kỷ Mão / Bính Dần |
| **Day Master** | Kỷ Thổ |
| **Birth used** | 1981-08-29 04:30 male, Asia/Ho_Chi_Minh · lunar 01/08/1981 |
| **Live Strength** | **raw 11 · 0.61 · balanced / Thân cân bằng** |
| **Thresholds** | unchanged: weak `<= 0.35` · balanced `(0.35, 0.65)` · strong `>= 0.65` |
| **Phase B repair** | **none** |

Old CASE_004 “weak” used a simplified quick-score model. It is **not** an oracle. Strength weights/thresholds were not changed.

Normalization: `(raw + 50) / 100` = `(11 + 50) / 100` = **0.61**.

---

## Phase A — Exact ledger

Context:

| Field | Value |
|-------|-------|
| `month_status` | **Hưu** |
| `month_branch` / element | Dậu / **Kim** |
| `month_branch_ten_god` | **Thực Thần** (Dậu bản khí Tân) |
| `season` / phase | autumn / mid_autumn |
| `root_level` / `root_count` | Thông căn 1 chi / **1** |
| `support_type` | Ấn tinh sinh thân |
| `control_type` | Bị Thực Thương tiết |
| `drain_type` | Thực Thương tiết khí |
| `resource_elements` | Thiên Ấn, Chính Ấn |
| `output_elements` | Thực Thần |
| `officer_elements` / `wealth_elements` / `companion_elements` | empty |
| `output_branch_count` | **2** (year Dậu, month Dậu) |
| `drain_count` | **3** = `output_count 1` + `wealth 0` + `output_branch_count 2` |

Visible thập thần: year Tân **Thực Thần** · month Đinh **Thiên Ấn** · hour Bính **Chính Ấn**.

| Category | Rule ID | Exact evidence | Points | Occurrence | Overlap |
|----------|---------|----------------|-------:|------------|---------|
| Season / 月令 | `sea_003` | Kỷ Thổ sinh Dậu Kim → Hưu | +10 | 1 | — |
| Root | `root_003` | Hour Dần tàng **Mậu** Thổ (余气) | +12 | 1 pillar | — |
| Resource type | `sup_002` | `support_type` from first visible 印: month **Đinh** Thiên Ấn | +10 | 1 | not the same stem as `sup_006` |
| Resource named | `sup_006` | `resource_elements` contains **Chính Ấn** = hour **Bính** | +5 | 1 | independent stem from Đinh |
| Hidden Resource | — | Dần tàng Bính Chính Ấn | **0** | hidden | visible-list design |
| Peer | — | no visible Tỷ/Kiếp; Dần Mậu Kiếp Tài hidden only | **0** | — | — |
| Output drain presence | `flw_001` | `drain_type` from visible Tân **or** Dậu bản khí | −8 | once, not ×2 | with `ctl_002`; year 透+藏 in `drain_count` |
| Output volume | `flw_005` | `drain_count >= 3` | −10 | once | uses Tân visible + 2× Dậu |
| Wealth | — | no visible Tài | 0 | — | — |
| Officer/Killings | — | Mão Ất Thất Sát, Dần Giáp Chính Quan are **hidden only** | **0** | 0 visible | see Phase G |
| Control type (output) | `ctl_002` | first visible non-support: year Tân Thực Thần | −8 | 1 | dual-dimension with `flw_001` |
| Special | — | 月令 is Thực Thần, not 印; `spc_004` off | 0 | — | — |
| Combination | — | `officer_count=0`; `cmb_*` off | 0 | — | — |
| Caps / clamp | — | no raw clamp; `flw_005` is volume rule not a class cap | 0 | — | — |
| **Raw** | — | 10+12+10+5−8−8−10 | **11** | — | — |
| **Normalized** | — | (11+50)/100 | **0.61** | — | — |
| **Class** | `pri_level_balanced` | 0.35 < 0.61 < 0.65 | balanced | — | — |

Matched: `sea_003`, `root_003`, `sup_002`, `sup_006`, `ctl_002`, `flw_001`, `flw_005`.

Evidence compact: `Hưu khí theo tháng +10 · Có căn khí +12 · Ấn tinh sinh thân +10 · Có Chính Ấn +5 · Bị Thực Thương tiết -8 · Thực Thương tiết khí -8 · Tiết khí nặng -10`.

Check: `10 + 12 + 10 + 5 − 8 − 8 − 10 = 11`.

---

## Phase B — Four classical dimensions (engine evidence only)

No new points. Mapping of the same seven rules:

| Dimension | Engine evidence | Points |
|-----------|-----------------|-------:|
| 1. Đắc lệnh | Not 旺. `month_status=Hưu` (`sea_003`) | +10 |
| 2. Đắc địa / thông căn | 1 chi Dần/Mậu (`root_003`) | +12 |
| 3. Đắc thế / sinh trợ | Visible 印 type + named Chính Ấn (`sup_002`+`sup_006`) | +15 |
| 4. Khắc · tiết · hao | Output type + drain presence + drain volume (`ctl_002`+`flw_001`+`flw_005`). **No** scored 克 from Wood | −26 |

Peer/special/wealth/officer CSV rows: 0.

---

## Phase C — Season

| Item | Value |
|------|-------|
| Relation | Day Master **Thổ sinh** month **Kim** |
| BTE class | **休 Hưu** (not 旺 Đắc lệnh, not 相 Tướng, not 囚 Tù, not 死 Tử) |
| Rule | `sea_003` |
| Points | **+10** |
| Table | `database/12_strength/01_season_rules.csv` |
| Mapper | `_compute_month_status`: DM produces month → Hưu |

Tù would require Kỷ **khắc** Dậu (Thổ khắc Thủy). Dậu is Kim. Tử would require Dậu **khắc** Kỷ (Kim does not khắc Thổ). Đắc lệnh would require month element = Thổ. Tướng would require month sinh DM (Kim does not sinh Thổ).

**Confirmed: Hưu, +10.** Some popular 旺相休囚 lists call 土 “相” in autumn; BTE does **not**. This chart is consistent with Sơn (Tướng), Huỳnh (Tù), Dung (Hưu) on the same 生克 table. Not a mapping bug.

---

## Phase D — Root

Branches: **Dậu / Dậu / Mão / Dần**.

Earth hidden stems:

| Pillar | Branch | Hidden | Earth? |
|--------|--------|--------|--------|
| Year | Dậu | Tân only | no |
| Month | Dậu | Tân only | no |
| Day | Mão | Ất only | no |
| Hour | Dần | Giáp, Bính, **Mậu** | **yes — Mậu 余气** |

**Only Earth root:** hour Dần / hidden **Mậu**.

| Question | Answer |
|----------|--------|
| Only Earth root? | **Yes** |
| Quality in engine | Binary per pillar: any same-element hidden stem → 1 chi. **Not** 本气 vs 余气 |
| Points | `root_003` **+12** |
| Hidden Mậu full or weaker? | Treated as **full 1-chi** (+12), not `root_004` tàng-can +6 |
| Other branch wrongly as Earth? | **No.** Dậu is Kim; Mão is Mộc |

Gap (same as G1-02R2): no 本气/中气/余气 quality. Not redesigned here.

---

## Phase E — Resource

| Stem | Where | Ten-god vs Kỷ | Scored? | Points |
|------|-------|---------------|---------|-------:|
| Đinh | month visible | Thiên Ấn | `support_type` → `sup_002` | **+10** |
| Bính | hour visible | Chính Ấn | `sup_006` contains Chính Ấn | **+5** |
| Bính | Dần hidden (中气) | Chính Ấn | **no** | 0 |

`_detect_support_type` walks year → month → hour. Year Tân is output, so the first resource is **Đinh**, not Bính. Generic “Ấn sinh thân” therefore attaches to **Đinh**, not to hour Bính.

Named `sup_006` requires **Chính Ấn**, so it attaches to **Bính**, not Đinh (Thiên Ấn has no `contains` rule).

| Question | Answer |
|----------|--------|
| Points from Đinh? | **+10** (`sup_002` only) |
| Points from Bính? | **+5** (`sup_006` only) |
| Hidden Bính scored? | **No** |
| Two visible 印 independent? | **Yes** — two stems, two rules |
| Generic Ấn + named on the **same** stem? | **No** |
| Duplicate? | **No.** Legitimate two-object 印 (Thiên Ấn type vs Chính Ấn named) |

---

## Phase F — Two Dậu output drain

Kỷ Thổ sinh Kim = Thực/Thương. Dậu bản khí = Tân / Thực Thần.

| Object | Enters | Effect |
|--------|--------|--------|
| Year Dậu | `output_branch_count` +1 | — |
| Month Dậu | `output_branch_count` +1 | — |
| Year stem Tân | `output_elements` = [Thực Thần] | sets `drain_type`; `output_count=1` |
| `output_branch_count` | 2 | both Dậu counted **per pillar**, not collapsed |
| `drain_count` | 1+0+2 = **3** | `flw_005` |
| `flw_001` | once | **−8** (not 2×−8) |
| `flw_003` | no | Tân is Thực Thần, not Thương Quan |
| `ctl_002` | year Tân as `control_type` | **−8** (control bucket) |

| Question | Answer |
|----------|--------|
| Each Dậu in drain? | **Yes** — `output_branch_count=2` |
| Branch repetition capped? | **Not by unique name.** Per-pillar count. `flw_001` still once; volume via `flw_005` if count ≥ 3 |
| Tân visible separately? | **Yes** — `output_elements` and `control_type` |
| Same Tân/Dậu double-counted? | **Year 透 Tân and year 藏 Dậu both increment `drain_count`.** Two Dậu pillars are independent. Year 透+藏 toward `flw_005` is the G1-02R visible+branch sum, same dual-dimension family as 透/通根 |
| Exact Output/Drain penalty | `flw_001` **−8** + `flw_005` **−10** = **−18** drain. Plus `ctl_002` **−8** in control = **−26** weakening from Metal output |

Repeated Dậu is **not missing**. Missing-drain defect **not** proven.

---

## Phase G — Officer / Killings

| Source | Ten-god vs Kỷ | In engine? |
|--------|---------------|------------|
| Day Mão bản khí **Ất** | Thất Sát | **No** — hidden/branch; `officer_elements=[]` |
| Hour Dần bản khí **Giáp** | Chính Quan | **No** |
| Dần 中气 Bính | 印 | not officer |
| Visible stems | Tân / Đinh / Bính | output / 印 / 印 |

`control_type` is **output** (year Tân found first), not Quan Sát. `ctl_001` / `ctl_006` do **not** fire. No officer cap.

**Neither Wood control source is included.** Drain uses branch bản khí; officer does **not**. That is frozen visible-officer design (G1-02R connected **drain**, not control). Documented **gap**, not a matcher bug: rules `ctl_001`/`ctl_006` never see hidden Ất/Giáp.

Repairing by copying output-branch logic into officer would be a **new general control model** (would add Quan/Sát on this chart). Not done in this gate.

---

## Phase H — Support vs weakening (exact)

### Support side

| Item | Points |
|------|-------:|
| Season | +10 |
| Root | +12 |
| Resource | +15 |
| Peer | 0 |
| Special | 0 |
| **TOTAL** | **+37** |

### Weakening side

| Item | Points |
|------|-------:|
| Output drain (`flw_001`+`flw_005`) | −18 |
| Wealth | 0 |
| Officer/Killings | 0 |
| Other (`ctl_002` output-as-control) | −8 |
| **TOTAL** | **−26** |

Raw (CSV sum): `37 + (−26) = 11`.

Baseline is **not** inside raw:

`(raw + 50) / 100` = `(11 + 50) / 100` = **0.61**.

If written as display math: `50 + 37 − 26 = 61` → **0.61** on the 0–1 scale.

Class: **balanced**.

---

## Phase I — Old CASE_004 conceptual comparison

Do **not** import 48/86 weights.

| Structural fact | Old CASE_004 (conceptual) | BTE engine |
|-----------------|---------------------------|------------|
| Not 旺 / not in command | yes (“not in season”) | yes — **Hưu +10**, not a large minus |
| Fire/Earth support | yes | yes — Đinh/Bính 印 **+15**; Earth root Mậu **+12** |
| Strong Metal output | yes | yes — two Dậu + Tân **−18** drain and **−8** control |
| Wood control | yes (Mão/Dần) | **not scored** (hidden only) |
| Conclusion | weak | **0.61 balanced** |

Same bones except **hidden Wood 克** (BTE omits) and **Hưu as a plus** (old model treated “not in season” as weakness). Difference is **weights + visible-only 克**, not a wrong Dậu/Đinh/Tân inventory.

---

## Phase J — Defect decision

| Code | Claim | Proven? |
|------|-------|---------|
| A | Duplicate Resource scoring | **No** — Đinh `sup_002` vs Bính `sup_006` |
| B | Root over-credit | **No** relative to binary 1-chi model. Residual Mậu = full +12 is a known quality **gap**, not a wrong branch |
| C | Missing repeated-Dậu drain | **No** — both Dậu in `output_branch_count`; `flw_001`+`flw_005` |
| D | Missing Wood control | **Not a broken visible-officer rule.** Hidden Ất/Giáp omitted by design. Gap vs CASE_004 conceptual 克 |
| E | Seasonal mapping error | **No** — Hưu is the 生克 table result for Thổ sinh Kim |
| F | Asymmetric/cap bug | Drain vs officer branch-bản khí is **asymmetric by freeze**, not a failed `flw_005` cap. Year Tân+Dậu both in `drain_count` is G1-02R visible+branch summing |

**No general-rule repair.** Thresholds unchanged. Sơn / Huỳnh / Dung not recalculated for a Strength patch (none landed).

---

## Completion

**G1-02R3: 0.61 CALCULATION CONFIRMED — MODEL-WEIGHT DIFFERENCE ONLY**
