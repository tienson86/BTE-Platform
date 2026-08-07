# SCORE_ENGINE_ARCHITECTURE_REPORT.md

Version: 1.0  
Date: 2026-08-07  
Pack: 03 — Score Engine  
Status: IMPLEMENTED (runtime aligned to production ScoreResult + Pack 03 aggregate)

---

## 1. Position in Platform Pipeline

```
BirthRequest
    ↓
Calendar Engine
    ↓
BaZi Engine → BaziChart
    ↓
(Pattern / RuleContext publish)
    ↓
Score Engine
    ↓
ScoreResult  (production)
AnalysisResult (Pack 03 aggregate via analyze())
    ↓
Interpretation Engine  ← out of scope for this epic
```

---

## 2. Runtime Pipeline (implemented)

```
RuleContext (bazi + wuxing + …)
    ↓
Module Calculators (ordered)
    ├── WuxingScoreCalculator          → five_elements / wuxing
    ├── SeasonScoreCalculator          → season
    ├── TemperatureScoreCalculator     → temperature
    ├── StrengthScoreCalculator        → strength
    ├── TenGodScoreCalculator          → ten_gods
    ├── PatternScoreCalculator         → pattern
    ├── UsefulGodScoreCalculator       → useful_god
    ├── ShenshaScoreCalculator         → shensha (extended)
    └── LuckScoreCalculator            → luck (extended)
    ↓
FinalScoreCalculator                   → overall / total
    ↓
ScoreResult
    ↓ (optional)
AnalysisResultBuilder → AnalysisResult
```

---

## 3. Responsibility Boundaries

| Layer | Responsibility |
|-------|----------------|
| Loader | Read CSV rules only |
| Matcher / Adapter | Rule Contract V1 matching |
| Calculators | Dimension scores only |
| FinalScoreCalculator | Weighted overall + grade |
| AnalysisResultBuilder | Aggregate construction + evidence |
| ScoreEngine | Orchestration |

Does **not**: interpret text, render reports, mutate published RuleContext, write database.

---

## 4. Aggregate Mapping (Pack 03)

| Pack 03 Node | Source |
|--------------|--------|
| StrengthAnalysis | `strength_score` + matched rules |
| SeasonAnalysis | `season_score` + `wuxing.season` |
| TemperatureAnalysis | `temperature_score` + `temperature.*` |
| FiveElementAnalysis | `wuxing_score` + element counts |
| TenGodAnalysis | `ten_god_score` + series |
| PatternAnalysis | `pattern_score` + pattern section |
| UsefulGodAnalysis | `useful_god_score` + useful_god section |
| OverallAnalysis | `total_score` / grade / confidence |
| EvidenceCollection | Matched rules from all modules |

---

## 5. Dependency Rules

- Score Engine depends **down** on RuleContext / Bazi facts.
- Score Engine does **not** import Interpretation or Report.
- Temperature scoring uses RuleContext facts + Score DB rules (no write to `temperature_engine`).
- Season scoring uses existing wuxing season CSV (read-only).

---

## 6. Backward Compatibility Strategy

| Concern | Strategy |
|---------|----------|
| Orchestrator | Still calls `calculate` → `ScoreResult` |
| Portal JSON | `to_portal_dict()` keys unchanged |
| Overall total | Season/Temperature weight = 0 (absent from dimension_weight) |
| Pack 03 API | Additive `analyze()` + `AnalysisResult` |
| Aliases | `five_elements_score`, `overall_score` properties |

---

## 7. Known Architecture Gaps (documented, not blocking)

Pack 03 docs describe full Evidence → Conflict → Priority → Scoring stages as separate engines.

Current implementation:

- Matching + scoring remain inside GenericScoreCalculator / FinalScoreCalculator
- Evidence is collected post-hoc from matched rules
- Dedicated Conflict Resolver / Priority Engine stages are not yet separate runtime services

These are deferred; production stability and Pack 03 aggregate delivery take priority for this epic.

---

## 8. Database Extension

| Path | Purpose |
|------|---------|
| `15_score_engine/10_temperature/01_temperature_level.csv` | Temperature dimension rules |

No existing columns renamed. No Golden Dataset edits.
