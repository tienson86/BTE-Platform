# Knowledge Selection & Sentence Composition Engine

Version: 1.0.0  
Engine ID: `knowledge_selection_engine`  
Sprint: IE-2  
Status: Canonical selection layer  
Foundation: v1.0.0 (frozen)

This engine transforms Canonical Results into structured interpretation candidates.

It does **not** generate free-form text, compose chapters, or render reports.

---

## Selection pipeline

```
CanonicalAnalysisResult (AX-2 2.0.0)
CanonicalDecisionResult (AX-3 1.0.0)
CanonicalLuckResult (AX-4 1.0.0)
InterpretationContext (IE-1 1.0.0)
        ↓
Composition Context (append-only)
        ↓
Knowledge Selector
        ↓
Evidence Selector + Reasoning Selector + Template Selector
        ↓
Placeholder Binder
        ↓
Sentence Candidate Builder
        ↓
CompositionResult
```

Order is registry-defined and deterministic:

`knowledge → evidence → reasoning → template → placeholder → sentence_candidate`

---

## Selection hierarchy

1. **Released knowledge only** — draft / unreleased catalog entries are ignored.
2. **Presence, not inference** — a knowledge item is selected only when its published field path resolves.
3. **Evidence** copies declared bundles, confidence tokens, references, and boundary flags.
4. **Reasoning** copies chain / graph / trace identifiers. No edits.
5. **Templates** are identifiers only. No rendering.
6. **Placeholders** bind published contract values only.
7. **Candidates** are structured records, not paragraphs.

---

## Placeholder model

| Field | Meaning |
|---|---|
| `placeholder_id` | Deterministic binding identity |
| `binding_path` | `analysis.*` / `decision.*` / `luck.*` / `interpretation.*` |
| `value` | Copied published field |
| `status` | `bound` or `unbound` |

Unpublished roots fail closed. No computed fields outside published contracts.

---

## Candidate model

Each `SentenceCandidate` contains:

- `sentence_id`
- `template_id`
- `placeholder_values`
- `evidence_ids`
- `reasoning_ids`
- `confidence`
- `references`

`sentence_id` is an identifier (`SC-…`), not a sentence string.

---

## Future IE-3 composition

IE-3 will consume `CompositionResult` candidates to assemble chapters and paragraphs.

IE-2 stops before chapter composition.

---

## Future AI rewrite hook

`ai_rewrite.enabled = false`

The hook is registered as `future_ie3_ai_rewrite` and remains disabled.

IE-2 must not rewrite sentences or call AI.

---

## Compliance

- Foundation v1.0.0 frozen
- AX-2 / AX-3 / AX-4 / IE-1 unchanged
- Knowledge Packages unread and unmodified
- Ready for IE-3 Composition Engine
