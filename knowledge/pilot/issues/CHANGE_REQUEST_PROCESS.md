# Change Request Process

Version: 1.0.0  
Sprint: Beta-5

Pilot default: **no** engine, pipeline, Knowledge package, API, UI, or deployment change.

## When a CR is filed

A freeze-touching fix seems required (e.g. true wrong-person header from a product bug in application layer — still not an engine rewrite).

## Steps

1. Link feedback ID(s).  
2. Describe user harm and alternatives.  
3. Name the layer that would change.  
4. Product Owner + Engineering + Release Manager review.  
5. If AF-1 / engine / Knowledge package / UI redesign: **reject for v1.0 pilot**, move to `releases/ROADMAP_INPUT.md`.  
6. If a tiny freeze-safe application bugfix is ever approved later, it is **out of this sprint’s implementation** and needs its own change window — not silent.

## Record

```
CR-ID:
Source PLT-IDs:
Layer:
Decision: reject / defer / approve-later
Rationale:
```

---

END
