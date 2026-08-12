# Knowledge Selection — PACK-01 Prototype

| Field | Value |
|-------|-------|
| Document | KNOWLEDGE_SELECTION |
| Pack | PACK-01 Prototype |
| Version | 1.0.0 |

---

# 1. Purpose

Show **how** knowledge units are selected.

The prototype does not hard-code “CASE-0001 is Strong so paste paragraph X”.

It applies predicates to published facts.

---

# 2. Unit source

Units live in:

`knowledge/interpretation_knowledge/PACK_01_STRENGTH/`

IDs follow `KNOWLEDGE_INDEX.md`:

```text
IK-STR-<TOPIC>-<CLASS>-<NN>
```

This prototype binds those IDs to file sections. It does not rewrite the knowledge pack.

---

# 3. Selection algorithm (logical)

```text
candidates = all IK-STR units
kept = []

for unit in candidates:
    if unit.class not in {mapped_class, ALL, EDGE}:
        reject(WRONG_CLASS)
        continue
    if unit.topic == luck and luck_interaction is missing:
        reject(MISSING_LUCK)
        continue
    if unit.use_when names a cause dimension that is not present:
        reject(CAUSE_ABSENT)
        continue
    if unit.do_not_use_when matches a present fact:
        reject(PREDICATE_BLOCK)
        continue
    if unit.topic == meaning and unit.class != mapped_class:
        reject(WRONG_CLASS)  # never load neighbor meaning as primary
        continue
    keep(unit)

then apply PRIORITY, CONFLICT, DUPLICATE stages
```

Rejection is first-class. Every rejected unit is listed with a reason in Mode A metadata (not in Mode B).

---

# 4. `use_when` catalog (Strength prototype)

| Predicate | True when |
|-----------|-----------|
| `class_strong` | mapped class = `strong` |
| `class_balanced` | mapped class = `balanced` |
| `class_weak` | mapped class = `weak` |
| `class_very_strong` | mapped class = `very_strong` |
| `class_very_weak` | mapped class = `very_weak` |
| `season_present` | season evidence status = present and polarity ≠ missing |
| `root_present` | root evidence present |
| `root_thin` | root present AND published root is single-branch / mild (e.g. Thông căn 1 chi) |
| `root_deep` | root present AND published as multiple branches / deep — CASE-0001 false |
| `support_present` | support evidence present and strengthen |
| `drain_present` | drain evidence present AND drain is not zero/null |
| `control_present` | control evidence present and weaken |
| `special_present` | special evidence present |
| `special_override` | special present AND engine treated it as level override |
| `luck_published` | luck×Day-Master interaction published |
| `conflict_support_vs_control` | both support-polarity and control-weaken present |
| `hidden_stems_missing` | hidden stems not exposed |

A unit may list several predicates (AND).

---

# 5. Topic gates

| Topic | Gate |
|-------|------|
| Meaning | class match only |
| Cause | class ALL or class match, AND named dimension present |
| Advantage / Challenge / Personality / Career / Wealth / Marriage / Health | class match |
| Luck | class match AND `luck_published` |
| Recommendation | class match; prefer units that `pairs_with` a kept challenge |
| Edge | EDGE class; predicate must match (conflict, thin root, missing luck, …) |
| Example vignettes (`13_EXAMPLES`) | **never selected into customer output** — teaching only |

---

# 6. Block assembly (after keep)

For Mode B, kept units are grouped into blocks:

```text
mapped class = strong
        ↓
Meaning Block      IK-STR-MEAN-ST-*
Cause Block        present-cause units only
Advantage Block    IK-STR-ADV-ST-* (priority subset)
Challenge Block    IK-STR-CHAL-ST-* (priority subset)
Personality Block  IK-STR-PERS-ST-*
Career Block       IK-STR-CAR-ST-*
Wealth Block       IK-STR-WEA-ST-*
Marriage Block     IK-STR-MAR-ST-*
Health Block       IK-STR-HEA-ST-*
Luck Block         only if luck_published else empty + insufficient
Recommendation Block  do/avoid paired with kept challenges
Edge Block         Mode A + optional Mode B qualifier only
```

Empty Luck Block → Insufficient Data shell, not a guessed decade.

---

# 7. Facet caps (anti-dump)

Do not emit every facet of a topic.

Prototype caps (Priority Model may drop further):

| Block | Max facets |
|-------|------------|
| Meaning | 2 (lived + one tendency) |
| Cause | all **present** dimensions (no absent ones) |
| Advantages | 3–5 |
| Challenges | 2–3 |
| Personality | 2–3 |
| Career / Wealth / Marriage / Health | 1–2 each |
| Recommendations | 3 do + 3 avoid max |
| Edge in Mode B | 0–1 qualifier |

---

# 8. What selection is not

- Not “if CASE-0001 then …”
- Not reading the customer’s job title
- Not using Pattern/Useful God to pick Strength units
- Not loading Weak meaning because an expert once said thiên nhược
- Not loading drain-cause units when drain is zero

---

END
