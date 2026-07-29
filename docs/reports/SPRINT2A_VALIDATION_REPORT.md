# Sprint 2A Validation Report

| Item | Value |
|------|-------|
| Document | `SPRINT2A_VALIDATION_REPORT.md` |
| Project | BTE Platform V1.0 |
| Sprint | Sprint 2A — RuleContext Enrichment & API Mapping |
| Source of truth | `docs/reports/PIPELINE_DATA_TRACE_REPORT.md` |
| Validation case | Male · 21/01/1987 · 04:30 · Asia/Ho_Chi_Minh |
| Date | 2026-07-28 |

---

# Executive Summary

Sprint 2A restores **runtime view fields after Stage 4** without redesigning Stages 0–12, Pattern recognition, Knowledge/Matcher/Priority, Sentence Library, or Report Engine.

| Area | Result |
|------|--------|
| Stage 5 RuleContext summaries | **Restored** — Cách Cục + score-input summaries derived from existing sections |
| Stage 6 Score | **Receives complete Stage 5 RC**; non-zero strength/pattern/ten-god/useful-god/shensha; `wuxing_score=0` and `luck_score=0` explained (not hardcoded) |
| Stage 10 Interpretation API | **Restored** — `summary`, `matched_rule_count`, `resolved_rule_count`, `coverage`, `metadata` |
| Frontend tabs (API evidence) | Lịch Việt / Bát Tự / Cách Cục / Đánh Giá **PASS**; Luận Giải **PARTIAL** |
| Architecture | Sprint 1 pipeline order preserved; Stage 5 RC not mutated by Score |

**Overall:** Sprint 2A objectives for enrichment + API mapping are met for the critical case. Remaining gaps are **upstream producers** (luck / combination / branch geometry) and **interpretation section coverage** (wealth / dedicated ngũ hành / thập thần / đại vận), not pipeline wiring.

---

# Stage 5 Before / After

Producer: `engines/pattern_engine/rule_context_bridge.py` → `build_rule_context` + `enrich_rule_context_summaries` (orchestrator Stage 5 sole publish).

## Fields enriched

| Field | Before (trace report) | After (this case) |
|-------|----------------------|-------------------|
| `than` | empty on PatternView until late | `Kim` |
| `than_vuong_nhuoc` | weak / month-only | Stage 5: `Đắc lệnh` (from month/strength); after Score compose on PatternView: `Trung hòa` |
| `dung_than` | often empty at Stage 4 stop | `Chính Quan` |
| `hy_than` | empty at Stage 4 stop | `Mộc` |
| `ky_than` | empty at Stage 4 stop | `Thủy` |
| `dieu_hau` | weak | `Đắc lệnh` |
| `tong_cach` | empty (`follow_type` null) | `Chính Quan` (fallback to `cach_cuc`) |
| `season` | not summarized | `{name: winter, status: IN_SEASON, month_branch: Sửu, …}` |
| `temperature` | partial / humidity null | present (`slightly_cold`, cold/hot scores); humidity/climate still null upstream |
| `element_balance` | not summarized | `EXCESS` + per-element counts |
| `ten_god_summary` | not summarized | items + month commander |
| `hidden_stem_summary` | not summarized | count=11, flat list |
| `branch_relation_summary` | absent | stub with `available=false` |
| `pattern_metadata` | sparse | main_pattern / score / matched_rules / follow_type |
| `combination` | `null` | `{available: false, reason: missing_upstream_combination_producer}` |
| `luck` | empty pillars | `{available: false, reason: missing_upstream_luck_producer}` |
| `score_inputs` | absent | readiness flags for Score modules |
| `strength` | `level=unknown`, `score=0` pre-Score | still `unknown`/0 on **published** Stage 5 RC (by design); Score compose updates copy only |

## Missing fields

| Field | Status | Reason |
|-------|--------|--------|
| `luck.pillars` / luck analytics | Empty | No upstream luck producer in Stages 0–5 (out of Sprint 2A; do not invent) |
| `combination.status` | Unavailable | No upstream combination producer on PatternContext |
| `branch_relation_summary.clash_count` | null | Pattern section does not emit clash/combination geometry |
| `temperature.humidity*` / climate | null | Builder section incomplete upstream |
| `strength.level` on published Stage 5 | `unknown` | Strength score is Stage 6; published RC remains immutable (Sprint 1 N-02) |
| `follow_type` / true “tòng cách” | null | Not produced by Pattern for this chart; `tong_cach` uses `cach_cuc` fallback |

Derivation rule followed: **only** existing PatternContext / RuleContext Builder sections — no duplicate business calculators, no PatternContext mutation.

---

# Stage 6 Before / After

Score Engine still receives Stage 5 `published_rule_context` only (no rebuild). Orchestrator composes a **copy** via `append_score_to_rule_context` for Interpretation.

## Scores calculated (critical case)

| Score | Before (trace) | After |
|-------|----------------|-------|
| `total_score` / overall | 55.25 | **55.25** |
| `strength_score` | 45.0 | **45.0** |
| `pattern_score` | 100.0 | **100.0** |
| `ten_god_score` | 100.0 | **100.0** |
| `useful_god_score` | present | **20.0** (now always on portal wire) |
| `shensha_score` | present | **100.0** (now always on portal wire) |
| `grade` | D+ | **D+** |
| `confidence` | medium | **medium** |
| `wuxing_score` | 0 | **0.0** (still) |
| `luck_score` | 0 | **0.0** (still; key now always emitted) |

API `data.score` now includes zero-valued `luck_score` / `useful_god_score` / `shensha_score` so Đánh Giá does not drop keys.

## Scores still zero

| Score | Reason |
|-------|--------|
| `wuxing_score = 0` | Upstream `element_balance.status = EXCESS` with high counts; Wuxing module runs and net contribution clamps to **0** — **not** missing Stage 5 fields; **not** hardcoded |
| `luck_score = 0` | `luck.available = false` / `missing_upstream_luck_producer` — Score correctly matches **0** luck rules; fix requires upstream luck data (Sprint 2B+ / Runtime), not Score hardcoding |

No fake scores were introduced.

---

# Stage 10 Before / After

## API fields restored

| Field | Before (portal) | After |
|-------|-----------------|-------|
| `summary` | null / stripped | Restored (fallback from `sections[id=summary]` when raw summary scrubbed) — preview present |
| `matched_rule_count` | null / omitted | **84** |
| `resolved_rule_count` | null / omitted | **35** |
| `coverage` | null / omitted | **≈0.0707** |
| `confidence` | present | **1.0** |
| `metadata` | often omitted | Present when engine provides |
| `section_count` / `sentence_count` | 11 / 25 | Unchanged commercial sanitize size |

## Interpretation restored

Engine still receives composed RuleContext (with Score) → Knowledge → Matching → Priority → `build_from_resolved`. Interpretation logic was **not** rewritten.

Commercial sections returned for this case:

`summary`, `personality`, `career`, `relationship`, `health`, `useful_god`, `pattern`, `conclusion`, `warning`, `strength`, `weakness`

## Remaining null / empty values

| Item | Notes |
|------|-------|
| Dedicated `wealth` section | Not in portal sections for this case (engine/sanitize coverage) |
| Dedicated `luck` / Đại vận section | Filtered or empty after sanitize; aligns with empty luck upstream |
| Dedicated Ngũ hành / Thập thần narrative sections | Not separate section IDs in current commercial map (charts live under Score) |
| Portal `rule_context` body | Still metadata-only `{published, sections[]}` — intentional; Cách Cục uses `data.pattern` |

---

# Frontend Verification

Evidence: live `OrchestratorService.analyze(...)` JSON for the critical case (no UI screenshots captured in this environment). Presenters: `pattern.js`, `score.js`, `interpretation.js`.

| Tab | Status | Evidence |
|-----|--------|----------|
| **Lịch Việt** | **PASS** | `calendar` payload present |
| **Bát Tự** | **PASS** | `bazi` pillars / day master present |
| **Cách Cục** | **PASS** | `than`, `than_vuong_nhuoc`, `dung_than`, `hy_than`, `ky_than`, `dieu_hau`, `tong_cach` all non-empty on `data.pattern` |
| **Đánh Giá** | **PASS** | `total_score`, `strength_score`, `pattern_score`, `wuxing_score`, `ten_god_score`, strength series, `confidence` present; zeros explicit for luck/wuxing |
| **Luận Giải** | **PARTIAL** | Tổng quan / Cách cục / Dụng thần / Sự nghiệp / Quan hệ→Hôn nhân / Sức khỏe present; **missing** dedicated Tài vận, Ngũ hành, Thập thần narrative blocks, Đại vận |

### Cách Cục checklist

- Thân — PASS (`Kim`)
- Thân vượng / nhược — PASS (`Trung hòa` on final PatternView after Score compose)
- Dụng thần — PASS
- Hỷ thần — PASS
- Kỵ thần — PASS
- Điều hậu — PASS
- Tổng cách — PASS

### Đánh Giá checklist

- Điểm tổng — PASS (`55.25`)
- Điểm thân — PASS (`45`)
- Điểm cách cục — PASS (`100`)
- Điểm ngũ hành — PASS key (`0` legitimate)
- Điểm thập thần — PASS (`100`)
- Cường độ — PASS (strength score + series)
- Confidence — PASS (`medium`)

### Luận Giải checklist

- Tổng quan — PASS
- Cách cục — PASS (section)
- Dụng thần — PASS
- Ngũ hành — FAIL (no dedicated interpretation section)
- Thập thần — FAIL (no dedicated interpretation section)
- Sự nghiệp — PASS
- Tài vận — FAIL (no wealth section this case)
- Hôn nhân — PASS via `relationship` alias
- Sức khỏe — PASS
- Đại vận — FAIL (not in portal sections; luck upstream empty)

---

# Remaining Work

## Critical

- None blocking Sprint 2A tab restore for Cách Cục / Đánh Giá.

## High

- **Upstream luck producer** so `luck.available=true` and `luck_score` can be non-zero when rules match.
- **Upstream combination / branch-relation producer** so `combination` and `branch_relation_summary` are real signals.
- **Align API tests** still expecting Sprint-0 contracts (Pattern-owned RC, in-place Score mutation, hide `matched_rule_count`) — 16 failures; tests not modified per workspace rules.

## Medium

- Interpretation commercial coverage: wealth / luck sections empty or sanitized out.
- Temperature humidity / climate fields still null upstream.
- Published Stage 5 `strength.level=unknown` until Score compose (by design); document for consumers.

## Low

- `wuxing_score=0` under EXCESS may need product/UX explanation (not a missing field).
- Portal still omits full RuleContext body (metadata only) — acceptable if Pattern/Score/Interpretation views stay complete.

---

# Final Recommendation

## Is the project ready for Sprint 2B?

**YES**

### Justification

1. Stage 5 now publishes the summary fields required by Cách Cục and Score readiness (`score_inputs`) from existing contexts only.
2. Score Engine receives that RuleContext; zero scores are traced to upstream emptiness or calculator netting — not missing mapping or hardcoded fills.
3. Interpretation portal contract restores the metrics lost in the data-trace report.
4. Architecture from Sprint 1 (Stages 0–12, immutable published RC, Pattern ≠ RuleContext owner) is preserved.
5. Remaining work (luck/combination producers, narrative section coverage, test-contract updates) belongs to **Sprint 2B+ / Runtime**, not another 2A enrichment pass.

---

# Implementation Notes

## Files changed

| File | Change |
|------|--------|
| `engines/pattern_engine/rule_context_bridge.py` | `enrich_rule_context_summaries` + Cách Cục / summary fields |
| `applications/api/services/orchestrator.py` | Re-enrich PatternView from Score-composed copy (no Stage 5 mutation) |
| `engines/interpretation_engine/portal_view.py` | Restore summary/metrics; summary fallback from section body |
| `applications/api/models/analysis_result.py` | InterpretationView + Pattern/Score portal zero-key emission |
| `applications/api/services/interpretation_truth.py` | Map restored Interpretation fields |
| `engines/score_engine/result.py` | Always emit luck/useful_god/shensha scores on portal dict |

## Tests executed

```text
pytest applications/api/tests tests/score tests/pattern -q
→ 16 failed, 87 passed
```

Failing tests (unchanged policy — source preferred; tests not edited):

- `test_integration_api` (3)
- `test_phase3_unified_pattern` (2) — still expect Pattern-owned RuleContext
- `test_phase4_unified_score` (4) — mutation / payload expectations
- `test_phase5_unified_interpretation` (4)
- `test_phase6_unified_report` (2)
- `test_production_readiness::test_analyze_hides_internal_metadata_and_debug_fields` — asserts `matched_rule_count` **absent**; Sprint 2A intentionally restores it

## Application start

- `create_app()` succeeds (`BTE Applications API`).
- Critical-case `analyze` completes Stages 0–12 without runtime errors; result page presenters receive non-empty Pattern/Score/Interpretation payloads as above.

## Remaining failures

Same 16 API/contract tests as Sprint 1 drift + production-readiness assertion conflict with restored interpretation metrics. No Golden Dataset / snapshot edits.

---

END
