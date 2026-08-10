# Pilot Strategy

Version: 1.0.0  
Sprint: Beta-5

## Approach

**Progressive exposure.** Each phase increases user realism and volume only after exit criteria pass.

```
Internal (5–10)
    → Expert consultants (10–20)
        → Real customers (20–50)
            → Controlled commercial usage
```

## Why this order

Internal finds blocking defects cheaply. Experts test professional credibility. Customers test first-use understanding. Commercial pilot tests support + ops under light production load.

## In scope for learning

Usability of analysis → report → Knowledge → save/share/history. Feedback quality. Support load. Completion and return behavior (observed or self-reported).

## Out of scope

Engine rule debates as a pilot “feature.” Payment checkout. Auth product build. UI redesign. Price experiments in git.

## Risk control

Small cohorts, consent, confidentiality, P0/P1 stop-ship gates, rollback via existing deployment plan (unchanged).

---

END
