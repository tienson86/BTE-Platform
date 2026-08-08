# 01 — Content Quality Audit

Version: 1.0  
Status: **Release B — Content Quality**  
Date: 2026-08-08  
Scope: Documentation audit only — no runtime change

---

## 1. Purpose

Audit every class of user-facing text in BTE V1 commercial surfaces.

Goal: make BTE read like an experienced BaZi consultant, not like a software system.

Rating scale used throughout:

| Rating | Meaning |
|--------|---------|
| **GOOD** | Consultant-ready; keep |
| **ACCEPTABLE** | Usable; polish later |
| **TECHNICAL** | Engine / English / internal jargon exposed |
| **TOO SHORT** | Structurally present but commercially thin |
| **PLACEHOLDER** | Mock, coming-soon, or approved insufficient stand-in |
| **REQUIRES IMPROVEMENT** | Wrong voice, wrong language, or weak consulting quality |

---

## 2. Audit scope

### In scope

| Surface | Sources reviewed |
|---------|------------------|
| NarrativeResult sections | Pack 05 composers + Sprint C writing system |
| Portal Result Page | Canonical Desktop, Result presentation, content cards |
| BaZi Result path | Parallel Wave-3 screens (BC) |
| Pack 06 consultation screens | Executive / Consultation / Appendix stack |
| Portal chrome | Nav, CTAs, gates, i18n `vi.json` |
| System states | Loading, empty, error |

### Out of scope (by Release B rules)

- Runtime / Narrative Engine / Interpretation / Score edits  
- Foundation / Design System / Public API / Architecture edits  
- Inventing analytical facts  

---

## 3. Narrative sections

Official Pack 05 commercial prose path:

```
Analysis → Interpretation → Narrative Runtime → Composer → NarrativeResult → API → Portal
```

Section titles (composer constants):

| Section | Title | Tone key |
|---------|-------|----------|
| Executive Summary | Tóm tắt điều hành | briefing |
| Observation | Quan sát | neutral_factual |
| Reasoning | Lý giải | explanatory |
| Impact | Tác động | empathic_concrete |
| Recommendation | Khuyến nghị | directive_supportive |
| Warning | Lưu ý | cautionary_calm |
| Conclusion | Kết luận | settling |

Portal Result Page maps paragraph roles to:

| Role | UI label | Notes |
|------|----------|-------|
| observation | Quan sát | GOOD |
| explanation | Giải thích | Maps Reasoning; ACCEPTABLE naming |
| impact | Tác động | GOOD |
| suggestion | Gợi ý | GOOD |

There is no separate Knowledge section inside `NarrativeResult`. Knowledge on Portal is a structural / glossary zone (see §6).

---

## 4. Section-by-section audit

### 4.1 Executive Summary

| Aspect | Finding | Rating |
|--------|---------|--------|
| Slot contract (identity / strengths / weaknesses / priority / next action) | Spec complete; five commercial questions defined | GOOD |
| Voice target | Briefing, decisive consultant | GOOD (spec) |
| Live richness | Often derives from thin upstream Interpretation; many runs `partial_insufficient` | TOO SHORT / PLACEHOLDER |
| Framing | No framing prefix (good); slots may still echo source fragments | ACCEPTABLE |
| Generic risk | When filled from short sources, can feel like list dumps rather than a person briefing | REQUIRES IMPROVEMENT |
| Technical leakage | Forbidden patterns filtered; technical sources → insufficient text | GOOD (guard) |
| Missing commercial slots in practice | Opportunities / risks / immediate priority not always distinct from weaknesses / next_action | REQUIRES IMPROVEMENT (guideline gap) |

**Verdict:** Architecture GOOD; commercial depth REQUIRES IMPROVEMENT until evidence enrichment.

### 4.2 Observation

| Aspect | Finding | Rating |
|--------|---------|--------|
| UI label | Quan sát | GOOD |
| Spec voice | Neutral, factual | GOOD |
| Runtime pattern | Optional prefix `Quan sát từ dữ liệu phân tích:` + source body | ACCEPTABLE (structural, slightly system-flavored) |
| Quality when source is commercial | Can be consultant-grade | GOOD |
| Quality when source is thin | Falls to approved insufficient line | PLACEHOLDER |
| Bad upstream | Rule-prose filtered out | GOOD (guard) |

**Verdict:** ACCEPTABLE structure; depth depends on Interpretation.

### 4.3 Reasoning (UI: Giải thích / Lý giải)

| Aspect | Finding | Rating |
|--------|---------|--------|
| Spec voice | Explanatory, patient | GOOD |
| Runtime prefix | `Lý giải dựa trên nguồn đã kiểm chứng:` | ACCEPTABLE / mild TECHNICAL flavor |
| Risk | Sounds like a citation system, not a consultant explaining | REQUIRES IMPROVEMENT (wording of frames) |
| Content depth | Rarely reaches Sprint C “good example” essay quality | TOO SHORT |

**Verdict:** REQUIRES IMPROVEMENT for consultant naturalness of framing + depth.

### 4.4 Impact

| Aspect | Finding | Rating |
|--------|---------|--------|
| UI label | Tác động | GOOD |
| Spec voice | Empathic, concrete | GOOD |
| Runtime prefix | `Ý nghĩa thực tế từ nguồn phân tích:` | ACCEPTABLE |
| Commercial risk | May restatement Observation without lived consequence | TOO SHORT when thin |

**Verdict:** ACCEPTABLE; needs richer consequence language without inventing facts.

### 4.5 Recommendation

| Aspect | Finding | Rating |
|--------|---------|--------|
| UI labels | Khuyến nghị / Gợi ý / Hành động · Lý do · Lợi ích | GOOD |
| Spec | Actionable, evidence-backed, no invented actions | GOOD |
| Runtime wrapper | `Ưu tiên phát huy theo nguồn phân tích: {action}` | ACCEPTABLE |
| Common failure modes | Repeat observation; echo scores; generic “ưu tiên phát huy…” | REQUIRES IMPROVEMENT |
| Priority badges | Ưu tiên cao / Cao / Trung bình / Thấp | GOOD |

**Verdict:** Labels GOOD; action specificity REQUIRES IMPROVEMENT.

### 4.6 Warning

| Aspect | Finding | Rating |
|--------|---------|--------|
| UI labels | Cần lưu ý / Điểm cần lưu ý / Lưu ý | GOOD |
| Spec | Cautionary, calm; no catastrophe; no invention | GOOD |
| Runtime wrapper | `Cần lưu ý: {action}` / `Cần lưu ý theo nguồn phân tích:` | ACCEPTABLE |
| Fear / certainty risk | Forbidden patterns block “thảm họa chắc chắn” class | GOOD (guard) |
| Mitigation | Spec asks caution; mitigation phrasing not consistently present | REQUIRES IMPROVEMENT |

**Verdict:** Tone guards GOOD; mitigation completeness REQUIRES IMPROVEMENT.

### 4.7 Conclusion

| Aspect | Finding | Rating |
|--------|---------|--------|
| Canonical S11 title | KẾT LUẬN TỔNG QUAN | GOOD |
| Spec voice | Settling, integrative | GOOD |
| Runtime prefix | `Điểm then chốt từ các nguồn đã nêu:` | ACCEPTABLE |
| Pack 06 panel title | `Conclusion` (English) | REQUIRES IMPROVEMENT |
| Risk | New unsupported claims | Guarded by meaning lock — GOOD |

**Verdict:** Official path ACCEPTABLE–GOOD; Pack 06 path REQUIRES IMPROVEMENT.

### 4.8 Knowledge

| Aspect | Finding | Rating |
|--------|---------|--------|
| Result zone title | KIẾN THỨC | GOOD |
| Accordion labels | Thuật ngữ / Tài liệu tham chiếu / Lý thuyết truyền thống / Phụ lục | GOOD |
| Content nature | Structural / glossary / chart facts — not Pack 05 prose (G5) | ACCEPTABLE by design |
| i18n leftovers | `Knowledge`, `Insight`, `AI Knowledge Expert`, `Priority Rules · Knowledge` | TECHNICAL |
| Educational flow | Can feel textbook / interruptive when English or engine terms appear | REQUIRES IMPROVEMENT |

**Verdict:** Zone structure GOOD; copy consistency REQUIRES IMPROVEMENT; educational richness ACCEPTABLE (structural only).

---

## 5. Portal labels, CTAs, and chrome

### 5.1 Navigation & Result chrome

| Item | Sample | Rating |
|------|--------|--------|
| Nav items | Trang chủ, Luận giải, Kết quả, Báo cáo… | GOOD |
| Result TOC (S00) | Tóm tắt, Bát Tự, Biểu đồ, Phân tích, Luận giải, Kiến thức | GOOD |
| Result TOC (navItems) | BaZi (English spelling) | TECHNICAL / ACCEPTABLE |
| Zone titles (presentation) | TÓM TẮT ĐIỀU HÀNH, KHUYẾN NGHỊ, LUẬN GIẢI… | GOOD |
| CTAs | Xem tất cả khuyến nghị →, Mở rộng luận giải, Thu gọn, Xem thêm | GOOD |
| Aria EN on VI pages | Summary Zone, Recommendation Zone, Menu | TECHNICAL |

### 5.2 System states (official Result path)

| State | Sample | Rating |
|-------|--------|--------|
| Loading | Đang tải kết quả… | GOOD |
| Empty | Chưa có kết quả / Nhập thông tin sinh để xem lá số Bát Tự. | GOOD |
| Error | Không tải được kết quả | GOOD |
| Unavailable prose | Chưa đủ dữ liệu để đưa ra kết luận. | GOOD (approved) |
| API errors | Dữ liệu không hợp lệ / Phiên đăng nhập hết hạn… | GOOD |

### 5.3 Pack 06 / consultation stack (parallel)

| Item | Sample | Rating |
|------|--------|--------|
| Gates | Loading / No data available / Unable to load content | REQUIRES IMPROVEMENT |
| Screen titles | Loading executive summary, Analysis Blocks | TECHNICAL |
| Panels | Conclusion, Explanation, Risks, Evidence, Knowledge Reference | REQUIRES IMPROVEMENT |
| Stem/branch labels | Heavenly Stem, Earthly Branch, Hidden Stems | TECHNICAL |

### 5.4 i18n `vi.json` residual English / jargon

| Key area | Sample | Rating |
|----------|--------|--------|
| report.an_knowledge | Knowledge | TECHNICAL |
| report.kw_insight | Insight | TECHNICAL |
| report.knowledge_expert | AI Knowledge Expert | TECHNICAL |
| report.chart_source_score | Score payload | TECHNICAL |
| report.chart_metric_*_hint | strength_score (0–100)… | TECHNICAL |
| discussion.ask_placeholder | Hỏi Why / How / Evidence… | TECHNICAL |
| pattern.na | N/A | TECHNICAL |
| coming_soon | Sắp ra mắt | PLACEHOLDER (acceptable if true) |

### 5.5 Mock / fixture surfaces

| Item | Sample | Rating |
|------|--------|--------|
| BaZi mock recommendations | (mock — chờ Interpretation) | PLACEHOLDER |
| ShenSha legend | (sau Engine) | TECHNICAL |
| Dashboard mock | Mock stats / hints | PLACEHOLDER |
| Cân xương đoán mệnh (S10) | Often forced unavailable | PLACEHOLDER |

---

## 6. Cross-cutting findings

### 6.1 What is already strong

1. Pack 05 meaning lock + forbidden wording filters block calculator / prophecy / developer tone.  
2. Official Result Page section titles and narrative role labels are Vietnamese and commercial.  
3. Approved insufficient narrative is consistent and non-inventive.  
4. Sprint C writing system (docs 13–20) already defines consultant voice — Release B extends it into release standards.  
5. Content guards (`commercialOrUnavailable`) keep mock/rule prose off the Result Page.

### 6.2 Primary quality gaps

| ID | Gap | Severity |
|----|-----|----------|
| CQ-1 | Upstream Interpretation thin → frequent insufficient / TOO SHORT narrative | High |
| CQ-2 | Composer framing prefixes sound system-like (“từ nguồn phân tích”) | Medium |
| CQ-3 | Executive Summary rarely answers full consultant briefing (who + strengths + weaknesses + opportunities + risks + priority + next action) as a coherent paragraph set | High |
| CQ-4 | Recommendations often generic; weak specificity / benefit / mitigation | High |
| CQ-5 | Warnings rarely pair risk + calm mitigation | Medium |
| CQ-6 | Knowledge / i18n / Pack 06 expose English and engine jargon | High (surface consistency) |
| CQ-7 | Parallel surfaces (Pack 06 EN gates, BaZi mocks) dilute voice | Medium |
| CQ-8 | Aria / screen-reader labels remain English on Vietnamese pages | Low–Medium |

### 6.3 Mapping to Product Integration gaps

| Integration gap | Content implication |
|-----------------|---------------------|
| G5 Knowledge structural | Knowledge educate-without-interrupting needs copy guidelines, not NarrativeResult rewrite |
| G6 Insufficient evidence | Core commercial richness blocker |
| G2 Pack 06 not on NarrativeResult | English consultation copy debt remains |

---

## 7. Inventory summary counts (by rating class)

Approximate distribution across audited string classes (labels + states + section quality):

| Rating | Share (approx.) | Notes |
|--------|-----------------|-------|
| GOOD | ~45% | Official Result path titles, gates, CTAs, guards |
| ACCEPTABLE | ~20% | Structural framing, Knowledge glossary design |
| TECHNICAL | ~15% | i18n leftovers, aria EN, Pack 06 stem labels |
| TOO SHORT | ~10% | Live narrative depth when evidence thin |
| PLACEHOLDER | ~5% | Insufficient line, mocks, coming soon |
| REQUIRES IMPROVEMENT | ~15% | Pack 06 EN stack, recommendation specificity, executive coherence |

Percentages overlap (one item can be TECHNICAL and REQUIRES IMPROVEMENT). Use for prioritization, not as a metric freeze.

---

## 8. Audit conclusion

BTE V1 has a **sound content architecture** and **strong safety rails** (no invention, no prophecy, no rule-engine leakage on the official path).

It does **not** yet consistently deliver **consultant-grade commercial prose**.

Release B documents define the quality bar and roadmap. Implementation belongs to later content enrichment / copy polish epics — **not** this documentation release.

---

## 9. Related documents

| Doc | Role |
|-----|------|
| `02_EXECUTIVE_SUMMARY_GUIDELINES.md` | Executive standards |
| `03_RECOMMENDATION_GUIDELINES.md` | Recommendation standards |
| `04_WARNING_GUIDELINES.md` | Warning standards |
| `05_KNOWLEDGE_PRESENTATION_GUIDELINES.md` | Knowledge standards |
| `06_COPYWRITING_GUIDELINES.md` | Portal / UI copy voice |
| `07_CONTENT_STYLE_CHECKLIST.md` | Review gate |
| `08_CONTENT_QUALITY_FINAL_REPORT.md` | Release readiness |

Upstream references (frozen / existing): Pack 05 docs `13`–`20`, Product Integration V1 remaining gaps G5–G6.
