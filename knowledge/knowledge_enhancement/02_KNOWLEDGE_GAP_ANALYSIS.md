# 02 — Knowledge Gap Analysis

Version: 1.0  
Status: **AUDIT COMPLETE — Awaiting review**  
Date: 2026-08-08  
Epic: Knowledge Coverage Audit (EPIC 1)  
Depends on: `01_KNOWLEDGE_COVERAGE_AUDIT.md`  

---

## 1. Purpose

Identify **what is missing** for commercial-grade BaZi consultation — without proposing architecture or runtime changes.

Gap categories:

1. Missing rules  
2. Missing mappings  
3. Missing explanations  
4. Missing edge cases  
5. Missing examples  
6. Missing practical guidance  

---

## 2. Gap summary

| Category | Severity | Commercial impact |
|----------|----------|-------------------|
| Missing explanations (classical + modern) | **Critical** | Cannot cite / teach / build trust |
| Thin narrative evidence units | **Critical** | Pack 05 → `partial_insufficient` / short prose |
| Orphan life-domain rules (unmapped to pipeline) | **High** | Wealth/marriage/career knowledge unused |
| Missing life domains (Parents, Education) | **High** | Incomplete consultation scope |
| Missing mappings (Canon citations, rule↔sentence) | **High** | Traceability / governance blocked |
| Missing edge cases (transform, follow break, clash+combine) | **Medium** | Wrong or silent special charts |
| Missing examples / gold consultation samples | **Medium** | Authoring & QA without reference |
| Missing practical guidance | **High** | Recommendations stay generic (CQ-4) |

---

## 3. Missing rules

### 3.1 Domains with no dedicated operational rule pack

| Domain | Gap | Notes |
|--------|-----|-------|
| Education | No CSV / no BaZi module | Entire domain absent |
| Parents | Schema file only (`17_parents.csv`) | No `05_phan_tich` pack |
| Personality (as consultation topic) | Interpreter stubs only | No knowledge pack |
| Transformations (first-class) | Framework domain empty | Partial coverage via pattern special cases only |

### 3.2 Domains with rules that are incomplete for consultation

| Domain | What exists | What is missing as rules |
|--------|-------------|--------------------------|
| Health | `health_rules.csv` (~13), health star scores | Condition → safe advice rules; contraindication language |
| Feng Shui | `fengshui_rules.csv` (~14) | Scope rules for “hint only” vs full feng shui product |
| Luck | Cycle tables + `luck_rules.csv` | Year/month narrative trigger rules for warnings |
| Useful God | Calculation rules strong | Soft-priority conflict narrative rules |

### 3.3 Dual-store risk (not missing, but confusing)

Operational CSVs (`database/12–15_*`) and knowledge JSON packs (`knowledge/rule_database/*_rules/`) both exist. Gap is **authoritative mapping documentation for content owners** — which store is the content expansion target for consultation prose vs calculation.

---

## 4. Missing mappings

| Mapping | Status | Gap |
|---------|--------|-----|
| Analysis signal → Knowledge entry (`20_knowledge.condition`) | Undefined in practice | 0 rows; no loader contract in production consultation path |
| Interpretation section → Pack 05 evidence kind | Partially defined | Technical prose still leaks then filtered → insufficient |
| Life-domain CSVs → Engines / Interpreters | **Unwired** | `08_hon_nhan`, `09_tu_tuc`, `10_tai_van`, most `interpretation_rules` |
| Knowledge Canon REF IDs → V1.0 SSOT | **Misaligned** | Wood citations use legacy REF meanings |
| Rule ID (CSV) ↔ Rule ID (JSON packs) ↔ Knowledge Record | Incomplete | Traceability for Official promotion blocked |
| Sentence Library ↔ Pack 04 library | Dual / unlinked | Framework empty; Pack 04 thin local library |
| BaZi module KR ↔ Canon concept | Policy drafted; content sparse | Fundamental KR markdown not promoted to Official JSON |

---

## 5. Missing explanations

### 5.1 Classical Knowledge Base (`database/20_knowledge`)

All 20 topic files: **header only, 0 rows**.

Missing for every planned topic:

- `classical_text`
- `modern_interpretation`
- `condition` (when to retrieve)
- `reference` (REF-/SRC- binding)
- `priority` / `confidence`

### 5.2 BaZi Blueprint academic content

| Module | Structure | Academic records |
|--------|-----------|------------------|
| `01_fundamental_knowledge` | Complete | Markdown KR notes only; **0** JSON in `knowledge_records/` |
| `02`–`14` | Complete | **Structure only — no academic Knowledge Records** |

### 5.3 Knowledge Canon

| Expected domains | Populated |
|------------------|-----------|
| 19 concept domains | Essentially **Wood** only |

Missing explanations for stems, branches, ten gods, strength, patterns, useful gods, clashes, punishments, harms, transformations, seasonal qi, temperature, shensha, luck, special cases.

### 5.4 Sentence / consultant phrasing

| Library | Status |
|---------|--------|
| `knowledge/sentence_library/` | Framework; no real sentences |
| Pack 04 `sentences.json` | ~11 sentences — far below commercial need |
| Content Quality guidelines | Specs exist (Exec / Rec / Warning) — **content inventory does not meet them** |

---

## 6. Missing edge cases

Documented or observed gaps:

| Edge case family | Knowledge gap |
|------------------|---------------|
| Follow / pseudo-follow break under luck | JSON packs cover calculation families; consultant explanation of “cách cục bị phá” thin |
| Clash + combine coexistence | Special-case rules exist; narrative mitigation language missing |
| Transformed patterns | Framework `09_transformations` empty; limited explainable doctrine |
| Extreme temperature imbalance | Rules thin; practical balance advice missing |
| Conflicting useful god vs season | Priority rules exist; user-facing resolution story missing |
| Empty / low-confidence evidence | Approved insufficient copy exists; **enrichment path** missing |
| Ethical life-domain (marriage / health / children) | No approved caution templates for sensitive claims |
| Dual pillar voids / missing hour | Chart edge handling vs consultation disclaimer gap |

Reference: `knowledge/rule_database/EDGE_CASES.md` (framework coexistence) — does not replace consultation edge-case knowledge.

---

## 7. Missing examples

| Example type | Status |
|--------------|--------|
| BaZi module `examples/example_record.json` | Template / placeholder level |
| Consultation gold samples (full NarrativeResult) | Not a curated knowledge corpus |
| Life-domain worked examples (career / marriage / wealth) | Missing |
| Classical quotation → modern paraphrase pairs | Missing (`20_knowledge` empty) |
| Edge-case chart → correct warning/recommendation | Sparse vs commercial need |
| Reference chapter anchors for classics | Chapter support empty (Reference Coverage Report) |

---

## 8. Missing practical guidance

Commercial consultation requires actionable guidance. Current gaps:

| Guidance need | Current state | Gap |
|---------------|---------------|-----|
| What to do this decade / year | Luck analysis factual | Timing language + next action specificity |
| How to use Useful God in life choices | Score / selection present | Practical “do / avoid” without superstition overclaim |
| Career direction | Orphan `tai_van` / career_rules | Wired, curated, consultant-safe advice |
| Relationship caution | Orphan marriage rules | Ethical framing + mitigation |
| Health lifestyle hints | Thin / unwired | Non-medical, element-balance guidance |
| Wealth pacing | Orphan wealth rules | Risk vs opportunity language |
| Warning mitigation (CQ-5) | Inconsistent | Every warning needs a paired mitigation |
| Recommendation specificity (CQ-4) | Often generic | Condition-bound actions |

---

## 9. Gap → commercial symptom map

| User-visible symptom | Upstream knowledge gap |
|----------------------|------------------------|
| `partial_insufficient` / “Chưa đủ dữ liệu…” | Thin commercial evidence units |
| Short Executive Summary | Missing identity/strength/weakness/action packing |
| Generic recommendations | Missing practical guidance corpus |
| Warnings without next step | Missing mitigation templates |
| No marriage/career depth on Result Page | Life domains unwired + empty explainable KB |
| Cannot cite classics | `20_knowledge` empty; Canon sparse |
| Inconsistent terminology | Terminology seed too small for life topics |

---

## 10. Explicit non-gaps (out of scope for “knowledge missing”)

These are **not** knowledge gaps of this epic:

- Pack 05 composer architecture (complete)
- Foundation / Design System (frozen)
- Portal preference for `narrative_result` (Product Integration done)
- Parallel BaZi Result screen (product cleanup, not knowledge)
- Report Engine redesign (separate epic)

---

## 11. Recommended gap closure order (preview)

Full ranking in `06_PRIORITY_EXPANSION_PLAN.md`. Preview:

1. Commercial evidence / sentence units for structural domains (feed Pack 05)  
2. Seed `20_knowledge` for Five Elements, Ten Gods, Useful God, Strength, Patterns  
3. Map or retire orphan life-domain rules; seed Career / Wealth / Marriage explanations  
4. Canon population + REF remapping  
5. Parents / Education / Transformations / Personality  

---

## 12. Stop line

Gap analysis complete. **Await review before authoring knowledge rows.**

---

END
