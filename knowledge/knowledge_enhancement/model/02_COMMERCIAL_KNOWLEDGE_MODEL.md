# 02 — Commercial Knowledge Model

Version: 1.0  
Status: **SPRINT A — Commercial Knowledge Architecture**  
Date: 2026-08-08  
Depends on: `00_KNOWLEDGE_MODEL_INDEX.md`, `01_CONSULTATION_KNOWLEDGE_MODEL.md`  

---

## 1. Purpose

Define how **commercial knowledge** is organized for BTE.

Commercial Knowledge is the official layer that turns analytical truth into **professional advisory capability**.

It is:

| Is | Is not |
|----|--------|
| Explainable | Rule Database calculation tables |
| Advisory | Narrative composition engine |
| Traceable to Analysis signals | Free-form marketing copy |
| Reusable across Narrative / Portal / future Report | UI layout or Design System tokens |
| Consultant-facing | Engine-internal matcher dumps |

---

## 2. Position in the V1 stack

```
Rule Database / Operational CSVs     →  calculate & match
AnalysisResult                       →  facts & scores
Commercial Knowledge (this model)    →  meaning, advice, risk, strategy
Interpretation (commercial evidence) →  select & bind units
Narrative Engine                     →  compose NarrativeResult
Portal / Report                      →  present
```

**Single source of commercial advisory capability:** Commercial Knowledge (and the evidence units derived from it).  
Narrative must not invent advisory claims. Portal must not invent analysis.

---

## 3. Knowledge layer separation

### 3.1 Analytical Knowledge

| Attribute | Definition |
|-----------|------------|
| **Role** | Explain what the analysis *means* in human language |
| **Answers** | What is true about this chart structure? |
| **Inputs** | Strength, pattern, useful god, ten gods, elements, season, temperature, shensha, luck facts |
| **Outputs** | Identity language, structural explanations, grade framing |
| **Must not** | Duplicate numeric thresholds already in Rule Database |
| **Feeds** | Observation, Reasoning, Exec identity/grade |

### 3.2 Consultation Knowledge

| Attribute | Definition |
|-----------|------------|
| **Role** | Map analysis into consultation domains (Career, Finance, …) |
| **Answers** | What does this mean for the client’s life topic? |
| **Inputs** | Analytical Knowledge + domain catalog (`01`) |
| **Outputs** | Domain-themed implications and framing |
| **Must not** | Invent domain claims without analytical support |
| **Feeds** | Impact, domain-colored Exec / Conclusion |

### 3.3 Practical Guidance

| Attribute | Definition |
|-----------|------------|
| **Role** | Translate structure into usable everyday guidance |
| **Answers** | How should the client live with this structure? |
| **Inputs** | Useful god, strength, temperature, lifestyle/luck signals |
| **Outputs** | Habits, pacing, environment themes |
| **Must not** | Medical or legal prescriptions |
| **Feeds** | Recommendation support, Lifestyle domain |

### 3.4 Action Knowledge

| Attribute | Definition |
|-----------|------------|
| **Role** | Specify concrete next steps |
| **Answers** | What should I do now / this period? |
| **Inputs** | Useful god priorities, luck windows, decision criteria |
| **Outputs** | `action` evidence; priority recommendation; next action |
| **Must not** | Generic filler (“try harder”) without chart binding |
| **Feeds** | Recommendation, Exec priority/next action, Conclusion |

### 3.5 Risk Knowledge

| Attribute | Definition |
|-----------|------------|
| **Role** | Name cautions calmly and accurately |
| **Answers** | What should I watch for? |
| **Inputs** | Clash/harm, enemy gods, weak useful god, hostile luck, selected shensha |
| **Outputs** | `risk` / `weakness` evidence |
| **Must not** | Fear, curse, absolute doom language |
| **Feeds** | Warning, Exec weaknesses/risks |

### 3.6 Mitigation Knowledge

| Attribute | Definition |
|-----------|------------|
| **Role** | Pair every material risk with a constructive response |
| **Answers** | If this risk applies, what helps? |
| **Inputs** | Risk Knowledge + useful god / lifestyle / timing levers |
| **Outputs** | Mitigation actions bound to the same signal as the risk |
| **Must not** | Exist as orphan tips disconnected from risks (CQ-5) |
| **Feeds** | Warning (risk + mitigation), Recommendation |

### 3.7 Life Strategy Knowledge

| Attribute | Definition |
|-----------|------------|
| **Role** | Multi-horizon posture (years / decade) |
| **Answers** | How should I position my life path? |
| **Inputs** | Pattern path, useful god arc, đại vận narrative |
| **Outputs** | Strategy themes; growth priorities |
| **Must not** | Contradict current-period Action Knowledge |
| **Feeds** | Conclusion, Personal Growth, Exec opportunity framing |

### 3.8 Future Opportunity Knowledge

| Attribute | Definition |
|-----------|------------|
| **Role** | Name constructive openings without inventing facts |
| **Answers** | Where can I lean in? What windows exist? |
| **Inputs** | Strengths + useful god + favorable luck / combines |
| **Outputs** | Opportunity language (may map into strengths/priority when no separate field) |
| **Must not** | Fabricate opportunities when evidence is missing (use insufficient honesty) |
| **Feeds** | Exec opportunity reading, Recommendation, Impact |

---

## 4. Layer diagram

```
┌──────────────────────────────────────────────────────────┐
│                 Commercial Knowledge                      │
│                                                          │
│  Analytical Knowledge ──► Consultation Knowledge         │
│           │                        │                     │
│           ▼                        ▼                     │
│  Practical Guidance ◄── Life Strategy ◄── Opportunity    │
│           │                        │                     │
│           ▼                        ▼                     │
│      Action Knowledge ◄──► Risk Knowledge                │
│                ▲                  │                      │
│                └──── Mitigation Knowledge                │
└──────────────────────────────────────────────────────────┘
```

**Dependency rule:** Mitigation depends on Risk. Action should be consistent with Strategy. Opportunity must derive from Analytical + Luck support. Consultation depends on Analytical.

---

## 5. Commercial Knowledge Unit (conceptual record shape)

Sprint A defines the **logical unit** only — no schema files created here.

Every future commercial knowledge record should be expressible as:

| Field (logical) | Purpose |
|-----------------|---------|
| `knowledge_id` | Stable id |
| `kind` | One of the eight kinds in §3 |
| `consultation_domain` | CK-* from `01` (or `structural` for pure analytical) |
| `signal_condition` | When this unit may apply (bound to Analysis / RuleContext signals) |
| `advisory_text` | Consultant-facing language (commercial VI) |
| `evidence_kind` | Pack 05 kind: identity / strength / weakness / risk / action / explanation / implication / grade |
| `trace_refs` | Links to analytical signal ids / rule ids / REF-* |
| `priority` | Selection preference |
| `confidence` | Knowledge confidence |
| `ethics_flags` | e.g. sensitive_marriage, non_medical |
| `status` | draft / review / official |

Population format (CSV vs JSON vs Pack 04 library) is a **later decision**; the model is format-agnostic.

---

## 6. Mapping to Pack 05 evidence kinds

| Commercial kind | Primary evidence kinds |
|-----------------|------------------------|
| Analytical Knowledge | identity, explanation, grade, strength |
| Consultation Knowledge | implication (domain-framed), identity |
| Practical Guidance | action, implication |
| Action Knowledge | action |
| Risk Knowledge | risk, weakness |
| Mitigation Knowledge | action (paired to risk) |
| Life Strategy Knowledge | implication, action (horizon) |
| Future Opportunity Knowledge | strength, action |

---

## 7. Separation from Rule Database

| Rule Database | Commercial Knowledge |
|---------------|----------------------|
| Scores, weights, activation conditions | Meaning and advice |
| Machine-oriented | Human-oriented |
| May be technical | Must be commercial / non-technical |
| SSOT for *whether* a signal fires | SSOT for *what to say and advise* when it fires |
| Read by engines | Read by Interpretation / Knowledge retriever (future) |

**Rule:** If a statement is a threshold, weight, or match condition → Rule Database.  
**Rule:** If a statement is an explanation, recommendation, warning, or strategy → Commercial Knowledge.

Duplicating Rule Database inside Commercial Knowledge is forbidden (`05`).

---

## 8. Separation from Narrative

| Narrative | Commercial Knowledge |
|-----------|----------------------|
| Orders and composes sections | Supplies fillable meaning |
| Applies tone/filters | Authors advisory content |
| Emits NarrativeResult | Emits (future) knowledge/evidence units |
| May show approved insufficient copy | Must allow honest emptiness — never invent |

---

## 9. Completeness model for “commercial grade”

A chart consultation is commercially grade when, for the **active** domains in scope:

| Requirement | Knowledge kinds required |
|-------------|--------------------------|
| Can introduce the person | Analytical (identity) |
| Can explain why | Analytical (explanation) |
| Can state life impact | Consultation + Opportunity/Risk as supported |
| Can recommend | Action (+ Practical Guidance) |
| Can warn safely | Risk + Mitigation |
| Can settle a path | Life Strategy + Decision action |

Missing kinds → `partial_insufficient` or scoped insufficient slots — **correct**, not a failure of honesty.

---

## 10. Stop line

Commercial Knowledge Model defined.  
No records authored in this sprint.

---

END
