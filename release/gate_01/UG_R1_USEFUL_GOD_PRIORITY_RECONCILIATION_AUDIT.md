# UG-R1 — Useful God Priority Reconciliation Audit

**Phase:** 1 — audit only. **No engine, CSV, priority, Strength, Pattern, Temperature, Five Elements, or Hỷ/Kỵ change.**  
**Date:** 2026-08-20  
**Primary case:** Vũ Thị Thanh Tuyền · Giáp Tý / Tân Mùi / Mậu Thân / Quý Hợi · Nhật chủ Mậu  
**Upstream after G1-X01 (frozen for this audit):** Strength `0.66 / strong / raw 16` · Pattern `kiep_tai` / Kiếp Tài / `pat_ktai_01` · Temperature `hot` / Nhiệt · Cần làm mát · G1-05 occurrence Mộc3 · Hỏa1 · Thổ4 · Kim3 · Thủy6 (sum 17)

Current Overall Dụng: **Thủy · Nhâm · Thiên Tài** (`sea_002`).

Reference ChatGPT path (Mộc / conditional Thủy) is **comparison only**, not an oracle.

---

## Production implementation inventory

Canonical V1.0 Useful God is **UsefulGodEngine V2**, not the Knowledge Board `bz_07_useful_god_priority` package.

| Piece | Path |
|-------|------|
| Engine | `engines/useful_god_engine/engine.py` |
| Context builder | `engines/useful_god_engine/utils/context_builder.py` |
| Loader | `engines/useful_god_engine/loader.py` |
| Matcher | `engines/useful_god_engine/matcher.py` |
| Candidate pipeline | `engines/useful_god_engine/analyzer.py` + `calculators/{strength,season,temperature,flow,special_case,balance}.py` |
| Priority | `engines/useful_god_engine/priority.py` · `PriorityResolver.resolve` |
| Token enrich | `engines/useful_god_engine/roles.py` (G1-01 `ten_god_name` / `stem_for_ten_god`) |
| Result | `engines/useful_god_engine/models.py` · `UsefulGodResult` |
| Rule source | **`database/13_useful_god`** (`DEFAULT_DATABASE_PATH`) |

Not production:

| Asset | Fact |
|-------|------|
| `knowledge/packages/useful_god/priority` (`bz_07`) | Explicitly **not wired** to Analysis Engine (`assumptions_and_limitations.md`) |
| `knowledge/golden_dataset/04_useful_gods` | Framework only — **zero** CASE records |
| `07_examples.csv`, `08_rule_conditions.csv` | **Not loaded** |

Orchestrator: Strength + Temperature overlay → Pattern → `build_useful_god_context` → `UsefulGodEngine.calculate`.

---

## 1. Rule-group inventory

Loader `RULE_FILES` + `status==active`. All loaded rows are `active` / `enabled=true`.

| Group | File | Loaded | Active / reachable in code | Group priority | Purpose | Candidate type |
|-------|------|------:|---------------------------:|---------------:|---------|----------------|
| special | `06_special_rules.csv` | 4 | 4 (`spc_001`–`spc_004`) | 100 | Tòng / chuyên override | Ten God token |
| season | `02_season_rules.csv` | 4 | 4 (`sea_001`–`sea_004`) | 90 | Month-season (+ climate on 001/002) | Stem token |
| strength | `01_strength_rules.csv` | 5 | 5 (`str_001`–`str_005`) | 80 | Thân vượng / nhược / trung hòa | Ten God token |
| temperature | `03_temperature_rules.csv` | 4 | 4 (`tmp_001`–`tmp_004`) | 70 | CSV labels these **điều hậu** | Stem token |
| flow | `04_flow_rules.csv` | 4 | 4 (`flo_001`–`flo_004`) | 60 | Unique-max ngũ hành 克 | Stem token |
| balance | *(no CSV)* | 0 | summary only | — | spread status; **no candidate** | none |
| pattern-main | — | 0 | **none** | — | `main_pattern` is copied onto context; **no rule reads `kiep_tai`** | — |
| fallback god | — | 0 | none | — | empty candidates → `success=False` | — |

**Reachable as *winner* in production** (Strength always populated):

- special, season, strength — yes.
- temperature, flow — match as **losing** candidates only (see §2 / §22). Strength covers `weak|strong|balanced`, group 80 > 70 > 60.

Stage filters: season / temperature / flow / special check `status`. Strength also checks `enabled`. No other reachability gate.

---

## 2. Priority algorithm (exact)

From `PriorityResolver.resolve` and `05_priority_rules.csv`:

```text
winner = max(candidates, key = (group_priority, row_score, row_priority))
```

Group map: special 100, season 90, strength 80, temperature 70, flow 60  
(`pri_001`–`pri_005`; same defaults hard-coded in resolver if CSV missing).

Answers:

| # | Question | Answer |
|---|---------|--------|
| 1 | Group priority absolute? | **Yes.** First tuple field. A season row always beats any strength/temperature/flow row. |
| 2 | Priority outrank candidate score? | **Yes.** `tmp_002` score 0.87 loses to `sea_002` score 0.88 *and* would lose to `str_004` score 0.77 because 70 < 80. |
| 3 | Specificity? | **No** extra specificity layer. Row `priority` is only the third key. |
| 4 | Candidate confidence? | Row `score` copied to result `confidence`. Not a separate model. |
| 5 | Veto / reconciliation stage? | **None.** `balance_summary` is unused. No incompatible-winner check. |
| 6 | Can lower-priority reject higher? | **No.** |
| 7 | Tie-breaker? | Python `max` on equal keys returns the **first** maximal item. Append order: strength → season → temperature → flow → special. |
| 8 | Multiple Dụng coexist? | **No.** One Overall winner. Hỷ/Kỵ are lists on that row, not extra Dụng slots. |
| 9 | Winner supplies Hỷ/Kỵ? | **Yes.** `favorable_gods` / `unfavorable_gods` of the winning CSV row only. |

Documented ladder (implementation, not classical treatise):

- `database/13_useful_god/CHANGELOG.md`: “Priority order applied from database: **special > season > strength > temperature > flow**.”
- `05_priority_rules.csv` `pri_002` reason: “Season high priority” / description “Season rules second priority” / reference `BTE-UG-V2`.
- G1-06 freeze: group priorities **unchanged** 90 / 80 / 70 / 60.

No Product Manifesto / G1-04 text states “调候 is Overall Dụng.” G1-04 freeze criterion 8: **“Điều hậu is not Overall Useful God.”**

---

## 3–4. Season group and `sea_002`

| Rule | Trigger | Token | Intended CSV theory |
|------|---------|-------|---------------------|
| `sea_001` | `season==winter` **and** `temperature_type==cold` | Bính | Đông hàn → hỏa ôn ấm |
| `sea_002` | `season==summer` **and** `temperature_type==hot` | Nhâm | Hạ nhiệt → thủy điều hậu |
| `sea_003` | `season_phase in {early_spring, mid_spring}` | Canh | Xuân mộc → kim |
| `sea_004` | `season_phase in {early_autumn, mid_autumn}` | Đinh | Thu kim → hỏa |

### What is sufficient for `sea_002` to match?

**Exactly two predicates, AND:**

1. `context.season == "summer"`
2. `context.temperature_type == "hot"`

Nothing else.

### Tuyền condition trace

| Condition | Source | Value | Match |
|-----------|--------|-------|-------|
| `season == summer` | month branch **Mùi** → `summer` / `late_summer` | summer | yes |
| `temperature_type == hot` | G1-04 `climate_state` overlay after G1-06 | `hot` | yes |

### `sea_002` required questions

| | Question | Answer |
|--|----------|--------|
| A | Match simply because summer + hot? | **Yes.** |
| B | Inspect `StrengthResult`? | **No.** |
| C | Inspect `PatternResult`? | **No.** (`follow_pattern` unused here) |
| D | Inspect current Water presence? | **No.** |
| E | Inspect Nhâm/Quý visible or hidden? | **No.** (Nhâm is hidden in Thân; Quý is hour stem — unused) |
| F | Inspect Five Elements weighted strength? | **No.** |
| G | Inspect structural distribution? | **No.** |
| H | Inspect root/support of Day Master? | **No.** |
| I | Distinguish Điều hậu cần Thủy vs Overall Dụng = Thủy? | **No.** CSV reason/description are điều hậu; group 90 makes the row Overall Dụng. |

Mark: **`sea_002` does not distinguish Điều hậu cần Thủy from Overall Dụng thần = Thủy.**

---

## 5. Why priority 90?

Evidence that exists:

1. CSV `pri_002` = 90, text “Season high priority”.
2. CHANGELOG v2.0.0 business-data assumption: special > season > strength > temperature > flow.
3. G1-06 repair/freeze **kept** that ladder and **accepted** CASE-0001 winner `sea_001` (winter+cold → Bính as Overall).

Evidence that does **not** exist:

- No classical 调候-优先 treatise bound to this number.
- G1-04 freeze: Điều hậu ≠ Overall Useful God.
- G1-06 freeze text: “Điều hậu stays Temperature climate/need” **and** “Overall Useful God from rule groups + priority” — while the frozen CASE-0001 Overall **is** a season climate rule.

**Interpretation**

| Option | Fit |
|--------|-----|
| A — Seasonal/Điều hậu absolute over Strength | **Operationally true** in code + G1-06 CASE-0001 freeze. |
| B — Season is a candidate that still needs reconciliation | **Not implemented.** G1-06 audit asked this Product question; V2 only ranks. |
| C — Implementation convenience, no documented theoretical hierarchy | **Origin.** CHANGELOG calls it a **business-data assumption**. `pri_002` does not cite a theory pack. |

Critical distinction: V1.0 **behavior** is A. V1.0 **theory documentation** is C plus a G1-04/G1-06 wording clash. That is not a coherent published hierarchy.

---

## 6. Temperature vs season

Both exist because CSV split “mùa/nguyệt lệnh” vs “hàn nhiệt / điều hậu”, then ranked season above temperature (`pri_004` description: **“Temperature fallback”**).

Tuyền:

| Rule | Group | Stem | Ten God vs Mậu | Reasoning |
|------|-------|------|----------------|-----------|
| `sea_002` | 90 | Nhâm | Thiên Tài / Thủy | summer + hot → thủy |
| `tmp_002` | 70 | Quý | Chính Tài / Thủy | `hot` → nhuận hạ |

| Season knows | Temperature knows |
|--------------|-------------------|
| `season` / `season_phase` (Mùi → summer) | only `temperature_type` |
| `sea_002` also requires `hot` | `tmp_002` is `hot` alone |

For Tuyền both encode **“nóng / hạ → Water stem”**. Different stems (Nhâm vs Quý), same element.

**`POTENTIAL REASONING DUPLICATION`** — not scoring duplication: only `sea_002` can win.

Because every chart with `strength_level` matches a `str_*` rule, **temperature can never win** (70 < 80) unless Strength is absent. Live golden: **temperature winners = 0**. The “fallback” group is dead as Overall.

---

## 7. Strength candidate (Tuyền)

Matched: **`str_004` only**.

| | |
|--|--|
| Trigger | `strength_level == strong` (no officer/Ấn extra clause) |
| CSV token | Thực Thần |
| G1-01 map Mậu | Thực Thần → **Canh** / Kim |
| Group key | `(80, 0.77, 76)` |
| Reason | “Than vượng cần tiết khí” |

`str_003` (Chính Quan when `officer_elements contains Chính Quan`) does **not** match: Tuyền `officer_elements = ['Thất Sát']` (Giáp). Ất = Chính Quan is not in that list.

**Balancing principle for strong Mậu Thổ in Strength group:** drain/output (食伤), not 官杀 control, unless Chính Quan is already listed. Fallback `str_004` always fires on `strong`.

Loses solely because 80 < 90.

---

## 8. Pattern candidate

After G1-X01: `kiep_tai`. Context `main_pattern=kiep_tai`, `follow_pattern=None`, `special_pattern=None`.

No `spc_*` / `str_*` / `sea_*` / `tmp_*` / `flo_*` condition reads `main_pattern` or `kiep_tai`.

**`NO PATTERN-SPECIFIC USEFUL-GOD RECONCILIATION`.**

---

## 9. Flow candidate `flo_004`

| | |
|--|--|
| Trigger | `element_distribution contains Thủy` |
| Predicate (G1-06) | **unique maximum** of stored counts, not key presence |
| Source | PatternContext stems + hidden (**not** G1-05 17-count card) |
| Tuyền engine dist | Mộc3 · Kim2 · Thổ3 · Thủy**4** · Hỏa1 (sum **13**) |
| Unique max | Thủy 4 > 3 → match |
| Token | **Mậu** / Thổ / Tỷ Kiên (DM already Mậu) |
| Group key | `(60, 0.76, 74)` |
| G1-05 Thủy=6 | unused by this matcher |

G1-06 unique-max repair is **intact** (Thủy=1 would not match).

**Does flow treat structural occurrence as element strength?**  
It treats **internal occurrence counts** as “quá thịnh” (CSV reason). That is **not** G1-05 customer strength, and **not** StrengthEngine. Documentation basis: CSV wording + G1-06 matcher docstring (“relative dominance of the stored counts”). No rule says G1-05 Thủy6 = Water strength.

---

## 10. Special candidates (Tuyền)

| Rule | Needs | Tuyền | Match |
|------|-------|-------|-------|
| `spc_001` | `follow_pattern == tong_tai` | `None` (G1-X01) | **no** |
| `spc_002` | `tong_quan` | no | no |
| `spc_003` | `tong_sat` | no | no |
| `spc_004` | `special_pattern in {khuc_truc, viem_thuong, nhuan_ha, gia_sac}` | none | no |

`spc_001` correctly does not fire.

---

## 11. Complete Tuyền candidate table

All matcher hits (no omitted match). Non-matches listed below.

| Rank | Rule | Group | Group pri | Candidate | Stem | Element | Ten God | Match reason | Winner? |
|-----:|------|-------|----------:|-----------|------|---------|---------|--------------|---------|
| 1 | `sea_002` | season | 90 | Nhâm | Nhâm | Thủy | Thiên Tài | summer + hot | **YES** |
| 2 | `str_004` | strength | 80 | Thực Thần | Canh | Kim | Thực Thần | strong → tiết khí | no |
| 3 | `tmp_002` | temperature | 70 | Quý | Quý | Thủy | Chính Tài | hot → nhuận hạ | no |
| 4 | `flo_004` | flow | 60 | Mậu | Mậu | Thổ | Tỷ Kiên | unique-max Thủy | no |

Did not match: `str_001` `str_002` `str_003` `str_005` `sea_001` `sea_003` `sea_004` `tmp_001` `tmp_003` `tmp_004` `flo_001` `flo_002` `flo_003` `spc_001`–`spc_004`.

Balance: `slightly_unbalanced` (spread 3) — not a candidate.

---

## 12. Winner proof

Keys:

```text
sea_002  (90, 0.88, 88)
str_004  (80, 0.77, 76)
tmp_002  (70, 0.87, 86)
flo_004  (60, 0.76, 74)
```

`90 > 80 > 70 > 60` → **`sea_002`**. No tie. Nhâm / Thủy / Thiên Tài via G1-01 (`Mậu` controls `Nhâm` = Thiên Tài).

Why others lose: lower group priority only. No veto that Water is already unique-max, that Nhâm is already hidden, that Pattern is Kiếp Tài, or that Strength wants output Metal.

---

## 13. Water abundance

G1-05 Thủy=6 is occurrence, **not** Water strength. This audit does not argue “count high ⇒ cannot be Dụng” from that card alone.

Useful God **has no** check for:

- candidate already abundant / unique-max;
- candidate already visible or hidden;
- candidate rooted;
- candidate excess vs scarcity.

Flow’s “quá thịnh” is a **separate** candidate (`Mậu`), not a veto on `sea_002`.

> Current Useful God selection does not reconcile candidate abundance/presence.

Model fact, not automatically a defect.

---

## 14. Overall Dụng vs Điều hậu

G1-04 canonical Điều hậu: `climate_state` + `balancing_need` (Tuyền: `hot` / `cooling` · Nhiệt · Cần làm mát). Explicit freeze: Điều hậu **is not** Overall Useful God.

G1-06 Overall: one winner from ranked groups. Season rows **are written as điều hậu** (`sea_002` description: “mệnh nhiệt ưu tiên thủy điều hậu”). Group 90 makes them Overall whenever they match.

**`Điều hậu is functionally dominating Overall Useful God through season priority`.**

Intended?

- G1-04: **no** (Điều hậu ≠ Overall).
- G1-06 freeze text: Điều hậu stays Temperature; Overall is UG winner — **fields** are separate on the payload.
- G1-06 CASE-0001 freeze **chose** `sea_001` as Overall — same mechanism as Tuyền `sea_002`.

Presentation still shows G1-04 Điều hậu beside UG Dụng. For Tuyền they **happen to agree** on cooling/Water. That is ranking coincidence, not a reconciliation stage.

---

## 15. Reconciliation matrix (Tuyền)

| Layer | Says | Candidate implication |
|-------|------|------------------------|
| Strength | strong Mậu Thổ | `str_004` Canh / Thực Thần (drain) |
| Pattern | Kiếp Tài | **none** in UG |
| Season | summer + hot | `sea_002` Nhâm / Thủy (**wins**) |
| Temperature | Nhiệt / Cần làm mát | `tmp_002` Quý / Thủy (duplicate climate; loses) |
| Five Elements structural | Water occurrence high (G1-05=6; engine unique-max=4) | `flo_004` Mậu; **does not block** Nhâm |
| Useful God | Nhâm / Thủy | season group 90 |

> These layers are **ranked**, not reconciled.

---

## 16. Old Mộc path vs BTE Thủy path

Reference report (not oracle): Mậu has Earth foundation; use **Mộc** to control/direct Earth; Thủy may help **conditionally**; do not add Thổ/Hỏa.

| | Reference | BTE V2 |
|--|-----------|--------|
| Path | Structural 抑身 / 官杀 (Mộc) | Seasonal/climate priority (Thủy stem) |
| Thủy | Conditional Hỷ | Overall Dụng (`sea_002`) |
| Thổ | Avoid adding | `flo_004` proposes Mậu (loses); Strength is already strong Earth |
| Pattern | unused in that memo | unused in UG |

Conceptual difference: **control-the-body** vs **调候-as-Overall via group 90**. Both can be schools; BTE implements only the second as the published Dụng.

---

## 17. Can BTE generate Mộc for this chart?

Scan of `database/13_useful_god` `useful_god` tokens: **no Giáp, Ất, or Mộc** as proposed Dụng.

Control-adjacent:

- `str_003` → Chính Quan → for Mậu that is **Ất / Mộc**, but requires `officer_elements contains Chính Quan`. Tuyền has **Thất Sát** (Giáp), not Chính Quan.
- `spc_002`/`spc_003` → Quan/Sát only on tòng.

**`Current Useful God rulebase has no reachable Mộc-balancing path for this configuration.`**

Giáp is on the chart and maps to Thất Sát; no strong-DM Thất Sát rule exists.

---

## 18. Five Day Master coverage (obvious holes only)

| Intended family | Rule | Hole |
|-----------------|------|------|
| Strong → output/drain | `str_004` always if `strong` | reachable |
| Strong → control/officer | `str_003` **Chính Quan only** | Thất Sát-present strong charts (Tuyền) get **no** 官杀 candidate |
| Weak → resource | `str_001`/`str_002` | reachable |
| Climate Water/Fire | `sea_001`/`sea_002` | become Overall, not a parallel slot |
| Pattern 劫财 | — | no rule |

No new rules added in this audit.

---

## 19. Multi-objective model

V2 supports **one Overall winner**. Stages emit parallel *candidates*, then collapse.

There are **not** separate published objects for:

- primary Dụng;
- Điều hậu Dụng;
- balance Dụng;
- pattern Dụng.

G1-04 TemperatureView is the only separate Điều hậu **presentation**. UG season/tmp rows compete for the **same** Overall seat.

This explains Tuyền: climate candidate and strength candidate cannot both be true; climate wins by ladder.

---

## 20. Hỷ / Kỵ consequence

Winner `sea_002` sets:

- Hỷ: Nhâm, Quý, Canh → Thủy · Nhâm · Thiên Tài / Thủy · Quý · Chính Tài / Kim · Canh · Thực Thần  
- Kỵ: Bính, Đinh → Hỏa · Bính · Thiên Ấn / Hỏa · Đinh · Chính Ấn

`str_004` would have published a different Hỷ/Kỵ (食伤 vs 比劫). No second pass checks Pattern Kiếp Tài, Water unique-max, or G1-04 beyond the overlay already used to *match* `sea_002`.

> Hỷ/Kỵ inherit winner-row theory and are not independently reconciled.

---

## 21. Control-case traces

All four PO regression charts: **season wins**.

| Case | Strength | Climate overlay | Pattern | Winner rule/group | Group pri |
|------|----------|-----------------|---------|-------------------|----------:|
| Nguyễn Tiến Sơn | 0.87 strong | cold | `chinh_an` | `sea_001` / season · Hỏa · Bính · Thất Sát | 90 |
| Lương Ngọc Huỳnh | 0.64 balanced | cool | `chinh_tai` | `sea_004` / season · Hỏa · Đinh · Kiếp Tài | 90 |
| Đặng Thị Dung | 0.24 weak | hot | `sat_an` | `sea_002` / season · Thủy · Nhâm · Chính Ấn | 90 |
| Đoàn Quang Hưng | 0.61 balanced | cool | `thuc_than` | `sea_004` / season · Hỏa · Đinh · Thiên Ấn | 90 |
| Vũ Thị Thanh Tuyền | 0.66 strong | hot | `kiep_tai` | `sea_002` / season · Thủy · Nhâm · Thiên Tài | 90 |

Dung: Strength candidates `str_001`/`str_002` (Ấn) **exist** and lose to `sea_002`. Weak body + climate Water as Overall is the same overreach pattern as Tuyền, opposite Strength theory.

Sơn: G1-06-frozen shape (climate season beats `str_004`).

---

## 22. Season dominance rate

`knowledge/golden_dataset/04_useful_gods` has **no** populated cases. Live recompute of **`tests/golden_dataset/inputs` (n=101)** through the production pipeline (not editing Golden expected files):

| Winning group | Count | % |
|---------------|------:|--:|
| season | 71 | **70.3** |
| strength | 18 | 17.8 |
| special | 12 | 11.9 |
| temperature | 0 | 0.0 |
| flow | 0 | 0.0 |

**`PRIORITY DOMINANCE`.** Season wins whenever `sea_*` matches. Temperature/flow never win while `strength_level` is set. Not labelled a correctness defect until Product theory is chosen; it is the mechanical consequence of 90 > 80 > 70 > 60 plus universal `str_*` coverage.

---

## 23. Model classification (documentation, not preference)

| Model | Documentation | Implementation |
|-------|---------------|----------------|
| **A Hierarchical** | CHANGELOG + `pri_002` + G1-06 CASE-0001 freeze | **This is what runs** |
| **B Reconciliation** | G1-06 audit Product question; not built | **Missing** |
| **C Multi-Dụng** | G1-04: Điều hậu ≠ Overall; G1-06: “Điều hậu stays Temperature” | **Collapsed:** season điều hậu text occupies Overall |

Intended model in **frozen G1-06 behavior** = A (one ranked Overall).  
Intended model in **G1-04 freeze language** = C (separate Điều hậu).  
Reconciliation (B) is **not** in V2.

The Tuyền contradiction is therefore expected under A and incomplete under B/C.

---

## 24. Blocker findings (`REVIEW REQUIRED`)

| # | Condition | Mark |
|---|-----------|------|
| 1 | Priority 90 has no documented **theoretical** basis (only CSV/CHANGELOG assumption + G1-06 keep) | **YES** |
| 2 | Season and Temperature duplicate summer/hot → Water | **YES** (`POTENTIAL REASONING DUPLICATION`) |
| 3 | Overall Dụng is effectively Điều hậu when `sea_001`/`sea_002` match | **YES** |
| 4 | Strength/Pattern cannot veto incompatible seasonal winner | **YES** |
| 5 | Candidate presence/excess never reconciled; flow “quá thịnh” does not veto climate Water | **YES** |
| 6 | Strong Mậu has no reachable Mộc/control candidate | **YES** |
| 7 | Hỷ/Kỵ inherited blindly from winner row | **YES** |
| 8 | Winner hierarchy is implementation convenience vs G1-04 “Điều hậu is not Overall” | **YES** |

---

## Minimum repair options *(not implemented)*

Product must pick one V1.0 story before freeze:

1. **Confirm Model A in writing:** 调候/`sea_*` is Overall Dụng; keep Nhâm for Tuyền; accept Dung Ấn loss; document G1-04 Điều hậu as *labels only*.
2. **Model B:** keep one Overall but add reconciliation (e.g. climate cannot win if proposed element is unique-max; or Strength may veto).
3. **Model C:** publish Điều hậu Dụng (`sea_*`/`tmp_*`) **beside** Overall (Strength/Pattern); stop letting group 90 overwrite Overall.
4. Deduplicate `sea_002` vs `tmp_002` (one climate family).
5. If control path is in-scope: officer rule for Thất Sát / Mộc — **only if Product asks**; not in this audit.

Do **not** retune Strength, Five Elements, Temperature climate, Pattern, or force Mộc to match the old reference.

---

## Files consulted (read-only)

`engines/useful_god_engine/**`, `database/13_useful_god/**`, `release/gate_01/G1_04_TEMPERATURE_FREEZE_CHECKLIST.md`, `G1_06_USEFUL_GOD_AUDIT.md`, `G1_06_USEFUL_GOD_REPAIR_REPORT.md`, `G1_06_USEFUL_GOD_FREEZE_CHECKLIST.md`, `knowledge/packages/useful_god/priority/documentation/assumptions_and_limitations.md`.

Live traces: Tuyền + Sơn + Huỳnh + Dung + Hưng; 101 golden inputs winner-group counts.

---

UG-R1: USEFUL GOD PRIORITY / ĐIỀU HẬU OVERREACH — REVIEW REQUIRED
