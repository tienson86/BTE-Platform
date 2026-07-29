# Sprint 4 Foundation Report

| Item | Value |
|------|-------|
| Document | `SPRINT4_FOUNDATION_REPORT.md` |
| Project | BTE Platform V1.0 |
| Sprint | Sprint 4 — Luck Engine Foundation |
| Sources | `PIPELINE_DATA_TRACE_REPORT.md`, `SPRINT3_BUSINESS_COMPLETION_REPORT.md`, `SPRINT35_PRODUCER_COMPLETION_REPORT.md` |
| Case | Male · 21/01/1987 · 04:30 · Asia/Ho_Chi_Minh |
| Date | 2026-07-28 |
| Scope | Foundation only — **no** DaYun / Lưu niên / luck scoring algorithms |

---

# Architecture

Luck Engine is a **standalone** runtime engine.

```text
Calendar → BaZi → Feng Shui → Pattern → RuleContext → Score
    → Luck → Knowledge → Matching → Priority → Interpretation → Report → Delivery
```

| Rule | Enforcement |
|------|-------------|
| Does not calculate BaZi / Pattern / Useful God / Strength / Temperature / Combination | `LuckEngine.build` only consumes upstream objects |
| RuleContext immutable | Published Stage 5 RC unchanged; LuckContext is separate |
| One producer for LuckContext | `engines.luck_engine.engine.LuckEngine` |
| Luck optional for Interpretation | `build_from_resolved(..., luck_context=None)` |

---

# LuckContext model

Immutable (`@dataclass(frozen=True, slots=True)`):

| Field | Foundation value (case) |
|-------|-------------------------|
| `current_dayun` | `null` |
| `current_liunian` | `null` |
| `current_liuyue` | `null` |
| `current_liuri` | `null` |
| `current_liushi` | `null` |
| `support_elements` | `[]` |
| `attack_elements` | `[]` |
| `support_level` | `null` |
| `attack_level` | `null` |
| `luck_stage` | `null` |
| `luck_strength` | `null` |
| `luck_summary` | `null` |
| `confidence` | `null` |
| `metadata` | engine/sprint/provider flags + upstream presence |
| `available` | `false` |
| `reason` | `luck_engine_foundation_no_calculation` |

File: `engines/luck_engine/context.py`

---

# Pipeline integration

| Change | Detail |
|--------|--------|
| `PIPELINE_ORDER` | Inserts `"luck"` immediately after `"score"` |
| Stage Literal | Adds `"luck"` |
| Orchestrator | `self.luck_engine = LuckEngine()`; Stage builds LuckContext; `payload["luck"] = luck_context.to_dict()` |
| Interpretation | Receives `luck_context` kwarg; attaches to `InterpretationResult.luck_context` without changing portal narrative |

Stage indices after insert:

| Stage | Name |
|------:|------|
| 6 | score |
| 7 | **luck** |
| 8 | knowledge |
| 9 | matching |
| 10 | priority |
| 11 | interpretation |
| 12 | report |
| 13 | delivery |

---

# New interfaces

File: `engines/luck_engine/interfaces.py`

| Protocol | Role |
|----------|------|
| `DayunProvider` | Đại vận pillars |
| `LiunianProvider` | Lưu niên |
| `LiuyueProvider` | Lưu nguyệt |
| `LiuriProvider` | Lưu nhật |
| `LiushiProvider` | Lưu thì |
| `SupportEvaluator` | support elements/level |
| `AttackEvaluator` | attack elements/level |
| `LuckEvaluator` | stage / strength / summary / confidence |

No implementations in Sprint 4 — injectable via `LuckEngine(...)` for Sprint 4.1+.

---

# Modified / new files

| File | Role |
|------|------|
| `engines/luck_engine/__init__.py` | Public API |
| `engines/luck_engine/context.py` | LuckContext |
| `engines/luck_engine/engine.py` | LuckEngine |
| `engines/luck_engine/interfaces.py` | Provider protocols |
| `engines/luck_engine/exceptions.py` | LuckEngineError |
| `applications/api/services/orchestrator.py` | Pipeline + stage wiring |
| `engines/interpretation_engine/engine.py` | Optional `luck_context` on `build_from_resolved` |
| `engines/interpretation_engine/legacy_builder.py` | `InterpretationResult.luck_context` field |
| `engines/bazi_engine/luck/interface.py` | Points to `engines.luck_engine` (compat) |
| `engines/bazi_engine/luck/__init__.py` | Compat exports |

**Not modified:** Score Engine, Pattern Engine, Knowledge, Matcher, Priority, frontend, Rule Database.

---

# Validation

Case: Male · 21/01/1987 · 04:30 · Asia/Ho_Chi_Minh

| Check | Result |
|-------|--------|
| Pipeline completes | **PASS** — includes `luck` |
| Score unchanged | **PASS** — `total_score=55.25` |
| Interpretation unchanged | **PASS** — section_count=11, sentence_count=25 |
| LuckContext exists | **PASS** — `payload.luck` present |
| Fields may be NULL | **PASS** — available=false, pillars null |
| RuleContext not mutated by Luck | **PASS** — Stage 5 publish remains metadata snapshot |
| `tests/score` + `tests/pattern` | **45 passed** |
| FE score binding verifier | **10 PASS** |

Pipeline list:

```text
input → calendar → bazi → feng_shui → pattern → rule_context → score
→ luck → knowledge → matching → priority → interpretation → report → delivery
```

---

# Readiness for Sprint 4.1

**YES**

Sprint 4.1 can implement concrete `DayunProvider` / `LiunianProvider` / evaluators and inject them into `LuckEngine` without changing pipeline order, RuleContext ownership, or Score algorithms.

---

END
