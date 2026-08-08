# 19 — Narrative Support Matrix

Version: 1.0  
Status: **SPRINT D — Knowledge Catalog Blueprint**  
Date: 2026-08-08  
Depends on: `16`, `18`, Sprint A `03`, Content Quality Release B  

---

## 1. Purpose

Map planned Knowledge Units to delivery surfaces:

```
Knowledge Unit
    ↓
Narrative Component
    ↓
Portal Zone
    ↓
Report Section
```

Identify **coverage gaps** (planned vs needed for commercial grade).

No implementation. Portal/Report zone names are logical (Foundation layouts frozen — not redesigned here).

---

## 2. Narrative component ← KU kind coverage

| Narrative component | Primary KU kinds | Planned P0 coverage | Gap today (content) |
|---------------------|------------------|---------------------|---------------------|
| Executive Summary | AN, AC, RK, OP | Strong plan (identity+action+risk+opp) | **Empty content** — G6 |
| Observation | AN | Strong plan | Empty content |
| Reasoning | AN (explanation) | Strong plan | Empty content |
| Impact | CN, OP, RK | Partial P0 + P1 | Empty; life CN mostly P1 |
| Recommendation | AC, PG, ST | Strong plan | Empty content |
| Warning | RK + MT | Strong plan (pairs) | Empty content |
| Conclusion | AN + AC | Strong plan | Empty content |
| NarrativeSummary slots | AN/AC/RK | Mapped via Exec pack | Empty content |

**Structural Narrative support (composer):** Ready.  
**Knowledge support:** Catalog planned; **0 Published units**.

---

## 3. KU family → Narrative / Portal / Report

| KU family (examples) | Narrative components | Portal zone (logical) | Report section (logical) |
|----------------------|----------------------|------------------------|---------------------------|
| AN-ID-* identity | Exec, Observation, Conclusion | Hero / Executive zone | Executive briefing |
| AN-*-explanation | Reasoning | Analysis explain / Insight | Reasoning / analysis notes |
| AN-XX observation pack | Observation | Chart/structure context | Observations |
| CN-* implications | Impact, Exec framing | Impact / life theme cards | Life impact chapters |
| AC-DM / AC-* actions | Recommendation, Exec, Conclusion | CTA / Recommendation zone | Recommendations |
| PG-* practical | Recommendation | Guidance / lifestyle | Practical guidance |
| RK-* risks | Warning, Exec | Warning / caution zone | Cautions |
| MT-* mitigations | Warning, Recommendation | Warning (paired) | Mitigations |
| OP-* opportunities | Exec, Recommendation, Impact | Opportunity highlight | Opportunities |
| ST-* strategy | Conclusion, Recommendation | Long-horizon / growth | Strategy outlook |
| CN-XX / AN-XX Knowledge Panel | — (not Pack 05 section) | Knowledge / glossary zone | Appendix / glossary |
| AC-DM-000006 insufficient honesty | Any underfilled slot | Insufficient state | Insufficient notice |

---

## 4. Portal zone coverage matrix

| Portal zone (logical) | Required KU support | Catalog status | Gap |
|-----------------------|---------------------|----------------|-----|
| Executive / Hero briefing | AN-ID + AC-DM + RK/OP as applicable | P0 planned | Content gap |
| Observation / structure | AN-XX-000001, AN-ID | P0 planned | Content gap |
| Reasoning / insight | AN-ID-000005…000007, AN-XX-000002/3 | P0 planned | Content gap |
| Impact / life themes | CN-* | P0 thin; P1 heavy | Phase 2 content |
| Recommendations | AC-*, PG-* | P0/P1 planned | Content gap |
| Warnings | RK+MT pairs | P0/P1 planned | Content gap |
| Conclusion | AN-ID-000008, AC-DM-000007 | P0 planned | Content gap |
| Knowledge / glossary | CN-XX-000002, AN-XX-000007 | P2 planned | Deferred |
| Timeline / luck | CN-LU-*, AC-LU-*, OP-LU-* | P0/P1 planned | Content gap |

---

## 5. Report section coverage matrix

| Report section (logical) | KU support | Notes |
|--------------------------|------------|-------|
| Cover / Exec summary | Same as Exec Narrative | Must consume NarrativeResult, not new KU scrape |
| Analysis explanation | AN explanation units | |
| Life chapters (career/finance/…) | CN/AC/RK/MT per scenario | Phase 2+ |
| Recommendations appendix | AC/PG/ST | |
| Risks & mitigations | RK+MT | |
| Timing / luck chapter | CN/AC/OP/RK LU | |
| Glossary | Knowledge Panel KUs | P2 |
| Disclaimers | ethics-flagged units + product legal | Not KU-duplicated legal text |

**Gap:** Report Engine redesign is a separate epic; catalog assumes Report reads **NarrativeResult** backed by same KUs.

---

## 6. Coverage gap register

| ID | Gap | Severity | Closes when |
|----|-----|----------|-------------|
| GAP-N1 | Zero Published KUs → live `partial_insufficient` | Critical | Phase 1 publish P0 |
| GAP-N2 | Impact thin if only P0 structural CN | High | Phase 2 CN life units |
| GAP-N3 | Sensitive Warning/Rec ethics packs absent until P2 | High for those scenarios | Phase 3 |
| GAP-N4 | Knowledge Panel KUs deferred P2 | Medium | Phase 3 |
| GAP-N5 | Shensha depth optional | Medium | Phase 2 curated set |
| GAP-N6 | Portal zone still may bind chart facts (G5) without KU prose | Low/by design | Optional polish |
| GAP-N7 | Report not yet NarrativeResult consumer | High for print | Report epic |
| GAP-N8 | Transformation / Na Yin narrative L priority | Low | Future |

---

## 7. Minimum Narrative commercial pack (definition)

Default Result Page is Narratively supported when these Planned KUs are **Published**:

1. KU-AN-ID-000001…000003, 000005…000008  
2. KU-AN-XX-000001  
3. KU-AC-DM-000001…000007  
4. KU-PG-XX-000001  
5. KU-RK/MT-XX-000001…000004  
6. KU-OP-LU-000001; KU-CN-LU-000001; KU-AC-LU-000001  
7. KU-CN-XX-000001; KU-CN-CA-000001; KU-AC-CA-000001  

This is the **Phase 1 exit pack** (see `20`).

---

## 8. Stop line

Narrative support matrix complete. Gaps are content/report epics — not catalog defects.

---

END
