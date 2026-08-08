# 04 — Narrative Integration Spec

Version: 1.0  
Status: **EPIC 4 · SPRINT A**  
Date: 2026-08-08  
Depends on: `01`–`03`, Pack 05 Narrative models (frozen)  

---

## 1. Purpose

Define how Narrative consumes Commercial Knowledge **without redesigning** Pack 05.

```
Commercial Knowledge (via Adapter payload)
        ↓
Executive Summary
Recommendation
Warning
Insight (Observation / Reasoning / Impact)
Knowledge Panel
```

Preserve **traceability** and **analytical meaning**.

---

## 2. Consumption principle

Narrative already consumes typed evidence kinds:

`identity | strength | weakness | risk | action | grade | explanation | implication`

Commercial Knowledge Adapter emits **the same kinds**.  
Therefore Narrative Runtime/Composer need **no new section types**.

Phase B: merge payload into existing Narrative input path at orchestrator (preferred), not a Pack 05 redesign.

---

## 3. Component consumption map

| Narrative surface | Evidence kinds from CK | Wave 1.1 units |
|-------------------|------------------------|----------------|
| **Executive Summary** | identity, strength, weakness, explanation, action | ID, ST, WK, UG, RC |
| **Recommendation** | action (+ explanation as reason support) | RC, UG |
| **Warning** | weakness (soft); risk+mitigation future | WK (limited) |
| **Insight** | Observation←identity/strength; Reasoning←explanation; Impact←explanation | ID, ST, UG |
| **Knowledge Panel** | optional glossary units (not Wave 1.1) | — |
| **Conclusion** | identity + action settle | ID, RC |

---

## 4. Traceability requirements

Every filled commercial paragraph/slot must retain:

| Trace field | Source |
|-------------|--------|
| `knowledge_unit_id` | Selected KU |
| `version` | KU version |
| `evidence_kind` | KU / payload |
| `signal_refs` | Analysis keys used to bind/match |
| `bundle_id` | Retrieval run |

Portal may hide ids from customers; internal/debug and future Report must keep them.

---

## 5. Analytical meaning preservation

| Allowed | Forbidden |
|---------|-----------|
| Select KU whose condition matches Analysis | Emit ST text when strength unfavorable |
| Bind labels from Analysis | Invent day master / useful god |
| Omit slots when no KU | Fill with marketing copy |
| Use approved insufficient when empty | Fabricate Recommendation |

---

## 6. Interaction with Interpretation (unchanged engine)

| Rule | Detail |
|------|--------|
| IE code | **Not modified** |
| IE output | May remain for BC / technical paths |
| Commercial prose preference | Narrative should prefer CK evidence for Exec/Rec when payload present |
| Conflict | If IE technical prose and CK commercial prose both exist, Composer/filters already drop technical; CK fills commercial |

---

## 7. Status / sufficiency

| Bundle status | Likely Narrative status |
|---------------|-------------------------|
| complete (ID+RC at minimum when signals allow) | Improved chance of `complete` |
| partial | `partial_insufficient` possible but richer than baseline |
| empty | Baseline G6 behavior |

Wave 1.1 success metric (after Phase B + allow-list): noticeably better Exec + Rec when signals present.

---

## 8. Stop line

Narrative integration specified without engine redesign.

---

END
