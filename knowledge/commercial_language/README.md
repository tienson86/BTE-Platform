# Commercial Language Layer V1.2

| Field | Value |
|-------|-------|
| Package | Consulting Writer |
| Version | 1.2.0 |
| Status | AUTHORITATIVE (language layer) |
| Scope | Platform-wide commercial consulting prose |
| Not this layer | Engines · Knowledge packs · Cross-domain reasoning · Claim plans |

---

## Purpose

Transform **validated claim plans** into **commercial consulting paragraphs**.

```
ExecutiveClaimPlan
IdentityClaimPlan
CareerClaimPlan
(+ future claim plans)
        ↓
Commercial Language Layer V1.2
        ↓
Consulting paragraphs (Customer Mode)
```

This layer **does not**:

- change facts
- invent BaZi doctrine
- re-run reasoning
- invent claim values
- invent job titles, income, timing, or medical diagnoses

---

## Five layers

| Layer | Name | Job |
|------:|------|-----|
| 1 | Plain Language | Remove jargon; keep meaning |
| 2 | Consulting Style | Consultant voice, not calculator dump |
| 3 | Recognition Language | “This is me” — felt recognition |
| 4 | Action Language | What to do / what to avoid |
| 5 | Memorable Closing | One line that sticks |

Every paragraph must answer:

1. **So what?**
2. **Why should I care?**
3. **What should I do?**

---

## Document index

| Doc | Role |
|-----|------|
| [COMMERCIAL_LANGUAGE_ARCHITECTURE.md](COMMERCIAL_LANGUAGE_ARCHITECTURE.md) | Boundaries, flow, owners |
| [CONSULTING_STYLE.md](CONSULTING_STYLE.md) | Layer 2 — consulting voice |
| [PLAIN_LANGUAGE.md](PLAIN_LANGUAGE.md) | Layer 1 — plain language |
| [PARAGRAPH_PATTERNS.md](PARAGRAPH_PATTERNS.md) | Paragraph shapes from claim slots |
| [TRANSITION_PATTERNS.md](TRANSITION_PATTERNS.md) | Bridges between sections |
| [MEMORY_LINES.md](MEMORY_LINES.md) | Layer 5 — memorable closings |
| [ACTION_LANGUAGE.md](ACTION_LANGUAGE.md) | Layer 4 — action / avoid |
| [CUSTOMER_TONE.md](CUSTOMER_TONE.md) | Tone spectrum |
| [STYLE_GUIDE.md](STYLE_GUIDE.md) | Do / don’t checklist |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

---

## Upstream / downstream

| Upstream (read-only) | Downstream (writes prose) |
|----------------------|---------------------------|
| CDR `ExecutiveClaimPlan` | Identity Report body |
| Feature claim plans | Career Report body |
| Domain conclusions (as evidence only) | Executive Consulting body |
| Brand Language / Experience Principles | Future customer features |

Composers **own wording**. Reasoner **owns classification**. This package **owns the writing standard** composers must follow.
