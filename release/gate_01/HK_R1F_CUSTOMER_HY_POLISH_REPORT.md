# HK-R1F — Dụng / Hỷ customer semantic polish

**Date:** 2026-08-20  
**Scope:** Customer presentation only.  
**Not in scope:** Useful God Engine redesign, CSV, canonical `favorable_gods`, Kỵ rules, Golden, G1-FINAL.

## Status

**HK-R1F: DỤNG/HỶ CUSTOMER SEMANTICS REPAIRED — HỶ/KỴ V1.0 FREEZE READY**

Do **not** start G1-FINAL. Do **not** update Golden.

---

## Product Owner decision implemented

HK-R1 proved Hỷ/Kỵ are copied from the Overall winner row, and that 101/101 charts repeated the exact Dụng triple as the first Hỷ line.

V1.0 repair:

- Keep internal `UsefulGodResult` unchanged.
- When building **customer** Hỷ, omit **only** an entry that is an exact semantic duplicate of Overall Dụng (same element + stem + Ten God).
- Same-element remainder with a different stem or Ten God is kept.
- If the remainder is empty, show `Chưa có Hỷ thần bổ trợ riêng`. Never reinsert Dụng.
- Kỵ stays winner-row output. No V1.0 Kỵ completeness work.

---

## 1. Canonical internal data — unchanged

| Field | After HK-R1F |
|-------|----------------|
| `UsefulGodResult.useful_god` / `useful_display` | unchanged |
| `favorable_gods` / `favorable_roles` | unchanged (still includes Dụng token) |
| `favorable_display` on the **engine result** | unchanged full formatted set |
| `unfavorable_gods` / `unfavorable_display` | unchanged |
| Winning rule / CSV | unchanged |

API View now publishes:

- `favorable_gods` — internal set
- `canonical_favorable_display` — full engine Hỷ (includes Dụng)
- `favorable_display` — **customer** Hỷ (exact Dụng omitted)

Contract fingerprint: `analysis_result.UsefulGodView@1.3`.

---

## 2. One presentation builder

SSOT: `engines/useful_god_engine/presentation.py`

```
Canonical Engine
  → favorable set unchanged
  → customer_favorable_display / customer_favorable_tokens
  → UsefulGodView.favorable_display
  → Portal / Report / HTML / PDF / DOCX / Pattern overlay hy_than / narrative
```

Consumers copy the published customer string. They do **not** independently filter Hỷ.

Safety (no second filter — prevent reinsertion):

- Portal `canonicalFavorableDisplay` no longer falls back to internal `favorable_gods`.
- Report adapter / HTML sections no longer join `favorable_gods` when display is blank; they use the empty-state string.

---

## 3. Exact-duplicate rule

Omit only when all three are non-empty and equal:

- element
- stem
- Ten God

Example (Ngô Đắc Dũng):

| Layer | Value |
|-------|--------|
| Dụng | Thủy · Nhâm · Thực Thần |
| Internal Hỷ | Thủy · Nhâm · Thực Thần / Thủy · Quý · Thương Quan |
| Customer Hỷ | Thủy · Quý · Thương Quan |

Nhâm/Thực Thần and Quý/Thương Quan are both Thủy and are **not** collapsed.

---

## 4. Empty Hỷ safety

Implemented. Current 101-case remainder after exact-Dụng removal: **0 empty**. Future `[Dụng only]` will show:

`Chưa có Hỷ thần bổ trợ riêng`

---

## 5. Kỵ — no V1.0 repair

Kỵ remains canonical winner-row output.

**Technical limitation (not customer UI):**

> Kỵ thần V1.0 follows the selected structural Useful God rule and does not yet perform full-chart Kỵ reconciliation.

See `release/gate_01/HK_V1.1_RECONCILIATION_BACKLOG.md`.

---

## 6. Narrative

Useful God explainer and production composer use the **filtered customer Hỷ**.

Ngô Đắc Dũng live domain meaning:

- `Dụng thần chính: Thực Thần — trụ cột điều tiết hệ.`
- `Hỷ thần (Thương Quan) hỗ trợ duy trì cân bằng; …`

Not equivalent to “Dụng Thực Thần; Hỷ Thực Thần…”.

Internal decision-path “Preserve Hỷ / Kỵ” still records engine lists.

---

## 7. Surfaces (Sơn / Dũng live)

| Surface | Customer Hỷ | Exact Dụng under Hỷ |
|---------|-------------|---------------------|
| UsefulGodView / Result | filtered | no |
| ReportInputV1 | copies View | no |
| HTML | same presented section | no |
| DOCX | same presented section | no |
| PDF | same presented section | no |
| Canonical Desktop / Full Report | copy `favorable_display` | no |

Nguyễn Tiến Sơn: Dụng `Hỏa · Đinh · Chính Quan` remains on the Dụng line; customer Hỷ is `Thủy · Nhâm · Thực Thần`.

---

## Files changed

| File | Role |
|------|------|
| `engines/useful_god_engine/presentation.py` | SSOT exact-Dụng omission |
| `applications/api/services/useful_god_truth.py` | View customer `favorable_display` |
| `applications/api/models/analysis_result.py` | `canonical_favorable_display` |
| `engines/pattern_engine/rule_context_bridge.py` | overlay `hy_than` from customer tokens |
| `engines/interpretation_engine/foundation/interpreters/useful_god/explainer.py` | customer Hỷ sentences |
| `applications/production/interpretation/useful_god_composer.py` | customer Hỷ section |
| `engines/report_engine/adapters/report_input_v1_adapter.py` | no gods-join fallback |
| `engines/report_engine/rendering/report_sections_v1.py` | no gods-join fallback |
| `applications/customer_portal/src/adapters/canonicalUsefulGod.ts` | no gods-list fallback |
| `tests/useful_god/test_hk_r1f_customer_hy.py` | new module tests |

**Not changed:** Strength, Pattern winners, Useful God CSV, engine `favorable_gods`, Kỵ, Five Elements, Temperature, Điều hậu, Ten Gods, ShenSha, Luck, priorities, Golden.

---

## Tests

```
python -m pytest tests/useful_god -q
38 passed, 1 failed
```

New HK-R1F tests pass. Engine `favorable_display` (internal full set) still passes G1-06 engine asserts.

---

## Remaining failures (existing tests not edited)

| Test | Why |
|------|-----|
| `tests/useful_god/test_g1_06_useful_god_binding.py::test_api_payload_publishes_rich_fields` | API `favorable_display` is now customer Hỷ (`Thủy · Nhâm · Thực Thần`); test still expects it to start with Dụng. Contract string still `@1.2`. |
| `tests/report_engine/test_g1_06_useful_god_binding.py::test_case_0001_report_uses_rich_useful_god_not_dieu_hau` | Report Hỷ is customer-only. |
| `tests/report_engine/test_g1_06_useful_god_binding.py::test_case_0001_html_shows_three_layer_useful_god` | HTML no longer contains `Hỏa · Đinh · Chính Quan / Thủy · Nhâm · Thực Thần` as one Hỷ string. |

`test_case_0001_api_and_report_same_useful_god` **passes** — API and Report now share the same customer Hỷ.

Do not treat these as product defects. They encode the pre-HK-R1F “print Dụng again under Hỷ” contract.

---

## 101-case (live recompute)

See `release/gate_01/HK_R1F_101_CASE_REGRESSION.md`.

| Metric | Required | After |
|--------|----------|------:|
| Exact Dụng in customer Hỷ | 0 | **0** |
| Same-element distinct remainder preserved | keep | **27** |
| Empty customer Hỷ | report | **0** |
| Internal `favorable_gods` changed | 0 | **0** |
| Overall Dụng changed | 0 | **0** |
| Kỵ changed | 0 | **0** |

---

**HK-R1F: DỤNG/HỶ CUSTOMER SEMANTICS REPAIRED — HỶ/KỴ V1.0 FREEZE READY**
