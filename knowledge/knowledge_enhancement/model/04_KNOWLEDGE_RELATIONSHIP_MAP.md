# 04 — Knowledge Relationship Map

Version: 1.0  
Status: **SPRINT A — Commercial Knowledge Architecture**  
Date: 2026-08-08  
Depends on: `00`–`03`  

---

## 1. Purpose

Document relationships among:

- Knowledge Domains (consultation + commercial kinds)  
- Rule Database  
- Evidence  
- Narrative  
- Portal  
- Report  

Show dependency direction. Higher commercial layers must not write lower analytical layers.

---

## 2. System topology (V1 frozen)

```
┌─────────────────────────────────────────────────────────────────┐
│ Foundation (frozen) — Brand / Experience / Design System         │
│        constrains voice & presentation only                       │
└─────────────────────────────────────────────────────────────────┘
                              │ constrains
                              ▼
┌──────────────┐   read    ┌──────────────────┐
│ Rule Database│ ────────► │ Analysis Engines │
│ (CSV / packs)│           │ Score / Pattern… │
└──────────────┘           └────────┬─────────┘
                                    │ AnalysisResult
                                    ▼
┌──────────────────────────────────────────────┐
│ Commercial Knowledge (model SSOT for advice) │
│  Analytical / Consultation / Action / Risk…  │
└──────────────────────┬───────────────────────┘
                       │ knowledge units
                       ▼
               ┌───────────────┐
               │   Evidence    │
               └───────┬───────┘
                       ▼
               ┌─────────────────────┐
               │ Interpretation      │
               │ InterpretationResult│
               └──────────┬──────────┘
                          ▼
               ┌─────────────────────┐
               │ Narrative Engine    │
               │ NarrativeResult     │
               └──────────┬──────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
        ┌──────────┐            ┌──────────┐
        │  Portal  │            │  Report  │
        │ Result UI│            │ (future) │
        └──────────┘            └──────────┘
```

---

## 3. Relationship matrix

| From → To | Relationship | Allowed? |
|-----------|--------------|----------|
| Rule Database → Analysis | Inputs for calculation | Yes |
| Analysis → Commercial Knowledge | Signals select knowledge | Yes (read facts) |
| Commercial Knowledge → Rule Database | Knowledge writes rules | **No** |
| Commercial Knowledge → Evidence | Materializes typed units | Yes |
| Evidence → Interpretation | Matching / binding | Yes |
| Interpretation → Narrative | Commercial refs / sections | Yes |
| Narrative → Portal | NarrativeResult presentation | Yes |
| Narrative → Report | NarrativeResult presentation | Yes (future) |
| Portal → Commercial Knowledge | UI invents advice | **No** |
| Report → Interpretation scrape | Bypass NarrativeResult | **No** (future policy) |
| Foundation → Commercial Knowledge | Voice constraints | Yes (soft) |
| Commercial Knowledge → Foundation | Knowledge edits DS | **No** |

---

## 4. Knowledge Domains ↔ Rule Database

Consultation domains (`01`) consume analytical signals produced via Rule Database — they do not replace them.

```
Rule DB: strength / pattern / useful_god / ten_gods / luck / clash…
        ↓ signals
Consultation domains: Career / Finance / Marriage / Luck / …
        ↓ framed by
Commercial kinds: Analytical / Consultation / Action / Risk / Mitigation…
```

| Consultation domain | Typical Rule DB signal families |
|---------------------|---------------------------------|
| Identity | day master, pattern, strength |
| Personality | ten gods, day master |
| Career / Business / Leadership | useful god, ten gods, pattern, luck |
| Finance | wealth structures, useful/enemy, luck, clash |
| Marriage / Relationships / Children / Parents | palace/relation rules, clash/harm, ten gods |
| Health (lifestyle) | temperature, wuxing, selected shensha |
| Education | output/resource, useful god, luck |
| Luck | đại vận / lưu niên / clash with natal |
| Decision Making / Lifestyle / Growth | useful god, strength, pattern, luck |
| Environment | useful god elements (+ optional feng shui rules) |

---

## 5. Knowledge Domains ↔ Evidence ↔ Narrative

```
CK Domain + Commercial Kind
        ↓
Evidence kind (identity/strength/weakness/risk/action/…)
        ↓
Pack 05 component(s)
```

| Evidence kind | Primary Narrative components |
|---------------|------------------------------|
| identity | Exec, Observation, Conclusion |
| strength | Exec, Observation, Conclusion |
| weakness | Exec, Warning, Conclusion |
| risk | Warning, Exec |
| action | Recommendation, Warning mitigation, Exec, Conclusion |
| grade | Observation, Exec |
| explanation | Reasoning |
| implication | Impact |

Detail: `03_NARRATIVE_KNOWLEDGE_MODEL.md`.

---

## 6. Evidence ↔ Portal / Report

```
Evidence ──► Interpretation ──► NarrativeResult ──┬──► Portal adapters
                                                 └──► Report (future)
```

| Surface | May read | Must not read for commercial prose |
|---------|----------|-------------------------------------|
| Portal Result Page | `narrative_result` | Raw Rule DB; inventing from scores alone |
| Portal Knowledge zone | Structural glossary / chart facts (G5) | Alternate advice corpus |
| Report Engine (future) | `narrative_result` | Re-scrape technical Interpretation |

---

## 7. Dual stores (documented coexistence)

Epic 1 noted multiple knowledge/rule surfaces. Relationship policy:

| Store | Relationship to Commercial Knowledge Model |
|-------|---------------------------------------------|
| `database/11–15_*`, `02_quan_he` | Analytical Rule SSOT (runtime) |
| `database/05_phan_tich` life packs | Candidate **inputs** after triage — not auto commercial SSOT |
| `database/interpretation_rules` | Partial; must align to Commercial Knowledge when wired |
| `database/20_knowledge` | Primary candidate **commercial explainable corpus** |
| `knowledge/rule_database/*_rules` | Documentary / design rules — not Portal advice SSOT |
| `knowledge/bazi/*` | Academic authoring aligned to domains |
| Pack 04 sentence library | Runtime commercial evidence consumer — must map to model kinds |
| `knowledge/sentence_library` | Framework; future alignment under Expansion Guidelines |

---

## 8. Dependency diagrams (logical)

### 8.1 Authoring dependency

```
References / Terminology / Canon
        ↓ cite
Commercial Knowledge units
        ↓ require signals from
Rule Database (stable signals)
```

### 8.2 Runtime dependency (target architecture)

```
Chart → AnalysisResult
           ↓
    Knowledge Retriever / Matcher  (future implementation epic)
           ↓
    Evidence units
           ↓
    Interpretation → Narrative → Portal
```

### 8.3 Forbidden dependency

```
Portal ──X──► Rule Database (for prose)
Narrative Composer ──X──► invent Commercial Knowledge
Commercial Knowledge ──X──► rewrite Score thresholds
```

---

## 9. Ownership summary

| Concern | Owner |
|---------|-------|
| Calculation rules | Rule Database + Analysis engines |
| Commercial advisory meaning | Commercial Knowledge Model (content owners) |
| Evidence typing & selection | Interpretation (runtime) + Knowledge content |
| Prose composition | Narrative Engine |
| Presentation | Portal / Report |
| Brand / layout | Foundation |

---

## 10. Stop line

Relationship map complete.  
No wiring implemented in this sprint.

---

END
