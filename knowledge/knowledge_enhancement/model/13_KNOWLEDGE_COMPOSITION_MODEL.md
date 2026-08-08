# 13 — Knowledge Composition Model

Version: 1.0  
Status: **SPRINT C — Knowledge Unit Model**  
Date: 2026-08-08  
Depends on: `11`, `12`, Sprint B `07`–`09`  

---

## 1. Purpose

Define how **multiple Knowledge Units** compose into one consultation delivery.

```
Scenario
    ↓
Knowledge Unit
    ↓
Knowledge Unit
    ↓
Knowledge Unit
    ↓
Commercial Knowledge Layer (composed set)
    ↓
Narrative Component
    ↓
Narrative Result
```

Composition is design for future retrieval/runtime. No implementation in this sprint.

---

## 2. Composition thesis

| Thesis | Meaning |
|--------|---------|
| Units are atoms | Composition builds molecules of advice |
| Scenario sets the recipe | Required/optional/conditional profiles (`07`) |
| Commercial Knowledge layer is the composed set | SSOT for that consultation run |
| Narrative consumes composed evidence | Does not pick units ad hoc outside model |
| Independence preserved | Units remain reusable outside any one composition |

---

## 3. Composition order

Recommended assembly order for a run:

1. **Resolve scenario** (explicit CS-* or default CS-ID + CS-LT light + CS-MD light)  
2. **Load domain/kind profile** (`07`) + decision overlay if DS-*  
3. **Select Analytical units** (identity / explanation / grade substrate)  
4. **Select Consultation / Implication units** for active life themes  
5. **Select Opportunity units** (only if signals support)  
6. **Select Risk units** (conditional on hostile signals)  
7. **Select Mitigation units** paired to selected Risks  
8. **Select Action / Practical Guidance / Strategy units** consistent with posture  
9. **Deduplicate & conflict-resolve**  
10. **Map to evidence kinds → Narrative components**  
11. **Fill Pack 05 in official component order**  
12. **Mark insufficient** where Required profile unmet  

---

## 4. Priority within composition

| Priority band | Typical units |
|---------------|---------------|
| P0 Safety / ethics | Ethics-gated withholds; Protect posture Actions |
| P1 Risk + Mitigation | Caution pairs before aggressive Opportunity |
| P2 Identity / Analytical | Who + why (Exec/Observation/Reasoning) |
| P3 Action / Decision posture | Recommendation / next action |
| P4 Opportunity / Strategy | Lean-in only after risk gate |
| P5 Enrichment | Optional depth, Knowledge Panel |

Unit `priority` field breaks ties within a band (`09` ranking).

---

## 5. Conflict resolution

| Conflict | Resolution |
|----------|------------|
| Advance Action vs Wait Action | Higher Risk severity → Wait/Protect; else higher unit priority; else decision posture rules (`08`) |
| Opportunity vs Risk | Keep both; Recommendation must not claim Advance unless Opportunity survives Risk gate |
| Two Implications disagree | Prefer higher confidence + tighter `applicable_conditions`; suppress loser |
| Duplicate near-text | Keep highest rank; drop duplicates |
| Knowledge vs Analysis | Drop knowledge unit |
| Multi-scenario clash | Ethics > Mitigation > scenario-explicit Action > generic |

Conflicts must be logged in composition trace (design).

---

## 6. Fallback

| Gap | Fallback |
|-----|----------|
| No scenario KUs | Analytical identity/grade only |
| Required kind empty | Broader domain parent units |
| Still empty | Approved insufficient for slot/component |
| Risk without Mitigation pair | Family-level Mitigation template if Published; else soft Warning + insufficient mitigation flag |
| Decision without Opportunity | Allow Wait/Prepare Actions only |

Never fallback to technical rule prose or UI-invented advice.

---

## 7. Reuse

Composition **references** Published units by id; it does not clone text into Narrative templates.

| Reuse pattern | Example |
|---------------|---------|
| Same Identity KU | Default Result + CS-ID session |
| Same Mitigation KU | CS-IV and CS-FI sharing wealth-clash mitigation |
| Same Action Wait KU | CS-CC and CS-MD |

---

## 8. Deduplication

Rules:

1. Same `knowledge_unit_id` appears once per run.  
2. Semantically equivalent summaries (authoring-time) should have been prevented; runtime still drops near-duplicates by id family / hash if available.  
3. Risk+Mitigation pair is not a duplicate of either alone.  
4. Exec may *summarize* units already used in Recommendation — presentation reuse, not second selection of contradictory Actions.

---

## 9. Conditional composition

| Trigger | Compose |
|---------|---------|
| Hostile luck / clash signals | Add Risk (+ Mitigation Required) |
| Favorable useful-god luck | Allow Opportunity |
| Sensitive scenario (MA/CH/HE) | Only ethics-flagged units |
| Decision scenario | Force Action + posture vocabulary |
| No hostile signals | Do not invent Risk units |

Conditional composition aligns with `07` conditional cardinality.

---

## 10. Mapping composed set → Narrative

| Narrative component | Typical KU kinds in composition |
|---------------------|----------------------------------|
| Executive Summary | Analytical + Action + Risk (+ Opportunity derived) |
| Observation | Analytical |
| Reasoning | Analytical (explanation) |
| Impact | Consultation / Opportunity / Risk implication |
| Recommendation | Action / Practical Guidance / Strategy |
| Warning | Risk + Mitigation |
| Conclusion | Analytical settle + Action / Strategy |

Evidence typing follows `03` and `12.evidence_kind`.

---

## 11. Composition cardinality (guidance)

| Component | Soft max units (design) | Rationale |
|-----------|-------------------------|-----------|
| Exec | Small multi-kind pack | Briefing, not dump |
| Observation | 1–3 | Factual |
| Reasoning | 1–3 | Explain, don’t lecture |
| Impact | 1–4 | Focused implications |
| Recommendation | 1–3 actions | Specificity |
| Warning | 1–3 risk(+mitigation) pairs | Calm caution |
| Conclusion | 1–2 settle units | Memorable |

Exact caps are product-tunable later; principles stay.

---

## 12. Trace of a composition

A composed consultation should be able to export:

```
scenario_id
selected_knowledge_unit_ids[]
dropped_unit_ids[] + reasons
evidence_map: component → unit_ids
posture (if decision)
status: complete | partial_insufficient
```

This preserves end-to-end audit without coupling to UI.

---

## 13. Stop line

Composition model complete.  
No composer implementation in this sprint.

---

END
