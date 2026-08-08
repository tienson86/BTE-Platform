# 11 — Knowledge Unit Model

Version: 1.0  
Status: **SPRINT C — Knowledge Unit Model**  
Date: 2026-08-08  
Depends on: Sprint A–B (`00`–`10`) — **frozen**  
Scope: Documentation only — no records, no JSON/CSV, no runtime  

---

## 1. Purpose

Define the **Knowledge Unit (KU)** — the atomic, reusable building block of Commercial Knowledge.

```
Knowledge Units (many, independent)
        ↓ compose
Commercial Knowledge (advisory SSOT layer)
        ↓ select / bind
Evidence → Interpretation → Narrative → NarrativeResult
        ↓
Portal / Report / future AI
```

Sprint A introduced a conceptual commercial unit shape.  
Sprint C makes that concept **official, complete, and operationalizable** for future population — without creating records yet.

---

## 2. What is a Knowledge Unit?

A Knowledge Unit is **one reusable piece of professional advisory knowledge**.

| Property | Requirement |
|----------|-------------|
| Atomic | One primary advisory intent (not a whole report) |
| Reusable | Usable across scenarios, channels, and compositions |
| Traceable | Linked to signals, domains, scenarios, and Narrative targets |
| Versionable | Independent lifecycle and version identity |
| Independent | Does not depend on a specific UI, renderer, or Report layout |
| Explainable | Consultant-facing meaning; not engine jargon |
| Composable | Combines with other units under Scenario profiles |

**One sentence test:** *If this unit disappeared, which single advisory building block would consultants lose?*

---

## 3. Why it exists

| Problem without KU | Solution with KU |
|--------------------|------------------|
| Advice buried in Narrative templates | Advice lives as reusable knowledge |
| Portal/Report invent parallel copy | One SSOT unit → many consumers |
| Academic folders ≠ customer problems | Units answer consultation intents |
| G6 thin evidence | Units materialize commercial evidence candidates |
| Unreviewable prose blobs | Units are reviewable, versionable atoms |

Knowledge Units are the foundation for future `database/20_knowledge` (and/or evidence libraries) population — schema-first, content-later.

---

## 4. What a Knowledge Unit is not

| Concept | Difference |
|---------|------------|
| **Rule** | Rules calculate/match (thresholds, weights, activation). KU advises when signals already exist. Never duplicates Rule Database. |
| **Evidence** | Evidence is the **typed runtime selection** of a KU (or allowed Analysis substrate) for Pack 05 kinds. KU is the authored source; Evidence is the selected instance in a run. |
| **Interpretation** | Interpretation matches/binds and emits InterpretationResult. It consumes KU-derived evidence; it does not own advisory SSOT. |
| **Narrative** | Narrative composes ordered components into NarrativeResult. It does not author KU content. |
| **Commercial Knowledge** | Commercial Knowledge is the **layer / corpus** of advisory meaning. KUs are the **atoms** that compose that layer. |
| **Scenario** | Scenario is customer intent entry point (`CS-*`). It selects which KUs may apply; it is not knowledge itself. |
| **Report section / Portal card** | Rendering concerns. KU must remain render-independent. |

### Principle lock

| Statement |
|-----------|
| A Knowledge Unit is **NOT** a Rule. |
| A Knowledge Unit is **NOT** Narrative. |
| A Knowledge Unit is **NOT** a Report section. |
| Multiple Knowledge Units **form** Commercial Knowledge. |
| Commercial Knowledge **supports** Narrative. |
| Narrative **generates** user-facing consultation. |

---

## 5. Responsibilities

A Knowledge Unit is responsible for:

1. Stating one advisory meaning (summary + body intent)  
2. Declaring when it may apply (conditions / signals)  
3. Declaring which commercial **kind** it belongs to (`02`)  
4. Declaring domain / scenario affinity  
5. Declaring primary & secondary usage (Narrative + channels)  
6. Declaring evidence kind and Narrative component support  
7. Carrying trace, confidence, priority, ethics, version, review status  
8. Remaining safe to compose with other units  

A Knowledge Unit is **not** responsible for:

- Scoring charts  
- Ordering Pack 05 sections  
- Laying out Portal/Report  
- Resolving multi-unit conflicts at runtime (Composition + Retrieval models do)  

---

## 6. Granularity

| Too big (reject) | Right size | Too small (usually reject) |
|------------------|------------|----------------------------|
| Entire Career consultation | One Action for career-change Wait posture | Single synonym with no advisory value |
| Full Exec Summary text | One Identity framing for thân vượng band | Orphan classical quote with no modern advisory use |
| Whole Warning chapter | One Risk + linkable Mitigation pair ids | UI label string |

**Guideline:** Prefer units that fill **one evidence kind** and **one primary usage**, optionally supporting secondary channels.

Risk and Mitigation may be separate KUs with explicit pairing metadata (preferred for reuse).

---

## 7. Reuse strategy

| Reuse axis | How |
|------------|-----|
| Across scenarios | Same Action KU usable in CS-CC and CS-MD when conditions match |
| Across domains | Analytical Identity KU reused whenever CS-ID / default Result needs identity |
| Across Narrative components | One implication KU may serve Impact and Exec opportunity reading |
| Across channels | Primary Narrative usage + Secondary Portal/Report/AI/Search |
| Across time | Versioned unit; traces keep old version ids |

**Dedup rule:** Do not create a new KU that only rephrases an Official unit without new conditions or intent.

---

## 8. Traceability

Mandatory chain:

```
Knowledge Unit
    ↓
Commercial Knowledge (composed selection)
    ↓
Evidence
    ↓
Interpretation
    ↓
Narrative Component
    ↓
Narrative Result
    ↓
Portal / Report
```

Every published KU must be able to appear in traces with stable `knowledge_unit_id` (see `12`).

---

## 9. Lifecycle (summary)

```
Draft → Technical Review → Knowledge Review → Commercial Review
    → Approved → Published → Revised → Deprecated
```

Full stage definitions: `14_KNOWLEDGE_LIFECYCLE.md`.

Only **Published** (and approved-for-prod equivalents) units may feed production Narrative.

---

## 10. Primary / Secondary usage

Every KU must declare usage metadata (detail in `12`).

### Primary Usage (consultation delivery)

| Primary target | Why |
|----------------|-----|
| Executive Summary | Briefing slots |
| Recommendation | Directive actions |
| Warning | Caution (+ mitigation pairing) |
| Interpretation | Explainable binding upstream of Narrative |
| Knowledge Panel | Glossary / structural explain surfaces (non–Pack 05 section, still KU-sourced) |

### Secondary Usage (distribution)

| Secondary target | Why |
|------------------|-----|
| Portal | Same meaning via NarrativeResult / panels — no parallel copy |
| Report | Long-form via NarrativeResult |
| AI Assistant | Retrieval answers from same SSOT |
| Search | Discoverability of advisory topics |
| Mobile | Same units; different chrome |
| Future APIs | Machine-stable advisory atoms |

**Why this metadata matters:** Without primary/secondary declaration, teams re-author the same advice per surface, breaking SSOT and traceability. Usage metadata also drives retrieval ranking (`09`) and composition targeting (`13`).

---

## 11. Intended usage examples (illustrative — not records)

These are **examples of intent**, not authored units:

| Example intent | Kind | Primary usage | Scenario affinity |
|----------------|------|---------------|-------------------|
| “Identity: thân vượng + cách cục X — how to name the person” | Analytical | Executive Summary, Observation | CS-ID |
| “Career change: Wait this đại vận if useful god is suppressed” | Action | Recommendation | CS-CC, DS-CC |
| “Wealth clash period — capital overextension caution” | Risk | Warning | CS-IV, CS-FI |
| “If wealth clash risk applies — liquidity buffer mitigation” | Mitigation | Warning, Recommendation | paired to risk family |
| “Favorable output luck — selective opportunity lean-in” | Opportunity | Exec / Recommendation | CS-LT, CS-CA |
| “Lifestyle: pace recovery when temperature extreme” | Practical Guidance | Recommendation | CS-HE, CS-LS |

No JSON/CSV created for these examples.

---

## 12. Independence from rendering

KUs must not embed:

- CSS / Design System tokens  
- Portal component names as sole identity  
- Report markdown layout  
- Locale-specific presentation hacks as the only body  

KUs may include commercial VI advisory text as content.  
Presentation systems adapt; they do not own the meaning.

---

## 13. Relationship to Sprint A conceptual shape

Sprint A `02` §5 logical fields remain valid and are **superseded in detail** by `12_KNOWLEDGE_UNIT_SCHEMA.md` (superset).  
Sprint C does not invalidate Sprint A kinds (`02` §3) or Scenario model (Sprint B).

---

## 14. Stop line

Knowledge Unit Model defined.  
No Knowledge Units authored in this sprint.

---

END
