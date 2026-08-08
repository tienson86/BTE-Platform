# 03 — Commercial Knowledge Adapter

Version: 1.0  
Status: **EPIC 4 · SPRINT A**  
Date: 2026-08-08  
Depends on: `01`, `02`  
Scope: Adapter specification — no implementation  

---

## 1. Purpose

Specify the **Commercial Knowledge Adapter**: the sole production component responsible for turning Knowledge Units + Analysis context into a Narrative-ready commercial payload.

| Adapter is | Adapter is not |
|------------|----------------|
| Filter / rank / bind / package | Score Engine |
| Advisory selector | Interpretation Engine rewrite |
| Trace emitter | Narrative Composer |
| Version gate | Portal |

Suggested logical module name (Phase B): `CommercialKnowledgeAdapter` (application/orchestrator layer).

---

## 2. Responsibilities

1. **Load** allow-listed Knowledge Units from corpus  
2. **Filter** by contract (`01`)  
3. **Map** KU → evidence units  
4. **Rank** candidates  
5. **Deduplicate** near-identical advice  
6. **Resolve conflicts**  
7. **Bind** placeholders from Analysis  
8. **Emit** Bundle + NarrativeKnowledgePayload  
9. **Honor** version compatibility  
10. **Extend** safely for future waves  

---

## 3. Mapping

| From | To |
|------|----|
| `modern_interpretation` (bound) | evidence `text` |
| `evidence_kind` | evidence kind enum |
| `narrative_targets` | `component_targets` |
| `knowledge_unit_id` + `version` | trace |
| `kind` | ranking hints / conflict classes |
| `paired_unit_ids` | pair boost / co-selection hints |

Wave 1.1 explicit map: see `05` / `06`.

---

## 4. Filtering

Apply in order (must match Retrieval Contract):

1. Status allow-list  
2. Ethics scope  
3. Condition match  
4. Scenario affinity  
5. Target component intersect (Wave 1.1: Exec + Rec)  
6. Confidence gates  
7. Contradiction drop  

---

## 5. Ranking

Conceptual score (align EPIC 2 retrieval model):

```
rank =
  + required_slot_fill
  + unit.priority
  + confidence
  + pair_boost
  + trace_quality
  - conflict_penalty
  - duplication_penalty
```

Wave 1.1 Exec fill order preference:

1. identity (KU-ID-001)  
2. strength (KU-ST-001) if eligible  
3. weakness (KU-WK-001) if eligible  
4. explanation (KU-UG-001) if eligible  
5. action (KU-RC-001) if eligible → also Rec  

---

## 6. Deduplication

| Rule | Detail |
|------|--------|
| Same `knowledge_unit_id` | Once per run |
| Same evidence_kind + near-identical text | Keep higher rank |
| UG explanation vs RC action | Not duplicates — different kinds |
| Exec may summarize Rec action | Presentation concern; Adapter still emits both kinds once |

---

## 7. Conflict resolution

| Conflict | Resolution |
|----------|------------|
| ST vs WK both eligible | Allow both (different slots); if bands mutually exclusive by condition, typically one fires |
| Multiple actions | Prefer higher priority; Wave 1.1 only one RC |
| Opportunity vs Risk (future) | Keep both; Rec posture must not Advance without opportunity gate |
| Knowledge vs Analysis | Drop knowledge unit |
| Bound text empty | Drop unit |

---

## 8. Version compatibility

| Rule | Detail |
|------|--------|
| Payload contract | `bte.commercial_knowledge.retrieval.v1` |
| Unit semver | Trace includes version |
| Unknown future fields | Ignore (forward compatible) |
| Unknown evidence_kind | Drop unit + log (do not pass to Narrative) |
| Corpus schema drift | Adapter validates required columns; fail soft |

---

## 9. Future expansion

| Expansion | Adapter impact |
|-----------|----------------|
| New Wave units | Filter/rank automatically if schema-compliant |
| RK+MT pairs | Enforce co-selection / Warning path |
| Multi-scenario | Scenario profile union |
| Report / AI | Same Bundle; different consumers |
| Interpretation Engine still frozen | Keep Adapter outside IE |

---

## 10. Public operations (logical API)

```text
adapt(
  analysis_signals,
  scenario_id,
  allow_list_status,
  target_components?= [executive_summary, recommendation],
  interpretation_hints?= null
) -> CommercialKnowledgeBundle + NarrativeKnowledgePayload
```

No runtime in Sprint A.

---

## 11. Stop line

Adapter specified. No implementation.

---

END
