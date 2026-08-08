# 07 — Call to Action Strategy

Version: 1.0.0  
Status: **OFFICIAL — Design Reference**  
Date: 2026-08-08  
Sprint: Product Polish V1 · Sprint A  

---

## 1. Purpose

Define CTA strategy for the commercial Result experience **without changing Portal routes** or inventing new screens.

CTAs steer attention and conversion *inside* the existing Result Page composition.

---

## 2. CTA tiers

| Tier | Role | Count |
|------|------|-------|
| **Primary CTA** | Drive the main commercial action for this session | **Exactly one** per Result view |
| **Secondary CTA** | Support milestone / deepen plan | ≤2 visible |
| **Tertiary / disclosure** | Expand detail, learn more | As needed, quiet |

---

## 3. Primary CTA

| Field | Definition |
|-------|------------|
| **Anchors to** | Career Strategy / primary Recommendation (CAP-CAREER-SEL-001) |
| **Customer job** | Accept and begin the career direction plan |
| **Label intent** | Action on the plan (e.g. focus / save / continue with career plan — use existing product verbs only) |
| **Placement** | Recommendation zone · adjacent to What/How |
| **Must not** | Jump to a new Capability route; open Marketing landing; outrank Exec content with chrome |

Primary CTA answers: **“Start acting on my career direction.”**

---

## 4. Secondary CTA

| Field | Definition |
|-------|------------|
| **Anchors to** | Promotion Readiness milestone (CAP-CAREER-PRO-001) |
| **Customer job** | Inspect readiness / 90-day promotion detail |
| **Label intent** | Explore promotion milestone (expand or in-page emphasis) |
| **Placement** | Secondary Rec block |
| **Must not** | Equal visual weight to Primary; replace Career as session goal |

Secondary CTA answers: **“Check my promotion readiness next.”**

---

## 5. Progressive disclosure CTAs

| Trigger | Behavior | Route change? |
|---------|----------|---------------|
| Long How / 90-day detail | Expand in place | No |
| Interpretation depth | Expand section | No |
| Chart metrics table | Expand / show table | No |
| Knowledge teaser | Expand KU text | No |
| Technical details | Collapse by default | No |

Disclosure CTAs are **Tertiary** — text-button / quiet control patterns from Design System only.

---

## 6. Commercial upsell locations (no new routes)

Upsell = invite deeper commercial value **inside** Result, not a new Portal page.

| Location | Upsell intent | Mechanism |
|----------|---------------|-----------|
| After Primary Rec | Reinforce Career plan commitment | Primary CTA |
| Secondary Rec block | Promotion as natural next milestone | Secondary CTA + short value line |
| End of Exec conclusion | “Next: action plan below” | In-page affordance / scroll cue |
| After Actions beat | Optional deepen Promotion | Secondary only |
| Knowledge teaser | Education, not hard sell | Tertiary expand |
| Footer | Soft revisit / consult continuity (copy only) | No new route |

**Forbidden upsell patterns:** new nav items, new Result URLs, modal funnels that bypass Result architecture, chip storms, multi-offer galleries.

---

## 7. CTA vs Capability rule

```
Primary CTA  →  CAP-CAREER-SEL-001 (Career Strategy)
Secondary CTA → CAP-CAREER-PRO-001 (Promotion milestone)
```

Leadership and later Capabilities: **no CTA** until Product approves them into a Commercial train.

---

## 8. Success criteria

- One unmistakable Primary CTA.  
- Promotion CTA visibly secondary.  
- Zero new Portal routes introduced for polish.  
- Progressive disclosure covers density without losing content.  

---

## 9. Stop line

CTA strategy fixed for Product Polish V1. Implementation must stay route-stable.

---

END
