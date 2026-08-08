# 02_NARRATIVE_PIPELINE.md

Version: 1.0

Status: DRAFT — Sprint A Architecture

Pack: 05 (Narrative Engine)

Engine: Narrative Engine

---

# 1. Purpose

This document defines the official Narrative Engine pipeline.

It describes every stage.

It does not describe implementation code, libraries, or file layout decisions.

---

# 2. Official Pipeline

```
AnalysisResult
    ↓
Evidence
    ↓
Narrative Composer
    ↓
Narrative Section Builder
    ↓
Narrative Story Builder
    ↓
NarrativeResult
```

Optional parallel input (not a substitute for AnalysisResult):

```
InterpretationResult  →  Evidence (as candidate evidence units)
```

---

# 3. Pipeline Philosophy

| Principle | Meaning |
|-----------|---------|
| Deterministic | Same inputs + same narrative assets → same NarrativeResult |
| Traceable | Every paragraph links to evidence |
| Ordered | Stages run in fixed order; no skipping Composer |
| Fail-closed | Invalid AnalysisResult aborts the run |
| No invention | Missing evidence → insufficient-data slots, not fabricated story |
| Stateless | No cross-request memory inside the engine |

---

# 4. Stage 0 — Preconditions

Before the pipeline starts:

| Check | Requirement |
|-------|-------------|
| AnalysisResult present | Required |
| AnalysisResult validated | Required by Score / orchestrator contract |
| Locale / profile | Optional NarrativeContext options |
| InterpretationResult | Optional |

If AnalysisResult is missing or invalid → pipeline does not start → Public API error.

---

# 5. Stage 1 — AnalysisResult (Input Boundary)

## Role

Authoritative analytical facts enter the Narrative Engine.

## What this stage provides

- Day master / chart identity signals  
- Strength / pattern / useful god / five elements / ten gods  
- Scores, grades, confidence  
- Existing short recommendations from Score (facts, not final story)  

## What this stage is not

- Not narrative wording  
- Not report layout  
- Not portal ViewModels  

## Exit artifact

Immutable reference to AnalysisResult inside NarrativeContext.

---

# 6. Stage 2 — Evidence

## Role

Extract typed **Evidence Units** from AnalysisResult (and optionally from InterpretationResult).

## Responsibilities

✓ Normalize analytical facts into evidence units  

✓ Attach source pointers (module, field, confidence)  

✓ Classify evidence by narrative intent (identity, strength, risk, action, …)  

✓ Mark commercial suitability of optional Interpretation text  

✓ Drop or quarantine technical rule prose from customer path  

## Evidence Unit (logical)

| Field group | Purpose |
|-------------|---------|
| `id` | Stable evidence identifier for tracing |
| `kind` | identity / strength / weakness / opportunity / risk / action / grade / … |
| `payload` | Fact payload (labels, values, scores) |
| `source` | AnalysisResult path and/or Interpretation section id |
| `confidence` | Inherited or derived confidence |
| `commercial_ok` | Whether text is suitable for customer narrative |

## Rules

- Evidence does not compose paragraphs.  
- Evidence does not decide section order (Composer does).  
- Evidence must not invent facts.  

## Exit artifact

`EvidenceSet` held by NarrativeContext.

```
AnalysisResult (+ optional InterpretationResult)
        ↓
   Evidence Extractor
        ↓
     EvidenceSet
```

---

# 7. Stage 3 — Narrative Composer

## Role

Decide **what story to tell** and **in what structure**, given EvidenceSet.

## Responsibilities

✓ Build the section plan (required + optional sections)  

✓ Map evidence kinds → section intents  

✓ Resolve priority among competing evidence  

✓ Decide depth / inclusion when confidence is low  

✓ Emit composition directives for Section Builder  

✓ Reserve insufficient-data markers where evidence is missing  

## Composer does not

✗ Write final customer paragraphs (Section Builder does)  

✗ Assemble the final aggregate (Story Builder does)  

✗ Call Score or mutate AnalysisResult  

## Composition policy (architecture-level)

Required commercial section intents:

1. Identity — Who is this person?  
2. Strengths — Main strengths  
3. Weaknesses — Main weaknesses  
4. Priority recommendation  
5. Next action  

Optional intents (examples for later sprints — not implementation):

- Career / relationship / health themes when evidence exists  
- Closing summary  

## Exit artifact

`CompositionPlan` inside NarrativeContext.

```
EvidenceSet
    ↓
Narrative Composer
    ↓
CompositionPlan
```

---

# 8. Stage 4 — Narrative Section Builder

## Role

For each planned section intent, build a **NarrativeSection** with paragraphs and recommendations as needed.

## Responsibilities

✓ Select evidence assigned to the section  

✓ Produce NarrativeParagraph units in commercial language  

✓ Attach evidence references to each paragraph  

✓ Produce NarrativeRecommendation when section intent requires action  

✓ Emit insufficient-data section body when evidence is inadequate  

✓ Preserve locale and tone constraints  

## Section Builder does not

✗ Change the CompositionPlan order (Composer owns plan)  

✗ Finalize NarrativeSummary / NarrativeResult root  

✗ Render markdown/HTML for Report  

## Per-section flow

```
CompositionPlan.section_intent
        ↓
  select Evidence
        ↓
  build paragraphs / recommendations
        ↓
  NarrativeSection
```

## Exit artifact

Ordered list of `NarrativeSection`.

---

# 9. Stage 5 — Narrative Story Builder

## Role

Assemble sections into a coherent **NarrativeResult**, including summary and metadata.

## Responsibilities

✓ Order sections per CompositionPlan  

✓ Build NarrativeSummary (executive-level answers)  

✓ Attach run metadata (version, locale, confidence aggregate)  

✓ Ensure required commercial questions are represented  

✓ Hand off to Validator (logical gate before return)  

## Story Builder does not

✗ Re-extract evidence  

✗ Re-score analysis  

✗ Perform Portal adaptation  

## Exit artifact

`NarrativeResult` (pre-validation).

```
NarrativeSection[]
        ↓
Narrative Story Builder
        ↓
NarrativeResult (candidate)
        ↓
Narrative Validator
        ↓
NarrativeResult (accepted)
```

---

# 10. Stage 6 — NarrativeResult (Output Boundary)

## Role

Canonical commercial narrative aggregate for downstream engines.

## Consumers

| Consumer | Use |
|----------|-----|
| Report Engine | Preferred content source for report body |
| Portal Adapter | Executive Summary, interpretation cards, recommendations |
| API | `narrative` view serialization |

## Guarantees

- Immutable after acceptance  
- Traceable to evidence  
- No technical rule-activation prose in customer-facing fields  
- Explicit insufficient-data handling where facts are missing  

---

# 11. End-to-End Stage Diagram

```
┌──────────────────┐
│ AnalysisResult   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐     optional
│ Evidence         │◄──── InterpretationResult
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Narrative        │
│ Composer         │  → CompositionPlan
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Narrative        │
│ Section Builder  │  → NarrativeSection[]
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Narrative        │
│ Story Builder    │  → NarrativeSummary + NarrativeResult
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ NarrativeResult  │
└──────────────────┘
```

---

# 12. Error Paths (Pipeline Level)

| Condition | Pipeline behavior |
|-----------|-------------------|
| Missing / invalid AnalysisResult | Abort — Public API error |
| Empty EvidenceSet | Abort or accepted result with all required slots insufficient — architecture prefers explicit insufficient NarrativeResult if context is valid but thin |
| Composer cannot plan required intents | Validator fail — error or insufficient-complete result (policy fixed in Sprint B contract) |
| Section Builder lacks assets for wording | Insufficient-data slot — do not invent |
| Validator fails integrity | Abort — do not publish partial corrupt NarrativeResult |

Exact error types are defined in `04_NARRATIVE_PUBLIC_API.md`.

---

# 13. Observability (Architecture)

Each run should be able to expose (without defining implementation):

- Stage completed markers  
- Evidence counts by kind  
- Sections produced / insufficient slots  
- Overall narrative confidence  

Logging must not print customer PII beyond existing platform policy.

---

# 14. What This Document Does Not Decide

- Concrete class names in Python/TypeScript  
- Template file formats  
- Database schema for sentence libraries  
- Portal card layout  
- Report markdown formatting rules  

Those belong to later sprints.

---

# 15. Pipeline Readiness for Sprint B

Sprint B may implement stage contracts and empty shells **only after** architecture acceptance.

Sprint A defines stages only.

---

END
