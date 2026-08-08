# 06 — Card Responsibility

Version: 1.0.0  
Status: **OFFICIAL — Design Reference**  
Date: 2026-08-08  
Sprint: Product Polish V1 · Sprint A  

---

## 1. Rule

**Every Result card answers one customer question only.**

If a card answers two questions, split responsibility (presentation) or demote the secondary answer — do not merge unrelated jobs.

---

## 2. Card catalog (existing Result surfaces)

### C-01 · Context / Identity

| Field | Definition |
|-------|------------|
| **Purpose** | Establish who the report is for |
| **Question** | Who is this about? |
| **Input** | Profile / chart identity fields from pipeline |
| **Output** | Compact identity strip (name/context/date as available) |
| **CTA** | None (or soft “verify details” only if already in product) |
| **Dependencies** | Portal Context row · frozen adapters |
| **Success** | Customer immediately trusts the report is theirs |

### C-02 · Executive Summary

| Field | Definition |
|-------|------------|
| **Purpose** | Deliver the consulting conclusion |
| **Question** | What is the essence of my situation? |
| **Input** | Narrative commercial executive composition |
| **Output** | 1 central + ≤3 supporting + 1 conclusion |
| **CTA** | Soft scroll/affordance toward Recommendation (no new route) |
| **Dependencies** | NarrativeResult · commercial presentation rules |
| **Success** | Customer can restate the conclusion without reading charts |

### C-03 · Core Analysis

| Field | Definition |
|-------|------------|
| **Purpose** | Explain the pattern behind the conclusion |
| **Question** | Why does this conclusion fit me? |
| **Input** | Analysis narrative / score-pattern framed prose |
| **Output** | Short structured explanation (strength/challenge seeds OK if single arc) |
| **CTA** | Optional expand to deeper interpretation |
| **Dependencies** | Narrative / Interpretation evidence |
| **Success** | Understanding without calculator feel |

### C-04 · Charts & Indicators

| Field | Definition |
|-------|------------|
| **Purpose** | Visually confirm analytical structure |
| **Question** | What does the analysis look like? |
| **Input** | Visualization models from pipeline |
| **Output** | Charts/indicators (Reference band) |
| **CTA** | Expand table / metric detail |
| **Dependencies** | Visualization adapters · Design System chart patterns |
| **Success** | Confirms advice; never replaces advice |

### C-05 · Primary Recommendation (Career Strategy)

| Field | Definition |
|-------|------------|
| **Purpose** | Tell the customer what to do next for career direction |
| **Question** | What should I do about my career path? |
| **Input** | Career Selection Assessment projection + Rec structure |
| **Output** | What / Why / How / When / Expected outcome |
| **CTA** | **Primary CTA** — commit to plan / save / continue consulting flow (existing mechanisms only) |
| **Dependencies** | CAP-CAREER-SEL-001 · Narrative merge policy |
| **Success** | Clear actionable primary path; owns commercial primary |

### C-06 · Secondary Recommendation (Promotion Readiness)

| Field | Definition |
|-------|------------|
| **Purpose** | Position promotion as a career milestone |
| **Question** | How ready am I to advance, as a next milestone? |
| **Input** | Promotion Readiness Assessment projection |
| **Output** | Readiness posture + shorter action summary |
| **CTA** | **Secondary CTA** — explore promotion plan detail (expand / in-page) |
| **Dependencies** | CAP-CAREER-PRO-001 · subordinate to C-05 |
| **Success** | Visible value; never outranks Career Strategy |

### C-07 · Detailed Interpretation

| Field | Definition |
|-------|------------|
| **Purpose** | Provide evidence-depth consulting prose |
| **Question** | What is the deeper reading behind this? |
| **Input** | Interpretation / enriched narrative sections |
| **Output** | Sectioned interpretation (expandable) |
| **CTA** | Expand / collapse only |
| **Dependencies** | Interpretation · Knowledge enrich-only |
| **Success** | Supports trust; optional on first pass |

### C-08 · Knowledge Reference

| Field | Definition |
|-------|------------|
| **Purpose** | Teach / deepen selected concepts |
| **Question** | What should I learn more about? |
| **Input** | Knowledge Units surfaced for the case |
| **Output** | Teaser + reference depth |
| **CTA** | “Learn more” expand (no new marketing route required) |
| **Dependencies** | Knowledge Layer (frozen) |
| **Success** | Education without derailing Actions |

### C-09 · Strength (when distinct card/block)

| Field | Definition |
|-------|------------|
| **Purpose** | Name what the customer can rely on |
| **Question** | What are my strengths here? |
| **Input** | Strength-oriented narrative / KU |
| **Output** | Short strength list |
| **CTA** | None / link tone into Rec How |
| **Dependencies** | Narrative · SEL/Wave content |
| **Success** | Empowerment without fluff |

### C-10 · Challenge / Risk / Mitigation (when distinct)

| Field | Definition |
|-------|------------|
| **Purpose** | Bound risk and show mitigation posture |
| **Question** | What could go wrong, and how do I handle it? |
| **Input** | Risk/mitigation narrative |
| **Output** | Risk + mitigation pairing |
| **CTA** | Feed into Rec How |
| **Dependencies** | Narrative · Domain KUs |
| **Success** | Honest, actionable caution |

### C-11 · Useful God / Support axis (customer-facing)

| Field | Definition |
|-------|------------|
| **Purpose** | Express support direction in commercial language |
| **Question** | What kind of support should I lean toward? |
| **Input** | Useful-god / support signals (commercialized wording) |
| **Output** | One clear support framing |
| **CTA** | None |
| **Dependencies** | commercial presentation layer · Wave 1.1 |
| **Success** | Understood without jargon |

---

## 3. Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| Card mixes Career + Promotion as equals | Split Primary/Secondary responsibility |
| Exec includes full 90-day plan | Move plan to Recommendation |
| Chart card includes advice essay | Advice stays in Rec; chart stays visual |
| Knowledge card sells upsell loudly | Upsell via CTA strategy, not Knowledge body |

---

## 4. Success criteria

- Each visible card maps to exactly one row in this catalog.  
- Reviewers can name the single question each card answers.  

---

## 5. Stop line

Card responsibility model is binding for Product Polish V1 presentation work.

---

END
