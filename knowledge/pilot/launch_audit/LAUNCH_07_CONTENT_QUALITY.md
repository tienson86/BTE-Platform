# LAUNCH-07 — Real Chart Content Quality & Readability

**Task:** BTE LAUNCH-07  
**Date:** 2026-08-12  
**Scope:** Portal presentation only — no engine, pipeline, API, Knowledge, or interpretation changes  

**Evidence base:** LAUNCH-04 live capture  
`applications/customer_portal/src/features/portal/fixtures/launch_04_real_chart_response.json`  
Subject: **Nguyen Tien Son** · Pillars: Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần  

---

## 1. Executive Summary

LAUNCH-07 improves **readability and trust** of the live Result V2 page without rewriting interpretation meaning.

| Area | Outcome |
|------|---------|
| Accidental Portal truncation | **No CSS line-clamp / text-overflow ellipsis** on narrative; full section prose is visible when Knowledge is open |
| Seven narrative sections | Ordered, titled, fully readable as separate cards/paragraphs |
| Portal duplication | Career no longer remounts all seven sections; primary recommendation no longer doubles as a domain card |
| Upstream ellipsis / recycled commercial strings | **Left unchanged** (`UPSTREAM_CONTENT_ISSUE`) |
| Hierarchy | Chart summary → recommendations → narrative → career → technical (collapsed) |
| Live vs demo | `data-analysis-source="api"` preserved; demo path intact |

**Classification reminder**

- **FIXED_IN_PORTAL** — presentation/composition/CSS/adapter mapping in `applications/customer_portal/**`
- **UPSTREAM_CONTENT_ISSUE** — payload already truncated or duplicated before Portal

---

## 2. Truncation Findings

| Location | Mechanism | Classification | Action |
|----------|-----------|----------------|--------|
| `commercial_executive_summary.*`, `summary.identity`, `primary_recommendation.what/why/how`, supporting points | Source strings already end with `…` in live API capture | **UPSTREAM_CONTENT_ISSUE** | Document only — do not rewrite |
| Result V2 CSS | No `-webkit-line-clamp` / `text-overflow: ellipsis` on narrative/recommendation body | N/A (no Portal clip) | Keep |
| Knowledge body (pre-fix) | Single `<p>{body}</p>` with `\n\n` not rendered as paragraphs; teaser + expanded body could duplicate first paragraph | **FIXED_IN_PORTAL** | Split paragraphs; show full body when section open |
| Summary bullets | Cap of 5 (scannable summary contract) | Intentional compact summary | Keep; full narrative lives in seven sections |
| Technical panel | Collapsed by default (secondary) | Intentional hierarchy | Full content via “Xem chi tiết kỹ thuật” |

**P0 result:** Meaningful Pack-05 section text for this chart contains **no** `…` and is fully readable in Result V2 Knowledge.

---

## 3. Narrative Readability

| Change | Type |
|--------|------|
| Knowledge section open by default | FIXED_IN_PORTAL |
| Eager Knowledge mount (no Suspense blank) | FIXED_IN_PORTAL |
| Paragraph spacing / measure via existing tokens | FIXED_IN_PORTAL |
| Hero remains chart-fact concise (LAUNCH-06) | KEEP |
| Long-form stays out of Hero | KEEP |

Summary vs full narrative:

- **SUMMARY:** ≤5 bullets led by chart fundamentals  
- **FULL NARRATIVE:** seven Knowledge cards with complete section text  

---

## 4. Seven-Section Validation

Source order preserved and verified in tests:

1. Tóm tắt điều hành  
2. Quan sát  
3. Lý giải  
4. Tác động  
5. Khuyến nghị  
6. Lưu ý  
7. Kết luận  

| Check | Status |
|-------|--------|
| Titles visible | PASS |
| Ordering preserved | PASS |
| Content equals source paragraph text | PASS |
| No Portal clipping of section body | PASS |
| Paragraph separation for multi-block prose | PASS (`splitProseParagraphs`) |

---

## 5. Duplicate / Repeated Content Findings

| Finding | Class | Action |
|---------|-------|--------|
| Career `analysis_detail` previously dumped all seven Knowledge sections | **B — Presentation duplication** | **FIXED_IN_PORTAL** — career uses Career Selection Assessment fields only |
| Primary recommendation card also auto-injected into domain via empty `recommendation_ids` fallback | **B — Presentation duplication** | **FIXED_IN_PORTAL** — explicit `[]` respected in `mapDomains` |
| Teaser + full body both showing first paragraph | **B — Presentation duplication** | **FIXED_IN_PORTAL** — full body only when section open |
| `priority_recommendation` ≈ `next_action` ≈ primary composed_text | **C — Upstream content duplication** | **UPSTREAM_CONTENT_DUPLICATION** — unchanged |
| Commercial supporting points recycled into identity/summary upstream | **C — Upstream** | Unchanged |
| Chart fundamentals in summary **and** technical metadata | **A — Intentional** | KEEP (summary first-read; technical reference) |

---

## 6. Career Content Hierarchy

Reading order (DOM):

1. Hero (identity + chart headline)  
2. Executive summary (fundamentals)  
3. Recommendations (primary career rec once)  
4. Warnings  
5. **Narrative (Knowledge / seven sections)**  
6. **Career domain** (assessment preview + expandable detail — no second rec card)  
7. Technical (collapsed)  

Career remains available and secondary to chart + narrative.

---

## 7. Technical Information Hierarchy

- Technical moved **after** narrative/career in main + nav  
- Collapsed by default; expand reveals pillars, day master, pattern, strength, score, metadata  
- Fundamentals remain in summary bullets for first-read (LAUNCH-06)  

---

## 8. Mobile Validation

| Width | Approach |
|-------|----------|
| 1440 / 1024 / 390 | Existing Result V2 tokens, `overflow-x: clip`, `overflow-wrap: anywhere` preserved |
| Long recommendation / analysis text | Field/article wrap rules reinforced — **no broad responsive refactor** |
| Overflow helper | No dedicated Result V2 DOM overflow helper for these breakpoints; layout conventions unchanged |

---

## 9. Changes Made (FIXED_IN_PORTAL)

| File | Change |
|------|--------|
| `liveAnalysisResultAdapter.ts` | Career from assessment fields; no narrative remount; explicit empty domain rec ids |
| `portalPresentationAdapter.ts` | Respect explicit empty `recommendation_ids` |
| `ResultPage/index.tsx` | Hierarchy: Summary → Rec → Warnings → Knowledge → Domains → Technical |
| `Knowledge/index.tsx` | Full readable paragraphs; `data-narrative-sections` |
| `DomainSection/index.tsx` | Paragraph split for analysis prose |
| `useResultPage.ts` | Knowledge expanded; Technical collapsed |
| `visibility.ts` | Nav order matches reading hierarchy |
| `result_v2.css` | Knowledge list gap; article paragraph spacing; field wrap |
| `launch_07_content_quality.test.tsx` | Focused quality tests |
| Existing Result V2 / LAUNCH portal tests | Adjusted for technical secondary behavior |

---

## 10. Upstream Issues Not Changed

| Issue | Tag |
|-------|-----|
| Mid-sentence `…` in commercial executive / primary recommendation fields | UPSTREAM_CONTENT_ISSUE |
| Recycled commercial strings across identity / summary / recommendation | UPSTREAM_CONTENT_DUPLICATION |
| Mixed unaccented Vietnamese in some weakness strings | UPSTREAM_CONTENT_ISSUE |
| Empty wealth/relationship/health/luck domain packages | NOT_AVAILABLE_FROM_API (still hidden) |
| Narrative “Khuyến nghị” section text quality | UPSTREAM_CONTENT_ISSUE |

---

## 11. Tests

```text
npx vitest run src/features/portal tests/js/result_v2_adapter.test.ts tests/js/result_v2_page.test.tsx
```

**Result:** 7 files / **36 passed**

Coverage includes:

1. Long narrative not Portal-truncated  
2. Full section content accessible  
3. Summary ≤5 / fundamentals-first  
4. Seven-section order  
5. No Portal duplicate narrative/rec cards  
6. Upstream `…` preserved on primary title  
7. Career after narrative; technical secondary  
8. Live `api` source  
9. Demo path separate  
10. Existing Result V2 green  

---

## 12. TypeScript

```text
npx tsc --noEmit
```

**Result:** exit 0  

---

## 13. Scope Validation

```text
git diff --name-only
```

All production modifications under:

`applications/customer_portal/**`

Audit doc (this file): `knowledge/pilot/launch_audit/LAUNCH_07_CONTENT_QUALITY.md`

No engines / pipelines / API / Knowledge Packages / Golden Dataset changes.

---

## 14. Remaining Product Gaps

- Upstream commercial truncation/ellipsis still visible wherever those fields are shown (e.g. primary recommendation title)  
- Domain packages beyond career still absent  
- Charts / appendix still empty for this live chart  
- Content tone/jargon quality remains an upstream narrative concern  
- Visual polish beyond spacing/hierarchy not redesigned (by design)

---

LAUNCH_07_STATUS: COMPLETE

NEXT_TASK: LAUNCH-08
