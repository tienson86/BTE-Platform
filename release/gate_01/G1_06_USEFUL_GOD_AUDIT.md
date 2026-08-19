# G1-06 — Useful God / Dụng · Hỷ · Kỵ Truth & Evidence Audit

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-06 |
| **Document** | `release/gate_01/G1_06_USEFUL_GOD_AUDIT.md` |
| **Phase** | 1 — Audit only |
| **Date** | 2026-08-20 |
| **Status** | AUDIT PASS / G1-06 NOT READY — REPAIR REQUIRED |
| **Scope** | Production Useful God Engine, rules, CASE-0001 candidates, Portal/Report binding |
| **Out of scope** | Engine repair; rule/priority edits; Strength; Temperature; Pattern; Five Elements counting |

Live CASE-0001 was executed read-only through:

`CalendarEngine` → `BaziEngine` → `StrengthEngine` → `TemperatureEngine` → `PatternEngine` → `build_useful_god_context` → `UsefulGodEngine.calculate` → `OrchestratorService.analyze` → `ReportInputV1Adapter`.

No Engine, CSV, or adapter was modified for this audit.

---

# Verdict

| # | Question | Answer |
|---|----------|--------|
| 1 | Production Useful God Engine? | **`engines.useful_god_engine.engine.UsefulGodEngine` V2** (`database/13_useful_god`) |
| 2 | Canonical input? | **`UsefulGodContext`** copied from **`PatternContext`** (after Strength/Temperature overlays) |
| 3 | Strength effect? | Reads **`strength_level` only** (`strong` / `weak` / `balanced`). Does **not** read `strength_score` or Score Engine `45.0`. CASE-0001 `strong` → `str_004` |
| 4 | Temperature / Điều hậu effect? | Reads **`temperature_type`**. Production overlay is still **`temperature_score ≥ 0.65 → hot`**, not G1-04 `climate_state=cold`. CASE-0001 overlay = **`hot`** while published climate = **`cold`** |
| 5 | Pattern effect? | Copies `main_pattern` / `follow_pattern` / `special_pattern`. CASE-0001 `chinh_an` matches **no** special/season-from-pattern rule. Pattern does **not** create the winner |
| 6 | Five Elements effect? | Uses Pattern **`element_distribution`** (stems + hidden = **15**), **not** customer 19-count. `flo_*` matches if the element **key exists**, labeled “quá thịnh” even when count = 1 |
| 7 | Candidates from where? | Six stages: strength, season, temperature, flow, special (+ balance summary, no candidate). CASE-0001: `str_004`, `tmp_002`, `flo_001`–`flo_004` |
| 8 | Winner selection? | `PriorityResolver`: **group priority** then **score** then **rule priority**. Deterministic `max()` |
| 9 | Why Dụng = Thực Thần? | **`str_004`**: `strength_level == strong` (fallback thân vượng). Group **80** beats temperature **70** and flow **60** |
| 10 | Thực Thần ↔ Canh? | G1-01: Canh Kim Dương sinh Nhâm Thủy Dương = **Thực Thần**. Engine **does not store** Nhâm / Thủy; it stores the string **`Thực Thần`** |
| 11 | Why `tmp_002` → Quý loses? | Matches because overlay is **`hot`**. Loses because group **temperature 70 < strength 80**. Not because climate is cold |
| 12 | Hỷ rule? | **Not an independent engine.** Copied from **winning rule** `favorable_gods` JSON. `str_004` → `Thực Thần, Thương Quan` |
| 13 | Kỵ rule? | Same: winning rule `unfavorable_gods`. `str_004` → `Tỷ Kiên, Kiếp Tài` |
| 14 | Portal shows Thập thần; what is stored? | Canonical `data.useful_god.useful_god` is a **bare string**. For this winner it **is** a Ten God name. Other candidates are **stems** (`Quý`, `Canh`, `Nhâm`, …) |
| 15 | Mixing overall UG / Điều hậu / balance / Ten God rec? | **Yes in input and candidate vocabulary.** Display Desktop keeps S01 climate vs S02 Dụng. Report section 07 **co-locates** Dụng/Hỷ/Kỵ with Điều hậu |

---

# PHASE 1 STATUS

**G1-06 PHASE 1: AUDIT PASS / G1-06 NOT READY — REPAIR REQUIRED**

Do not start repair in this phase. Product Owner must choose representation Option A vs B and decide whether correcting the Temperature overlay is allowed to change CASE-0001 winner.

---

## 1. Canonical production implementation

**Canonical module:** `engines/useful_god_engine/`

| Piece | Path |
|-------|------|
| Entry | `UsefulGodEngine.calculate` |
| Context | `utils/context_builder.py` → `UsefulGodContext` |
| Loader | `loader.py` → `database/13_useful_god` |
| Matcher | `matcher.py` (`==`, `contains`, `in`, …) |
| Analyzer | `analyzer.py` (six stages) |
| Calculators | `calculators/{strength,season,temperature,flow,special_case,balance}.py` |
| Priority | `priority.py` `PriorityResolver` |
| Output | `models.py` `UsefulGodResult` |
| Version | Engine **V2**; CSV `reference=BTE-UG-V2`; API view `UsefulGodView@1.0` |

Production call site (`applications/api/services/orchestrator.py`):

```text
build_pattern_context
  → StrengthEngine  (pattern_context.strength_level / strength_score)
  → TemperatureEngine
  → pattern_context.temperature_type = temperature_result.useful_god_temperature_overlay()
  → PatternEngine.calculate
  → build_useful_god_context(pattern_context, pattern_result)
  → UsefulGodEngine.calculate
  → build_useful_god_view → data.useful_god
```

G1-04 comment in Orchestrator: overlay **intentionally frozen until G1-06** so Overall Useful God is not rewritten.

### Other implementations (not production analyze)

| Implementation | Class | Role |
|----------------|-------|------|
| `engines.useful_god_engine` | **canonical** | Live Orchestrator / Report |
| `applications.api.services.useful_god_truth` | presentation adapter | `UsefulGodResult` → `UsefulGodView` |
| `engines.pattern_engine.rule_context_bridge` | overlay | Copies UG into `pattern.dung_than` / RuleContext |
| `engines.report_engine.adapters.report_input_v1_adapter` | adapter | Report V1 fields + G1-04 climate rows |
| `engines.bazi_engine.useful_god.useful_god` | **unused** on analyze | Legacy domain models |
| `engines.analysis_engine.analyzers.useful_god` | **unused** on analyze | Analysis-engine analyzer package |
| `engines/analysis_engine/04_useful_god_engine/` | **legacy docs** | Not imported by Orchestrator |
| `database/15_score_engine/06_useful_god/` | **Score Engine** | Quality scoring, not Dụng selection |
| `database/05_phan_tich/05_dung_than/` | **unused** by UG V2 | Older analysis CSVs |
| `knowledge/packages/useful_god/` | knowledge packs | Not loaded by `UsefulGodLoader` |
| Portal `canonicalDesktopAdapter` / `baziResultAdapter` | presentation helper | Copy `data.useful_god` strings; fallback `pattern.dung_than` |

---

## 2. Dependency graph

```text
G1-02 StrengthResult.strength_level
        ↓
PatternContext.strength_level          G1-04 TemperatureResult
        ↓                                      ├ climate_state  → Portal Điều hậu (cold)
        │                                      └ useful_god_temperature_overlay()
        │                                           score≥0.65 → "hot"   ★ frozen pre-G1-04
        ↓                                      ↓
PatternContext  ←  temperature_type overlay
        ↓
PatternEngine (G1-03 Chính Ấn; does not pick Dụng)
        ↓
UsefulGodContext
        ├ strength_level
        ├ temperature_type     ★ not climate_state
        ├ season / season_phase (from month branch)
        ├ element_distribution (15-tally, Vietnamese keys)
        ├ ten-god family lists (from visible ten_gods_list)
        └ main_pattern / follow_pattern / special_pattern
        ↓
UsefulGodEngine (CSV rules)
        ↓
UsefulGodResult.useful_god / favorable_gods / unfavorable_gods
        ↓
UsefulGodView  →  data.useful_god
        ↓
Desktop S02 / Portal / Full Report / Report V1 HTML·PDF·DOCX
```

Upstream frozen values are **not rewritten** by Useful God. Useful God **does** still consume a **Temperature overlay that disagrees** with frozen `climate_state`.

---

## 3. Rule inventory

Loader `RULE_FILES` (reachable):

| Rule group | File | Rows | Loaded | Reachable | Disabled | Invalid |
|------------|------|------|--------|-----------|----------|---------|
| strength | `01_strength_rules.csv` | 5 (`str_001`–`str_005`) | yes | yes | none (`enabled=true`) | none observed |
| season | `02_season_rules.csv` | 4 (`sea_001`–`sea_004`) | yes | yes | none | none observed |
| temperature | `03_temperature_rules.csv` | 4 (`tmp_001`–`tmp_004`) | yes | yes | none | none observed |
| flow | `04_flow_rules.csv` | 4 (`flo_001`–`flo_004`) | yes | yes | none (stage does not even check `enabled`) | `contains` on dict = **key presence**, not abundance |
| priority | `05_priority_rules.csv` | 5 (`pri_001`–`pri_005`) | yes | yes (group ladder) | none | none observed |
| special | `06_special_rules.csv` | 4 (`spc_001`–`spc_004`) | yes | yes | none | none observed |

Not loaded (orphan relative to engine):

| File | Role |
|------|------|
| `07_examples.csv` | examples only |
| `08_rule_conditions.csv` | condition library; matcher reads JSON on each rule, not this file |

Duplicate `rule_id`: **none** in loaded CSVs.

Priority ladder (from `05_priority_rules.csv` + resolver defaults):

| Group | Group priority |
|-------|----------------|
| special | 100 |
| season | 90 |
| strength | 80 |
| temperature | 70 |
| flow | 60 |

Balance stage computes a summary (`balanced` / `slightly_unbalanced` / `unbalanced` from max−min of the **15-tally**). It **does not** emit a candidate.

---

## 4. Candidate model

Engine public candidate (`UsefulGodEngine._public_candidate`):

| Field | Present |
|-------|---------|
| `rule_id` | yes |
| `rule_group` | yes |
| `useful_god` | yes (Ten God **or** stem — mixed) |
| `priority` | yes (row `priority`) |
| `score` | yes (row `score`) |
| `reason` | yes |
| proposed stem | **no** dedicated field |
| proposed element | **no** |
| proposed Ten God | **only if** CSV `useful_god` happens to be a Ten God |
| status | **no** (active filter happens before list) |
| full evidence object | **no** — one reason string |

`UsefulGodCandidate` dataclass exists but production uses **dicts**. API `UsefulGodView` **drops** `candidate_list` entirely.

Favorable / unfavorable lists live on the **winning row only**, not per-candidate in the public API.

---

## 5. Priority algorithm

```text
winner = max(candidates, key = (group_priority, score, rule_priority))
```

- No rule-id tie-break.
- Equal keys: Python `max` returns the **first** maximal item (stable by candidate append order: strength → season → temperature → flow → special).
- Empty list → `success=False`, `error="no useful god rule matched"`. No hardcoded default god.
- Deterministic for the same context.

---

## 6. CASE-0001 full candidate list

Live context:

| Field | Value |
|-------|--------|
| Day master | Canh |
| `strength_level` | `strong` (G1-02 `0.87`) — **not** Score `45.0` |
| `season` | `winter` |
| `season_phase` | `late_winter` |
| `temperature_type` (UG input) | **`hot`** ← overlay (`score 0.7167 ≥ 0.65`) |
| G1-04 `climate_state` | **`cold`** (not passed into UG matcher) |
| `main_pattern` | `chinh_an` |
| `follow_pattern` / `special_pattern` | none |
| `element_distribution` | `{Hỏa:4, Kim:3, Thổ:5, Mộc:2, Thủy:1}` **sum 15** |
| Customer G1-05 | Mộc 4 · Hỏa 5 · Thổ 6 · Kim 3 · Thủy 1 **sum 19** |
| `officer_elements` | `['Thất Sát']` (Bính vs Canh) |
| `resource_elements` | `['Thiên Ấn']` |
| `companion_elements` | `['Kiếp Tài']` |
| `ten_gods_list` | `Thất Sát, Kiếp Tài, Thiên Ấn` (visible stems only; Nhật Chủ stripped) |

| Candidate | Source | Rule | Group pri | Score | Rule pri | Token in `useful_god` | Evidence | Result |
|-----------|--------|------|-----------|-------|----------|----------------------|----------|--------|
| Thực Thần | Strength | `str_004` | **80** | 0.77 | 76 | Ten God | Thân vượng cần tiết khí | **WINNER** |
| Quý | Temperature | `tmp_002` | 70 | 0.87 | 86 | Stem | Nhiệt khí nặng cần nhuận hạ | lose (group) |
| Canh | Flow | `flo_001` | 60 | 0.76 | 74 | Stem | Mộc quá thịnh cần kim chế | lose |
| Nhâm | Flow | `flo_002` | 60 | 0.76 | 74 | Stem | Hỏa quá thịnh cần thủy chế | lose |
| Đinh | Flow | `flo_003` | 60 | 0.76 | 74 | Stem | Kim quá thịnh cần hỏa luyện | lose |
| Mậu | Flow | `flo_004` | 60 | 0.76 | 74 | Stem | Thủy quá thịnh cần thổ chế | lose |

Did **not** match:

| Rule | Why |
|------|-----|
| `str_003` Chính Quan | needs `officer_elements contains Chính Quan`; chart has **Thất Sát** |
| `str_001`/`str_002` | need `weak` |
| `str_005` | need `balanced` |
| `sea_001` Bính | needs `season=winter` **and** `temperature_type=cold`; overlay is **hot** |
| `sea_002`–`sea_004` | season/phase mismatch |
| `tmp_001`/`tmp_003`/`tmp_004` | type not cold/cool/warm |
| `spc_*` | no tòng / chuyên pattern |

`matched_rules` on API: `str_004, tmp_002, flo_001, flo_002, flo_003, flo_004`.

---

## 7. Winner trace

Sort key for `str_004`: `(80, 0.77, 76)`  
Sort key for `tmp_002`: `(70, 0.87, 86)`  
`80 > 70` → Strength wins even though Temperature has higher row score and higher row priority.

`str_004` is explicitly described in CSV as **“Fallback cho thân vượng”**. The stronger strength rule `str_003` (Chính Quan, priority 82) does not match this chart.

---

## 8. Why Dụng = Thực Thần

1. Rule **`str_004`**.
2. Source: **Strength** (`strength_level == strong`).
3. Group priority **80**.
4. Competitors: `tmp_002` + four `flo_*`.
5. Wins on **group ladder**, not because Temperature is “weaker theoretically”.
6. Canonical stored value: string **`Thực Thần`** (Ten God). Not Nhâm. Not Thủy.

Reasoning published: `Than vượng cần tiết khí`.  
Confidence published: **0.77** (CSV `score` of winner).

---

## 9. `tmp_002` → Quý full trace

CSV:

```text
tmp_002 | temperature | priority 86 | score 0.87
condition: temperature_type == "hot"
useful_god: Quý
favorable: Quý, Nhâm, Tân
unfavorable: Bính, Đinh
reason: Nhiệt khí nặng cần nhuận hạ
```

| Item | Fact |
|------|------|
| Match? | **Yes** on production CASE-0001 |
| Why match? | Overlay maps `temperature_score 0.72` → **`hot`**. Matcher never reads `climate_state` |
| G1-04 climate | **cold** / Hàn / Cần ôn ấm |
| Semantic of rule | Điều hậu **nóng** → stem **Quý** |
| Quý vs Canh (G1-01) | Quý = **Thương Quan**, element **Thủy** |
| Engine stores | **`Quý`** (stem), not Thương Quan |
| Why lose | Group temperature **70 < 80** strength |

This is **not** a G1-01 mapping bug. It is a **Temperature semantic** bug relative to G1-04 freeze: `tmp_002` still means “hot” via the discarded score-as-heat overlay.

If overlay used `climate_state=cold` instead:

- `tmp_002` would **not** match.
- `tmp_001` (Đinh, cold) **would** match (group 70).
- `sea_001` (Bính, winter+cold) **would** match (group **90**).
- Winner would become **`Bính`**, not Thực Thần.

That is why G1-04 froze the overlay. Repairing it in G1-06 **changes Overall Useful God** unless Product also changes the season/strength ladder.

---

## 10. Why `tmp_002` loses

Not because climate is cold (the rule never sees cold).  
Not because Quý is a worse Ten God.  
Because **`pri_003` strength 80 > `pri_004` temperature 70**.

---

## 11. Hỷ thần trace

Not computed by a second matcher. Copied from **winner row** `favorable_gods`.

`str_004`: `["Thực Thần", "Thương Quan"]`.

Order = CSV array order. First item **duplicates Dụng**.

G1-01 for Canh:

| Ten God | Stem | Element |
|---------|------|---------|
| Thực Thần | Nhâm | Thủy |
| Thương Quan | Quý | Thủy |

Engine does **not** store those stems/elements. Presentation would have to derive them (Option A) or wait for Option B fields.

If `tmp_002` had won, Hỷ would be **stems** `Quý, Nhâm, Tân` — a different vocabulary.

---

## 12. Kỵ thần trace

Same mechanism: winner `unfavorable_gods`.

`str_004`: `["Tỷ Kiên", "Kiếp Tài"]`.

Cause: **static CSV on the thân-vượng fallback**, not a separate “strong → kỵ companion” calculator. Strength `strong` is why `str_004` won; Kỵ tokens are whatever that row lists.

G1-01 for Canh:

| Ten God | Stem | Element |
|---------|------|---------|
| Tỷ Kiên | Canh | Kim |
| Kiếp Tài | Tân | Kim |

Canonical meaning in the engine: **two functional roles** listed as strings. It does **not** collapse to “Kim bất lợi”. Presentation currently cannot show `Kim · Tỷ Kiên / Kiếp Tài` without derive.

---

## 13. Ten God ↔ Stem ↔ Element mapping

**G1-01 `ten_god_name(day_master, stem)` is the only canonical map.** Useful God has **no private Ten God table**.

For Nhật chủ **Canh**:

| Stem | Ten God | Element |
|------|---------|---------|
| Nhâm | Thực Thần | Thủy |
| Quý | Thương Quan | Thủy |
| Canh | Tỷ Kiên | Kim |
| Tân | Kiếp Tài | Kim |
| Đinh | Chính Quan | Hỏa |
| Bính | Thất Sát | Hỏa |

Three layers:

| Level | CASE-0001 winner | Stored in UsefulGodResult? |
|-------|------------------|----------------------------|
| A Functional role | Thực Thần | **yes** (`useful_god`) |
| B Stem | Nhâm | **no** |
| C Element | Thủy | **no** |

Candidates **mix A and B** in the same field (`Thực Thần` vs `Quý` vs `Nhâm`). That is not a second mapping; it is **inconsistent token type in CSV `useful_god`**.

BTE does **not** currently persist all three layers. Option A can derive B+C from A **when the token is a Ten God**. Option A is ambiguous when the token is already a stem (`Quý`).

---

## 14. Dụng / Hỷ overlap semantic

`Thực Thần` is both Dụng and first Hỷ.

This is **intended by `str_004` CSV** (favorable list includes the useful god). Not a Portal artifact. Not a second Hỷ engine.

Whether V1.0 should **dedupe** Hỷ is a Product decision. Audit must not strip it.

Two Ten Gods both Thủy: the engine treats them as **two independent role names**, not as “one Hỷ element Thủy”.

---

## 15. Điều hậu separation

| Layer | CASE-0001 | Owner |
|-------|-----------|--------|
| Published climate | Hàn / Cần ôn ấm / `climate_state=cold` | Temperature Engine (G1-04) |
| UG overlay input | `temperature_type=hot` | `useful_god_temperature_overlay()` |
| Overall Dụng | Thực Thần | Strength rule `str_004` |
| Điều hậu candidate | `tmp_002` Quý (matched, lost) | Temperature CSV |
| Genuine winter+cold rule | `sea_001` Bính | **does not match** because overlay ≠ cold |

Desktop: S01 climate rows vs S02 Dụng thần — **labels are separate**.

Report V1 section **07. Dụng thần – Hỷ thần – Kỵ thần** also prints:

- Điều hậu nhiệt ← `climate_state` (`Hàn`)
- Nhu cầu điều hòa ← `balancing_need`
- Căn cứ khí hậu

It does **not** replace `Dụng thần` with Quý. It **co-locates** two layers in one section.

**BLOCKER 12 as specified (Điều hậu overwrite Overall without priority evidence):** **No.** Overlay does not overwrite the winner; group priority keeps `str_004`. Mixing is **presentation/contract** (same Report section; overlay still `hot` internally).

**BLOCKER 4 / 6:** **Yes.** UG still consumes pre-G1-04 heat-axis overlay; `tmp_002` still fires.

---

## 16. Five Elements interaction

Customer structural distribution (G1-05): **19**.  
UG `element_distribution`: **15** (visible stems + hidden occurrences; **no** branch bản hành).

`flo_*` condition: `element_distribution contains "Mộc"` etc.

Matcher `contains` on a **dict** = **key in dict**. Any present element matches “quá thịnh”:

- Mộc 2 → `flo_001` “Mộc quá thịnh”
- Hỏa 4 → `flo_002` “Hỏa quá thịnh”
- Kim 3 → `flo_003` “Kim quá thịnh”
- Thủy **1** → `flo_004` “Thủy quá thịnh”

No Thổ flow rule. Highest 15-tally element is **Thổ 5**, unused.

This is **not** “lowest count → Dụng”. It is **presence → 克泄 stem**, then **lowest group priority**.

No rule: `min(count) → useful god`.  
No rule uses customer 4/5/6/3/1.

**BLOCKER 5:** flow semantic treats internal 15-tally **presence** as abundance/strength, conflicting with G1-05 (count ≠ strength) and even with the 15-tally magnitudes (Thủy 1 ≠ thịnh).

---

## 17. Strength interaction

Reads **`strength_level`** only (`== strong|weak|balanced`).

Does **not** read:

- `StrengthResult.strength_score` (`0.87`)
- `score.strength_score` (`45.0`)
- `pattern.than_vuong_nhuoc`

CASE-0001 `strong` → `str_004` (and would also match `str_003` if `Chính Quan` were in `officer_elements`).

---

## 18. Pattern interaction

- `main_pattern=chinh_an` is copied; **no CSV condition** on `main_pattern`.
- `month_branch_ten_god=Chính Ấn` is on context; **no UG rule reads it**.
- Special rules need `follow_pattern` / `special_pattern` — empty on CASE-0001.
- Pattern identification is **not** overridden.
- After UG, `merge_upstream_into_rule_context` + `enrich_result_from_rule_context` copies Dụng/Hỷ/Kỵ onto **`pattern.dung_than`**. That is a **mirror**, not a Pattern-calculated god.

Portal fallback `pattern.dung_than` on the live path is the **same** Useful God string.

---

## 19. UsefulGodResult contract

| Field | Engine | API `UsefulGodView` |
|-------|--------|---------------------|
| `useful_god` | yes | yes |
| `favorable_gods` | yes | yes |
| `unfavorable_gods` | yes | yes |
| `candidate_list` | yes (dicts) | **dropped** |
| `matched_rules` | yes | yes |
| `confidence` | winner CSV score | yes |
| `reasoning` | winner reason | yes |
| `temperature_reason` / `season_reason` / `strength_reason` | first candidate of that stage | **dropped** |
| `balance_reason` | yes | **dropped** |
| stem / element / Ten God split | **no** | **no** |
| winning rule id | only inside `metadata.trace.winner` and as first of `matched_rules` | `matched_rules` list, not a dedicated field |
| evidence object | reason string only | reason string |

---

## 20. Portal / Report / PDF / DOCX binding

Exact CASE-0001 strings:

| Surface | Dụng | Hỷ | Kỵ | Source |
|---------|------|----|----|--------|
| API `data.useful_god` | Thực Thần | Thực Thần, Thương Quan | Tỷ Kiên, Kiếp Tài | `UsefulGodView` |
| Canonical Desktop S02 | same | `join(", ")` of arrays | same | `data.useful_god`; fallback `pattern.dung_than` |
| Full Report | `useful.useful_god \|\| pattern.dung_than` | `favorable_gods \|\| pattern.hy_than` | same | no recount |
| Report V1 / PDF / DOCX | `ReportUsefulGodV1.useful_god` | arrays | arrays | adapter copies view; fallback Pattern mirror |
| Report section 07 extra | — | — | — | G1-04 climate fields, **not** `tmp_002` Quý |

Renderers **do not** recompute Useful God. They **do not** map Ten God → stem/element.

Portal shows Thập thần because **the winner token is a Ten God name**. It is not a separate “Ten God recommendation engine”.

---

## 21. Test coverage

Existing `tests/useful_god/`:

| File | What it covers | CASE-0001 / overlay / collision |
|------|----------------|----------------------------------|
| `test_engine.py` | weak+cold synthetic returns some god | no |
| `test_priority.py` | special group beats strength | no CASE list |
| `test_matcher.py` | `contains` | no dict-key abundance |
| `test_loader.py` | groups load | no inventory |
| `test_analyzer.py` | stages run | no |
| `test_context_builder.py` | field copy | no |
| `test_regression.py` | 1970–1990 not 95% one god | no |

G1-04 `test_case_0001_useful_god_overlay_frozen_until_g1_06` **locks overlay=`hot` and winner=`Thực Thần`**. That documents the freeze; it is not a climate-correct UG test.

Gaps vs requested matrix: strong/weak/balanced; cold/hot; pattern collision; 0-count element; Strength vs Temperature vs Pattern equal priority; stem-vs-Ten-God token type; API vs Report equality (exists indirectly via report G1-03/04).

---

## 22. Blockers

| ID | Spec blocker | Finding |
|----|--------------|---------|
| 1 | CASE-0001 Dụng not traceable | **No.** `str_004` |
| 2 | Portal self-derives Dụng/Hỷ/Kỵ | **No** on live path (copy). Fallback to Pattern mirror of the same engine |
| 3 | Reads Score `strength_score=45` | **No.** `strength_level` only |
| 4 | Reads `0.72` as hot after G1-04 | **YES.** `useful_god_temperature_overlay()` |
| 5 | Treats 4/5/6/3/1 as strength | **Partial/YES.** Does not use 19-count; `flo_*` treats **15-tally key presence** as “quá thịnh” (including Thủy=1) |
| 6 | `tmp_002` uses discarded Temperature semantic | **YES.** Matches `hot` overlay while climate is `cold` |
| 7 | Ten God mapping ≠ G1-01 | **No private map.** Token **type** mixed (Ten God vs stem) |
| 8 | Pattern input ≠ G1-03 | **No.** `chinh_an` / Chính Ấn |
| 9 | Winner not deterministic | **No.** |
| 10 | Hỷ/Kỵ not traceable | **No.** Winning CSV columns |
| 11 | API ≠ Report Dụng | **No.** Both Thực Thần |
| 12 | Điều hậu overwrites Overall without priority | **No overwrite.** Co-location + frozen overlay |
| 13 | Missing element auto-Dụng | **No.** |
| 14 | Stem/Ten God/Element self-contradict | **YES as representation.** Same field holds `Thực Thần` and `Quý`/`Nhâm` depending on winner |

Additional audit blockers (same class as 4/6):

- `sea_001` (winter + cold → Bính), the rule that would match **actual** G1-04 climate, is **suppressed** by the hot overlay.
- Repairing overlay without Product decision **flips CASE-0001 winner** Strength `Thực Thần` → Season `Bính`.

---

## 23. Gap classification

| Gap | Layer |
|-----|--------|
| Overlay `score→hot` vs frozen `climate_state=cold` | **semantic** (Temperature→UG contract) |
| `tmp_002` still matches hot | **rule** + **semantic** |
| `flo_*` “quá thịnh” = dict key present | **rule** + **semantic** (Five Elements) |
| 15-tally vs customer 19 | **contract** (documented G1-05; UG must not substitute) |
| `useful_god` CSV mixes Ten God and stem | **contract** / **semantic** |
| No stem/element on result | **contract** |
| API drops `candidate_list` | **adapter** / **contract** |
| Hỷ = copy of winner including Dụng | **semantic** (intended CSV) |
| Report §07 co-locates Điều hậu with Dụng | **presentation** |
| `pattern.dung_than` mirror | **adapter** (safe if UG present) |
| Tests lock overlay=`hot` | **test** |
| No CASE-0001 candidate-table test | **test** |
| Balance summary unused | **calculation** (dead output) |
| `08_rule_conditions.csv` unused | **rule** (orphan file) |

---

## 24. Minimum changes required for G1-06 PASS

Audit-only: **do not implement here.**

1. **Product: Overall vs Điều hậu after overlay unfreeze.**  
   If `temperature_type` becomes `climate_state` (`cold`):
   - `tmp_002` stops matching;
   - `sea_001` matches and **wins** (group 90) → Dụng **`Bính`** unless season/strength priorities change.
   Decide whether V1.0 Overall Dụng stays Strength-based (`Thực Thần`) or becomes climate `sea_*` / `tmp_*`.

2. **Product: representation Option A vs B** (below). Do not redesign the engine without that choice.

3. **Stop mixing token types** in `useful_god` (all Ten God, or all stem, or three explicit fields).

4. **Flow rules:** stop treating key presence as “quá thịnh”; do not use customer 19-count as strength; keep 15-tally internal and named as such if retained.

5. **Publish** winning `rule_id`, candidate list, and (if Option B) stem/element. Portal/Report remain copy-only.

6. **Tests:** CASE-0001 candidate table; overlay vs `climate_state`; Strength vs Temperature vs Season collision; `flo_*` must not fire on count=1 as “thịnh”; API=Report; G1-01 mapping for winner; Hỷ/Kỵ source = winner row.

7. Do **not** change Strength/Temperature/Pattern/Five Elements **formulas**. Only the **UG input field** and UG rules/priority if Product requires.

---

# Canonical concepts (as implemented)

### Dụng thần

Production winner is a **single CSV string**. On CASE-0001 it is a **Ten God** (`Thực Thần`). Other rules emit a **Heavenly Stem**. It is **not** a structured candidate object on the API. It is **not** an element. Combination only exists as Hỷ/Kỵ **lists on the same row**.

### Hỷ thần

**Derived from the winning rule**, not ranked independently, not “second candidate”. Duplicate of Dụng is **CSV-intended**.

### Kỵ thần

**Derived from the winning rule**, not opposite-element math, not a Strength calculator beyond “this row matched because `strong`”.

---

# PRODUCT OWNER DECISIONS REQUIRED

## Representation

Engine currently stores **one string** (Ten God **or** stem) + two string lists.

Presentation example `Thủy · Nhâm · Thực Thần` is **not** in the payload. Canonical G1-01 **can** derive it **when the token is a Ten God**.

**Option A** — Derive Ngũ hành / Can from canonical Ten God + Day Master using G1-01. No engine schema change. Fails or is ambiguous if winner is already a stem (`Quý`, `Bính`).

**Option B** — Extend `UsefulGodResult` / `UsefulGodView` with explicit `ten_god`, `stem`, `element` (and the same for Hỷ/Kỵ).

**Do not auto-choose.**

## Overall Dụng vs Điều hậu

Today: Overall = Strength `Thực Thần`; Điều hậu display = Hàn / Cần ôn ấm; hidden UG climate input = **hot**.

Unfreezing overlay to G1-04 climate **changes the winner** to season `Bính` under current `pri_002=90 > pri_003=80`.

Product must say whether that flip is desired.

## Dụng inside Hỷ

Report as **intended CSV duplication**, not a bug, until Product asks to dedupe.

---

# Minimum presentation proposal (not implemented)

Canonical calculation **supports** the two-layer example **only via Option A + G1-01**, and **only while the winner remains a Ten God**:

```text
Dụng thần    Thủy · Nhâm · Thực Thần
Hỷ thần      Thủy · Thực Thần / Thương Quan
Kỵ thần      Kim · Tỷ Kiên / Kiếp Tài
```

If Product unfreezes overlay and `sea_001` wins, the stored token is **`Bính`** (stem). The example above would be **wrong** unless Option B (or stem→Ten God via G1-01: Bính = Thất Sát / Hỏa for Canh).

Do not force CASE-0001 UI to that example until representation + overlay decisions are made.

---

Stop. Do not edit Useful God Engine, rule database, priority, Strength, or Temperature.

G1-06 PHASE 1: AUDIT PASS / G1-06 NOT READY — REPAIR REQUIRED
