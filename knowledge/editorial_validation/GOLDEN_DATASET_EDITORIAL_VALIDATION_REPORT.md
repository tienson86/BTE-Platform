# GOLDEN_DATASET_EDITORIAL_VALIDATION_REPORT

| Field | Value |
|-------|-------|
| Phase | Golden Dataset Editorial Validation V1 |
| Date | 2026-08-16 |
| Standard | BTE Editorial Standard v1.0 |
| Conclusion band | Provisional (n=10; target was 20–30) |
| Code changed | **NONE** |
| Status | STOPPED — waiting for Product Owner review |

This report aggregates customer-PDF reviews. It does not implement fixes.

---

## 1. Status

Evidence collection is complete for every valid named/bound real case in the repository plus Product Owner–supplied Tân.

**STOP.** Do not patch Narrative Composer, engines, templates, or knowledge. Do not start Luck Domain, Temperature Domain, Story Engine, or Case Identity Engine.

Verdict: **READY_FOR_PRODUCT_REPAIR_PLANNING** (provisional).

---

## 2. Number of real cases

| Class | Count | Used? |
|-------|-------|-------|
| Named/bound charts with birth datetime and a 2026-08-16 production PDF | **10** | Yes — all reviewed |
| Anonymous `validation/real_cases/case_01`–`case_20` | 20 | **No** — pipeline fixtures, no consulting identity |
| Pilot CASE-0008 / CASE-0009 | 2 | **No** — no birth datetime |
| Synthetic Readiness Subject | 1 | **No** — labelled synthetic |
| Invented charts | 0 | Forbidden |

Actual editorial n = **10**. Coverage gaps are listed in §3 and `COVERAGE_MATRIX.md`. No cases were invented to reach 20.

---

## 3. Dataset coverage

**Strength:** strong 6 · balanced 3 · weak 1 (gap: weak under-sampled; strong over-sampled)

**Pattern:** Chính Ấn 2 (Sơn, Tân) · Chính Tài 1 · Thiên Ấn 1 · Thiên Tài 1 · Thực Thần 1 · Thực Thần sinh Tài 1 · Tòng Nhi 2 · Tòng Tài 1.  
Gap: Chính Quan / Thất Sát / Thương Quan as governing pattern; transformation.

**Useful God:** Thực Thần (role) 2 · Canh 3 · Đinh 3 · Nhâm 2.  
Gap: other stems. **Finding:** UG stem/role clusters collapse harder than Pattern clusters.

**Day Master:** Canh, Bính (×3), Nhâm (×2), Mậu (×2), Quý, Giáp. Gap: Ất, Đinh, Kỷ, Tân as Day Master.

**Gender:** male 6 · female 4

**Age:** child 3 · teen 1 · young adult 1 · middle age 4 · older adult 1

**Current Da Yun:** 10 distinct labels. Interpretation: **0**.

Full matrix: `COVERAGE_MATRIX.md`.

---

## 4. Average editorial scores

Mean of 10 scorecards (0–100):

| Dimension | Average |
|-----------|---------|
| Readability | 46.7 |
| Reasoning | 43.0 |
| Case Specificity | 45.6 |
| Expert Language | 41.6 |
| Knowledge Usage | 36.8 |
| Customer Relevance | 39.6 |
| Actionability | 38.5 |
| Commercial Quality | 32.4 |
| **Overall** | **40.6** |

Best overall: EV-0002 Huỳnh **59**. Worst: EV-0005 Khang **22**.  
No case ≥ 70. No case READY_FOR_CUSTOMERS.

---

## 5. Customer readiness

| Band | Count | Cases |
|------|-------|-------|
| **READY** | 0 | — |
| **REPAIR** (thesis audible; not customer-ready) | 4 | EV-0001 Sơn, EV-0002 Huỳnh, EV-0003 Tân, EV-0007 Mai |
| **NOT_READY** | 6 | EV-0004 Trung, EV-0005 Khang, EV-0006 Minh, EV-0008 Tuyền, EV-0009 Phương, EV-0010 child |

READY_FOR_CUSTOMERS on every scorecard: **NO**.

---

## 6. Case specificity

| | Value | Case |
|--|-------|------|
| Average `case_specificity_ratio` | **0.47** | template-collapse risk (< 0.50) |
| Best | 0.68 | EV-0002 Huỳnh |
| Worst | 0.32 | EV-0005 Khang |

Band: 0 strong (≥0.85) · 0 acceptable (0.70–0.84) · 4 generic (0.50–0.69: Sơn, Huỳnh, Tân, Mai) · 6 collapse-risk.

Judgment, not mechanical optimization: Huỳnh/Sơn openings are people; Khang/Minh/Phương/Tuyền are token sheets; Tân’s opening is a person whose recommendations belong to a stem cluster.

---

## 7. Cross-case similarity

Detail: `CROSS_CASE_SIMILARITY.md`.

**Highest-risk pairs / clusters**

1. **Canh-cut cluster (Critical):** Tân ↔ Trung ↔ CASE-0003 — same `Người chỉnh trục` + same rec stack despite balanced-Ấn-teen / strong-Thiên Ấn-49 / weak-Thực Thần-child.
2. **Đinh-generic cluster (Critical):** Khang ↔ Minh — recs/warnings interchangeable; two children, one consultation.
3. **Nhâm-generic cluster (Major):** Mai recs ↔ Phương recs — identical ritual; only Mai has a thesis.
4. **Cover identity theft (Critical):** Huỳnh cover = Sơn’s `Người tự gánh`.

**Legitimate similar pairs**

- Sơn vs Tân: shared Chính Ấn *background* is allowed; openings now differ (gánh vs chỉnh trục). Remaining clone is career/relationship leftover.
- Sơn vs Huỳnh: shared *strong / needs a channel* is allowed; body theses differ.

**Sơn vs Tân (mandatory)** — see § below and `CROSS_CASE_SIMILARITY.md`.  
Historical feared collapse (same Chính Ấn) is **partially repaired at thesis**. Actual worst collapse is **same Useful God stem**.

---

## 8. Useful God quality

| Measure | Count / 10 |
|---------|------------|
| Label-only executive (`useful_god_label_only`) | **4** — Khang, Minh, Tuyền, Phương |
| Reason present in Reasoning | 6 — Sơn, Huỳnh, Tân, Trung, Mai, CASE-0003 |
| Reason missing as a customer explanation | 4 (the label-only set) |
| Application missing or thin (`useful_god_application_missing`) | **9** — only Huỳnh recs 1–3 consistently apply |
| Hỷ/Kỵ undifferentiated (list recs) | 8 |
| Hypothetical role leak (Hỷ/Kỵ essays crowding this life) | 6 |

Best UG write-up: Huỳnh (Đinh vs Bính).  
Best UG-in-thesis: Tân (Canh cuts wood).  
Worst: child Đinh climate stamp.

---

## 9. Domain synthesis quality

`domain_synthesis_missing` is still a major historical weakness, now **split by layer**:

| Layer | Synthesis? |
|-------|------------|
| Case Thesis opening (when it fires) | Often **yes** (Sơn, Huỳnh, Tân, Mai) |
| Cover class | Often **no** (Huỳnh, Trung, Tân mismatch; three empty covers) |
| Career / recs / conclusion | **No** — god textbooks and Hỷ lists |

Follow charts (Khang, Tuyền, Phương) never synthesise Pattern + Strength + UG. Trung synthesises the **wrong** trio (Canh-cut as if Tân). CASE-0003 states weak-need-ground then applies Tân’s cut thesis.

---

## 10. Ten Gods quality

| Flag | Frequency |
|------|-----------|
| `ten_god_catalogue_dump` | 10/10 in Reasoning and/or Conclusion |
| `ten_god_position_ignored` | 10/10 |
| `ten_god_case_relevance_low` | 8/10 (Sơn/Huỳnh slightly better at the first paragraph only) |

No report interprets only the gods that matter for this chart. Nhật Chủ system note is a recurring engine leak in conclusions.

---

## 11. Shen Sha quality

| Flag | Frequency |
|------|-----------|
| `shensha_catalogue_dump` | 4 dense charts teach matching rules (Sơn, Huỳnh, Minh, Tuyền) |
| `shensha_alias_leak` | Huỳnh warning 2 (`Ất/Đức/Nguyệt`); alias pairs Thiên Ất / Thiên Ất Quý Nhân on covers |
| `shensha_overweight` | 0 as personality takeover — stars do not define the whole person (good) |
| `shensha_without_application` | 10/10 |

Secondary placement is mostly respected (stars don’t become the thesis). They still appear as pedagogy, not as this life.

---

## 12. Luck quality

| Code | Count |
|------|-------|
| `luck_list_only` | **10/10** |
| `luck_no_interpretation` | 10/10 |
| `luck_application_missing` | 10/10 |

Da Yun is a timestamp on cover, observation, and sometimes a frame sentence. It is never a decade the person is living. Ten distinct cycles, zero readings.

This is the cleanest evidence in the dataset for a later Luck Domain — **after** template-collapse repair, not instead of it.

---

## 13. Recommendation quality

Typical stack size: **5** (all cases).

| Metric | Dataset picture |
|--------|-----------------|
| Genuinely case-specific | High only on Sơn 1/5, Huỳnh 1–3, Tân 1, Trung 1 |
| Actionable | Those same items |
| Prioritized | **0/10** reports rank a first move |
| Duplicated cross-case | Khang=Minh; Tân≈Trung≈CASE-0003; Mai=Phương |
| Anyone-could-use | `Đặt {UG} làm trọng tâm…` / `Ưu tiên hành động gắn Hỷ thần` / environment checklist |

Average `recommendation_specificity_ratio` ≈ **0.16**.  
Flags: `generic_recommendation`, `recommendation_overload` (five ritual items), `duplicate_recommendation` (cross-case), `recommendation_not_actionable` (engine recs).

---

## 14. Commercial quality

Mean Commercial Quality **32.4**.

Would a paying customer finish / understand / act / get a signed premium consult?

| Case | Finish | Self | Why | Next | Sign | Premium |
|------|--------|------|-----|------|------|---------|
| Sơn | PARTIAL | PARTIAL | PARTIAL | PARTIAL | NO | NO |
| Huỳnh | PARTIAL | PARTIAL | PARTIAL | PARTIAL | NO | NO |
| Tân | PARTIAL | PARTIAL | PARTIAL | PARTIAL | NO | NO |
| Mai | PARTIAL | PARTIAL | PARTIAL | NO | NO | NO |
| Other six | NO | NO | NO | NO | NO | NO |

A senior consultant would not sign any of the ten. The four REPAIR cases would be a draft to rewrite, not a product.

---

## 15. Top recurring strengths

1. When Case Thesis fires, the executive door is a consultation (Sơn, Huỳnh, Tân, Mai).
2. Useful God *reason* essays can distinguish Dụng vs Hỷ vs Kỵ (Huỳnh Đinh/Bính; Tân Canh harshness).
3. Observation *slot* is the right shape (facts, not interpretation) when it doesn’t leak English or double labels.
4. A few recommendations have stop-conditions (Sơn 1/5, Tân 1, Huỳnh 2).
5. Shen Sha does not usually hijack personality.
6. Anti-overclaim instincts exist (`Không suy ra bằng cấp`, `Không hứa giàu`) — locally right.
7. Sơn vs Tân openings now differ despite shared Chính Ấn — the original feared collapse is not the worst remaining failure.

Evidence lines: `GOOD_PATTERN_LIBRARY.md`.

---

## 16. Top recurring weaknesses

1. Same consultation with different BaZi tokens — especially **Useful God stem routing**.
2. Case Thesis does not own cover class (Huỳnh/Trung/Tân mismatches; empty covers).
3. Reasoning and Conclusion are knowledge exports (`conclusion_restart`).
4. Recommendations are a five-item Hỷ ritual, not a first move.
5. Life stage is ignored (children and a teen get adult career).
6. Luck is a label.
7. Pattern leftover (Ấn mentor, Tài not-an-accountant) pastes across people.
8. English `balanced`, engine `Hệ thống xác định nhãn`, broken warning fragments.
9. Follow vs Strength labels can coexist unexplained.
10. Disclaimer voice (`Không chẩn đoán` repeated) becomes the brand.

---

## 17. Top 20 systemic product defects

Ordered by frequency × severity × customer impact (editorial ranking, n=10).

| # | Defect | Type | Freq | Sev | Impact |
|---|--------|------|------|-----|--------|
| 1 | Useful God stem/role writes the whole remaining report | Narrative + Mapping | 8/10 | Critical | Customer gets another person’s consultation |
| 2 | Recommendation ritual (`Đặt UG…` / Hỷ list / Kỵ check) | Narrative + Mapping | 10/10 | Critical | No next step for *this* life |
| 3 | `conclusion_restart` encyclopedia | Knowledge dump / Editorial | 10/10 | Critical | Destroys the retellable ending |
| 4 | Ten God catalogue; positions ignored | Knowledge usage / Editorial | 10/10 | Critical | Glossary not consult |
| 5 | Luck list-only | Missing Domain | 10/10 | Critical | Decade unnamed as lived time |
| 6 | Cover class ≠ body thesis or empty | Mapping / Rendering | 7/10 | Critical | First identity is wrong or blank |
| 7 | Life stage unused (child/teen as worker) | Missing Domain + Editorial | 4/10 + Tân | Critical | Product is not about this person |
| 8 | Case Thesis mis-assignment (Canh cluster) | Narrative (thesis layer) | 3/10 | Critical | Thesis can unify the wrong people |
| 9 | Case Thesis non-firing (token exec) | Narrative | 4/10 | Critical | No human at the door |
| 10 | Pattern leftover sentences (mentor / not-teacher / not-accountant) | Knowledge + Mapping | 6/10 | Major | Shared Ấn/Tài prose |
| 11 | `domain_synthesis_missing` below the opener | Narrative | 10/10 | Major | Three stickers, one dump |
| 12 | Engine language in customer PDF | Editorial | 8/10 | Major | `Nhật Chủ` rec; `Hệ thống xác định nhãn` |
| 13 | English `balanced` / doubled strength labels | Mapping / Rendering | 5+/10 | Major | Unfinished surface |
| 14 | Broken Vietnamese fragments in warnings | Mapping / Editorial | 5/10 | Major | Unreadable “Hệ vượng bị kìm / căng…” |
| 15 | Disclaimer overuse | Editorial | 10/10 | Major | Voice of fear, not consult |
| 16 | Shen Sha matching pedagogy | Knowledge / Editorial | 6/10 | Major | Aliases and rules, no application |
| 17 | Hỷ treated as a second Dụng list | Knowledge + Narrative | 8/10 | Major | Undifferentiated gods |
| 18 | Feng Shui / Cung Phi inventory on cover | Report Layout | 10/10 | Major | Spreadsheet vs conversation |
| 19 | Follow vs Strength unexplained | Analytical candidate | 3/10 | Major | Customer sees contradictory stickers |
| 20 | Missing-element / climate unused (Huỳnh Water=0; temperature leftovers) | Missing Domain | 2–6/10 | Major | Facts on cover, silence in story |

---

## 18. Issues that are truly Narrative

- Case Thesis firing vs non-firing vs **mis-assignment**
- Section restatement (Impact reprints Exec)
- Conclusion restart vs memorable synthesis
- Recommendation ritual vs one prioritized move
- Sentence skeletons 2–6 in `CROSS_CASE_SIMILARITY.md`
- “Same consultation, different tokens” as a prose problem **after** truth is already different

Do not classify the whole phase as Narrative. Thesis already helps when it fires and is right.

---

## 19. Issues that are truly Knowledge

- Ten God entries used as complete essays regardless of chart
- Pattern knowledge leaking as career clones (Ấn → mentor/teacher disclaimer)
- Useful God climate lines (`Thu kim vượng cần hỏa tôi luyện`) dumped into Executive Summary
- Shen Sha matching-rule text
- Disclaimer library over-applied
- Hỷ/Kỵ hypothetical paragraphs that teach the library, not the person

These are not “write better transitions.” They are **wrong objects in the customer book**.

---

## 20. Issues that are Missing Domain

- **Luck Domain:** 10/10 list-only — strongest missing-domain evidence
- **Life stage / consulting frame:** child, teen, older adult not voiced
- **Temperature / climate as a lived domain:** fragments exist (`giữ ấm`, `hàn khí`, `Thu kim vượng`) without a coherent customer chapter
- **Follow-pattern life** as a domain (Tòng Nhi / Tòng Tài never become a story)
- **Missing element** (Huỳnh Water=0) unused

Missing Domain is **not** the first repair if the report still pastes one stem’s story onto three ages.

---

## 21. Issues that are Mapping/Rendering

- Cover class vs body thesis (Huỳnh, Tân, Trung, Mai)
- Empty cover class (Khang, Minh, CASE-0003)
- HTML/PDF showing English `balanced` beside `Trung hòa`
- Doubled `Thân vượng Thân vượng`
- Concatenated warning fragments without punctuation
- Cover Feng Shui + full Da Yun table competing with the class line
- Rec 2 Sơn: engine label instruction mapped into customer recommendations

---

## 22. Issues that may be Analytical

Recorded, **not repaired**:

1. EV-0005 Tòng Nhi + Thân vượng 0.66
2. EV-0008 Tòng Tài + Thân vượng 0.76
3. EV-0009 Tòng Nhi + balanced 0.61 (Follow without “cực nhược” in the strength label)
4. CASE-0003 source historically had stated vs engine pillar tension in validation notes — this run’s live pillars were used as PDF truth; not re-litigated here

Tân live truth **matches** PO stated truth. Do not treat Tân as an analytical dispute.

Editorial rule for this phase: do not judge engine results except obvious contradiction. The three Follow+not-weak stickers are obvious enough to log.

---

## 23. Evidence for/against Case Thesis Generator

**For (keep; do not rip out):**

- Sơn and Huỳnh body openings are consultations, not god lists.
- Tân vs Sơn now differ at the door despite shared Chính Ấn — the original product question is partially answered.
- Mai’s `Người điều phối` is a person-shaped start.
- Huỳnh vs Sơn body split (kiến tạo vs tự gánh) is the best pair in the set.

**Against (do not expand as the next build):**

- Cover class is not driven by the same thesis (Huỳnh still `Người tự gánh`).
- Non-firing leaves a climate-token executive (Khang, Minh, Tuyền, Phương).
- Mis-assignment: Canh → `Người chỉnh trục` for Tân **and** Trung **and** a weak child.
- Thesis does not constrain Career, Recs, Warnings, Conclusion.

**Product implication:** Case Thesis is a useful *opening component*. It is not a Story Engine, and it is not finished. Next work should **bind thesis through the report and stop wrong reuse**, not add a second generator beside it.

---

## 24. Evidence for/against Story Seed Generator

**Against building now (strong):**

- The dataset already has a seed-like object (Case Thesis). A second generator would stack frameworks while Recs/Conclusion still dump knowledge.
- Collapse is downstream of a stem key (`Canh` / `Đinh` / `Nhâm`), not absence of a seed.
- Children and Follow charts need **suppression of adult career seed**, not more narrative machinery.

**For later (weak, only after repair):**

- When thesis is right, Impact still restates instead of unfolding a life. A seed *might* help progression — after catalogues are banned and UG routing is fixed.

**This phase recommendation:** do **not** build Story Seed Generator next.

---

## 25. Evidence for prioritizing Luck Domain

**For (evidence is clean):** 10 distinct Da Yun labels, 0 interpretations. Customers pay during a decade that is only a timestamp.

**Against prioritizing as the *first* repair:** A Luck paragraph generated by the same stem-routing would produce **ten more interchangeable paragraphs**. Luck on Tân vs Trung would likely still be the Canh essay with a year stamp.

**Priority:** after (or tightly with) collapse repair and life-stage voice — not as the next standalone engine.

---

## 26. Evidence for prioritizing Temperature Domain

**For:** Climate leftovers already leak (`Thu kim vượng cần hỏa`, `giữ ấm / điều hậu mát`, `Thêm hàn khí…`). Huỳnh Water=0 is unused. Tân’s wood-thick / fire-thin is used in the thesis but not as temperature.

**Against first:** Those leftovers are currently **misplaced knowledge**, not a missing chapter customers are asking for. Building Temperature now would add another catalogue.

**Priority:** later; first **stop dumping climate strings into Executive Summary**.

---

## 27. Recommended next 3 product actions

1. **Repair template collapse at Useful God routing + recommendation ritual** — bind one case story through Career/Recs/Conclusion; stop identical rec stacks; kill engine recs. (Product repair plan, not a new engine.)
2. **Make identity one thing** — cover class = body thesis; never empty; never Sơn’s class on Huỳnh.
3. **Ban knowledge catalogues from customer PDF** — Ten God / Shen Sha / Nhật Chủ system notes out of Reasoning and Conclusion; unpublished truth is allowed.

Then, only then: life-stage voice (especially children) and a Luck *interpretation* spike.

---

## 28. What NOT to build next

- Story Seed Generator / Story Engine
- Case Identity Engine as a new framework
- Luck Domain as a large new engine
- Temperature Domain
- New knowledge packs to “fill” Follow or climate
- Narrative Composer rewrite while catalogues still map 1:1 into PDF
- Fabricating 10 more charts to force n=20

Wait for Product Owner review.

---

## 29. Files created

Under `knowledge/editorial_validation/`:

- `README.md`
- `GOLDEN_DATASET_MANIFEST.json`
- `COVERAGE_MATRIX.md`
- `EDITORIAL_VALIDATION_STATUS.md`
- `GOOD_PATTERN_LIBRARY.md`
- `CROSS_CASE_SIMILARITY.md`
- `GOLDEN_DATASET_EDITORIAL_VALIDATION_REPORT.md` (this file)
- `exports/` — 10 production PDFs + HTML sidecars
- `cases/EV-0001` … `EV-0010` — `INPUT.md`, `ANALYTICAL_TRUTH.md`, `PRODUCT_REVIEW.md`, `SCORECARD.json`, `FINDINGS.md`, `PDF.md`
- Working extract: `_extract.json` (live truth + quoted customer text from the same run)

---

## 30. Code changed

**NONE.**

No engine, composer, template, knowledge, or test files were modified. Defects were documented only.

---

## 31. Final verdict

**READY_FOR_PRODUCT_REPAIR_PLANNING**

Provisional (10 genuine distinct real cases; fewer than 20). Not `DATASET_TOO_SMALL`.

Central answer:

> BTE currently produces a consultation for **this** person only at the opening of a few thesis-fired reports (Sơn, Huỳnh, Tân, Mai). From recommendations through conclusion — and for entire Follow/child PDFs — it produces **the same consultation with different BaZi tokens**, keyed more by Useful God than by the life in front of the consultant.

Stop. Wait for Product Owner.
