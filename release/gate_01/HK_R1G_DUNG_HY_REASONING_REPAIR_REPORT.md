# HK-R1G — Dụng reasoning + Hỷ role semantics

**Date:** 2026-08-20  
**Scope:** Presentation / customer semantics only.  
**Not in scope:** winner selection, CSV, Kỵ algorithm, Golden, G1-PREFINAL / G1-FINAL.

## Status

**HK-R1G: DỤNG REASONING + HỶ ROLE SEMANTICS REPAIRED — V1.0 SEMANTIC FREEZE READY**

Do **not** start G1-PREFINAL. Do **not** update Golden.

---

## Phase 1 — live screenshot cause (Dũng)

Live Result/PDF still showed:

```
Dụng: Thủy · Nhâm · Thực Thần
Hỷ:   Thủy · Nhâm · Thực Thần / Thủy · Quý · Thương Quan
```

That string is the **canonical engine** `favorable_display`, not the HK-R1F customer string.

| Hypothesis | Evidence |
|------------|----------|
| **A. Stale backend** | **Confirmed.** Uvicorn PID 8068 started **18:18** (before HK-R1F landed ~19:19). Process was never restarted, so `build_useful_god_view` still published full Hỷ. |
| B. Stale frontend bundle | Contributing only if API sent the old field. Portal copies `favorable_display`; it does not rebuild Hỷ from `favorable_gods`. |
| **C. Stale ResultStore** | **Confirmed as required companion.** Result page reads the last Analyze payload. A screenshot taken against the 18:18 API / stored payload would keep the duplicated Hỷ even after later code existed on disk. |
| D. PDF renderer bypass | **Not the cause on a fresh run.** Report V1 HTML/PDF copy View `favorable_display`. Old PDF would match the stale API. |
| E. Another adapter reconstructing Hỷ | Portal fallback to `favorable_gods` was already removed in HK-R1F. Not reconstructing on a fresh payload. |
| F. Repair not loaded | Same as A: repair was on disk, not in the running interpreter. |

This is **not** “cache” without proof: it is a **running Python process started before the repair**, plus **ResultStore holding that Analyze**.

**Fresh verification (this task):** backend restarted (PID 10776), Portal `npm run build:result`, new POST `/api/v1/analyze` (not ResultStore).

| Field | Fresh Dũng |
|-------|------------|
| Canonical Dụng | Thủy · Nhâm · Thực Thần |
| Canonical Hỷ | Thủy · Nhâm · Thực Thần / Thủy · Quý · Thương Quan |
| Customer Hỷ | **Thủy · Quý · Thương Quan** |
| Exact Dụng under Hỷ | **0** |
| Reason | Canh Kim thân vượng → Tiết → Kim sinh Thủy → Nhâm = Thực Thần |
| Điều hậu | Hỏa · Đinh · Chính Quan (separate; not merged into Overall) |
| Contract | `UsefulGodView@1.4` |

---

## 1. Canonical vs customer

Internal `favorable_gods` / engine `favorable_display` unchanged.

Customer Hỷ = exact-Dụng omit **then** independent-role gate.

---

## 2. Reasoning archetypes (existing rules only)

| Rule | Strength state | Archetype | Problem | Balancing relation | Candidate role |
|------|----------------|-----------|---------|--------------------|----------------|
| `str_001` | weak | SINH / TRỢ | nhược, cần dưỡng có Chính Ấn | useful sinh nhật chủ | Chính Ấn |
| `str_002` | weak | SINH / TRỢ | nhược, fallback Thiên Ấn | useful sinh nhật chủ | Thiên Ấn |
| `str_003` | strong | CHẾ | vượng + Chính Quan reachable | useful khắc nhật chủ | Chính Quan |
| `str_004` | strong | TIẾT | vượng, đường thường Tiết | nhật chủ sinh useful | Thực Thần |
| `str_005` | balanced | BALANCED-WEALTH | trung hòa, lưu thông | nhật chủ khắc Tài | Chính Tài |
| `spc_001` | follow | FOLLOW / SPECIAL | Tòng Tài | follow Tài | Chính Tài |
| `spc_002` | follow | FOLLOW / SPECIAL | Tòng Quan | follow Quan | Chính Quan |
| `spc_003` | follow | FOLLOW / SPECIAL | Tòng Sát | follow Sát | Thất Sát |
| `spc_004` | special | FOLLOW / SPECIAL | chuyên Ấn (not a live Overall after PAT-R1F) | — | Thiên Ấn |

No Hao archetype (no V1.0 Hao Overall). No rule IDs on the customer card.

Wording uses **“theo mô hình cân bằng V1.0”**. Does not claim the only possible Dụng.

---

## 3. Reasoning chain

STATE → NEED → PRINCIPLE → ELEMENT RELATION → STEM / TEN GOD → RESULT

SSOT: `engines/useful_god_engine/reasoning.py`  
Published on View: `short_reason`, `reason_archetype`, `customer_reason` (no `rule_id`).

---

## 8–11. Hỷ role policy

Knowledge used (no invention):

- `output_role` — Thực Thần / Thương Quan cùng nhóm hỗ trợ kênh thoát  
- `officer_role` — Chính Quan / Thất Sát  
- `resource_role` — Chính Ấn / Thiên Ấn  
- `wealth_role` — Chính Tài / Thiên Tài  
- `companion_role` + `support_day_master` — Tỷ/Kiếp as Hỷ on SINH/TRỢ only  

| Class | Customer |
|-------|----------|
| Exact Dụng | remove |
| SUPPORTED_ROLE | display |
| STATIC_FAVORABLE_ONLY / UNKNOWN | `Chưa đủ căn cứ tách Hỷ thần bổ trợ riêng` |

**Not implemented:** hide Hỷ because element == Dụng element.

Dũng remaining Quý / Thương Quan is **SUPPORTED_ROLE** (sibling Output of Thực Thần), even though the element is also Thủy. That is Ten God group support, not “another Water because Water.”

Tuyền remaining Thực Thần under Chính Quan Dụng is **STATIC_FAVORABLE_ONLY** (CSV leftover; no approved concept that Output independently supports Officer Dụng). Customer Hỷ is the insufficient state — not Canh/Thực Thần presented as a justified Hỷ.

---

## 12. Kỵ

Algorithm unchanged. Customer row **Phạm vi Kỵ**: `Kỵ thần theo rule cân bằng hiện tại`.

Technical limitation unchanged: Kỵ V1.0 follows the selected structural row and does not yet perform full-chart reconciliation.

---

## 14. Customer card (shared)

```
Dụng thần
Căn cứ chọn Dụng
Hỷ thần
Kỵ thần
```

Portal Canonical Desktop S02 + Full Report HTML; Report V1 HTML / PDF / DOCX section 07.

---

## Control reasoning (winners unchanged)

**Ngô Đắc Dũng** — `str_004` / TIẾT. Canh Kim is strong. V1.0 ordinary structural path uses Tiết. Kim sinh Thủy. Nhâm relative to Canh = Thực Thần. Customer: Dụng theo mô hình cân bằng V1.0. Does **not** claim Thủy is the only possible Dụng. Điều hậu remains Hỏa · Đinh · Chính Quan / ưu tiên Hỏa — not merged with Overall. Customer Hỷ: Quý / Thương Quan (SUPPORTED sibling Output).

**Vũ Thị Thanh Tuyền** — `str_003` / CHẾ. Strong Earth. Chế is valid because canonical Chính Quan exists. Mộc khắc Thổ. Ất maps to Chính Quan. Remaining Thực Thần is STATIC leftover, not a justified Hỷ.

**Cao Xuân Trường** — `str_001` / SINH / TRỢ. Weak Water needs support. Kim sinh Thủy. Tân maps to Chính Ấn. Strength not reopened.

**Lưu Hoàng Sơn / Đoàn Quang Hưng / Lương Ngọc Huỳnh** — `str_005` / BALANCED-WEALTH. Current V1.0 model is balanced → Chính Tài / circulation. Customer chain says it does not deep-reconcile the whole chart. That limitation stays in technical docs.

---

## Files changed

| File | Role |
|------|------|
| `engines/useful_god_engine/reasoning.py` | archetype + short chain |
| `engines/useful_god_engine/presentation.py` | Hỷ role gate + overlay text |
| `applications/api/services/useful_god_truth.py` | View `@1.4` |
| `applications/api/models/analysis_result.py` | `short_reason` / `customer_reason` / `hy_role_status` |
| `engines/pattern_engine/rule_context_bridge.py` | overlay Hỷ uses same policy |
| `engines/report_engine/contracts/report_input_v1.py` | report fields |
| `engines/report_engine/adapters/report_input_v1_adapter.py` | copy reason |
| `engines/report_engine/rendering/report_sections_v1.py` | card rows |
| Portal `canonicalUsefulGod.ts`, `canonicalDesktopAdapter.ts`, `fullReportViewModel.ts` | copy published reason / Hỷ |
| `tests/useful_god/test_hk_r1g_reasoning.py` | new |

**Not changed:** Strength, Pattern winner, Useful God CSV, engine `favorable_gods`, Kỵ lists, climate, Golden.

---

## Tests

```
python -m pytest tests/useful_god -q
40 passed, 3 failed
```

New HK-R1G tests pass. Remaining failures are **existing** asserts that customer `favorable_display` still contains Dụng or Tuyền `Thực Thần` leftover. Not edited.

---

**HK-R1G: DỤNG REASONING + HỶ ROLE SEMANTICS REPAIRED — V1.0 SEMANTIC FREEZE READY**
