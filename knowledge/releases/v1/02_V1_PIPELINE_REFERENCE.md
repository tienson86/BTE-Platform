# 02 — BTE V1 Pipeline Reference

Version: 1.0  
Status: **CANONICAL** — Release Candidate A  
Date: 2026-08-08  
Scope: Documentation only

---

## 1. Purpose

Document the **official production pipeline** and every interface between stages for BTE V1.

Two views are canonical:

1. **Commercial narrative path** — official Result Page prose.  
2. **Orchestrator stage path** — full `/analyze` production run.

---

## 2. Commercial Narrative Path (Official Product Path)

```
Knowledge Database
        ↓
Rule Database
        ↓
Score Engine (+ upstream analysis stages)
        ↓
AnalysisResult / analysis fact bag
        ↓
Interpretation Engine
        ↓
InterpretationResult / interpretation payload
        ↓
Narrative Runtime (D1)
        ↓
NarrativeTree
        ↓
Narrative Composer (D2)
        ↓
NarrativeResult
        ↓
Application API (`data.narrative_result`)
        ↓
Portal Adapter (`adaptAnalysisToCanonicalDesktop`)
        ↓
Canonical Desktop ViewModel (+ `narrativeResult`)
        ↓
Result Presentation Adapter (`adaptResultPageViewModel`)
        ↓
Result Page ViewModel
        ↓
Result Page (zones / cards)
```

---

## 3. Stage Interfaces (Commercial Path)

| From → To | Interface | Contract notes |
|-----------|-----------|----------------|
| Knowledge → Rule DB | CSV / JSON rule files via Loaders | Read-only; stable schema |
| Rule DB → Score / Matching | Loader + RuleContext | Engines do not write DB |
| Score (+ peers) → Analysis | `AnalysisResult` / payload slices (`bazi`, `pattern`, `score`, `strength`, `useful_god`, …) | Fact authority |
| Analysis → Interpretation | Analysis + RuleContext / matched rules | Interpretation does not invent chart facts |
| Interpretation → Narrative Runtime | Analysis bag + interpretation dict / result | Evidence only; insufficient → Insufficient Evidence state |
| Runtime → Tree | `NarrativeTree` | Structure only; no prose |
| Tree → Composer | `NarrativeTree` + SourceBundle facts | Source-traced sentences; no invented facts |
| Composer → API | `NarrativeResult.to_dict()` + `contract: pack05_narrative_result_v1` | Official commercial narrative |
| API → Portal Adapter | `AnalysisDataDto.narrative_result` | Prefer over `interpretation` |
| Adapter → Canonical VM | `CanonicalDesktopViewModel.narrativeResult` | S01 / S08 / S11 prefer Pack 05 |
| Canonical VM → Result VM | Presentation mapping only | No BaZi business logic in presentation |
| Result VM → UI | Zone / card props | Foundation layout patterns |

---

## 4. Full Orchestrator Pipeline (`/analyze`)

Canonical stage order in `OrchestratorService` (`PIPELINE_ORDER`):

```
0  input
1  calendar
2  bazi
3  feng_shui          (optional soft-fail)
3.5 strength          (feeds PatternContext)
3.6 temperature       (feeds PatternContext)
4  pattern
5  rule_context       (Pattern-published; immutable snapshot)
6  score
7  luck               (LuckContext; does not mutate RuleContext)
8  knowledge
9  matching
10 priority
11 interpretation
   + Pack 05 narrative_result publish (API layer)
12 report
13 delivery           (payload field `narrative` = Report delivery)
```

Stage stop aliases include BC name `narrative` → delivery.

---

## 5. Orchestrator Stage Interfaces

| Stage | Primary output on payload | Downstream consumers |
|-------|---------------------------|----------------------|
| `input` | Validated birth / gender / request meta | All |
| `calendar` | `calendar` | BaZi, Pattern, UI |
| `bazi` | `bazi` | Pattern, Score, UI |
| `feng_shui` | `feng_shui` (best-effort) | UI S09 |
| `pattern` | `pattern` | RuleContext, Score labels, UI |
| `rule_context` | Published RuleContext snapshot | Score, Matching, Interpretation |
| `score` | `score` / strength refresh | Interpretation, UI |
| `luck` | LuckContext | Interpretation (optional) |
| `knowledge` | Knowledge match inputs | Matching |
| `matching` | Matched rules | Priority |
| `priority` | Ordered rules | Interpretation |
| `interpretation` | `interpretation` + `interpretation_source` | Narrative, Report, legacy Portal fallback |
| *(after interpretation)* | `narrative_result` + `narrative_result_source` | **Official Portal commercial prose** |
| `report` | `report` | Delivery |
| `delivery` | `narrative` (title / markdown / html) | Legacy delivery clients |

---

## 6. Naming Contracts (Critical)

| Payload field | Meaning | V1 official? |
|---------------|---------|--------------|
| `narrative_result` | Pack 05 commercial `NarrativeResult` | **Yes — official** |
| `interpretation` | Interpretation Engine sections | Legacy + evidence + fallback |
| `narrative` | ReportEngine delivery markdown/html | Delivery BC — **not** Pack 05 |
| `report` | Report view object | Formatting / delivery |

---

## 7. Portal Adapter Pipeline

```
POST /api/v1/analyze  (or stored analyze payload)
        ↓
AnalysisDataDto
        ↓
adaptAnalysisToCanonicalDesktop(...)
        ↓
CanonicalDesktopViewModel
        ↓
adaptResultPageViewModel(...)
        ↓
ResultPageViewModel
        ↓
PortalPage / Result zones (Executive, Analysis, Recommendation, Interpretation, Knowledge, …)
```

Preference rule (frozen for V1):

1. If `narrative_result` usable (`contract` Pack 05 or equivalent usable shape) → use it for commercial prose.  
2. Else fall back to legacy `interpretation` / derived S08 lists.  
3. Always gate rule-prose / non-commercial text via content guards where applicable.

---

## 8. Out of Pipeline (V1)

| System | Status |
|--------|--------|
| Report Engine redesign consuming NarrativeResult | Future |
| Bone-weight / S10 full engine | Not in production pipeline |
| LLM generation | Not part of V1 narrative |

---

## 9. Validation Gates (Conceptual)

```
Validate input → Calculate / Compose → Validate output → Publish Result
```

Applies per engine. Portal adapters **format and prefer**; they do not recalculate analysis.

---

END
