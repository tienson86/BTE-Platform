# Sprint 4.5 Liuyue Rule Implementation Report

| Item | Value |
|------|-------|
| Document | `SPRINT45_LIUYUE_RULE_IMPLEMENTATION_REPORT.md` |
| Project | BTE Platform V1.0 |
| Sprint | Sprint 4.5 — Liuyue Rule-Based Evaluation |
| Spec | `knowledge/luck_engine/03_liuyue/LIUYUE_SPEC.md` v1.0 (written §§1–20; §§21–36 incomplete) |
| Prerequisites | Sprint 4 / 4.1 / 4.2 / 4.3 / 4.4 reports |
| Case | Male · 21/01/1987 · 04:30 · Asia/Ho_Chi_Minh |
| Date | 2026-07-28 |

---

# 1. Files modified

| File | Change |
|------|--------|
| `engines/luck_engine/liuyue_validation.py` | **NEW** — structural validation per LIUYUE_SPEC §§8–16 / §§5–6 |
| `engines/luck_engine/evaluators/liuyue.py` | **NEW** — Liuyue Support/Attack/Strength/Stage |
| `engines/luck_engine/evaluators/layered.py` | Extended Dayun → Liunian → **Liuyue** merge + summary |
| `engines/luck_engine/evaluators/__init__.py` | Export Liuyue APIs |
| `engines/luck_engine/engine.py` | Sprint `4.5`; layer_order includes `liuyue` |
| `engines/luck_engine/__init__.py` | Public exports |

**Preserved:** Dayun + Liunian evaluators/validation (Sprint 4.3 / 4.4).

**Not modified:** Calendar, BaZi, Pattern, RuleContext, Score, Knowledge, Interpretation, Luck Providers / interfaces, LuckContext schema, Support→Attack→Strength→Stage→Summary pipeline slots, frontend, tests, Golden Dataset.

---

# 2. Implemented Liuyue rules

Source: **written LIUYUE_SPEC.md only**. No invented clash/seasonal scoring.

| Spec section | Implementation |
|--------------|----------------|
| §§7–8 MonthlyContext structure | `liuyue_runtime_snapshot` |
| §§9–10 Solar-term month determination | Require `solar_term`; match month_index → major term |
| §11 Monthly sequence Dần→…→Sửu | Branch must match `month_index` |
| §12 Five Tiger Dunjia (五虎遁) | Stem vs Liunian year stem + month_index |
| §14 Hidden stems (DB order) | Match `BRANCH_HIDDEN` |
| §15 Ten Gods present | Require monthly-stem ten_god label |
| §16 Five Element mapping | Require element + yin/yang |
| §§5–6 Dayun / Liunian inputs | Readiness checks |
| §§17–20 / 21–36 Interactions & strength | `UNKNOWN` / deferred — Rule DB + incomplete SPEC |

### Layering (coexistence)

```text
Providers
    ↓
Support / Attack / Strength / Stage
    (Dayun → Liunian → Liuyue → merge)
    ↓
CombinedLuckSummaryBuilder
    ↓
LuckContext
```

| Evaluator | Role |
|-----------|------|
| `LiuyueSupportEvaluator` | `UNKNOWN` + validation metadata |
| `LiuyueAttackEvaluator` | `UNKNOWN` + reasons |
| `LiuyueLuckStrengthEvaluator` | `NULL` strength (§26 incomplete); validation confidence |
| `LiuyueLuckStageEvaluator` | `UNKNOWN` |
| `Layered*Evaluator` | Three-layer merge (backward compatible kwargs) |
| `CombinedLuckSummaryBuilder` | Dayun + Liunian + Liuyue JSON |

---

# 3. Validation results

Case: Male · 21/01/1987 · 04:30 · Asia/Ho_Chi_Minh

| Check | Result |
|-------|--------|
| Score unchanged | **PASS** — `total_score=55.25` |
| Dayun unchanged | **PASS** — Ất Tỵ; validation `ok=true` |
| Liunian unchanged | **PASS** — Bính Ngọ 2026; validation `ok=true` |
| Liuyue populated | **PASS** — Ất Mùi · month_index 6 · Tiểu Thử; validation `ok=true` |
| RuleContext unchanged | **PASS** |
| Pipeline slots unchanged | **PASS** |
| Layer order | **PASS** — `["dayun", "liunian", "liuyue"]` |

### Tests

| Suite | Result |
|-------|--------|
| `pytest tests/score -q` | **38 passed** |
| `pytest tests/luck -q` | **N/A** — not present |

---

# 4. Runtime output example

```text
available=true
current_dayun=Ất Tỵ
current_liunian=Bính Ngọ (2026)
current_liuyue=Ất Mùi (month_index=6, solar_term=Tiểu Thử)
support_level=UNKNOWN
attack_level=UNKNOWN
luck_strength=null
confidence=1.0
luck_stage=UNKNOWN
```

---

# 5. Remaining UNKNOWN / NULL fields

| Field | Value | Why |
|-------|-------|-----|
| `support_level` / elements | `UNKNOWN` / `[]` | No support taxonomy in written SPEC |
| `attack_level` / elements | `UNKNOWN` / `[]` | Clash/harm need Rule Database |
| `luck_strength` | `null` | §26 Seasonal Strength not written |
| `luck_stage` | `UNKNOWN` | No stage taxonomy |
| Stem/Branch/Hidden interactions | UNKNOWN | §§18–20 need Rule DB |
| Seasonal influence details | UNKNOWN | §17 / §26 incomplete |
| LiuNian/Dayun relation results | UNKNOWN | §§21–22 not written |
| Useful/Unfavorable god interaction | not populated | §§27–28 not written |

---

# 6. Combined runtime summary structure

```json
{
  "kind": "dayun_liunian_liuyue_runtime_summary",
  "layer_order": ["dayun", "liunian", "liuyue"],
  "specs": {
    "dayun": "DAYUN_SPEC.md",
    "liunian": "LIUNIAN_SPEC.md",
    "liuyue": "LIUYUE_SPEC.md"
  },
  "dayun_runtime": { "...": "..." },
  "liunian_runtime": { "...": "..." },
  "liuyue_runtime": {
    "monthly_pillar": {
      "year": 2026,
      "month": 7,
      "month_index": 6,
      "ganzhi": "Ất Mùi",
      "heavenly_stem": "Ất",
      "earthly_branch": "Mùi",
      "solar_term": "Tiểu Thử"
    },
    "hidden_stems": ["Kỷ", "Đinh", "Ất"],
    "ten_gods": {"monthly_stem": "Chính Tài"},
    "seasonal_influence": {"status": "UNKNOWN"},
    "interactions": {"status": "UNKNOWN"}
  },
  "validation": {
    "dayun": {"ok": true, "confidence": 1.0},
    "liunian": {"ok": true, "confidence": 1.0},
    "liuyue": {"ok": true, "confidence": 1.0, "failed": []}
  },
  "evaluation": {
    "support_level": "UNKNOWN",
    "attack_level": "UNKNOWN",
    "luck_strength": null,
    "luck_stage": "UNKNOWN",
    "confidence": 1.0
  },
  "notes": [
    "summary_is_machine_readable_only",
    "no_natural_language_interpretation",
    "dayun_liunian_liuyue_coexist",
    "interaction_detection_deferred_pending_rule_database"
  ]
}
```

Sprint 4.4 keys `dayun_runtime` / `liunian_runtime` remain present (backward compatible).

---

# 7. Compliance with LIUYUE_SPEC.md

| Requirement | Compliance |
|-------------|------------|
| Deterministic / rule-based / no AI (§2) | **YES** |
| No NL / report rendering (Excluded) | **YES** |
| Solar-term months only (§9–11) | **YES** — validated |
| Five Tiger Dunjia (§12) | **YES** — validated vs Liunian stem |
| Hidden stems / ten gods / elements | **YES** — validated |
| Do not invent undocumented BaZi logic | **YES** |
| Dayun + Liunian coexistence | **YES** |
| LiuRi / LiuShi excluded | **YES** |
| Incomplete §§21–36 | Honest UNKNOWN/NULL |

---

# 8. Outstanding work for LIURI_SPEC.md

| Item | Depends on |
|------|------------|
| Daily pillar evaluation layer | `LIURI_SPEC.md` |
| Layer Dayun → Liunian → Liuyue → **Liuri** | Same layered pattern |
| Day × Month × Year × Dayun interactions | Liuri + completed Liuyue interaction tables |
| Complete LIUYUE_SPEC Part 2 | §§21–36 (relations, seasonal strength, risk, validation taxonomy) |
| Rule Database wiring for clash/harmony/punishment/harm | Shared rule DB |
| Non-UNKNOWN Support/Attack levels | Explicit taxonomies in knowledge specs |
| LiuShi / unified timeline | Later specs |

---

END
