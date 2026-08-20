# UG-R4 — Strong Day Master Hao / Tài knowledge audit

**Date:** 2026-08-20  
**Phase:** 1 — knowledge audit only. **No engine, CSV, or priority change.**  
**Subject chart:** Lương Văn Mạnh — `Đinh Mão / Đinh Mùi / Kỷ Dậu / Đinh Mão` · Nhật Chủ **Kỷ**.  
**Reference report:** not an oracle. Not used to select a rule.

## Status

**`UG-R4: NO CANONICAL HAO USEFUL-GOD KNOWLEDGE — V1.1 KNOWLEDGE AUTHORING REQUIRED`**

Phase 2 **not executed**.

Adding a strong→Tài / Hao Overall path would be **new Useful God theory**. Existing canonical selection assigns Tài to **balanced** (`str_005` / `cand_ug_wealth_balanced`) and **Tòng Tài** (`spc_001`), not to strong.

Do not start G1-FINAL. Do not update Golden.

---

## 1. Search scope

Searched (no web theory):

- `knowledge/packages/useful_god/` (`cand_ug_*`, Hỷ/Kỵ packs, reasoning)
- `knowledge/interpretation/domains/useful_god/` (`chinh_tai.json`, `thien_tai.json`, …)
- `knowledge/interpretation/concepts/core/` (`wealth_role`, `drain_strong_day_master`, `output_role`, `officer_role`, `control_excess`)
- `knowledge/interpretation/domains/pattern/jia_wang.json`
- `knowledge/rule_database/05_useful_gods/` (framework, **zero records**)
- `database/13_useful_god/` (production UG V2)
- `database/12_strength/` (`Tài tinh hao thân`)
- `database/05_phan_tich/05_dung_than/` (legacy Dụng thần CSV)
- `database/20_knowledge/08_useful_god.csv` (empty header)
- UG-R2 / UG-R3 / UG-R3F gate reports
- Strength knowledge packs (`Tài hao thân` explanations)

---

## 2. Classification of findings

### A — Canonical Useful God selection (strong → Tài / Hao)

**None.**

Closest canonical statements **exclude** that path:

| Source | What it says |
|--------|----------------|
| `database/13_useful_god/01_strength_rules.csv` `str_005` | `strength_level == balanced` → Chính Tài. Not strong. |
| `knowledge/packages/useful_god/foundation/rules/candidate_useful_gods.json` `cand_ug_wealth_balanced` (UGD-000026) | `strength_score` 36–64 → Chính Tài. Band **stops at 64**. Strong is ≥65. |
| `cand_ug_officer_strong` (UGD-000024) | strong ≥65 → **Chính Quan** (Chế). |
| `cand_ug_output_strong` (UGD-000025) | very strong ≥70 → **Thực Thần** (Tiết). |
| `cand_fav_officer_set` (UGD-000034) | strong ≥65 Hỷ = **Chính Quan, Thực Thần**. Not Tài. |
| `knowledge/interpretation/domains/useful_god/chinh_tai.json` `evidence_notes` | “Engine chọn Chính Tài ở **str_005 (thân trung hòa)** và **spc_001 (tòng tài)**. Knowledge không đổi lựa chọn.” |

There is **no** `cand_ug_wealth_strong` and **no** `str_*` with `strong` + Chính Tài / Thiên Tài.

### B — Supporting knowledge (Hao exists, not UG selection)

| Source | Class | Note |
|--------|-------|------|
| `database/12_strength/05_flow_rules.csv` `flw_002` | B | `drain_type == Tài tinh hao thân` → Strength **penalty**, not Dụng. |
| `flw_004` | B | `wealth_elements contains Thiên Tài` → Strength penalty “Tài hao thân”. |
| `database/12_strength/04_control_rules.csv` `ctl_003` | B | `Bị Tài tinh hao` — Strength control penalty. |
| `knowledge/packages/strength/core/rules/element_restriction.json` | B | “Quan khắc, Thực tiết, Tài hao…” — strength restriction copy. |
| `knowledge/packages/strength/core/evidence/explanations/hidden_stem_support.json` | B | “Tàng can Tài hao thân.” |
| `knowledge/interpretation/concepts/core/wealth_role.json` | B | Tài = nguồn / lưu thông. `related_to` `drain_strong_day_master`. Does **not** say strong Overall = Tài. |
| `database/05_phan_tich/05_dung_than/tai_lieu_tham_chieu.md` §VI | B | Ngũ hành vocabulary lists Sinh / Khắc / **Tiết** / **Hao** / Trợ. Ontology names, not a UG row. |
| `database/05_phan_tich/05_dung_than/cau_truc.md` | B | Strength scoring uses “tiết hao” as a **strength input**, not Overall Dụng. |
| `database/05_phan_tich/05_dung_than/02_dieu_kien_chon.csv` `DT003` | B | Thân **Vượng** → “Ưu tiên hành **tiết** Nhật Chủ” (output). |
| `DT004` | B | Thân **Vượng** → “Ưu tiên hành **khắc** Nhật Chủ” (officer/Chế). **No** “Nhật Chủ khắc” (Hao) row. |
| `DT026` | B | “Ngũ hành mất cân bằng → Tăng hành thiếu.” Generic missing-element, **not** Hao, **not** loaded by UG V2. |

### C — Historical / reference only

| Source | Note |
|--------|------|
| UG-R2 / UG-R3 coverage matrices | Already recorded Hao **ABSENT** as Overall. Audit, not a rule. |
| Pilot Strength calibration JSON (`drain_type: Tài tinh hao thân`) | Strength evidence, not UG. |
| Editorial / narrative copy “thân vượng cần tiết xuất” | Tiết language, not Hao. |
| External reference report for Mạnh (Dụng Thủy, Hỷ Kim) | Case text. Not canonical. |

### D — No knowledge

- `knowledge/rule_database/05_useful_gods/`: framework only; **Next Free ID RUL-000400; allocated records: none.**
- `database/20_knowledge/08_useful_god.csv`: header only.
- No project sentence equivalent to 身旺用财 / “thân vượng dụng Tài” as a **Useful God decision**.

---

## 3. Existing Useful God rule inventory

Production loader: `database/13_useful_god` only. All listed rows `status=active`, `enabled=true`. No disabled strong-wealth row.

| Rule | Active? | Condition | Candidate | Role | Reachable? |
|------|---------|-----------|-----------|------|------------|
| `str_001` | yes | weak + `resource_elements contains Chính Ấn` | Chính Ấn | SUPPORT | yes |
| `str_002` | yes | weak | Thiên Ấn | SUPPORT fallback | yes (every weak) |
| `str_003` | yes | strong + `officer_elements contains Chính Quan` | Chính Quan | CHẾ | yes when CQ visible or hidden (UG-R3F) |
| `str_004` | yes | strong | Thực Thần | TIẾT | yes (**every** strong) |
| `str_005` | yes | **balanced** | Chính Tài | WEALTH / lưu thông | yes (every balanced). **Not strong.** |
| `spc_001` | yes | `follow_pattern == tong_tai` | Chính Tài | SPECIAL follow | yes if G1-X01 publishes token |
| `spc_002` | yes | `tong_quan` | Chính Quan | SPECIAL | yes |
| `spc_003` | yes | `tong_sat` | Thất Sát | SPECIAL | yes |
| `spc_004` | yes | `special_pattern in {khuc_truc, viem_thuong, nhuan_ha, gia_sac}` | Thiên Ấn | SPECIAL | yes; **jia_wang omitted** (UG-R3F) |
| `flo_001`–`004` | yes | unique-max element | 克 stem | FLOW | candidate only; never Overall |
| `sea_*` / `tmp_*` | yes | season / temperature | climate stems | ĐIỀU HẬU | climate layer only (UG-R2) |

**Strong→Tài rule:** never existed in production CSV. Not unreachable; **not authored**.

Knowledge pack mirrors CSV: wealth candidate is **balanced-only**. This is **not** `KNOWLEDGE-TO-RUNTIME GAP`. Runtime matches the pack.

---

## 4. Candidate knowledge pack

`knowledge/packages/useful_god/foundation/rules/candidate_useful_gods.json` (11 rules).

Strong-related:

| Code | Trigger | Outcome | Role |
|------|---------|---------|------|
| `cand_ug_officer_strong` | score ≥ 65 | Chính Quan | Chế |
| `cand_ug_output_strong` | score ≥ 70 | Thực Thần | Tiết |
| `cand_ug_pattern_good_officer` | good/excellent pattern **and** ≥ 65 | Chính Quan | Chế |
| `cand_ug_wealth_balanced` | 36–64 | Chính Tài | Hao **only when not strong** |
| `cand_ug_pattern_average_wealth` | average pattern **and** 36–64 | Chính Tài | same |

**No** `strong + wealth` / `strong → wealth element` candidate.

---

## 5. Theory role — Tiết / Hao / Chế

Documented **Useful God** alternatives for **strong**:

| Path | Meaning | Canonical UG? |
|------|---------|---------------|
| Tiết | Nhật Chủ sinh → Output (Thực Thần) | **Yes** `str_004` / `cand_ug_output_strong` |
| Chế | Quan/Sát khắc Nhật Chủ | **Partial yes** `str_003` / `cand_ug_officer_strong` — **Chính Quan only** |
| Hao | Nhật Chủ khắc → Tài | **No UG rule** |

Hỷ pack for strong (`cand_fav_officer_set`) lists **Quan + Thực**, i.e. Chế and Tiết as the two helpers — not Tài.

Legacy `DT003` (tiết, prio 100) and `DT004` (khắc Nhật Chủ, prio 90) are the same two paths. Hao would be “Nhật Chủ khắc”; that row does not exist.

**Are Tiết / Hao / Chế intended as alternative Overall paths for strong?**

**No — not as a three-way UG set.** Repository evidence supports Tiết and Chế only. Hao is a Strength drain label and a ngũ hành vocabulary term.

---

## 6. Lương Văn Mạnh — canonical structural facts

Chart (given): **Đinh Mão / Đinh Mùi / Kỷ Dậu / Đinh Mão**. DM **Kỷ** (Âm Thổ).  
G1-01 / hidden stems = `database/09_hidden_stems` = Pattern `_BRANCH_HIDDEN`.

### Support

| Item | Fact |
|------|------|
| Month / season | Mùi → late summer; branch element **Thổ** (peer to DM) |
| Pattern gate | Earth DM + Earth month + no officer in Pattern `officer_elements` → `jia_wang` / Giá Vượng (`spe_jw_01`) |
| Visible Resource | Year/month/hour **Đinh** = **Thiên Ấn** (Fire sinh Earth, cùng âm) |
| Hidden Resource | Mùi **Đinh** = Thiên Ấn again |
| Peer | Day DM Kỷ = Tỷ Kiên; Mùi hidden **Kỷ** = Tỷ Kiên |
| Chính Ấn | **Bính** would be Chính Ấn; **not on chart** |

### Tiết

| Item | Fact |
|------|------|
| Dậu | bản hành **Kim**; hidden **Tân** = **Thực Thần** (Kỷ × Tân) |
| Visible Output | none (no Canh/Tân on thiên can) |
| `str_004` | does **not** require Output to appear; maps Thực Thần → **Tân / Kim** |

Current Overall **Kim · Tân · Thực Thần** is this path.

### Hao

| Item | Fact |
|------|------|
| Nhâm / Quý | **none** visible or hidden |
| Thủy branch | no Hợi / Tý |
| Wealth ten gods | **none** |
| G1-05 Thủy | **0** |

### Chế

| Item | Fact |
|------|------|
| Ất | hidden in **Mão** (year + hour) and **Mùi** (month) |
| Kỷ × Ất | **Thất Sát** (Wood khắc Earth, cùng âm) |
| Giáp | would be **Chính Quan**; **absent** |
| `str_003` | requires **Chính Quan**, not Thất Sát → **not eligible** |

### G1-05 occurrence (can + bản hành chi + tàng can)

**Mộc 5 · Hỏa 4 · Thổ 3 · Kim 2 · Thủy 0** (matches the stated BTE distribution). Disclaimer unchanged: count is **not** Dụng.

---

## 7. Thủy = 0

G1-05 invariant holds: **no Water occurrence**.  
It does **not** mean Water must be Useful God.

No canonical UG rule creates a candidate from a zero count.

---

## 8. Absent-element candidate

| Layer | Behavior |
|-------|----------|
| Production UG | **Mixed.** `str_003` / `str_001` require the Ten God **on context lists**. `str_002` / `str_004` / `str_005` map the token via G1-01 **even if the stem is not natal**. |
| Legacy `DT026` / `DT029` | “Tăng hành thiếu” / “Giảm hành không căn” — **not loaded** by Useful God Engine V2. |
| G1-05 copy | Absence is structural fact, not auto-Dụng. |

If a Hao path were ever authored, **presence vs reverse-mapping is unspecified**. Mạnh has **no natal Tài**. Choosing “allow absent Water” vs “require Tài on chart” would be new knowledge.

---

## 9. Stem selection — Nhâm vs Quý (G1-01, Kỷ)

| Stem | Element | Ten God vs Kỷ |
|------|---------|----------------|
| **Nhâm** | Thủy Dương | **Chính Tài** |
| **Quý** | Thủy Âm | **Thiên Tài** |

No Hao UG row exists, so this mapping is **factual only**.

**`ELEMENT PATH EXISTS — STEM SELECTION KNOWLEDGE MISSING`** does not apply as a Hao *path* (the path is missing).  
If V1.1 authors Hao: **STEM SELECTION KNOWLEDGE MISSING** for strong (which polarity). Do not pick Nhâm because the old report says “Thủy”.

Climate `sea_002` maps **Nhâm** for summer/hot — that is **Điều hậu**, not Overall stem choice.

---

## 10. Chính Tài vs Thiên Tài

Existing UG theory:

| Context | Token |
|---------|--------|
| Balanced Overall | **Chính Tài** (`str_005`, `cand_ug_wealth_balanced`) |
| Tòng Tài | **Chính Tài** (`spc_001`); Thiên Tài is Hỷ |
| Weak | Tài is **Kỵ** (`str_001`/`str_002`) |
| Strong | **neither** is Overall |

No strong Hao preference. No invention.

---

## 11–12. Priority vs `str_004` / `str_003`

Existing Overall (structural) order that **is** documented:

| Rule | Row prio | Group prio | Role |
|------|--------:|-----------:|------|
| `str_003` | 82 | 80 | Chế if Chính Quan |
| `str_004` | 76 | 80 | Tiết fallback |
| `str_005` | 70 | 80 | Tài **balanced only** |

No Hao row. No document that Chế > Hao > Tiết.

**`PRIORITY/RECONCILIATION KNOWLEDGE GAP`** — cannot implement a Hao competitor without inventing a number (forbidden in Phase 2 §22).

Tuyền / Sơn already win `str_003`. A later Hao rule with unknown priority could override valid Chế. **Do not add it.**

---

## 13. Pattern — Giá Vượng / `jia_wang`

| Source | Link to Water / Tài? |
|--------|----------------------|
| `database/14_pattern/02_special_pattern.csv` `spe_jw_01` | Earth DM + Earth month + empty Pattern officers. No UG token. |
| `knowledge/interpretation/domains/pattern/jia_wang.json` | “chứa có động”; wealth application “Thiên giữ / đọng”. **Not** “Dụng Thủy”. |
| `spc_004` | Four chuyên codes; **jia_wang omitted** (UG-R3F). **Do not add here.** |

No existing UG rule: Giá Vượng → Thủy / Tài.

---

## 14. Điều hậu vs structural Hao

Mạnh month Mùi → summer / hot → climate **`sea_002` Nhâm / Thủy** (Nhiệt · Cần làm mát · ưu tiên Thủy).

UG-R2: Điều hậu ≠ Overall.

**Hypothetical:** if a structural Hao path for Kỷ were Water, climate Water and Hao Water would **converge**. That is **not** evidence to author Hao. Label only as:

`INDEPENDENT THEORY CONVERGENCE` — **conditional on a Hao rule that does not exist.**

Current Overall remains Tiết (Kim), climate remains Thủy. Split is correct.

---

## 15. Reference report (after audit)

Reference: strong Kỷ; Dụng Thủy; Hỷ Kim; Kỵ Hỏa / Thổ.

| Piece | Closest BTE analogue |
|-------|----------------------|
| Dụng Thủy | Hao (Earth khắc Water) **and/or** climate `sea_002` |
| Hỷ Kim | Tiết / current `str_004` candidate |
| Kỵ Hỏa / Thổ | Resource + Peer (Ấn / Tỷ) — typical “don’t add more body” |

**Classification: mixture** (Hao-style Dụng + Tiết as Hỷ + climate Water).  
Not importable. Weights not used.

---

## 16. Control — Vũ Thị Thanh Tuyền (counterfactual)

After UG-R3F: **Mộc · Ất · Chính Quan** via `str_003` (hidden Mùi Ất).

A Hao rule with unspecified priority could beat 82. **Must not blindly override Chế.** No code change.

---

## 17. Control — Nguyễn Tiến Sơn (counterfactual)

After UG-R3F: **Hỏa · Đinh · Chính Quan** via `str_003` (hidden Ngọ Đinh).

Same risk. No code change.

---

## 18. 101-case strong coverage

Live recompute `tests/golden_dataset/inputs` (n=101). Golden not edited.  
**Strong = 52.**

**Candidate availability under existing UG knowledge:**

| Candidate availability | Count |
|------------------------|------:|
| Tiết only | 7 |
| Chế + Tiết | 45 |
| Hao + Tiết | **0** |
| Chế + Hao + Tiết | **0** |
| Other | 0 |

Tiết = `str_004` always matches strong.  
Chế = `officer_elements` contains Chính Quan after UG-R3F.  
Hao = **no existing UG candidate**.

Strong Overall winners (post-R3F): `str_003` 40 · `spc_004` 8 · `str_004` 4.

Natal **wealth star** (visible or hidden Chính/Thiên Tài) is a Strength/chart fact, **not** a UG Hao candidate: present 49 / absent 3 (`case_0065`, `case_0074`, `case_0086`). Mạnh’s Thủy0 / no Tài is in this **absent-star** family but is **not** in the 101 file set.

**Hao gap is systemic** (0/52 strong UG Hao candidates), not a Mạnh-only miss.

---

## 19. Decision

Not **A**: knowledge pack and `chinh_tai.json` assign Tài to **balanced / tòng**, and runtime already does that. There is no unimplemented strong→Tài rule.

Not **B** as the primary status: Hao as **Strength drain** is complete for scoring; what is missing for Overall is **selection theory**, not a half-written UG row. Treating Strength “Tài hao thân” as permission to publish Overall Tài would mix engines.

**C.** Authoring strong→Tài requires: token (Chính vs Thiên), presence vs absent mapping, priority vs `str_003`/`str_004`, and whether `jia_wang` participates. That is V1.1 knowledge work (already listed as UG-V1.1-KNOWLEDGE **A**).

---

## Phase 2

**Stopped.** No general Hao rule. No Mạnh hard-code. No `Thủy0 → Dụng Thủy`. No new priority.

Invariants preserved by inaction: climate ≠ Overall, hidden Chính Quan, G1-X01, Strength/Pattern/G1-05, no missing-element auto-Dụng.

---

## Deliverables this phase

- `release/gate_01/UG_R4_STRONG_HAO_KNOWLEDGE_AUDIT.md` (this file)

Not created (Phase 2 skipped): repair report, 101 regression, refreeze checklist.
