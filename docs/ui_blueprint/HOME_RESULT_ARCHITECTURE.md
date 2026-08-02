# HOME / RESULT ARCHITECTURE

| Field | Value |
|-------|--------|
| **Document** | `HOME_RESULT_ARCHITECTURE.md` |
| **Pack** | UI Sprint -00 — UX Blueprint Freeze |
| **Version** | `1.1.0` |
| **Status** | **Final Freeze — Blueprint V1.1** |
| **Audience** | Product, Design, Frontend, Domain Review |

---

## 1. Purpose of this document

Define the **Information Architecture** of the Result experience — the primary commercial screen of BTE Customer Portal.

This document answers:

- What the screen is for
- How a user should move through it
- What information appears, in what order, at what visual weight
- How scroll and interaction support reading — not hunting

**Out of scope:** CSS, React, component code, API contracts, engine logic.

**Related blueprints:** [WIREFRAME.md](WIREFRAME.md), [USER_READING_FLOW.md](USER_READING_FLOW.md), [COMPONENT_MAP.md](COMPONENT_MAP.md), [VISUAL_HIERARCHY.md](VISUAL_HIERARCHY.md), [NAVIGATION_SPEC.md](NAVIGATION_SPEC.md), [UX_PRINCIPLES.md](UX_PRINCIPLES.md).

---

## 2. Screen goal

### Primary goal

When the user opens **Result**, they must instantly feel:

> “This is my BaZi analysis report.”

Not:

> “This is an admin dashboard of JSON fields.”

### Success criteria (product)

| Criterion | Pass signal |
|-----------|-------------|
| Insight first | First viewport answers who the Day Master is, body strength framing, useful/helpful/unfavorable gods, pattern, and quality cue |
| Guided reading | User can finish a meaningful read by scrolling top → bottom without opening tabs |
| Hierarchy | Important facts are larger; secondary facts are smaller or collapsed |
| Honesty | Missing payload fields show Unavailable — never fabricated values |
| Professional analysis feel | Layout reads like TradingView/Bloomberg/Perplexity analysis surfaces — not CMS tables |

### Non-goals

- Replacing Report Center export workflows
- Mobile-first layout (desktop / laptop / tablet only in this blueprint era)
- Inventing Đại vận / Hợp-Xung data not present upstream

---

## 3. User journey (Result)

```text
[Analyze succeeds OR History/Dashboard Open]
        │
        ▼
[ResultStore loadForView]
        │
        ▼
[Result page mounts]
        │
        ├─► First 2 seconds: Executive Summary (Hero) dominates attention
        ├─► Optional: jump via Navigation Rail
        └─► Default: scroll Tier 1 → Tier 6
                │
                ▼
        [Optional: ask Knowledge Expert in Tier 6]
                │
                ▼
        [Exit to Reports / New Analyze / History]
```

Actors:

| Actor | Intent on Result |
|-------|------------------|
| End customer | Understand chart in plain professional language |
| Practitioner / power user | Scan structure, then drill interpretation + knowledge |
| Support / QA | Verify honesty of Unavailable vs present fields |

---

## 4. Mandatory reading order (Information Architecture spine)

**Fixed order. Do not reorder for “feature tabs.”**

| Order | Tier ID | Name (VI product) | Job of the tier |
|-------|---------|-------------------|-----------------|
| 1 | `tier-executive` | Tóm tắt điều hành | Answer the chart in one glance |
| 2 | `tier-bazi` | Bát Tự | Show Four Pillars as the chart identity |
| 3 | `tier-charts` | Biểu đồ | Support structure with visual encoding |
| 4 | `tier-analysis` | Phân tích | Large thematic analysis blocks |
| 5 | `tier-interpretation` | Luận giải | Domain narrative report |
| 6 | `tier-knowledge` | Kiến thức | Traceability + expert dialogue |

**Rule:** Navigation may *jump* to a tier; it must never *replace* this spine with peer tabs of equal weight.

---

## 5. Information hierarchy

### L0 — Page chrome (lowest narrative weight)

- Brand / app header (global shell)
- Result title + birth meta (date, gender)
- Actions: Open Reports, New Analyze

Chrome orients; it does not compete with Executive Summary.

### L1 — Executive Summary (highest weight)

**Normative block order (Addendum A):**

1. Eyebrow: Tóm tắt điều hành  
2. Nhật Chủ (+ element / yin-yang)  
3. **QualityVerdictCaption** (calm quality/confidence framing — never invent “lá số tốt”)  
4. One summary sentence (facts only)  
5. Metrics: Thân · Dụng · Hỷ · Kỵ · Cách Cục · Quality value  
6. Điểm mạnh / Điểm yếu (score lists only if present)  
7. **FirstRecommendation** callout (first recommendation from score/advice — else Unavailable)

| Fact | Role |
|------|------|
| Nhật Chủ (+ element / yin-yang) | Identity anchor |
| QualityVerdictCaption | Calm answer to “lá số thế nào?” without fear language |
| Thân (strength framing) | Structural hinge |
| Điểm mạnh / Điểm yếu | Score-derived lists only if present |
| Dụng Thần | Guidance axis |
| Hỷ Thần | Support axis |
| Kỵ Thần | Caution axis |
| Cách Cục | Pattern identity |
| Chất lượng lá số (value) | Grade / overall score / confidence if present |
| FirstRecommendation | First actionable guidance — Hero mandatory slot |
| One summary sentence | Narrative glue — no new facts |

Bindings: [18_BINDING_INDEX.md](18_BINDING_INDEX.md). Empty rules: [16_EMPTY_UNAVAILABLE_STATES.md](16_EMPTY_UNAVAILABLE_STATES.md).

### L2 — Four Pillars

Per pillar (Year / Month / Day / Hour):

- Can (stem)
- Chi (branch)
- Tàng Can
- Thập Thần
- Trường Sinh
- Nạp Âm

Day pillar is the visual anchor (highlight), not “one more equal card.”

### L3 — Charts (support L1–L2)

| Chart | Encodes |
|-------|---------|
| Element radar | Ngũ hành balance shape |
| Strength gauge | Numeric strength score only when available |
| Element bars | Distribution |
| Ten-god bars | Presence / frequency from pillars or score series |

Charts **support** narrative; they do not replace Executive Summary.

### L4 — Analysis (large sections)

One **large** section card per theme (not a grid of equal mini-cards):

1. Ngũ hành  
2. Thập thần  
3. Cách cục  
4. Dụng / Hỷ / Kỵ  
5. Hợp · Xung · Hình · Hại · Phá (Unavailable if absent)  
6. Thần sát  
7. Priority / Knowledge status (payload status only)

### L5 — Interpretation (report **document** — Addendum B)

Not a dashboard of peer cards. Structure:

- InterpretationHeader (title, confidence)  
- **InterpretationTOC** (required when ≥2 chapters available)  
- Chapters as **H2** document sections: Điểm nổi bật, Sự nghiệp, Tài vận, Hôn nhân, Sức khỏe, Tính cách, Lời khuyên  
- Optional H3, ReportCallout, References  

Empty chapter body → Unavailable; **titles never hidden**.

### L6 — Classical / Knowledge (Addendum C)

- Evidence rows: label, source_type (`rule`\|`classical`\|`reasoning`\|`status`), reference, confidence  
- Consumer UI: **no engine class names** by default  
- Knowledge Expert conversation (secondary within this tier)  
- Rule display titles only — no raw rule ids for consumers  

---

## 6. Section hierarchy (containment)

```text
ResultPage
├── ResultChrome (title, meta, actions)
├── NavigationRail (sticky, scroll-spy)
└── ReportStream
    ├── ExecutiveHero
    │     ├── DayMasterDisplay
    │     ├── QualityVerdictCaption
    │     ├── SummaryMetric[]
    │     ├── StrengthWeaknessPanel
    │     └── FirstRecommendation
    ├── PillarGrid
    ├── ChartBand
    ├── AnalysisStack
    │     └── AnalysisSection[] (large)
    ├── InterpretationDocument
    │     ├── InterpretationTOC
    │     └── InterpretationChapter[] (H2)
    └── KnowledgeStack
          ├── KnowledgeEvidencePanel
          └── KnowledgeExpertPane
```

Related: [15_VISUAL_GRAMMAR.md](15_VISUAL_GRAMMAR.md), [19_BLUEPRINT_V1_1_FINAL_FREEZE.md](19_BLUEPRINT_V1_1_FINAL_FREEZE.md).

---

## 7. Visual hierarchy (summary — detail in VISUAL_HIERARCHY.md)

| Level | Treatment |
|-------|-----------|
| Hero | Largest type, most whitespace, single dominant surface in first viewport |
| Pillar columns | Large equal columns; Day emphasized |
| Chart band | Medium surfaces; charts readable without zoom |
| Analysis / Interpretation | Large cards; collapse secondary |
| Knowledge | Dense but calm; expert pane nested |
| Captions / Unavailable | Smallest type; never alarm-red doom styling |

**Accent reserved for:** Nhật Chủ, Dụng, Hỷ, Kỵ, Thân — not every metric.

---

## 8. Scroll experience

| Behavior | Spec |
|----------|------|
| Default | Continuous vertical scroll through tiers 1→6 |
| First viewport | ≥60% of attention on Executive Hero (+ rail visible on desktop) |
| Scroll margin | Each tier has clear heading landing under sticky rail |
| Progress | Reading progress indicator on rail or thin top bar |
| Motion | Short fade/slide-in on tier enter; no noisy parallax |
| Skeleton | First paint shows hero + rail skeleton until model ready |

**Forbidden as primary UX:** horizontal tab strip that swaps the entire workspace and resets orientation.

---

## 9. Interaction model

| Interaction | Allowed | Role |
|-------------|---------|------|
| Scroll | Yes | Primary reading |
| Rail click / anchor jump | Yes | Secondary navigation |
| Expand / collapse large sections | Yes | Progressive disclosure inside T4–T6 |
| Hover on metrics / pillars | Yes | Subtle emphasis |
| Knowledge Expert ask | Yes | Only in T6; uses existing discussion API |
| Primary tab bar for tiers | **No** | Breaks reading order |
| Accordion as sole nav for tiers | **No** | Hides spine |

---

## 10. Data honesty contract (IA-level)

| Situation | UX |
|-----------|-----|
| Field present | Show value at correct hierarchy level |
| Field absent | Unavailable block with calm copy |
| Partial chart | Show text label without inventing gauge numbers |
| Knowledge offline | Error + Retry in Expert pane; keep narrative fallback |

IA must not pressure implementation to invent Hợp/Xung or luck decades.

---

## 11. Relationship to other portal pages

| Page | Relationship to Result |
|------|------------------------|
| Analyze | Produces payload → navigates here |
| Dashboard / History | “Open” lands here |
| Reports | Export / preview of same story; not a substitute for Result reading |
| Knowledge Expert (if promoted later) | Deep-link may land on `#tier-knowledge` |

See [SCREEN_BLUEPRINT.md](SCREEN_BLUEPRINT.md).

---

## 12. Acceptance checklist (architecture)

- [ ] Six tiers defined in fixed order  
- [ ] Executive facts listed without requiring tabs  
- [ ] Day pillar called out as visual anchor  
- [ ] Charts positioned as support, not homepage  
- [ ] Unavailable policy explicit  
- [ ] Navigation is rail + scroll-spy, not tabs  
- [ ] Cross-links to other blueprint docs present  

---

## Version

`1.1.0` — Blueprint V1.1 Final Freeze
