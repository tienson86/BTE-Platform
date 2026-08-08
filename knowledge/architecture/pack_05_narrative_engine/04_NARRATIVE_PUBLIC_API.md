# 04_NARRATIVE_PUBLIC_API.md

Version: 1.0

Status: DRAFT — Sprint A Architecture

Pack: 05 (Narrative Engine)

Engine: Narrative Engine

---

# 1. Purpose

This document defines the official Public API of the Narrative Engine.

Consumers call the public facade only.

Consumers never call Evidence Extractor, Composer, Section Builder, or Story Builder directly.

---

# 2. API Philosophy

| Principle | Meaning |
|-----------|---------|
| Single facade | One primary engine/service entry |
| Result objects | Return NarrativeResult (or typed error) — not tuples / ad-hoc dicts as the contract |
| Validate in / validate out | Input and output validation gates |
| Stateless | No process-global narrative cache required |
| Backward compatible | Additive evolution; wrappers if signatures must change |
| No UI types | No ViewModels in the Public API |

---

# 3. Public Surface

Canonical public types:

- `NarrativeEngine` (facade)  
- `NarrativeService` (optional thin orchestration alias — same contract)  
- `NarrativeResult`  
- `NarrativeSummary`  
- `NarrativeSection`  
- `NarrativeParagraph`  
- `NarrativeRecommendation`  
- Narrative error types  

Internal (not public):

- Evidence Extractor  
- Narrative Composer  
- Section Builder  
- Story Builder  
- NarrativeContext  

---

# 4. Official Entry Points

## 4.1 Primary method

```
NarrativeEngine.compose(analysis: AnalysisResult, options?: NarrativeOptions)
  → NarrativeResult
```

Logical signature (language-agnostic):

| Name | `compose` |
|------|-----------|
| Input | `AnalysisResult` (required) |
| Options | `NarrativeOptions` (optional) |
| Output | `NarrativeResult` |
| Errors | Narrative engine errors (see §7) |

## 4.2 Extended method (optional Interpretation evidence)

```
NarrativeEngine.compose_from_sources(
  analysis: AnalysisResult,
  interpretation?: InterpretationResult,
  options?: NarrativeOptions
) → NarrativeResult
```

Rules:

- `analysis` remains the fact authority.  
- `interpretation` is optional evidence only.  
- Omitting interpretation must still allow a valid NarrativeResult when AnalysisResult is sufficient.  

## 4.3 Convenience alias (compatibility)

```
NarrativeEngine.run(...)
```

May alias `compose` / `compose_from_sources` for orchestrator symmetry with other engines.

Must not introduce a second divergent behavior path.

---

# 5. Input Contract

## 5.1 AnalysisResult (required)

| Requirement | Rule |
|-------------|------|
| Canonical | Produced by Score / analysis pipeline |
| Immutable | Narrative must not mutate it |
| Validated | Invalid input → error before composition |

Narrative does not accept raw UI JSON as the architectural input.

API/orchestrator adapters may rebuild AnalysisResult before calling Narrative.

## 5.2 InterpretationResult (optional)

| Requirement | Rule |
|-------------|------|
| Optional | Never required for compose |
| Read-only | Narrative must not mutate it |
| Filtered | Technical rule prose must not pass into customer fields |

## 5.3 NarrativeOptions (optional)

Logical fields:

| Field | Description |
|-------|-------------|
| `locale` | Target locale |
| `profile` | Audience depth profile |
| `verbosity` | short / standard / detailed |
| `include_optional_sections` | Whether optional theme sections are attempted |
| `run_id` | Correlation id |

Options must not inject new analytical facts.

---

# 6. Output Contract

## 6.1 Success

Output: `NarrativeResult`

Must include:

- `metadata`  
- `summary` with five commercial answers (value or insufficient)  
- `sections` covering required intents  
- `confidence`  
- `source_fingerprint`  

## 6.2 Insufficient data (still success)

When AnalysisResult is valid but thin:

- Return `NarrativeResult` with `status = partial_insufficient`  
- Fill missing commercial slots with insufficient-data markers  
- Do **not** invent content  

This is not an exception path.

## 6.3 Failure

When composition cannot produce an integrity-valid NarrativeResult:

- Raise / return Narrative engine error  
- Do not return a corrupt partial aggregate  

---

# 7. Error Handling

## 7.1 Error categories

| Error type | When |
|------------|------|
| `NarrativeValidationError` | Input AnalysisResult invalid / missing required analytical core |
| `NarrativeCompositionError` | Composer cannot produce a valid plan under integrity rules |
| `NarrativeBuildError` | Section/Story builders fail integrity validation |
| `NarrativeEngineError` | Generic engine failure wrapper |

Exact class naming may align with platform exception style in Sprint B.

## 7.2 Error principles

- Prefer specific errors over generic catch-alls.  
- Never swallow errors into empty successful narratives.  
- Never return `null` as a silent success.  
- Log with run_id when provided.  

## 7.3 Mapping to API layer

Orchestrator / API may map Narrative errors to HTTP-safe messages without exposing internals.

---

# 8. Extension Points

Architecture allows extension **without** changing Score or Interpretation public APIs:

| Extension | Mechanism |
|-----------|-----------|
| New optional section intents | CompositionPlan + Section Builder strategies |
| New evidence kinds | Evidence Extractor mapping from existing AnalysisResult fields |
| New locales | Narrative assets / locale options |
| Audience profiles | NarrativeOptions.profile |
| Commercial filters | Pluggable suitability policy for Interpretation text |

Forbidden extension patterns:

- Embedding Score calculators inside Narrative  
- Portal-specific branching inside NarrativeEngine  
- Hard-coded consultant conclusions without evidence  

---

# 9. Orchestrator Integration (Contract)

Recommended pipeline position:

```
... → Score → Interpretation → Narrative → Report → Delivery
```

Logical orchestrator call:

```
narrative_result = NarrativeEngine.compose_from_sources(
  analysis_result,
  interpretation_result,
  options
)
payload.narrative = serialize(narrative_result)
```

Report Engine preferred input becomes NarrativeResult.

Legacy Interpretation → Report path remains until compatibility window ends.

---

# 10. Portal Integration (Contract)

Portal Adapter:

```
NarrativeResult → Result / Executive ViewModels
```

Rules:

- Prefer NarrativeSummary for Executive Summary answers.  
- Prefer NarrativeSection / NarrativeRecommendation for content cards.  
- If Narrative absent (legacy payloads), keep existing fallback behavior.  
- If insufficient flags set, show platform unavailable conclusion — do not invent.  

Narrative Public API does not return ViewModels.

---

# 11. Report Integration (Contract)

Report Engine:

```
NarrativeResult → Report layout / render / export → ReportResult
```

Legacy:

```
InterpretationResult → ReportResult
```

Compatibility wrapper may accept either input and normalize to report presentation structures.

Narrative Public API does not return ReportResult.

---

# 12. Backward Compatibility

| Rule | Requirement |
|------|-------------|
| No breaking removal | Once Sprint B freezes method names, do not remove them |
| Additive fields | New NarrativeResult fields must be optional or versioned |
| Wrappers | If signatures must change, keep old method as wrapper |
| Dual publish | Orchestrator may publish both `interpretation` and `narrative` during transition |
| Portal fallback | Portal must tolerate missing `narrative` during rollout |

Interpretation Engine Public API remains unchanged by this pack.

Score Engine Public API remains unchanged by this pack.

---

# 13. Versioning

NarrativeResult metadata should carry:

| Field | Purpose |
|-------|---------|
| `engine_version` | Narrative Engine version |
| `schema_version` | NarrativeResult schema version |
| `asset_version` | Narrative knowledge/asset pack version (when assets exist) |

Version bumps:

- Additive compatible → minor  
- Breaking field semantics → major (requires wrapper period)  

---

# 14. Non-Goals of the Public API

The Public API does **not** expose:

- Template editing  
- Rule matching  
- Score recalculation  
- UI theming  
- PDF export  

Those remain owned by Knowledge tooling, Score, Design System / Portal, and Report Engine respectively.

---

# 15. Sprint A API Completeness Checklist

| Item | Status |
|------|--------|
| Primary compose method defined | Yes |
| Optional interpretation evidence method defined | Yes |
| Input / output contracts defined | Yes |
| Error categories defined | Yes |
| Extension points defined | Yes |
| Backward compatibility rules defined | Yes |
| Implementation code | **No — forbidden in Sprint A** |

---

# 16. Ready for Sprint B

Sprint B may implement Public API shells and model types matching this specification.

Sprint A stops after this document set.

---

END
