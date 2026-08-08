# 03 — Narrative Knowledge Model

Version: 1.0  
Status: **SPRINT A — Commercial Knowledge Architecture**  
Date: 2026-08-08  
Depends on: `02_COMMERCIAL_KNOWLEDGE_MODEL.md`, Epic 1 `04`/`05` reports  

---

## 1. Purpose

Define how **Narrative consumes knowledge** under the frozen V1 pipeline.

Invariant:

```
Knowledge
    ↓
Evidence
    ↓
Interpretation
    ↓
Narrative Component
    ↓
Narrative Result
```

Every Narrative component must be **traceable back to Knowledge**.  
No commercial claim may appear in NarrativeResult without an upstream evidence unit grounded in Commercial Knowledge (or direct Analysis facts explicitly allowed as identity/grade substrate).

---

## 2. Official pipeline (frozen)

```
Rule Database / Analysis engines
        ↓
AnalysisResult                          (facts)
        ↓
Commercial Knowledge selection          (advisory meaning)   ← model layer
        ↓
Evidence units                          (typed commercial evidence)
        ↓
Interpretation Engine                   (InterpretationResult / refs)
        ↓
Narrative Runtime → NarrativeTree
        ↓
Narrative Composer
        ↓
NarrativeResult                         (7 sections + summary)
        ↓
API → Portal / future Report
```

Sprint A documents the **Knowledge → Evidence** contract. It does not implement loaders.

---

## 3. Traceability chain (required)

| Stage | Artifact | Trace requirement |
|-------|----------|-------------------|
| Knowledge | Commercial Knowledge Unit (`02` §5) | Stable `knowledge_id` |
| Evidence | Evidence unit with `evidence_kind` | Links `knowledge_id` + analytical `signal_id` |
| Interpretation | Section / ref body | Retains knowledge/evidence refs; no silent rewrite of meaning |
| Narrative Component | Paragraph / slot | Trace refs on filled paragraphs (existing Pack 05 behavior) |
| NarrativeResult | Full object | Status reflects sufficiency; insufficient when chain breaks |

**Honesty rule:** If the chain cannot fill a required slot → approved insufficient copy for that slot/component. Never invent.

---

## 4. Evidence kinds (consumer contract)

Aligned with Pack 05 / Epic 1 evidence model:

| Evidence kind | Narrative use |
|---------------|---------------|
| `identity` | Exec, Observation, Conclusion |
| `strength` | Exec, Observation, Conclusion, Opportunity reading |
| `weakness` | Exec, Warning, Conclusion |
| `risk` | Warning, Exec |
| `action` | Recommendation, Exec priority/next, Mitigation, Conclusion |
| `grade` | Observation, Exec |
| `explanation` | Reasoning |
| `implication` | Impact, Consultation framing |

Technical / rule-match prose is **not** a valid commercial evidence kind (filter remains).

---

## 5. Component binding matrix

| Narrative component | Required knowledge kinds (commercial) | Primary evidence kinds | Traceable when |
|---------------------|----------------------------------------|------------------------|----------------|
| **Executive Summary** | Analytical + Action + Risk (+ Opportunity as derived) | identity, strength, weakness, action, risk, grade | Each briefing answer cites evidence |
| **Observation** | Analytical | identity, strength, grade | Facts not invented |
| **Reasoning** | Analytical (explanation) | explanation | Explanation units non-technical |
| **Impact** | Consultation (+ Opportunity/Risk as supported) | implication | Implication bound to signal |
| **Recommendation** | Action + Practical Guidance (+ Strategy consistency) | action | Actions bound to useful god / luck / domain |
| **Warning** | Risk + **Mitigation** | risk, weakness, action | Every warning risk pairs mitigation when material |
| **Conclusion** | Analytical + Action + Strategy settle | mixed | Settles only supported claims |

### NarrativeSummary slots

| Slot | Knowledge kind | Evidence |
|------|----------------|----------|
| `identity` | Analytical | identity |
| `strengths[]` | Analytical / Opportunity | strength |
| `weaknesses[]` | Risk / Analytical | weakness |
| `priority_recommendation` | Action / Strategy | action |
| `next_action` | Action / Practical Guidance | action |
| `insufficient_flags` | — | Set when chain empty |

---

## 6. Knowledge → component flow (diagram)

```
Analytical Knowledge ──► identity/explanation/grade ──► Observation
         │                                              Reasoning
         │                                              Exec (who / grade)
         ▼
Consultation Knowledge ──► implication ───────────────► Impact
         │                                              Exec (life framing)
         ▼
Action + Practical Guidance ──► action ───────────────► Recommendation
         │                                              Exec priority/next
         ▼
Risk Knowledge ──► risk/weakness ──┐
                                   ├──► Warning
Mitigation Knowledge ──► action ───┘
         │
Life Strategy + Opportunity ──► implication/action ──► Conclusion / Exec opportunity reading
```

---

## 7. Sufficiency model (Narrative status)

| Condition | Narrative status expectation |
|-----------|------------------------------|
| All components have required evidence kinds for in-scope briefing | `complete` |
| Some components/slots missing commercial units | `partial_insufficient` |
| Pipeline failure upstream | `failed` |

Commercial Knowledge volume and quality directly control the rate of `partial_insufficient` (Epic 1 G6). Narrative Engine behavior is already correct to prefer honesty over filler.

---

## 8. What Narrative may use without a Commercial Knowledge record

Allowed **minimal substrate** from AnalysisResult (facts, not advice):

- Day master / pattern codes rendered via approved Analytical Knowledge templates (preferred) or tightly constrained identity formatters  
- Numeric grade / band as `grade` when Analysis provides it  

Not allowed without Commercial Knowledge:

- Recommendations  
- Warnings / mitigations  
- Life-domain implications (career, marriage, …)  
- Strategy and opportunity language beyond restating supported strengths  

---

## 9. Multi-consumer rule

The same Knowledge → Evidence chain must serve:

| Consumer | Consumes |
|----------|----------|
| Pack 05 NarrativeResult | Evidence via Interpretation |
| Portal Result Page | NarrativeResult (preferred) |
| Future Report Engine | NarrativeResult (not a second knowledge scrape) |
| Future Knowledge Expert answers | Commercial Knowledge retrieval directly |

**One advisory SSOT.** Presentation layers do not maintain parallel advice corpora.

---

## 10. Anti-patterns

| Anti-pattern | Why forbidden |
|--------------|---------------|
| Composer invents mitigation when Risk exists without Mitigation Knowledge | Breaks traceability |
| Portal writes career advice from raw score fields | Bypasses Knowledge |
| Report Engine re-scrapes Interpretation technical text | Circumvents commercial model |
| Duplicate advice strings only in UI i18n | Second SSOT; drifts from Knowledge |
| Filling Exec with marketing claims | Violates Content Quality + truthfulness |

---

## 11. Stop line

Narrative Knowledge Model defined.  
No runtime or library changes in this sprint.

---

END
