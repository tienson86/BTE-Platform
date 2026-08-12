# Phase 02 — CAUSES Review

| Field | Value |
|-------|-------|
| Document | PHASE_02_CAUSES_REVIEW |
| Pack | PACK_01_STRENGTH |
| Topic | causes |
| Phase | 2 — CAUSES only |
| Units reviewed | 25 |
| Source | `knowledge/interpretation_knowledge/PACK_01_STRENGTH/02_CAUSES.md` |
| Catalog | `knowledge/knowledge_catalog/PACK_01_STRENGTH/catalog/causes/` |
| Date | 2026-08-12 |
| Role | Knowledge QA — no knowledge rewritten |

---

# 1. QA process (deterministic)

Review order: by `knowledge_id` ascending (`IK-STR-CAUS-0001` … `IK-STR-CAUS-0025`).

Each unit scored **0–10** on six criteria:

| # | Criterion | What was checked |
|---|-----------|------------------|
| 1 | Professional correctness | Faithful to source §2–§11; WHY not MEANING; no algorithm/score/rule leakage |
| 2 | Evidence support | `required_facts`, `forbidden_conditions`, `required_evidence` match runtime contract |
| 3 | Duplicate risk | Overlap with other cause units; cross-phase MEANING/CHAL/EDGE bleed |
| 4 | Customer value | Pay-worthiness when selected under budget |
| 5 | Readability | Claim clarity; supporting points stay on one cause |
| 6 | Commercial quality | Consultant weather language; safe So what |

**CAUSES-specific checks (each unit):**

| Check | Question |
|-------|----------|
| A | Is this truly a CAUSE, not MEANING or algorithm? |
| B | Does it explain WHY without recalculating Strength? |
| C | Does it require facts actually exposed by runtime? |
| D | Does it misuse absence of evidence as evidence? |
| E | Does it overlap another cause unit? |
| F | Does it leak scoring / rule logic into customer knowledge? |
| G | Suitable for Customer Mode, Validation Mode, or both? |

Overall verdict:

- **PASS** — ready for Validated review; no blocking defect
- **REVIEW** — usable but governance or evidence gate needs fix before Validated
- **FAIL** — blocking defect; do not promote

No catalog status, schema, or duplicate clusters were modified.

---

# 2. Unit reviews

## IK-STR-CAUS-0001 — A cause is how the chart feeds, holds, empties, or presses

| Criterion | Score |
|-----------|------:|
| Professional correctness | 9 |
| Evidence support | 10 |
| Duplicate risk | 8 |
| Customer value | 8 |
| Readability | 9 |
| Commercial quality | 9 |
| **Average** | **8.8** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | ✓ | ✓ | △ | ✓ | Both — with composer guard |

**Overall: REVIEW**

What is missing:

- Meta-frame from source §2 is correct, but supporting_points list all six structures — if printed verbatim in Customer Why, it becomes a glossary dump despite limitations.
- Overlaps individual cause units (0002–0019) and class clusters (0020–0024); Composer must select present causes only, not this taxonomy intro plus each cause.
- Borderline MEANING phrase (“class is not a mood”) — acceptable because sourced from §2 cause definition, not lived identity.

Not FAIL: limitations explicitly forbid glossary dump and inventing unpublished causes.

---

## IK-STR-CAUS-0002 — Season agrees — natal climate already on your side

| Criterion | Score |
|-----------|------:|
| Professional correctness | 10 |
| Evidence support | 7 |
| Duplicate risk | 9 |
| Customer value | 10 |
| Readability | 10 |
| Commercial quality | 10 |
| **Average** | **9.3** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | △ | ✓ | △ | ✓ | Both |

**Overall: REVIEW**

What is missing:

- **Runtime evidence risk:** `0002` and `0003` share `required_facts: classification, season` with no polarity key. Runtime must infer feeding vs hostile from published season evidence — not encoded in catalog gate.
- `optional_facts: special` and merge instruction align with golden `MERGED_CAUSE_SPECIAL_INTO_SEASON` — good, but merge behavior is limitation text only.
- Overlaps `0004` (natal vs luck) if both selected.

Not FAIL: claim is source-faithful; CASE-0001 golden uses this family.

---

## IK-STR-CAUS-0003 — Season disagrees — same effort costs more

| Criterion | Score |
|-----------|------:|
| Professional correctness | 10 |
| Evidence support | 7 |
| Duplicate risk | 9 |
| Customer value | 10 |
| Readability | 10 |
| Commercial quality | 10 |
| **Average** | **9.3** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | △ | ✓ | △ | ✓ | Both |

**Overall: REVIEW**

What is missing:

- Same **season polarity gate** gap as 0002 — mutual exclusivity is not in schema.
- Limitation correctly blocks use when season unpublished (`REJECTED_MISSING_EVIDENCE`).

Not FAIL.

---

## IK-STR-CAUS-0004 — Season is natal climate, not decade luck

| Criterion | Score |
|-----------|------:|
| Professional correctness | 10 |
| Evidence support | 9 |
| Duplicate risk | 7 |
| Customer value | 7 |
| Readability | 10 |
| Commercial quality | 8 |
| **Average** | **8.5** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | ✓ | ✓ | △ | ✓ | Both — prefer Validation / qualifier |

**Overall: REVIEW**

What is missing:

- Redundant with limitations already on 0002/0003; limitation itself says prefer as qualifier, not standalone headline.
- `customer_mode: ALLOWED` conflicts with own limitation when budget is tight.
- Low incremental value if 0002 already kept.

Not FAIL.

---

## IK-STR-CAUS-0005 — Root present — identity has a floor

| Criterion | Score |
|-----------|------:|
| Professional correctness | 10 |
| Evidence support | 10 |
| Duplicate risk | 9 |
| Customer value | 10 |
| Readability | 10 |
| Commercial quality | 10 |
| **Average** | **9.8** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Both |

**Overall: PASS**

Ready because claim matches source §4 “with root”, `forbidden_conditions: root_thin` correctly separates from 0007, and absent/published distinction is in limitations. True WHY; no score leakage.

---

## IK-STR-CAUS-0006 — Root absent — talent has nowhere to sit

| Criterion | Score |
|-----------|------:|
| Professional correctness | 10 |
| Evidence support | 10 |
| Duplicate risk | 9 |
| Customer value | 10 |
| Readability | 10 |
| Commercial quality | 10 |
| **Average** | **9.8** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Both |

**Overall: PASS**

Ready because limitation distinguishes published absent from unpublished (`REJECTED_MISSING_EVIDENCE`), and claim is distinct from thin root (0007). Professionally frames ground need without grit moralizing.

---

## IK-STR-CAUS-0007 — Thin root — the floor is close

| Criterion | Score |
|-----------|------:|
| Professional correctness | 10 |
| Evidence support | 10 |
| Duplicate risk | 9 |
| Customer value | 10 |
| Readability | 10 |
| Commercial quality | 10 |
| **Average** | **9.8** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Both |

**Overall: PASS**

Ready because `root_thin` fact key matches CASE-0001 golden (`CAUSE-ROOT-THIN`). Claim is atomic. Optional `drain` correctly defers combo story to 0009. Does not recalculate Strength.

---

## IK-STR-CAUS-0008 — Deep root plus surplus season — hard to empty

| Criterion | Score |
|-----------|------:|
| Professional correctness | 9 |
| Evidence support | 8 |
| Duplicate risk | 8 |
| Customer value | 8 |
| Readability | 9 |
| Commercial quality | 9 |
| **Average** | **8.5** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | △ | ✓ | △ | ✓ | Both |

**Overall: REVIEW**

What is missing:

- Requires `root_deep` + `season` — both must be **published** on runtime; many cases may only expose `root_thin` or generic `root`.
- Overlaps 0002 + 0005 composite picture without being a declared combo unit.
- Class gate `very_strong` is correct; limitation blocks use on Strong — good.

Not FAIL: professionally correct when facts exist.

---

## IK-STR-CAUS-0009 — Thin root plus drain — Weak floor story

| Criterion | Score |
|-----------|------:|
| Professional correctness | 10 |
| Evidence support | 10 |
| Duplicate risk | 9 |
| Customer value | 9 |
| Readability | 10 |
| Commercial quality | 10 |
| **Average** | **9.7** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | ✓ | ✓ | △ | ✓ | Both |

**Overall: PASS**

Ready because `forbidden_conditions: drain_inactive` aligns with frozen evidence policy (`INACTIVE` ≠ `MISSING`). Correctly fails on CASE-0001 where drain is inactive. Overlap with 0007 alone is acceptable — combo is distinct.

---

## IK-STR-CAUS-0010 — Support present — not the only one holding the line

| Criterion | Score |
|-----------|------:|
| Professional correctness | 10 |
| Evidence support | 10 |
| Duplicate risk | 8 |
| Customer value | 10 |
| Readability | 10 |
| Commercial quality | 10 |
| **Average** | **9.7** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | ✓ | ✓ | △ | ✓ | Both |

**Overall: PASS**

Ready because golden CASE-0001 keeps this (`CAUSE-SUPPORT`). Limitation requires `CONFLICT_QUALIFY` with control — matches C1 policy. True cause, not meaning.

---

## IK-STR-CAUS-0011 — Support absent — every task is a solo climb

| Criterion | Score |
|-----------|------:|
| Professional correctness | 10 |
| Evidence support | 10 |
| Duplicate risk | 9 |
| Customer value | 10 |
| Readability | 10 |
| Commercial quality | 10 |
| **Average** | **9.8** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Both |

**Overall: PASS**

Ready because polar opposite of 0010 is cleanly gated by published support polarity. Source §5 faithful. Does not treat missing publication as absent.

---

## IK-STR-CAUS-0012 — Support is chart backup, not a friend count

| Criterion | Score |
|-----------|------:|
| Professional correctness | 10 |
| Evidence support | 9 |
| Duplicate risk | 7 |
| Customer value | 6 |
| Readability | 9 |
| Commercial quality | 8 |
| **Average** | **8.2** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | ✓ | ✓ | △ | ✓ | Both — detail only |

**Overall: REVIEW**

What is missing:

- Clarifier unit; limitation says do not use as headline when 0010/0011 already kept — but `customer_mode: ALLOWED` without enforcement.
- Overlaps 0010/0011 socially.
- Better as Validation-side guardrail than Customer Why line.

Not FAIL.

---

## IK-STR-CAUS-0013 — Drain — productive while getting thinner

| Criterion | Score |
|-----------|------:|
| Professional correctness | 10 |
| Evidence support | 10 |
| Duplicate risk | 9 |
| Customer value | 10 |
| Readability | 10 |
| Commercial quality | 10 |
| **Average** | **9.8** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | ✓ | ✓ | △ | ✓ | Both |

**Overall: PASS**

Ready because `drain_inactive` forbidden condition matches evidence policy. Golden rejects on CASE-0001 (`REJECTED_FACT_INACTIVE`). Does not moralize kindness as cause. Overlap with 0014/0015 is class-specific variants — acceptable if severity gating works.

---

## IK-STR-CAUS-0014 — Mild drain on Strong — useful brake

| Criterion | Score |
|-----------|------:|
| Professional correctness | 9 |
| Evidence support | 8 |
| Duplicate risk | 7 |
| Customer value | 9 |
| Readability | 9 |
| Commercial quality | 9 |
| **Average** | **8.5** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | △ | ✓ | △ | ✓ | Both |

**Overall: REVIEW**

What is missing:

- **Severity not in facts:** “mild drain” is not a fact key; runtime must infer from drain magnitude or type not declared in catalog.
- If 0013 and 0014 both pass, Customer Why may double-print drain.
- Limitation says do not use heavy-drain story — good — but no mutual-exclusion field vs 0013.

Not FAIL: professionally correct for Strong when active drain is mild.

---

## IK-STR-CAUS-0015 — Heavy drain on Weak — exhaustion story

| Criterion | Score |
|-----------|------:|
| Professional correctness | 9 |
| Evidence support | 8 |
| Duplicate risk | 7 |
| Customer value | 9 |
| Readability | 9 |
| Commercial quality | 9 |
| **Average** | **8.5** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | △ | ✓ | △ | ✓ | Both |

**Overall: REVIEW**

What is missing:

- Same **mild/heavy severity gap** as 0014.
- Overlaps 0013 generic drain and Weak CHAL exhaustion stories (cross-phase).
- `drain_inactive` forbidden — good.

Not FAIL.

---

## IK-STR-CAUS-0016 — Control — pressure sitting on you

| Criterion | Score |
|-----------|------:|
| Professional correctness | 10 |
| Evidence support | 10 |
| Duplicate risk | 9 |
| Customer value | 10 |
| Readability | 10 |
| Commercial quality | 10 |
| **Average** | **9.8** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | ✓ | ✓ | △ | ✓ | Both |

**Overall: PASS**

Ready because golden CASE-0001 keeps control (`CAUSE-CONTROL`) and policy says never drop control. Base cause unit; 0017/0018 are surplus/deficit nuance layers. No rule leakage.

---

## IK-STR-CAUS-0017 — Control on surplus — missing steering wheel

| Criterion | Score |
|-----------|------:|
| Professional correctness | 9 |
| Evidence support | 8 |
| Duplicate risk | 7 |
| Customer value | 9 |
| Readability | 9 |
| Commercial quality | 9 |
| **Average** | **8.5** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | △ | ✓ | △ | ✓ | Both |

**Overall: REVIEW**

What is missing:

- `strength_class: all` but surplus use restricted to **limitation text** only (strong / very_strong) — not in `forbidden_conditions`.
- Can pass gate alongside 0016 and double-print control unless Composer dedupes.
- “Surplus” is classification-derived, not a separate fact — acceptable if runtime uses class, but gate is loose.

Not FAIL.

---

## IK-STR-CAUS-0018 — Control on deficit — a tighter grip is not fuel

| Criterion | Score |
|-----------|------:|
| Professional correctness | 9 |
| Evidence support | 8 |
| Duplicate risk | 7 |
| Customer value | 10 |
| Readability | 9 |
| Commercial quality | 9 |
| **Average** | **8.7** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | △ | ✓ | △ | ✓ | Both |

**Overall: REVIEW**

What is missing:

- Same layering issue as 0017 vs 0016.
- Advice clause (“do not tell Weak more discipline will create fuel”) is cause-adjacent steering — borderline REC, but sourced from §7.
- Class gate in limitation only (weak / very_weak).

Not FAIL: commercially important safety line.

---

## IK-STR-CAUS-0019 — Combination, clash, void — a piece will not sit still

| Criterion | Score |
|-----------|------:|
| Professional correctness | 10 |
| Evidence support | 10 |
| Duplicate risk | 9 |
| Customer value | 9 |
| Readability | 10 |
| Commercial quality | 9 |
| **Average** | **9.7** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ✓ | ✓ | ✓ | ✓ | △ | ✓ | Both |

**Overall: PASS**

Ready because requires `combination` published; limitation blocks when not published. Golden rejects on CASE-0001 (combination 0). Not a Pattern lecture. Overlaps EDGE units later — expected.

---

## IK-STR-CAUS-0020 — Very Strong cluster — fuel, floor, and backup at once

| Criterion | Score |
|-----------|------:|
| Professional correctness | 8 |
| Evidence support | 6 |
| Duplicate risk | 7 |
| Customer value | 8 |
| Readability | 9 |
| Commercial quality | 8 |
| **Average** | **7.7** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| △ | ✓ | ✗ | △ | △ | ✓ | Both — high invent risk |

**Overall: REVIEW**

What is missing:

- **Evidence gate mismatch:** `CLASS_ONLY` but claim enumerates season, root, support, drain, control — composite class picture from source §9.
- Limitations say do not invent unpublished causes — but unit can **pass gate without any cause facts** and still narrate a multi-cause story in Customer Why.
- Overlaps 0002–0018 if those are also selected — summary vs atomic causes.
- Borderline MEANING (“excess, not competence”) though sourced as class cluster So what.

Not FAIL: limitations explicitly warn; defect is gate strength, not wrong doctrine.

---

## IK-STR-CAUS-0021 — Strong cluster — can carry load, still has weather

| Criterion | Score |
|-----------|------:|
| Professional correctness | 8 |
| Evidence support | 6 |
| Duplicate risk | 6 |
| Customer value | 8 |
| Readability | 9 |
| Commercial quality | 8 |
| **Average** | **7.5** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| △ | ✓ | ✗ | △ | △ | ✓ | Both — risky default |

**Overall: REVIEW**

What is missing:

- **Highest runtime risk in Phase 2:** Claim includes “Drain exists but does not win” under `CLASS_ONLY`. On CASE-0001 drain is **INACTIVE** — limitation says do not narrate drain if inactive, but gate does not enforce → Composer could leak drain language if cluster unit is selected instead of atomic causes.
- Cross-phase duplicate with `IK-STR-MEAN-0006` (“can carry load”, “not a machine”).
- Overlaps atomic season/root/support units when those are already in Why.

Not FAIL: golden plan uses atomic causes, not this cluster — cluster should stay Validation or post-atomic summary only.

---

## IK-STR-CAUS-0022 — Balanced cluster — feed and empty are both real

| Criterion | Score |
|-----------|------:|
| Professional correctness | 8 |
| Evidence support | 7 |
| Duplicate risk | 7 |
| Customer value | 8 |
| Readability | 9 |
| Commercial quality | 8 |
| **Average** | **7.8** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| △ | ✓ | △ | ✓ | △ | ✓ | Both |

**Overall: REVIEW**

What is missing:

- `CLASS_ONLY` composite; “feed and empty” not tied to published season/drain/control facts.
- Cross-phase overlap with `IK-STR-MEAN-0010` (range, choosing vs waiting).
- True as consulting picture (§9) but weak as selectable Customer Why unit without atomic backing.

Not FAIL.

---

## IK-STR-CAUS-0023 — Weak cluster — spend more than it holds

| Criterion | Score |
|-----------|------:|
| Professional correctness | 8 |
| Evidence support | 6 |
| Duplicate risk | 7 |
| Customer value | 8 |
| Readability | 9 |
| Commercial quality | 8 |
| **Average** | **7.7** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| △ | ✓ | ✗ | ✓ | △ | ✓ | Both |

**Overall: REVIEW**

What is missing:

- Claim names drain, control, hostile season, root, support without requiring any — same CLASS_ONLY composite gap as 0020–0021.
- Cross-phase overlap with `IK-STR-MEAN-0013` (environment pays difference).
- Limitation “narrate only published members” is Composer duty, not schema enforcement.

Not FAIL.

---

## IK-STR-CAUS-0024 — Very Weak cluster — fuel architecture that needs protection

| Criterion | Score |
|-----------|------:|
| Professional correctness | 8 |
| Evidence support | 6 |
| Duplicate risk | 7 |
| Customer value | 8 |
| Readability | 9 |
| Commercial quality | 8 |
| **Average** | **7.7** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| △ | ✓ | ✗ | ✓ | △ | ✓ | Both |

**Overall: REVIEW**

What is missing:

- Composite CLASS_ONLY picture; lists thin floor, against climate, scarce backup, heavy output without fact keys.
- Cross-phase overlap with `IK-STR-MEAN-0016` (design constraint, protection, structure).
- Professionally sourced from §9 but should not compete with atomic causes in Customer Why.

Not FAIL.

---

## IK-STR-CAUS-0025 — Customer Why — only present weather

| Criterion | Score |
|-----------|------:|
| Professional correctness | 10 |
| Evidence support | 10 |
| Duplicate risk | 10 |
| Customer value | 8 |
| Readability | 10 |
| Commercial quality | 10 |
| **Average** | **9.7** |

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| N/A (governance) | ✓ | ✓ | ✓ | ✓ | ✓ | **Validation only** |

**Overall: PASS**

Ready because `customer_mode: FORBIDDEN` correctly implements source §11 composition rule. Not a customer claim. Prevents inventing causes from absence. `DEFERRED_TO_VALIDATION` in reason_codes is appropriate.

---

# 3. Summary

| Metric | Value |
|--------|------:|
| **Total reviewed** | **25** |
| **PASS** | **10** |
| **REVIEW** | **15** |
| **FAIL** | **0** |

## Average scores

| Criterion | Average |
|-----------|--------:|
| Professional correctness | 9.4 |
| Evidence support | 8.8 |
| Duplicate risk | 8.2 |
| Customer value | 8.9 |
| Readability | 9.6 |
| Commercial quality | 8.8 |
| **Overall average** | **8.8 / 10** |

## PASS units

`IK-STR-CAUS-0005`, `0006`, `0007`, `0009`, `0010`, `0011`, `0013`, `0016`, `0019`, `0025`

## REVIEW units

`IK-STR-CAUS-0001`, `0002`, `0003`, `0004`, `0008`, `0012`, `0014`, `0015`, `0017`, `0018`, `0020`, `0021`, `0022`, `0023`, `0024`

## FAIL units

None.

---

# 4. Cross-phase duplicate candidates

| Cause unit | Overlaps with | Risk |
|------------|---------------|------|
| `CAUS-0001` | `MEAN-0001` (standing not grade / not mood) | Taxonomy vs identity frame |
| `CAUS-0021` | `MEAN-0006` (carry load, not a machine) | Why vs meaning double-print |
| `CAUS-0022` | `MEAN-0010` (range, choosing) | Cluster summary vs lived meaning |
| `CAUS-0023` | `MEAN-0013` (environment pays difference) | Weak cause picture vs winning move |
| `CAUS-0024` | `MEAN-0016` (protection, structure, fuel architecture) | Cluster vs identity meaning |
| `CAUS-0014` / `0015` | Future CHAL drain facets | Cause severity vs operating cost |
| `CAUS-0017` / `0018` | `CAUS-0016` + future CHAL control | Layered control narration |
| `CAUS-0019` | `EDGE-0004` special structure | Cause vs edge qualifier |

No duplicate clusters were modified. These are **candidates for Composer policy or future cluster declaration**, not FAIL defects.

---

# 5. Runtime evidence risks

| # | Risk | Affected units | Severity |
|---|------|----------------|----------|
| 1 | **Season polarity not encoded** — `season` fact alone cannot choose 0002 vs 0003 | 0002, 0003 | High |
| 2 | **Drain severity not encoded** — mild vs heavy not in fact keys | 0013, 0014, 0015 | High |
| 3 | **CLASS_ONLY class clusters narrate unpublished causes** — gate passes on classification only | 0020–0024 | **Critical** for 0021 on CASE-0001 (drain INACTIVE) |
| 4 | **`root_deep` may be MISSING** on charts that only publish `root_thin` | 0008 | Medium |
| 5 | **Surplus/deficit control layers** — 0017/0018 use class in limitations, not forbidden_conditions | 0016, 0017, 0018 | Medium |
| 6 | **`special` merge into season** — optional on 0002; merge is limitation/reason code, not unit field | 0002 | Low — golden handles via `MERGED_CAUSE_SPECIAL_INTO_SEASON` |
| 7 | **INACTIVE vs MISSING drain** — 0013/0009 handle correctly; cluster 0021 does not | 0013, 0009, 0021 | High if 0021 selected |
| 8 | **Support present/absent polarity** — same key `support` for 0010 vs 0011 | 0010, 0011 | Medium — same pattern as season |

Golden CASE-0001 Why uses **atomic** units: 0002 (+ special merge), 0007, 0010, 0016 — not class clusters. QA confirms atomic PASS units align with golden; cluster units are the main evidence risk.

---

# 6. Recommendations (QA only — no rewrites performed)

1. **Composer policy (immediate):** In Customer Mode Why, prefer atomic cause units (0002–0019) over class clusters (0020–0024). Golden plan already follows this; enforce in selection design.

2. **Before Validated:** Document runtime polarity rules for `season` and `support` (mutual exclusion of agree/disagree and present/absent pairs) — schema change not required if documented in Reasoning selection spec.

3. **Before Validated:** Document drain severity selection (when to keep 0013 vs 0014 vs 0015) based on published drain evidence — or accept 0013 as default and treat 0014/0015 as class-conditional nuance layers.

4. **Block 0021 on INACTIVE drain:** Even without catalog edit, Reasoning must not select 0021 for CASE-0001-style payloads where drain is INACTIVE — limitation text is insufficient without selection rule.

5. **Keep PASS atomic units stable:** 0005, 0006, 0007, 0009, 0010, 0011, 0013, 0016, 0019 are golden-aligned and evidence-safe.

6. **Phase 3 prep (CHALLENGES):** Cross-check 0014/0015 against CHAL drain units; cross-check 0017/0018 against CHAL control units.

7. **0025 remains Validation-only:** Do not flip `customer_mode` — correctly PASS as governance unit.

---

# 7. Phase 2 gate

| Gate | Result |
|------|--------|
| All 25 CAUSES units reviewed | Yes |
| Any FAIL | No |
| Phase 2 CAUSES QA | **Complete — proceed to Phase 3 (CHALLENGES) when requested** |
| Catalog promotion to Validated | **Not authorized** — 15 REVIEW units; class-cluster evidence gates need governance |

---

END
