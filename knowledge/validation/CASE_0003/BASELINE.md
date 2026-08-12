# CASE-0003 Validation — Baseline Output

| Field | Value |
|-------|-------|
| Case | CASE-0003 (extreme chart stress) |
| Subject | Female · Hà Nội |
| Solar birth (input) | **2015-02-15 · 05:30** · Asia/Ho_Chi_Minh |
| Lunar (stated) | 27/12/2014 |
| Stated pillars | Giáp Ngọ / Đinh Sửu / Nhâm Tuất / Quý Mão |
| Pipeline pillars | **Ất Mùi / Mậu Dần / Nhâm Tuất / Quý Mão** |
| Golden reference | CASE-0001 only |
| Rule | **No code fixes this cycle** |
| Pipeline | `ProductionEndToEndOrchestrator.run` (generic) |
| Date | 2026-08-12 |
| Success | **True** |

Hour **05:30** chosen as Mão-window so hour pillar = Quý Mão (only hour matching the stated hour pillar on this solar date).

---

## Pillar discrepancy (critical baseline fact)

| Pillar | Stated | Engine (2015-02-15 05:30) | Match |
|--------|--------|---------------------------|-------|
| Year | Giáp Ngọ | Ất Mùi | **NO** |
| Month | Đinh Sửu | Mậu Dần | **NO** |
| Day | Nhâm Tuất | Nhâm Tuất | YES |
| Hour | Quý Mão | Quý Mão | YES |

Scan note: No solar day in Dec 2014–Feb 2015 produced the full stated four-pillar set under this engine. Validation proceeds on **engine-published chart** from the birth input (extreme weak-child profile), and records the stated-vs-engine gap as an issue.

Day Master (engine): **Nhâm** (Thủy).

---

## Published engine facts

| Field | Value |
|-------|-------|
| Strength | **weak · 0.19** |
| Pattern | **Thực Thần** · tong_cach **Tòng Nhi** · than_vuong_nhuoc **Nhược** · Đắc lệnh · thân Thủy |
| Useful God | **Canh** · Favorable Canh/Tân/Nhâm · Unfavorable Giáp/Ất · “Xuân mộc vượng cần kim tiết chế” |
| Ten Gods primary | **Thương Quan** (shang_guan) · secondary includes Thất Sát |

---

## Cross-domain (CDR)

| Field | Value |
|-------|-------|
| Primary theme | `OPERATING_OUTPUT` |
| Secondary | `FOLLOW_STRUCTURE` |
| Supporting | BALANCE_DIRECTION, **CAPACITY_WEAK**, OPERATING_STANDARDS |
| Tensions | str_pattern_scope, follow_qualifies_strength, follow_strength_nuance, tg_vs_pattern_scope |
| Conflicts | **ug_drain_vs_weak** |
| Unresolved | **TRUE_CONFLICT_NEEDS_ARBITRATION** |

---

## Feature availability

| Feature | Status |
|---------|--------|
| Identity | AVAILABLE |
| Career | AVAILABLE |
| Executive | AVAILABLE |
| Domains | AVAILABLE |
| Master | NOT_AVAILABLE (policy) |
| PDF | `exports/BTE_CASE-0003_Production_E2E.pdf` |

---

## Domain conclusions (as produced)

- **Strength:** nhóm nhược — bảo toàn lực.  
- **Ten Gods:** Thương Quan (+ Thất Sát).  
- **Pattern:** Thực Thần (Tòng Nhi).  
- **Useful God:** Canh / tiết chế.

Full Identity / Career / Executive bodies in `_raw_pipeline.json`.

---

## Baseline verdict

| Artifact | Status |
|----------|--------|
| Pipeline | PASS |
| Extreme weak strength published | PASS (0.19) |
| CDR detects UG↔weak conflict | PASS |
| Stated pillars vs engine | **FAIL / mismatch** |
| Commercial fitness for minor + weak chart | **NOT READY** (see reviews) |
