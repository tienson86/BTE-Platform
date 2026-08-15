# Knowledge Architecture — Interpretation Layer (K1)

## Frozen flow

```text
Engine Truth
    ↓
Canonical Facts
    ↓
Decision Explanation
    ↓
Concept Layer          ← K1.5
    ↓
BaZi Knowledge System  ← K1
    ↓
Narrative
    ↓
Report
```

## Ownership

| Layer | Owns |
|---|---|
| Analytical engines | Truth |
| Domain interpreters | Explanation structure |
| Decision Explanation Framework | Reasoning path |
| **Concept Layer** | Reusable semantic meaning |
| **BaZi Knowledge System** | Domain-specific expert entries |
| Narrative | Customer prose |
| UI | Rendering |

## Domain independence

Each knowledge domain is independent:

- UsefulGod knowledge MUST NOT import TenGods knowledge
- Strength knowledge MUST NOT depend on Luck knowledge
- Cross-domain links use explicit `related_entities` references only

## Registry contract

Interpreters call:

```text
get(domain, key) → KnowledgeEntity | None
```

The interpreter does not know file paths, JSON vs YAML, or future database backends.

## Semantic interpretation classes (K3 / R1)

The reasoning layer contains exactly three classes. Do not merge them.
No additional reasoning class without explicit architectural review.

```text
Decision Reasoning

Useful God
```

```text
State Reasoning

Strength
```

```text
Relationship Reasoning

Pattern (K4)
```

### Decision pipeline

```text
Engine Truth → Canonical Facts → Decision Explanation → Knowledge → Narrative
```

Winner and alternatives. Not used for state or relationship.

### State pipeline

```text
Engine Truth → Canonical Facts → Assessment → Knowledge → Narrative
```

Condition/state. No winner. No alternatives.

### Relationship pipeline

```text
Engine Truth → Canonical Facts → Relationship Assessment → Relationship Knowledge → Narrative
```

Interaction only. No decisions. No state evaluation.

Relationship types (semantic, not encoded rules):

```text
supports | generates | drains | controls | balances | conflicts | transforms | combines
```

Meaning belongs to Knowledge. Relationship belongs to Reasoning.

Conceptual future uses (not implemented in R1; names are documentation only):

```text
Month Command → Day Master → Pattern relationship
```

```text
Ten God → Day Master → Role interaction
```

```text
Luck cycle → Natal chart → Relationship
```
