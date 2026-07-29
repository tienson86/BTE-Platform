# SYSTEM DATA FLOW

**BTE Platform V1.0**  
**Location:** `engines/interpretation_engine/knowledge/docs/SYSTEM_DATA_FLOW.md`  
**Sprint Audit 2 — after Data Producer fixes**  
**Mode:** Documentation / audit only

---

## 1. End-to-End Data Flow

```text
Input (year, month, day, hour, minute, gender)
        ↓
Calendar Engine          → CalendarResult
        ↓
Bazi Engine              → BaziChart (pillars, hidden_stems, ten_gods, shensha)
        ↓
Pattern Engine           → PatternResult + RuleContext (sole RC producer)
        ↓
Score Engine             → ScoreResult → append into RuleContext.score / strength.level
        ↓
KnowledgeRuleLoader      → 495 matchable rules (05_rule_database)
        ↓
Rule Matcher             → matched rules
        ↓
Priority (MatchedRuleResolver) → resolved rules  [08 KB NOT loaded here]
        ↓
Interpretation Builder + Sentence Generator → InterpretationResult / portal sections
        ↓
Report Engine            → HTML/MD from interpretation sections only
        ↓
Portal Presenters        → calendar / bazi / pattern / score / interpretation views
        ↓
API Orchestrator         → AnalysisResult JSON
```

**SSOT orchestrator:** `applications/api/services/orchestrator.py`

---

## 2. Producer of Each Critical Field

| Field | Producer | Stage | Consumer(s) |
|-------|----------|-------|-------------|
| solar / lunar / julian_day / solar_term | CalendarEngine | Calendar | API, RuleContext.calendar, Portal chart_info |
| year/month/day/hour_pillar | BaziEngine | Bazi | PatternContext, RuleContext.bazi, Portal |
| hidden_stems | BaziEngine | Bazi | RuleContext, Portal |
| ten_gods | BaziEngine (+ BaziView enrich) | Bazi | Pattern, RuleContext, Portal |
| **shensha** | **ShenShaService ← BaziEngine.build** | Bazi | RuleContext.shensha, BaziView, Portal |
| nap_am / truong_sinh | bazi_truth.build_bazi_view | API truth | Portal |
| pattern / cach_cuc | PatternCalculator + labels | Pattern | PatternView, Portal |
| **follow_type** | **FollowPatternCalculator.detect** | Pattern | RuleContext.pattern.follow_type |
| **tong_cach** | enrich_result_from_rule_context | Pattern | PatternView, Portal |
| **dung_than** | RuleContextBuilder._build_useful_god → enrich | Pattern | PatternView, Portal, Matcher |
| **hy_than / ky_than** | useful_god.favorable/unfavorable → enrich | Pattern | PatternView, Portal |
| than / than_vuong_nhuoc | enrich (DM element + strength/month) | Pattern | PatternView, Portal |
| dieu_hau | enrich (month.status / season) | Pattern | PatternView, Portal |
| RuleContext (full) | RuleContextBuilder.build | Pattern | Score, Interpretation |
| **strength.level** | ScoreEngine.append_score_to_rule_context | Score | Matcher facts, Interpretation |
| score.* / grade | ScoreEngine.calculate | Score | API ScoreView, Matcher |
| **temperature.status** | RuleContextBuilder._build_temperature (month branch) | RuleContext | Temperature rules, facts |
| matched rules | RuleMatcher | Interpretation | Priority resolver |
| resolved rules | MatchedRuleResolver | Interpretation | Builder |
| interpretation sections | legacy_builder + portal_view | Interpretation | Report, Portal |
| report html/md | ReportEngine.render_from_analysis | Report | API / Portal narrative |
| Portal `--` placeholders | presenters (JS) | Portal | UI only |

---

## 3. Consumer Map (who reads what)

| Consumer | Reads |
|----------|-------|
| PatternEngine | CalendarResult, BaziChart |
| RuleContextBuilder | calendar, bazi, pattern (+ optional score/luck/temperature) |
| ScoreEngine | RuleContext |
| KnowledgeRuleLoader | JSON under `05_rule_database` (skips labels/examples) |
| RuleMatcher | RuleContext + loaded rules |
| MatchedRuleResolver | matched rule list (priority/confidence/section caps) |
| InterpretationBuilder | ordered rules + RuleContext |
| ReportEngine (production) | AnalysisResult.interpretation only |
| Portal calendar.js | payload.calendar |
| Portal bazi.js | payload.bazi |
| Portal pattern.js | payload.pattern |
| Portal score.js | payload.score |
| Portal interpretation.js | payload.interpretation |
| PriorityRuleLoader | `08_priority_rules` — **not on production Interpretation path** |

---

## 4. Rule Database Inventory

Root: `engines/interpretation_engine/knowledge/05_rule_database/`

| Module | Purpose | Disk records (approx) |
|--------|---------|----------------------:|
| 01_strength_rules | Thân vượng/nhược | 162 |
| 02_season_rules | Mùa / lệnh | 147 |
| 03_temperature_rules | Hàn nhiệt / khí hậu | 375 |
| 04_pattern_rules | Cách cục | 172 |
| 05_special_case_rules | Đặc cách | 370 |
| 06_follow_pattern_rules | Tòng cách | 600 |
| 07_combination_rules | Hợp hội xung | 500 |
| 08_priority_rules | Ưu tiên PR* | 200 |
| **Total** | | **2,526** |

See `KNOWLEDGE_USAGE_REPORT.md` for file-level counts.

---

## 5. Knowledge Loader

### 5.1 Interpretation path

```text
InterpretationEngine.__init__
  → RuleLoader(rule_path=None)
  → KnowledgeRuleLoader().load()
       walk **/*.json
       SKIP: *_labels.json, *_examples.json, *_index.json, metadata.json
       KEEP only items with conditions | condition | required_conditions
```

**Loaded today: 495 rules.**

### 5.2 Priority path (unused in production Interpretation)

```text
PriorityService.from_project_root
  → PriorityRuleLoader.load()
       REQUIRED: priority_rules, conditions, order, labels
       OPTIONAL: examples
```

**Status:** FAIL on `priority_rules.json` (concatenated JSON / Extra data).  
Production uses `PriorityService.for_matched_rules()` instead (no 08 KB).

### 5.3 Folder → section map

| Folder | Section |
|--------|---------|
| 01_strength_rules | strength |
| 02_season_rules | summary |
| 03_temperature_rules | warning |
| 04_pattern_rules | pattern |
| 05_special_case_rules | warning |
| 06_follow_pattern_rules | pattern |
| 07_combination_rules | warning |
| 08_priority_rules | summary |

---

## 6. Pipeline Coverage (snapshot)

| Stage | Coverage | Comment |
|-------|----------|---------|
| Calendar | 🟢 ~95% | timezone param unused |
| Bazi | 🟢 ~90% | shensha producer fixed |
| Pattern | 🟢 ~85% | follow/hy/ky fixed; geometry attrs empty |
| RuleContext | 🟡 ~80% | luck/combination/humidity weak |
| Score | 🟢 ~90% | strength.level sync fixed |
| Knowledge load | 🟡 ~20% of disk records | many no-condition files |
| Matcher | 🟡 ~22% of loaded | 10-case union |
| Priority KB | 🔴 0% production | resolver-only |
| Interpretation | 🟡 ~75% sections | luck missing |
| Report | 🟡 prose-only | structural bind deferred |
| Portal | 🟡 | waits on Report bind + remaining producers |
| API | 🟢 | Orchestrator stable |

---

## 7. Unused Knowledge (summary)

- **388 / 495** loaded rules never matched in 10-case sample.
- **19** JSON files have records but no matchable conditions.
- **10** labels/examples files skipped by design.
- **follow_pattern_actions.json** — no action executor.
- **08_priority_rules** PR* pipeline unused in production Interpretation.
- **cold_hot_rules.json / humidity_rules.json** — not loaded as matcher rules (cold/hot month scores are **hardcoded** in RuleContextBuilder from same TEMP001–012 knowledge).

---

## 8. Dead JSON (summary)

Hard-dead for matcher: strength/season files without conditions; special_case_rules/score/priority; follow conditions/actions/priority; combination conditions/priority; humidity; cold_hot (as matcher input).

Soft-dead: all module `*_labels.json` / `*_examples.json` for Interpretation.

Broken for Priority loader: `priority_rules.json` multi-document.

---

## 9. TODO (audit backlog — not started)

1. Repair Priority multi-JSON loading.
2. Decide production Priority strategy (KB PR* vs MatchedRuleResolver).
3. Luck Engine / luck signals in RuleContext.
4. Combination geometry facts producer.
5. Humidity / full climate scores beyond month branch.
6. Join or formally deprecate orphan conditions/actions catalogs.
7. Report Binding (structural sections) — **only after producers complete**.
8. Portal Binding — **only after Report Binding**.

---

## 10. Optimization Recommendations

| Priority | Recommendation | Why |
|----------|----------------|-----|
| P0 | Keep Report/Portal frozen until luck/combination producers exist | Avoid binding empty `--` |
| P0 | Fix or isolate 08_priority_rules multi-JSON | Unblocks PriorityRuleLoader |
| P1 | Document which JSON are “matcher rules” vs “reference tables” | Reduces false “dead” noise |
| P1 | Align folder→section map with career/wealth/health… | Clear Interpretation coverage |
| P2 | Deduplicate 103 overlapping IDs | Hygiene |
| P2 | Action runner for follow_pattern_actions **or** delete from “runtime KB” docs | Clarity |
| P3 | Replace hardcoded TEMP month map with loader of cold_hot_rules | Single source of truth |

---

## 11. Example Trace — `dung_than`

```text
Input datetime + gender
  → CalendarEngine.build
  → BaziEngine.build → day_master
  → PatternEngine.calculate → pattern code (e.g. chinh_quan)
  → RuleContextBuilder._build_useful_god
       PATTERN_USEFUL_GOD["chinh_quan"] = "Chính Quan"
       element + favorable/unfavorable (hy/ky)
  → enrich_result_from_rule_context
       PatternResult.dung_than / hy_than / ky_than
  → PatternView / API pattern.*
  → Portal pattern presenter
  → Interpretation useful_god section (rules)
  → Report HTML (prose useful_god section only today)
```

---

*End of SYSTEM_DATA_FLOW.md*
