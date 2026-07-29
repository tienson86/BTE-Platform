# Pipeline Data Trace Report

| Item | Value |
|------|-------|
| Document | PIPELINE_DATA_TRACE_REPORT.md |
| Project | BTE Platform V1.0 |
| Audit Type | Runtime Data Flow Trace (READ-ONLY) |
| Case | **21/01/1987 04:30** (male) |
| Chart | Canh Ngọ — Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần |
| Production Path | `OrchestratorService` Stages 0–12 |
| Date | 2026-07-28 |

**Constraints:** No source modifications. Report only.

---

## Executive Summary

Traced one live chart through Stages **0→12**. Core calculation contexts (Calendar, BaZi, Pattern recognition, RuleContext, ScoreResult, Knowledge→Match→Priority→Interpretation→Report) **carry data**, but several contract contexts are **untyped / empty / sparse**, and there are clear **loss points**:

| Loss / empty onset | What happens |
|--------------------|--------------|
| **Stage 4 (stop at `pattern`)** | PatternView thiếu `than` / `hy_than` / `ky_than` / `dung_than` (chưa enrich Stage 5) |
| **Stage 5 RuleContext** | `luck` rỗng; `combination` = null; nhiều field pattern = null; `strength.level` = `unknown`; `score.*` = 0; `tong_cach` rỗng (`follow_type` null) |
| **Stage 6 Score** | `wuxing_score` = 0; `luck_score` = 0 (dù module chạy) |
| **Stages 7–9** | Không có typed `KnowledgeContext` / `MatchedRuleSet` / `ResolvedRuleSet` — chỉ list + meta; funnel **495 → 84 → 35** |
| **Stage 10 → API view** | Portal Interpretation **mất** `matched_rule_count` / `resolved_rule_count` / `coverage` / `summary` (null); `sentence_count` 46→25; `section_count` 12→11 |
| **Contract gaps** | `ScoreContext`, `KnowledgeContext`, `MatchedRuleSet`, `ResolvedRuleSet`, `ReportDocument`, `InputRequestContext` **không được publish** đúng tên contract |

**Overall data health for this case:** Pipeline runnable; richest payload at Stage 5–6; largest semantic drop at **luck/combination emptiness** and **Interpretation portal projection**.

---

## Case Snapshot

| Field | Value |
|-------|-------|
| Birth | 1987-01-21 04:30 male |
| Day Master | **Canh** (Kim) |
| Pillars | Bính Dần · Tân Sửu · Canh Ngọ · Mậu Dần |
| Ten Gods | Thất Sát, Kiếp Tài, Nhật Chủ, Thiên Ấn |
| Shensha (8) | Thiên Ất Quý Nhân, Thiên Ất, Hồng Loan, Thiên Hỷ, Thiên Đức, Thiên Đức Quý Nhân, Nguyệt Đức, Nguyệt Đức Quý Nhân |
| Pattern | **chinh_quan** / Chính Quan (score 91, priority 100) |
| Feng Shui | Khôn · Tây Tứ Trạch |
| Score total | **55.25** (grade D+, confidence medium) |
| Knowledge | loaded **495** → matched **84** → resolved **35** (discarded 49) |
| Interpretation (engine) | 12 sections, 46 sentences, coverage ~0.0707 |
| Report | HTML 1738 chars, Markdown 1498 chars, 11 sections |

---

## Stage-by-Stage Trace

### Stage 0 — Input

| Item | Detail |
|------|--------|
| Contract context | `InputRequestContext` — **MISSING** (ad-hoc dict) |
| Published | `input`: year/month/day/hour/minute/gender, `validated=true` |
| Count | 7 fields, all nonempty |
| Empty? | No |
| Loss? | No — validation only |

---

### Stage 1 — Calendar

| Item | Detail |
|------|--------|
| Contract context | `CalendarContext` unused; runtime **`CalendarResult`** |
| Published (API) | solar 1987-01-21 04:30; later can_chi filled after BaZi |
| Main content | Solar + lunar objects present on engine result |
| Empty? | No |
| Loss? | Can_chi not native on Calendar SSOT until orchestrator view merge (after Stage 2/3) |

---

### Stage 2 — BaZi

| Item | Detail |
|------|--------|
| Contract context | `BaziContext` unused as publish type; runtime **`BaziChart` / BaziView** |
| Counts | 4 pillars; 11 hidden stems; 4 ten_gods; 8 shensha |
| Main content | Day Master Canh; pillars + nap_am + hidden per pillar; shensha list |
| Empty? | No |
| Loss? | Enrichment still via API `bazi_truth` (outside engine purity) — data present |

---

### Stage 3 — Feng Shui

| Item | Detail |
|------|--------|
| Contract context | `FengShuiContext` — **MISSING typed**; dict published |
| Main content | gua_number=2, Khôn, Tây Tứ Trạch, cung_phi/menh_quai/nhom_trach |
| Empty? | No (gender present) |
| Loss? | Also merged into calendar view fields |

---

### Stage 4 — Pattern

| Item | Detail |
|------|--------|
| Contract context | **`PatternContext`** (input) — FULL |
| PatternContext | year/month/day/hour pillars, day_master, ten_gods.list (4), shensha (8), calendar+bazi refs |
| PatternResult (engine) | success, pattern=`chinh_quan`, cach_cuc, score=91, priority=100, matched_rules=5 |
| PatternResult before Stage 5 enrich | `than`/`tong_cach`/`dung_than`/`hy_than`/`ky_than` = **""**; `rule_context` = **{}** |
| API stop at `pattern` | Only success/pattern/cach_cuc/score/priority — **view fields empty** |
| Empty / loss onset | **First intentional empty:** PatternView enrich fields until Stage 5 |

---

### Stage 5 — RuleContext

| Item | Detail |
|------|--------|
| Contract context | **`RuleContext`** (dict) — PUBLISHED |
| Producer | `build_rule_context` / RuleContextBuilder (sole Stage 5) |
| Top-level keys | **71** |
| After enrich PatternResult | than=Kim; dung_than=Chính Quan; hy=Mộc; ky=Thủy; dieu_hau=Đắc lệnh; `tong_cach` still **""** |
| `rule_context` attached to PatternResult | 71 keys |

#### RuleContext section health

| Section | Nonempty keys | Empty / null highlights | Status |
|---------|--------------:|-------------------------|--------|
| calendar | 9/9 | — | Healthy |
| bazi | 11/11 | — | Healthy |
| pattern | 10/28 | follow_type, category, clash_count, combination_status, purity, … | **Sparse** |
| wuxing | 9/15 | balance_level, combination_type, clash_type, … | Partial |
| hidden_stems | 5/5 | — | Healthy |
| ten_gods | 22/24 | structure, destroyed_ten_gods | Mostly healthy |
| shensha | 12/12 | — | Healthy |
| strength | 6/6 | level=**unknown**, score=**0.0** (pre-Score) | Weak until Stage 6 |
| useful_god | 8/10 | role=null | Mostly healthy |
| temperature | status/cold/hot present | **12 nulls** (humidity, climate_pattern, damp/dry, bands, …) | Partial |
| **luck** | **0/6** | pillars=[], status/phase/support/attack null, available=false | **EMPTY** |
| metadata | 0 | empty dict | Empty |
| score (stub) | zeros / empty grade | total/modules = 0 | Stub until Stage 6 |
| combination | — | **null** (no section) | **MISSING** |
| facts | True≈44; False≈112 | many false flags | Present |

**Loss onset (Stage 5):** first major business emptiness — **luck**, **combination**, **tong_cach/follow_type**, pattern detail fields, **strength.level=unknown**, temperature humidity/climate nulls.

---

### Stage 6 — Score

| Item | Detail |
|------|--------|
| Contract context | **`ScoreContext` — NOT PUBLISHED** (class exists, unused on SSOT) |
| Published | **`ScoreResult`** + composed matching dict (copy; published RC immutable) |
| ScoreResult | total=**55.25**; strength=45; ten_god=100; pattern=100; useful_god=20; shensha=100; **wuxing=0**; **luck=0**; grade=D+; confidence=medium |
| Modules in details | final_score, luck, pattern, shensha, strength, ten_gods, useful_god, wuxing |
| Composed strength.level | **balanced** (was unknown) |
| Facts added by Score | balanced_day_master, day_master_strength_calculated, strength_balanced, than_score_da_tinh, than_vuong_nhuoc_da_xac_dinh |
| Empty / loss | **wuxing_score=0** and **luck_score=0** despite modules listed — numeric loss for those dimensions |

---

### Stage 7 — Knowledge

| Item | Detail |
|------|--------|
| Contract context | **`KnowledgeContext` — MISSING** |
| Runtime | rule list via `load_knowledge_rules()` |
| Count | **495** loaded rules |
| API payload | `{ rule_count: 495 }` only — **no rule bodies published** |
| Empty? | Count nonempty; typed context absent |
| Loss? | Full rule set not exposed in API stage payload (only count) |

---

### Stage 8 — Matching

| Item | Detail |
|------|--------|
| Contract context | **`MatchedRuleSet` — MISSING** (plain list) |
| Count | **84** matched / scored |
| Sample IDs | FPR092, FPR030, FPR040, … SDR_0301 |
| API payload | `{ matched_count: 84 }` |
| Funnel drop | 495 → 84 (**~83% rules never match** this chart) |
| Loss onset | Large unused knowledge (expected matching filter; still a coverage drop) |

---

### Stage 9 — Priority

| Item | Detail |
|------|--------|
| Contract context | **`ResolvedRuleSet` — MISSING** (list + meta dict) |
| Count | resolved **35**; discarded **49**; matched meta 84 |
| Discard reason (sample) | section `pattern` diversity cap (20) — PAT*/PSC* discarded vs FPR092 |
| API | resolved_count/matched_count/discarded lists |
| Loss | 84 → 35 (**49 discarded** by MatchedRuleResolver, not 08 Priority KB) |

---

### Stage 10 — Interpretation

| Item | Detail |
|------|--------|
| Contract context | **`InterpretationResult`** — present (engine) |
| Engine result | summary_len=151; sections=**12**; sentences=**46**; matched=84; resolved=35; coverage≈0.0707; rules_used=35; unused=460; discarded=49 |
| Section keys | career, conclusion, health, luck, pattern, personality, relationship, strength, summary, useful_god, warning, weakness, wealth |
| API Interpretation view | section_count=**11**; sentence_count=**25**; matched/resolved/coverage/summary = **null**; sections type=`list` |
| Loss onset | **Portal/view projection** strips metrics + reduces sentences/sections vs engine object |

---

### Stage 11 — Report

| Item | Detail |
|------|--------|
| Contract context | **`ReportDocument` — MISSING**; runtime ReportResult / portal dict |
| Content | title “Bản luận Bát tự”; section_count=11; html_len=1738; markdown_len=1498 |
| Empty? | No |
| Loss? | Bound to Interpretation **view** (already reduced), not full engine InterpretationResult |

---

### Stage 12 — Delivery

| Item | Detail |
|------|--------|
| Contract context | ClientResponse — implicit JSON |
| Published | `delivery={format:json, includes_narrative:true}` + `narrative` (title/html/markdown/section_count) |
| Empty? | No |
| Loss? | Transport only; inherits upstream view losses |

---

## Context Ownership Matrix (this run)

| Context | Produced? | Count / main | Empty / sparse? | Notes |
|---------|-----------|--------------|-----------------|-------|
| InputRequestContext | No (ad-hoc) | 7 fields | No | Stage 0 |
| CalendarContext | No | CalendarResult used | No | |
| BaziContext | No | BaziChart/View used | No | |
| FengShuiContext | No | dict | No | |
| PatternContext | Yes | Full pillars/gods/shensha | No | Stage 4 input |
| PatternResult | Yes | chinh_quan + enrich after S5 | View empty if stop@S4 | |
| RuleContext | Yes | 71 keys | luck empty; combination null; many nulls | Stage 5 |
| ScoreContext | **No** | — | Contract gap | ScoreResult instead |
| ScoreResult | Yes | 55.25 / D+ | wuxing=0, luck=0 | Stage 6 |
| Composed matching dict | Yes | strength.level=balanced | Not published as Stage 5 RC | Downstream only |
| KnowledgeContext | **No** | 495 rules (internal) | API only count | Stage 7 |
| MatchedRuleSet | **No** | 84 list | Untyped | Stage 8 |
| ResolvedRuleSet | **No** | 35 list | Untyped | Stage 9 |
| InterpretationResult | Yes | 12 sec / 46 sent | API view loses fields | Stage 10 |
| ReportDocument | **No** | portal report dict | Untyped | Stage 11 |

---

## Data Funnel

```text
Birth 1987-01-21 04:30 male
  → CalendarResult OK
  → BaziChart OK (4 pillars, 8 shensha)
  → FengShui dict OK
  → PatternContext OK → PatternResult (chinh_quan, score 91)
  → RuleContext 71 keys
        ✗ luck EMPTY
        ✗ combination NULL
        ✗ tong_cach / follow_type EMPTY
        ~ temperature partial (12 null fields)
        ~ strength.level unknown (pre-Score)
  → ScoreResult 55.25
        ✗ wuxing_score = 0
        ✗ luck_score = 0
  → Knowledge 495
  → Matched 84          (−411 never matched)
  → Resolved 35         (−49 discarded)
  → InterpretationResult 12/46/coverage 0.07
  → API Interpretation view 11/25 + null metrics   ← VIEW LOSS
  → Report HTML/MD OK
  → Delivery JSON OK
```

---

## Where Data Starts Missing (ordered)

1. **Stage 4 stop** — PatternView enrich fields empty until Stage 5 (by design after Sprint 1).
2. **Stage 5** — **Luck completely empty**; **combination absent**; **follow_type/tong_cach empty**; many pattern analytics null; strength not yet scored; temperature humidity/climate null.
3. **Stage 6** — **Wuxing score and Luck score remain 0** in ScoreResult.
4. **Stage 7–9** — No typed contexts; knowledge body not in API; **495→84→35** funnel.
5. **Stage 10 API projection** — Engine has summary/metrics/46 sentences; **portal drops metrics and shrinks content**.

---

## Verdict for this chart

| Question | Answer |
|----------|--------|
| Does pipeline produce a usable report? | **Yes** |
| Is RuleContext rich enough to match rules? | **Yes** (84 matches) |
| Are all contract contexts present? | **No** |
| Earliest structural emptiness | **Stage 5: luck + combination** |
| Earliest presentation emptiness | **Stage 4 stop (pre-enrich)** |
| Largest post-engine loss | **Interpretation → API/Report view** |

---

## Appendix — Pipeline completed list (full analyze)

```text
input → calendar → bazi → feng_shui → pattern → rule_context
→ score → knowledge → matching → priority → interpretation
→ report → delivery
```

---

**END** — Read-only runtime trace. No source code modified.
