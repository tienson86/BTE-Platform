# Sprint 4.3 Dayun Rule Implementation Report

| Item | Value |
|------|-------|
| Document | `SPRINT43_DAYUN_RULE_IMPLEMENTATION_REPORT.md` |
| Project | BTE Platform V1.0 |
| Sprint | Sprint 4.3 — Dayun Rule-Based Evaluation |
| Spec | `knowledge/luck_engine/01_dayun/DAYUN_SPEC.md` v1.0 (Draft) |
| Prerequisites | Sprint 4 / 4.1 / 4.2 reports |
| Case | Male · 21/01/1987 · 04:30 · Asia/Ho_Chi_Minh |
| Date | 2026-07-28 |

---

# 1. Files modified

| File | Change |
|------|--------|
| `engines/luck_engine/dayun_validation.py` | **NEW** — DAYUN_SPEC §§13–14 validation |
| `engines/luck_engine/evaluators/dayun.py` | **NEW** — Dayun* evaluators / summary builder |
| `engines/luck_engine/evaluators/__init__.py` | Export Dayun evaluators |
| `engines/luck_engine/evaluation_models.py` | Add `reasons` on Support/Attack evaluations |
| `engines/luck_engine/engine.py` | Default to Dayun evaluators; set `confidence`; sprint `4.3` |
| `engines/luck_engine/__init__.py` | Public exports |

**Not modified:** Calendar, BaZi, Pattern, RuleContext, Score, Knowledge, Interpretation, providers, LuckContext schema, evaluation pipeline order, frontend, tests, Golden Dataset.

---

# 2. Implemented business rules

Source: **DAYUN_SPEC.md only** (no invented cát hung algorithms).

| Spec section | Implementation |
|--------------|----------------|
| §2 Out of scope (scoring / luận giải / Liunian…) | `luck_strength=NULL`; no narrative |
| §4 “Module không đánh giá cát hung” | Support/Attack → `UNKNOWN`, empty elements |
| §§6–7 Output / DayunRuntime attributes | `DayunLuckSummaryBuilder` JSON snapshot |
| §8 / §14 Ten-year continuous cycles | Validation checks age/year span + sequence continuity |
| §13 Validation Rules | `validate_dayun_runtime` (stem/branch/fields/windows/sequence) |
| §14 Business Rules | Single stem+branch; metadata presence; immutable inputs |
| §7 Confidence (runtime metadata) | `confidence` = validation pass-rate (not a luck score) |

### Evaluator behaviour

| Evaluator | Result |
|-----------|--------|
| `DayunSupportEvaluator` | `support_level=UNKNOWN`, `support_elements=[]`, `support_reasons` cite §2/§4 |
| `DayunAttackEvaluator` | `attack_level=UNKNOWN`, `attack_elements=[]`, `attack_reasons` cite §2/§4 |
| `DayunLuckStrengthEvaluator` | `luck_strength=NULL`, `confidence` from validation |
| `DayunLuckStageEvaluator` | `luck_stage=UNKNOWN` (no taxonomy in SPEC) |
| `DayunLuckSummaryBuilder` | Machine-readable JSON string (no NL interpretation) |

Pipeline unchanged:

```text
Providers → Support → Attack → Strength → Stage → Summary → LuckContext
```

---

# 3. Remaining UNKNOWN / NULL fields

| Field | Value | Why |
|-------|-------|-----|
| `support_level` | `UNKNOWN` | SPEC forbids cát hung evaluation |
| `support_elements` | `[]` | No support-element rule in SPEC |
| `attack_level` | `UNKNOWN` | Same |
| `attack_elements` | `[]` | Same |
| `luck_strength` | `null` | Scoring out of scope (§2) |
| `luck_stage` | `UNKNOWN` | No stage taxonomy in DAYUN_SPEC |
| Liunian/Liuyue/Liuri/Liushi evaluation | Not applied | Out of DAYUN_SPEC scope (§2) |

`confidence` is populated (validation pass-rate) — runtime quality, not favorable/unfavorable strength.

---

# 4. Validation result

Case: Male · 21/01/1987 · 04:30 · Asia/Ho_Chi_Minh

| Check | Result |
|-------|--------|
| Pipeline unchanged | **PASS** |
| Score unchanged | **PASS** — `total_score=55.25` |
| RuleContext unchanged | **PASS** — read-only; Luck does not mutate |
| Providers unchanged | **PASS** — Dayun Ất Tỵ present |
| Evaluation executes under DAYUN_SPEC | **PASS** — `status=dayun_spec_evaluation_executed` |
| Dayun validation | **PASS** — `ok=true`, `confidence=1.0` |
| No fabricated cát hung | **PASS** — Support/Attack UNKNOWN |

### Tests

| Suite | Result |
|-------|--------|
| `pytest tests/score -q` | **38 passed** |
| `pytest tests/luck -q` | **N/A** — `tests/luck` not present |

---

# 5. Runtime example

```text
available=true
current_dayun=Ất Tỵ (index=3, ages 35–44, years 2022–2031)
support_level=UNKNOWN  support_elements=[]
attack_level=UNKNOWN   attack_elements=[]
luck_strength=null
confidence=1.0
luck_stage=UNKNOWN
luck_summary=<JSON dayun_runtime_summary>
```

Structured summary (abbreviated):

```json
{
  "kind": "dayun_runtime_summary",
  "spec": "DAYUN_SPEC.md",
  "spec_version": "1.0",
  "current_dayun": {
    "identity": {"index": 3},
    "time": {"start_age": 35, "end_age": 44, "start_year": 2022, "end_year": 2031},
    "heavenly_layer": {"heavenly_stem": "Ất", "yin_yang": "Âm", "five_element": "Mộc"},
    "earth_layer": {"earthly_branch": "Tỵ", "hidden_stems": ["Bính", "Mậu", "Canh"]},
    "relationship": {"ten_god": "Chính Tài"}
  },
  "validation": {"ok": true, "failed": [], "confidence": 1.0},
  "notes": [
    "summary_is_machine_readable_only",
    "no_natural_language_interpretation",
    "cat_hung_not_evaluated_per_dayun_spec"
  ]
}
```

---

# 6. Compliance with DAYUN_SPEC.md

| Requirement | Compliance |
|-------------|------------|
| Do not evaluate cát hung (§4) | **YES** — UNKNOWN |
| Do not score (§2) | **YES** — `luck_strength=null` |
| Do not mutate upstream contexts | **YES** |
| Immutable / serializable runtime | **YES** |
| Validation fail-soft (§16) | **YES** — ValidationResult in metadata |
| Only Dayun scope (no Liunian rules) | **YES** |
| No invented BaZi school rules | **YES** |

---

# 7. Future work required for LIUNIAN_SPEC.md

| Item | Blocked on |
|------|------------|
| Annual Support/Attack vs Dayun + Mệnh | `LIUNIAN_SPEC.md` |
| Liunian strength / stage taxonomy | `LIUNIAN_SPEC.md` |
| Year-layer structured summary | `LIUNIAN_SPEC.md` |
| Interaction rules Dayun × Liunian | Both Dayun + Liunian specs |
| Non-UNKNOWN cát hung (if ever allowed) | Explicit business rules in knowledge — **not** in current DAYUN_SPEC |
| `luck_stage` vocabulary | Dedicated stage taxonomy in knowledge |
| Numeric `luck_strength` scale | Scoring contract (currently excluded by DAYUN_SPEC §2) |
| Interpretation / Report luck narrative | Downstream of real evaluation vocabulary |

---

END
