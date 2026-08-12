# CASE-0001 Reasoning Walkthrough

| Field | Value |
|-------|-------|
| Document | CASE_0001_WALKTHROUGH |
| Pack | PACK-01 Strength Reasoning Engine |
| Status | DESIGN REVIEW FIXTURE |
| Input | Prototype-published Strength Facts only |

---

# 0. Scope

This walkthrough uses **only** Strength facts already published in the PACK-01 prototype (`EXAMPLE_CASE_0001.md` / calibration evidence).

It does **not** add biography, job, luck decades, Pattern, Useful God, Temperature, gender, or expert expected class.

It does **not** generate a report.

It shows:

```text
Candidates
  → Evidence Gate
    → Eligibility
      → Ranking
        → Duplicate removal
          → Conflict handling
            → Narrative budget
              → NarrativePlan
```

Numbers below (0.87, 72%, Balanced alternative, C1) are **prototype-published**, not new truths.

---

# 1. ReasoningInput (condensed)

```text
subject: strength
classification.class_id: strong
facts:
  season AVAILABLE support (Tướng)
  root AVAILABLE support thin (Thông căn 1 chi)
  support AVAILABLE support (Đồng hành)
  control AVAILABLE weaken (Quan Sát / Thất Sát)
  drain AVAILABLE inactive (0)
  special AVAILABLE support (Ấn mùa lạnh, not override)
  luck MISSING
  hidden_stems MISSING
confidence.interpretation_confidence: 72  band: high
alternative: primary strong, runner_up balanced
conflicts: C1 support-side vs control
question_context: general
```

---

# 2. Candidates (illustrative set)

From selector / knowledge families:

| ID | purpose | notes |
|----|---------|-------|
| IK-STR-MEAN-ST-01 | MEANING | class strong |
| IK-STR-MEAN-ST-03 | MEANING | endurance-as-proof tendency |
| IK-STR-MEAN-BA-* | MEANING | balanced class |
| IK-STR-MEAN-WK-* | MEANING | weak |
| IK-STR-CAUSE-SEASON-01 | WHY | |
| IK-STR-CAUSE-ROOT-THIN-01 | WHY | |
| IK-STR-CAUSE-ROOT-DEEP-01 | WHY | forbidden if thin |
| IK-STR-CAUSE-SUPPORT-01 | WHY | |
| IK-STR-CAUSE-CONTROL-01 | WHY | |
| IK-STR-CAUSE-SPECIAL-01 | WHY | |
| IK-STR-CAUSE-DRAIN-01 | WHY | needs drain active |
| IK-STR-CAUSE-CLASS-ST-01 | WHY | cluster |
| IK-STR-ADV-ST-* | ADVANTAGE | several facets |
| IK-STR-CHAL-ST-* | CHALLENGE | |
| IK-STR-CAR/WEA/MAR/HEA-ST-* | domains | |
| IK-STR-LUCK-ST-* | LUCK | |
| IK-STR-REC-ST-* | RECOMMENDATION | |
| IK-STR-EDGE-C1 | EDGE_QUALIFIER | |
| IK-STR-EX-* | — | teaching |

---

# 3. Evidence Gate

| Unit | State | Reason |
|------|-------|--------|
| MEAN-ST-01, ST-03 | eligible | class match |
| MEAN-BA-*, WK-* | ineligible | REJECTED_CLASS_MISMATCH |
| CAUSE-SEASON/SUPPORT/CONTROL/SPECIAL/ROOT-THIN | eligible | facts AVAILABLE |
| CAUSE-ROOT-DEEP | ineligible | REJECTED_FORBIDDEN_CONDITION (`root_thin`) |
| CAUSE-DRAIN | ineligible | REJECTED_MISSING_EVIDENCE / drain inactive |
| LUCK-* | ineligible | REJECTED_MISSING_EVIDENCE → INSUFFICIENT_DATA_LUCK for section |
| EX-* | ineligible | REJECTED_TEACHING_EXAMPLE |
| ADV/CHAL/CAR/… ST | eligible | class match; no extra required luck |

No `partially_supported` firm conclusions. Hidden stems MISSING does not fail season/root-thin units.

---

# 4. Eligibility set (after gate)

All `eligible` rows above except rejected class/drain/deep-root/luck/examples.

---

# 5. Ranking (relevance then salience)

High salience (this chart’s weather):

- WHY control + season + root-thin (C1 + specificity)
- MEANING ST-01 / ST-03
- CHALLENGE endurance-as-proof, receptivity
- REC paired to those challenges
- EDGE-C1 qualifier

Lower salience:

- ADV adaptability (generic, not Strong headline)
- extra career facets beyond load + employment condition
- learning/leadership extras

Relevance is high for all class-matching present-cause units.

Salience distinguishes **thin-root + control** from **generic persist**.

Strength score 0.87 is **not** used as relevance.

---

# 6. Duplicate removal

| Drop / merge | Kind |
|--------------|------|
| ADV stress_tolerance vs MEAN full-tank vs HEA downshift | semantic_overlap — keep MEAN + HEA domain specialization; drop ADV stress_tolerance |
| Career “persist” vs Meaning | same_implication — rewrite career to *where load sits* or drop |
| Multiple “you can carry” advantages | keep responsibility + staying-power leadership; drop clones |

Representative: more specific, cause-aware, higher customer_value.

---

# 7. Conflict handling

**C1 FACT_CONFLICT:** support-side vs control.

Action: `qualify` — Why keeps both polarities. Primary class unchanged.

**Nuance:** Strong / decisive staying vs closed ear under Quan Sát = CONDITIONAL NUANCE, not TRUE CONTRADICTION. Keep both with context.

**Alternative:** Balanced 28% → Validation only. Customer: EDGE qualifier, `language_strength = qualified`. Do not load MEAN-BA.

**Advice:** no quit-job / must-invest.

---

# 8. Narrative budget (Customer Mode kept)

| Slot | Kept (design) |
|------|----------------|
| Conclusion | 1 (classification) |
| Why | 4: special, season, root-thin, support+control compressed to stay ≤4 — **must include control**. Prototype order: special, season, root-thin, support, control is 5 causes → compress support+special as “feed” if needed, **never drop control**. Preferred keep: season, root-thin, support, control (4). Special folds into season/feed (Ấn in cold season) as qualifier on season unit, traced as two ids merged in Why. |
| Meaning | 2: ST-01, ST-03 |
| Advantages | 3: responsibility, leadership staying power, decision |
| Challenges | 3: endurance-as-proof, receptivity, battery |
| Career | 2: load family, employment+recovery condition |
| Wealth | 1: earn-by-carrying |
| Marriage | 1: love-by-carrying |
| Health | 1: scheduled downshift |
| Luck | 0 units; insufficient shell |
| Recs | 4: rest calendar, invite reviser, avoid difficulty-identity, avoid hear-without-revise |
| Edge | 1 qualifier |
| Personality | 1–2 if budget; else omit as secondary |

Omitted: luck content, drain, deep-root, Weak/Balanced meaning, examples, adaptability ADV.

---

# 9. NarrativePlan (review shape)

```text
primary_conclusion: strong, language_strength=qualified

sections:
  CONCLUSION     NAME_STANDING
  WHY            EXPLAIN_CAUSES     transition NAME_TO_CAUSE
  MEANING        STATE_MEANING      CAUSE_TO_IMPLICATION
  ADVANTAGE      LIST_ADVANTAGES    IMPLICATION_TO_CAPACITY
  CHALLENGE      LIST_CHALLENGES    CAPACITY_TO_COST
  CAREER/WEALTH/MARRIAGE/HEALTH     DOMAIN_IMPLICATION
  LUCK           LUCK_INSUFFICIENT  DOMAIN_TO_LUCK
  RECOMMENDATION ADVISE             IMPLICATION_TO_ACTION
  SUMMARY        SUMMARIZE

warnings: caution on closed-ear / battery — not doom

omitted_domains: luck content; maybe learning/leadership

missing_data: luck_interaction, hidden_stems

alternative: Validation Strong/Balanced shares; customer qualifier only

executive_summary_plan: 7 claims
  conclusion, feed+control, capacity, endurance-as-proof,
  recovery condition, rec rest+reviser, close (strong ≠ no brake)

diagnostics: full candidate/reject/rank/trace
```

Reasoning chain:

```text
FACT: season, root_thin, support, special, control
INTERPRETATION: Strong with feed and sitting pressure
IMPLICATION: can carry; endurance mistaken for correctness
ACTION: rest; one reviser; do not collect difficulty as identity
```

Luck chain: not built.

---

# 10. Selected vs rejected (required list)

**Selected meaning:** IK-STR-MEAN-ST-01, IK-STR-MEAN-ST-03

**Selected cause:** season, root-thin, support, control; special merged/qualified onto feed

**Selected practical:** ADV responsibility/leadership/decision; CHAL endurance/receptivity/battery; CAR load+recovery; WEA carrying; MAR carrying-love; HEA downshift; REC four paired; EDGE-C1

**Rejected deep-root:** REJECTED_FORBIDDEN_CONDITION

**Rejected drain:** REJECTED_MISSING_EVIDENCE (inactive)

**Rejected luck units:** REJECTED_MISSING_EVIDENCE; section INSUFFICIENT_DATA_LUCK

**Rejected Weak/Balanced meaning:** REJECTED_CLASS_MISMATCH / REJECTED_ALTERNATIVE_CLASS_AS_PRIMARY

**Conflict:** qualify C1; nuance on receptivity vs decisiveness

**Alternative:** Validation Mode; customer qualified language only

---

# 11. What this walkthrough is for

Reviewers decide whether this reasoning model is good enough as the **production standard**.

Not for implementing `reasoning_engine.py` in this task.

---

END
