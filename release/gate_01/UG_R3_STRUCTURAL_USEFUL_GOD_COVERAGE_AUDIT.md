# UG-R3 — Structural Useful God Coverage Audit

**Date:** 2026-08-20  
**Phase:** Audit only. **No engine, CSV, priority, Strength, Pattern, Temperature, or Tuyền-Mộc change.**  
**Production:** `engines/useful_god_engine` V2 + `database/13_useful_god`  
**Climate:** `sea_*` / `tmp_*` confirmed **out of Overall** (UG-R2). Not re-audited as Overall competitors.

## Status

**`UG-R3: MIXED KNOWLEDGE + IMPLEMENTATION GAP — REVIEW REQUIRED`**

Do not start G1-FINAL. Do not implement repair in this task.

---

## Five primary answers

| # | Question | Answer |
|---|----------|--------|
| 1 | Strong: đủ Tiết / Hao / Chế? | **Không.** Tiết **FULL** (`str_004` always). Chế **PARTIAL** (visible **Chính Quan** only via `str_003`). Hao **ABSENT**. |
| 2 | Vì sao `str_003` nhận Chính Quan không nhận Thất Sát? | **B — Data omission.** CSV value is exactly `Chính Quan`. Matcher would accept `Thất Sát` if a row existed. `officer_elements` already contains Thất Sát on Tuyền/Sơn/Dung. Knowledge pack `cand_ug_officer_strong` is also Chính Quan only. |
| 3 | Pattern-main có ảnh hưởng Overall? | **Không.** `main_pattern` is copied onto context and **never read**. 0/101 winners from main Pattern. |
| 4 | Vì sao 89/101 là Strength? | Strength class always matches one of `str_001`–`str_005`. Special (100) overrides 12 cases. Flow (60) never beats Strength (80). Climate is no longer Overall. |
| 5 | A / B / C / D? | **D — Mixed B + C.** Production CSV is a Strength-class mapper; multi-factor paths were never authored there (B). Hidden Chính Quan (Ất in Tuyền Mùi) does not enter `officer_elements` (C, visibility). `jia_wang` is published to `special_pattern` but omitted from `spc_004` (C, list). |

**One-line model fact:**

`Overall Useful God currently behaves primarily as a Strength-class mapper.`

---

## 1. Structural rule inventory

Active/reachable Overall rules. Group priority from `05_priority_rules.csv`. Climate groups omitted except confirmation: `pri_002` season 90 / `pri_004` temperature 70 are **climate-layer only** after UG-R2.

| Rule | Group | Trigger | Candidate | Theory role | Priority (row / group) | Reachable |
|------|-------|---------|-----------|-------------|------------------------:|-----------|
| `str_001` | strength | `weak` AND `resource_elements contains Chính Ấn` | Chính Ấn | SUPPORT | 80 / 80 | Yes |
| `str_002` | strength | `weak` | Thiên Ấn | SUPPORT | 78 / 80 | Yes (always on weak) |
| `str_003` | strength | `strong` AND `officer_elements contains Chính Quan` | Chính Quan | CONTROL — CHẾ | 82 / 80 | Yes when **visible** Chính Quan |
| `str_004` | strength | `strong` | Thực Thần | DRAIN — TIẾT | 76 / 80 | Yes (**every** strong) |
| `str_005` | strength | `balanced` | Chính Tài | WEALTH — HAO | 70 / 80 | Yes (**every** balanced) |
| `flo_001` | flow | unique-max `element_distribution` Mộc | Canh | OTHER (element 克, not DM-relative) | 74 / 60 | Yes; never Overall winner |
| `flo_002` | flow | unique-max Hỏa | Nhâm | OTHER | 74 / 60 | Yes; never winner |
| `flo_003` | flow | unique-max Kim | Đinh | OTHER | 74 / 60 | Yes; never winner |
| `flo_004` | flow | unique-max Thủy | Mậu | OTHER | 74 / 60 | Yes; never winner |
| `spc_001` | special | `follow_pattern == tong_tai` | Chính Tài | SPECIAL | 95 / 100 | Yes if G1-X01 publishes token |
| `spc_002` | special | `follow_pattern == tong_quan` | Chính Quan | SPECIAL | 95 / 100 | Yes; 0/101 live |
| `spc_003` | special | `follow_pattern == tong_sat` | Thất Sát | SPECIAL | 95 / 100 | Yes; 1/101 live |
| `spc_004` | special | `special_pattern in {khuc_truc, viem_thuong, nhuan_ha, gia_sac}` | Thiên Ấn | SPECIAL / SUPPORT | 92 / 100 | Yes; **`jia_wang` omitted** |
| Pattern-main | — | `main_pattern` / `kiep_tai` / `chinh_an` / … | — | — | — | **No rule** |
| Balance stage | — | spread of `element_distribution` | none | OTHER | — | Summary only; **no candidate** |
| Fallback empty Overall | — | no structural match | incomplete message | OTHER | — | Unreachable while Strength class is set |

`08_rule_conditions.csv` is a library; **not loaded**. `07_examples.csv` not loaded.

---

## 2. Theory-role classification

Taken from **condition + `useful_god` token**, not from file names.

| Role | Rules |
|------|-------|
| SUPPORT | `str_001`, `str_002`; `spc_004` (Ấn for chuyên cách) |
| DRAIN — TIẾT | `str_004` only. Thương Quan is Hỷ of `str_004`, never Overall. |
| WEALTH — HAO | `str_005` (balanced only); `spc_001` (Tòng Tài, not ordinary strong) |
| CONTROL — CHẾ | `str_003` (Chính Quan); `spc_002` / `spc_003` (tòng only) |
| SPECIAL | `spc_001`–`spc_004` |
| OTHER | `flo_001`–`flo_004` (unique-max element 克); balance summary |

---

## 3. Strong Day Master coverage

Rules are **Ten God tokens**, then G1-01 maps stem/element. Shape is identical for all five Day Master elements.

| Day Master | Tiết path | Hao path | Chế path | Conditions | Reachable? |
|---|---|---|---|---|---|
| Mộc | `str_004` → Thực Thần → Hỏa | — | `str_003` → Chính Quan → Kim | Tiết: `strong` only. Chế: + visible Chính Quan | Tiết yes. Hao **no**. Chế conditional |
| Hỏa | `str_004` → Thực Thần → Thổ | — | `str_003` → Chính Quan → Thủy | same | same |
| Thổ | `str_004` → Thực Thần → Kim | — | `str_003` → Chính Quan → Mộc | same | Tuyền: Tiết yes (Canh). Hao no. Chế no (visible Thất Sát, hidden Ất ignored) |
| Kim | `str_004` → Thực Thần → Thủy | — | `str_003` → Chính Quan → Mộc | same | Sơn: Tiết yes (Nhâm). Visible Thất Sát does not unlock Chế |
| Thủy | `str_004` → Thực Thần → Mộc | — | `str_003` → Chính Quan → Hỏa | same | same |

**Q1 restated:** V1.0 production does **not** have three balancing paths for strong. It has **Tiết always**, **Chế iff visible Chính Quan**, **Hao never**.

---

## 4. Weak Day Master coverage

| Day Master | Resource/Sinh | Peer/Trợ | Other | Reachable? |
|---|---|---|---|---|
| All five | `str_001` Chính Ấn if **visible** Chính Ấn; else `str_002` Thiên Ấn always | Tỷ Kiên / Kiếp Tài only on Hỷ lists | follow `spc_*` if G1-X01 | Resource always. Peer **not selectable** as Overall |

Live 20 weak: `str_002` 15, `str_001` 1, `spc_001` 3, `spc_003` 1.

**Weak model is nearly `weak → Resource`.** Preferred Chính Ấn only when visible; otherwise Thiên Ấn fallback. Not a peer-support selector.

---

## 5. Balanced coverage

`str_005` trigger: **`strength_level == balanced` only.** No Pattern, no officer, no wealth-presence clause.

- Huỳnh `0.64 balanced` → `str_005` Kim · Tân · Chính Tài. Extra `flo_002` loses.
- Hưng `0.61 balanced` → `str_005` Thủy · Nhâm · Chính Tài. Pattern `thuc_than` **does not change** the winner. No unique-max flow (Kim=Hỏa tie).

Live 29 balanced: **29/29 `str_005`.** No other balanced structural Overall rule exists.

Pattern cannot change a balanced Overall winner unless a follow/special token is published (none of the 29).

---

## 6. `str_003` forensic

| Item | Fact |
|------|------|
| Conditions | `strength_level == strong` AND `officer_elements contains Chính Quan` |
| Candidate | `Chính Quan` (then G1-01 stem/element) |
| Favorable / unfavorable | Chính Quan, Thực Thần / Tỷ Kiên, Kiếp Tài |
| Row priority / score | 82 / 0.84 (beats `str_004` 76 / 0.77 when both match) |
| Group | strength → group priority 80 |
| Condition library | `cond_008`: field `officer_elements`, value **Chính Quan**, description **“Có Quan thần”** |
| Knowledge pack | `cand_ug_officer_strong` / UGD-000024: outcome **Chính Quan**; explanation cites `str_003` |
| Interpretation | `chinh_quan.json`: engine at `str_003` and `spc_002`. `that_sat.json`: engine at **`spc_003` and Hỷ of tòng quan** — **not** `str_003` |
| `officer_elements` source | Visible pillar-stem Ten Gods only (`BaziChart.ten_gods`, excluding Nhật Chủ) |

**Why Chính Quan and not Thất Sát?**

| Class | Fit |
|-------|-----|
| **A. Explicit theory decision** | Not proven. Description “Quan thần” can mean the officer *family*. Interpretation treats Thất Sát as a Dụng role, but only via tòng. |
| **B. Data omission** | **Best fit.** CSV token is `Chính Quan`. No second row. Matcher `contains` on a list is `right in left` — a `Thất Sát` value would match Tuyền today. |
| **C. Implementation limitation** | **Not for Thất Sát.** Matcher already stores Thất Sát in `officer_elements`. It does not map “Quan thần” → {Chính Quan, Thất Sát}. |
| **D. Unknown** | Residual: whether authors *meant* family vs Chính Quan only. |

Do not treat this as A.

---

## 7. Thất Sát control knowledge search

**Production `database/13_useful_god`:** no strong + Thất Sát Overall row. Thất Sát Overall only via `spc_003` (`tong_sat`).

**`knowledge/packages/useful_god/foundation` (bz_06, not loaded by UsefulGodLoader):**

- `cand_ug_officer_strong` → Chính Quan
- `cand_ug_pattern_good_officer` → Chính Quan when pattern quality good/excellent **and** strength_score ≥ 65
- No `candidate_useful=Thất Sát` for ordinary strong
- Thất Sát appears in **unfavorable** candidate bundles

**`knowledge/interpretation/domains/useful_god/that_sat.json`:** role may be Dụng; runtime cited as `spc_003` / Hỷ of tòng quan.

**`knowledge/bazi/05_useful_god_knowledge`:** blueprint, zero academic records.

**Python `_OFFICER_GODS`:** `{Chính Quan, Thất Sát}` — used to *fill* `officer_elements`, not to expand `str_003`.

| Verdict | |
|---------|-|
| Strong + Thất Sát as Overall Dụng in production CSV | **does not exist** → knowledge coverage gap |
| bz_06 officer candidate | exists as **Chính Quan**, **not wired** (documented: “Not wired to Analysis Engine”) |
| Matcher blocking Thất Sát | **false** |

---

## 8. Wealth / Hao coverage

**`STRONG-WEALTH/HAO PATH ABSENT`.**

No `str_*` / `flo_*` / `spc_*` (except Tòng Tài) selects Chính Tài or Thiên Tài for `strength_level == strong`.

Tuyền has **visible** Quý = Chính Tài and hidden Nhâm = Thiên Tài. Neither creates an Overall Hao candidate.

`str_005` is balanced-only. `spc_001` is follow-only.

bz_06 `cand_ug_wealth_balanced` is the same balanced-Tài idea; no strong-wealth object found.

---

## 9. Output / Tiết coverage (`str_004`)

| Item | Fact |
|------|------|
| Condition | `strength_level == strong` **only** |
| Candidate | always **Thực Thần** |
| Thương Quan | Hỷ only; **cannot** be Overall |
| Pattern / evidence | none |
| Always matches every strong? | **Yes** |

> Every ordinary strong chart receives a drain candidate regardless of chart-specific structure.

That is why `str_004` dominates remaining strong charts (29/52). When visible Chính Quan exists, `str_003` still matches **and wins** (15/52). When special pattern publishes, `spc_004` wins (8/52). The 29 are “strong, not visible Chính Quan, not chuyên cách.”

---

## 10. Pattern-main coverage

| Pattern token | Useful God rule exists? | Candidate | Priority | Reachable? |
|---|---|---|---:|---|
| `chinh_quan` | No | — | — | No |
| `that_sat` | No | — | — | No |
| `chinh_tai` | No | — | — | No |
| `thien_tai` | No | — | — | No |
| `thuc_than` | No | — | — | No |
| `thuong_quan` | No | — | — | No |
| `chinh_an` | No | — | — | No |
| `thien_an` | No | — | — | No |
| `ty_kien` | No | — | — | No |
| `kiep_tai` | No | — | — | No |
| `quan_an` / `sat_an` / `thuc_than_sinh_tai` / `thuong_quan_phoi_an` / `tai_quan_song_my` | No | — | — | No |
| `tong_tai` | `spc_001` | Chính Tài | 100 | If follow winner |
| `tong_quan` | `spc_002` | Chính Quan | 100 | If follow winner |
| `tong_sat` | `spc_003` | Thất Sát | 100 | If follow winner |
| `tong_vuong` / `tong_nhi` / `tong_an` | No | — | — | Gap |
| `khuc_truc` `viem_thuong` `nhuan_ha` `gia_sac` | `spc_004` | Thiên Ấn | 100 | Yes |
| `jia_wang` | **list miss** | — | — | Context may set `special_pattern`; **no CSV match** |

**Main Pattern has no influence on Overall Useful God.**

---

## 11. Special vs main Pattern

UG-R2 12 special Overall winners:

- **Follow (4):** `spc_001` ×3 (`tong_tai` + weak), `spc_003` ×1 (`tong_sat` + weak)
- **Chuyên (8):** `spc_004` on `viem_thuong` / `khuc_truc` / `gia_sac` / `nhuan_ha` + strong

They override Strength because **group priority 100 > 80**. G1-X01 still blocks invalid follow tokens.

Main Pattern does not participate because **no rule reads `main_pattern`.** Special/follow participate only through `follow_pattern` / `special_pattern`.

---

## 12. Vũ Thị Thanh Tuyền — structural opportunities

Chart: Giáp Tý / Tân Mùi / Mậu Thân / Quý Hợi · Mậu · `0.66 strong` · `kiep_tai` · Điều hậu Nhiệt · ưu tiên Thủy · Overall `str_004` Kim · Canh · Thực Thần.

Do **not** treat Mộc as expected winner.

| Theory path | Expected element role | Rule exists? | Match? | Why |
|---|---|---:|---:|---|
| Tiết | Kim (Mậu sinh Kim) | Yes `str_004` | **Yes** | `strong` only. Maps to Canh / Kim / Thực Thần |
| Hao | Thủy (Mậu khắc Thủy) | **No** | No | Visible Quý = Chính Tài unused. `STRONG-WEALTH/HAO PATH ABSENT` |
| Chế | Mộc (Mộc khắc Thổ) | Partial `str_003` | **No** | Needs **Chính Quan** in `officer_elements`. Visible officer = Thất Sát (Giáp). Hidden Ất = Chính Quan **not listed** |
| Pattern Kiếp Tài | undefined in UG | **No** | No | `main_pattern=kiep_tai` unread |
| Special / follow | — | `spc_*` | No | `follow_pattern` None; not chuyên codes |
| Flow unique-max Thủy | Thổ 克 Thủy | Yes `flo_004` | Yes, **loses** | Group 60 < 80. Token Mậu = Tỷ Kiên (peer, not Hao/Chế) |

Matched Overall: `str_004`, `flo_004`. Winner `str_004`.

---

## 13. Giáp / Ất / Quan Sát on Tuyền

Visible stems (`BaziChart.ten_gods`):

| Pillar | Stem | Ten God vs Mậu | In `officer_elements`? |
|--------|------|----------------|------------------------|
| Năm | Giáp | **Thất Sát** | Yes |
| Tháng | Tân | Thương Quan | No (output) |
| Ngày | Mậu | Nhật Chủ | Dropped |
| Giờ | Quý | Chính Tài | No (wealth) |

Hidden:

| Location | Stem | Ten God | Consumed by UG families? |
|----------|------|---------|--------------------------|
| Tý | Quý | Chính Tài | **No** |
| Mùi | Kỷ | Kiếp Tài | **No** |
| Mùi | Đinh | Chính Ấn | **No** |
| **Mùi** | **Ất** | **Chính Quan** | **No** |
| Thân | Canh | Thực Thần | **No** |
| Thân | Nhâm | Thiên Tài | **No** |
| Hợi | Giáp | Thất Sát | **No** (visible Giáp already counted) |

`str_003` requires Chính Quan in `officer_elements`. **Hidden Ất does not qualify** because `officer_elements` is built from **visible** `ten_gods_list` only.

This is a **visibility coverage issue on the existing Chính Quan path**, not a Thất Sát matcher bug. If hidden Ất were listed, `str_003` would match and **beat** `str_004` (82 > 76) → Overall **Ất / Mộc / Chính Quan**. That is a counterfactual, not a recommended Tuyền change.

---

## 14. Five control cases

| Case | Strength | Pattern | Structural candidates | Winner | Why |
|------|----------|---------|----------------------|--------|-----|
| Nguyễn Tiến Sơn | 0.87 strong | `chinh_an` | `str_004` only | `str_004` Thủy · Nhâm · Thực Thần | Strong + visible Thất Sát (not Chính Quan). Main Pattern unread. Dist max Thổ; no `flo_*` for Thổ |
| Lương Ngọc Huỳnh | 0.64 balanced | `chinh_tai` | `str_005`, `flo_002` | `str_005` Kim · Tân · Chính Tài | Fixed balanced → Tài. Pattern unread. Flow unique-max Hỏa loses (60) |
| Đặng Thị Dung | 0.24 weak | `sat_an` | `str_001`, `str_002`, `flo_003` | `str_001` Thủy · Nhâm · Chính Ấn | Visible Chính Ấn unlocks `str_001` over `str_002`. Combination Pattern unread. Flow Kim unique-max loses |
| Đoàn Quang Hưng | 0.61 balanced | `thuc_than` | `str_005` | `str_005` Thủy · Nhâm · Chính Tài | Same mapper as Huỳnh. Pattern Thực Thần unread. Dist tie → no flow |
| Vũ Thị Thanh Tuyền | 0.66 strong | `kiep_tai` | `str_004`, `flo_004` | `str_004` Kim · Canh · Thực Thần | Same as Sơn class. Hidden Ất unused. Kiếp Tài unread |

---

## 15. 101-case exact-rule distribution

Live `OrchestratorService.analyze` on `tests/golden_dataset/inputs` (n=101). Golden expected files not edited.

| Rule | Winner count | % |
|------|-------------:|----:|
| `str_004` | 29 | 28.7 |
| `str_005` | 29 | 28.7 |
| `str_003` | 15 | 14.9 |
| `str_002` | 15 | 14.9 |
| `spc_004` | 8 | 7.9 |
| `spc_001` | 3 | 3.0 |
| `str_001` | 1 | 1.0 |
| `spc_003` | 1 | 1.0 |
| `spc_002` | 0 | 0.0 |
| `flo_*` | 0 | 0.0 |
| `sea_*` / `tmp_*` | 0 | 0.0 |

Two generic Strength rules (`str_004` + `str_005`) are **57.4%** of Overall winners.

---

## 16. Strength-class cross-tab

| Strength class | Cases | Winner rules |
|---|---:|---|
| strong | 52 | `str_004` 29 · `str_003` 15 · `spc_004` 8 |
| balanced | 29 | `str_005` **29** |
| weak | 20 | `str_002` 15 · `spc_001` 3 · `str_001` 1 · `spc_003` 1 |

- Almost every **balanced** → `str_005`. **Yes (100%).**
- Almost every **strong** → `str_004`. **No** (56% of strong; 29% Chế if visible Chính Quan; 15% chuyên Ấn).
- Almost every **weak** → `str_001`. **No** — **75% are `str_002`** (no visible Chính Ấn).

`Overall Useful God currently behaves primarily as a Strength-class mapper.`  
The only intra-class branch is “is visible Chính Quan / Chính Ấn present?” plus rare special/follow override.

---

## 17. Candidate diversity (structural Overall)

| Metric | Value |
|--------|------:|
| Average | 1.703 |
| Min | 1 |
| Max | 3 |
| Exactly one candidate | 44 / 101 = **43.6%** |
| Two | 43 |
| Three | 14 |

Not “almost always one,” but the second/third candidate is usually **flow** (priority 60) or the **losing Strength sibling** (`str_004` under `str_003`, `str_002` under `str_001`). Those contests are predetermined. **Priority cannot meaningfully reconcile Tiết vs Hao vs Chế** because Hao is absent and Chế is a gated sibling of Tiết, not an independent third path.

---

## 18. Pattern influence rate (101)

| Source | Overall winners caused | Rate |
|--------|----------------------:|-----:|
| Main Pattern | **0** | 0% |
| Special / chuyên (`spc_004`) | **8** | 7.9% |
| Follow (`spc_001`–`spc_003`) | **4** | 4.0% |

Do not combine: main is unused; only follow/special tokens that UG CSV already names can override Strength.

---

## 19. Flow influence rate (101)

| | Count |
|--|------:|
| Charts generating a `flo_*` Overall candidate | 42 |
| Flow Overall winners | **0** |
| Flow vetoes | **0** (no veto stage) |

`FLOW STRUCTURALLY NON-COMPETITIVE`.

G1-06 unique-max remains; occurrence ≠ excess. Not promoted.

---

## 20. Theory coverage matrix

| Strength state | Sinh/Trợ | Tiết | Hao | Chế | Main Pattern | Special |
|---|---|---|---|---|---|---|
| Strong | ABSENT as Overall | **FULL** `str_004` | **ABSENT** | **PARTIAL** `str_003` visible Chính Quan only | **ABSENT** | **PARTIAL** `spc_004` four codes; not `jia_wang` |
| Balanced | ABSENT | ABSENT as Overall (Hỷ of `str_005` includes Thực Thần) | **FULL** `str_005` | ABSENT | **ABSENT** | none in 101 |
| Weak | **FULL** `str_001`/`str_002` | ABSENT | ABSENT (Kỵ of Ấn rules) | ABSENT except follow `spc_002`/`spc_003` | **ABSENT** | **PARTIAL** follow Tài/Sát |

---

## 21. Intended V1.0 model vs implementation

| Source | Promise | Model |
|--------|---------|-------|
| `database/13_useful_god` README + CSV reasons | Thân vượng/nhược + tòng/chuyên; climate files exist but UG-R2 moved them to Điều hậu | **Model 1** Strength-class + special overlay |
| `engines/analysis_engine/04_useful_god_engine/ALGORITHM.md` | Generate candidates from Strength **and** climate **and** Pattern; resolve conflicts | **Model 4** hybrid — **not the live engine** |
| `bz_06` decision philosophy | strength_score bands → Ấn/Quan/Tài; Pattern quality gates | Hybrid, **not wired** |
| `bz_07` priority package | Rank/conflict — **not wired**; Wave 2 follow/special | Unused |
| UG-R2 Product order | Overall from structural reconciliation; Strength primary; Pattern where rules exist | **Model 4 requested**; Pattern “where rules exist” is almost empty |

**Promise vs live:** Product UG-R2 and unused architecture docs describe multi-factor Overall. **Shipped V2 CSV is a Strength-class mapper** with a Chính Quan gate, a Resource gate, and rare special override.

Missing Hao/Chế-Sát/Pattern-main are **not documented as “V1.0 deferred”** in the production CSV. They are simply absent. Architecture docs that promised Pattern inputs were never connected to `database/13_useful_god`.

---

## 22. Classification

**D — MIXED B + C**

**B — Knowledge coverage gap**

- No strong Hao row.
- No strong Thất Sát Chế row (bz_06 also names Chính Quan only).
- No Pattern-main UG rows.
- Thương Quan never Overall.
- Peer never Overall for weak.
- Follow gaps: `tong_vuong` / `tong_nhi` / `tong_an`.

**C — Implementation / reachability**

- Hidden Chính Quan (Tuyền Mùi Ất) not in `officer_elements` though `str_003` already keys on Chính Quan.
- `jia_wang` copied onto `special_pattern` but omitted from `spc_004` `in` list.
- bz_06 / bz_07 exist and stay unloaded (explicitly documented; wiring would be a new pipeline, not a one-line matcher fix).

Not A: no production document says “V1.0 Overall is Strength-only and Hao/Chế/Pattern are out of scope” while also asking UG-R2 for structural reconciliation.

Not C-only: Thất Sát exclusion is a missing row, not a matcher defect.

---

## 23. Minimum repair proposal — **do not implement here**

### Must fix V1.0 (only if Product confirms intent)

1. **Visibility of `officer_elements` / `resource_elements`:** if “Có Quan thần / Có Ấn thần” includes tàng can, extend family lists with hidden-stem Ten Gods. That is the only repair that could change Tuyền **without inventing a Mộc rule** (counterfactual `str_003` → Ất). Requires an explicit PO yes/no. Default without that yes: **do not change Tuyền.**
2. **`jia_wang` vs `spc_004` list:** if chuyên Thổ is already a canonical Pattern token, adding it to the existing `in` list is a reachability fix, not new theory.

### Can defer V1.1 (new theory — do not author in a freeze rush)

- Strong Hao (Chính Tài / Thiên Tài) row(s).
- Strong Thất Sát Chế row, **or** an explicit written decision that Chế V1.0 is Chính Quan only.
- Pattern-main UG mapping (including `kiep_tai`).
- Thương Quan as selectable Tiết, not only Hỷ.
- Flow competitiveness / excess semantics.
- Wiring bz_06/bz_07.

Do **not** turn this into a Useful God rewrite. Do **not** hard-code Tuyền → Mộc. Do **not** restore season Overall.

---

## 24. Not done (as ordered)

No Strength retune. No season/temperature Overall. No Tuyền Mộc. No new CSV rows. No priority edits. No Golden / snapshot / expected edits.

---

## Files / evidence

Live traces: production pipeline on five PO cases + 101 golden **inputs**.  
Related: `UG_R2_*`, `G1_06_USEFUL_GOD_AUDIT.md`.
