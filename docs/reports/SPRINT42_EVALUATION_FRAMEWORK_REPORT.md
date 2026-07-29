# Sprint 4.2 Evaluation Framework Report

| Item | Value |
|------|-------|
| Document | `SPRINT42_EVALUATION_FRAMEWORK_REPORT.md` |
| Project | BTE Platform V1.0 |
| Sprint | Sprint 4.2 — Luck Evaluation Framework |
| Prerequisites | `SPRINT4_FOUNDATION_REPORT.md`, `SPRINT41_PROVIDER_REPORT.md` |
| Knowledge (draft) | `knowledge/luck_engine/README.md`, `ARCHITECTURE.md` |
| Case | Male · 21/01/1987 · 04:30 · Asia/Ho_Chi_Minh |
| Date | 2026-07-28 |
| Scope | Evaluation **framework** only — UNKNOWN / NULL until business rules exist |

---

# Architecture compliance

| Rule | Status |
|------|--------|
| Architecture frozen (pipeline order unchanged) | **PASS** |
| Luck Providers unchanged (still produce pillars) | **PASS** |
| No mutation of RuleContext / Calendar / BaZi / Pattern / Score / Knowledge / Interpretation | **PASS** — only `engines/luck_engine/**` touched |
| No school-specific BaZi evaluation invented | **PASS** — Null evaluators only |
| No fabricated favorable / unfavorable conclusions | **PASS** |
| Knowledge specs remain authoritative for future refinements | **PASS** — referenced as pending |
| Immutable runtime (providers + evaluation results) | **PASS** |
| Dependency injection for all evaluators | **PASS** |

### Evaluation flow

```text
Luck Providers
    ↓
SupportEvaluator
    ↓
AttackEvaluator
    ↓
LuckStrengthEvaluator
    ↓
LuckStageEvaluator
    ↓
LuckSummaryBuilder
    ↓
LuckContext
```

Legacy `LuckEvaluator` remains injectable for backward compatibility; it is **not** part of the default pipeline.

---

# Implemented evaluators

## Protocols (`engines/luck_engine/interfaces.py`)

| Protocol | Responsibility | Return type |
|----------|----------------|-------------|
| `SupportEvaluator` | Hành / thần hỗ trợ level | `SupportEvaluation` |
| `AttackEvaluator` | Khắc / xung / hại / hình / phá level | `AttackEvaluation` |
| `LuckStrengthEvaluator` | Numeric luck strength | `StrengthEvaluation` |
| `LuckStageEvaluator` | Luck stage label | `StageEvaluation` |
| `LuckSummaryBuilder` | Structured summary (not narrative) | `SummaryEvaluation` |

## Immutable result models (`evaluation_models.py`)

| Model | Default when no rule |
|-------|----------------------|
| `SupportEvaluation` | `elements=[]`, `level=UNKNOWN` |
| `AttackEvaluation` | `elements=[]`, `level=UNKNOWN` |
| `StrengthEvaluation` | `value=NULL` |
| `StageEvaluation` | `stage=UNKNOWN` |
| `SummaryEvaluation` | `summary=NULL` |

Constants: `UNKNOWN`, `NO_BUSINESS_RULE`.

## Default implementations (`evaluators/null.py`)

| Class | Behaviour |
|-------|-----------|
| `NullSupportEvaluator` | UNKNOWN / empty elements |
| `NullAttackEvaluator` | UNKNOWN / empty elements |
| `NullLuckStrengthEvaluator` | strength NULL |
| `NullLuckStageEvaluator` | stage UNKNOWN |
| `NullLuckSummaryBuilder` | summary NULL (no invented text) |

`LuckEngine(use_default_evaluators=True)` installs these by default.

---

# Modified / new files

| File | Change |
|------|--------|
| `engines/luck_engine/evaluation_models.py` | **NEW** — immutable evaluation results |
| `engines/luck_engine/evaluators/__init__.py` | **NEW** |
| `engines/luck_engine/evaluators/null.py` | **NEW** — Null* defaults |
| `engines/luck_engine/interfaces.py` | Added Strength / Stage / Summary protocols; Support/Attack return evaluation objects |
| `engines/luck_engine/engine.py` | Evaluation pipeline + DI for all evaluators |
| `engines/luck_engine/__init__.py` | Public exports |

**Not modified:** Calendar, BaZi, Pattern, RuleContext, Score, Knowledge, Interpretation, Report, providers, frontend, tests, Golden Dataset.

---

# Pipeline validation

Case: Male · 21/01/1987 · 04:30 · Asia/Ho_Chi_Minh

| Check | Result |
|-------|--------|
| Pipeline unchanged | **PASS** — score → luck → knowledge → … |
| Score unchanged | **PASS** — `total_score=55.25` |
| Providers unchanged | **PASS** — Dayun Ất Tỵ, Liunian Bính Ngọ present |
| Evaluation framework executes | **PASS** — `metadata.evaluation.status=framework_executed` |
| Pipeline order recorded | **PASS** — `[support, attack, strength, stage, summary]` |
| LuckContext valid | **PASS** — `available=true` |

---

# Runtime validation

| Field | Value | Notes |
|-------|-------|-------|
| `support_level` | `UNKNOWN` | No business rule |
| `support_elements` | `[]` | Not fabricated |
| `attack_level` | `UNKNOWN` | No business rule |
| `attack_elements` | `[]` | Not fabricated |
| `luck_stage` | `UNKNOWN` | No business rule |
| `luck_strength` | `null` | No scale defined |
| `luck_summary` | `null` | No narrative invented |
| `confidence` | `null` | Unchanged |
| Provider pillars | Present | Unaffected by evaluators |

### Tests executed

| Suite | Result |
|-------|--------|
| `pytest tests/score -q` | **38 passed** |

---

# Outstanding business rules (awaiting knowledge specs)

Knowledge docs are **Draft**; `DAYUN_SPEC.md` not yet present. The following require authoritative specifications before non-Null evaluators:

| Area | Needed from knowledge |
|------|------------------------|
| Support rules | Which elements / ten-gods count as trợ vs Nhật Chủ / Dụng thần / Cách cục |
| Attack rules | Mapping for khắc / xung / hại / hình / phá against luck pillars |
| Strength scale | Numeric definition of `luck_strength` (range, inputs, clamps) |
| Stage taxonomy | Allowed `luck_stage` values and transition rules |
| Summary contract | Structured summary fields (still **not** Interpretation narrative) |
| Dayun / Liunian / Liuyue / Liuri / Liushi layer evaluators | Spec’d in ARCHITECTURE draft (§24) but not Sprint 4.2 scope |
| Trend / Risk evaluators | Spec’d in draft; deferred |
| Score `luck_score` integration | Requires matched luck rules + strength — later sprint |
| Interpretation / Report luck sections | Downstream of real evaluation results |

Until those specs land, Null evaluators remain the correct commercial default: **honest UNKNOWN / NULL**, no invented school logic.

---

# Sprint readiness

| Next | Ready? |
|------|--------|
| Bind real Support/Attack rules from knowledge | **YES** — swap Null* via DI |
| Layer-specific Dayun/Liunian evaluators | After DAYUN_SPEC / related specs |
| Interpretation consumption of luck evaluation | After non-UNKNOWN results exist |

---

END
