# UG-R2 — Useful God Coverage Matrix

**Date:** 2026-08-20  
**Scope:** existing `database/13_useful_god` reachable Overall paths after climate separation.  
**No new theory authored.**

Production Overall groups: `strength` (80), `flow` (60), `special` (100).  
Climate (`season` 90, `temperature` 70) is **not** in this matrix.

---

## 1. Strong Day Master — Overall paths

Rules:

- Drain/output: `str_004` — `strength_level == strong` → **Thực Thần** (always matches).
- Control: `str_003` — strong **and** `officer_elements contains Chính Quan` → **Chính Quan**.
- Wealth: **no** `str_*` for strong. `str_005` is `balanced` only.

Tokens are Ten Gods, then G1-01 maps stem/element per Day Master. Coverage is therefore **the same shape for all five elements**.

| Day Master element | Drain candidate | Wealth candidate | Control candidate | Coverage |
|---|---|---|---|---|
| Mộc | `str_004` Thực Thần | — | `str_003` Chính Quan **if** Chính Quan is listed | Drain always. Control conditional. Wealth **none**. |
| Hỏa | `str_004` Thực Thần | — | `str_003` Chính Quan if listed | same |
| Thổ | `str_004` Thực Thần | — | `str_003` Chính Quan if listed | same — Tuyền takes drain (Canh). Thất Sát does **not** unlock control. |
| Kim | `str_004` Thực Thần | — | `str_003` Chính Quan if listed | same — Sơn takes drain (Nhâm). |
| Thủy | `str_004` Thực Thần | — | `str_003` Chính Quan if listed | same |

**Engine structurally favors drain/output for strong** whenever Chính Quan is absent. That is the live Tuyền / Sơn path.

101-case strong winners (live): `str_004` 29, `str_003` 15, plus special overrides (below).

---

## 2. Weak Day Master — Overall paths

Rules:

- Resource (preferred): `str_001` — weak **and** `resource_elements contains Chính Ấn` → **Chính Ấn**.
- Resource (fallback): `str_002` — weak → **Thiên Ấn**.
- Peer/support: Tỷ Kiên / Kiếp Tài appear only on **favorable lists**, never as Overall `useful_god`.

| Day Master element | Resource candidate | Peer candidate | Other | Coverage |
|---|---|---|---|---|
| Mộc | `str_001` Chính Ấn if listed, else `str_002` Thiên Ấn | — (Hỷ only) | — | Resource always. Peer not selectable. Dung = `str_001`. |
| Hỏa | same | — | — | same |
| Thổ | same | — | — | same |
| Kim | same | — | — | same |
| Thủy | same | — | — | same |

101-case weak winners (live): `str_002` 15, `str_001` 1, plus follow specials.

**Engine structurally favors Resource for weak.** There is no peer-as-Overall path.

---

## 3. Balanced

`str_005` → **Chính Tài** (wealth/flow). Huỳnh and Hưng take this. 101-case: `str_005` 29.

---

## 4. Special / follow (override only when canonical Pattern winner is that token)

| Token | UG rule | Overall token |
|-------|---------|---------------|
| `tong_tai` | `spc_001` | Chính Tài |
| `tong_quan` | `spc_002` | Chính Quan |
| `tong_sat` | `spc_003` | Thất Sát |
| `tong_vuong` / `tong_nhi` / `tong_an` | **none** | gap |
| `khuc_truc` `viem_thuong` `nhuan_ha` `gia_sac` | `spc_004` | Thiên Ấn |
| `jia_wang` | **none** | gap |

G1-X01: follow token is published only if Pattern winner is that follow rule. Strength compatibility remains.

101-case special: `spc_004` 8, `spc_001` 3, `spc_003` 1, `spc_002` 0.

---

## 5. Pattern token → UG map (gaps)

Every main and combination Pattern token has **no** Useful God rule:

`chinh_quan`, `that_sat`, `chinh_tai`, `thien_tai`, `thuc_than`, `thuong_quan`, `chinh_an`, `thien_an`, `ty_kien`, `kiep_tai`, `quan_an`, `sat_an`, `thuc_than_sinh_tai`, `thuong_quan_phoi_an`, `tai_quan_song_my`.

`main_pattern` is copied onto UsefulGodContext and **never read**.

---

## 6. Flow as Overall source

`flo_001`–`flo_004`: unique-max occurrence → control stem (Mộc→Canh, Hỏa→Nhâm, Kim→Đinh, Thủy→Mậu).

Theoretically **not** suitable as a strong Overall claim of excess. Not promoted. With Strength always set, flow never won the 101-case Overall set.

---

## 7. Mộc / strong Mậu

**`V1.0 KNOWLEDGE GAP — PRODUCT OWNER DECISION REQUIRED`**

Not an unreachable `str_003`. The rule exists and is reachable; Tuyền fails its Chính Quan clause. No production row for Thất Sát control or Wood officer for Earth. Do not add in UG-R2.
