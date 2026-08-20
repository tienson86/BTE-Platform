# G1-02R — Strength Repair Report

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-02R Phase 2 |
| **Date** | 2026-08-20 |
| **Defect class** | A. Missing drain + D. Repeated-branch aggregation |
| **Thresholds** | Unchanged (`weak <= 0.35`, `strong >= 0.65`) |
| **Taxonomy** | Still `weak` / `balanced` / `strong` only |

---

## 1. Drain investigation

See audit Q1. Pre-repair: `drain_type=None`, `drain_count=0`, three Tỵ ignored.

Repair: count **output branches** — pillars whose earthly-branch **bản khí** is the element the Day Master produces (`Mộc→Hỏa`, so Tỵ/Ngọ count). Visible-stem drain is unchanged. Residual non-main hidden stems (e.g. Quý in Sơn’s Sửu) are **not** copied into drain lists (protects control case).

Aggregation (not `3 × −8`):

- `flw_001` −8 once if `drain_type` is output (visible **or** `output_branch_count > 0`)
- `flw_005` −10 once if `drain_count >= 3` (`drain_count` = visible output+wealth stems + output-branch count)

---

## 2. Root investigation

Vô căn −20 for Dung is correct (no Mộc in Tuất/Tỵ). Root now counts **per pillar** (repeated branches no longer collapse). Sơn still 1 chi (Sửu/Tân only).

---

## 3. Resource double-count investigation

`sup_002` + `sup_006` remain (same dual-dimension as frozen `ctl_001`+`ctl_006` on Sơn). Not repaired.

---

## 4. Seasonal-support investigation

`sea_003` Hưu +10 kept. Classification was correct. Asymmetry fixed by connecting drain, not by cutting Hưu.

---

## 5–6. Decompositions AFTER

### Đặng Thị Dung AFTER

| Category | Evidence | Rule ID | Contribution |
|----------|----------|---------|-------------:|
| Season | Hưu | sea_003 | +10 |
| Root | Vô căn | root_005 | −20 |
| Resource | Ấn type + Chính Ấn | sup_002, sup_006 | +10, +5 |
| Peer | Tỷ Kiên | sup_007 | +5 |
| Drain | 3 output Tỵ | flw_001, flw_005 | −8, −10 |
| Control | Tân Thất Sát | ctl_001, ctl_006 | −10, −8 |
| Special / combo | — | — | 0 |

Raw **−26**. Normalized `(50−26)/100 = 0.24`. Class **weak / Thân nhược**.

### Nguyễn Tiến Sơn AFTER (regression)

Identical to G1-02 freeze: raw **37**, **0.87**, **strong / Thân vượng**, drain **0**, same six rules.

---

## 7. Proven root cause (exact)

> Previous 0.42 happened because drain used only visible heavenly stems, so Ất Mộc sinh Hỏa through three Tỵ contributed 0. Connecting branch bản khí drain yields `flw_001` + `flw_005` = −18, raw −8 → −26, 0.42 → 0.24 weak.

No chart-specific hard-code. No threshold move.

---

## 8. Files / rules changed

| File | Change |
|------|--------|
| `engines/strength_engine/utils/context_builder.py` | Per-pillar hidden list; `output_branch_count`; drain_type from output branches; drain_count includes those branches; element_distribution counts repeated Tỵ |
| `engines/strength_engine/context.py` | Field `output_branch_count` |
| `engines/strength_engine/engine.py` | Trace snapshot includes drain fields |
| `tests/strength/test_g1_02r_strength_correctness.py` | Regression coverage |
| CSV thresholds / season scores | **Not changed** |

---

## 9. Before / after

### Đặng Thị Dung

| | Before | After |
|--|--------|-------|
| raw | −8 | **−26** |
| normalized | 0.42 | **0.24** |
| class | balanced / Thân cân bằng | **weak / Thân nhược** |
| drain rules | none | `flw_001`, `flw_005` |

### Nguyễn Tiến Sơn

| | Before | After |
|--|--------|-------|
| raw | 37 | **37** |
| normalized | 0.87 | **0.87** |
| class | strong / Thân vượng | **strong / Thân vượng** |

No material control-case movement.

---

## 10. Downstream (Dung)

Strength `balanced → weak` is a real Pattern/Useful God input.

| Layer | Before (0.42 balanced) | After (0.24 weak) |
|-------|------------------------|-------------------|
| Strength | 0.42 balanced | 0.24 weak |
| Pattern | (prior live balanced path) | `Sát Ấn tương sinh — Thất Sát chế bởi Chính Ấn` `com_san_01` |
| Useful God | not preserved | `Thủy · Nhâm · Chính Ấn` `sea_002` |
| Score composite | not preserved | `total_score=45.35` `grade=D` `strength_score=15.0` |
| Narrative | not preserved | `Dụng thần được chọn: Nhâm`; Thân nhược |

Sơn downstream unchanged: Chính Ấn, `Hỏa · Bính · Thất Sát` `sea_001`, score 55.05 D+, Dụng Bính.

Old Dung outputs were **not** manually kept.

---

## 11. Five-case calibration

Expected classes from **structure / 08_examples families**, not from “whatever the engine said then.”

| # | Case | Structure | After Strength | Notes |
|---|------|-----------|----------------|-------|
| 1 | Nguyễn Tiến Sơn 1987-01-21 04:30 | Tướng + 1 chi + companion; no output branch | 0.87 strong raw 37 | Control freeze |
| 2 | Đặng Thị Dung 1982-05-22 09:30 | Hưu + vô căn + 3 output Tỵ | 0.24 weak raw −26 | Suspect; drain connected |
| 3 | 1960-07-01 12:00 Canh Tý / Nhâm Ngọ / Canh Dần / Nhâm Ngọ | Tử + vô căn + output | 0.00 weak raw −58 | Clearly weak (ex_002 family) |
| 4 | 1976-04-12 10:00 Bính Thìn / Nhâm Thìn / Giáp Ngọ / Kỷ Tỵ | Tù + 2 chi + Ấn + some drain | 0.46 balanced raw −4 | Mixed, in-band |
| 5 | 1974-02-12 08:00 Giáp Dần / Bính Dần / Giáp Thân / Mậu Thìn | Đắc lệnh + 3 chi | 1.00 strong raw 77 | Additional strong (ex_001 family) |

---

## 12. Tests

`pytest tests/strength -q` → **31 passed**

New file asserts component rules (drain, root −20, overlap provenance, control+drain, Sơn freeze), not class-only.

---

## 13. Live runtime

Stale API PID 1380 (10:31) **stopped**. New uvicorn listen **PID 1136**, start **2026-08-20 11:14** (UTC 04:14), cwd workspace `.venv`.

`POST http://127.0.0.1:8081/backend/api/v1/analyze`:

| Case | Live strength | Live useful god |
|------|---------------|-----------------|
| Sơn | 0.87 strong Thân vượng | Hỏa · Bính · Thất Sát |
| Dung | 0.24 weak Thân nhược | Thủy · Nhâm · Chính Ấn |

---

## 14. V1.1 calibration backlog

- Unify type-bucket + named-star double scoring (Ấn / Quan)
- Whether residual hidden stems (non-bản khí) should drain
- Hưu +10 magnitude vs 0 / slight negative
- `rất nhược` taxonomy (out of V1.0)
- Wealth-branch drain (would move Sơn if enabled naively)

**G1-02R STATUS: STRENGTH CORRECTNESS REPAIRED — REFREEZE READY**
