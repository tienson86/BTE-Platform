# G1-PREFINAL — Contract cleanup report

**Date:** 2026-08-20  
**Live customer Useful God contract:** `analysis_result.UsefulGodView@1.5`  
**PO prompt mentioned @1.4:** stale relative to HK-R1H, which published `@1.5`.

No analytical engine was retuned in this phase.

---

## 1. Stale tests updated to Frozen Truth

| Test file | Old expectation | New expectation | Frozen Truth source |
|-----------|-----------------|-----------------|---------------------|
| `tests/useful_god/test_g1_06_useful_god_binding.py` | Customer Hỷ starts with Dụng; contract `@1.2` | Customer Hỷ = insufficient; canonical Hỷ kept; contract `@1.5` | HK-R1H; live `useful_god_truth.py` |
| `tests/useful_god/test_hk_r1f_customer_hy.py` | Dũng Hỷ = Quý/Thương Quan; Tuyền Hỷ = Canh/Thực Thần | Both customer Hỷ = insufficient | HK-R1H |
| `tests/useful_god/test_hk_r1g_reasoning.py` | Dũng `HY_ROLE_SUPPORTED` + Quý; Trường keeps Thiên Ấn | Dũng `STATIC_SAME_ELEMENT`; Trường `Thủy · Nhâm · Tỷ Kiên` only | HK-R1H |
| `tests/useful_god/test_ug_r3f_hidden_chinh_quan.py` | Tuyền customer Hỷ contains Thực Thần | Thực Thần on canonical display only | UG-R3F + HK-R1H |
| `tests/report_engine/test_g1_06_useful_god_binding.py` | HTML Hỷ = concatenated Dụng/Hỷ | Customer insufficient; concatenated Dụng/Hỷ must not appear | HK-R1H |
| `tests/report_engine/test_case_0001_report_input.py` | Snapshot ignored `useful_god` | Snapshot includes customer Hỷ + `short_reason` | UG-R3F + HK-R1H |
| `tests/five_elements/test_g1_05_five_elements_binding.py` | `useful_god=Bính`, climate display as Overall | Overall `Chính Quan` / `Hỏa · Đinh · Chính Quan`; climate separate | G1-06 / UG-R2 |
| `tests/strength/test_g1_02r_strength_correctness.py` | 1960-07-01 month `Tử`, `sea_005`, weak | CAL-P0B month `Tướng`, `sea_002`, balanced 0.37 | CAL-P0B |
| `tests/production/test_p0_analytical_truth.py` | Huỳnh strong 0.66 / Đinh / sea_004 / Hỷ Đinh-Bính-Ất | balanced 0.64 / Chính Tài / str_005 / customer insufficient | G1-02R + UG-R2 + HK-R1H |
| `tests/production/test_p1_calendar_data_recovery.py` | Same Huỳnh P0 strings; Five Elements from `wuxing_series` | Frozen Huỳnh; analytical `five_elements` source | G1-02R + G1-05 |
| `tests/production/test_sprint4_composition.py` | Sơn Dụng Thực Thần; strength-copy divergence | Sơn Dụng Chính Quan; Useful God/Pattern divergence | UG-R2 |
| `tests/production/test_cross_domain_reasoning.py` | `follow_qualifies_strength` tension | `str_pattern_scope` / `tg_vs_pattern_scope` | G1-X01 / PAT-R1F |
| Interpretation Huỳnh/Sơn suites | Đinh/sea_004/strong/Thực Thần as Overall | Chính Tài / str_005 / balanced; Sơn Chính Quan | UG-R2 + G1-02R |
| Portal `canonical_desktop.test.tsx` | English `Critical` / `Observation` | `Ưu tiên cao` / `Quan sát` / `Tác động` / `Gợi ý` | V1 customer copy |
| Portal ten-gods / Hỷ / strength labels | Bare god names; internal Hỷ; `CÂN BẰNG` | `— Lộ rõ`; customer Hỷ; `Thân cân bằng` / `Thân vượng` | G1-01 + HK-R1H + G1-02 |

---

## 2. Contract matrix

| Surface | Contract version | Live? | Canonical? | Deprecated? |
|---------|------------------|-------|------------|-------------|
| API Analyze `useful_god_source.contract` | `analysis_result.UsefulGodView@1.5` | **Yes** | **Yes** | No |
| `UsefulGodView` fields `favorable_display` vs `canonical_favorable_display` | @1.5 | Yes | Yes — customer vs internal | No |
| `ReportInputV1.report_version` | `1.0` | Yes | Yes for HTML/PDF/DOCX | No |
| `AnalysisResult.contract_version` | `1.0` | Yes | Envelope only | No |
| Portal launch_08 / launch_04 fixtures | `UsefulGodView@1.0` | No | No — copy/smoke fixtures | **Yes** (synthetic) |
| Tests asserting `@1.2` | `@1.2` | No | No | **Removed** (updated to @1.5) |
| PO G1-PREFINAL prompt `@1.4` | `@1.4` | No | No | Stale vs HK-R1H @1.5 |
| Knowledge package tests | various | N/A | Not Gate-1 runtime | Legacy |

Internal `favorable_gods` remains the engine remainder list (may include Overall Dụng token). Customer Hỷ is only `favorable_display`. Portal/Report copy `favorable_display` and must not fall back to `favorable_gods`.

---

## 3. Presentation-only copy change

`KY_SCOPE_NOTE` in `engines/useful_god_engine/presentation.py`:

- old: `Kỵ thần theo rule cân bằng hiện tại`
- new: `Kỵ thần theo quy tắc cân bằng hiện tại`

Kỵ **values** unchanged. English `rule` was leaking into customer HTML/DOCX (`test_presented_report_has_no_customer_rule_ids`). This is contract wording, not Kỵ algorithm.

---

## 4. What was not changed

Strength CSV, Pattern CSV, Useful God winner CSV, Temperature, Five Elements calculator, Ten Gods mapping, ShenSha, Luck, Calendar Month Pillar SSOT.
