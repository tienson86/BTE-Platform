# UG-R3F — Existing-knowledge reachability repair

**Date:** 2026-08-20  
**Scope:** Useful God context construction only.  
**Not in scope:** new theory, CSV token/priority edits, Golden Dataset, G1-FINAL.

## Status

**`UG-R3F: EXISTING-KNOWLEDGE REACHABILITY REPAIRED — USEFUL GOD V1.0 FREEZE READY`**

Do **not** start G1-FINAL. Do **not** update Golden.

---

## What was repaired

`str_003` already said: **strong + `officer_elements contains Chính Quan` → Chính Quan (Chế).**

The matcher was correct. Pattern `officer_elements` was built from **visible** stems only, so canonical hidden Chính Quan (G1-01 / `database/09_hidden_stems`) never reached the condition.

### Fix

In `build_useful_god_context` only:

- Keep Pattern `officer_elements` **visible-only** (Pattern specials such as `jia_wang` / `khuc_truc` still see the old lists).
- Map hidden stems with G1-01 `ten_god_name`.
- If hidden Chính Quan exists and the token is not already present, append **`Chính Quan` once**.
- Store `officer_provenance` (`visible` / `hidden`, pillar, stem, branch).
- Do **not** add Thất Sát to `str_003`.
- Do **not** change `str_003` token, score, or priority (82).

Visible + hidden of the same Ten God does **not** publish a second `str_003` candidate. 101-case `str_003` publication count never exceeded 1.

---

## 1. `str_003` — hidden Chính Quan reachability

| Item | Value |
|------|--------|
| Rule | `str_003` unchanged |
| Token | `Chính Quan` only |
| Priority | 82 / strength group 80 |
| Visible | already in Pattern `officer_elements` |
| Hidden | now copied onto Useful God `officer_elements` with provenance |
| Thất Sát | not added to the rule |

Tuyền evidence: Mùi hidden **Ất**; Mậu × Ất = **Chính Quan**. Provenance: `hidden / month / Ất / Mùi / g1_01_hidden_stem`.

---

## 2. Vũ Thị Thanh Tuyền — natural re-evaluation

Chart: **Giáp Tý / Tân Mùi / Mậu Thân / Quý Hợi**. Strength **0.66 strong**. Pattern **Kiếp Tài**. Hidden Mùi **Ất = Chính Quan**.

| | Before (UG-R2) | After (UG-R3F) |
|--|----------------|----------------|
| `officer_elements` (UG) | `['Thất Sát']` | `['Thất Sát', 'Chính Quan']` |
| `str_003` eligible | no | **yes** |
| Overall winner | `str_004` | **`str_003`** |
| Display | Kim · Canh · Thực Thần | **Mộc · Ất · Chính Quan** |
| Hỷ | Thực Thần, Thương Quan | **Chính Quan, Thực Thần** |
| Kỵ | Tỷ Kiên, Kiếp Tài | Tỷ Kiên, Kiếp Tài (from `str_003`, not stale `str_004`) |
| Điều hậu | `sea_002` Thủy · Nhâm · Thiên Tài | **unchanged** |

### Candidates (Overall + climate)

| Candidate | Layer | Priority (row / group) | Evidence | Winner? |
|-----------|-------|------------------------:|----------|---------|
| `str_003` | overall | 82 / 80 | strong + hidden Chính Quan (Mùi Ất) | **Overall** |
| `str_004` | overall | 76 / 80 | strong fallback Tiết | no |
| `flo_004` | overall | 74 / 60 | unique-max Thủy | no (non-competitive vs Strength) |
| `sea_002` | climate | 90 / 90 | summer → Thủy | **Điều hậu only** |

Existing priority makes `str_003` win. **Accepted.** Mộc is the G1-01 mapping of Chính Quan for Mậu, not a hard-coded Mộc rule.

---

## 3. `jia_wang` → `spc_004` — **not wired**

Intended `spc_004` condition is documented as an explicit four-code `in` list, not “any special_pattern field.”

| Source | Codes |
|--------|--------|
| `database/13_useful_god/06_special_rules.csv` `spc_004` | `khuc_truc`, `viem_thuong`, `nhuan_ha`, `gia_sac` |
| `database/13_useful_god/08_rule_conditions.csv` `cond_010` | same four — “Chuyên cách thường dùng” |
| `knowledge/rule_database/05_special_case_rules/special_case_rules.json` `ug_spc_004` / SPC-000019 | same four |

`jia_wang` **is** a Pattern chuyên token (`spe_jw_01`, Giá Vượng) and **is** published onto `UsefulGodContext.special_pattern` via `_SPECIAL_CODES`. That is a **field**, not a rule clause.

**Decision:** do **not** add `jia_wang` to `spc_004` in V1.0. Adding it because the field exists would author a new Useful God mapping (chuyên Thổ → Thiên Ấn) that the production rule never stated.

Live: 3 `jia_wang` charts. `case_0088` remains `str_004` (no Chính Quan). `case_0004` / `case_0014` now win `str_003` from **hidden Chính Quan**, not from `spc_004`.

Defer chuyên-Thổ Ấn mapping to **UG-V1.1-KNOWLEDGE**.

---

## 4. Rules explicitly not added (V1.1)

- strong → Wealth / Hao  
- strong + Thất Sát → Chế  
- main Pattern → Overall Useful God  
- Kiếp Tài → Useful God  
- new Mộc rule / new priority / new Flow priority  

Climate split (UG-R2) unchanged: `sea_*` / `tmp_*` remain climate-only.

Flow unique-max and G1-06 semantics unchanged. Flow remains non-competitive in V1.0 (group 60 < strength 80).

---

## 5. Control cases (fresh)

| Case | Strength | Pattern | Điều hậu | Old Overall | New Overall | Winning rule | Reason |
|------|----------|---------|----------|-------------|-------------|--------------|--------|
| Nguyễn Tiến Sơn | 0.87 strong | Chính Ấn (`chinh_an`) | Hàn · Cần ôn ấm · ưu tiên Hỏa (`sea_001`) | Thủy · Nhâm · Thực Thần (`str_004`) | **Hỏa · Đinh · Chính Quan** | `str_003` | Hidden Ngọ **Đinh = Chính Quan**; priority 82 beats `str_004` 76. Hỷ/Kỵ from `str_003`. |
| Lương Ngọc Huỳnh | 0.64 balanced | Chính Tài | Lương · Cần ôn ấm · ưu tiên Hỏa (`sea_004`) | Kim · Tân · Chính Tài (`str_005`) | Kim · Tân · Chính Tài | `str_005` | No Chính Quan. Balanced path unchanged. |
| Đặng Thị Dung | 0.24 weak | Sát Ấn (`sat_an`) | Nhiệt · Cần làm mát · ưu tiên Thủy (`sea_002`) | Thủy · Nhâm · Chính Ấn (`str_001`) | Thủy · Nhâm · Chính Ấn | `str_001` | Hidden Chính Quan is now visible to UG, but `str_003` requires **strong**. Weak still uses Ấn. |
| Đoàn Quang Hưng | 0.61 balanced | Thực Thần | Lương · Cần ôn ấm · ưu tiên Hỏa (`sea_004`) | Thủy · Nhâm · Chính Tài (`str_005`) | Thủy · Nhâm · Chính Tài | `str_005` | Hidden Chính Quan present; `str_003` still requires strong. Balanced unchanged. |
| Vũ Thị Thanh Tuyền | 0.66 strong | Kiếp Tài | Nhiệt · Cần làm mát · ưu tiên Thủy (`sea_002`) | Kim · Canh · Thực Thần (`str_004`) | **Mộc · Ất · Chính Quan** | `str_003` | Hidden Mùi Ất now reaches `str_003`. |

Old Overall values were **not** preserved for compatibility.

---

## 6. 101-case Chính Quan classes

See `UG_R3F_101_CASE_REGRESSION.md`. Summary:

| Class | Meaning | n | `str_003` candidates before → after | Winner change |
|-------|---------|--:|-------------------------------------:|---------------|
| A | visible only | 11 | 6 → 6 | 0 |
| B | hidden-only | 47 | 0 → 29 | **25** (`str_004` → `str_003`) |
| C | visible + hidden | 22 | 10 → 10 (no duplicate token) | 0 |
| D | none | 21 | 0 → 0 | 0 |

`spc_004` wiring: **0** winner changes (not applied).

---

## 7. UG-V1.1-KNOWLEDGE backlog (non-blocking)

A. Strong → Hao / Tài path  
B. Strong + Thất Sát → Chế path  
C. Main Pattern → Overall Useful God reconciliation  
D. Flow competitiveness  
E. Chính Quan vs Thất Sát visibility/weighting research  
F. Multi-candidate reconciliation rather than fixed class mapping  
G. `jia_wang` vs `spc_004` chuyên-Ấn mapping (documented omission, not a matcher bug)  
H. Tiết vs Chế reconciliation when both are reachable  
I. Absent-element candidate theory  
J. Same-element Hỷ theory beyond Ten God sibling groups  
K. Independently derived Hỷ (not CSV leftover)  
L. Full-chart Kỵ  
M. Confidence / competing candidates  
N. Alternative theory explanations on the customer card  

Added from HK-R1G. Non-blocking for V1.0.

---

## Files changed

### Engine

- `engines/useful_god_engine/utils/context_builder.py` — hidden Chính Quan reachability + provenance  
- `engines/useful_god_engine/context.py` — `officer_provenance`  
- `engines/useful_god_engine/engine.py` — snapshot provenance  

### Tests (live Overall SSOT only; no Golden)

- `tests/useful_god/test_ug_r3f_hidden_chinh_quan.py` (new)  
- `tests/useful_god/test_g1_06_useful_god_binding.py`  
- `tests/useful_god/test_ug_r2_climate_overall_split.py`  
- `tests/temperature/test_g1_04_temperature_binding.py`  
- `tests/report_engine/test_g1_06_useful_god_binding.py`  
- `tests/report_engine/test_g1_04_temperature_binding.py`  
- `tests/report_engine/test_case_0001_report_input.py`  

Not edited: Golden Dataset, snapshots, expected JSON, `str_003` CSV, Flow, climate layer.

---

## Tests executed

```
python -m pytest tests/useful_god tests/temperature/test_g1_04_temperature_binding.py tests/report_engine/test_g1_06_useful_god_binding.py tests/report_engine/test_g1_04_temperature_binding.py tests/report_engine/test_g1_05_five_elements_binding.py tests/report_engine/test_case_0001_report_input.py -q
```

**51 passed.** Remaining failures in this module set: **none.**
