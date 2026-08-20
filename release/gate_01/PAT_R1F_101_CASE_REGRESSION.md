# PAT-R1F — 101-case regression

**Date:** 2026-08-20  
**Input:** `tests/golden_dataset/inputs` (n=101). **Golden expected files were not edited.**  
**Pipeline:** Calendar → BaZi → Strength → Temperature overlay → Pattern → Useful God.

PAT-R1 old special Overall winners (12): `spc_004`×8, `spc_001`×3, `spc_003`×1.

---

## Overall winner groups

| Group | UG-R3F | PAT-R1F | Role |
|-------|-------:|--------:|------|
| `strength` | 89 | **97** | Overall Dụng thần |
| `special` | 12 | **4** | follow `spc_001`/`spc_003` only |
| `season` / `temperature` | 0 | **0** | climate-only |
| `flow` | 0 | **0** | never beats Strength |
| incomplete | 0 | **0** | |

### Overall rule IDs

| Rule | UG-R3F | PAT-R1F | Delta |
|------|-------:|--------:|------:|
| `str_003` | 40 | **45** | +5 |
| `str_005` | 29 | 29 | 0 |
| `str_002` | 15 | 15 | 0 |
| `str_004` | 4 | **7** | +3 |
| `str_001` | 1 | 1 | 0 |
| `spc_004` | 8 | **0** | −8 |
| `spc_001` | 3 | 3 | 0 |
| `spc_003` | 1 | 1 | 0 |
| `spc_002` | 0 | 0 | 0 |

`str_003` +5 and `str_004` +3 = the 8 former `spc_004` charts returning to ordinary structural selection (hidden Chính Quan still reaches `str_003` after UG-R3F).

---

## Detected LEVEL-1 special Patterns (11)

Detected, **not** override-qualified, `spc_*` **not** in Overall:

| Case | Pattern | Strength | New Overall |
|------|---------|----------|-------------|
| case_0004 | `jia_wang` | strong | `str_003` Mộc · Ất · Chính Quan |
| case_0014 | `jia_wang` | strong | `str_003` Mộc · Ất · Chính Quan |
| case_0015 | `viem_thuong` | strong | `str_004` Thổ · Kỷ · Thực Thần |
| case_0022 | `khuc_truc` | strong | `str_004` Hỏa · Đinh · Thực Thần |
| case_0032 | `khuc_truc` | strong | `str_003` Kim · Tân · Chính Quan |
| case_0057 | `gia_sac` | 0.95 strong | `str_003` Hỏa · Đinh · Chính Quan |
| case_0059 | `nhuan_ha` | strong | `str_004` Mộc · Giáp · Thực Thần |
| case_0077 | `gia_sac` | strong | `str_003` Hỏa · Đinh · Chính Quan |
| case_0084 | `viem_thuong` | strong | `str_003` Thủy · Quý · Chính Quan |
| case_0087 | `gia_sac` | strong | `str_003` Hỏa · Bính · Chính Quan |
| case_0088 | `jia_wang` | strong | `str_004` Kim · Tân · Thực Thần |

`jia_wang` (0004, 0014, 0088) was already not in `spc_004`; Overall unchanged vs UG-R3F. They are listed because detection is now explicitly LEVEL 1 / suppressed.

---

## Override-qualified special Overall (4)

G1-X01 published follow. Unchanged vs PAT-R1 / UG-R3F:

| Case | Pattern | Level | Rule | Display |
|------|---------|------:|------|---------|
| case_0021 | `tong_tai` | 2 | `spc_001` | Kim · Canh · Chính Tài |
| case_0073 | `tong_tai` | 2 | `spc_001` | Hỏa · Đinh · Chính Tài |
| case_0093 | `tong_sat` | 2 | `spc_003` | Thổ · Kỷ · Thất Sát |
| case_0095 | `tong_tai` | 2 | `spc_001` | Thổ · Kỷ · Chính Tài |

---

## PAT-R1 twelve special winners — after gate

| Case | Pattern | Qual. | Old `spc_*` | Override eligible? | New Overall | Reason |
|------|---------|------:|-------------|--------------------|-------------|--------|
| case_0015 | `viem_thuong` | 1 | `spc_004` | **No** | `str_004` Thổ · Kỷ · Thực Thần | LEVEL-1 chuyên; strong fallback Tiết |
| case_0021 | `tong_tai` | 2 | `spc_001` | **Yes** | `spc_001` Kim · Canh · Chính Tài | G1-X01 weak follow preserved |
| case_0022 | `khuc_truc` | 1 | `spc_004` | **No** | `str_004` Hỏa · Đinh · Thực Thần | LEVEL-1; no CQ → `str_004` |
| case_0032 | `khuc_truc` | 1 | `spc_004` | **No** | `str_003` Kim · Tân · Chính Quan | LEVEL-1; hidden/visible CQ path |
| case_0057 | `gia_sac` | 1 | `spc_004` | **No** | `str_003` Hỏa · Đinh · Chính Quan | LEVEL-1; hour Bính / CQ |
| case_0059 | `nhuan_ha` | 1 | `spc_004` | **No** | `str_004` Mộc · Giáp · Thực Thần | LEVEL-1; no CQ |
| case_0073 | `tong_tai` | 2 | `spc_001` | **Yes** | `spc_001` Hỏa · Đinh · Chính Tài | G1-X01 preserved |
| case_0077 | `gia_sac` | 1 | `spc_004` | **No** | `str_003` Hỏa · Đinh · Chính Quan | LEVEL-1; visible Chính Quan now reaches Overall |
| case_0084 | `viem_thuong` | 1 | `spc_004` | **No** | `str_003` Thủy · Quý · Chính Quan | LEVEL-1; CQ path |
| case_0087 | `gia_sac` | 1 | `spc_004` | **No** | `str_003` Hỏa · Bính · Chính Quan | LEVEL-1; CQ path |
| case_0093 | `tong_sat` | 2 | `spc_003` | **Yes** | `spc_003` Thổ · Kỷ · Thất Sát | G1-X01 preserved |
| case_0095 | `tong_tai` | 2 | `spc_001` | **Yes** | `spc_001` Thổ · Kỷ · Chính Tài | G1-X01 preserved |

**Ngô Đắc Dũng** (not in 101): LEVEL 1 `gia_sac`, eligible **No**, Overall `str_004` Thủy · Nhâm · Thực Thần. Same class as 0015/0022/0059 (strong, no Chính Quan).

Attention cases **0077 / 0057 / Dũng**: detection remains Giá Sắc; Overall is ordinary Strength, not `spc_004`.

Changed Overall vs PAT-R1 twelve: **8** (all former `spc_004`). Unchanged: **4** follow.

---

## Suppressed `spc_*` candidates

- `spc_004`: **0** Overall publications (was 8).
- Follow `spc_001` / `spc_003`: still published when Pattern winner is that follow token.
- No incomplete Overall.

---

## Follow regression (G1-X01)

| Invariant | Result |
|-----------|--------|
| Weak-follow only when `weak` | Holds (0021, 0073, 0095, 0093) |
| Tòng Vượng only when `strong` | Holds; `tong_vuong` still has no `spc_*` |
| Token normalization | Holds (`tests/useful_god/test_g1_x01_follow_token_normalization.py`) |
| Qualified follow still invokes `spc_*` | Holds (4/101) |

---

Golden Dataset: **not updated**.

Live API (restarted uvicorn PID 8068) independently confirmed the Dũng reconstruct: LEVEL-1 `gia_sac` detected, `spc_004` absent, Overall `str_004`.
