# PIPELINE COVERAGE REPORT

**BTE Platform V1.0 — Sprint Audit 2**  
**Date:** 2026-07-28  
**Mode:** Audit only — no Report / Portal / code changes  

Companion docs:

- `KNOWLEDGE_USAGE_REPORT.md` (repo root)
- `engines/interpretation_engine/knowledge/docs/SYSTEM_DATA_FLOW.md`

---

## 1. Pipeline Coverage Matrix

| Stage | Producer | Consumer | Coverage % | Status |
|-------|----------|----------|------------:|--------|
| Calendar | CalendarEngine | Bazi, RuleContext, Portal, API | 95 | 🟢 |
| Bazi | BaziEngine (+ ShenShaService) | Pattern, RuleContext, Portal, API | 90 | 🟢 |
| Pattern | PatternEngine + FollowPatternCalculator | RuleContext, Portal, API | 85 | 🟢 |
| RuleContext | RuleContextBuilder | Score, Matcher, Interpretation | 80 | 🟡 |
| Score | ScoreEngine (+ strength.level sync) | RuleContext, Portal, API | 90 | 🟢 |
| Knowledge | KnowledgeRuleLoader | Matcher | 20* | 🟡 |
| Matcher | RuleMatcher | Priority resolver | 22** | 🟡 |
| Priority | MatchedRuleResolver (08 KB unused) | Builder | 50*** | 🟡 |
| Interpretation | Builder + Sentences + portal_view | Report, Portal, API | 75 | 🟡 |
| Report | render_from_analysis (interpretation only) | API / Narrative | 60 | 🟡 |
| Portal | JS presenters | User | 75 | 🟡 |
| API | OrchestratorService | Clients | 95 | 🟢 |

\* Knowledge % = loaded matchable / disk records (495 / 2,526).  
\*\* Matcher % = unique matched / loaded (107 / 495) over 10 cases.  
\*\*\* Priority % = match→resolve retention (~50%); 08 KB coverage = 0% on production path.

---

## 2. Producer Status After Sprint Producer Fixes

| Producer target | Status | Evidence (10-case sample) |
|-----------------|--------|---------------------------|
| Pattern.follow_type → tong_cach | 🟢 | Appears when chart qualifies (e.g. Tòng Vượng, Tòng Tài) |
| useful_god → hy_than / ky_than | 🟢 | Always populated when dung_than exists |
| Score → strength.level | 🟢 | balanced / weak after append |
| Bazi.shensha → RC → BaziView | 🟢 | 2–8 stars typical |
| temperature.status | 🟢 | slightly_hot / slightly_cold / neutral |

### Still weak / missing producers

| Gap | Status | Blocks |
|-----|--------|--------|
| Luck pillars / luck.available | 🔴 | Interpretation `luck` section |
| Combination geometry facts | 🔴 | Most 07_combination matches |
| Humidity / damp / dry scores | 🔴 | humidity_rules.json |
| Special case_name | 🔴 | Named special-case rules |
| Priority PR* KB execution | 🔴 | 08_priority_rules runtime |

---

## 3. Stage Detail

### 3.1 Calendar — 95%

| Signal | OK? |
|--------|-----|
| solar Y/M/D/H/M | 🟢 |
| lunar + leap | 🟢 |
| julian_day | 🟢 |
| solar_term | 🟢 |
| can_chi enrich from Bazi | 🟢 |
| timezone localization | 🟡 param unused (UTC+7 civil) |

### 3.2 Bazi — 90%

| Signal | OK? |
|--------|-----|
| Four pillars | 🟢 |
| hidden_stems | 🟢 |
| ten_gods | 🟢 |
| shensha | 🟢 (fixed) |
| Legacy ShenShaCalculator (FourPillars) | 🟡 unused; service classical path used |

### 3.3 Pattern — 85%

| Signal | OK? |
|--------|-----|
| main pattern / cach_cuc | 🟢 |
| follow_type / tong_cach | 🟢 when detected |
| dung_than / hy / ky | 🟢 |
| dieu_hau / than | 🟢 |
| pattern geometry attrs (visibility, clash_count, …) | 🔴 empty stubs |

### 3.4 RuleContext — 80%

| Namespace | Non-empty path ratio | Notes |
|-----------|---------------------:|-------|
| calendar | 10/10 | OK |
| bazi | 24/24 | OK |
| strength | 7/7 | OK after Score sync |
| temperature | 7/19 | status/cold/hot OK; humidity dead |
| useful_god | 10/11 | OK |
| luck | 2/7 | stub |
| pattern | 12/29 | follow_type intermittent; geometry empty |
| facts | present | many False → rules idle |

### 3.5 Score — 90%

| Signal | OK? |
|--------|-----|
| total / module scores | 🟢 |
| grade / confidence | 🟢 |
| append score section | 🟢 |
| strength.level update | 🟢 |
| luck_score meaningful | 🟡 luck unavailable |

### 3.6 Knowledge → Matcher → Priority → Interpretation

```text
Disk 2526 records
  → Loader 495 (19.6%)
  → Matched 107 union (21.6% of loaded)
  → Resolved 53 union (10.7% of loaded)
  → Interpreted ~65 union (13.1% of loaded)
  → Portal sections: summary/personality/career/relationship/health/
                     useful_god/conclusion/warning/strength (±weakness/wealth/pattern)
  → luck / children / yearly_fortune: 0/10
```

### 3.7 Report — 60%

| Aspect | Status |
|--------|--------|
| Runs without crash | 🟢 |
| HTML/MD from interpretation | 🟢 |
| Structural bind (Tứ trụ, Ngũ hành, Điểm số tables) | 🔴 deferred |
| Uses WP6 templates in orchestrator | 🔴 not on production path |

### 3.8 Portal — 75%

| UI block | Data source | Status |
|----------|-------------|--------|
| Chart info | calendar + input | 🟢 |
| Tứ trụ | bazi | 🟢 |
| Pattern cards | pattern | 🟢 (hy/ky/tong fixed) |
| Thần sát | bazi.shensha | 🟢 |
| Score | score | 🟢 |
| Interpretation prose | interpretation | 🟢 |
| Đại vận | — | 🔴 |
| Report structural HTML | report | 🟡 prose only |

---

## 4. Per-Case Pipeline Snapshot (10 cases)

| Case | Matched | Resolved | Sections | strength | temp | follow | shensha |
|------|--------:|---------:|----------|----------|------|--------|--------:|
| 1990-05-15 M | 87 | 35 | 9 | balanced | slightly_hot | Tòng Vượng | 5 |
| 1987-01-21 M | 84 | 35 | 11 | balanced | slightly_cold | — | 8 |
| 1992-02-04 F | 86 | 35 | 10 | balanced | neutral | — | 4 |
| 2000-02-29 F | 87 | 33 | 11 | balanced | neutral | Tòng Tài | 2 |
| 1984-02-04 M | 83 | 35 | 11 | balanced | neutral | — | 4 |
| 1975-07-01 M | 89 | 35 | 11 | balanced | slightly_hot | — | 2 |
| 1988-11-15 F | 83 | 35 | 12 | balanced | slightly_cold | — | 5 |
| 1995-08-08 M | 87 | 33 | 11 | balanced | neutral | Tòng Tài | 5 |
| 1968-02-05 F | 83 | 35 | 12 | balanced | neutral | — | 4 |
| 2010-06-21 M | 91 | 34 | 10 | weak | slightly_hot | — | 3 |

---

## 5. Interpretation Section Coverage

| Section | Rules (loader section map) | Rendered in sample | Coverage note |
|---------|---------------------------:|-------------------:|---------------|
| summary | 31 | 10/10 | 🟢 |
| strength | 17 | 10/10 | 🟢 post producer fix |
| pattern | 157 | 4/10 | 🟡 many follow/pattern idle |
| warning | 290 | 10/10 | 🟢 but tiny fraction of 290 |
| career | alias | 10/10 | 🟢 |
| wealth | alias | 5/10 | 🟡 |
| relationship | alias | 10/10 | 🟢 |
| health | alias | 10/10 | 🟢 |
| useful_god | alias | 10/10 | 🟢 |
| luck | — | 0/10 | 🔴 no luck producer |
| conclusion | alias | 10/10 | 🟢 |
| weakness | polarity | 9/10 | 🟢 |
| personality | alias | 10/10 | 🟢 |

---

## 6. Knowledge Funnel Diagram

```text
                    2526 disk records
                           │
              ┌────────────┴────────────┐
              │                         │
         soft-dead                 candidate
      labels/examples              + other JSON
           (10 files)                    │
                                         ▼
                              KnowledgeRuleLoader
                              requires conditions
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
              loaded 495           no_cond dead          priority broken
                                   (19 files)            (08 multi-JSON)
                    │
                    ▼
              RuleMatcher (10 cases)
                    │
              matched 107
                    │
              MatchedRuleResolver
                    │
              resolved 53
                    │
              Interpretation ~65 ids / sections
                    │
              Report (prose) / Portal
```

---

## 7. Aggregate Health Scores

| Score | % | How computed |
|-------|--:|--------------|
| **Knowledge Health** | **20** | 495 loaded ÷ 2,526 disk records |
| **Pipeline Health** | **82** | Weighted stage coverages (Calendar→Interpretation); Report/Portal held back |
| **Rule Coverage** | **22** | 107 matched ÷ 495 loaded |
| **Dead Knowledge** | **80** | 1 − (495 ÷ 2,526) |
| **Ready for Report Binding** | **75** | Core producers OK; luck/combination/humidity & Priority KB still open |

### Readiness gate for Report Binding

| Gate | Ready? |
|------|--------|
| Tứ trụ / Ngũ hành / Thập thần producers | ✅ |
| Cách cục / Dụng / Hỷ / Kỵ / Tòng / Thần sát | ✅ |
| Thân vượng nhược (strength.level) | ✅ |
| Temperature.status | ✅ |
| Đại vận (luck) | ❌ |
| Combination facts | ❌ |
| Priority KB (08) wired | ❌ |
| Report structural mapping designed | ❌ (deferred by policy) |

**Verdict:** Data producers for **core chart + pattern + strength + temperature + shensha** are ready.  
**Not yet green** for full commercial Report Binding until luck/combination (and Priority strategy) are decided.

---

## 8. Next Recommended Sprint (audit suggestion only)

1. Luck producer → `RuleContext.luck`  
2. Combination geometry facts  
3. Fix Priority multi-JSON + decide runtime wiring  
4. Then — and only then — Report Binding → Portal Binding  

---

*End of PIPELINE_COVERAGE_REPORT.md*
