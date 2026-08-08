# 00_NARRATIVE_INDEX.md

Version: 1.1

Status: Sprint A FROZEN · Sprint B Grammar DRAFT

Pack: 05 (Narrative Engine)

Engine: Narrative Engine

---

# 1. Purpose

This index is the entry point for PACK_05 Narrative Engine architecture and grammar.

The Narrative Engine reorganizes **validated Interpretation** into a coherent **commercial narrative**.

It does not score.

It does not infer new facts.

It does not render reports or UI.

| Sprint | Scope | Status |
|--------|-------|--------|
| A | Architecture | **FROZEN** |
| B | Narrative grammar (components + flow) | **This sprint — documentation only** |

No implementation.

No templates.

No natural-language generation in Sprint B.

---

# 2. Architecture Overview

```
Knowledge / Rule Database
        ↓
Score Engine
        ↓
AnalysisResult
        ↓
Interpretation Engine
        ↓
InterpretationResult (validated)
        ↓
┌──────────────────────────────────────────────────┐
│              Narrative Engine                     │
│                                                   │
│  Evidence → Composer → Section Builder            │
│       → Story Builder → NarrativeResult           │
│                                                   │
│  Grammar flow:                                    │
│  Executive Summary → Observation → Reasoning      │
│  → Impact → Recommendation → Warning → Conclusion │
└──────────────────────────────────────────────────┘
        ↓
Report Engine / Portal Adapter
```

---

# 3. Dependency Graph

## Upstream

| Dependency | Rule |
|------------|------|
| AnalysisResult | Fact authority / evidence |
| InterpretationResult | Validated meaning Narrative reorganizes |
| Knowledge assets | Future content sprints only |

## Downstream

| Consumer | Rule |
|----------|------|
| Report Engine | Prefers NarrativeResult |
| Portal Adapter | Maps grammar components to ViewModels |
| API | `narrative` view |

## Forbidden

```
Narrative  ✗→  Score / rule matching / inference of new conclusions
Narrative  ✗→  Portal UI / Design System / Foundation edits
```

---

# 4. Document Navigation

## Sprint A — Architecture (FROZEN)

| File | Title |
|------|-------|
| `00_NARRATIVE_INDEX.md` | Index |
| `01_NARRATIVE_ARCHITECTURE.md` | Architecture |
| `02_NARRATIVE_PIPELINE.md` | Pipeline |
| `03_NARRATIVE_MODELS.md` | Models |
| `04_NARRATIVE_PUBLIC_API.md` | Public API |

## Sprint B — Grammar

| File | Title |
|------|-------|
| `05_EXECUTIVE_SUMMARY_SPEC.md` | Executive Summary |
| `06_OBSERVATION_COMPONENT.md` | Observation |
| `07_REASONING_COMPONENT.md` | Reasoning |
| `08_IMPACT_COMPONENT.md` | Impact |
| `09_RECOMMENDATION_COMPONENT.md` | Recommendation |
| `10_WARNING_COMPONENT.md` | Warning |
| `11_CONCLUSION_COMPONENT.md` | Conclusion |
| `12_NARRATIVE_FLOW_SPEC.md` | Official flow |

---

# 5. Reading Order

### Architecture (Sprint A)

1. Index → 01 Architecture → 02 Pipeline → 03 Models → 04 Public API

### Grammar (Sprint B)

1. `12_NARRATIVE_FLOW_SPEC.md` (order and rules)
2. `05` Executive Summary
3. `06` → `11` components in flow order

---

# 6. Pack Naming Clarification

| Name | Meaning |
|------|---------|
| `pack_05_narrative_engine` | Narrative Engine (this pack) |
| `pack_05_report_engine` | Report Engine (layout / render / export) |
| Design System PACK_05 | Accessibility — unrelated |

---

# 7. Sprint B Invariants

- Narrative is NOT an inference / rule / scoring engine
- Narrative only reorganizes validated Interpretation
- Narrative never changes analytical meaning
- Insufficient support → explicit **Insufficient Evidence** state
- No prose, templates, paragraphs, or examples in Sprint B docs

---

# 8. Success Criteria

| Sprint | Done when |
|--------|-----------|
| A | Architecture clear — **frozen** |
| B | Every component has contract, dependencies, quality rules, output spec + flow defined |

**Stop after Sprint B.**

---

END
