# G1-02R — Strength Correctness Revalidation Audit

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-02R Phase 1 forensic |
| **Date** | 2026-08-20 |
| **Control** | Nguyễn Tiến Sơn — Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần |
| **Suspect** | Đặng Thị Dung — Nhâm Tuất / Ất Tỵ / Ất Tỵ / Tân Tỵ |
| **Civil date used for Dung** | 1982-05-22 09:30 (same pillars; also 2042-05-07 09:30) |

Phase 1 ran **before** repair. Numbers below are the **pre-repair** engine (drain_type from visible stems only).

---

## Q1 — Drain / tiết hao (Đặng Thị Dung)

Nhật chủ **Ất Mộc** sinh **Hỏa**. Chart has **three Tỵ**. Tỵ bản khí = **Bính / Hỏa**. Main ten-god vs Ất = **Thương Quan**.

| Source | Ten-god vs Ất | Entered drain? |
|--------|---------------|----------------|
| Visible year Nhâm | Chính Ấn | no (resource) |
| Visible month Ất | Tỷ Kiên | no (peer) |
| Visible hour Tân | Thất Sát | no (officer) |
| Tỵ ×3 bản khí Bính | Thương Quan | **NO** |
| Tỵ hidden Bính | Thương Quan | **NO** |
| Tỵ hidden Mậu | Chính Tài | **NO** |
| Tỵ hidden Canh | Chính Quan | **NO** |
| Tuất hidden Đinh | Thực Thần | **NO** (residual) |

Context before repair:

- `drain_type = None`
- `output_elements = []`
- `output_count = 0`
- `drain_count = 0`
- `drain_matches = []`

Rules that **would** fire if drain were connected (`05_flow_rules.csv`):

| Rule | Condition | Score |
|------|-----------|------:|
| `flw_001` | `drain_type == Thực Thương tiết khí` | −8 |
| `flw_003` | `output_elements contains Thương Quan` | −5 |
| `flw_005` | `drain_count >= 3` | −10 |

**Caps:** none applied because nothing matched. Drain was **zero**.

**Repeated Tỵ:** `hidden_by_branch` was a **dict keyed by branch name**, so three Tỵ collapsed to one entry. Element distribution undercounted Hỏa/Thổ/Kim. Drain still would have been zero even with one Tỵ, because drain looked only at **visible heavenly stems**.

### CALCULATION BLOCKER

Three Tỵ / Hỏa / Thương Quan were structurally present and **absent from Strength weakening**. Drain cannot disappear merely because the output sits in địa chi / tàng can chính khí.

---

## Q2 — Root / thông căn

Hidden stems by pillar:

| Pillar | Branch | Hidden | Contains Mộc? |
|--------|--------|--------|---------------|
| Year | Tuất | Mậu, Tân, Đinh | no |
| Month | Tỵ | Bính, Mậu, Canh | no |
| Day | Tỵ | Bính, Mậu, Canh | no |
| Hour | Tỵ | Bính, Mậu, Canh | no |

`root_level = Vô căn`, `root_count = 0`, rule `root_005` **−20**.

No Mộc root. Vô căn is a **flat −20**; it does not multiply drain/control. Interaction is additive only (raw sum).

---

## Q3 — Resource double counting

| Rule | Score | Evidence object |
|------|------:|-----------------|
| `sup_002` Ấn tinh sinh thân | +10 | `support_type` from **first** visible resource stem: year **Nhâm** |
| `sup_006` Có Chính Ấn | +5 | `resource_elements` contains `Chính Ấn` — same year **Nhâm** |
| `sup_007` Có Tỷ Kiên | +5 | month stem **Ất** (different object) |

`sup_002` + `sup_006` share **one stem**. Same dual-dimension pattern as frozen officer on Sơn: `ctl_001` (−10, control_type) + `ctl_006` (−8, contains Thất Sát) on year **Bính**.

**Verdict:** treated as **intended V1.0 dual dimension** (mechanism vs named star), not repaired here. Unifying it would require revisiting Sơn’s frozen −18 control. Logged as V1.1 backlog.

Peer `sup_007` is independent (month Ất ≠ year Nhâm).

---

## Q4 — Seasonal support

| Item | Value |
|------|-------|
| Rule | `sea_003` |
| Table | `database/12_strength/01_season_rules.csv` |
| Category | 旺相休囚死 — **休 Hưu** |
| Why +10 | Month Tỵ bản khí Hỏa; Ất Mộc **sinh** Hỏa → `month_status = Hưu` |
| Not | Đắc lệnh (same element), Tướng (month sinh DM), Tử (month khắc DM) |

Seasonal Hỏa is **the same relation as drain** (DM produces month). Before repair, `sea_003 +10` existed and **seasonal/branch drain was omitted**. That asymmetry is the Q1 blocker, not a misclassification of Hưu.

Hưu magnitude +10 is **not** changed (not a threshold/class fix).

---

## Phase 1B — Đặng Thị Dung decomposition (BEFORE)

Raw **−8**. Normalized `(50 − 8) / 100 = 0.42`. Class **balanced / Thân cân bằng**.

| Category | Evidence | Rule ID | Contribution | Repeated? | Notes |
|----------|----------|---------|-------------:|-----------|-------|
| Season | Hưu, Tỵ/Hỏa | sea_003 | +10 | no | 休, not đắc lệnh |
| Root | no Mộc in 4 branches | root_005 | −20 | no | flat vô căn |
| Visible support | year Nhâm → support_type Ấn | sup_002 | +10 | overlaps sup_006 | year stem |
| Resource named | Chính Ấn in list | sup_006 | +5 | same Nhâm | dual-dimension |
| Peer | month Ất Tỷ Kiên | sup_007 | +5 | no | independent |
| Hidden support | — | — | 0 | | not in visible lists |
| Output/drain | 3× Tỵ Thương Quan | — | **0** | **omitted** | **BLOCKER** |
| Wealth drain | Tỵ Mậu / Tuất Mậu | — | 0 | | residual/hidden; not modeled as visible wealth |
| Officer | hour Tân Thất Sát | ctl_001 | −10 | with ctl_006 | control_type |
| Killings named | contains Thất Sát | ctl_006 | −8 | same Tân | dual-dimension |
| Combinations | — | — | 0 | | cmb_* not matched |
| Special | — | — | 0 | | |
| Caps | — | — | 0 | | flw_005 never reached |
| Normalization | baseline 50 / scale 100 | cfg_* | 0.42 | | thresholds 0.35 / 0.65 unchanged |

---

## Control comparison (BEFORE)

| Component | Nguyễn Tiến Sơn | Đặng Thị Dung |
|-----------|----------------:|--------------:|
| Season | Tướng +25 (`sea_002`) | Hưu +10 (`sea_003`) |
| Root | 1 chi Sửu/Tân +12 (`root_003`) | Vô căn −20 (`root_005`) |
| Resource/support | Đồng hành +8 (`sup_001`); no Chính Ấn presence | Ấn +10 + Chính Ấn +5 + Tỷ Kiên +5 = +20 |
| Peer | in support_type Kiếp Tài | Tỷ Kiên +5 |
| Drain/output | **0** (no output branch) | **0 (omitted; 3 Tỵ present)** |
| Control | −10 −8 = −18 | −10 −8 = −18 |
| Special | Ấn mùa lạnh +10 (`spc_004`) | 0 |
| Raw | **37** | **−8** |
| Normalized | **0.87 strong** | **0.42 balanced** |

---

## Proven root cause

**Strength V2 set `drain_type` only from visible heavenly-stem thập thần.**  
Branch bản khí and tàng can chính khí never entered `05_flow_rules.csv`. For Ất Mộc, three Tỵ are output and scored **nothing**.

This is a general engine defect (missing drain / wrong aggregation of repeated output branches), not a request to force a “weak” label.

Repair is documented in `G1_02R_STRENGTH_REPAIR_REPORT.md`.
