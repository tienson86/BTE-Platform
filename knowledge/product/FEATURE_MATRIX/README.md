# Feature Matrix V1.0 — Customer Question Architecture

| Field | Value |
|-------|-------|
| Document set | FEATURE_MATRIX |
| Version | 1.0.0 |
| Status | **COMPLETE** |
| Layer | Product — Customer Feature Architecture |
| Date | 2026-08-12 |

---

## Purpose

Define how **customer questions** map to **domains**, **interpretation**, and **commercial output**.

This is **not**:

- an Engine task
- a Knowledge authoring task
- a Rule Database task
- a Production code change

This **is** the customer-facing feature architecture for BTE Platform.

---

## Dependency chain

```
Customer Questions
      ↓
Required Domains
      ↓
Interpretation
      ↓
Commercial Output
```

Product Manifesto wins conflicts.

---

## Documents

| File | Content |
|------|---------|
| CUSTOMER_QUESTIONS.md | Top 50 questions ranked by business value |
| DOMAIN_MAPPING.md | Question → domain Required / Optional / Unavailable |
| FEATURE_MATRIX.md | Full matrix (questions × domains × priority × output) |
| PRIORITY_MATRIX.md | P0 / P1 / P2 classification |
| COMMERCIAL_FEATURES.md | Sellable feature packages |
| MVP_SCOPE.md | Minimum viable commercial consulting product |
| FEATURE_ROADMAP.md | Production Wave order by customer value |
| CHANGELOG.md | Version history |

---

## Design principles

1. **Consultant, not calculator** — features answer life questions, not expose scores.
2. **Honesty over completeness** — Unavailable domains stay Unavailable; no invented claims.
3. **Value before technical order** — Wave order follows customer willingness-to-pay, not engine dependency alone.
4. **One question → clear deliverable** — each feature maps to a commercial section or package.
