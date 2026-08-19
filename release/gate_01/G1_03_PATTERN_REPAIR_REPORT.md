# G1-03 — Pattern Repair Report

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-03 Phase 2 |
| **Date** | 2026-08-19 |
| **Canonical production** | `engines/pattern_engine` |
| **V1.0 freeze** | Primary pattern identification only |
| **Status** | FINAL FREEZE READY |

No Pattern selection formula change. No priority CSV value change. No Strength / Temperature / Ten Gods / Useful God calculation change. No Deep Pattern Interpretation (thành/phá/cứu ứng/thanh thuần/hỗn tạp/cường nhược của cách).

Main-pattern V1.0 lock:

```text
Nguyệt lệnh / nguyệt chi → khí chính → Thập thần với Nhật chủ → primary main-pattern candidate
```

Thấu can is evidence / qualification status only. It does not rename the primary pattern in V1.0.

---

## 1. Why tests/golden used to emit Chính Quan

Production Orchestrator already called `build_pattern_context`. CASE-0001 live winner was always:

| Item | Value |
|------|-------|
| Month branch | Sửu |
| Hidden stems | Kỷ, Quý, Tân |
| Main qi | Kỷ |
| Day Master | Canh |
| Ten God | Chính Ấn (`ten_god_name(Canh, Kỷ)`) |
| Rule | `pat_ca_01` |
| Primary | **Chính Ấn** |

Several test / golden / validation helpers built a bare `PatternContext` with pillars and `bazi` (sometimes without `bazi`) but **without** `month_branch_ten_god`.

`pat_ca_01` condition is `month_branch_ten_god == "Chính Ấn"`. Empty field → main rule does not match.

`pat_fallback` has empty conditions, `pattern=chinh_quan`, priority 1. It always matches. When no substantive rule validates, fallback wins → **Chính Quan**.

That is not a CASE-0001 chart disagreement. It is an incomplete-context path that looked canonical.

Golden Report V1 `expected_report_input.json` already stored `primary_pattern: "Chính Ấn"` (production adapter). The Pattern Engine snapshot and API phase helpers were the paths that still showed Chính Quan.

---

## 2. Canonical context repair

Reuse production builder. Do not duplicate mapping in tests.

| Mechanism | Role |
|-----------|------|
| `build_pattern_context` | Canonical Lệnh Tháng mapping (Orchestrator Stage 4) |
| `ensure_canonical_pattern_context` | If `bazi` is present and lệnh-tháng is missing, rebuild via `build_pattern_context` and keep Strength / Temperature overlays |
| `applications/api/tests/unified_stack.py` | Phase 3–6 helpers now use the same Pattern → Strength → Temperature overlay as Orchestrator |

Supported production paths (unchanged owner):

```text
CalendarEngine → BaziEngine → build_pattern_context
    → Strength / Temperature overlay
    → PatternEngine.calculate
```

Test / golden / validation paths repaired to call `build_pattern_context` (or `ensure` when `bazi` is attached):

- `applications/api/tests/test_phase3_unified_pattern.py`
- `applications/api/tests/unified_stack.py` (phase 4–6)
- `tests/golden_dataset/wp45_coverage_runner.py`
- `validation/live_e2e_trace.py`
- `validation/rc1_audit_runner.py`

Complete BaZi on `PatternContext` can no longer silent-fallback only because the caller skipped the builder.

---

## 3. Fallback behavior

`pat_fallback` is **kept**. Production still needs it when Lệnh Tháng cannot be determined.

| Situation | Behavior |
|-----------|----------|
| Empty `PatternContext()` (no BaZi, no `month_branch_ten_god`) | Fallback allowed → `chinh_quan` / `fallback_used=True`. Log: `pattern.fallback_incomplete_context` |
| Complete BaZi present, builder missing | `ensure_canonical_pattern_context` rebuilds; CASE-0001 → `pat_ca_01`, **not** fallback |
| Substantive rule matches | Fallback rejected (`fallback_superseded`) |
| Fallback still wins despite BaZi / lệnh-tháng signals | Warning: `pattern.fallback_with_canonical_signals` |

Fallback must not silently mint a canonical-looking result for a valid complete chart just because an adapter skipped context.

Priority values were **not** changed. `pat_fallback` remains priority 1.

---

## 4. CASE-0001 full trace

Chart: Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần. Nhật chủ **Canh**.

```text
Month Branch = Sửu
    → hidden stems: Kỷ, Quý, Tân
    → main qi: Kỷ
    → Day Master: Canh
    → Ten God: Chính Ấn
    → rule: pat_ca_01
    → primary pattern: Chính Ấn
```

Not hard-coded. Same path as any other chart: `_BRANCH_MAIN_STEM["Sửu"] = "Kỷ"` then `ten_god_name`.

Candidates on this chart:

| Rule | Pattern | Status |
|------|---------|--------|
| `pat_ca_01` | `chinh_an` | **winner** (priority 72) |
| `pat_fallback` | `chinh_quan` | rejected `fallback_superseded` |
| `fol_tsat_01` | follow | rejected `follow_not_detected` |
| `com_san_01` | `sat_an` | **does not match** (visible `ten_gods_list` does not contain both Thất Sát and Chính Ấn) |

---

## 5. Penetration evidence

Qualification evidence only. Does not rename primary pattern.

| Check | CASE-0001 |
|-------|-----------|
| Exact stem 透 | **Kỷ không thấu** on thiên can |
| Same-element related stem | **Mậu** thấu trụ Giờ, Thổ, Ten God **Thiên Ấn** |
| `Mậu == Kỷ` because both Thổ? | **No.** Exact stem ≠ related stem |

Compact evidence (identification, no thành/phá wording):

```text
Nguyệt lệnh Sửu · khí chính Kỷ · Kỷ đối với Canh là Chính Ấn · Kỷ không thấu trực tiếp · Mậu Thiên Ấn thấu tại trụ Giờ · rule pat_ca_01
```

Published on `PatternResult` / `PatternView` (additive): `winning_rule_id`, `evidence_compact`, `month_branch`, `month_hidden_stems`, `month_main_qi`, `month_main_qi_ten_god`, `day_master`, `penetration_exact`, `penetration_related`, `candidate_patterns`, `fallback_used`, plus existing `priority`.

`to_portal_dict()` still omits `matched_rules`.

---

## 6. Priority verification

CSV priority values unchanged.

| Fixture | Main | Combination | Winner |
|---------|------|-------------|--------|
| CASE-0001 | Chính Ấn (`pat_ca_01`, 72) | `com_san_01` does not match | Chính Ấn |
| Regression (synthetic) | `month_branch_ten_god=Chính Ấn` + `ten_gods_list=["Thất Sát","Chính Ấn"]` | `com_san_01` / `sat_an` priority **85** | **Sát Ấn** because `85 > 72` |

Deterministic winner: Priority Engine `max_rules_per_section=1`, sort `(priority, score, rule_id)`.

---

## 7. Cross-surface result

No renderer computes Pattern. All read `data.pattern.cach_cuc` / Report V1 `pattern.primary_pattern`.

| Surface | CASE-0001 primary |
|---------|-------------------|
| PatternEngine | Chính Ấn / `pat_ca_01` |
| Orchestrator | Chính Ấn |
| API `/api/v1/analyze` | Chính Ấn |
| Canonical Desktop S01 | Cách cục / Căn cứ from PatternView |
| Portal Technical Info | `pattern` + `pattern_evidence` → **Căn cứ** |
| Full Report HTML | Cách cục + Căn cứ |
| Report V1 / PDF source | `primary_pattern = Chính Ấn` |
| DOCX | Chính Ấn in body |
| Golden Report V1 | `primary_pattern: "Chính Ấn"` |
| Pattern snapshot | `primary: "chinh_an"` |

Presentation (no tốt/xấu, no thành/phá):

**Cách cục** `Chính Ấn`

**Căn cứ** `Nguyệt lệnh Sửu · khí chính Kỷ · Kỷ đối với Canh là Chính Ấn` plus compact `Kỷ không thấu trực tiếp · Mậu Thiên Ấn thấu tại trụ Giờ`.

---

## 8. Files changed

Engine (context + evidence only; match conditions / priority CSV unchanged):

- `engines/pattern_engine/utils/context_builder.py` — `month_main_qi`, `ensure_canonical_pattern_context`
- `engines/pattern_engine/context.py` — `month_main_qi`
- `engines/pattern_engine/calculator.py` — ensure + fallback diagnostic
- `engines/pattern_engine/engine.py` — evidence fields on `PatternResult`
- `engines/pattern_engine/evidence.py` — **new** identification / penetration evidence

API / tests:

- `applications/api/models/analysis_result.py` — additive PatternView fields
- `applications/api/services/pattern_truth.py`
- `applications/api/tests/unified_stack.py`
- `applications/api/tests/test_phase3_unified_pattern.py`
- `applications/api/tests/test_phase4_unified_score.py`
- `applications/api/tests/test_phase5_unified_interpretation.py`
- `applications/api/tests/test_phase6_unified_report.py`

Portal (bind only):

- `applications/customer_portal/src/adapters/canonicalPattern.ts` — **new**
- `applications/customer_portal/src/adapters/canonicalDesktopAdapter.ts`
- `applications/customer_portal/src/report/fullReportViewModel.ts`
- `applications/customer_portal/src/features/portal/liveAnalysisResultAdapter.ts`
- `applications/customer_portal/src/features/result_v2/components/TechnicalInfo/index.tsx`

Golden / validation / tests:

- `tests/golden_dataset/snapshots/pattern_engine/case_0001.json` — CASE-0001 identity → Chính Ấn
- `tests/golden_dataset/wp45_coverage_runner.py`
- `validation/live_e2e_trace.py`
- `validation/rc1_audit_runner.py`
- `tests/pattern/test_g1_03_pattern_binding.py` — **new**
- `tests/report_engine/test_g1_03_pattern_binding.py` — **new**
- `applications/customer_portal/tests/js/g1_03_pattern_binding.test.ts` — **new**

Not changed: Strength Engine, Temperature Engine, Ten Gods Engine, Useful God Engine, Pattern CSV priority values, Report V1 `expected_report_input.json`.

---

## 9. Tests

| Suite | Result |
|-------|--------|
| `pytest tests/pattern -q` | **14 passed** |
| `pytest applications/api/tests/test_phase3_unified_pattern.py` … `test_phase6_unified_report.py` + G1-03 pattern/report + pattern_engine/calculator | **35 passed** |
| Portal vitest `g1_03` + `g1_02` + desktop + full_report | **22 passed** |

Task 9 coverage:

1. CASE-0001 canonical context — PASS  
2. Main qi = Kỷ — PASS  
3. Canh × Kỷ = Chính Ấn — PASS  
4. Winning rule `pat_ca_01` — PASS  
5. Final primary Chính Ấn — PASS  
6. No accidental `pat_fallback` on complete BaZi — PASS  
7. Direct penetration Kỷ = false — PASS  
8. Visible Mậu distinguished from Kỷ — PASS  
9. Combination non-match CASE-0001 — PASS  
10. Combination priority fixture `85 > 72` — PASS  
11. Production / test / golden same primary — PASS  
12. Portal / Report same primary — PASS  

Phase 4–6 helpers no longer rebuild incomplete Pattern context. Score / Interpretation engines were not rewritten. Helpers consume Orchestrator-aligned RuleContext (including Luck for interpretation parity). Report view section count for CASE-0001 follows production Chính Ấn narrative (the old hardcoded `7` was a Chính Quan fallback artifact).

---

## 10. Remaining issues / V1.1 backlog

Frozen out of G1-03 (do not treat as V1.0 identification failures):

- Deep qualification: thành cách, phá cách, cứu ứng, thanh thuần, hỗn tạp, cường nhược của cách.
- Do not read `khí chính = pattern` as “đã hoàn toàn thành cách”.
- `database/14_pattern/05_priority_rules.csv` remains metadata-only (executable priority is the `priority` column on 01–04).
- `tests/golden_dataset/snapshots/interpretation_engine/case_0001.json` still contains legacy wording “Chính Quan thành cách”. That is Interpretation narrative, not Pattern identification. G1-03 does not rewrite Interpretation.
- On-disk `tests/golden_dataset/reports/wp45_coverage_report.json` is a historical dump from the old incomplete-context runner. The runner now uses `build_pattern_context`; the report file was not regenerated (not CASE-0001 production golden).

G1-03 STATUS: FINAL FREEZE READY

Do not start G1-04 from this gate.
