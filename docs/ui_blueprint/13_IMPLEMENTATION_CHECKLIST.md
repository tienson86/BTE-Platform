# 13 — IMPLEMENTATION CHECKLIST

| Field | Value |
|-------|--------|
| **Document** | `13_IMPLEMENTATION_CHECKLIST.md` |
| **Version** | `1.1.0` |
| **Use** | Gate UI sprints after PO signs Blueprint V1.1 Final Freeze |
| **Code** | None in Blueprint milestone |

---

## Pre-flight (PO / Architect)

- [ ] Docs 01–10 reviewed at V1.1  
- [ ] [11_BLUEPRINT_REVIEW.md](11_BLUEPRINT_REVIEW.md) read (historical)  
- [ ] [12_GAP_ANALYSIS.md](12_GAP_ANALYSIS.md) Addenda A–I **applied**  
- [ ] Addenda J–L accepted ([15](15_VISUAL_GRAMMAR.md)–[17](17_LOCALIZATION_CONTRACT.md))  
- [ ] [18_BINDING_INDEX.md](18_BINDING_INDEX.md) accepted as sole slot map  
- [ ] [19_BLUEPRINT_V1_1_FINAL_FREEZE.md](19_BLUEPRINT_V1_1_FINAL_FREEZE.md) acknowledged  
- [ ] [14_ACCEPTANCE_CRITERIA.md](14_ACCEPTANCE_CRITERIA.md) signed  
- [ ] Explicit written approval: “UI Sprint 01 unlocked”  
- [ ] Confirm: no frontend work until unlock  
- [ ] Confirm: UI sprints must not change IA / Nav / Reading Flow / Component Hierarchy / Design Language  

---

## Global constraints (every sprint)

- [ ] No engines / API / database / business-rule changes  
- [ ] No primary tier tabs  
- [ ] No inventing missing BaZi fields  
- [ ] Bindings only from [18](18_BINDING_INDEX.md)  
- [ ] Unavailable / Empty per [16](16_EMPTY_UNAVAILABLE_STATES.md)  
- [ ] i18n keys/rules per [17](17_LOCALIZATION_CONTRACT.md)  
- [ ] Visual polish inside [15](15_VISUAL_GRAMMAR.md)  
- [ ] Desktop / Laptop / Tablet only  
- [ ] Blueprint V1.1 is SSOT over any prior Phase 2/3 UI  

---

## UI Sprint 01 — Shell

- [ ] ResultPage = Chrome + NavigationRail + ReportStream  
- [ ] Anchors: `tier-executive` … `tier-knowledge`  
- [ ] Scroll spy + smooth jump  
- [ ] Reading progress (rail steps or top bar)  
- [ ] Skeleton then empty-or-stream  
- [ ] Deep link hash works  
- [ ] Naming: NavigationRail (not NavRail)  

---

## UI Sprint 02 — Hero + Pillars (+ Addendum A)

- [ ] DayMasterDisplay largest  
- [ ] QualityVerdictCaption per Addendum A  
- [ ] Metrics: Thân, Dụng, Hỷ, Kỵ, Cách Cục, Quality  
- [ ] Strengths / Weaknesses from score only  
- [ ] **FirstRecommendation** callout or Unavailable  
- [ ] Summary sentence facts-only  
- [ ] PillarGrid 4 columns; Day highlighted  
- [ ] Cells: Can, Chi, Tàng Can, Thập Thần, Trường Sinh, Nạp Âm  
- [ ] Accents only on allowed tokens  

---

## UI Sprint 03 — Charts

- [ ] ElementRadar / StrengthGauge / DistributionBars / TenGodBars  
- [ ] Gauge only if numeric score; else text fallback  
- [ ] ChartEmpty when series missing  
- [ ] Charts below Hero/Pillars in scroll order  

---

## UI Sprint 04 — Analysis

- [ ] Large sections only (no mini-card carpet)  
- [ ] Order: Ngũ hành → Thập thần → Cách cục → Dụng/Hỷ/Kỵ → Relations → Thần sát → Knowledge status  
- [ ] Primary four default expanded (or first two on short viewports)  
- [ ] Relations Unavailable per missing field  
- [ ] Priority/Knowledge status = payload only (Addendum C.3)  

---

## UI Sprint 05 — Interpretation (+ Addendum B)

- [ ] InterpretationDocument wrapper  
- [ ] InterpretationTOC when ≥2 chapters available  
- [ ] Chapters as H2 document sections (not peer dashboard cards)  
- [ ] Callout component available for key insight/caution  
- [ ] Reference hooks when citations exist  
- [ ] Empty chapter → Unavailable inside chapter; title visible  

---

## UI Sprint 06 — Knowledge (+ Addendum C)

- [ ] KnowledgeEvidencePanel with EvidenceRow fields  
- [ ] No consumer-facing engine class names (default)  
- [ ] No fake classical books  
- [ ] Expert 3-pane; existing discussion API only  
- [ ] ErrorPanel + Retry + request id when available  
- [ ] Narrative fallback collapsed  
- [ ] Tier remains last in spine  

---

## UI Sprint 07 — Visual language

- [ ] Type tokens: display/title/subtitle/body/metric/caption/eyebrow  
- [ ] VH1 dominates mass  
- [ ] Neutrals dominate; accent scarcity  
- [ ] Elevation / grid / motion per Visual Grammar J  
- [ ] Motion: short, non-noisy  
- [ ] Pass Design Language QA questions  

---

## UI Sprint 08 — Secondary screens

- [ ] Dashboard: CTA Analyze never hidden; recent → Result  
- [ ] Analyze: grouped sections order frozen  
- [ ] Reports: list + preview + actions (Addendum I); export order aligns Result spine  
- [ ] History/Profile/Login: design-language consistent  
- [ ] Responsive matrix Addendum G applied  
- [ ] Empty states per Addendum K  

---

## UI Sprint 09 — Harden

- [ ] Portal pytest module green  
- [ ] Preview snapshots under docs/reports  
- [ ] a11y: headings, focus, rail keyboard  
- [ ] Localization spot-check per Addendum L  
- [ ] Diff freeze: no engines/api/db  
- [ ] Stranger test: read Result without training  
- [ ] Acceptance criteria doc all checked  

---

## Definition of Done (per sprint)

- [ ] Matches checklist items for that sprint  
- [ ] No new product guesses outside frozen Blueprint V1.1  
- [ ] Demo against USER_READING_FLOW moments  
- [ ] PO or Architect sign-off on sprint exit criteria  

---

## Version

`1.1.0`
