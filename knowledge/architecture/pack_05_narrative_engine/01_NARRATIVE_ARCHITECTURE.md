# 01_NARRATIVE_ARCHITECTURE.md

Version: 1.0

Status: DRAFT — Sprint A Architecture

Pack: 05 (Narrative Engine)

Engine: Narrative Engine

---

# 1. Purpose

The Narrative Engine transforms a canonical **AnalysisResult** into a customer-facing **NarrativeResult**.

Its responsibility is commercial storytelling from analytical facts.

The Narrative Engine never performs analysis.

The Narrative Engine never recalculates scores.

The Narrative Engine never executes rule matching for scoring.

The Narrative Engine never renders UI, PDF, or layout themes.

---

# 2. Goals

| Goal | Description |
|------|-------------|
| Commercial language | Produce natural language suitable for consultants and customers |
| Fact fidelity | Every narrative claim must trace to AnalysisResult evidence |
| Separation of concerns | Separate Interpretation (analytical expression) from Narrative (commercial story) |
| Portal readiness | Supply clean sections for Result Page Executive / cards without technical rule prose |
| Report readiness | Supply NarrativeResult as preferred input to Report Engine |
| Determinism | Same AnalysisResult → same NarrativeResult (given same narrative assets / locale) |
| Extensibility | Allow new section types without changing Score or Interpretation public APIs |

---

# 3. Responsibilities

The Narrative Engine is responsible for

✓ Evidence extraction from AnalysisResult (and optional InterpretationResult)

✓ Narrative composition policy (what to say, in what order, at what depth)

✓ Section construction (who / strengths / weaknesses / recommendations / …)

✓ Story assembly (coherent NarrativeResult)

✓ Commercial tone constraints (no rule-activation prose, no developer text)

✓ Traceability metadata (evidence references per paragraph)

✓ Validation of NarrativeResult completeness for required commercial questions

The Narrative Engine is **NOT** responsible for

✗ Calendar / BaZi / Pattern / Strength / Useful God calculation

✗ Score calculation or grade changes

✗ Rule database matching for analytical conclusions

✗ Inventing facts not present in AnalysisResult

✗ Portal ViewModel adaptation

✗ Report layout, theme, render, or export

✗ Design System / Visual Language / Foundation documents

---

# 4. Scope

## In Scope (architecture)

- NarrativeContext lifecycle  
- Evidence model and evidence selection rules  
- Narrative Composer responsibilities  
- Narrative Section Builder responsibilities  
- Narrative Story Builder responsibilities  
- NarrativeResult aggregate and public API  
- Interaction contracts with Score, Interpretation, Portal, Report  

## Out of Scope (this sprint and this engine)

| Out of Scope | Owner |
|--------------|-------|
| Implementation code | Future sprints |
| Sentence / template authoring | Knowledge / content sprints |
| UI redesign | Portal / Foundation (frozen) |
| Changing Interpretation Engine | Pack 04 |
| Changing Score Engine | Pack 03 |
| Changing Report Layout/Theme engines | `pack_05_report_engine` |
| Hard-coded business rules in Narrative | Forbidden — use AnalysisResult + narrative assets |

---

# 5. Position in Platform Pipeline

```
BirthRequest
    ↓
Calendar Engine
    ↓
BaZi Engine
    ↓
Pattern / Strength / Useful God / Score
    ↓
AnalysisResult                          ← authoritative analytical facts
    ↓
Interpretation Engine
    ↓
InterpretationResult                    ← structured analytical expression
    ↓
Narrative Engine                        ← commercial story (THIS PACK)
    ↓
NarrativeResult
    ↓
Report Engine  /  Portal Adapter
    ↓
ReportResult   /  Result Page ViewModels
```

**Canonical analytical truth** remains AnalysisResult.

**Canonical commercial story** becomes NarrativeResult.

InterpretationResult may feed Narrative as optional evidence; it must not replace AnalysisResult as the fact source.

---

# 6. Layer Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Delivery Layer                            │
│         Portal Adapter · Report Engine · API views           │
└───────────────────────────▲─────────────────────────────────┘
                            │ NarrativeResult
┌───────────────────────────┴─────────────────────────────────┐
│                 Narrative Engine Layer                        │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │  Evidence    │→ │  Composer    │→ │  Section Builder   │  │
│  └─────────────┘  └──────────────┘  └─────────┬──────────┘  │
│                                               ↓               │
│                                     ┌────────────────────┐  │
│                                     │  Story Builder     │  │
│                                     └─────────┬──────────┘  │
│                                               ↓               │
│                                     NarrativeResult           │
└───────────────────────────▲─────────────────────────────────┘
                            │ AnalysisResult (+ optional InterpretationResult)
┌───────────────────────────┴─────────────────────────────────┐
│              Analytical Layer                                 │
│     Score Engine · Interpretation Engine · Knowledge          │
└─────────────────────────────────────────────────────────────┘
```

---

# 7. Module Diagram

Architecture modules (logical — not an implementation layout decision):

```
Narrative Engine
├── NarrativeContext Builder
├── Evidence Extractor
├── Narrative Composer
├── Narrative Section Builder
├── Narrative Story Builder
├── Narrative Validator
└── NarrativeEngine (Public Facade)
```

| Module | Responsibility |
|--------|----------------|
| NarrativeContext Builder | Build immutable runtime context from AnalysisResult |
| Evidence Extractor | Collect typed evidence units (strength, pattern, useful god, score, …) |
| Narrative Composer | Decide section plan, priority, and composition policy |
| Narrative Section Builder | Build NarrativeSection + paragraphs for one section intent |
| Narrative Story Builder | Assemble sections into NarrativeSummary + NarrativeResult |
| Narrative Validator | Validate required commercial answers and evidence linkage |
| NarrativeEngine | Public orchestration only |

Internal modules are not part of the Public API.

---

# 8. Dependency Rules

## Rule 1 — One-way dependency

```
Score → Interpretation → Narrative → Report / Portal
```

No reverse imports.

## Rule 2 — Facts over prose

Narrative claims must cite Evidence derived from AnalysisResult.

Interpretation prose may be used only if it passes commercial suitability; it never overrides AnalysisResult facts.

## Rule 3 — No scoring in Narrative

Narrative must not recompute strength, pattern, or grade.

## Rule 4 — No UI in Narrative

Narrative returns models only.

Portal adapters map NarrativeResult → ViewModels.

## Rule 5 — No invention

If evidence is insufficient for a required commercial answer, Narrative emits an explicit insufficient-data outcome for that slot.

It must not invent consultant conclusions.

## Rule 6 — Stateless engine

NarrativeEngine is stateless.

All state lives in NarrativeContext / NarrativeResult for one run.

---

# 9. Interaction with Score Engine

| Aspect | Contract |
|--------|----------|
| Input | AnalysisResult (canonical) |
| Narrative may read | strength, pattern, useful god, five elements, ten gods, grade, recommendation fields, confidence |
| Narrative must not | call Score calculators, mutate ScoreResult, alter grade |
| Failure mode | If AnalysisResult invalid → NarrativeEngine error (no partial fake story) |

Score owns analytical truth.

Narrative owns commercial wording of that truth.

---

# 10. Interaction with Interpretation Engine

| Aspect | Contract |
|--------|----------|
| Primary fact source | AnalysisResult |
| Optional evidence | InterpretationResult sections / sentences |
| Use of Interpretation | Candidate phrasing or section hints after commercial filter |
| Must not | Treat rule-activation text as customer narrative |
| Must not | Modify InterpretationResult |
| Coexistence | Interpretation remains available for analytical / audit views |

**Separation principle**

```
Interpretation  = analytical expression of conclusions
Narrative       = commercial story for the customer
```

Both may exist in one pipeline.

Portal commercial cards prefer NarrativeResult.

---

# 11. Interaction with Portal Adapter

| Aspect | Contract |
|--------|----------|
| Portal consumes | NarrativeResult (preferred) |
| Fallback | Existing Interpretation / Score fields only when Narrative absent (compatibility) |
| Mapping ownership | Portal Adapter |
| Narrative must not | Know Result Page zones, cards, or Design System packs |
| Required commercial answers | Who / Strengths / Weaknesses / Priority recommendation / Next action |

Portal never invents narrative content.

If Narrative marks insufficient data, Portal displays the platform unavailable message.

---

# 12. Interaction with Report Engine

| Aspect | Contract |
|--------|----------|
| Preferred Report input | NarrativeResult |
| Legacy Report input | InterpretationResult (backward compatibility) |
| Report responsibilities | Layout, theme, render, export |
| Narrative responsibilities | Story content only |
| Report must not | Rewrite commercial meaning |
| Narrative must not | Produce HTML/PDF layout |

```
NarrativeResult  →  Report Engine  →  ReportResult
```

Report formats Narrative; it does not author it.

---

# 13. Commercial Content Principles

Narrative output must answer:

1. Who is this person?  
2. Main strengths  
3. Main weaknesses  
4. Priority recommendation  
5. Next action  

Narrative output must avoid:

- Rule descriptions (“Kích hoạt khi…”)  
- Developer / pack references  
- Raw engine identifiers as customer prose  
- Calculator tone without consultant meaning  

Tone follows Brand Language: consultant, not calculator.

(Foundation documents remain frozen; Narrative complies, does not edit them.)

---

# 14. Architecture Decision Summary

| Decision | Choice |
|----------|--------|
| Aggregate output | NarrativeResult |
| Primary input | AnalysisResult |
| Optional input | InterpretationResult |
| Downstream preferred consumer | Report Engine + Portal |
| Invention policy | Forbidden |
| Implementation in Sprint A | Forbidden |

---

# 15. Ready for Sprint B

Sprint B may implement models and Public API contracts **only after** this architecture is accepted.

Sprint A stops here.

---

END
