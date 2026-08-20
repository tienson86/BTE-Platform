# G1-02R — Strength Refreeze Checklist

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-02R |
| **Date** | 2026-08-20 |
| **Prior freeze** | G1-02 CASE-0001 0.87 / strong **preserved** |

---

## Invariants

| # | Invariant | Status |
|---|-----------|--------|
| 1 | Same input → same Strength | PASS (pytest + live 8081) |
| 2 | No duplicate evidence without explicit reason | Dual-dimension Ấn/Quan **documented**, not newly added |
| 3 | Every contribution has provenance | Rule IDs on evidence_compact |
| 4 | Drain cannot vanish only because source is hidden | PASS — branch bản khí drain |
| 5 | Repeated structures: documented aggregation | Per-pillar count; `flw_001` once + `flw_005` if ≥3; **not** 3×−8 |
| 6 | Root ≠ season | Unchanged |
| 7 | Score 0–1 | Unchanged baseline/scale |
| 8 | Classification boundaries unchanged | 0.35 / 0.65 |
| 9 | Confidence ≠ score | Unchanged |
| 10 | Score Engine composite separate | Sơn 55.05 D+ vs Điểm thân 0.87 |

---

## Must remain frozen (G1-02 control)

- Nguyễn Tiến Sơn: raw 37, **0.87**, **strong**, Thân vượng, drain 0
- Taxonomy three classes only
- `cfg_weak_threshold` 0.35 / `cfg_strong_threshold` 0.65
- Season CSV scores (`sea_003` Hưu +10 included)

## Newly frozen (G1-02R)

- Đặng Thị Dung (Nhâm Tuất / Ất Tỵ / Ất Tỵ / Tân Tỵ): raw **−26**, **0.24**, **weak**
- Drain from output-branch bản khí + `flw_005` volume cap
- Residual tàng can **not** in drain lists

---

## Sign-off

- [x] Forensic Q1–Q4 recorded
- [x] Defect proven (missing drain)
- [x] Repair is general (context builder)
- [x] Control case unmoved
- [x] Five-case calibration table
- [x] `tests/strength` 31 passed
- [x] Live API restarted (PID 1136) and 8081 smoke both cases
- [ ] Product Owner live `/result` confirm Dung Thân nhược 0.24

---

G1-02R STATUS: STRENGTH CORRECTNESS REPAIRED — REFREEZE READY

Stop. Do not start G1-FINAL. Do not start Gate 2.
