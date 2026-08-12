# LAUNCH-05 — Real Chart Result UX Audit

**Task:** BTE LAUNCH-05  
**Date:** 2026-08-12  
**Scope:** AUDIT ONLY — no UI, CSS, engine, pipeline, or API changes  

**Evidence base:** LAUNCH-04 live capture  
`applications/customer_portal/src/features/portal/fixtures/launch_04_real_chart_response.json`  
→ `adaptLiveAnalysisResult` → `adaptPortalResult` → Result V2 zones  

---

## 1. Executive Summary

The live Nguyen Tien Son path works (`source=api`, adapter OK, Result V2 renders without error). The page is **not yet consultant-grade for ONE BaZi chart**.

What works:

- Subject name is correct and live
- Career-oriented narrative and one primary recommendation are real API content
- Technical block exposes live Four Pillars
- Empty charts/knowledge/appendix are correctly **not mounted**

What fails the “understand ONE real chart” test:

1. **Chart fundamentals are demoted** — day master, pattern (Chính Ấn), strength, score exist in API but barely appear in the reading hierarchy (pillars only inside collapsed Technical).
2. **Hero / summary are long, jargon-dense career prose** (Thực Thần, Chính Ấn) without a short “who + chart snapshot + plain conclusion” layer.
3. **Four empty domain shells still render** (wealth / relationship / health / luck), adding noise.
4. **Rich narrative sections (7) are not mapped** into Result V2 — reading path loses Observation → Reasoning → Impact.
5. **Content quality issues upstream** — mid-sentence ellipsis truncation, recycled strings, mixed technical/unaccented Vietnamese in weaknesses.

**Commercial readiness (overall):** PARTIALLY_READY for private consultant review; **NOT_READY** for first-time customer or polished commercial demo.

---

## 2. Real Chart Under Audit

| Field | Value |
|-------|--------|
| Name | Nguyen Tien Son |
| Gender | male |
| Birth | 1987-01-21 04:30 |
| Place | Ha Noi, Vietnam |
| Source | **api** (not demo) |
| Analysis id | `launch04-nguyen-tien-son` |

**Verified Four Pillars (runtime match confirmed in LAUNCH-04):**

| Pillar | Runtime |
|--------|---------|
| Year | Bính Dần |
| Month | Tân Sửu |
| Day | Canh Ngọ |
| Hour | Mậu Dần |

**Also present on live API (not fully surfaced in Result V2):**

- Day master: **Canh**
- Pattern: **Chính Ấn**
- Strength: **strong** (~0.87), reasoning “Thân vượng”
- Score: **D+** / 51.25
- `narrative_result`: status `complete`, 7 sections, commercial executive + primary recommendation + career assessment

---

## 3. Result V2 Zone Audit

### Hero

| Question | Answer |
|----------|--------|
| What does the user learn? | Name + long career headline + long one-line summary + ready status |
| Real analysis data? | **YES** (customer name; executive `central_message` / `conclusion`) |
| Specific to this chart? | **YES** (references Chính Ấn / Thực Thần for this case) |
| Hierarchy correct? | Partial — Who is clear; “overall BaZi conclusion” is replaced by career essay |
| Useful? | Weak for first-time customer; partial for consultant |
| Empty? | No |
| Action | **IMPROVE_PRESENTATION** (+ optional **MAPPING** to add chart snapshot fields if contract allows without inventing copy) |

### Executive Summary

| Question | Answer |
|----------|--------|
| What does the user learn? | Up to 5 bullets from executive supporting points / strengths |
| Real data? | **YES** |
| Chart-specific? | **PARTIALLY_SPECIFIC** — career-specific but truncated (`…`) and repetitive |
| Hierarchy? | Appears after Hero (correct), but bullets are long career paragraphs, not scannable conclusions |
| Useful? | Weak–acceptable for consultant; weak for customer |
| Empty? | No |
| Action | **IMPROVE_PRESENTATION** / **CONTENT_PROBLEM** (upstream truncation) |

### Recommendations

| Question | Answer |
|----------|--------|
| What does the user learn? | One career primary recommendation (what/why/how/expected) |
| Real data? | **YES** (`primary_recommendation`) |
| Chart-specific? | **CHART_SPECIFIC** |
| Hierarchy? | Correct position; content is very long |
| Useful? | Yes for career consulting; hard to scan |
| Empty? | No (1 item). Root narrative rec without `domain` correctly omitted (no invented domain) |
| Action | **IMPROVE_PRESENTATION** (scanability); **NEEDS_DATA** only if multi-domain recs are required later |

### Warnings

| Question | Answer |
|----------|--------|
| What does the user learn? | Career risk + mitigation from career assessment |
| Real data? | **YES** |
| Chart-specific? | **CHART_SPECIFIC** |
| Useful? | Yes |
| Empty? | No (1 warning when career risks exist) |
| Action | **KEEP** (with presentation polish later) |

### Domain sections

| Domain | Rendered | Content | Action |
|--------|----------|---------|--------|
| career | Yes | Available via primary rec ids; no intro/preview/detail | **IMPROVE_PRESENTATION** / **MAPPING** (could attach narrative career text as preview without inventing) |
| wealth | Yes | EmptyState | **HIDE_WHEN_EMPTY** |
| relationship | Yes | EmptyState | **HIDE_WHEN_EMPTY** |
| health | Yes | EmptyState | **HIDE_WHEN_EMPTY** |
| luck | Yes | EmptyState | **HIDE_WHEN_EMPTY** |

Empty domains: real data **NO** for Result V2 presentation envelope; API has no domain-shaped wealth/relationship/health/luck packages → **NOT_AVAILABLE_FROM_API** for those Result V2 keys. Problem type: **EMPTY_STATE_PROBLEM** + **DATA** for missing domains.

### Charts

| Question | Answer |
|----------|--------|
| Empty? | Yes — **NOT_RENDERED** (visibility hides when length 0) |
| Why? | Adapter sets `charts: []`; API has score series but no Result V2 chart envelope |
| Action | **DEFER** / **NEEDS_DATA** if charts become product-required |

### Technical information

| Question | Answer |
|----------|--------|
| What does the user learn? | Pillars string, timezone, schema/contract, analysis id, some metadata |
| Real data? | **YES** |
| Chart-specific? | **CHART_SPECIFIC** (pillars match fixture) |
| Hierarchy? | Too late / collapsed — consultant must open Technical to see pillars |
| Birth date/time? | **Not in technical** (not echoed as structured fields on customer; only in original request) |
| Action | **IMPROVE_PRESENTATION** (surface pillars earlier) + **MAPPING** (add birth datetime if available without inventing) |

### Knowledge

| Empty? | **NOT_RENDERED** |
| Why? | No knowledge items mapped; API `knowledge_expert` portal status ≠ Result V2 knowledge cards |
| Action | **DEFER** / **NEEDS_DATA** |

### Appendix

| Empty? | **NOT_RENDERED** |
| Why? | No appendix in live presentation |
| Action | **DEFER** |

### Footer / empty / loading / error

| Zone | Status |
|------|--------|
| Footer | Renders chrome footer — **KEEP** |
| Loading / offline / error / empty page states | Exist in Result V2; live path uses reading state — **KEEP** |
| Live map failure | Portal `PvError` (LAUNCH-03) — **KEEP** |

---

## 4. Real Data Coverage

| Zone | Real Data Available | Rendered | Specific To Chart | Quality | Problem Type | Recommended Action |
|------|---------------------|----------|-------------------|---------|--------------|--------------------|
| Hero identity (name) | YES | YES | YES | 3 | — | KEEP |
| Hero headline / one-liner | YES | YES | PARTIAL | 1 | CONTENT + PRESENTATION | IMPROVE_PRESENTATION |
| Executive summary bullets | YES | YES | PARTIAL | 1 | CONTENT (truncation) | IMPROVE_PRESENTATION |
| Recommendations | YES (career primary) | YES | YES | 2 | PRESENTATION (length) | IMPROVE_PRESENTATION |
| Warnings | YES (career risk) | YES | YES | 2 | — | KEEP |
| Domain career | PARTIAL | YES | PARTIAL | 1 | MAPPING (no intro/detail) | IMPROVE_PRESENTATION |
| Domain wealth/rel/health/luck | NO | YES (empty shells) | NO | 0 | EMPTY_STATE | HIDE_WHEN_EMPTY |
| Charts | NO (no V2 chart envelope) | NO | — | — | DATA | DEFER |
| Technical pillars | YES | YES (collapsed) | YES | 2 | PRESENTATION (hierarchy) | IMPROVE_PRESENTATION |
| Technical birth DT | NO in payload echo | NO | — | — | DATA / MAPPING | NEEDS_DATA or MAPPING if request echo added later |
| Knowledge | NO for V2 cards | NO | — | — | DATA | DEFER |
| Appendix | NO | NO | — | — | DATA | DEFER |
| Pattern / strength / score | YES in API | NO in V2 reading zones | YES | — | MAPPING | IMPROVE_PRESENTATION / MAPPING |
| Narrative sections (7) | YES in API | NO | YES | — | MAPPING | MAPPING or DEFER |

---

## 5. User Experience Audit

### A. First-time customer

| Need | Met? |
|------|------|
| Who the report is about | **YES** — Nguyen Tien Son |
| Main conclusion | **WEAK** — long career prose with specialist terms, not a plain takeaway |
| What matters most | **WEAK** — one dense recommendation; no clear “start here” chart frame |
| What to read next | **PARTIAL** — nav exists; empty domains confuse |

**Verdict:** Not ready as a self-serve first-time customer result.

### B. Consultant

| Need | Met? |
|------|------|
| Four Pillars | **PARTIAL** — only in Technical (collapsed) |
| Core interpretation | **WEAK** on page — exists in API narrative sections but not mapped |
| Strength conclusion | **NO** on Result V2 reading surface (API has `strong` / Thân vượng) |
| Major recommendations | **YES** (1 career primary) |
| Evidence | **WEAK** — pillars technical-only; score/pattern not surfaced |
| Caveats | **YES** (career warning) |

**Verdict:** Usable for private review only if consultant already trusts the engines and opens Technical; not a strong consulting canvas.

### C. Returning user

| Need | Met? |
|------|------|
| Subject | **YES** |
| Report identity | **PARTIAL** (analysis id in technical) |
| Major conclusion | **WEAK** (same dense headline) |
| Continue reading | **PARTIAL** |

---

## 6. Specificity Audit

| Visible block | Classification |
|---------------|----------------|
| Name “Nguyen Tien Son” | **CHART_SPECIFIC** |
| Headline referencing Chính Ấn / Thực Thần career framing | **CHART_SPECIFIC** (but jargon-heavy) |
| Summary bullets (environment / advantage / risk) | **PARTIALLY_SPECIFIC** — chart-tied career text, truncated, somewhat template-like |
| Primary recommendation what/why/how | **CHART_SPECIFIC** |
| Career warning | **CHART_SPECIFIC** |
| Technical pillars Bính Dần · Tân Sửu · Canh Ngọ · Mậu Dần | **CHART_SPECIFIC** |
| Empty domain empty-states | **GENERIC** |
| Chrome / footer labels | **GENERIC** (expected) |

**Test:** “Could this appear unchanged on another report?”  
Empty domain shells: **YES (GENERIC)**. Hero name/pillars/primary rec: **NO**.

---

## 7. Information Hierarchy Audit

**Desired order:**

1. Who  
2. Overall conclusion  
3. Why  
4. Major recommendations  
5. Detailed domain analysis  
6. Supporting evidence  
7. Technical  
8. Knowledge / further reading  

**Actual order / deviations:**

1. Who — **OK** (name)  
2. Overall conclusion — **DEVIATION**: career essay headline, not chart structural conclusion (day master / pattern / strength / score)  
3. Why — **DEVIATION**: buried inside long recommendation “why”, not a clear why-block after conclusion  
4. Recommendations — **OK** position; density high  
5. Domain analysis — **DEVIATION**: four empty domains + thin career shell  
6. Evidence — **DEVIATION**: pillars/score/pattern not treated as evidence section; pillars demoted to Technical  
7. Technical — present but late  
8. Knowledge — absent (OK if deferred)

---

## 8. Empty Zone Audit

| Zone | State |
|------|--------|
| wealth | **RENDERED_EMPTY** (EmptyState mounted) · **NOT_AVAILABLE_FROM_API** as V2 domain package |
| relationship | **RENDERED_EMPTY** · **NOT_AVAILABLE_FROM_API** |
| health | **RENDERED_EMPTY** · **NOT_AVAILABLE_FROM_API** |
| luck | **RENDERED_EMPTY** · **NOT_AVAILABLE_FROM_API** |
| charts | **NOT_RENDERED** · **NOT_AVAILABLE_FROM_API** (no V2 chart envelope) |
| knowledge | **NOT_RENDERED** · **NOT_AVAILABLE_FROM_API** for V2 knowledge cards |
| appendix | **NOT_RENDERED** · **NOT_AVAILABLE_FROM_API** |

Do **not** fill with fake content.

---

## 9. Zone Quality Scores

Scale: 0 unusable · 1 weak · 2 acceptable · 3 strong  

| Zone | Score | Note |
|------|-------|------|
| Hero | 1 | Name strong; headline weak UX |
| Executive Summary | 1 | Real but truncated / hard to scan |
| Recommendations | 2 | Real primary career rec |
| Warnings | 2 | Real career risk |
| Domain career | 1 | Thin shell |
| Domain other (×4) | 0 | Empty shells still shown |
| Charts | — | Not rendered (N/A) |
| Technical | 2 | Correct pillars; wrong prominence |
| Knowledge | — | Not rendered |
| Appendix | — | Not rendered |
| Footer / chrome | 3 | Stable |

**Average over scored rendered zones (weighted impression):** ~1.3 → **weak–acceptable**, not strong.

---

## 10. Commercial Readiness

| Audience | Status | Why |
|----------|--------|-----|
| Private consultant review | **PARTIALLY_READY** | Live chart + pillars + career narrative exist if reviewer knows where to look |
| Invited beta user | **PARTIALLY_READY** | Works end-to-end; UX still jargon-heavy and empty-domain noisy |
| First-time customer | **NOT_READY** | Cannot quickly grasp chart + plain conclusion |
| Commercial demo | **NOT_READY** | Empty domains + dense prose undermine trust/polish |

**Overall:** **PARTIALLY_READY**

---

## 11. Top 5 Problems

| Rank | Severity | Problem |
|------|----------|---------|
| 1 | **P0** | Chart fundamentals (Four Pillars, day master, pattern, strength, score) are missing from the primary reading hierarchy |
| 2 | **P0** | Hero/summary are long truncated specialist career prose — poor first-screen comprehension |
| 3 | **P1** | Four empty domain sections still render EmptyState — visual noise |
| 4 | **P1** | Seven live narrative sections are not mapped into Result V2 — lost reading structure |
| 5 | **P1** | Upstream content quality (ellipsis truncation, recycled strings, mixed-quality Vietnamese in weaknesses) reduces trust |

---

## 12. Minimal Fix Strategy

| Problem | Type | Smallest responsible layer |
|---------|------|----------------------------|
| P0 Chart fundamentals not prominent | **MAPPING_PROBLEM** + **PRESENTATION_PROBLEM** | `liveAnalysisResultAdapter` (surface existing API fields into presentation/technical/hero-adjacent fields already allowed by contract) + Result V2 only if layout already supports — **do not change engines** |
| P0 Dense hero/summary | **CONTENT_PROBLEM** + **PRESENTATION_PROBLEM** | Prefer shorter existing structured fields if any; otherwise mark **UPSTREAM_CHANGE_REQUIRED** for narrative composition length — **do not invent Portal copy** |
| P1 Empty domains mounted | **EMPTY_STATE_PROBLEM** / **PRESENTATION_PROBLEM** | Result V2 `ResultPage` / domain visibility (hide unavailable domains) — Portal presentation only |
| P1 Narrative sections unused | **MAPPING_PROBLEM** | `liveAnalysisResultAdapter` map section titles/paragraph text into allowed presentation fields (e.g. summary / career analysis_detail) **without fabricating** |
| P1 Truncation / language quality | **CONTENT_PROBLEM** | Narrative / commercial composition upstream → **UPSTREAM_CHANGE_REQUIRED** if Portal cannot shorten without inventing |

**Do not** fix presentation emptiness by fabricating recommendations, domains, charts, or knowledge.

---

## 13. Upstream Dependencies

| Item | Required now? | Mark |
|------|---------------|------|
| AF-1 / Foundation / canonical pipeline redesign | No | — |
| Strength Engine / Knowledge Packages / API contract change | No for P0 presentation/mapping | — |
| Narrative composition length / truncation quality | Yes for content polish | **UPSTREAM_CHANGE_REQUIRED** (record only) |
| New domain analysis packages (wealth/…) | Only if product requires those zones | **UPSTREAM_CHANGE_REQUIRED** later — else **HIDE_WHEN_EMPTY** |

No upstream implementation in this audit.

---

## 14. Recommended LAUNCH-06

**LAUNCH-06 — Result V2 live-chart readability pass (presentation + mapping only)**

Suggested minimal scope:

1. Hide unavailable domain sections (wealth/relationship/health/luck) when `available=false` and no content.  
2. Surface Four Pillars (+ day master if already in API) in the early reading path via existing presentation/technical fields — **no invented prose**.  
3. Map existing `narrative_result.sections` text into allowed presentation slots where semantically valid (no new zones).  
4. Optionally map score grade / pattern label / strength level as technical metadata or identity-adjacent fields **only if already present** — no fabricated interpretation.  
5. Leave charts/knowledge/appendix empty/hidden; do not invent.  
6. Document remaining content-quality issues as upstream, not Portal fiction.

Out of scope for LAUNCH-06: engine changes, AF-1, Strength calibration, new API contracts, CSS redesign.

---

## 15. Validation

### Tests run (lightweight, supporting audit)

| Test | Result |
|------|--------|
| `npx vitest run src/features/portal/launch_04_real_chart_e2e.test.tsx src/features/portal/launch_03_live_result_mapping.test.tsx` | **12 passed** |
| Production tests modified? | **No** |
| Existing relevant tests remain green? | **Yes** |

### Scope gate

```text
git diff --name-only
```

Expected production tracked diff for this task: **none**.  
Only new audit artifact:

`knowledge/pilot/launch_audit/LAUNCH_05_RESULT_UX_AUDIT.md`

---

LAUNCH_05_STATUS:
AUDIT_COMPLETE

NEXT_TASK:
LAUNCH_06
