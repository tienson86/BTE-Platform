# Phase 03 — ADVANTAGES Review

| Field | Value |
|-------|-------|
| Document | PHASE_03_ADVANTAGES_REVIEW |
| Pack | PACK_01_STRENGTH |
| Topic | advantages |
| Phase | 3 — ADVANTAGES only |
| Units reviewed | 35 |
| Source | `knowledge/interpretation_knowledge/PACK_01_STRENGTH/03_ADVANTAGES.md` |
| Catalog | `knowledge/knowledge_catalog/PACK_01_STRENGTH/catalog/advantages/` |
| Date | 2026-08-12 |
| Role | Knowledge QA — no knowledge rewritten |

---

# 1. QA process (deterministic)

Review order: by `knowledge_id` ascending (`IK-STR-ADV-0001` … `IK-STR-ADV-0035`).

Seven facets × five classes = 35 units. All units share the same schema shape: `CLASS_ONLY`, `required_facts: classification`, and a limitation that cause must be present — **without cause fact keys in schema**.

Each unit scored **0–10** on nine criteria:

| # | Criterion | What was checked |
|---|-----------|------------------|
| 1 | Professional correctness | Usable capacity, not compliment; source-faithful; class-appropriate |
| 2 | Evidence compatibility | Strength facts only; no hidden Pattern/UG/Ten Gods/Luck need |
| 3 | Domain purity | True ADVANTAGE vs Meaning/Personality/Career/Recommendation/Challenge bleed |
| 4 | Duplicate risk | Same customer value elsewhere; declared clusters noted, not merged |
| 5 | Customer value | Insight if read alone; generic vs decisive |
| 6 | Actionability | Customer can use it vs descriptive only |
| 7 | Readability | Natural consultant language; commercial tone |
| 8 | Explainability | If removed, is an important insight lost? (LOW if no) |
| 9 | Strength-only validity | No cross-pack dependency (Career, Luck, Marriage, Pattern, UG, Ten Gods, ShenSha) |

Overall: **PASS** / **REVIEW** / **FAIL**. No catalog edits performed.

---

# 2. Cross-cutting findings (all 35 units)

## 2.1 Systemic evidence gap

Every unit uses `required_evidence: CLASS_ONLY` and `required_facts: classification` only. Every unit’s limitations say: *“If a cause that creates the advantage is absent in the case, do not use this unit.”*

That rule is **not schema-enforced**. Composer/Reasoning must gate on published season/root/support/drain/control — otherwise advantages can print on class alone. This caps Evidence Compatibility at **8** for most units unless selection policy compensates.

## 2.2 Composition rule not catalogued

Source §8 (“pick three to five facets”) is not a Knowledge Unit. All 35 units remain individually selectable. Budget policy is external — not a FAIL, but drives duplicate and explainability risk when all seven print.

## 2.3 Declared duplicate clusters (unchanged)

| Cluster | Members in ADVANTAGES |
|---------|----------------------|
| `DUP-STR-CARRY_LOAD` | `ADV-0006`, `ADV-0013` (0013 = golden representative intent) |
| `DUP-STR-FULL_TANK` | `ADV-0014` (member; `MEAN-0006` = representative per architecture) |

Golden CASE-0001 keeps `ADV-0013` + `ADV-0009`; rejects `ADV-0014` via `DUP-STR-FULL_TANK` / budget.

---

# 3. Unit reviews

Scores: **PC** Professional | **EV** Evidence | **DP** Domain purity | **DR** Duplicate | **CV** Customer value | **AC** Actionability | **RD** Readability | **EX** Explainability | **ST** Strength-only

---

## Very Strong (`ADV-0001` – `ADV-0007`)

| ID | Title | PC | EV | DP | DR | CV | AC | RD | EX | ST | Avg | Verdict |
|----|-------|---:|---:|---:|---:|---:|---:|---:|---:|---:|----:|---------|
| 0001 | decision making | 10 | 8 | 9 | 9 | 9 | 9 | 10 | 9 | 10 | 9.2 | **PASS** |
| 0002 | leadership | 10 | 8 | 9 | 8 | 9 | 8 | 10 | 8 | 10 | 8.9 | **PASS** |
| 0003 | learning | 10 | 8 | 8 | 9 | 8 | 7 | 9 | 7 | 9 | 8.3 | **REVIEW** |
| 0004 | discipline | 10 | 8 | 9 | 8 | 8 | 7 | 9 | 7 | 10 | 8.4 | **REVIEW** |
| 0005 | adaptability | 10 | 8 | 9 | 9 | 7 | 8 | 9 | 6 | 10 | 8.2 | **REVIEW** |
| 0006 | responsibility | 9 | 8 | 8 | 6 | 9 | 8 | 9 | 8 | 10 | 8.3 | **REVIEW** |
| 0007 | stress tolerance | 10 | 8 | 9 | 7 | 8 | 7 | 9 | 7 | 10 | 8.3 | **REVIEW** |

**0001 PASS** — Actionable (“use where delay is the real risk”). True advantage; no cross-pack.

**0002 PASS** — Turnaround leadership capacity; overlaps MEAN “certainty” slightly but adds commercial use-case.

**0003 REVIEW** — Domain: learning examples (craft, sport, exam) lightly bleed **Career** (soft cross-pack). Explainability moderate if other facets kept. Missing: cause gate in schema.

**0004 REVIEW** — Explainability LOW if customer already has discipline-themed MEANING traits. Optional facet.

**0005 REVIEW** — Source says *not headline gift*; `OPTIONAL`/`DETAIL` correct. **LOW EXPLAINABILITY** if removed when 0001–0002 present. Meta-instruction (“Sell capacity…”) is composer-facing.

**0006 REVIEW** — `DUP-STR-CARRY_LOAD` member; overlaps `ADV-0013` family and future CHAL “take every load”. Domain bleed toward **Challenge** if cost sentence implied. Do not co-select with 0013.

**0007 REVIEW** — Advantage overlaps CHAL “never leaving fire” (limitation acknowledges). Pair with challenge later, not alone.

---

## Strong (`ADV-0008` – `ADV-0014`)

| ID | Title | PC | EV | DP | DR | CV | AC | RD | EX | ST | Avg | Verdict |
|----|-------|---:|---:|---:|---:|---:|---:|---:|---:|---:|----:|---------|
| 0008 | decision making | 10 | 8 | 9 | 8 | 8 | 7 | 10 | 7 | 10 | 8.6 | **REVIEW** |
| 0009 | leadership | 10 | 8 | 9 | 8 | 9 | 8 | 10 | 9 | 10 | 8.9 | **PASS** |
| 0010 | learning | 10 | 8 | 8 | 8 | 8 | 8 | 9 | 7 | 8 | 8.3 | **REVIEW** |
| 0011 | discipline | 10 | 8 | 9 | 9 | 8 | 7 | 9 | 7 | 10 | 8.4 | **REVIEW** |
| 0012 | adaptability | 9 | 8 | 9 | 9 | 6 | 7 | 9 | 5 | 10 | 8.0 | **REVIEW** |
| 0013 | responsibility | 10 | 8 | 9 | 6 | 10 | 9 | 10 | 10 | 9 | 9.0 | **PASS** |
| 0014 | stress tolerance | 10 | 8 | 9 | 5 | 8 | 7 | 9 | 6 | 10 | 8.0 | **REVIEW** |

**0008 REVIEW** — Overlaps MEAN-0006 “decision stays decided” / inner weight. **LOW EXPLAINABILITY** if MEANING already kept. Still valid as DECISION_MAKING facet.

**0009 PASS** — Golden CASE-0001 unit. “Staying power, not theatre” is distinct, actionable, Strength-only.

**0010 REVIEW** — **CROSS-PACK (Career):** “apprenticeship, on-the-job mastery, roles that reward persistence”. Domain purity: learning advantage with career examples. Acceptable from source but mark Career dependency.

**0011 REVIEW** — Generic maintenance advantage; removable if budget tight without losing class story.

**0012 REVIEW** — `OPTIONAL`/`DETAIL` correct. **LOW EXPLAINABILITY** — sprint-by-effort is detail, not headline Strong asset.

**0013 PASS** — Golden representative for `DUP-STR-CARRY_LOAD`. High commercial value (“employable in the deep sense”). Actionable employability frame without job titles.

**0014 REVIEW** — `DUP-STR-FULL_TANK` member vs `MEAN-0006`. Golden **rejects** when representative MEAN passes. Must not co-print with MEAN full-tank story.

---

## Balanced (`ADV-0015` – `ADV-0021`)

| ID | Title | PC | EV | DP | DR | CV | AC | RD | EX | ST | Avg | Verdict |
|----|-------|---:|---:|---:|---:|---:|---:|---:|---:|---:|----:|---------|
| 0015 | decision making | 10 | 8 | 9 | 7 | 9 | 8 | 10 | 8 | 10 | 8.8 | **PASS** |
| 0016 | leadership | 10 | 8 | 9 | 8 | 9 | 8 | 10 | 8 | 10 | 8.9 | **PASS** |
| 0017 | learning | 10 | 8 | 9 | 9 | 7 | 6 | 9 | 6 | 10 | 8.2 | **REVIEW** |
| 0018 | discipline | 10 | 8 | 9 | 9 | 8 | 7 | 9 | 7 | 10 | 8.4 | **REVIEW** |
| 0019 | adaptability | 10 | 8 | 8 | 8 | 9 | 8 | 10 | 9 | 8 | 8.8 | **PASS** |
| 0020 | responsibility | 10 | 8 | 9 | 9 | 8 | 7 | 9 | 7 | 10 | 8.4 | **REVIEW** |
| 0021 | stress tolerance | 10 | 8 | 9 | 8 | 8 | 7 | 9 | 7 | 10 | 8.4 | **REVIEW** |

**0015 PASS** — Prevents binary mistakes; limitation points cost to CHAL — good separation.

**0016 PASS** — Mixed-team leadership value; commercially distinct.

**0017 REVIEW** — **LOW EXPLAINABILITY**; adequate not headline. Removable without losing Balanced story if 0019 kept.

**0018 REVIEW** — Creative-operational hybrid mention is mild **Career** touch. Optional depth.

**0019 PASS** — Headline Balanced facet per source. **CROSS-PACK (Career):** “rotation, consulting, cross-functional work” — career examples embedded in advantage; Strength-valid but Career-tagged.

**0020 REVIEW** — Deputy/integrator overlaps MEAN “range” and CAR integrator roles. Medium explainability.

**0021 REVIEW** — “Healthier than glory-under-fire” overlaps Balanced CHAL/HEALTH themes. Support facet.

---

## Weak (`ADV-0022` – `ADV-0028`)

| ID | Title | PC | EV | DP | DR | CV | AC | RD | EX | ST | Avg | Verdict |
|----|-------|---:|---:|---:|---:|---:|---:|---:|---:|---:|----:|---------|
| 0022 | decision making | 10 | 8 | 9 | 8 | 9 | 9 | 10 | 8 | 10 | 8.9 | **PASS** |
| 0023 | leadership | 10 | 8 | 8 | 8 | 9 | 8 | 10 | 8 | 10 | 8.8 | **PASS** |
| 0024 | learning | 10 | 8 | 9 | 7 | 9 | 8 | 10 | 8 | 10 | 8.8 | **PASS** |
| 0025 | discipline | 10 | 8 | 9 | 9 | 8 | 7 | 9 | 7 | 10 | 8.4 | **REVIEW** |
| 0026 | adaptability | 10 | 8 | 8 | 7 | 9 | 8 | 10 | 8 | 10 | 8.7 | **PASS** |
| 0027 | responsibility | 10 | 8 | 9 | 8 | 8 | 7 | 9 | 7 | 9 | 8.4 | **REVIEW** |
| 0028 | stress tolerance | 10 | 8 | 9 | 8 | 9 | 8 | 10 | 9 | 10 | 8.9 | **PASS** |

**0022 PASS** — Actionable framing (“clear brief, constraints, trusted counterpart”). Reframes Weak judgment without dominance theatre.

**0023 PASS** — “Room livable / truth-telling” — distinct leadership advantage; mild PERS overlap acceptable.

**0024 PASS** — “How your tank fills” ties to Strength fuel metaphor; links MEAN but adds learning method.

**0025 REVIEW** — Selective craft depth overlaps MEAN/CAR specialist themes. Optional.

**0026 PASS** — Professional radar — actionable sensitivity; overlaps PERS “read atmosphere” but advantage-framed.

**0027 REVIEW** — Lists domains (operations, care, research) — mild **Career** bleed. **LOW EXPLAINABILITY** vs 0022–0024.

**0028 PASS** — Early warning is high-value, distinct Weak asset; limitation blocks “unbreakable stress tolerance” misuse.

---

## Very Weak (`ADV-0029` – `ADV-0035`)

| ID | Title | PC | EV | DP | DR | CV | AC | RD | EX | ST | Avg | Verdict |
|----|-------|---:|---:|---:|---:|---:|---:|---:|---:|---:|----:|---------|
| 0029 | decision making | 10 | 8 | 9 | 8 | 9 | 8 | 9 | 8 | 9 | 8.7 | **PASS** |
| 0030 | leadership | 10 | 8 | 8 | 8 | 9 | 8 | 9 | 8 | 8 | 8.6 | **REVIEW** |
| 0031 | learning | 10 | 8 | 9 | 9 | 8 | 7 | 9 | 7 | 10 | 8.7 | **REVIEW** |
| 0032 | discipline | 10 | 8 | 9 | 8 | 9 | 9 | 10 | 9 | 10 | 9.0 | **PASS** |
| 0033 | adaptability | 10 | 8 | 9 | 7 | 9 | 9 | 10 | 9 | 10 | 8.9 | **PASS** |
| 0034 | responsibility | 10 | 8 | 9 | 9 | 8 | 7 | 9 | 7 | 10 | 8.4 | **REVIEW** |
| 0035 | stress tolerance | 10 | 8 | 9 | 8 | 9 | 8 | 10 | 9 | 10 | 8.9 | **PASS** |

**0029 PASS** — “Precision in a held space” — actionable boundary; aligns with Very Weak MEAN without repeating it.

**0030 REVIEW** — **CROSS-PACK (Career):** “counsel, specialist, editor” are role/niche labels — Career-adjacent. Domain purity: leadership advantage with career nouns. Overlaps CAR Very Weak counsel.

**0031 REVIEW** — **LOW EXPLAINABILITY** if 0032/0033 kept. Environment requirement overlaps MEAN protection theme.

**0032 PASS** — Conservation discipline is core Very Weak usable capacity; overlaps REC “say no” but advantage-owned.

**0033 PASS** — “Change environment not inflate yourself” — high actionability; distinct from MEAN costume warning.

**0034 REVIEW** — Trust in delicate work — generic virtue unless paired with niche context. Low priority facet.

**0035 PASS** — “True energy budget” — commercially strong; organizational framing is Strength-valid.

---

# 4. FAIL units

None.

No unit fails professional doctrine, leaks Rule IDs/scores, requires unpublished Pattern/UG/Ten Gods/Luck, or mislabels a class.

---

# 5. Summary

| Metric | Value |
|--------|------:|
| **Total reviewed** | **35** |
| **PASS** | **16** |
| **REVIEW** | **19** |
| **FAIL** | **0** |

## Average scores

| Criterion | Average |
|-----------|--------:|
| Professional correctness | 9.9 |
| Evidence compatibility | 8.0 |
| Domain purity | 8.7 |
| Duplicate risk | 8.0 |
| Customer value | 8.5 |
| Actionability | 7.7 |
| Readability | 9.4 |
| Explainability | 7.6 |
| Strength-only validity | 9.7 |
| **Overall average** | **8.6 / 10** |

## PASS units (16)

`ADV-0001`, `0002`, `0009`, `0013`, `0015`, `0016`, `0019`, `0022`, `0023`, `0024`, `0026`, `0028`, `0029`, `0032`, `0033`, `0035`

## REVIEW units (19)

`ADV-0003`, `0004`, `0005`, `0006`, `0007`, `0008`, `0010`, `0011`, `0012`, `0014`, `0017`, `0018`, `0020`, `0021`, `0025`, `0027`, `0030`, `0031`, `0034`

---

# 6. Cross-phase duplicate candidates

| ADV unit | Overlaps | Notes |
|----------|----------|-------|
| `ADV-0008` | `MEAN-0006` | Decided decisions / inner weight |
| `ADV-0009` | `MEAN-0006`, `PERS-strong` | Battery / staying power |
| `ADV-0013`, `ADV-0006` | `CHAL-* carry load`, `CAR-strong employment` | `DUP-STR-CARRY_LOAD` |
| `ADV-0014` | `MEAN-0006` | `DUP-STR-FULL_TANK`; golden rejects 0014 if MEAN rep kept |
| `ADV-0015` | `MEAN-0010` | Multiple viable paths / range |
| `ADV-0019` | `MEAN-0010`, `CAR-balanced` | Adaptability headline |
| `ADV-0024` | `MEAN-0013` | Tank fills via people |
| `ADV-0026` | `PERS-weak` | Atmosphere radar |
| `ADV-0028` | `CHAL-weak`, `HEA-weak` | Early warning / overload |
| `ADV-0032` | `REC-very_weak do` | Conservation / say no |
| `ADV-0007`, `0014` | `CHAL-* stress` | Advantage vs cost boundary |

Clusters were **not** modified per instructions.

---

# 7. Cross-pack dependency candidates

| ID | Dependency | Severity |
|----|------------|----------|
| `ADV-0010` | **Career** — apprenticeship, roles | Soft (examples in learning claim) |
| `ADV-0019` | **Career** — rotation, consulting, cross-functional | Soft (headline adaptability) |
| `ADV-0003` | **Career** — craft, sport, exam paths | Soft |
| `ADV-0030` | **Career** — counsel, specialist niche | Soft |
| `ADV-0027` | **Career** — operations, care, research domains | Soft |

No unit requires Pattern, Useful God, Ten Gods, Luck, Marriage, or ShenSha at runtime.

All cross-pack flags are **embedded examples**, not hard dependencies — Strength-only validity remains high (avg 9.7).

---

# 8. Explainability risks (LOW EXPLAINABILITY units)

Units where removal often loses little if another facet or MEANING already selected:

| ID | Why LOW |
|----|---------|
| `ADV-0005` | VS adaptability explicitly not headline |
| `ADV-0012` | Strong adaptability = optional sprint detail |
| `ADV-0017` | Balanced learning = adequate, not decisive |
| `ADV-0031` | Very Weak learning = environment-dependent detail |
| `ADV-0020`, `0025`, `0027`, `0034` | Responsibility/discipline facets = support tier |
| `ADV-0008`, `0011`, `0018`, `0021` | Removable when CORE MEANING + 1–2 headline facets kept |

Composer should enforce source §8: **3–5 facets max**, not seven.

---

# 9. Commercial risks

1. **Printing all seven facets** — violates source composition rule; dilutes pay-worthiness.
2. **`DUP-STR-CARRY_LOAD` double-select** — `ADV-0006` + `ADV-0013` or ADV + CAR employment.
3. **`DUP-STR-FULL_TANK` double-select** — `ADV-0014` + `MEAN-0006` duplicates full-tank story.
4. **Class-only gate** — advantages without published causes may read as generic praise (violates source §1).
5. **Weak stress mispairing** — praising unbreakable tolerance (source ban); `ADV-0028` limitation guards this.
6. **Very Strong flexibility oversell** — `ADV-0005` must not print as effortless adaptability.

---

# 10. Recommendations (QA only — no rewrites)

1. **Selection policy:** Max 3–5 advantage facets per class; prefer PASS units aligned with golden CASE-0001 pattern (`ADV-0013` + `ADV-0009` for Strong).

2. **Evidence gate (Reasoning):** Before selecting any ADV unit, require at least one published strengthen cause (season/root/support) when advantage implies capacity from feed — enforce limitation text externally.

3. **Duplicate enforcement:** Never co-select `ADV-0014` with `MEAN-0006`; never co-select `ADV-0006` with `ADV-0013`.

4. **Optional facets:** Default omit `ADV-0012`, `0005`, `0017`, `0031`, `0034` unless domain requested or budget allows.

5. **Career-tagged units:** When Career section omitted (`OMITTED_DOMAIN`), trim career example clauses from `ADV-0010`, `0019`, `0030` at compose time — or skip those units.

6. **Phase 4 prep (CHALLENGES):** Pair `ADV-0006/0013` with CHAL carry-load; pair `ADV-0007/0014` with CHAL stress cost.

7. **Keep PASS units stable** for Validated review — especially golden-aligned `ADV-0009`, `ADV-0013`.

---

# 11. Phase 3 gate

| Gate | Result |
|------|--------|
| All 35 ADVANTAGES units reviewed | Yes |
| Any FAIL | No |
| Phase 3 ADVANTAGES QA | **Complete — proceed to Phase 4 (CHALLENGES) when requested** |
| Catalog promotion to Validated | **Not authorized** — 19 REVIEW units; systemic cause-gate gap |

---

END
