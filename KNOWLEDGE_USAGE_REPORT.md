# KNOWLEDGE USAGE REPORT

**BTE Platform V1.0 — Sprint Audit 2**  
**Date:** 2026-07-28  
**Scope:** `engines/interpretation_engine/knowledge/05_rule_database`  
**Mode:** Audit only — no code / UI / Report changes  

**Sample:** 10 birth cases through production pipeline  
(Calendar → Bazi → Pattern → RuleContext → Score → Interpretation)

---

## 1. Executive Summary

| Metric | Value |
|--------|------:|
| JSON files on disk | 48 |
| Disk records (all kinds) | 2,526 |
| KnowledgeRuleLoader matchable rules | 495 |
| Loader coverage vs disk records | 19.6% |
| Unique rule_ids matched (10 cases) | 107 / 495 (21.6%) |
| Unique rule_ids resolved | 53 / 495 (10.7%) |
| Unique rule_ids interpreted | ~65 / 495 (13.1%) |
| Never matched (loaded) | 388 (78.4% of loaded) |
| Dead JSON (no loader consume as rules) | 19 files |
| Soft-dead (labels/examples skip by design) | 10 files |
| PriorityRuleLoader (08) | **FAIL** — multi-JSON parse error |
| Production Priority path | `for_matched_rules()` — **does not load 08 KB** |

---

## 2. TASK 1 — Knowledge Base Inventory

### 2.1 Per module

| Module | Files | Rules | Conditions | Actions | Labels | Examples | Priority |
|--------|------:|------:|-----------:|--------:|-------:|---------:|---------:|
| 01_strength_rules | 8 | 162 | 0 | 0 | 0 | 0 | 0 |
| 02_season_rules | 6 | 147 | 0 | 0 | 0 | 0 | 0 |
| 03_temperature_rules | 7 | 263 | 0 | 0 | 42 | 30 | 40 |
| 04_pattern_rules | 5 | 50 | 0 | 0 | 47 | 40 | 35 |
| 05_special_case_rules | 6 | 130 | 100 | 0 | 50 | 50 | 40 |
| 06_follow_pattern_rules | 6 | 100 | 100 | 100 | 100 | 100 | 100 |
| 07_combination_rules | 5 | 100 | 100 | 0 | 100 | 100 | 100 |
| 08_priority_rules | 5 | 40 | 40 | 0 | 40 | 40 | 40 |
| **TOTAL** | **48** | **992** | **340** | **100** | **379** | **360** | **355** |

**Grand total records = 2,526**

### 2.2 Notes on classification

- Files named `*_priority.json` / `priority_order.json` counted as **priority**.
- Files named `*_score_rules.json`, `*_adjustment_rules.json`, `cold_hot_rules.json`, etc. counted as **rules**.
- Multi-document JSON (concatenated arrays) is counted via multi-decode (same as KnowledgeRuleLoader).

---

## 3. TASK 2 — Knowledge Loader Audit

### 3.1 Loader vs disk (matchable rules)

| Module | Disk rule-like records* | Loaded by KnowledgeRuleLoader | Status |
|--------|------------------------:|------------------------------:|--------|
| 01_strength_rules | 162 | 12 | 🔴 Gap |
| 02_season_rules | 147 | 15 | 🔴 Gap |
| 03_temperature_rules | 263 (+72 L/E/P) | 76 | 🟡 Partial |
| 04_pattern_rules | 50 (+122 L/E/P) | 55 | 🟢 OK (rules+priority subset) |
| 05_special_case_rules | 230 (+140 L/E/P) | 100 | 🟡 Only conditions |
| 06_follow_pattern_rules | 300 (+300 aux) | 97 | 🟡 Only rules |
| 07_combination_rules | 200 (+300 aux) | 100 | 🟡 Only rules |
| 08_priority_rules | 80 (+120 aux) | 40 | 🟡 Only conditions |

\* “rule-like” = records in files classified as rules/conditions/actions/priority that *could* be matchable if they had conditions.

**Loaded total: 495**  
**By section map:** strength=17, summary=31, warning=290, pattern=157

### 3.2 Files that contribute to loader (disk → loaded)

| File | Disk | Loaded |
|------|-----:|-------:|
| final_strength_rules.json | 27 | 6 |
| root_strength_rules.json | 34 | 6 |
| season_definition_rules.json | 18 | 5 |
| seasonal_element_rules.json | 21 | 5 |
| seasonal_strength_rules.json | 41 | 5 |
| adjustment_rules.json | 38 | 38 |
| climate_score_rules.json | 42 | 33 |
| temperature_priority.json | 40 | 5 |
| pattern_priority.json | 35 | 5 |
| pattern_rules.json | 21 | 21 |
| pattern_score_rules.json | 29 | 29 |
| special_case_conditions.json | 100 | 100 |
| follow_pattern_rules.json | 100 | 97 |
| combination_rules.json | 100 | 100 |
| priority_conditions.json | 40 | 40 |

### 3.3 Files NOT loaded as matchable rules

**Reason A — intentional skip (`*_labels.json`, `*_examples.json`):** 10 files

**Reason B — no `conditions` / `required_conditions` / `condition`:** 19 files

| File | Reason |
|------|--------|
| 01_strength_rules/combination_adjustment_rules.json | no_cond=31 |
| 01_strength_rules/control_strength_rules.json | no_cond=16 |
| 01_strength_rules/drain_strength_rules.json | no_cond=16 |
| 01_strength_rules/month_strength_rules.json | no_cond=12 |
| 01_strength_rules/strength_score_rules.json | no_cond=1 |
| 01_strength_rules/support_strength_rules.json | no_cond=25 |
| 02_season_rules/final_season_rules.json | no_cond=16 |
| 02_season_rules/seasonal_adjustment_rules.json | no_cond=23 |
| 02_season_rules/seasonal_exception_rules.json | no_cond=28 |
| 03_temperature_rules/cold_hot_rules.json | no_cond=100 |
| 03_temperature_rules/humidity_rules.json | no_cond=83 |
| 05_special_case_rules/special_case_priority.json | no_cond=40 |
| 05_special_case_rules/special_case_rules.json | no_cond=60 |
| 05_special_case_rules/special_case_score_rules.json | no_cond=70 |
| 06_follow_pattern_rules/follow_pattern_actions.json | no_cond=100 |
| 06_follow_pattern_rules/follow_pattern_conditions.json | no_cond=100 |
| 06_follow_pattern_rules/follow_pattern_priority.json | no_cond=100 |
| 07_combination_rules/combination_conditions.json | no_cond=100 |
| 07_combination_rules/combination_priority.json | no_cond=100 |

**Also unloaded:**

| File | Notes |
|------|-------|
| 08_priority_rules/priority_rules.json | KnowledgeRuleLoader: no matchable conditions; PriorityRuleLoader: **JSON Extra data** (multi-doc) |
| 08_priority_rules/priority_order.json | Only PriorityRuleLoader — currently fails before use |
| 08_priority_rules/priority_labels.json | Soft-dead for Interpretation; Priority loader broken |
| 08_priority_rules/priority_examples.json | Soft-dead; Priority loader broken |

### 3.4 Priority loader status

```
PriorityRuleLoader.from_project_root → FAIL
Invalid JSON in priority_rules.json: Extra data: line 123 column 3
```

Production Interpretation uses:

```python
PriorityService.for_matched_rules()  # NO KB load — section cap resolver only
```

→ **Entire `08_priority_rules` PR* pipeline is unused in production Interpretation.**

---

## 4. TASK 3 — Rule Matcher Coverage

Across **10 cases** (union of rule_ids):

```
loaded rules          495
        ↓ match
matched (union)       107   (21.62%)
        ↓ priority resolve
resolved (union)       53   (10.71%)
        ↓ builder / sentences
interpreted (union)  ~65    (13.13%)
        ↓ report portal
rendered               = interpretation sections (prose only)
```

| Funnel step | Count | % of loaded |
|-------------|------:|------------:|
| Loaded | 495 | 100% |
| Matched ≥1 case | 107 | 21.62% |
| Resolved ≥1 case | 53 | 10.71% |
| Interpreted ≥1 case | ~65 | 13.13% |
| Never matched | 388 | 78.38% |

Per-case typical funnel: matched ≈ 83–91 → resolved ≈ 33–35 → interpreted sentences ≈ 44–47.

**Match → Resolve retention:** 49.5% (Priority discards ~half of matches).

---

## 5. TASK 4 — Unused Knowledge

### 5.1 Rules never matched (loaded but idle)

- **388 / 495** loaded rules never matched in the 10-case sample.
- Dominant idle pools: warning/combination/follow/special_case conditions that require facts still False (`combination_*`, many `tong_*` subtypes, humidity extremes, etc.).

### 5.2 Conditions never used as matchable rules

Standalone condition catalogs are **not joined** by KnowledgeRuleLoader:

- `follow_pattern_conditions.json` (100)
- `combination_conditions.json` (100)
- `special_case_conditions.json` **is** loaded (100) — exception
- `priority_conditions.json` **is** loaded (40)

### 5.3 Actions never called

- `follow_pattern_actions.json` (100) — **no engine imports / executes actions**
- No Action runner in Interpretation pipeline

### 5.4 Labels not read by Interpretation

All `*_labels.json` under 03–07 skipped by KnowledgeRuleLoader.  
Only Priority labels would be read by PriorityRuleLoader (currently broken).  
Narrative/Report have their **own** label files under different knowledge roots.

### 5.5 Examples not used at runtime

All `*_examples.json` under 03–08 — documentation / golden only; not loaded into matcher.

### 5.6 Priority not referenced in production resolve

- `*_priority.json` files: only a few records with conditions enter matcher (`temperature_priority`, `pattern_priority` subsets).
- `special_case_priority`, `follow_pattern_priority`, `combination_priority`, `priority_order` — **not applied** by production `MatchedRuleResolver`.

---

## 6. TASK 5 — Dead JSON Audit

### 6.1 Hard-dead for Interpretation matcher (19)

See §3.3 Reason B. These exist on disk, are not skipped by suffix, but yield **0** matchable rules.

### 6.2 Soft-dead by design (10)

All `*_labels.json` / `*_examples.json` in modules 03–07 (and 08 examples/labels for Interpretation path).

### 6.3 Dead relative to Priority Engine

Because `PriorityRuleLoader` fails and production uses `for_matched_rules()`:

| File | Interpretation | Priority Engine |
|------|----------------|-----------------|
| priority_rules.json | not loaded | cannot parse |
| priority_conditions.json | loaded as KB rules | cannot parse full set |
| priority_order.json | not loaded | cannot parse |
| priority_labels.json | skipped | cannot parse |
| priority_examples.json | skipped | cannot parse |

### 6.4 Code reference scan

| Token | Referenced in engines? |
|-------|------------------------|
| `05_rule_database` | Yes (interpretation + priority) |
| `KnowledgeRuleLoader` | Yes |
| `PriorityRuleLoader` | Yes (but broken on multi-JSON) |
| `*_actions.json` | **No** |
| Module `*_conditions.json` (follow/combination) | **No** (only priority_conditions) |
| Module `*_priority.json` (non-08) | Only if records have conditions (partial) |

---

## 7. TASK 6 — RuleContext Coverage (10 cases)

| Namespace | Field paths | Non-empty paths | Always empty (sample) | Producer | Consumer |
|-----------|------------:|----------------:|-----------------------|----------|----------|
| calendar.* | 10 | 10 | — | CalendarEngine | Matcher / facts |
| bazi.* | 24 | 24 | — | BaziEngine + RuleContextBuilder | Matcher / Pattern |
| pattern.* | 29 | 12 | category, clash_count, combination_status, visibility_*, … | PatternEngine | Matcher / Portal pattern |
| strength.* | 7 | 7 | — | Builder + Score append | Matcher / facts |
| temperature.* | 19 | 7 | humidity*, damp/dry, cold_min/max, … | RuleContextBuilder (month branch) | Temperature rules |
| useful_god.* | 11 | 10 | role | Builder (PATTERN_USEFUL_GOD + hy/ky) | Pattern enrich / Matcher |
| score.* | 14 | 13 | modules | ScoreEngine | Matcher |
| luck.* | 7 | 2 | pillars, phase, support, attack | Stub (available=False) | Luck rules mostly idle |
| shensha.* | 41 | 41 | — | Bazi ShenShaService → Builder | Matcher / Portal |
| wuxing.* | 31 | 25 | balance_*, special_case, … | Builder | Matcher |
| ten_gods.* | 139 | 137 | destroyed_ten_gods, structure | Builder | Matcher |
| facts.* | 157 | 157* | many False but present | Builder + Score sync | Matcher / Priority facts |
| month.* | 4 | 4 | — | Builder | Pattern enrich |
| root/support/control | 9 | 9 | — | Builder | Strength rules |
| hidden_stems.* | 10 | 10 | — | Builder | Matcher |

\* Facts keys exist; many boolean facts remain **False** (combination geometry, luck analysis, etc.) → rules requiring them never match.

### Missing / weak producers

| Gap | Impact |
|-----|--------|
| luck.available=False | Đại vận / luck section rules idle |
| combination geometry facts False | 07_combination mostly unmatched |
| pattern.follow_type only sometimes | Follow subtype rules partial |
| temperature humidity / damp / dry None | humidity_rules.json unused |
| special.case_name None | Special-case name rules limited |

---

## 8. TASK 7 — Interpretation Section Coverage

### 8.1 Rules available by loader section map

| Section key | Loaded rules | Notes |
|-------------|-------------:|-------|
| warning | 290 | temperature + special + combination |
| pattern | 157 | pattern + follow |
| summary | 31 | season + priority_conditions |
| strength | 17 | strength subset |

**Folder→section map does NOT map to career/wealth/relationship/health/useful_god/luck/conclusion.**  
Those sections appear in portal output via builder aliases / sentence section tags, not from folder map counts above.

### 8.2 Sections actually rendered (hits / 10 cases)

| Section | Cases with section | Est. available rules (folder map) | Actual hit rate |
|---------|-------------------:|----------------------------------:|-----------------|
| summary | 10/10 | 31 | 🟢 |
| personality | 10/10 | (alias) | 🟢 |
| career | 10/10 | (alias) | 🟢 |
| relationship | 10/10 | (alias) | 🟢 |
| health | 10/10 | (alias) | 🟢 |
| useful_god | 10/10 | (alias) | 🟢 |
| conclusion | 10/10 | (alias) | 🟢 |
| warning | 10/10 | 290 | 🟢 (few of many) |
| strength | 10/10 | 17 | 🟢 (post strength.level fix) |
| weakness | 9/10 | (polarity) | 🟢 |
| wealth | 5/10 | (alias) | 🟡 |
| pattern | 4/10 | 157 | 🟡 |
| luck | 0/10 | — | 🔴 |
| children / yearly_fortune | 0/10 | — | 🔴 |

---

## 9. TASK 9 — Cross Reference Audit

| Check | Result |
|-------|--------|
| Unique IDs across KB | 2,375 |
| Duplicate IDs (same id in >1 place) | 103 |
| Orphan refs matching ID-like tokens (FPC/FPR/…) | 0 in scanned rule refs |

**Duplicate note:** Many duplicates are intentional mirrors (condition id referenced in multiple docs) or repeated codes across concatenated JSON documents. Not necessarily bugs — needs curated review before deletion.

**Action IDs / label IDs:** Not cross-linked at runtime (no action engine).

---

## 10. Health Scores (summary)

| Score | Value | Definition used |
|-------|------:|-----------------|
| Knowledge Health | **20%** | 495 loaded / 2,526 disk records |
| Pipeline Health | **82%** | Producers fixed; luck/combination/humidity still weak |
| Rule Coverage | **22%** | matched_union / loaded |
| Dead Knowledge | **80%** | 1 − loaded/disk (includes soft-dead labels/examples) |
| Ready for Report Binding | **75%** | Core fields produced; luck/combination incomplete |

See also: `PIPELINE_COVERAGE_REPORT.md`, `engines/interpretation_engine/knowledge/docs/SYSTEM_DATA_FLOW.md`.

---

## 11. Recommendations (audit only — do not implement here)

1. Fix `priority_rules.json` multi-JSON **or** teach PriorityRuleLoader `load_multi_json`.
2. Decide: wire `PriorityService.from_project_root` into Interpretation **or** accept MatchedRuleResolver-only.
3. Add `conditions` to strength/season score JSON **or** a calculator-side loader (not Interpretation matcher).
4. Either join `*_conditions.json` + `*_actions.json` via adapter, or mark them as documentation-only.
5. Produce luck signals before expecting luck sections.
6. Produce combination geometry facts before expecting 07 rules to fire.
7. Only after producers for luck/combination: Report / Portal binding.

---

*End of KNOWLEDGE_USAGE_REPORT.md*
