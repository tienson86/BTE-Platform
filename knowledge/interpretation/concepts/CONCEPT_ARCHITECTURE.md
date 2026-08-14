# Concept Architecture — Interpretation Layer (K1.5)

## Frozen flow

```text
Engine Truth
    ↓
Canonical Facts
    ↓
Decision Explanation
    ↓
Concept Layer          ← this layer
    ↓
Knowledge Entities
    ↓
Narrative
    ↓
Report
```

## Ownership

| Layer | Owns |
|---|---|
| Decision Explanation | Reasoning path and selected keys |
| **Concept Layer** | Reusable semantic meaning |
| Knowledge Entities | Domain-specific expert entries |
| Narrative | Customer prose combining Decision + Concept + Entity |

## Concept vs Entity

- **ConceptEntity** — reusable semantic unit (e.g. `refining_metal`)
- **KnowledgeEntity** — domain key entry (e.g. `UsefulGod/Đinh`)
- Entities reference concepts via `concept_ids[]`
- Entity JSON MUST NOT duplicate concept meaning fields

## Graph relationships

Supported types (model only — no graph algorithms in K1.5):

```text
supports | requires | opposes | extends | specializes | related_to
```

## Registry contract

```text
get(id) → ConceptEntity | None
exists(id) → bool
list(category) → tuple[ConceptEntity, ...]
validate() → ConceptValidationResult
related(id, relationship?) → tuple[ConceptEntity, ...]
```

## Sprint K1.5

Framework only. One golden example proves entity → concept mapping.
