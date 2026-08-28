# 04 — Composition Pipeline

| Field | Value |
|-------|--------|
| Document | INT-02A Composition Pipeline |
| Version | 1.0.0 |
| Status | Canonical for INT-02A |

---

## 1. Official order

```
Engine Result (read-only)
        ↓
Topic Evidence Pack
        ↓
Block Fill
        Observation
            ↓
        Reasoning
            ↓
        Impact
            ↓
        Recommendation
            ↓
        Conclusion
        ↓
Topic Narrative Unit
        ↓
(later sprints) Chart assembly / Identity keys / Report / Portal
```

Stages are fixed. Block Fill must not reorder blocks.

---

## 2. Stage rules

### Engine Result

Input boundary. Already computed.

Narrative may read. Narrative may not call the engine.

### Topic Evidence Pack

Copy published fields for one topic.

If a field is missing, list it in `missing`. Do not infer it from sibling engines.

### Block Fill

For each block in order:

1. Bind eligible sentence templates to evidence-pack slots.
2. If no eligible sentence exists, mark the block insufficient.
3. Never fill a later block with facts reserved for an earlier block.

Reasoning may only explain Observation facts already packed.

Impact may only follow from Observation + Reasoning evidence.

Recommendation may only follow from published guidance / useful-god / existing recommendation assets.

Conclusion may only restated packed facts. It may not introduce a new classification.

### Topic Narrative Unit

Assemble the five blocks.

Derive `status`:

| Condition | Status |
|-----------|--------|
| All five blocks available | `complete` |
| Some blocks insufficient | `partial` |
| Observation insufficient | `insufficient` |

A topic with no observation cannot produce a responsible recommendation.

---

## 3. Chart assembly (out of INT-02A runtime)

Later sprints may compose many Topic Narrative Units into a chart narrative.

Pack 05 remains the chart-level commercial engine.

INT-02A does not implement chart assembly and does not modify Pack 05.

---

## 4. Determinism

Same engine result + same sentence assets → same Topic Narrative Unit.

No wall-clock, no LLM, no random order.

---

## 5. Fail-closed

Invalid engine payload → no topic unit pretending to be complete.

Insufficient facts → explicit insufficient blocks.

Never a silent empty string that looks like a finished reading.

---

END
