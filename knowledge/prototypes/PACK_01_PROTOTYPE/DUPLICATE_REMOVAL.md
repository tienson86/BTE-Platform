# Duplicate Removal — PACK-01 Prototype

| Field | Value |
|-------|-------|
| Document | DUPLICATE_REMOVAL |
| Pack | PACK-01 Prototype |
| Version | 1.0.0 |

---

# 1. Purpose

Each paragraph must add **new information**.

This stage enforces the Interpretation Knowledge Value Framework inside the composer.

---

# 2. What counts as a duplicate

Two units are duplicates if a reviewer can swap them between sections without losing a decision-relevant idea.

Typical Strength collisions:

| Keep in | Drop or specialize |
|---------|-------------------|
| Meaning: “you start with a full tank” | Advantage: “you have stamina” (same idea) |
| Why: season + root + support | Meaning repeating those three causes |
| Advantage: staying power | Career: “you are strong at work” |
| Challenge: closed to correction | Recommendation avoid: “don’t be stubborn” (too close — specialize the avoid) |
| Personality: pillar | Career: backbone (same metaphor — keep only one metaphor) |

---

# 3. Algorithm (logical)

```text
for each kept unit in narrative order:
    claim = normalize(unit.so_what)
    if claim matches an earlier kept claim at synonym level:
        if later unit has a domain facet (career/wealth/marriage/health):
            rewrite_to_domain_question  OR  drop if rewrite would still be the same
        else:
            drop(DUPLICATE_OF unit_id)
```

Prototype synonym families (Strength):

- full tank / stamina / persist / carry load / backbone / pillar
- closed ear / not receptive / ignore feedback / stubborn
- rest / downshift / recovery / off-season

Only one member of a family may occupy Meaning.

Later sections may use the family **only** if they add a domain constraint (Career = where load sits; Health = scheduled downshift; Marriage = partner sees the tank).

---

# 4. Class name repetition

The class label may appear:

- once in Conclusion
- once in Executive Summary
- elsewhere only as a grammatical referent

Drop openings like “Because you are Strong…” in every section.

---

# 5. Why vs Meaning

Why owns causes.

Meaning owns lived consequence.

If a meaning unit restates “you have season and root”, drop that sentence; keep “you enter work already carrying force”.

---

# 6. Advantages vs Challenges

If challenge = “not” + advantage, drop the challenge and require a **cost of the same structure**.

Keep: “endurance becomes proof that the method is right”.

Drop: “you are not flexible” as the only challenge.

---

# 7. Recommendations vs earlier sections

Do must not paste Career.

Avoid must not paste Challenge verbatim.

Pair: Challenge “endurance as evidence” → Avoid “do not treat lasting as proof the method is correct”.

---

# 8. Output of this stage

A drop log for Mode A appendix:

```text
DROPPED IK-STR-ADV-ST-stress_tolerance
reason: DUPLICATE_OF IK-STR-MEAN-ST-01 (full-tank family)
kept_instead: IK-STR-HEA-ST-balance (domain: scheduled downshift)
```

Mode B never shows the log.

---

END
