# 05 — Content Density Guide

Version: 1.0.0  
Status: **OFFICIAL — Design Reference**  
Date: 2026-08-08  
Sprint: Product Polish V1 · Sprint A  

---

## 1. Purpose

Control **how much** content appears at each hierarchy band so the Result feels like consulting, not a scroll of paragraphs.

This guide constrains presentation density. It does **not** invent typography scales or spacing tokens — use Design System values as frozen.

---

## 2. Density by band

| Band | Max visible paragraphs (default) | Bullet preference | Expand? |
|------|----------------------------------|-------------------|---------|
| Hero (Exec) | 1 central + ≤3 supporting + 1 close | Short clauses OK | No for core; optional “more” only for overflow |
| Primary (Rec / Career) | What/Why/How/When/Outcome — one block each | Prefer bullets for How | Soft expand for long How |
| Secondary | ≤3 short paragraphs or ≤5 bullets | Bullets preferred | Yes |
| Supporting | ≤2 short paragraphs per card | Bullets for lists | Yes |
| Reference | Minimal teaser + expand/collapse | Tables OK when collapsed by default where possible | **Yes — default collapsed or quiet** |

---

## 3. Paragraph length

| Surface | Soft max (Vietnamese / EN mixed) | Hard stop guidance |
|---------|----------------------------------|--------------------|
| Hero central line | ~40–60 words | Split if longer |
| Supporting Exec lines | ~25–40 words each | Drop lowest-value line |
| Recommendation What | ~30–50 words | One sentence preferred |
| Why / When / Outcome | ~20–40 words each | No essays |
| How | ≤5 action bullets · ≤15 words/bullet | Extra → expandable “90-day detail” |
| Analysis / Interpretation body | ≤80 words visible | Remainder expandable |
| Knowledge units on Result | Teaser ≤50 words | Full text via expand / reference pattern |

Word counts are **product density targets**, not Engine truncation rules.

---

## 4. Bullet rules

1. Use bullets for **actions**, **gaps**, **risks**, **steps**.  
2. Do not bullet a single philosophical sentence — use prose.  
3. Max **5** bullets visible without expand on Primary/Secondary.  
4. Each bullet = **one** action or fact.  
5. No nested bullets on Hero / Primary.  

---

## 5. Whitespace

| Principle | Application |
|-----------|-------------|
| One job per card | Extra space between cards > cramped multi-topic cards |
| Separate beats | Breathing room between Who am I → Strengths → Actions |
| Quiet Reference | More margin above charts so they feel “below the advice” |
| No fake density | Do not fill whitespace with decorative chips or stat strips |

Spacing values: **Design System only** (frozen). This guide sets *intent*, not new px.

---

## 6. Typography intent (no new scale)

| Band | Intent using existing DS roles |
|------|--------------------------------|
| Hero | Highest emphasis text role available for summary |
| Primary | Strong heading + readable body |
| Secondary | Clear but quieter than Primary |
| Supporting | Body / secondary body |
| Reference | Smallest comfortable analytical text; labels muted |

Do not invent font families, sizes, or weights outside Design System.

---

## 7. Expandable sections

| Candidate | Default | Expand label intent |
|-----------|---------|---------------------|
| Long How / 90-day plan detail | Teaser + expand | “Xem kế hoạch 90 ngày” / equivalent |
| Detailed Interpretation | Collapsed or teaser | “Xem luận giải chi tiết” |
| Charts deep metrics | Visible chart simple; table collapsed if heavy | “Xem bảng chỉ số” |
| Knowledge deep KU | Teaser | “Tìm hiểu thêm” |
| Technical dump | Collapsed | “Chi tiết kỹ thuật” |

Expandables realize Priority 3 demotion **without** removing content or changing routes.

---

## 8. Redundancy control

| Symptom | Remedy |
|---------|--------|
| Same Useful God motif 4× | Show once in Supporting; reference elsewhere |
| Exec repeats full Rec | Exec = conclusion; Rec = actions |
| SEL + PRO both narrate full plans | Primary plan = Career; Promotion = milestone summary |

---

## 9. Success criteria

- First viewport is readable in ≤30 seconds.  
- No Hero paragraph exceeds soft max without split.  
- Reference content defaults to quieter / expandable where dense.  

---

## 10. Stop line

Content density guide fixed for Product Polish V1. Implementation phases apply this guide without Foundation edits.

---

END
