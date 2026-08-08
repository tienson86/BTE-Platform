# 02 — Review Process

Version: 1.0  
Status: **EPIC 3 · SPRINT A — Population Framework**  
Date: 2026-08-08  
Depends on: `01_POPULATION_WORKFLOW.md`, EPIC 2 `14`/`15`  

---

## 1. Purpose

Define official review stages for Knowledge Population:

1. Technical Review  
2. Knowledge Review  
3. Commercial Review  
4. Narrative Review  

Plus Approval / Publish ownership.

Each stage: **Purpose · Owner · Required checks · Exit criteria · Fail handling**.

---

## 2. Review order (mandatory)

```
Technical Review
    ↓
Knowledge Review
    ↓
Commercial Review
    ↓
Narrative Review
    ↓
Approval → Publish
```

Reviews are sequential for a single KU (or RK+MT pair treated as one package).  
Different KUs may be in different stages concurrently.

---

## 3. Technical Review

| Attribute | Definition |
|-----------|------------|
| **Purpose** | Structural correctness; store-ready metadata; no Rule Database duplication |
| **Owner** | Technical Reviewer (Knowledge Engineer / Architect) |
| **Inputs** | Draft KU (+ pair), author self-check |
| **Required checks** | See §3.1 |
| **Exit criteria** | Pass → Knowledge Review; Fail → Draft |
| **SLA guidance** | Set per content sprint (not fixed here) |

### 3.1 Required checks

- [ ] `knowledge_unit_id` matches catalog / naming (`15`)  
- [ ] Required logical fields present (`12`)  
- [ ] `kind`, `evidence_kind`, domains, scenarios valid enums/ids  
- [ ] `applicable_conditions` reference real Analysis signals  
- [ ] No thresholds/weights/match tables copied from Rule DB  
- [ ] `paired_unit_ids` correct for RK/MT  
- [ ] `primary_usage` / `secondary_usage` set  
- [ ] `supported_narrative_components` non-empty  
- [ ] No Portal/Report layout or CSS coupling  
- [ ] Version + status coherent  

---

## 4. Knowledge Review

| Attribute | Definition |
|-----------|------------|
| **Purpose** | BaZi advisory correctness; explainability; ethics |
| **Owner** | Knowledge Reviewer (domain expert) |
| **Required checks** | See §4.1 |
| **Exit criteria** | Pass → Commercial Review; Fail → Draft |

### 4.1 Required checks

- [ ] Body matches analytical meaning (no contradiction)  
- [ ] Classical support (if any) consistent with modern body  
- [ ] Granularity atomic; not a whole consultation dump  
- [ ] Domain/scenario affinity sensible  
- [ ] Ethics flags correct (MA/CH/HE/PA, non-medical, no return promises)  
- [ ] Not academic filler without advisory value  
- [ ] Reusable beyond a single marketing phrase  
- [ ] Risk language calm; no fate absolutism  

---

## 5. Commercial Review

| Attribute | Definition |
|-----------|------------|
| **Purpose** | Customer value, brand voice, commercial priority fit |
| **Owner** | Commercial / Product Reviewer |
| **Required checks** | See §5.1 |
| **Exit criteria** | Pass → Narrative Review; Fail → Draft (or Knowledge if meaning dispute) |

### 5.1 Required checks

- [ ] Answers a real consultation problem (`primary_intent`)  
- [ ] Improves Exec / Rec / Warning / Impact / decision posture as claimed  
- [ ] Priority aligns with wave (P0/P1/P2)  
- [ ] Consultant voice (not calculator)  
- [ ] Action specificity adequate when kind=AC  
- [ ] Opportunity does not overclaim  
- [ ] Sensitive domains acceptable for product scope  
- [ ] Commercial value (C/H/M/L) still accurate  

---

## 6. Narrative Review

| Attribute | Definition |
|-----------|------------|
| **Purpose** | Ensure unit can correctly feed Pack 05 / Content Quality without composer hacks |
| **Owner** | Narrative Reviewer (Narrative/Content Quality owner) |
| **Required checks** | See §6.1 |
| **Exit criteria** | Pass → Approval eligible; Fail → Draft |

### 6.1 Required checks

- [ ] `evidence_kind` matches intended Narrative slots  
- [ ] `supported_narrative_components` realistic for kind  
- [ ] Exec-targeted units fit briefing (identity/strength/weakness/action/risk)  
- [ ] Recommendation-targeted units are directive and chart-bound  
- [ ] Warning-targeted RK has MT pair path; mitigation actionable  
- [ ] No technical jargon that will be filtered to empty  
- [ ] Insufficient/honesty units (e.g. Reassess) use approved posture  
- [ ] Aligns Content Quality guidelines (Exec / Rec / Warning)  
- [ ] Will not force Narrative to invent claims  

**Narrative Review does not redesign Pack 05.** It accepts/rejects units against frozen grammar.

---

## 7. Approval process

| Attribute | Definition |
|-----------|------------|
| **Purpose** | Formal acceptance into release candidate set |
| **Owner** | Release Manager / Knowledge Ops |
| **Required checks** | All four reviews Pass; catalog id; pair integrity; wave membership |
| **Exit criteria** | `approved`; queued for Publish batch |

Approval may be **per unit** or **per wave batch**. Batch preferred for P0.

---

## 8. Publish process

| Attribute | Definition |
|-----------|------------|
| **Purpose** | Make unit production-eligible |
| **Owner** | Knowledge Ops |
| **Required checks** | Approved status; publish manifest updated; timestamps; no unresolved ethics hold |
| **Exit criteria** | `published`; visible to future retrieval allow-list |

Rollback: Deprecate published version; publish superseding unit (`04`).

---

## 9. Fail handling

| Outcome | Action |
|---------|--------|
| Minor fix | Author amends Draft; restart from failed stage (or Technical if metadata changed) |
| Major meaning rewrite | Restart from Technical |
| Reject / out of scope | Close Draft; catalog note; do not Publish |
| Pair fail | Both RK and MT return to Draft |

All fails recorded with reviewer, date, reason.

---

## 10. RACI (summary)

| Activity | Author | Tech | Know | Comm | Narr | Ops |
|----------|:------:|:----:|:----:|:----:|:----:|:---:|
| Draft | R | C | C | I | I | I |
| Technical Review | C | R/A | I | I | I | I |
| Knowledge Review | C | I | R/A | I | I | I |
| Commercial Review | C | I | C | R/A | I | I |
| Narrative Review | C | I | C | C | R/A | I |
| Approve / Publish | I | I | I | C | C | R/A |

R=Responsible A=Accountable C=Consulted I=Informed

---

## 11. Stop line

Review process defined. No reviews executed (no units exist yet).

---

END
