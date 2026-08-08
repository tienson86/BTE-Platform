# 04 — BTE V1 Dependency Graph

Version: 1.0  
Status: **CANONICAL** — Release Candidate A  
Date: 2026-08-08  
Scope: Documentation only

---

## 1. Purpose

Official dependency graph for BTE V1.  
Direction of arrows = **depends on / consumes**.

Illegal: reverse imports (e.g. Score importing Narrative; Portal importing engine internals).

---

## 2. Engine Dependency Graph

```
                    ┌──────────────────┐
                    │  Rule Database   │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        Calendar          Loaders        Knowledge
              │
              ▼
            BaZi
              │
    ┌─────────┼─────────┬────────────┐
    ▼         ▼         ▼            ▼
 Strength  Temperature  Feng Shui   Pattern
    │         │                      │
    └────┬────┘                      │
         └──────────► Pattern ───────┘
                         │
                         ▼
                   RuleContext
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
       Score            Luck         Matching/Priority
         │               │               │
         └───────┬───────┴───────┬───────┘
                 ▼               ▼
            Analysis facts   Interpretation
                                 │
                                 ▼
                         Narrative Engine
                         (Runtime → Composer)
                                 │
                                 ▼
                          NarrativeResult
                                 │
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                  ▼
           API publish     (future Report)    Portal adapters
```

Supporting: Useful God / Context feed Score / UI labels without reversing layer direction.

---

## 3. Narrative Dependencies

```
Analysis facts ──────────────┐
                             ├──► Narrative Runtime ──► NarrativeTree
Interpretation evidence ─────┘              │
                                            ▼
                                   Narrative Composer
                                            │
                                            ▼
                                     NarrativeResult
```

Narrative **must not** depend on Portal, Foundation, or Report layout.

WP7 `NarrativeReport` prose path may still exist inside the package for BC; Pack 05 `NarrativeResult` is the **official commercial** output for Portal.

---

## 4. Portal Dependencies

```
API JSON (AnalysisDataDto)
        │
        ├──► narrativeResultAdapter (helpers)
        │
        ├──► canonicalDesktopAdapter ──► CanonicalDesktopViewModel
        │                                      │
        │                                      ▼
        │                         resultPresentationAdapter
        │                                      │
        │                                      ▼
        │                              ResultPageViewModel
        │                                      │
        │                                      ▼
        │                         Result Page (Foundation components)
        │
        └──► baziResultAdapter ──► BaZiResultViewModel ──► BaZiResultScreen
             (parallel / deprecated path)
```

Portal depends on:

- API DTO shapes  
- Foundation / Design System  
- Adapter layer  

Portal does **not** depend on:

- Engine Python packages  
- Rule CSV loaders  
- Narrative Runtime internals  

---

## 5. Report Dependencies (V1 As-Is)

```
Interpretation / Analysis views
        │
        ▼
Report Engine (current)
        │
        ▼
report + delivery `narrative` (markdown/html)
```

**Future (not V1 implemented):**

```
NarrativeResult ──► Report Engine (redesign) ──► Printable / export layouts
```

V1 forbids Report Engine from becoming the authority that re-scrapes Interpretation to replace Pack 05.

---

## 6. Pack Relationships

```
Pack 01 Calendar ──► Pack 02 BaZi ──► Pack 03 Score
                                         │
                                         ▼
                                   Pack 04 Interpretation
                                         │
                                         ▼
                                   Pack 05 Narrative ──► Product Integration (Portal)
                                         │
                                         ╰──► Pack 05 Report (future consumer of NarrativeResult)

UI Foundation V1.0 ──► Design System ──► Portal screens
```

Note: Folder naming uses `pack_05_narrative_engine` and `pack_05_report_engine`. They are **sibling concerns**; Narrative is complete for V1 commercial prose; Report redesign is deferred.

---

## 7. Application Dependency Slice

```
HTTP routes
    │
    ▼
OrchestratorService
    ├── CalendarEngine
    ├── BaziEngine
    ├── Pattern / Strength / Temperature / FengShui / …
    ├── ScoreEngine
    ├── LuckEngine
    ├── InterpretationEngine
    ├── build_narrative_result_dict → NarrativeEngine (public)
    ├── ReportEngine
    └── delivery narrative view
```

---

## 8. Forbidden Edges (Frozen)

| From | To | Why forbidden |
|------|-----|---------------|
| Portal | `engines.*` internals | Cross-language / layer violation |
| Narrative | Portal ViewModels | Engine purity |
| Score | Interpretation / Narrative | Reverse pipeline |
| Interpretation | Report layout / UI tokens | Wrong responsibility |
| Any engine | Database write | Database read-only rule |
| Feature code | Foundation doc edits | Foundation freeze |

---

END
