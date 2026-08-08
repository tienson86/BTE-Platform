# 03_NARRATIVE_MODELS.md

Version: 1.0

Status: DRAFT — Sprint A Architecture

Pack: 05 (Narrative Engine)

Engine: Narrative Engine

---

# 1. Purpose

This document defines the canonical models of the Narrative Engine.

Models are architectural contracts.

This document does not prescribe programming language syntax, ORMs, or serializers.

---

# 2. Design Principles

| Principle | Meaning |
|-----------|---------|
| Immutable | Models are not mutated after construction |
| Strongly typed | Prefer typed fields over free-form bags |
| Traceable | Customer text links to evidence |
| Versioned | NarrativeResult carries schema / engine version |
| Locale-aware | Locale is first-class on context / result |
| No UI types | No ViewModel, CSS, or Design System types |
| No Score mutation | Models never rewrite AnalysisResult |

---

# 3. Model Set

Official models:

1. `NarrativeContext`  
2. `NarrativeSection`  
3. `NarrativeParagraph`  
4. `NarrativeRecommendation`  
5. `NarrativeSummary`  
6. `NarrativeResult`  

Supporting logical models (pipeline, not public aggregate roots):

- `EvidenceUnit` / `EvidenceSet`  
- `CompositionPlan`  

---

# 4. Relationship Diagram

```
NarrativeContext
    │ contains references to
    ├── AnalysisResult (read-only)
    ├── EvidenceSet
    ├── CompositionPlan
    └── options (locale, profile)
            │
            ▼
NarrativeResult  ◄──────────────────────────────┐
    │                                           │
    ├── NarrativeSummary                        │
    │     ├── identity_answer                   │
    │     ├── strengths[]                       │
    │     ├── weaknesses[]                      │
    │     ├── priority_recommendation           │
    │     └── next_action                       │
    │                                           │
    ├── NarrativeSection[] ─────────────────────┤
    │     ├── NarrativeParagraph[]              │
    │     │     └── evidence_refs[]             │
    │     └── NarrativeRecommendation[]  (opt)  │
    │                                           │
    └── metadata / confidence / version         │
```

**Aggregate Root:** `NarrativeResult`

Downstream engines consume `NarrativeResult` only (not Context, not EvidenceSet).

---

# 5. NarrativeContext

## Purpose

Runtime context for one Narrative Engine execution.

## Ownership

Internal to Narrative Engine.

Not a public output.

## Field descriptions

| Field | Description |
|-------|-------------|
| `analysis` | Read-only AnalysisResult reference |
| `interpretation` | Optional InterpretationResult reference |
| `evidence` | EvidenceSet extracted for this run |
| `plan` | CompositionPlan produced by Composer |
| `locale` | Target language / locale code |
| `profile` | Optional audience profile (e.g., customer vs consultant depth) |
| `options` | Non-analytical flags (verbosity, include optional sections) |
| `run_id` | Correlation id for tracing |
| `started_at` | Run timestamp |

## Lifecycle

```
created at run start
  → filled by Evidence Extractor
  → plan attached by Composer
  → read by Section / Story builders
  → discarded after NarrativeResult accepted
```

NarrativeContext must not escape as API payload.

---

# 6. EvidenceUnit / EvidenceSet (Supporting)

## Purpose

Typed facts Narrative may narrate.

## EvidenceUnit fields

| Field | Description |
|-------|-------------|
| `id` | Stable id within the run |
| `kind` | identity / strength / weakness / opportunity / risk / action / grade / other |
| `label` | Short factual label |
| `value` | Factual value or structured payload |
| `source_path` | Path into AnalysisResult (and optional Interpretation section id) |
| `confidence` | 0–1 or enum aligned with platform |
| `commercial_ok` | Whether associated text is customer-safe |
| `raw_text` | Optional source text (may be non-commercial) |

## EvidenceSet

Ordered / indexed collection of EvidenceUnit for one run.

EvidenceSet is not part of NarrativeResult public aggregate (trace ids may be copied into paragraphs).

---

# 7. NarrativeParagraph

## Purpose

Smallest customer-facing narrative unit.

## Field descriptions

| Field | Description |
|-------|-------------|
| `id` | Stable paragraph id |
| `role` | observation / explanation / impact / suggestion / summary / other |
| `text` | Commercial natural language |
| `evidence_refs` | List of EvidenceUnit ids supporting this text |
| `confidence` | Paragraph-level confidence |
| `insufficient_data` | True when text is the platform insufficient-data outcome |

## Rules

- `text` must not be technical rule-activation prose.  
- If `insufficient_data` is true, `text` uses the platform unavailable conclusion string.  
- Paragraphs do not contain layout markup responsibilities (Report owns rendering).  

---

# 8. NarrativeRecommendation

## Purpose

Action-oriented narrative unit for priority / next steps.

## Field descriptions

| Field | Description |
|-------|-------------|
| `id` | Stable recommendation id |
| `priority` | critical / high / medium / low (semantic, not UI badge styling) |
| `action` | What the person should do |
| `reason` | Why (evidence-backed) |
| `benefit` | Expected benefit (evidence-backed or omitted) |
| `evidence_refs` | Supporting evidence ids |
| `insufficient_data` | True when action cannot be responsibly stated |

## Rules

- Recommendations must not invent actions without evidence (useful god, score recommendation, or approved narrative asset bound to evidence).  
- Priority is narrative semantics; Portal maps to presentation labels.  

---

# 9. NarrativeSection

## Purpose

Coherent block answering one narrative intent.

## Field descriptions

| Field | Description |
|-------|-------------|
| `id` | Stable section id |
| `intent` | identity / strengths / weaknesses / priority / next_action / overview / closing / optional theme |
| `title` | Customer-facing section title |
| `paragraphs` | Ordered NarrativeParagraph list |
| `recommendations` | Optional NarrativeRecommendation list |
| `evidence_refs` | Section-level evidence union |
| `confidence` | Aggregate section confidence |
| `insufficient_data` | True when section cannot conclude |

## Required intents (commercial minimum)

| Intent | Answers |
|--------|---------|
| `identity` | Who is this person? |
| `strengths` | Main strengths |
| `weaknesses` | Main weaknesses |
| `priority` | Priority recommendation |
| `next_action` | Next action |

Additional intents are extension points for later sprints.

---

# 10. NarrativeSummary

## Purpose

Executive-level answers for Portal Executive Summary and Report front matter.

## Field descriptions

| Field | Description |
|-------|-------------|
| `identity` | Short answer — who is this person |
| `strengths` | Short list of main strengths |
| `weaknesses` | Short list of main weaknesses |
| `priority_recommendation` | Single priority recommendation text |
| `next_action` | Single next action text |
| `overall_confidence` | Summary confidence |
| `insufficient_flags` | Which of the five answers are insufficient |

## Rules

- Summary must align with section content (no contradictory claims).  
- Summary is derived by Story Builder from sections + evidence, not authored independently of sections.  

---

# 11. NarrativeResult

## Purpose

Aggregate Root — canonical commercial narrative output.

## Field descriptions

| Field | Description |
|-------|-------------|
| `metadata` | engine version, schema version, locale, run_id, timestamps |
| `summary` | NarrativeSummary |
| `sections` | Ordered NarrativeSection list |
| `recommendations` | Flattened or top-level recommendation list (optional convenience) |
| `confidence` | Overall narrative confidence |
| `source_fingerprint` | Provenance: AnalysisResult / Interpretation versions |
| `status` | complete / partial_insufficient / failed (failed not returned as success) |

## Invariants

1. Immutable after acceptance.  
2. `summary` five commercial answers always present as fields (value or insufficient).  
3. Every non-insufficient paragraph has ≥ 1 evidence_ref **or** an explicit platform policy exception documented in Sprint B.  
4. No Portal / Report layout fields.  

---

# 12. CompositionPlan (Supporting)

## Purpose

Composer output describing section order and bindings.

## Logical fields

| Field | Description |
|-------|-------------|
| `section_intents` | Ordered intents to build |
| `evidence_bindings` | Intent → evidence ids |
| `options_applied` | Verbosity / optional themes |

Not part of public NarrativeResult.

---

# 13. Lifecycle

```
1. NarrativeContext created
2. EvidenceSet populated
3. CompositionPlan attached
4. NarrativeSection(s) built
5. NarrativeSummary built
6. NarrativeResult assembled
7. Validator accepts → NarrativeResult published
8. NarrativeContext discarded
```

Failed validation → no published NarrativeResult (Public API error).

---

# 14. Serialization Expectations (Architecture)

Downstream may serialize NarrativeResult to JSON for API / Portal.

Requirements:

- Stable field names once Sprint B freezes the contract  
- Backward-compatible additive evolution  
- No requirement to expose EvidenceSet wholesale in Portal payloads (refs sufficient)

Exact DTO shapes belong to Sprint B / API contract work — not Sprint A code.

---

# 15. Model Diagram (Compact)

```
                    NarrativeResult
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
   NarrativeSummary  NarrativeSection[]  metadata
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
     NarrativeParagraph[]   NarrativeRecommendation[]
              │                       │
              └───────────┬───────────┘
                          ▼
                   evidence_refs[]
                          │
                          ▼
                    EvidenceUnit (internal)
                          │
                          ▼
                    AnalysisResult
```

---

# 16. Ready for Sprint B

Sprint B may create typed model definitions matching this contract.

Sprint A defines models only.

---

END
