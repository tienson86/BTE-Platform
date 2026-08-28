# 04 — Matching Pipeline

| Field | Value |
|-------|--------|
| Document | CK-01A Matching Pipeline |
| Version | 1.0.0 |
| Status | Canonical for CK-01A |

---

## 1. Official order

```
Published truth
  Integrated Narrative
  Identity
  Canonical Analysis Result
        ↓
Signal projection (copy only)
        ↓
Condition match
        ↓
Scope filter
        ↓
Consulting Knowledge Pack
```

Stages are fixed. Later stages may not invent signals for earlier stages.

---

## 2. Stage rules

### Published truth

Input boundary. Already computed.

Knowledge may read. Knowledge may not call the engine.

### Signal projection

Copy published fields into a flat match-signal map.

If a field is missing, it is absent. Do not infer it from a sibling engine.

### Condition match

A unit matches when every required condition key is present and satisfies equality or membership.

No arithmetic. No ranking formula. No LLM.

### Scope filter

Drop units whose `applicable_scope` excludes the published audience (for example domain mismatch). Do not rewrite the unit.

### Consulting Knowledge Pack

Assemble matched units in catalog order.

Same published signals + same catalog → same pack.

---

## 3. Fail-closed

No catalog or no match → insufficient pack.

Never a silent empty string that looks like a finished consulting reading.

---

END
