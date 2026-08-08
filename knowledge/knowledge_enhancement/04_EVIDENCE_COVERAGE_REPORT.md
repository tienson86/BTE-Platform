# 04 — Evidence Coverage Report

Version: 1.0  
Status: **AUDIT COMPLETE — Awaiting review**  
Date: 2026-08-08  
Epic: Knowledge Coverage Audit (EPIC 1)  
Depends on: `01_KNOWLEDGE_COVERAGE_AUDIT.md`, `02_KNOWLEDGE_GAP_ANALYSIS.md`  

---

## 1. Purpose

Determine whether **Evidence** is sufficient for commercial Narrative outputs:

- Executive Summary  
- Recommendation  
- Warning  
- Narrative (Observation, Reasoning, Impact, Conclusion)  

Evidence here means **commercial evidence units** that Pack 05 can accept after technical filtering — not raw rule-match dumps.

---

## 2. Evidence model (V1)

### 2.1 Pack 05 evidence kinds

| Kind | Role in consultation |
|------|----------------------|
| `identity` | Who / what structure (day master, pattern) |
| `strength` | Favorable / supportive signals |
| `weakness` | Limiting signals |
| `risk` | Caution signals |
| `action` | What to do / prioritize |
| `grade` | Score / rating signal |
| `explanation` | Why (often gated if technical) |
| `implication` | So-what / impact |

### 2.2 Upstream sources

| Source | Commercial usefulness today |
|--------|----------------------------|
| AnalysisResult (strength, pattern, useful god, scores) | **Primary** factual substrate |
| InterpretationResult section bodies | Mixed — often filtered as technical |
| Pack 04 sentence library (~11) | **Too thin** |
| `database/20_knowledge` | **Empty** |
| `knowledge/sentence_library` | Empty framework |
| Orphan life-domain rules | Not available on Narrative path |

---

## 3. Sufficiency criteria

Aligned with Content Quality Release B (`knowledge/releases/v1/content_quality/`):

| Output | Minimum evidence for commercial grade |
|--------|----------------------------------------|
| Executive Summary | identity + ≥1 strength + ≥1 weakness/risk + ≥1 action + grade (when available) |
| Observation | identity + factual strength/grade |
| Reasoning | non-technical explanation |
| Impact | implication tied to chart facts |
| Recommendation | specific action bound to useful god / luck / pattern |
| Warning | risk/weakness **plus** mitigation action |
| Conclusion | settles identity + priority action |

Approved insufficient copy: *“Chưa đủ dữ liệu để đưa ra kết luận.”* — correct behavior when empty, **not** a commercial success.

---

## 4. Coverage by Narrative output

| Output | Required kinds | Typical availability | Sufficiency | Notes |
|--------|----------------|----------------------|-------------|-------|
| **Executive Summary** | identity, strength, weakness, action, risk, grade | Partial | **Insufficient for commercial briefing** | CQ-3: incomplete seven commercial answers |
| **Observation** | identity, strength, grade | Often present | **Partial** | Short when thin |
| **Reasoning** | explanation | Often technical → filtered | **Insufficient** | D2 quality: rule prose filtered |
| **Impact** | implication | Sparse | **Insufficient** | Few dedicated implication units |
| **Recommendation** | action | Generic / sparse | **Insufficient** | CQ-4 |
| **Warning** | risk, weakness (+ mitigation via action) | Risk sometimes; mitigation rare | **Partial** | CQ-5 |
| **Conclusion** | mixed settle set | Partial | **Partial** | Better when summary slots fill |
| **NarrativeSummary slots** | identity, strengths[], weaknesses[], priority_recommendation, next_action | Frequent `insufficient_flags` | **Partial** | G6 |

---

## 5. Evidence coverage matrix (by domain)

| Domain | Can emit identity | strength | weakness/risk | action | explanation | Commercial evidence grade |
|--------|-------------------|----------|---------------|--------|-------------|---------------------------|
| Day master / chart | Yes | — | — | — | Thin | Partial |
| Strength | Yes | Yes | Partial | Rare | Partial / technical | Partial |
| Pattern | Yes | Partial | Partial | Rare | Thin | Partial |
| Useful God | Yes | Partial | Partial | **Best action source** | Thin | Partial–Best |
| Ten Gods | Partial | Partial | Partial | Rare | Thin | Partial |
| Five Elements | Partial | Partial | Partial | Rare | Thin | Partial |
| Season / Temperature | Partial | Partial | Partial | Rare | Thin | Partial |
| Shensha | Partial | — | Partial (risk) | Rare | Thin | Partial |
| Luck | Partial | Partial | Partial | Partial | Thin | Partial |
| Combination / Clash | Partial | — | Partial | Rare | Thin | Partial |
| Career / Wealth / Marriage / … | No (unwired) | No | No | No | No | **Missing** |

---

## 6. Quantitative picture (approximate)

| Metric | Estimate |
|--------|----------|
| Pack 04 commercial sentences | ~11 |
| Pack 04 narrative rules | ~12 |
| `20_knowledge` explainable rows | 0 |
| Structural AnalysisResult fields usable as evidence | Moderate |
| Life-domain evidence on commercial path | ~0 |
| Live runs with `partial_insufficient` | Common (documented G6) |

**Verdict:** Evidence is **structurally typed** but **volumetrically insufficient** for consultant-grade Narrative.

---

## 7. Filtering loss

Technical filters correctly remove calculator language (“kích hoạt khi”, matched rules, mock/placeholder).  

**Side effect:** When Interpretation only emits technical rule prose, filtering leaves **empty commercial evidence** → insufficient Narrative.

This is a **knowledge / authoring gap**, not a filter bug.

---

## 8. Evidence vs Content Quality gaps

| CQ ID | Gap | Evidence root cause |
|-------|-----|---------------------|
| CQ-1 / G6 | Thin upstream → short / insufficient | Too few commercial units |
| CQ-3 | Exec Summary incomplete | Missing packed kinds for briefing |
| CQ-4 | Generic recommendations | Missing condition-bound action corpus |
| CQ-5 | Warnings without mitigation | Missing risk→action pairs |
| CQ-2 | System framing prefixes | Composer wording (not primary knowledge volume) |

---

## 9. Sufficiency scorecard

| Target | Score | Ready for commercial consultation? |
|--------|------:|------------------------------------|
| Executive Summary evidence | 35% | No |
| Recommendation evidence | 30% | No |
| Warning evidence | 40% | No (mitigation gap) |
| Full Narrative (7 sections) | 40% | No |
| Structural factual substrate | 70% | Yes (as facts, not prose) |
| **Overall evidence readiness** | **~38%** | **No** |

---

## 10. What “enough evidence” would look like (target, not implementation)

Without changing architecture:

1. For each structural domain, a curated set of **commercial** evidence sentences keyed by Analysis signals.  
2. Explicit **action** and **risk+mitigation** pairs for Useful God / Luck / Clash.  
3. Optional retrieval from `20_knowledge` for classical + modern explanation (future Knowledge Expert).  
4. Life-domain evidence only after wiring and ethics review.

---

## 11. Stop line

Evidence coverage report complete. Enrichment is a **future epic** after review.

---

END
