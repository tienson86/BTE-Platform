# INTERPRETATION_ENGINE_ARCHITECTURE_REPORT.md

Version: 1.0  
Date: 2026-08-07  
Pack: 04 — Interpretation Engine  
Status: IMPLEMENTED (Pack 04 narrative path + production RuleContext path preserved)

---

## 1. Position

```
Score Engine → AnalysisResult
        ↓
Interpretation Engine (Pack 04)
        ↓
NarrativeInterpretationResult
        ↓
Report Engine  ← out of scope
```

Production orchestrator path (unchanged):

```
RuleContext → InterpretationEngine.run() → legacy InterpretationResult → Portal
```

---

## 2. Dual-Path Architecture (Backward Compatible)

| Path | Entry | Input | Output |
|------|-------|-------|--------|
| Production WP5 | `run(context)` | RuleContext | legacy `InterpretationResult` |
| Pack 04 narrative | `interpret_from_analysis(analysis)` | Score `AnalysisResult` | `EngineResult[NarrativeInterpretationResult]` |

Score Engine, Foundation, UI, and Presentation were **not** modified.

---

## 3. Pack 04 Runtime Pipeline (implemented)

```
AnalysisResult
    ↓
Narrative Context Builder
    ↓
Evidence Collector
    ↓
Narrative Rule Matching
    ↓
Sentence Selection
    ↓
Placeholder Binding
    ↓
Interpretation Builder
    ↓
EngineResult<NarrativeInterpretationResult>
```

| Stage | Module |
|-------|--------|
| Narrative Context | `pack04/narrative_context.py` |
| Evidence | `pack04/evidence.py` |
| Rule Matching | `pack04/rule_matching.py` |
| Sentence Selection | `pack04/sentence_selection.py` |
| Placeholder Binding | `pack04/placeholder_binding.py` |
| Interpretation Builder | `pack04/interpretation_builder.py` |
| Orchestrator | `pack04/pipeline.py` |

---

## 4. Knowledge Assets

| Asset | Path |
|-------|------|
| Sentence library | `pack04/library/sentences.json` |
| Narrative rules | `pack04/library/narrative_rules.json` |

Narrative rule matching selects sentences from the Pack 04 library.  
It does **not** recalculate Score Engine analytical rules.

---

## 5. Aggregate Sections

Overview · Strength · Pattern · Useful God · Ten Gods · Five Elements · Season · Temperature · Summary

Each section holds rendered `NarrativeSentence` records with template id, placeholders, evidence refs, and rule id.

---

## 6. Dependency Direction

```
Interpretation (Pack 04)
    ↓ reads
Score Engine AnalysisResult
```

Lazy imports avoid loading Score Engine during WP5 package init.

---

## 7. Documented Gaps (deferred)

- Full Pack 04 Template Engine / Explanation Engine as separate services (templates are embedded on sentences for V1)
- Expansion of `knowledge/07_sentence_library` (framework remains empty; Pack 04 uses `pack04/library`)
- Migration of orchestrator from RuleContext → AnalysisResult (explicitly out of scope — stop after IE)
