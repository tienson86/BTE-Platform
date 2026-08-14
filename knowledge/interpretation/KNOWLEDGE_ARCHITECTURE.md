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

## Sprint K1

Framework only. One example entity proves the architecture.

Population of full stem/pattern/shensha catalogs is Sprint K2+.
