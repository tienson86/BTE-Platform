# G1-FINAL — Freeze manifest

**Release name:** BTE V1.0 — Gate 1 Core Engine  
**Freeze date/time:** 2026-08-20 21:30 +07  
**Baseline:** G1-PREFINAL PASS — READY FOR G1-FINAL  
**G1-FINAL analytical edits:** none

---

## Repo

| Item | Value |
|------|-------|
| Branch | `release/v1.0-final` |
| HEAD | `ed6dba05fd7683ed686c1d0035767ede6b5532f3` |
| HEAD message | Refine UsefulGod HY classification and wording |
| Working tree | G1-PREFINAL test/Golden/presentation-copy + this freeze pack are **uncommitted**. No G1-FINAL engine edit. |

---

## Truth dump / Portal bundle (verified, not regenerated)

| Artifact | Path | SHA256 | Match |
|----------|------|--------|-------|
| 101-case Frozen Truth | `release/gate_01/G1_PREFINAL_101_TRUTH.json` | `46386BC955119F5DFE9482E7D620767BFB8BB74003A0968A17A6F82017FFA5CC` | **yes** |
| Portal result bundle | `applications/customer_portal/static/dist/result.js` | `DE5BA4972962ACF38B5B19DD15D53BBB5D83E3CDCA726C191352E4827D0C134C` | **yes** |

---

## Customer contract

**`analysis_result.UsefulGodView@1.5`**

| Concept | Frozen source |
|---------|----------------|
| Dụng | Overall structural Useful God (`useful_display`) |
| Căn cứ chọn Dụng | canonical V1.0 reasoning chain (`short_reason` / `customer_reason`); wording includes `theo mô hình cân bằng V1.0` |
| Customer Hỷ | `favorable_display` only |
| Internal remainder | `favorable_gods` / `canonical_favorable_display` — **not** customer Hỷ |
| Kỵ | V1.0 structural-rule `unfavorable_*` values |
| Điều hậu | climate layer (`climate_display`); **≠** Overall |

No V1.0 hotfix may silently merge these concepts.

---

## Canonical modules

| Domain | Frozen SSOT |
|--------|-------------|
| Calendar Month Pillar | Lunar month + Ngũ Hổ Độn (`BTE-MONTH-PILLAR-LUNAR-V1.0` / CAL-P0B). Solar Terms remain for season, climate, Luck jie timing. 12-Tiết Month Pillar is **not** restored. |
| BaZi construction | Existing BaziEngine; not retuned |
| Ten Gods (G1-01) | 100/100 mapping. Day stem = Nhật Chủ. Same stem elsewhere (including hidden) = Tỷ Kiên. Hidden Ten Gods structured and preserved. Compact-name fields must not replace canonical hidden entries. |
| Strength (G1-02) | `strength.strength_score`. Three classes only: `weak` / `balanced` / `strong`. Canonical thresholds: `weak_threshold=0.35`, `strong_threshold=0.65`. No very-weak / very-strong / extreme **engine** taxonomy in V1.0. |
| Pattern | Ordinary canonical path (month branch → main qi → Ten God). G1-X01 follow compatibility. |
| Special override (PAT-R1F) | `DETECTED ≠ QUALIFIED_FOR_OVERALL_OVERRIDE`. LEVEL-1 may display; may **not** override Overall. Fully qualified follow may override where currently canonical. |
| Temperature / Điều hậu (G1-04) | Climate state + imbalance score. Điều hậu ≠ Overall. Climate candidates must not re-enter Overall competition. |
| Five Elements (G1-05) | Customer “Phân bố Ngũ hành” = structural occurrence count only. Not seasonal strength, vượng suy, or Useful God score. Keep customer explanatory note. |
| Useful God (G1-06 / UG-R2 / UG-R3F) | Current Overall architecture. Hidden Chính Quan may feed `str_003`. No Hao; no Thất Sát→Chế; no Pattern-main Overall reconciliation. |
| Dụng reasoning | STATE → NEED → PRINCIPLE → ELEMENT RELATION → STEM/TEN GOD → RESULT. No customer rule IDs. |
| Hỷ (HK-R1H) | No exact Dụng repeat; no unsupported static siblings; independent role or `Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng`. Internal `favorable_gods` unchanged. |
| Kỵ | V1.0 rule-based values. Does **not** perform full-chart reconciliation. |
| ShenSha (G1-07) | Canonical names and provenance. No alias duplication, new stars, or new formulas. |
| Luck (G1-08) | Gender required. Internal `male`/`female`. Customer Nam/Nữ. No missing-gender default as product policy. Dayun precision remains year-level. Exact giao vận datetime is V1.1. |
| Score algorithms / rule priorities / knowledge rules | Frozen as of G1-PREFINAL baseline. |

---

## Golden

| Item | Value |
|------|-------|
| 101 freeze dump | `G1_PREFINAL_101_TRUTH.json` (hash above) |
| Report CASE-0001 | `tests/golden_dataset/report_v1/CASE-0001/expected_report_input.json` |
| Interpretation expected | `tests/golden_dataset/expected/case_0001.json` |
| Control set | `G1_FINAL_CONTROL_CASES.md` generated from `G1_PREFINAL_CONTROL_CASES.json` |

---

## Control-case set

Ten G1-PREFINAL cases, locked (not recomputed in G1-FINAL):

Nguyễn Tiến Sơn · Lương Ngọc Huỳnh · Đặng Thị Dung · Đoàn Quang Hưng · Vũ Thị Thanh Tuyền · Cao Xuân Trường · Lưu Hoàng Sơn · Phạm Thị Huyền · Lương Văn Mạnh · Ngô Đắc Dũng

See `release/gate_01/G1_FINAL_CONTROL_CASES.md`.

---

## Test results (G1-FINAL re-run)

| Suite | Result | vs PREFINAL |
|-------|--------|-------------|
| Python Gate-1 (`tests` + `applications/api/tests` + `applications/tests`; 6 legacy collectors ignored) | **1806 passed**, 2 failed, 10 subtests passed | **match** |
| Portal `npm test` / `vitest run` | **254 passed / 0 failed / 0 skipped** (39 files) | **match** |
| HTML/PDF/DOCX | G1-PREFINAL smoke PASS (`G1_PREFINAL_EXPORT_SMOKE.json`); not regenerated | **match** |

---

## Known non-blocking issues (Class D)

1. `tests/knowledge/test_indexes_cli.py::test_cli_real_scaffold`
2. `tests/knowledge/test_validators.py::test_real_scaffold_foundation`  
   Cause: `knowledge/knowledge_canon/01_five_elements/knowledge_records/wood.json` broken KNO-00000x relationships. Not Gate-1 engine.

Six legacy collectors (ignored at command line):  
`tests/test_builder.py`, `test_pipeline.py`, `test_rule_loader.py`, `test_rule_matcher.py`, `test_rule_scoring.py`, `test_sentence_generator.py`  
import `interpretation_engine` instead of `engines.interpretation_engine`.

Do not repair in G1-FINAL.

---

## V1.1 backlog

Authoritative list: `release/gate_01/G1_FINAL_V1_1_BACKLOG.md`.

---

## Source-control tag

Repo convention (`.github/workflows/release.yml`): tags `v*.*.*` trigger **package + GitHub Release**.  
Existing tags: `v1.0.0`, `v1.0-backend-admin`.

G1-FINAL does **not** package production (PO §23). **Do not push a tag.**  
Do not invent `bte-v1.0-gate1-freeze`. A later packaging gate may use the next unused `vX.Y.Z` only with Product Owner authorization.

---

## Freeze declaration

See `release/gate_01/G1_FINAL_FREEZE.md`.
