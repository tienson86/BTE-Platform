# G1-07 — ShenSha Repair Report

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-07 Phase 2 |
| **Date** | 2026-08-20 |
| **Product decisions** | 1 = Option A (Quý Nhân canonical). 2 = Hồng Loan / Thiên Hỷ independent. 3 = structured evidence |
| **Canonical production** | `ShenShaService.evaluate` → `ShenShaDetectionResult` → `calculate()` name projection |
| **Status** | FINAL FREEZE READY |

No Calendar / BaZi pillar / Ten Gods / Strength / Temperature / Pattern / Useful God formula change. No Deep ShenSha interpretation. Không Vong remains out of the natal catalog.

---

## 1. Old name-only architecture

```text
BaziEngine.build
  → ShenShaService.calculate
  → list[str] via dict.fromkeys(stars)
  → BaziChart.shensha
  → Report evidence = name
  → Portal S07 Cát/Hung from a hardcoded hung set
```

One detector could append two labels (`Thiên Ất` + `Thiên Ất Quý Nhân`). Hồng Loan’s `if` also appended Thiên Hỷ. Positions were discarded.

---

## 2. Structured canonical model

Single path:

```text
ShenShaService.evaluate(...)
  → ShenShaDetectionResult.matches[]
       id, canonical_name, aliases,
       source_type/value, target_type/value,
       occurrences[] (pillar, location, target_value),
       rule_source, presence_label, evidence_text
  → calculate() = matches.canonical_names()   # legacy projection
  → BaziChart.shensha + shensha_result
  → BaziView.shensha + shensha_matches
  → Report / Portal copy
```

Each published star answers: **dựa vào đâu → gặp gì → ở đâu.**

---

## 3. Alias decisions (Option A)

| Canonical V1.0 | Legacy alias (not published) |
|----------------|------------------------------|
| Thiên Ất Quý Nhân | Thiên Ất |
| Thiên Đức Quý Nhân | Thiên Đức |
| Nguyệt Đức Quý Nhân | Nguyệt Đức |

One match → one entity. Aliases remain on the match for compatibility and knowledge lookup. `SHEN_SHA_KEYS` still lists 12 names for knowledge; `SHEN_SHA_PUBLISHED_KEYS` is the 9 emit names.

---

## 4. Hồng Loan bug

Production appended Thiên Hỷ from `HONG_LUAN_OPPOSITE`. CASE-0001 Dần → Sửu therefore published both names. Thiên Hỷ’s intended table (unused `bang_thien_hy.csv`) is Dần → **Mùi**.

---

## 5. Thiên Hỷ repair

Independent map `signal_maps.TIAN_XI_BRANCH` (same table as `bang_thien_hy.csv`). Hồng Loan and Thiên Hỷ are separate detectors. CASE-0001 has no Mùi → Thiên Hỷ is absent. Regression: Dần + Mùi → Thiên Hỷ; Dần + Sửu without Mùi → no Thiên Hỷ.

---

## 6. CASE-0001 before / after

Chart unchanged: Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần. Nhật chủ Canh.

| Before (8 names) | After (4 canonical matches) |
|------------------|-----------------------------|
| Thiên Ất Quý Nhân | **Thiên Ất Quý Nhân** · Có · trụ Tháng · Nhật can Canh → gặp Sửu |
| Thiên Ất | *(alias, not published)* |
| Hồng Loan | **Hồng Loan** · Có · trụ Tháng · Niên chi Dần → gặp Sửu |
| Thiên Hỷ | **removed** (no Mùi) |
| Thiên Đức | *(alias)* |
| Thiên Đức Quý Nhân | **Thiên Đức Quý Nhân** · Có · trụ Ngày · Nguyệt chi Sửu → gặp Canh |
| Nguyệt Đức | *(alias)* |
| Nguyệt Đức Quý Nhân | **Nguyệt Đức Quý Nhân** · Có · trụ Ngày · Nguyệt chi Sửu → gặp Canh |

Golden interpretation health line now lists the four canonical names. Conclusion score text moved `57.25` → `55.05` on the live ReportInput snapshot because alias double-publish no longer inflates ShenSha presence used by scoring copy — Score Engine formulas were not edited.

---

## 7. Occurrence preservation

Matches are grouped by canonical `id`. `occurrences[]` keeps every pillar hit. Name projection is one string per id. Test: Canh + Sửu at Year and Hour → one Thiên Ất Quý Nhân with two occurrences.

---

## 8. S07 Cát/Hung handling

Portal `HUNG_SHENSHA` was a renderer-invented hung set with no rule/evidence. Removed.

S07 now lists engine entries:

- name
- `presence_label` (Có · trụ …)
- `Căn cứ: evidence_text`

No tốt/xấu, hôn nhân, tài vận, nghề nghiệp, or cát/hung scoring.

---

## 9. Golden synchronization

Updated current V1 golden:

`tests/golden_dataset/report_v1/CASE-0001/expected_report_input.json`

Left historical G1-07 audit, pilot snapshots, and launch fixtures.

---

## 10. Tests

| Suite | Result |
|-------|--------|
| `pytest tests/bazi -q` | **PASS** (39) |
| `pytest tests/bazi/test_g1_07_shensha.py` | **PASS** (14 required cases) |
| `pytest tests/report_engine/test_case_0001_report_input.py` + adapter/html/localization | **PASS** |
| `pytest tests/interpretation_engine/knowledge/test_shensha_expert_domain_k6.py` | **PASS** |
| `pytest tests/rule_contract/test_context_builder.py` + matcher | **PASS** |
| `pytest tests/interpretation_engine/foundation/test_sprint_a_foundation.py::test_g_shensha_never_fabricates_evidence` | **PASS** |
| Portal `canonical_desktop_adapter.test.tsx` + `full_report_composition.test.ts` | **PASS** (17) |

---

## 11. Remaining V1.1 backlog

- Không Vong natal wiring from Calendar sexagenary `khong_vong` (not in V1.0 catalog).
- Tân missing from `TIAN_YI_BRANCHES` (六辛).
- Hoa Cái production formula still “day branch in earth storage”, not unused tam hợp CSV.
- Optional CSV loader for maps; `database/08_than_sat` still absent.
- Deep ShenSha interpretation (cát/hung meaning, hôn nhân, career).
- Knowledge JSON still has alias entity keys for lookup compatibility.

Unrelated, not repaired: `test_sprint_a_foundation` Huỳnh temperature label / score grade assertions (`Khí mát` vs `Địa chi tháng mát`, grade `C` vs `D+`) — outside G1-07.

---

**G1-07 STATUS: FINAL FREEZE READY**
