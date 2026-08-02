# 12 — GAP ANALYSIS & NORMATIVE ADDENDA

| Field | Value |
|-------|--------|
| **Document** | `12_GAP_ANALYSIS.md` |
| **Version** | `1.1.0` |
| **Status** | **Applied** — Addenda A–I are normative in Blueprint V1.1 Final; see [19](19_BLUEPRINT_V1_1_FINAL_FREEZE.md) |
| **Code** | None |

---

## Purpose

List every gap that would force **implementation guessing**, and freeze **normative resolutions** so UI Sprint 01+ does not invent product behavior.

**V1.1 note:** Resolutions below are **integrated** into docs 01–10, Binding Index [18](18_BINDING_INDEX.md), and Addenda J–L ([15](15_VISUAL_GRAMMAR.md)–[17](17_LOCALIZATION_CONTRACT.md)). This file remains the audit trail.

---

## Gap register

| ID | Area | Gap | Severity | Blocks Sprint |
|----|------|-----|----------|---------------|
| G1 | Hero | No **first recommendation** | High | 02 |
| G2 | Hero | No explicit **quality verdict caption** (“tốt / cần chú ý” calm framing) | High | 02 |
| G3 | Interpretation | No **document model** (TOC, H2/H3, callout, citation) | High | 05 |
| G4 | Knowledge | No **evidence field matrix** / display rules | High | 06 |
| G5 | Knowledge | “Engine nào?” unspecified vs anti-jargon | Medium | 06 |
| G6 | Components | No Atomic/Composite/Layout/Business taxonomy | Medium | 01+ |
| G7 | Naming | Rail / Hero / Mermaid aliases | Low | 01 |
| G8 | Screens | Analysis/Interpretation/Knowledge vs Result tiers | Medium | 01 |
| G9 | Responsive | Laptop band + secondary screens | Medium | 07–08 |
| G10 | Reports | Thin wireframe / first-page export alignment | Medium | 08 |
| G11 | Dashboard | Must-never-hide CTA not explicit | Low | 08 |
| G12 | Analysis | “Short explain” body content source unspecified | Medium | 04 |
| G13 | Data map | No single payload→UI binding table | High | 02–06 |
| G14 | Priority Rules | Label present; meaning/UI content vague | Medium | 04 |

---

## Addendum A — Executive Hero (closes G1, G2)

### A.1 Required Hero blocks (normative order)

1. Eyebrow: Tóm tắt điều hành  
2. DayMasterDisplay (Nhật Chủ + element + yin-yang)  
3. **QualityVerdictCaption** (new)  
4. Summary sentence (facts only; no new claims)  
5. Metric row: Thân · Dụng · Hỷ · Kỵ · Cách Cục · Quality value  
6. Strengths / Weaknesses panels  
7. **FirstRecommendation** (new)  

### A.2 QualityVerdictCaption

| Input priority | Display |
|----------------|---------|
| `score.grade` | Calm phrase mapped by grade table (i18n) |
| else `score.total_score` / `overall_score` | Band: e.g. cao / trung bình / cần chú ý (thresholds product-owned; default 70+/40–69/<40) |
| else `interpretation.confidence` | “Độ tin cậy đọc: {value}” — not a quality verdict |
| else | Unavailable — do **not** invent “lá số tốt” |

**Forbidden:** Fear, absolute good/bad destiny language ([Interpretation Architecture](../architecture/interpretation/03_NARRATIVE_GUIDE.md) alignment).

### A.3 FirstRecommendation

| Input priority | Display |
|----------------|---------|
| `score.recommendations[0]` or first list item | Show as callout “Khuyến nghị đầu tiên” |
| else first non-empty Interpretation chapter `advice` / `conclusion` sentence | Same |
| else | Unavailable block (honest) |

Must not invent recommendations. Must appear **in Hero**, not only in Tier 5.

### A.4 Wireframe delta (ASCII)

```text
|  QualityVerdictCaption (calm)                                            |
|  ... metrics ...                                                         |
|  +-- Khuyến nghị đầu tiên (callout) ----------------------------------+ |
|  | one sentence OR Unavailable                                         | |
|  +---------------------------------------------------------------------+ |
```

---

## Addendum B — Interpretation as document (closes G3)

### B.1 Mental model

Interpretation Tier = **one Report Document**, not a dashboard of peer cards.

### B.2 Required structure

```text
InterpretationDocument
├── InterpretationHeader (title, confidence)
├── InterpretationTOC (mục lục — always visible when ≥2 chapters exist)
├── Chapter (H2) × N
│     ├── optional H3 subheads (if payload sections provide)
│     ├── Body
│     ├── Callout? (key insight / caution — policy-safe)
│     └── References? (links to Knowledge / classical ids if present)
└── DocumentFooter (optional “see Knowledge for sources”)
```

### B.3 Chapter set (unchanged IDs)

`highlights`, `career`, `wealth`, `marriage`, `health`, `personality`, `advice`

### B.4 Components to add to map

| Component | Layer | Purpose |
|-----------|-------|---------|
| InterpretationDocument | Composite | Owns Tier 5 |
| InterpretationTOC | Composite | Jump list to chapters |
| InterpretationChapter | Composite | H2 + body |
| ReportCallout | Atomic | Insight/caution callout |
| ReportReferenceList | Atomic | Citation lines when present |

InterpretationSection may remain as implementation alias of InterpretationChapter.

### B.5 Must never hide

- TOC (if ≥2 available chapters)  
- Chapter titles even when body Unavailable  

### B.6 May hide / collapse

- Empty chapter bodies (show Unavailable inside chapter)  
- Reference lists when no citations  

---

## Addendum C — Knowledge traceability (closes G4, G5, G14)

### C.1 Evidence panel rows (normative)

Each row:

| Field | Required | Source |
|-------|----------|--------|
| `label` | Yes | Human-readable claim or category |
| `source_type` | Yes | `rule` \| `classical` \| `reasoning` \| `status` \| `unknown` |
| `reference` | When present | Book name, reasoning conclusion text — **not** raw CSV paths |
| `confidence` | When present | Number or label |
| `trace_id` | Optional internal | Hidden on consumer UI |

### C.2 Questions → UI answers

| Question | UI behavior |
|----------|-------------|
| Rule nào? | Show rule **display title** if provided; else Unavailable — never dump `FPR0123` to consumers |
| Engine nào? | **Hidden** on consumer Result; method note only if `show_method_notes` product flag (default off) |
| Sách nào? | Classical bibliography entries when API/payload provides; else Unavailable |
| Confidence? | Show discussion/validation confidence when present |
| Traceable? | Expert Sources pane + Evidence rows; Retry on failure |

### C.3 Priority / Knowledge status section (Tier 4)

Show only:

- `knowledge_expert` additive status fields present on analyze payload  
- Do not invent Priority Rule narratives without payload text  

If only boolean flags exist, render StatusBadge list — not a fake rules essay.

---

## Addendum D — Component layers (closes G6)

| Layer | Definition | Examples |
|-------|------------|----------|
| **Atomic** | No domain orchestration | Icon, StatusBadge, FieldError, ChartEmpty, ReportCallout, SummaryMetric |
| **Composite** | Combines atomics for one UI job | ExecutiveHero, PillarColumn, ElementRadar, AnalysisSection, InterpretationChapter, KnowledgeExpertPane |
| **Layout** | Page regions / chrome | ResultPage, ResultChrome, NavigationRail, ReportStream, ChartBand |
| **Business (presentation)** | Binds ResultStore/view-model — still **no engine logic** | ReportViewModelAdapter, ScrollSpyController |

**Forbidden overlap:** Layout components must not fetch APIs except page-level orchestration already owned by ResultPage (discussion ask stays inside KnowledgeExpertPane).

---

## Addendum E — Naming freeze (closes G7, C4)

| Use | Not |
|-----|-----|
| NavigationRail | NavRail |
| tier-executive | tier-summary |
| KnowledgeEvidencePanel | KnowledgeSidebar (unless PO renames) |
| FirstRecommendation | HeroAdvice (avoid) |

---

## Addendum F — Screen vs tier (closes G8)

| Product name | V1 implementation |
|--------------|-------------------|
| Dashboard / Analyze / Result / Reports / History / Profile / Login | Routes |
| Analysis / Interpretation / Knowledge Expert | **Anchored tiers inside Result** |

No new routes required for V1.

---

## Addendum G — Responsive matrix (closes G9)

| Band | Width | Result behavior |
|------|-------|-----------------|
| Desktop | ≥1280 | Sticky left rail; 4 pillars; 2×2 charts |
| Laptop | 1100–1279 | Same topology; slightly tighter padding; stream max-width may fill |
| Tablet | <1100 | Horizontal chip rail; pillars 2×2→1×4; charts stack |
| Mobile | — | Out of scope |

Secondary screens: single column forms/lists below 1100; tables may scroll horizontally in Reports.

---

## Addendum H — Payload binding index (closes G13)

**Superseded for implementation by** the complete [18_BINDING_INDEX.md](18_BINDING_INDEX.md).  
The conceptual table below was the V1.0 addendum sketch; UI sprints must use **18** only.

| UI slot | Payload path (conceptual) | If missing |
|---------|---------------------------|------------|
| Nhật Chủ | `bazi.day_master` / day pillar stem | Unavailable |
| Element / YY | day master meta / STEM_META display map | `--` |
| Thân | `pattern.than_vuong_nhuoc` etc. | Unavailable |
| Dụng/Hỷ/Kỵ | pattern / useful_god fields | Unavailable |
| Cách cục | pattern name | Unavailable |
| Quality | score.grade / total_score | Unavailable |
| Strengths/Weaknesses | score lists | `--` lists |
| FirstRecommendation | score.recommendations[0] or interp advice | Unavailable |
| Pillars | bazi pillars + nap_am/tang_can/thap_than/truong_sinh | `--` per cell |
| Element charts | pillar-derived counts or score series | ChartEmpty |
| Gauge | numeric strength_score only | text Thân label |
| Relations | pattern/bazi hop/xung/… | Unavailable rows |
| Shen Sha | bazi.shensha | Unavailable |
| Interpretation chapters | interpretation.sections mapped by id | Unavailable chapter |
| Knowledge status | data.knowledge_expert | Unavailable |
| Expert Q&A | POST discussion (existing) | ErrorPanel |

Exact key aliases stay in SummaryBuilder — UI must not invent new keys.

---

## Addendum I — Reports (closes G10)

Export/preview page-1 **should** follow Result spine order when composing documents.  
Reports Center wireframe minimum:

1. List pane  
2. Preview pane  
3. Actions: open / print / copy / download  
4. Empty state  

Detail styling deferred to Sprint 08 — topology above is enough to avoid guessing.

---

## Duplication cleanup (non-blocking)

Keep tier order only **owned** by HOME_RESULT_ARCHITECTURE; other docs reference it.  
No need to delete duplicates before V1.1 — low risk.

---

## Residual risk after addenda

| Risk | Mitigation |
|------|------------|
| Thresholds for quality bands | PO confirms 70/40 defaults or supplies table at Final PASS |
| Classical books empty in many payloads | Unavailable is success ([16](16_EMPTY_UNAVAILABLE_STATES.md)) |
| Prior Phase 2 code ≠ blueprint | Implementation Plan: Blueprint V1.1 is SSOT |

---

## Application status (V1.1 Final)

| Addendum | Status |
|----------|--------|
| A–I | **Applied** into 01–10 / 18 / 19 |
| J Visual Grammar | **Normative** — [15](15_VISUAL_GRAMMAR.md) |
| K Empty/Unavailable | **Normative** — [16](16_EMPTY_UNAVAILABLE_STATES.md) |
| L Localization | **Normative** — [17](17_LOCALIZATION_CONTRACT.md) |

---

## Version

`1.1.0`
