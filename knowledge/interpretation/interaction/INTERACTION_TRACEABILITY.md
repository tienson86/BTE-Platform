# Interaction Traceability

Version: 1.0  
Status: SPECIFICATION  
Issue: B1-P0-002

---

## 1. Frozen chain

```text
Interaction Fact
        ↓
Narrative
        ↓
Published Narrative
        ↓
Professional PDF
        (and Executive PDF where the briefing includes the current period)
```

A customer sentence about the current life period is traceable only if every step on this chain can name an Interaction Fact.

If any step is skipped, the sentence is natal copy, thesis duplication, or filler.

---

## 2. Layer duties

| Layer | May do | Must not do |
|-------|--------|-------------|
| Interaction Truth | Record period identity, governors, overlap, directions, confidence, evidence | Write prose; reselect natal values; calculate luck |
| Narrative | Compose customer sentences from Interaction Facts + natal facts that those facts reference | Invent overlap; use thesis as luck evidence |
| Published Narrative | Keep, drop, or appendix already-composed sentences | Create a new interaction claim |
| Professional / Executive PDF | Print published sentences in the allowed section | Harvest natal thesis into `sec-luck` because the decade needs words |

---

## 3. Required trace fields (conceptual)

For every customer sentence that mentions the current Da Yun as a lived period:

| Trace field | Source |
|-------------|--------|
| `interaction_fact_ids` | Interaction Facts used |
| `period_ref` | LuckEngine identity copied on those facts |
| `natal_refs` | Natal owners copied on those facts |
| `narrative_node_id` | Composer node that wrote the sentence |
| `publication_decision` | PUBLISH / DROP / APPENDIX |
| `section_id` | Executive or Professional section that printed it |
| `edition` | `executive` or `professional` |

A Current Da Yun sentence with no `interaction_fact_ids` is invalid under this spec.

A natal sentence that never names the period does not need Interaction Facts.

---

## 4. Section responsibility — Professional

Professional page order is already frozen. This spec does not change it.

| Section | Interaction Facts required | Optional | Must never appear |
|---------|----------------------------|----------|-------------------|
| `sec-executive_summary` Tóm tắt | None required | Period identity + one summary overlap flag | Full helpful/pressure lists; ten-cycle list; natal dump labelled as luck |
| `sec-chart` Lá số | None | None | Any Interaction Fact. This page is natal / chart identity only |
| `sec-core_interpretation` Luận giải cốt lõi | None | `natal_governor_in_force` only if needed to stop a false “the decade changed the chart” claim | Helpful/pressure-as-decade-effect; period stem/branch as a new Useful God |
| `sec-ten_gods` Thập thần | None | Period ten-god **only** as identity overlap with a natal Ten God already on the chart | Recalculated decade Ten Gods essay |
| `sec-shen_sha` Thần sát | None | Period overlap with a natal matched star | New stars caused by Da Yun |
| `sec-luck` Đại vận hiện tại | **Required:** period identity; interaction summary; supported direction; restricted direction; confidence; evidence. Helpful/pressure lists required as lists (empty allowed) | Next-period-not-current; unused-domain diagnostics | Copied natal thesis; duplicated career implication; glossary of Da Yun theory; all ten cycles; ScoreEngine |
| `sec-career` Sự nghiệp | None | Helpful/pressure overlaps that are already career-relevant natal applications | Replacing natal career meaning with a luck story |
| `sec-life_areas` Tài chính · Quan hệ · Sức khỏe · Học hỏi | None | One overlap overlay per area, only if an Interaction Fact exists for that area’s natal application | Repeating the luck page; inventing area effects from period element math |
| `sec-professional_recommendation` Khuyến nghị | None | Actions that change **now** because of evidenced overlap | Natal standing advice relabelled “trong đại vận này” without overlap |
| `sec-professional_conclusion` Kết luận | None | At most one period-true closing fact | Second natal thesis; prediction; ten-cycle close |

`sec-luck` is the only Professional section that **cannot** be true without Interaction Facts.

If Interaction Truth is `MISSING`, `sec-luck` may name the decade as a time frame only, or omit the consultation. It must not back-fill from natal thesis.

---

## 5. Section responsibility — Executive

Executive remains a briefing over the same truth.

| Executive slot | Required | Optional | Must never appear |
|----------------|----------|----------|-------------------|
| Cover / identity | None | Current Da Yun **label** as time frame | Interaction essay |
| Executive Summary | None | One period identity + overlap flag | Helpful/pressure lists |
| Observation | None | None | Interaction Facts mixed into natal observation |
| Current Da Yun (briefing) | Period identity. Interaction summary if status is `AVAILABLE` or `PARTIAL` | Empty-overlap statement | Seven-paragraph Professional luck page; natal thesis paste |
| Recommendations | None | One now-only action tied to overlap | “Nuôi {natal Useful God}” restated as luck |
| Warnings | None | One pressure overlap | Natal Kỵ restated as luck |
| Conclusion | None | One period-true clause | Duplicated thesis |

---

## 6. Domain consumers

Career, Finance, Relationship, Health do not own Interaction Truth.

They may read:

- helpful factors whose natal application already belongs to that domain
- pressure factors whose natal application already belongs to that domain
- supported / restricted direction as constraints, not as new domain truth

They must not:

- treat empty overlap as “no career meaning”
- treat natal Useful God as a decade-specific career forecast
- introduce a Life State or Identity engine

---

## 7. Refusal path

```text
Interaction status MISSING
    → Narrative must not explain the living decade
    → Publisher may keep the cycle name as time frame
    → PDF must not present a fake consultation

Interaction status AVAILABLE with empty overlap
    → Narrative may name the decade and state natal governors remain in force
    → Narrative must not claim helpful/pressure period effects
    → PDF luck page must not paste thesis / career / risk slots to look complete

Interaction status AVAILABLE with overlap
    → Narrative may explain helpful / pressure / direction from those facts only
    → PDF may print that explanation in sec-luck and optional overlays
```

---

## 8. Anti-patterns already observed

B1-P0-001 assembled Professional `sec-luck` from:

1. Decade name
2. Natal case thesis
3. Natal Pattern / Strength / Dụng / Hỷ / Kỵ
4. Natal career implication
5. Natal thesis risk
6. Natal corrective + career
7. Next label

That chain skips Interaction Facts.

Traceability under this spec: **fail**.

The missing object is Interaction Truth, not another Narrative slot.
