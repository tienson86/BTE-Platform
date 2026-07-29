# Sprint 4.4 Liunian Rule Implementation Report

| Item | Value |
|------|-------|
| Document | `SPRINT44_LIUNIAN_RULE_IMPLEMENTATION_REPORT.md` |
| Project | BTE Platform V1.0 |
| Sprint | Sprint 4.4 — Liunian Rule-Based Evaluation |
| Spec | `knowledge/luck_engine/02_liunian/LIUNIAN_SPEC.md` v1.0 (written §§1–20; §§21–36 incomplete) |
| Prerequisites | Sprint 4 / 4.1 / 4.2 / 4.3 reports |
| Case | Male · 21/01/1987 · 04:30 · Asia/Ho_Chi_Minh |
| Date | 2026-07-28 |

---

# 1. Files modified

| File | Change |
|------|--------|
| `engines/luck_engine/liunian_validation.py` | **NEW** — structural validation per LIUNIAN_SPEC §§8–13 / §18 |
| `engines/luck_engine/evaluators/liunian.py` | **NEW** — Liunian Support/Attack/Strength/Stage |
| `engines/luck_engine/evaluators/layered.py` | **NEW** — Dayun → Liunian layered evaluators + combined summary |
| `engines/luck_engine/evaluators/__init__.py` | Export Liunian + layered APIs |
| `engines/luck_engine/engine.py` | Default to layered evaluators; sprint `4.4` |
| `engines/luck_engine/__init__.py` | Public exports |

**Preserved (not replaced):** Dayun evaluators (`evaluators/dayun.py`, `dayun_validation.py`).

**Not modified:** Calendar, BaZi, Pattern, RuleContext, Score, Knowledge, Interpretation, Luck Providers, LuckContext schema, Support→Attack→Strength→Stage→Summary pipeline slots, frontend, tests, Golden Dataset.

---

# 2. Implemented Liunian rules

Source: **written LIUNIAN_SPEC.md only**. No heuristic clash/harmony tables invented.

| Spec section | Implementation |
|--------------|----------------|
| §§7–8 Output / AnnualContext structure | `liunian_runtime_snapshot` |
| §§9–10 Annual pillar / Li Chun year | Validate `year` + `bazi_year` metadata |
| §11 Hidden stems (database order) | Match `BRANCH_HIDDEN` |
| §12 Ten Gods present | Require annual-stem ten_god label |
| §13 Five Element mapping | Require element + yin/yang |
| §18 Dayun interaction readiness | Require current Dayun stem/branch present |
| §§14–17 / 19–20 Interactions / Tai Sui / Kong Wang | Status `UNKNOWN` — need Rule Database; not fabricated |
| §§21–33 (unwritten) | Deferred — Support/Attack/Strength taxonomies UNKNOWN/NULL |

### Layering (coexistence)

```text
Providers
    ↓
Support / Attack / Strength / Stage
    (each slot: Dayun evaluator → Liunian evaluator → merge)
    ↓
CombinedLuckSummaryBuilder
    ↓
LuckContext
```

Dayun classes remain injectable and unchanged.

| Evaluator | Role |
|-----------|------|
| `LiunianSupportEvaluator` | `UNKNOWN` + validation metadata + reasons |
| `LiunianAttackEvaluator` | `UNKNOWN` + reasons (clash rules need DB) |
| `LiunianLuckStrengthEvaluator` | `luck_strength=NULL` (§27 not written); validation confidence |
| `LiunianLuckStageEvaluator` | `UNKNOWN` (no taxonomy) |
| `Layered*Evaluator` | Dayun then Liunian merge |
| `CombinedLuckSummaryBuilder` | JSON with DayunRuntime + LiunianRuntime |

---

# 3. Validation results

Case: Male · 21/01/1987 · 04:30 · Asia/Ho_Chi_Minh

| Check | Result |
|-------|--------|
| Score unchanged | **PASS** — `total_score=55.25` |
| Dayun unchanged | **PASS** — Ất Tỵ; Dayun validation `ok=true` |
| Liunian populated | **PASS** — Bính Ngọ · year 2026; validation `ok=true` |
| RuleContext unchanged | **PASS** — Luck read-only |
| Pipeline slots unchanged | **PASS** — support → attack → strength → stage → summary |
| Layer order | **PASS** — `["dayun", "liunian"]` |
| No invented interactions | **PASS** — interactions status `UNKNOWN` |

### Tests

| Suite | Result |
|-------|--------|
| `pytest tests/score -q` | **38 passed** |
| `pytest tests/luck -q` | **N/A** — `tests/luck` not present |

---

# 4. Runtime output example

```text
available=true
current_dayun=Ất Tỵ
current_liunian=Bính Ngọ (2026)
support_level=UNKNOWN  support_elements=[]
attack_level=UNKNOWN   attack_elements=[]
luck_strength=null
confidence=1.0
luck_stage=UNKNOWN
luck_summary=<JSON dayun_liunian_runtime_summary>
```

Structured summary (abbreviated):

```json
{
  "kind": "dayun_liunian_runtime_summary",
  "layer_order": ["dayun", "liunian"],
  "specs": {"dayun": "DAYUN_SPEC.md", "liunian": "LIUNIAN_SPEC.md"},
  "dayun_runtime": { "identity": {"index": 3}, "...": "..." },
  "liunian_runtime": {
    "annual_pillar": {
      "year": 2026,
      "ganzhi": "Bính Ngọ",
      "heavenly_stem": "Bính",
      "earthly_branch": "Ngọ"
    },
    "hidden_stems": ["Đinh", "Kỷ"],
    "ten_gods": {"annual_stem": "Thất Sát"},
    "interactions": {
      "status": "UNKNOWN",
      "reason": "liunian_spec_interaction_tables_require_rule_database"
    }
  },
  "validation": {
    "dayun": {"ok": true, "confidence": 1.0},
    "liunian": {"ok": true, "confidence": 1.0, "failed": []}
  },
  "notes": [
    "summary_is_machine_readable_only",
    "no_natural_language_interpretation",
    "dayun_and_liunian_coexist",
    "interaction_detection_deferred_pending_rule_database"
  ]
}
```

---

# 5. Remaining UNKNOWN fields

| Field | Value | Why |
|-------|-------|-----|
| `support_level` / elements | `UNKNOWN` / `[]` | No support taxonomy in written SPEC |
| `attack_level` / elements | `UNKNOWN` / `[]` | Clash/harm need Rule Database; §§21–33 incomplete |
| `luck_strength` | `null` | §27 Annual Strength not written |
| `luck_stage` | `UNKNOWN` | No stage taxonomy |
| Stem/Branch/Hidden interactions | empty + UNKNOWN | Detection listed but tables not in SPEC |
| Tai Sui / Kong Wang results | UNKNOWN | §§19–20 incomplete without special-rule DB |
| Fu Yin / Fan Yin / Priority / Risk | not populated | §§21–30 not written in SPEC file |

`confidence` remains validation pass-rate (runtime quality), not a favorable/unfavorable score.

---

# 6. Compliance with LIUNIAN_SPEC.md

| Requirement | Compliance |
|-------------|------------|
| Deterministic / no interpretation (§2) | **YES** |
| No NL generation (§2 / Excluded) | **YES** |
| Annual pillar / hidden / ten god / element contracts | **YES** — validated |
| Do not invent undocumented BaZi logic | **YES** |
| Dayun coexistence (§18 readiness) | **YES** |
| LiuYue / LiuRi / LiuShi excluded | **YES** |
| Incomplete §§21–33 | Honest UNKNOWN/NULL — not fabricated |

---

# 7. Outstanding work for LIUYUE_SPEC.md

| Item | Depends on |
|------|------------|
| Monthly pillar evaluation layer | `LIUYUE_SPEC.md` |
| Layer Dayun → Liunian → **Liuyue** | Same layered pattern |
| Month × Year × Dayun interaction rules | Liuyue + completed Liunian interaction tables |
| Complete LIUNIAN_SPEC Part 2/3 | §§21–36 (Fu Yin, strength, useful god, risk, validation taxonomy) |
| Rule Database wiring for clash/harmony/punishment/harm | Shared rule DB contract |
| Non-UNKNOWN Support/Attack levels | Explicit level taxonomies in knowledge specs |
| Numeric annual strength | LIUNIAN_SPEC §27 when written |
| Interpretation consumption | Downstream only after real evaluation vocabulary exists |

---

END
