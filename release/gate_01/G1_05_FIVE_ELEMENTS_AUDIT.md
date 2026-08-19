# G1-05 — Five Elements / Ngũ hành Truth & Evidence Audit

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-05 |
| **Document** | `release/gate_01/G1_05_FIVE_ELEMENTS_AUDIT.md` |
| **Phase** | 1 — Audit only |
| **Date** | 2026-08-19 |
| **Status** | READY FOR PRODUCT OWNER REVIEW |
| **Scope** | Calculation Truth → Evidence → Semantic → Presentation tối thiểu |
| **Out of scope** | Engine repair; Score/Strength/Portal/Report edits; Deep Interpretation; Useful God selection |

This report does not modify Engine, Rule Database, Score, Strength, Temperature, Pattern, Ten Gods, Useful God, Portal, or Report.

Live CASE-0001 was executed read-only through `CalendarEngine` → `BaziEngine` → `RuleContextBuilder._build_wuxing` → `OrchestratorService.analyze`.

---

# Verdict

| # | Question | Answer |
|---|----------|--------|
| 1 | `Mộc 4 · Hỏa 5 · Thổ 6 · Kim 3 · Thủy 1` is what? | **Structural occurrence count** (unweighted). Not seasonal strength. Not `wuxing_score`. |
| 2 | Why total = 19? | **4 Thiên can + 4 Địa chi (bản hành) + 11 tàng can occurrences** = 19. Model C. |
| 3 | Thiên can? | Each visible stem **+1** to its element. No weight, season, polarity, or position. |
| 4 | Địa chi? | Each branch **+1** to **bản hành of the chi** (Dần→Mộc, Sửu→Thổ, Ngọ→Hỏa). |
| 5 | Tàng can? | Each hidden-stem **occurrence +1**. Main/middle/residual qi are **equal**. Duplicates count twice. |
| 6 | Weighting on this counter? | **No.** Every contribution is `1`. (A unused calculator uses hidden `0.5` — not production.) |
| 7 | Nguyệt lệnh / mùa in the count? | **No.** Count ignores month command, solar term, and Temperature. |
| 8 | Đắc lệnh / đắc địa / thông căn in the count? | **No.** Those belong to Strength / Score, not this distribution. |
| 9 | Another Five Elements score? | **Yes.** Score Engine `wuxing_score` (quality 0–100). CASE-0001 live = **0.0**. Distinct. |
| 10 | Portal / Report / PDF / DOCX source? | Primary: `data.five_elements` ← `RuleContext.wuxing.counts`. Report V1 golden = 4/5/6/3/1. |
| 11 | Count called strength? | **Yes on Canonical Desktop S04** (Mạnh/Yếu, “vượng / thiếu”). Contract also labels count≥3 as `EXCESS`. |
| 12 | CASE-0001 traceable per unit? | **Offline yes** (formula + BaZi lists). **API no** — payload is aggregates only. |

Canonical production owner of the **customer distribution** is **not** Score Engine, despite `beta/BETA0_ANALYTICAL_TRUTH_LOCK.md`. Live owner:

```text
BaziEngine.hidden_stems / pillars
    → RuleContextBuilder._build_wuxing
    → PatternResult.rule_context["wuxing"]["counts"]
    → build_five_elements_payload
    → data.five_elements
```

Interpretation ownership map already says `five_elements: RuleContext.wuxing`.

---

# BLOCKERS

| ID | Rule | Finding | Layer |
|----|------|---------|-------|
| **B3** | Count presented as element strength | Canonical Desktop S04 title **CÂN BẰNG NGŨ HÀNH**; adapter maps count **percentage** to `Rất mạnh / Mạnh / Trung bình / Yếu / Rất yếu`; summary `{max} vượng • {min} thiếu • Điểm {score.grade}`. CASE-0001 Thổ=6 → “Mạnh/vượng”; Thủy=1 → “Rất yếu/thiếu”. `4` is occurrence, not power. | presentation |
| **B4** | Dual Five Elements systems, one chart | (A) structural count 4/5/6/3/1. (B) `wuxing_score` quality dimension (live **0.0**). S04 mixes **Score grade** into the count chart. Legacy `presenters/summary_builder.js` binds **`score.wuxing_score`** as a single “Ngũ hành” bar when the key exists. | semantic / adapter |
| **B10** | Useful God reads a different count | UG / Pattern / Strength / Temperature `element_distribution` = **visible stems + hidden stems only** (CASE-0001 total **15**). Customer `five_elements` = stems + **branch bản hành** + hidden (**19**). Same chart, two totals. UG flow CSV `flo_*` matches `element_distribution contains "Mộc"` as “Mộc quá thịnh”. | contract / G1-06 |
| **B11** | Legacy fallback can replace canonical distribution | Report V1 and Desktop fall back to `score.wuxing_series` if `five_elements` is empty. Today series is a **copy of counts**, so numbers match. If series meaning changes, surfaces diverge. | adapter |

Not blockers (checked):

| Rule | Result |
|------|--------|
| CASE-0001 `4/5/6/3/1` cannot be reconstructed | **False.** Live `_build_wuxing` and API payload match. |
| Portal vs Report V1 different numbers | **False** on the analytical path. Both 4/5/6/3/1. |
| Renderer invents a third count | **False.** S04 only derives **% and status labels** from the same counts. |
| Hidden-stem weights non-deterministic | **False** on production (always +1). |
| Count uses lunar month | **False.** Count does not read calendar month at all. |
| Strength G1-02 rewritten from FE count | **False.** Strength uses its own stem+hidden distribution + CSV rules. |
| Missing element auto-becomes Overall Useful God | **False on CASE-0001** (no zero). UG winner remains Strength `Thực Thần`. Flag `flo_*` / Score `Khuyết hành` for G1-06, do not repair here. |
| Branch+hidden double-count accidental | **False as a bug in this counter.** It is the **documented arithmetic** of `_build_wuxing` (Model C). Whether theory should do that is a Product question, not an implementation accident. |

---

# 1. Canonical production source

Exact function that creates CASE-0001 `Mộc 4`:

`engines/rule_contract/context_builder.py` → `RuleContextBuilder._build_wuxing`

Called from `RuleContextBuilder.build` when Pattern Engine publishes RuleContext via `ContextEngine.to_rule_context`.

Field path:

```text
rule_context["wuxing"]["counts"]["wood"] = 4
rule_context["wuxing"]["wood"] = {"status": "EXCESS", "count": 4}
```

API / Portal:

```text
applications.api.services.five_elements_truth.build_five_elements_payload
    payload["five_elements"]["wood"]["count"] = 4
    payload["five_elements"]["counts"]["wood"] = 4
```

Report V1:

```text
ReportInputV1Adapter._build_five_elements
    source.five_elements.counts / [element].count
    → ReportFiveElementsV1.wood = 4.0
```

Do **not** create a new Five Elements engine. The counter already exists.

`FiveElementCalculator` (`engines/bazi_engine/five_elements/calculator.py`) is **not** on the production analyze path. Its formula is stem 1 + branch 1 + hidden **0.5** → CASE-0001 would be **13.5**, not 19.

---

# 2. Inventory

| Implementation | Role | Model | Live V1.0? |
|----------------|------|-------|------------|
| `RuleContextBuilder._build_wuxing` | **Canonical production count** | Model C: stem+1, branch bản hành+1, hidden occurrence+1 | **Yes** |
| `build_five_elements_payload` | Adapter / SSOT for API | Copies `wuxing.counts` | **Yes** |
| `ScoreEngine._build_wuxing_series` | Copies counts into `score.wuxing_series` | Same 4/5/6/3/1 as floats | **Yes** (duplicate field) |
| `WuxingScoreCalculator` | Score Engine quality dimension | CSV 02_wuxing + weights; 0–100 | **Yes**, but **not** the chart numbers |
| Pattern / Strength / Temperature `element_distribution` | Internal stem+hidden tally | Model B-ish: **no** branch bản hành; CASE-0001 **15** | Yes, engines only |
| `FiveElementCalculator.calculate_balance` | Legacy weighted balance | hidden 0.5; metadata `stem_1_branch_1_hidden_0.5` | **Unused** on Orchestrator |
| Desktop `fiveElementCounts` / `analyticalFiveElementCounts` | Presentation | Reads `data.five_elements` | **Yes** |
| Desktop S04 `ELEMENT_STATUS(pct)` | Presentation inference | % of total → Mạnh/Yếu | **Yes** |
| `summary_builder.js` / `metrics.js` | Legacy | Can show **`wuxing_score` scalar** as “Ngũ hành” | Legacy JS |
| Interpretation `FiveElementsInterpretationFacts` | Copy of API counts | Explicitly not `wuxing_score` | Yes |
| Knowledge CSV / sentence library | Knowledge, not this counter | — | Unused for 4/5/6/3/1 |

---

# 3. Exact formula (production)

```text
for each of 4 pillars:
    counts[element(stem)]   += 1
    counts[element(branch)] += 1   # bản hành of 地支
for each item in BaziChart.hidden_stems:   # flat list, duplicates kept
    counts[element(hidden)] += 1
```

Maps: `STEM_ELEMENT` / `BRANCH_ELEMENT` in `context_builder.py`.

Hidden list producer: `engines/bazi_engine/engine.py`

```text
hidden = [stem for pillar in pillars for stem in HIDDEN[pillar.branch]]
```

Status labels on the same object (not shown as the numeric 4/5/6/3/1, but stored):

| count | `wuxing.{element}.status` |
|------:|---------------------------|
| 0 | `MISSING` |
| 1 | `PRESENT` |
| 2 | `STRONG` |
| ≥3 | `EXCESS` |

CASE-0001: Mộc/Hỏa/Thổ/Kim = `EXCESS`; Thủy = `PRESENT`. Aggregate `wuxing.status` = `EXCESS`.

**Five Elements distribution is structural occurrence, not seasonal strength.**

---

# 4. CASE-0001 full reconstruction

Chart: **Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần**. Nhật chủ Canh.

Hidden list (11, order from engine):

`Giáp, Bính, Mậu, Kỷ, Quý, Tân, Đinh, Kỷ, Giáp, Bính, Mậu`

## Provenance (each +1)

| Source | Position | Stem/Branch | Element | Contribution |
|--------|----------|-------------|---------|-------------:|
| Thiên can | Năm | Bính | Hỏa | 1 |
| Địa chi bản hành | Năm | Dần | Mộc | 1 |
| Tàng can | Năm / Dần | Giáp | Mộc | 1 |
| Tàng can | Năm / Dần | Bính | Hỏa | 1 |
| Tàng can | Năm / Dần | Mậu | Thổ | 1 |
| Thiên can | Tháng | Tân | Kim | 1 |
| Địa chi bản hành | Tháng | Sửu | Thổ | 1 |
| Tàng can | Tháng / Sửu | Kỷ | Thổ | 1 |
| Tàng can | Tháng / Sửu | Quý | Thủy | 1 |
| Tàng can | Tháng / Sửu | Tân | Kim | 1 |
| Thiên can | Ngày | Canh | Kim | 1 |
| Địa chi bản hành | Ngày | Ngọ | Hỏa | 1 |
| Tàng can | Ngày / Ngọ | Đinh | Hỏa | 1 |
| Tàng can | Ngày / Ngọ | Kỷ | Thổ | 1 |
| Thiên can | Giờ | Mậu | Thổ | 1 |
| Địa chi bản hành | Giờ | Dần | Mộc | 1 |
| Tàng can | Giờ / Dần | Giáp | Mộc | 1 |
| Tàng can | Giờ / Dần | Bính | Hỏa | 1 |
| Tàng can | Giờ / Dần | Mậu | Thổ | 1 |
| **Total** | | | | **19** |

## Totals by element

| Element | Stems | Branch bản hành | Hidden | **Sum** |
|---------|------:|----------------:|-------:|--------:|
| Mộc | 0 | Dần+Dần = 2 | Giáp+Giáp = 2 | **4** |
| Hỏa | Bính = 1 | Ngọ = 1 | Bính+Đinh+Bính = 3 | **5** |
| Thổ | Mậu = 1 | Sửu = 1 | Mậu+Kỷ+Kỷ+Mậu = 4 | **6** |
| Kim | Tân+Canh = 2 | 0 | Tân = 1 | **3** |
| Thủy | 0 | 0 | Quý = 1 | **1** |

Live API: `five_elements.counts = {wood:4, fire:5, earth:6, metal:3, water:1}`, `dominant=earth`, `missing=[]`.

---

# 5. Heavenly Stem contributions

CASE-0001 visible stems, each **+1**, no extras:

| Stem | Element | Contribution |
|------|---------|-------------:|
| Bính | Hỏa | 1 |
| Tân | Kim | 1 |
| Canh | Kim | 1 |
| Mậu | Thổ | 1 |

Not season-adjusted. Not yin/yang-adjusted. Not position-weighted (Năm = Tháng = Ngày = Giờ).

---

# 6. Earthly Branch contributions — Model C

Not Model A alone (chi only). Not Model B alone (hidden only).

Each chi contributes:

1. **+1 bản hành** of the branch;
2. **plus** each tàng can **+1**.

| Branch | Bản hành +1 | Hidden +1 each |
|--------|-------------|----------------|
| Dần (năm) | Mộc | Giáp Mộc, Bính Hỏa, Mậu Thổ |
| Sửu | Thổ | Kỷ Thổ, Quý Thủy, Tân Kim |
| Ngọ | Hỏa | Đinh Hỏa, Kỷ Thổ |
| Dần (giờ) | Mộc | Giáp Mộc, Bính Hỏa, Mậu Thổ |

Example: Dần adds Mộc from the chi **and** Mộc from Giáp. That is why the total exceeds 8.

---

# 7. Hidden Stem contributions

- Each occurrence **+1**.
- Main / middle / residual qi: **same weight**.
- Counted **in addition to** branch bản hành.
- Same stem in two branches: **two counts** (Giáp on both Dần; Bính on both Dần; Kỷ on Sửu and Ngọ; Mậu on both Dần).

CASE-0001 hidden occurrences = **11**. Proven.

---

# 8. Why total = 19

```text
4 stems + 4 branch-elements + 11 hidden occurrences = 19
```

This is the live `_build_wuxing` model. It is **not** 4+11=15 (that is `element_distribution` in Pattern/Strength/Temperature).

---

# 9. Count vs Strength

Two systems exist.

### A. Structural occurrence (customer chart)

`Mộc 4 · Hỏa 5 · Thổ 6 · Kim 3 · Thủy 1`

### B. Other “power” numbers

| System | What it is | CASE-0001 |
|--------|------------|-----------|
| Strength Engine | Nhật chủ vượng/nhược | **0.87 / strong** (G1-02 frozen) |
| Score `wuxing_score` | Quality of wuxing dimension | **0.0** |
| Score `grade` | Overall report grade | D+ on launch fixture / live score payload |
| Unused `FiveElementCalculator` | Weighted 0.5 hidden | 13.5 if it ran |

**Must not** present `Mộc 4` as `Mộc mạnh 4`. Desktop currently does the equivalent via % → Mạnh and “vượng”.

Thổ having the **highest count** must not be used as proof that **Thổ is the strongest useful force** or that Strength is Thổ. Strength is about the Day Master (Canh / Kim), frozen separately.

---

# 10. `wuxing_score` semantic

| Item | Finding |
|------|---------|
| Formula | `WuxingScoreCalculator` = generic CSV matcher on `database/15_score_engine/02_wuxing/*` + `wuxing_weight.csv`; then Pack 03 module score 0–100 |
| Range | 0–100 (normalizer clamp) |
| Semantic | **Chart quality / balance score**, including PRESENT/STRONG/MISSING/EXCESS **penalties** (`ES016+` “Khuyết Mộc”, `WX007` Khuyết hành, `WX006` quá vượng) |
| Input | RuleContext `wuxing.*` statuses derived from **the same counts** |
| Related to count? | Indirectly: count buckets become MISSING/STRONG/EXCESS which the scorer consumes |
| On Portal chart? | Canonical Desktop / Full Report / PDF **do not** use the scalar as the 4/5/6/3/1 bars. **S04 summary injects `score.grade`.** Legacy JS can show the scalar as “Ngũ hành” |
| Adapter swap? | `wuxing_series` is a **count copy**, not the scalar. Fallback is same numbers today, different field |

G1-02 analogue: Score was once bound as Strength. Here the **scalar** is mostly not bound as the bars, but **grade / Mạnh-Yếu** still contaminate the distribution UI.

---

# 11. Season / month interaction

Count: **none**.

`wuxing.season` is filled from **calendar `solar_month`** (`SEASON_BY_MONTH`), not from BaZi month branch. CASE-0001 month 1 → `winter` / `season_status=IN_SEASON`. That flag is **not** added into 4/5/6/3/1.

Đắc lệnh, thông căn, Temperature, solar term **do not** enter this counter.

---

# 12. Strength interaction

Strength `element_distribution` = visible stems + hidden stems (**15** on CASE-0001), used as context, not as the published Strength score.

G1-02 Strength remains `0.87 / strong` from Strength CSV. It does **not** conclude “Thổ mạnh nhất vì count 6”.

---

# 13. Useful God interaction

Overall Useful God CASE-0001: **Thực Thần** (Strength group). Not edited in this audit.

UG reads `UsefulGodContext.element_distribution` copied from **PatternContext** (15-count, Vietnamese keys), **not** `data.five_elements` (19-count).

| UG use | Behavior |
|--------|----------|
| `run_balance_stage` | dominant / weakest / spread from that 15-count; stored as `balance_reason`, **not** the winner by itself |
| `flo_001`–`flo_004` | `element_distribution contains "Mộc"` etc. labeled “quá thịnh cần chế”. Presence-like match, group priority 60 (below Strength 80) |
| Missing → Dụng thần | **No** dedicated “khuyết hành = Dụng thần” rule found in UG CSV |

**G1-06:** review `flo_*` “contains” vs “quá thịnh”, and the 15 vs 19 mismatch. Do not change UG in G1-05.

---

# 14. Missing-element behavior

| Layer | count = 0 |
|-------|-----------|
| `_build_wuxing` | status `MISSING` |
| `build_five_elements_payload` | key listed in `missing[]` |
| Score CSV | “Khuyết Mộc/Hỏa/…” **score penalty** (`ES016+`, `WX007`) |
| Customer Desktop | weakest row labeled **thiếu** even when count is **1** (CASE-0001 Thủy) |
| Useful God winner | not auto-assigned from missing |

Zero means **does not appear in this structural counter**, not automatically **cần bổ hành** in V1.0 consulting copy — except Score penalties and Desktop “thiếu”.

CASE-0001 has **no** zero. Huynh fixture used in tests has Thủy **0**.

---

# 15. Evidence availability

| Needed | Present? |
|--------|----------|
| Aggregates 4/5/6/3/1 | Yes — `five_elements.counts` |
| Per-row source type / pillar / stem / contribution | **No** on the API contract |
| Hidden list | Yes — `BaziChart.hidden_stems` (11 strings), `rule_context.hidden_stems.flat` |
| Why Hỏa = 5? | Reconstructable by auditors from BaZi + formula; **not** machine-published as a contribution table |

Phase 1 does not redesign the contract.

---

# 16. Portal / Report / PDF / DOCX binding

| Surface | Title | Values CASE-0001 | Source | Recompute? |
|---------|-------|------------------|--------|------------|
| Canonical Desktop S04 | **CÂN BẰNG NGŨ HÀNH** | 4/5/6/3/1 + **%** + Mạnh/Yếu | `data.five_elements`; else `score.wuxing_series` | % and status only |
| Canonical Desktop S02 | Ngũ hành | **“Thổ nổi”** (max count) | same counts | max() |
| Result page FiveElementsCard | NGŨ HÀNH | count + status + S04 summary | Desktop VM | no new count |
| Full Report | Ngũ hành | 4/5/6/3/1 | `analyticalFiveElementCounts` | no |
| Report V1 HTML/PDF/DOCX | 03. Ngũ hành | 4.0 … 1.0 | `five_elements.analytical_counts` | no |
| Golden `expected_report_input.json` | — | wood 4, fire 5, earth 6, metal 3, water 1 | same | — |
| Legacy executive JS | Ngũ hành | **`wuxing_score` (0)** if key present | Score scalar | different quantity |

All analytical V1.0 surfaces that bind `five_elements` show **the same 4/5/6/3/1**. The **labels** around those numbers do not.

S04 also appends overall **Điểm {grade}** into the five-element summary.

---

# 17. Representative regression coverage

Existing tests cover **adapter mapping** (Huynh 2/7/4/4/0, water=0) and “not `wuxing_score` as the bar values” (`canonical_result_routing.test.ts` F).

**Gaps** (no Phase 1 tests added):

1. CASE-0001 live 4/5/6/3/1 invariant;
2. chart with a true 0;
3. duplicate branches (two Dần);
4. repeated hidden stems;
5. visible + hidden same element;
6. branch bản hành ≠ hidden mix (Sửu Thổ vs Quý Thủy);
7. tied counts;
8. `sum == 8 + len(hidden_stems)`.

Counting is deterministic from the traced code; tests do not yet lock CASE-0001 identity for this gate.

---

# 18. Invariants (if this model is frozen)

If Product keeps Model C:

```text
sum(five_elements.counts) == 4 + 4 + N
N == len(BaziChart.hidden_stems)
CASE-0001: N = 11 → total 19
```

Do **not** apply this invariant to Pattern/Strength `element_distribution` (no branch bản hành).

---

# 19. Legacy / duplicate fields

| Field | Meaning |
|-------|---------|
| `five_elements.*.count` | Canonical customer occurrence |
| `wuxing.counts` | Same, upstream |
| `score.wuxing_series[].value` | Copy of counts |
| `score.wuxing_score` / `five_elements_score` | Quality score |
| `element_distribution` (Pattern/Strength/Temp/UG) | 15-count, no chi bản hành |
| `FiveElementCalculator` scores | Unused 0.5 model |
| `wuxing.{el}.status` EXCESS/MISSING | Count buckets, worded as strength |

---

# 20. Gap classification

| Gap | Type |
|-----|------|
| Desktop Mạnh/Yếu / vượng / thiếu / “Thổ nổi” from occurrence | **presentation / semantic** |
| S04 title “Cân bằng” + injecting `score.grade` | **presentation** |
| BETA0 owner = Score Engine vs live RuleContext.wuxing | **contract** |
| 19-count vs 15-count `element_distribution` | **contract** (G1-06 for UG) |
| No contribution evidence on API | **contract / evidence** |
| Legacy `wuxing_score` as “Ngũ hành” bar | **adapter / legacy** |
| Score CSV “Khuyết hành” / EXCESS from raw count | **semantic** (Score, not V1.0 chart) |
| CASE-0001 FE identity tests missing | **test** |
| Hidden 0.5 calculator unused | **legacy** (do not silently activate) |

Calculation of 4/5/6/3/1 on the production path is **internally consistent**. The freeze is blocked by **semantic/presentation**, not by an unreconcilable total.

---

# 21. Minimum changes required for G1-05 PASS (Phase 2 — do not implement now)

1. Freeze **Model C occurrence** as V1.0 “Phân bố Ngũ hành” (Option A unless Product picks B).
2. Presentation: title **Phân bố Ngũ hành**; show 4/5/6/3/1; optional compact note `Thiên can · Địa chi · Tàng can` and `Tổng đơn vị cấu trúc: 19`.
3. Remove Desktop **Mạnh/Yếu / vượng / thiếu** derived from count %. Do not call Thổ “mạnh nhất” from 6.
4. Do not put `wuxing_score` or overall `grade` on this chart.
5. Keep Report/Portal/PDF/DOCX on `data.five_elements` only; do not use Score as distribution.
6. Do not enable `FiveElementCalculator` 0.5 on the live path without a new Product decision.
7. Add CASE-0001 + `sum = 8 + N` tests. Do not change Golden except identity if a later repair changes published numbers (not expected if Model C stays).
8. Leave Useful God / Strength / Temperature counters as-is; record 15 vs 19 for **G1-06**.
9. No Deep Interpretation (bổ hành, tài vận, sức khỏe).

---

# Product Owner decision required

BTE has **both**:

- structural element **count** (19 units, live chart);
- a separate **wuxing quality score** (and an unused weighted 0.5 calculator).

UI currently has **one** chart and dresses the count as balance/strength.

Per gate rules this audit **does not choose Option B**.

### Option A (recommended for V1.0 freeze)

Show only **Phân bố Ngũ hành** (occurrence). Keep `wuxing_score` technical / Score dimension.

### Option B

Show two widgets: Phân bố Ngũ hành **and** Sức mạnh / điểm Ngũ hành (`wuxing_score`), clearly separated.

Do not merge them into one bar labeled both “4” and “mạnh”.

---

# PHASE 1 STATUS

`G1-05 PHASE 1: AUDIT PASS / G1-05 NOT READY — REPAIR REQUIRED`

Repair is **presentation + semantic + tests**, not a new engine, and not a change to the 4/5/6/3/1 arithmetic unless Product rejects Model C.

---

**STOP.** No Five Elements / Score / Strength / Temperature / Pattern / Ten Gods / Useful God / Portal / Report code was changed. Wait for Product Owner review before Phase 2.
