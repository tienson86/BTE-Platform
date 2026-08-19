# G1-04 — Temperature / Điều hậu Truth & Evidence Audit

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-04 |
| **Document** | `release/gate_01/G1_04_TEMPERATURE_AUDIT.md` |
| **Phase** | 1 — Audit only |
| **Date** | 2026-08-19 |
| **Status** | READY FOR PRODUCT OWNER REVIEW |
| **Scope** | Calculation Truth → Evidence → Presentation tối thiểu |
| **Out of scope** | Deep Interpretation; engine repair; Portal/Report repair; new Điều hậu algorithm; Strength/Pattern/Useful God edits |

This report does not modify Engine, Rule Database, Strength, Pattern, Useful God, Portal, or Report.

No new Temperature engine is proposed. Canonical implementation already exists.

Live CASE-0001 was executed read-only through `CalendarEngine` → `BaziEngine` → `StrengthEngine` → `build_temperature_context` → `TemperatureEngine.calculate` → `OrchestratorService.analyze`.

---

# Verdict

| Question | Result |
|----------|--------|
| Canonical Temperature Engine exists? | **Yes** — `engines/temperature_engine` |
| New engine required? | **No** |
| Engine computes climate scores + level? | **Yes** — `cold/cool/warm/hot` + 0–1 `temperature_score` + dry/humid components |
| Canonical Temperature score exists? | **Yes** — `TemperatureResult.temperature_score` (0–1). Distinct from Score Engine `score.temperature_score` |
| Taxonomy Hàn / Nhiệt / Táo / Thấp? | **Partial.** Level is `cold/cool/warm/hot`. Dry/humid are **component scores**, not a combined 4-way class. Report V1 labels exist: Hàn / Lương / Ôn / Nhiệt / Táo / Thấp |
| “Điều hậu” owned by Temperature Engine? | **No first-class Dụng thần điều hậu.** Engine returns **recommendation strings**. Useful God has a separate `tmp_*` stem candidate |
| Engine returns hành/can điều hậu? | **Not as a dedicated field.** Recommendations are free text (`Tăng Hỏa…`). Useful God `tmp_002` would pick **Quý** if it won (it does not) |
| Why Report `Điều hậu: —`? | **Adapter field mismatch** on Full Report: reads `temperature.dieu_hau` / `label` / `status` / `level`. Canonical field is `temperature_level` |
| Strength `Ấn mùa lạnh +10` from Temperature? | **No.** Strength `spc_004` uses Strength’s own `season` |
| Temperature rewrite Pattern `Chính Ấn`? | **No.** Pattern CSV does not read temperature |
| Temperature feeds Useful God? | **Yes** — `PatternContext.temperature_type` overlay. Candidate exists; **winner is Strength Dụng thần** |
| Portal / Report / PDF bind the same field? | **No** |
| G1-04 freeze-ready today? | **No** |

---

# BLOCKERS

| ID | Rule | Finding | Layer |
|----|------|---------|-------|
| **B1** | `Điều hậu: —` while Engine has a result | Full Report `temperatureText()` reads `dieu_hau \| label \| status \| level`. `TemperatureView` publishes `temperature_level`. Empty string → `kv(…, "—")`. Engine **did** return `hot` / `0.72` / recommendations. | adapter / presentation |
| **B2** | Portal and Report use two Temperature sources | (1) Full Report → missing keys → `—`. (2) Report V1 PDF/DOCX → `useful_god.temperature_adjustment` = `temperature.temperature_level` → **Nhiệt**. (3) Legacy pattern presenter → `pattern.dieu_hau` = **Đắc lệnh** labeled Điều hậu. | adapter / presentation |
| **B8** | Renderer tự suy ra Điều hậu | Legacy `presenters/pattern.js` maps keys `dieu_hau, climate, tiao_hou…` on **pattern**, not Temperature. `pattern.dieu_hau` is month 得令 status (`Đắc lệnh`), explicitly **not** temperature (`rule_context_bridge` comment). | presentation |
| **B9** | Same CASE, multiple climate classifications | Context `climate_type=cold` / `season=winter` vs published `temperature_level=hot`. Both are live engine facts on CASE-0001. | calculation / contract |

Not blockers (checked):

| Rule | Result |
|------|--------|
| Lunar month used instead of BaZi solar-term month | **False.** Season is mapped from **BaZi month branch** (Sửu). Calendar month pillar is solar-term (`Đại Hàn`). Lunar month 12/1986 is unused. |
| Strength G1-02 rewritten by Temperature | **False.** Strength runs first. Temperature does not write Strength. |
| Temperature score bound as confidence | **False** on current surfaces (Full Report binds nothing; confidence is `1.0`, score is `0.72`). |
| Useful God reads a non-canonical Temperature field | **False as source.** It reads `temperature_type` copied from `TemperatureResult.to_pattern_temperature_type()`. |
| Fallback hides missing context on CASE-0001 | **False.** Nine rules match. `success=True`. |
| Pattern primary overwritten | **False.** CASE-0001 remains `pat_ca_01` / Chính Ấn. |

---

# 1. Canonical production implementation

## 1.1 Production owner (frozen)

`beta/BETA0_ANALYTICAL_TRUTH_LOCK.md` assigns Temperature to:

```text
Temperature
    engines/temperature_engine
```

It must not be folded into Strength.

Public entry:

```text
from engines.temperature_engine import TemperatureEngine
from engines.temperature_engine.utils.context_builder import build_temperature_context

ctx = build_temperature_context(bazi_chart, calendar=calendar,
                                strength_level=..., strength_score=...)
result = TemperatureEngine().calculate(ctx)
```

| Item | Value |
|------|-------|
| Canonical module | `engines/temperature_engine` |
| Public class | `TemperatureEngine` |
| Public method | `TemperatureEngine.calculate(context) -> TemperatureResult` |
| Input model | `engines.temperature_engine.context.TemperatureContext` |
| Output model | `engines.temperature_engine.models.TemperatureResult` |
| Context builder | `utils/context_builder.py` `build_temperature_context` |
| Analyzer | `analyzer.py` `TemperatureAnalyzer` |
| Calculators | `calculators/{season_temperature,climate,dryness,humidity,special_case,flow,balance}` |
| Matcher | `matcher.py` `TemperatureMatcher` |
| Scorer | `scorer.py` `TemperatureScorer` |
| Priority / level | `priority.py` `TemperaturePriorityResolver` |
| Rule loader | `loader.py` `TemperatureLoader` |
| Rule database | `database/11_temperature` **V2 / 1.0.0** (2026-07-29) |
| Default DB path | `database/11_temperature` |
| API view | `applications.api.services.temperature_truth.build_temperature_view` → `TemperatureView` |
| Engine `__version__` | **not published** in `__init__.py` (README: “Temperature Engine V2”) |

Production callers:

| Caller | What it does |
|--------|----------------|
| `applications/api/services/orchestrator.py` | Stage 3.6: `build_temperature_context` → `TemperatureEngine.calculate` → `pattern_context.temperature_type = result.to_pattern_temperature_type()` → `analysis.temperature = TemperatureView` |
| `applications/production/engine_runner.py` | Same |

## 1.2 Other Temperature / Điều hậu implementations

| Module | Classification | Production leak? |
|--------|----------------|------------------|
| `engines/temperature_engine` | **canonical** | Yes — Orchestrator / production runner |
| `database/11_temperature` | **canonical rules** | Yes |
| `engines/score_engine/calculators/temperature_score.py` | **Score module** (0–100 harmony) | Yes as `score.temperature_score`, **not** Điều hậu |
| `database/15_score_engine/10_temperature/` | Score rules | Score only |
| `engines/useful_god_engine/calculators/temperature.py` + `database/13_useful_god/03_temperature_rules.csv` | Useful God **Điều hậu candidate** | Yes as UG candidates; **not** `AnalysisResult.temperature` |
| `engines/pattern_engine` `dieu_hau` | **misnamed** month 得令 / season_status | Yes on `data.pattern.dieu_hau` |
| `engines/analysis_engine/integration/temperature_stage.py` | knowledge-package bind | **No** — applications do not run this pipeline |
| `knowledge/packages/temperature/` | unused package JSON | **No** |
| `knowledge/rule_database/03_temperature_rules/` | legacy JSON | **No** |
| `engines/interpretation_engine/.../temperature_interpreter.py` + Pack-01 JSON | interpretation / unused analyze path | Does not write `AnalysisResult.temperature` |
| `engines/luck_engine/integration/temperature_impact_stage.py` | luck overlap tokens | Luck only |
| `engines/interpretation_engine/foundation/facts/temperature.py` | copies TemperatureEngine facts | Downstream narrative |

---

# 2. Dependency graph

Production analyze order (Orchestrator):

```text
CalendarEngine          (solar term → BaZi month branch)
    ↓
BaziEngine
    ↓
StrengthEngine          (own season from month branch; does not read Temperature)
    ↓
build_temperature_context(bazi, strength overlay unused by CSV)
    ↓
TemperatureEngine.calculate
    ↓
pattern_context.temperature_type ← TemperatureResult.to_pattern_temperature_type()
    ↓
PatternEngine           (identification CSV does not read temperature_type)
    ↓
UsefulGodEngine         (reads temperature_type; tmp_* compete with str_*)
    ↓
Score / Interpretation / Report
```

```text
build_pattern_context initially sets temperature_type from branch map (Sửu → cold)
Orchestrator overwrites it with TemperatureResult mapping (CASE-0001 → hot)
```

No engine replaces `temperature_level` after Temperature Engine. Score stage does not remap it. Report V1 copies `temperature_level` into `useful_god.temperature_adjustment`.

`calendar=` on `build_temperature_context` is **accepted and unused**. Season is not read from Calendar Engine fields.

---

# 3. Rule inventory

Production load: `TemperatureLoader.load_rule_groups()` concatenates:

1. `01_season_rules.csv`
2. `02_climate_rules.csv`
3. `03_dryness_rules.csv`
4. `04_humidity_rules.csv`
5. `05_balance_rules.csv`
6. `07_special_rules.csv` (rows with `score_target=flow` moved to group `flow`)

Also loaded, not as chart matchers:

- `06_priority_rules.csv` — group priority metadata + **level** rules
- `09_conditions.csv` — normalization config (`score_target=config`)
- `08_examples.csv` — `load_examples()` **never called** by `calculate`

| File | On disk | Loaded as match rules | Notes |
|------|--------:|----------------------:|-------|
| `01_season_rules.csv` | 6 | 6 | season / season_phase |
| `02_climate_rules.csv` | 6 | 6 | climate_type / month_branch |
| `03_dryness_rules.csv` | 5 | 5 | dryness_level / fire / earth |
| `04_humidity_rules.csv` | 5 | 5 | humidity_level / water / winter |
| `05_balance_rules.csv` | 5 | 5 | after component scores |
| `07_special_rules.csv` | 8 | 4 special + 4 flow | Day Master specials; flow |
| `06_priority_rules.csv` | 11 | 0 chart-match; 4 **level** | `pri_level_*` |
| `08_examples.csv` | 5 | **0** | orphan vs matcher |
| `09_conditions.csv` | 5 | config only | baseline 35, scale 100, divisor 3, hot 0.65, cold 0.35 |

All listed production CSVs `enabled=true` / `status=active`. Duplicate `rule_id` **inside** `11_temperature`: **none**. Cross-engine ID reuse (`sea_002`, `spc_004` also exist in Strength) is by separate loaders — not a Temperature collision.

### Unreachable / fallback

| Item | Status |
|------|--------|
| `flw_001`…`flw_004` | **Unreachable in production pipeline.** Flow runs in `analyze_primary` **before** `warm_score` / `dry_score` are written. Context defaults are `0.0`. CASE-0001 `flow_matches=[]`. |
| `08_examples.csv` | Unreachable |
| `knowledge/packages/temperature` | Unreachable |
| Empty `TemperatureContext` | `success=False`, `error=no temperature rule matched`, but dataclass default `temperature_level="warm"` still serializes if a caller ignores `success` |
| Disabled rules | **0** |

### Day Master / solar-term / element dependency

| Dependency | Used? |
|------------|-------|
| Day Master element | **Only** `spc_001`–`spc_004`. CASE-0001 Canh/Kim + cold climate matches **none** |
| Solar term name | **Not read** |
| Month branch | Yes (`cli_005/006`, season tables) |
| Element counts | Yes (dryness/humidity/balance) |
| Strength overlay | Fields exist on context; **no CSV condition** reads `strength_level` / `strength_score` |

---

# 4. Calendar / season source

Exact source for Temperature:

```text
BaziChart.month_pillar.branch
    → _BRANCH_SEASON / _BRANCH_SEASON_PHASE / _BRANCH_CLIMATE
```

| Concept | CASE-0001 | Source |
|---------|-----------|--------|
| Gregorian | 1987-01-21 04:30 | Calendar input |
| Solar term | **Đại Hàn** | Calendar Engine (Temperature **does not read it**) |
| Lunar month | 12 / 1986 | Calendar lunar (Temperature **does not read it**) |
| BaZi month branch | **Sửu** | BaziEngine from **solar-term month** |
| Temperature `season` | `winter` | `_BRANCH_SEASON["Sửu"]` |
| `season_phase` | `late_winter` | `_BRANCH_SEASON_PHASE["Sửu"]` |
| `climate_type` | `cold` | `_BRANCH_CLIMATE["Sửu"]` |

Lunar month and BaZi solar-term month are **not** substituted for each other inside Temperature Engine. The month command is the BaZi branch, which Calendar already aligned to solar terms.

`Sửu → Dần` boundary is therefore the **BaZi month-branch change at Lập Xuân**, not 1 January and not lunar New Year. Temperature has **no dedicated solar-term boundary test**.

---

# 5. Temperature formula

## 5.1 Context facts computed in builder (not CSV)

Element counts = visible stems + hidden stems of four branches.

```text
dry_index  = fire + earth - water
  >= 4 → dryness_level = dry
  >= 2 → slightly_dry
  else → normal

humid_index = water + earth - fire
  >= 4 → humid
  >= 2 → slightly_humid
  else → normal
```

CASE-0001: Hỏa 4, Thổ 5, Thủy 1 → `dry` and `slightly_humid`.

## 5.2 Scoring (`TemperatureScorer`)

1. Match season / climate / dryness / humidity / special / flow.
2. Bucket rule `score` into `warm_raw` / `cold_raw` / `dry_raw` / `humid_raw` by `score_target` and `temperature_level`.
3. Component scores = raw / `scale` (100).
4. Match **balance** rules on those component scores.
5. `raw_total = sum(all matched scores) / divisor(3)`
6. `temperature_score = clamp((raw_total + baseline(35)) / 100, 0, 1)`
7. Level = winning `pri_level_*` on `temperature_score` (then special `priority >= 105` may override — none on CASE-0001).
8. `confidence = min(1, n_matches/4 + 0.2 if level_rule)` — **match count**, not score.

**Semantic of `temperature_score`:** normalized 0–1 aggregate of **signed rule points including cold and dry bonuses as positive sum**. Cold winter rules **add** to `raw_total`. They do **not** pull the 0–1 score toward “cold”. That is why CASE-0001 can be `climate_type=cold` and `temperature_level=hot` simultaneously.

Range: **0.0–1.0**. Not confidence. Not Score Engine 0–100.

## 5.3 Classification taxonomy

Internal `temperature_level` (from `06_priority_rules.csv` level rows):

| Internal | Threshold | Vietnamese (Report V1 `TEMPERATURE_LABELS`) | Recommendation on level rule |
|----------|-----------|-----------------------------------------------|------------------------------|
| `hot` | `temperature_score >= 0.65` | Nhiệt | Nhuận hạ giáng nhiệt |
| `warm` | `> 0.50` and `< 0.65` | Ôn | Cân Hỏa Thủy |
| `cool` | `> 0.35` and `<= 0.50` | Lương | Tăng dương khí |
| `cold` | `<= 0.35` | Hàn | Ôn dưỡng tăng dương |

Default if no level rule matches: scorer uses `"warm"`.

Táo / Thấp are **not** this enum. They are `dry_score` / `humid_score` (and builder `dryness_level` / `humidity_level`). Labels `Táo` / `Thấp` exist in Report V1 tables but are **not** applied to `temperature_level`.

`to_pattern_temperature_type()` returns the level if already in `{cold,cool,warm,hot}`; otherwise falls back to the same numeric thresholds.

---

# 6. Four concepts (A–D) — not one field

| Concept | Exists? | Exact field / source |
|---------|---------|----------------------|
| **A. Seasonal climate** | Yes | Context `season`, `season_phase`, `climate_type` from month branch. CASE-0001: winter / late_winter / **cold** |
| **B. Temperature score** | Yes | `TemperatureResult.temperature_score` 0–1. CASE-0001: **0.7166…** Distinct: `ScoreResult.temperature_score` (Score module, ~10 on this chart historically) |
| **C. Balance requirement** | Partial | Rule `recommendation` strings (`Tăng Hỏa`, `Nhuận hạ…`). No enum `need_warm / need_cool / need_moisten / need_dry`. Mixed list on CASE-0001 includes **both** ôn dưỡng and nhuận hạ |
| **D. Điều hậu candidate (can/hành)** | **Not on TemperatureResult** | Useful God `03_temperature_rules.csv` `tmp_001`–`tmp_004` map `temperature_type` → stem (cold→Đinh, hot→**Quý**, cool→Bính, warm→Nhâm). CASE-0001 `tmp_002` matches Quý, **loses** to `str_004` Thực Thần |

Do not treat A–D as the same.

---

# 7. CASE-0001 full trace

Chart: Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần. Nhật chủ **Canh Kim**. Tháng Bát Tự **Sửu**. Tiết khí **Đại Hàn**.

## 7.1 Input facts the Engine actually reads

| Fact | Value | Used by |
|------|-------|---------|
| `day_master` | Canh | snapshot only (no special match) |
| `day_master_element` | Kim | special CSV (no hit) |
| `month_branch` | Sửu | `cli_006` |
| `season` | winter | `sea_002` |
| `season_phase` | late_winter | `sea_006` |
| `climate_type` | cold | `cli_002` |
| `dryness_level` | dry | `dry_001` |
| `humidity_level` | slightly_humid | `hum_002` |
| `fire_count` | 4 | `dry_003` |
| `earth_count` | 5 | `dry_004` |
| `water_count` | 1 | (no `hum_003`/`hum_004`) |
| `strength_level` | strong | **unused by CSV** |

Not used: solar term name, lunar month, `calendar` object, visible-stem list as stems, Ten Gods list.

## 7.2 Rule matches

| Rule ID | Condition | Evidence | Output (score / level / rec) | Priority |
|---------|-----------|----------|------------------------------|---------:|
| `sea_002` | season==winter | winter | +15 / cold / Tăng Hỏa giảm Thủy | 95 |
| `sea_006` | season_phase in mid/late winter | late_winter | +10 / cold / Ôn dưỡng tăng dương | 88 |
| `cli_002` | climate_type==cold | cold | +25 / cold / Dùng Hỏa Mộc ôn dưỡng | 100 |
| `cli_006` | month_branch in Hợi,Tý,Sửu | Sửu | +8 / cold / Tăng Hỏa ấm thân | 90 |
| `dry_001` | dryness_level==dry | dry | +18 / dryness / Tăng Thủy nhuận tao | 100 |
| `dry_003` | fire_count>=3 | 4 | +8 / dryness / Giảm Hỏa | 90 |
| `dry_004` | earth_count>=4 | 5 | +6 / dryness / Thông Thổ hóa Thủy | 88 |
| `hum_002` | humidity_level==slightly_humid | slightly_humid | +12 / humidity / Thông Thổ hóa Thủy | 95 |
| `bal_002` | dry_score>=0.10 and humid_score>=0.10 | 0.32 / 0.12 | +8 / balance / Điều tiết táo thấm | 95 |
| `pri_level_hot` | temperature_score>=0.65 | 0.7167 | level **hot** / Nhuận hạ giáng nhiệt | 100 |

Flow: none. Special: none.

## 7.3 Numeric result

```text
cold_raw = 15+10+25+8 = 58     → cold_score = 0.58
warm_raw = 0                   → warm_score = 0.00
dry_raw  = 18+8+6 = 32         → dry_score  = 0.32
humid_raw = 12                 → humid_score = 0.12

sum(scores) = 102 + 8 = 110
raw_total   = 110 / 3 = 36.666…
temperature_score = (36.666… + 35) / 100 = 0.71666…  (clamp 0–1)
confidence = 1.0
```

Winner level rule: `pri_level_hot` because `0.7167 >= 0.65`.

## 7.4 Classification

| Item | Value |
|------|-------|
| Internal | `hot` |
| Vietnamese (Report V1) | **Nhiệt** |
| Reasoning | `Nhiệt khí nặng` |
| Context climate (not the published level) | `cold` |

## 7.5 Điều hậu

**Temperature Engine hiện chưa tính Dụng thần điều hậu** as a structured can/hành field.

What it does return:

- `recommendations`: `Nhuận hạ giáng nhiệt`, `Dùng Hỏa Mộc ôn dưỡng`, `Tăng Thủy nhuận tao`, `Tăng Hỏa giảm Thủy`, `Thông Thổ hóa Thủy` (max 5; **internally contradictory**)
- Useful God temperature candidate: `tmp_002` → **Quý** (“Nhiệt khí nặng cần nhuận hạ”), priority 86
- Useful God **winner**: `str_004` → **Thực Thần** (“Than vượng cần tiết khí”)

Do not fill UI from season (`Hàn`) while publishing level `hot`.

---

# 8. Exact Temperature output (API `data.temperature`)

```text
success                 True
temperature_level       hot
temperature_score       0.7166666666666666
warm_score              0.0
cold_score              0.58
dry_score               0.32
humid_score             0.12
confidence              1.0
matched_rules           sea_002, sea_006, cli_002, cli_006, dry_001, dry_003, dry_004, hum_002, bal_002
reasoning               Nhiệt khí nặng
recommendations         [Nhuận hạ giáng nhiệt, Dùng Hỏa Mộc ôn dưỡng, Tăng Thủy nhuận tao, Tăng Hỏa giảm Thủy, Thông Thổ hóa Thủy]
```

No `dieu_hau`, `label`, `status`, or `level` key.

---

# 9. Exact meaning of each score

| Field | Meaning | CASE-0001 |
|-------|---------|-----------|
| `temperature_score` | `(sum(matched rule points)/3 + 35)/100` clipped to 0–1. **Not** “how hot the month is”. **Not** confidence | 0.72 |
| `warm_score` | Sum of warm/hot **season/climate** rule points / 100 | 0.00 |
| `cold_score` | Sum of cold/cool rule points / 100 | 0.58 |
| `dry_score` | Dryness rule points / 100 | 0.32 |
| `humid_score` | Humidity rule points / 100 | 0.12 |
| `confidence` | `min(1, n_matches/4 + 0.2)` | 1.0 |
| `score.temperature_score` | **Score Engine** module (khí hậu điều hòa 0–100) | separate; not TemperatureView |

---

# 10. Why UI shows `Điều hậu: —`

Path:

```text
TemperatureResult.to_portal_dict()
    → TemperatureView.to_dict()          # keys: temperature_level, temperature_score, …
    → data.temperature
    → fullReportViewModel.temperatureText()
         reads dieu_hau || label || status || level
         all missing → ""
    → kv("Điều hậu", "") → "—"
```

This is **(3) adapter does not bind** the canonical field, plus **(5) field name mismatch**.

Not (1): Engine has data.  
Not (2): `AnalysisResult.temperature` is populated.  
Not (4) alone: the row **is** rendered; the value is empty.  
Not (6) for this CASE: no Temperature fallback.  
(7) also true as a product gap: UI label **Điều hậu** expects a Dụng thần-like string; Engine never publishes `dieu_hau` on temperature.

Meanwhile:

| Surface | What it actually shows for CASE-0001 |
|---------|--------------------------------------|
| Full Report HTML `Điều hậu` | **—** (wrong keys) |
| Report V1 / PDF / DOCX `Điều hậu nhiệt` | **Nhiệt** (`temperature_level` → `TEMPERATURE_LABELS["hot"]`) if the row is kept (`_filled_rows` drops empty only; `hot` is kept) |
| Golden Report V1 | `useful_god.temperature_adjustment: "hot"` (matches live engine, not `—`) |
| Legacy pattern “Điều hậu” | **Đắc lệnh** (`pattern.dieu_hau`) |
| Canonical Desktop | **no Điều hậu row** |
| Portal Technical Info | **no temperature metadata key** |

Fixture `launch_04_real_chart_response.json` (1987-01-21) already has `temperature_level: "hot"` and `pattern.dieu_hau: "Đắc lệnh"` — same split.

---

# 11. Strength interaction (G1-02 frozen — not modified)

CASE-0001 Strength evidence includes `Ấn mùa lạnh +10`.

| Item | Value |
|------|-------|
| Rule | Strength `database/12_strength/07_special_rules.csv` **`spc_004`** |
| Engine | **Strength Engine**, not Temperature |
| Condition | `month_branch_ten_god == Chính Ấn` AND `season in [winter, autumn]` |
| Season source | Strength `_BRANCH_SEASON` from **month branch** (same table idea, independent copy) |
| Reads `TemperatureResult`? | **No** |
| Temperature change → Strength change? | **No** at runtime. Only if month branch / season mapping in Strength builder changes |
| Double-count? | **Not the same adjustment.** Strength +10 to Strength raw. Temperature `sea_002`/`sea_006` add to Temperature raw. Different outputs. Shared *idea* of “winter” only |

No G1-02 BLOCKER: Temperature does not rewrite Strength after it is calculated.

Note: Temperature also has `spc_004` (Mộc + cold climate). Different file, different meaning. CASE-0001 does not match Temperature `spc_004`.

---

# 12. Pattern interaction (G1-03 frozen — not modified)

- Pattern identification CSV has **no** `temperature_type` condition.
- CASE-0001 primary remains **Chính Ấn** / `pat_ca_01`.
- Orchestrator writes `temperature_type=hot` onto `PatternContext` **after** Strength, **before** Pattern calculate. Pattern still does not use it for main pattern.
- `build_pattern_context` initially sets `temperature_type=cold` from Sửu branch map; Orchestrator **overwrites** with TemperatureResult (`hot`). Useful God sees **hot**.
- `pattern.dieu_hau` is filled later from `month.status` / `wuxing.season_status` → **Đắc lệnh**. Comment in code: not temperature.

---

# 13. Useful God interaction

Useful God **does** read Temperature:

```text
temperature_type == PatternContext.temperature_type
                 == TemperatureResult.to_pattern_temperature_type()
```

| Layer | CASE-0001 |
|-------|-----------|
| `tmp_002` | matches `hot` → useful_god **Quý**, rec “Nhiệt khí nặng cần nhuận hạ”, priority 86 |
| Winner | `str_004` **Thực Thần** — Dụng thần cân bằng thân (“Than vượng cần tiết khí”) |
| `UsefulGodView` | drops `temperature_reason` (API `useful_god.temperature_reason` is absent) |

Two product concepts exist and presentation currently shows only the Strength winner as **Dụng thần**:

1. **Dụng thần cân bằng thân** — `useful_god` / `dung_than` = Thực Thần  
2. **Dụng thần điều hậu** — UG temperature candidate Quý, **not** shown as Điều hậu; Full Report Điều hậu is `—`

Do not merge them in Phase 2 without Product Owner Option B.

---

# 14. Evidence availability

| Needed trace | Present on TemperatureResult / View? | Lost where? |
|--------------|--------------------------------------|-------------|
| Season / month source | `metadata.trace.context` (`month_branch`, `season`, `climate_type`) | **Not** on `TemperatureView` / portal dict |
| Climate state | context `climate_type`; published **level** is different | Portal does not show either |
| Matching rules | `matched_rules` | Present on API; unused by Full Report |
| Score contribution per rule | only in unmatched raw rules; `raw_total` in `metadata.trace.scoring` | Trace-only; no `evidence_compact` |
| Final state | `temperature_level`, `temperature_score`, components | API yes; Full Report no |
| Balancing need | `recommendations` (strings) | API yes; Full Report no |
| Flow / điều hậu rules | designed in `flw_*` | **Never match** (pipeline order) |

No `evidence_compact` equivalent to G1-02/G1-03.

---

# 15. Portal / Report / PDF / DOCX binding

| Surface | Field bound | CASE-0001 display |
|---------|-------------|-------------------|
| API `data.temperature` | TemperatureView | `hot` / 0.72 / recs |
| Full Report HTML | `dieu_hau` on temperature | **Điều hậu: —** |
| Canonical Desktop | none | (no row) |
| Result V2 Technical Info | none | (no row) |
| Report V1 HTML/PDF/DOCX | `useful.temperature_adjustment` ← `temperature_level` | **Điều hậu nhiệt: Nhiệt** |
| Report V1 golden | `temperature_adjustment: "hot"` | internal code, matches engine |
| Legacy pattern card | `pattern.dieu_hau` | **Đắc lệnh** |
| Score surfaces | `score.temperature_score` | Score module, not Điều hậu |

No renderer **computes** Temperature. Several **mis-bind** or **omit**.

---

# 16. Boundary test coverage

Existing `tests/temperature/`: engine hot/cold **synthetic** contexts, loader, matcher, scorer, context_builder on two dates, 100-chart regression (asserts `success` and ≥2 levels, not CASE-0001).

| Boundary | Coverage |
|----------|----------|
| 12 month branches | **No** dedicated matrix |
| `Sửu → Dần` / Lập Xuân | **No** |
| Solar-term edges | **No** (engine does not read solar term) |
| Score min 0 / max 1 | implicit clamp; no explicit tests |
| Level thresholds 0.35 / 0.50 / 0.65 ± ε | **No** |
| Flow rules | untested as production-unreachable |
| CASE-0001 | **No** temperature test (fixture JSON only) |

---

# 17. Representative test coverage

`08_examples.csv` (not executed by engine):

| ID | DM | Month | Expected level |
|----|----|-------|----------------|
| ex_001 | Bính | Ngọ | hot |
| ex_002 | Nhâm | Tý | cold |
| ex_003 | Giáp | Dần | warm |
| ex_004 | Canh | Dậu | cool |
| ex_005 | Đinh | Mùi | hot |

Gaps: no Sửu/winter+Kim (CASE-0001); no Xuân/Hạ/Thu/Đông × each taxonomy cell; Day Master specials `spc_001`–`004` not in unit tests.

100-chart regression does not lock taxonomy vs season.

---

# 18. Legacy / duplicate implementations

See §1.2. Highest confusion risk: **`pattern.dieu_hau` named Điều hậu** vs Temperature vs Useful God `tmp_*` vs Score `temperature_score`.

---

# 19. Gap classification

| Gap | Layer |
|-----|-------|
| Full Report `—` despite live `hot` | **adapter / presentation** |
| Three UI sources (empty / Nhiệt / Đắc lệnh) | **adapter / presentation / contract** |
| `temperature_score` formula yields `hot` on winter Sửu | **calculation** (Product Owner must accept or redesign; Phase 1 does not change it) |
| Flow `flw_*` never match | **calculation** (stage order) |
| No structured Điều hậu can/hành on TemperatureResult | **contract / rule** (Option A vs B) |
| Contradictory `recommendations` | **rule / calculator aggregation** |
| `calendar` unused; solar term unused | **calendar** (by design today) |
| No `evidence_compact` | **contract** |
| Strength/Temperature duplicate season tables | **acceptable duplication**; not a rewrite |
| Tests miss CASE-0001 and 12 branches | **test** |
| `08_examples` / knowledge packages unused | **rule / unused** |

---

# 20. Presentation proposal (not implemented)

Do **not** invent Dụng thần from season.

### If Product Owner chooses **Option A** (V1.0 = climate / Temperature as computed today)

Bind **only** canonical TemperatureView:

**Khí hậu (phân loại điểm)**  
`Nhiệt` ← `temperature_level` + Report V1 labels (`hot`→Nhiệt)

**Điểm nhiệt**  
`0.72`

**Thành phần**  
`Hàn 0.58 · Táo 0.32 · Thấp 0.12` (optional compact)

**Căn cứ** (from existing facts, no new engine)  
`Nguyệt lệnh Sửu · mùa Đông · climate_type lạnh · rule pri_level_hot`

Do **not** label this **Điều hậu** unless PO accepts that the word currently means “temperature class”, not 用神调候.

Do **not** show `pattern.dieu_hau` (`Đắc lệnh`) as Điều hậu.

### If Product Owner chooses **Option B**

That is a **new canonical Điều hậu layer** (stem/element/need). Useful God `tmp_*` is a candidate source but is **not** frozen as winner. Phase 1 must not implement Option B.

---

# 21. Minimal changes required for G1-04 PASS (Phase 2 — do not do now)

1. **Bind** Portal Full Report / Desktop / Technical Info to `data.temperature.temperature_level` (and optional score / evidence). Stop reading `dieu_hau` on the temperature object.  
2. **Stop** labeling `pattern.dieu_hau` as Điều hậu (legacy presenters). That field is month 得令.  
3. **Product Owner A vs B** before any new điều hậu stem algorithm.  
4. If A: rename UI to **Khí hậu** / **Điểm nhiệt**, not Điều hậu Dụng thần.  
5. Optional evidence compact from `metadata.trace` (like G1-02) — additive, no formula change unless PO rejects `hot` on Sửu.  
6. Tests: CASE-0001 lock; adapter regression `—` vs `hot`; do not change Strength/Pattern/Ten Gods/Useful God **winners** unless PO chooses B.  
7. Document (do not silently “fix”) the winter→`hot` score identity if PO keeps the formula.  
8. Flow-stage order is a calculation bug if PO wants `flw_*`; still Phase 2 + PO.

Do not change Strength, Pattern, Ten Gods, or Useful God selection in G1-04 Phase 2 unless Option B is explicit.

---

# PRODUCT OWNER DECISION REQUIRED

Temperature Engine **computes khí hậu scores + `cold/cool/warm/hot` + recommendation strings**.

It **does not** compute a canonical **Dụng thần điều hậu** (can/hành) on `TemperatureResult`.

Useful God has a temperature stem candidate (`Quý` on CASE-0001) that **loses** to Strength Dụng thần (`Thực Thần`).

| Option | Meaning |
|--------|---------|
| **A** | V1.0 displays existing climate / `temperature_level` / score. Do not invent Điều hậu 用神. |
| **B** | Add a minimal canonical Điều hậu layer before freeze. |

This audit **does not choose Option B**.

---

# PHASE 1 STATUS

`G1-04 PHASE 1: AUDIT PASS / G1-04 NOT READY — REPAIR REQUIRED`

Stop. Do not start Phase 2. Do not edit Temperature, Strength, Pattern, Ten Gods, Useful God, Portal, or Report until Product Owner review.
