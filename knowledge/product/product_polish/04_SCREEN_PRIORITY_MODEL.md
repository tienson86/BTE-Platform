# 04 — Screen Priority Model

Version: 1.0.0  
Status: **OFFICIAL — Design Reference**  
Date: 2026-08-08  
Sprint: Product Polish V1 · Sprint A  

---

## 1. Purpose

Define **visual hierarchy bands** for the Result Page and map every existing card/surface into them.

Bands control emphasis only. They do **not** authorize new routes, zones, or Design System tokens.

---

## 2. Hierarchy bands

| Band | Name | Visual job | Reading weight |
|------|------|------------|----------------|
| **H0** | Hero | First conclusion the eye must catch | Maximum |
| **H1** | Primary | Main commercial advice & identity | High |
| **H2** | Secondary | Important but subordinate narrative | Medium |
| **H3** | Supporting | Proof, strength/risk detail | Medium–low |
| **H4** | Reference | Charts, tables, technical / knowledge depth | Lowest (on-demand) |

---

## 3. Band rules

| Rule | Detail |
|------|--------|
| One Hero | Executive Summary owns Hero; nothing else competes for first conclusion |
| One Primary commercial CTA surface | Primary Recommendation (Career Strategy) |
| Secondary never equals Primary | Promotion milestone = H2 |
| Reference cannot shout | Charts/tables: quieter type, optional collapse, no “dashboard” chrome |
| Frozen layout | Zone/row order per PACK_06 remains; bands are presentation priority inside rows |

---

## 4. Map — existing Result surfaces → bands

| Existing surface / card | PACK_06 home | Band | Notes |
|-------------------------|--------------|------|-------|
| Context / identity header | Row 01 Context | **H1** | Trust; compact |
| Executive Summary card | Row 02 Summary | **H0 Hero** | 1 central + ≤3 supporting + conclusion (Commercial V1 polish) |
| Day-master / profile identity lines (in Exec or Context) | Context / Summary | **H1** | Part of Who am I |
| Career Selection framing (labels / direction in existing slots) | Summary / Rec slots | **H1** | Named Capability |
| Primary Recommendation — Career Strategy | Row 05 Recommendations | **H1** | What/Why/How/When/Outcome |
| Secondary Recommendation — Promotion Readiness | Row 05 Recommendations | **H2** | Milestone under Career |
| Strength blocks | Analysis / Exec supporting | **H2–H3** | Prefer H2 if short |
| Challenge / risk / mitigation blocks | Analysis / Rec | **H2–H3** | Pair with strengths |
| Useful God / support-axis wording | Analysis / Knowledge | **H3** | Customer language |
| Core Analysis narrative cards | Row 03 Analysis | **H3** | Evidence of understanding |
| Chart / indicator cards | Row 04 Visualization | **H4 Reference** | After advice psychologically |
| Data tables / matrices | Visualization / Analysis | **H4** | Reference |
| Detailed Interpretation cards | Row 06 Interpretation | **H3–H4** | Progressive disclosure |
| Knowledge reference cards | Row 07 Knowledge | **H4** | Learn-more |
| Loading / empty / status gate | Status gate | **H1** (utility) | Clear, non-marketing |
| Footer | Footer | **H4** | Minimal |

Capabilities do **not** own dedicated zones; they project into Summary / Recommendation (and related) slots — bands apply to those projections.

---

## 5. First viewport composition (target experience)

Allowed in first viewport (ideal):

- Brand/context identity (compact)  
- Hero Executive Summary  
- Clear Career direction signal  
- Path toward Primary Recommendation (visible or one short scroll)  

Discouraged in first viewport:

- Dense chart grids  
- Multiple equal CTA blocks  
- Technical tables  
- Long Knowledge essays  

---

## 6. Success criteria

- Viewer can point to Hero and Primary in under 5 seconds.  
- Charts read as Reference, not Hero.  
- Promotion never visually equals Career Strategy.  

---

## 7. Stop line

Screen priority model defined. Implementation must obey bands without changing Foundation tokens or PACK_06 architecture.

---

END
