# Page State Machine

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-2

---

## 1. States

| State | Meaning |
|-------|---------|
| `loading` | Adapter not finished |
| `ready` | Hero + Summary + enough to consult; optional sections may hide |
| `partial_ready` | P1 present; some P2/P3/P4 missing |
| `error` | Cannot present a consultation |
| `empty` | Success-like bind with no presentation identity/content |
| `offline` | Reserved |
| `printing` | Reserved overlay on ready/partial |
| `exporting` | Reserved overlay on ready/partial |

---

## 2. Derivation (adapter, no business logic)

```
IF adapter not complete → loading

IF result null OR (success=false AND hero incomplete) → error
IF hero required fields missing → error
IF summary.bullets empty → error

IF hero+summary ok AND recommendations empty AND all domains unavailable
   AND no charts/knowledge/appendix → empty OR partial_ready
   (prefer empty if presentation envelope absent entirely)

IF hero+summary ok AND any optional slice missing → partial_ready

IF hero+summary ok AND recs present (or domains available) → ready

IF offline signal (reserved) → offline
IF print mode → printing
IF export mode → exporting
```

---

## 3. Transitions

```
loading → ready | partial_ready | error | empty | offline

ready ↔ printing
ready ↔ exporting
partial_ready ↔ printing
partial_ready ↔ exporting

error → loading          (retry)
empty → loading          (retry)
offline → loading        (retry)

printing → ready | partial_ready
exporting → ready | partial_ready
```

No `error → ready` without a new Receive Contract.

---

## 4. UI consequences

| State | Hero | Rec CTA | Optional sections |
|-------|------|---------|-------------------|
| loading | hidden/skeleton | disabled | hidden |
| ready | visible | per enabled flags | per visibility rules |
| partial_ready | visible | per flags | empty cards / hidden |
| error | no fake hero | hidden | hidden |
| empty | no fake hero | hidden | hidden |
| offline | none | hidden | hidden |
| printing/exporting | keep content | disabled | keep |

---

## 5. Stop line

Page state is derived from contract presence, not from scores.

END
