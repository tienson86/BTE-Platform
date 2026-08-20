# PAT-R1F — Special Override Safety Repair Report

**Date:** 2026-08-20  
**Status:** **PAT-R1F: UNDER-QUALIFIED SPECIAL OVERRIDE DISABLED — PATTERN V1.0 REFREEZE READY**  
**Golden Dataset:** not updated.

---

## Product Owner decision implemented

LEVEL-1 chuyên Pattern remains **detected**. It no longer grants Overall Useful God override (`spc_*`).

No new Giá Sắc / chuyên-vượng / phá-cách theory was authored.

---

## 1. Detection kept

Unchanged production rules:

- `database/14_pattern/02_special_pattern.csv` (`spe_gs_01` `gia_sac` and siblings)
- Pattern winner token, `winning_rule_id`, CSV description, candidate/validated lists

Ngô Đắc Dũng still publishes `pattern = gia_sac` / `spe_gs_01`.

---

## 2. Qualification authority

SSOT: `engines/pattern_engine/override_eligibility.py`

| State | Meaning |
|-------|---------|
| Detected | Pattern token may be the canonical winner |
| `ug_override_eligible` | Whether `spc_*` may enter Overall competition |

Published on `PatternResult` / `PatternView`:

- `ug_override_eligible`
- `qualification_level` (`1` chuyên, `2` published follow, omitted for ordinary)
- `detected_special_pattern`

Useful God context keeps the detected token in **metadata only**. Matcher `special_pattern` is **not** set for LEVEL-1.

---

## 3. Consumer inventory and V1.0 decision

| Consumer | Token / rule | Qualification | Overall `spc_*` V1.0 |
|----------|--------------|---------------|----------------------|
| Khúc Trực | `khuc_truc` `spe_kc_01` → `spc_004` | LEVEL 1 | **Suppressed** |
| Viêm Thượng | `viem_thuong` `spe_vt_01` → `spc_004` | LEVEL 1 | **Suppressed** |
| Nhuận Hạ | `nhuan_ha` `spe_nh_01` → `spc_004` | LEVEL 1 | **Suppressed** |
| Giá Sắc | `gia_sac` `spe_gs_01` → `spc_004` | LEVEL 1 | **Suppressed** |
| Giá Vượng | `jia_wang` `spe_jw_01` (not in `spc_004`) | LEVEL 1 | **Suppressed** (was already unwired) |
| Tòng Tài | `tong_tai` `fol_ttai_01` → `spc_001` | LEVEL 2 (G1-X01) | **Preserved** |
| Tòng Quan | `tong_quan` `fol_tquan_01` → `spc_002` | LEVEL 2 | **Preserved** (0/101 live) |
| Tòng Sát | `tong_sat` `fol_tsat_01` → `spc_003` | LEVEL 2 | **Preserved** |
| Tòng Nhi / Tòng Ấn / Tòng Vượng | no `spc_*` row | LEVEL 2 if published | no UG special row |
| Combination `com_*` | no `spc_*` | ordinary Pattern | unchanged |

G1-X01 is unchanged: weak-follow only when `weak`; Tòng Vượng only when `strong`; token canonicalization preserved.

---

## 4. `spc_*` gate

Before special-stage matching:

1. Canonical Pattern winner is classified.
2. `run_special_case_stage` runs only when `resolve_context_override_eligible` is true.
3. LEVEL-1 never copies `special_pattern` onto `UsefulGodContext`.

No Useful God **priority** numbers were changed. `spc_004` simply does not enter the candidate list.

Unset synthetic contexts with a follow token remain eligible (G1-X01 tests).

---

## 5. Ngô Đắc Dũng (fresh)

Reconstruct that yields the canonical pillars: **1985-09-18 08:00** male (calendar reconstruction, not a biographical claim).

| Field | Result |
|-------|--------|
| Chart | Ất Sửu / Ất Dậu / Canh Thân / Canh Thìn |
| Strength | **1.00 / strong** |
| Pattern token | `gia_sac` (`spe_gs_01`) |
| Display | `Cấu trúc đặc biệt được nhận diện: Giá Sắc` |
| Override eligible | **false** (LEVEL 1) |
| Overall | **`str_004` Thủy · Nhâm · Thực Thần** |
| Hỷ | Thực Thần / Thương Quan (Nhâm / Quý) |
| Kỵ | Tỷ Kiên / Kiếp Tài (Canh / Tân) |
| Reasoning | `Than vượng cần tiết khí` (not `Chuyên cách ưu tiên Ấn`) |
| `spc_004` in Overall | **absent** |
| Điều hậu | `sea_004` Hỏa · Đinh · Chính Quan (climate-only) |

Hỏa was **not** forced as Overall. Ordinary structural selection produced `str_004`. `str_003` does not match (no Chính Quan).

---

## 6. Customer wording

LEVEL-1 chuyên `cach_cuc`:

`Cấu trúc đặc biệt được nhận diện: {Khúc Trực|Viêm Thượng|Nhuận Hạ|Giá Sắc|Giá Vượng}`

Follow labels unchanged (`Tòng Tài`, …).

Narrative Useful God composer appends published `reasoning` from the **actual Overall winner**.

---

## 7. Hỷ / Kỵ

Copied from the Overall winner row. Dũng no longer publishes stale `spc_004` Ấn/Tài (Mậu/Kỷ vs Ất/Giáp). HK-R1 remains a separate audit.

---

## 8. Files changed

| File | Change |
|------|--------|
| `engines/pattern_engine/override_eligibility.py` | **new** SSOT classification |
| `engines/pattern_engine/labels.py` | detected chuyên wording |
| `engines/pattern_engine/calculator.py` | publish eligibility on winner |
| `engines/pattern_engine/engine.py` | PatternResult fields + display |
| `engines/pattern_engine/rule_context_bridge.py` | `cach_cuc` uses eligibility |
| `engines/useful_god_engine/context.py` | `ug_override_eligible` |
| `engines/useful_god_engine/utils/context_builder.py` | do not feed LEVEL-1 to matcher |
| `engines/useful_god_engine/calculators/special_case.py` | eligibility gate |
| `engines/useful_god_engine/engine.py` | snapshot metadata |
| `applications/api/models/analysis_result.py` | PatternView fields |
| `applications/api/services/pattern_truth.py` | copy fields |
| `tests/useful_god/test_pat_r1f_special_override_gate.py` | **new** module tests |

Not changed: Strength, ordinary Pattern CSV, Five Elements, Temperature, Điều hậu rules, `str_003`/`str_004`/`str_005`, Flow, UG priorities, Month Pillar, Ten Gods, ShenSha, Luck, Golden.

---

## 9. Tests

```
pytest tests/useful_god tests/pattern -q
59 passed
```

Includes G1-X01 follow Strength gate + token normalization + new PAT-R1F Dũng gate.

---

## 10. Live API

Stopped previous listener on `127.0.0.1:8000` (PID 7624). Started:

```
.\.venv\Scripts\python.exe -m uvicorn applications.api.app:app --host 127.0.0.1 --port 8000 --log-level info
```

Uvicorn child PID **8068**, `Application startup complete`. No `--reload`. Fresh `POST /api/v1/analyze` for the Dũng reconstruct (not `bte_last_result` / ResultStore).

| Check | Live HTTP Analyze |
|-------|-------------------|
| Strength | `1.0` / `strong` |
| Pattern | `gia_sac` / `spe_gs_01` / LEVEL 1 / `ug_override_eligible=false` |
| Display | `Cấu trúc đặc biệt được nhận diện: Giá Sắc` |
| Overall | `str_004` Thủy · Nhâm · Thực Thần |
| Reasoning | `Than vượng cần tiết khí` |
| Hỷ / Kỵ | Thực Thần·Thương Quan (Nhâm/Quý) vs Tỷ Kiên·Kiếp Tài (Canh/Tân) |
| Climate | `sea_004` Hỏa · Đinh · Chính Quan |
| `spc_004` in Overall | **absent** (candidates: `str_004`, `flo_003`) |
| `Chuyên cách ưu tiên Ấn` | **absent** from Analyze / Narrative / Report V1 |
| Interpretation Dụng | `Thực Thần` (not Thiên Ấn) |

Report V1 (same `ReportInputV1` as PDF/DOCX):

- Pattern Cách chính = detected Giá Sắc wording
- Dụng / Hỷ / Kỵ / reasoning = `str_004`
- Residual Pattern **Trạng thái = Đắc cách** is the Pattern-engine match flag (rule fired), not Useful God override authority. Knowledge `gia_sac.json` was not rewritten (V1.1 semantic review).

PDF exported from that input (`~154 KB`, 7 pages). HTML + DOCX contain the same Overall/Hỷ/Kỵ/wording. ResultStore is browser-only; a new Analyze overwrites it.

---

**PAT-R1F: UNDER-QUALIFIED SPECIAL OVERRIDE DISABLED — PATTERN V1.0 REFREEZE READY**
