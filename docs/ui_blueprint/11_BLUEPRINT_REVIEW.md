# 11 — BLUEPRINT REVIEW (Final Freeze V1.0 — historical)

| Field | Value |
|-------|--------|
| **Document** | `11_BLUEPRINT_REVIEW.md` |
| **Reviewer role** | Product Architect (not Frontend Developer) |
| **Pack reviewed** | `docs/ui_blueprint/` v1.0.0 (docs 00–10) |
| **Date** | 2026-08-02 |
| **Frontend code** | **Not modified** (review-only sprint) |
| **Superseded by** | Blueprint **V1.1.0 Final Freeze** — [19_BLUEPRINT_V1_1_FINAL_FREEZE.md](19_BLUEPRINT_V1_1_FINAL_FREEZE.md) |

---

## Executive verdict (V1.0)

| Verdict | Meaning |
|---------|---------|
| **CONDITIONAL PASS** (V1.0) | Core Information Architecture (6-tier spine, no tabs, rail + scroll-spy, Insight First) is **internally consistent** and implementable for the Result shell. |
| **Not Final PASS yet** (V1.0) | Several product requirements were **underspecified**. Gaps closed in V1.1 via Addenda A–L + Binding Index. |

**V1.1 status:** Addenda applied → pack ready for PO Final PASS via [14_ACCEPTANCE_CRITERIA.md](14_ACCEPTANCE_CRITERIA.md). This review document is retained as audit trail only.

---

## 1. Cross-document consistency

### 1.1 Contradictions

| ID | Finding | Severity | Resolution |
|----|---------|----------|------------|
| C1 | None on **tier order** — Architecture, Wireframe, Reading Flow, Navigation, Principles, Implementation Plan all agree: Executive → Bazi → Charts → Analysis → Interpretation → Knowledge | — | Keep as SSOT |
| C2 | None on **no primary tabs** — Navigation, Architecture, Principles, Reading Flow anti-patterns align | — | Keep |
| C3 | Soft naming drift: rail label “Tóm tắt” vs Architecture “Tóm tắt điều hành” vs Wireframe “EXECUTIVE SUMMARY” | Low | Freeze label: VI `Tóm tắt` (rail) / eyebrow `Tóm tắt điều hành` / EN internal `Executive` |
| C4 | Mermaid uses `NavRail`; COMPONENT_MAP uses `NavigationRail` | Low | Canonical name: **NavigationRail** |
| C5 | SCREEN_BLUEPRINT treats Analysis / Interpretation / Knowledge as “screens” while Architecture says they are **tiers of Result** | Medium (confusion) | Normative: they are **Result tiers**, not peer routes in V1 |
| C6 | Hero summary sentence vs “first recommendation” — Reading Flow Moment 1 does **not** require a recommendation; Executive Review in this sprint does | **High** | See Addendum A (Hero) in Gap Analysis |

### 1.2 Section name consistency (freeze table)

| Tier ID | Canonical VI | Canonical EN | Allowed aliases |
|---------|--------------|--------------|-----------------|
| `tier-executive` | Tóm tắt | Executive | Tóm tắt điều hành (eyebrow only) |
| `tier-bazi` | Bát Tự | Four Pillars | — |
| `tier-charts` | Biểu đồ | Charts | — |
| `tier-analysis` | Phân tích | Analysis | — |
| `tier-interpretation` | Luận giải | Interpretation | — |
| `tier-knowledge` | Kiến thức | Knowledge | Classical Knowledge (subtitle only) |

### 1.3 Component name consistency

| Canonical | Do not use |
|-----------|------------|
| NavigationRail | NavRail |
| KnowledgeEvidencePanel | KnowledgeSidebar (unless redefined as alias) |
| ReportStream | ReportBody / MainColumn (informal only) |
| ExecutiveHero | HeroCard / SummaryHero |

Full taxonomy: see Gap Analysis § Component layers.

### 1.4 Reading Flow ↔ Wireframe

| Moment | Wireframe region | Match? |
|--------|------------------|--------|
| 0 Empty/Skeleton | Global frame | Yes |
| 1 Hero | Tier 1 | Yes |
| 2 Pillars | Tier 2 | Yes |
| 3 Charts | Tier 3 | Yes |
| 4 Analysis | Tier 4 | Yes |
| 5 Interpretation | Tier 5 | Yes |
| 6 Knowledge | Tier 6 | Yes |

**Pass** for spine alignment.

### 1.5 Wireframe ↔ Architecture

Pillar fields, chart set, analysis section list, interpretation chapters, knowledge panes — **aligned**.  
Gap: Architecture L1 does not list **first recommendation**; Wireframe Hero also omits it.

### 1.6 Navigation ↔ Reading Flow

Rail order matches Moments 1–6. Scroll-spy + anchors support “no guessing.” **Pass.**

### 1.7 Implementation Plan ↔ Blueprint

Sprints 01–06 map cleanly to tiers; 07 visual; 08 secondary; 09 harden. **Pass** on sequencing.  
Gaps: Sprint 02/05/06 exit criteria must absorb Addenda A–C before coding.

### 1.8 Duplication

| Duplicated | Assessment |
|------------|------------|
| Tier order repeated in 6+ docs | Acceptable reinforcement; Architecture owns order |
| Unavailable policy repeated | Acceptable; Architecture owns policy |
| Analysis described as screen + tier | Needs C5 clarification (not content duplication) |

### 1.9 Missing elements (summary)

See [12_GAP_ANALYSIS.md](12_GAP_ANALYSIS.md). Top missing:

1. Hero first recommendation + quality verdict framing  
2. Interpretation document model (TOC, H1/H2, callout, citation)  
3. Knowledge traceability field matrix (rule / classical / confidence / engine display policy)  
4. Atomic/Composite/Layout/Business component layers  
5. Explicit Desktop / Laptop / Tablet matrices for non-Result screens  

### 1.10 Guesswork risk if coding now

| Area | Would developer guess? |
|------|------------------------|
| Tier order / no tabs | No |
| Hero metrics list | Partially — recommendation missing |
| Interpretation layout | **Yes** — cards vs document |
| Knowledge evidence binding | **Yes** — which JSON fields |
| Collapse defaults | Partially specified (primary four expanded) |
| Laptop vs desktop breakpoints | Partially — only tablet ~1100px |

---

## 2. Product review — per screen

### 2.1 Dashboard

| Question | Blueprint answer | Gap? |
|----------|------------------|------|
| Open to do what? | Orient, resume, start analyze | No |
| Most important? | CTA Analyze + recent charts | No |
| See first? | Greeting + quick actions | No |
| See next? | Recent → stats/health secondary | No |
| May hide? | Dense health detail | Underspecified wireframe |
| Must never hide? | Primary CTA Analyze; path to open Result | Should state explicitly |

### 2.2 Result

| Question | Blueprint answer | Gap? |
|----------|------------------|------|
| Open to do what? | Read professional analysis report | No |
| Most important? | Executive Hero | No |
| See first? | Nhật Chủ + core metrics + sentence | Recommendation missing |
| See next? | Pillars → Charts → Analysis → Interpretation → Knowledge | No |
| May hide? | Relations, Shen Sha, empty chapters, narrative fallback | No |
| Must never hide? | Hero identity facts when present; Unavailable honesty; tier spine | Add “first recommendation” when present |

### 2.3 Analysis (Result Tier 4)

| Question | Blueprint answer | Gap? |
|----------|------------------|------|
| Open to do what? | Understand thematic structure | No |
| Most important? | Ngũ hành, Thập thần, Cách cục, Dụng/Hỷ/Kỵ | No |
| See first? | Those four (expanded) | No |
| See next? | Relations, Shen Sha, Knowledge status | No |
| May hide? | Secondary sections collapsed | No |
| Must never hide? | Section titles in spine; Unavailable for missing relations | No |

### 2.4 Interpretation (Result Tier 5)

| Question | Blueprint answer | Gap? |
|----------|------------------|------|
| Open to do what? | Read domain guidance | No |
| Most important? | Highlights + advice | Partial |
| See first? | Điểm nổi bật | No |
| See next? | Domains → Lời khuyên | No |
| May hide? | Empty domain bodies | No |
| Must never hide? | Chapter list / TOC | **Yes — TOC/document model missing** |

### 2.5 Knowledge Expert (Result Tier 6)

| Question | Blueprint answer | Gap? |
|----------|------------------|------|
| Open to do what? | Trace trust + ask grounded questions | No |
| Most important? | Evidence + confidence + answer | Field matrix weak |
| See first? | Sources/status panel | No |
| See next? | Expert 3-pane | No |
| May hide? | Narrative fallback | No |
| Must never hide? | Error/Retry; no fake citations | No |

### 2.6 Report (Reports Center)

| Question | Blueprint answer | Gap? |
|----------|------------------|------|
| Open to do what? | Preview/export archive | No |
| Most important? | Selected preview | Wireframe thin |
| See first? | List + preview | Underspecified |
| See next? | Export actions | Underspecified |
| May hide? | PDF tab if unavailable | Implicit |
| Must never hide? | Empty state; no conflicting IA | Should freeze export page-1 = Result spine |

---

## 3. Executive (Hero) review

| Question | Covered in V1.0? | Required addendum |
|----------|------------------|-------------------|
| Lá số tốt hay không? | Partial via Quality metric only | **QualityVerdictCaption** — short calm band from grade/score/confidence; never fear language |
| Nhật Chủ là gì? | Yes | — |
| Thân thế nào? | Yes | — |
| Dụng thần là gì? | Yes (+ Hỷ/Kỵ) | — |
| Điểm mạnh? | Yes if payload | — |
| Điểm yếu? | Yes if payload | — |
| Khuyến nghị đầu tiên? | **No** | **FirstRecommendation** — first item of recommendations / conclusion chapter / score.recommendations[0]; else Unavailable |

Without FirstRecommendation + QualityVerdictCaption, Hero fails the Executive Review bar of this sprint.

---

## 4. Knowledge review

| Question | V1.0 answer | Gap |
|----------|-------------|-----|
| Rule nào? | Mentioned generically | Need display policy: show human labels; hide raw rule ids on consumer tier |
| Engine nào? | Not specified | **Do not show engine class names** to end users (aligns with commercial copy); optional Expert/Appendix “method note” only if product enables |
| Sách nào? | Classical citation if payload | Bind only when citation package / bibliography present |
| Confidence? | Yes (panel + expert) | Normalize 0–1 vs label |
| Traceable? | Intent yes | Need explicit EvidenceRow model: claim → source type → ref → confidence |

---

## 5. Interpretation review

V1.0 = **stack of chapter cards**.  
This sprint requires **document organization**:

| Element | V1.0 | Required |
|---------|------|----------|
| Mục lục (TOC) | Optional mention in NAV only | **Required** InterpretationTOC |
| Heading / Subheading | Chapter title only | Document outline H2 chapters / H3 optional |
| Callout | Missing | Callout for warnings / key insight (policy-safe) |
| Citation / Reference | Missing in Tier 5 | Footrefs or “see Knowledge” links — no orphan claims |

Treat Interpretation as **one report document** composed of chapters — not a dashboard of unrelated cards.

---

## 6. Component review (layers)

V1.0 lists components but **does not classify** Atomic / Composite / Layout / Business.

Normative classification is frozen in Gap Analysis §4. Overlap risks flagged:

| Risk | Notes |
|------|-------|
| SummaryMetric vs MetricCard | MetricCard = dashboard; SummaryMetric = hero-only accents |
| AnalysisSection vs InterpretationSection | Same shell pattern, different content contracts — keep separate |
| KnowledgeStatusPanel vs KnowledgeEvidencePanel | Status = analyze additive blob; Evidence = discussion/citation rows |

---

## 7. Responsive review

| Viewport | Specified? |
|----------|------------|
| Desktop ≥1280 | Yes (rail sticky, proportions) |
| Laptop | Implicit same as desktop | Need explicit 1100–1280 behavior |
| Tablet <~1100 | Yes (chip rail, 2×2 pillars) |
| Mobile | Out of scope — correct |

Non-Result screens lack responsive notes — Gap.

---

## 8. Alignment with UX Principles

| Principle | Blueprint support |
|-----------|-------------------|
| Insight First | Strong (minus first recommendation) |
| Facts before Narrative | Strong |
| Never overload | Strong |
| Executive first | Strong |
| Progressive Disclosure | Strong |
| Explain before Details | Medium (Analysis explain copy underspecified) |
| Evidence for conclusions | Medium (needs Knowledge/Interpretation addenda) |
| Knowledge traceable | Medium |
| Charts support narrative | Strong |
| Readable without training | Strong if rail labels frozen |

---

## 9. Review conclusion

| Gate | Status |
|------|--------|
| No major IA contradictions on spine | **PASS** |
| Enough to code shell + pillars + charts without guessing | **PASS** |
| Enough to code Hero / Interpretation / Knowledge to product bar of this review | **FAIL until Addenda A–C accepted** |
| Frontend unchanged this sprint | **PASS** |

**Recommendation to Product Owner:** Approve Blueprint V1.0 **plus** Gap Analysis Addenda as **V1.1 freeze**, then unlock UI Sprint 01.

---

## Cross references

- [12_GAP_ANALYSIS.md](12_GAP_ANALYSIS.md)  
- [13_IMPLEMENTATION_CHECKLIST.md](13_IMPLEMENTATION_CHECKLIST.md)  
- [14_ACCEPTANCE_CRITERIA.md](14_ACCEPTANCE_CRITERIA.md)  
- Docs 01–10  

---

## Version

`1.0.0` — Blueprint Review Sprint
