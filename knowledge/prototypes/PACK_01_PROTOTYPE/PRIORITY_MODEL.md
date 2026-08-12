# Priority Model — PACK-01 Prototype

| Field | Value |
|-------|-------|
| Document | PRIORITY_MODEL |
| Pack | PACK-01 Prototype |
| Version | 1.0.0 |

---

# 1. Purpose

When several eligible units compete for a capped slot, this model decides **keep order** and **drop order**.

It does not rank BaZi rules.

It does not rescore Strength.

---

# 2. Priority keys (highest first)

| Rank | Key | Meaning |
|------|-----|---------|
| P0 | Class match | Unit class = mapped class |
| P1 | Cause present | Cause units whose dimension is present beat generic ALL |
| P2 | Magnitude | Among present causes, stronger published polarity first in Why |
| P3 | Conflict relevance | If C1 live, keep a challenge/edge that names the cost of surplus-under-pressure |
| P4 | Pairing | Recommendation that `pairs_with` a kept challenge beats an unpaired generic |
| P5 | Information novelty | After duplicate scan, novel domain facet beats synonym |
| P6 | Facet cap | Drop remaining facets |

P0 is a gate more than a sort: wrong class never enters.

---

# 3. Why-section cause order

Fixed order among **present** causes (Interpretation Standard Rule Trace order, compressed for customer):

1. Special (only if present; as weather, not “override” unless it was)
2. Season
3. Root
4. Support
5. Drain (skip if inactive)
6. Control
7. Combination / clash / void (skip if inactive)

CASE-0001 Why order: special (Ấn in cold season) → season → root → support → control.

Drain skipped.

---

# 4. Advantage / challenge pick order (Strong)

When class = `strong` and caps apply:

**Advantages (keep 3–4):**

1. responsibility (load can be handed)
2. leadership as staying power
3. decision staying decided
4. discipline / long build

Drop first: adaptability-as-headline (not Strong’s gift). Drop stress-tolerance if Health will own downshift (duplicate family).

**Challenges (keep 2–3):**

1. endurance-as-proof (typical mistake)
2. receptivity / closed ear
3. becoming the battery (relational cost) if Marriage will not fully consume it

If control is present, prefer receptivity / pressure-related challenge over “you never meet friction”.

---

# 5. Recommendation pairing

| Kept challenge | Preferred rec |
|----------------|---------------|
| endurance-as-proof | do: invite one person who may revise the method; avoid: collecting difficulty as identity |
| closed ear | do: hear then revise; avoid: treating disagreement as optional commentary |
| family/org battery | do: rest on calendar; avoid: unpaid infrastructure as career |

Unpaired recs drop at P4 when the cap is full.

---

# 6. Executive Summary line priority

1. Standing
2. Compressed why (top 2 present causes + control if C1)
3. So what
4. One cost
5. One do
6. One avoid
7. Luck only if published
8. Close

Max 8 lines. If luck missing, skip 7.

---

# 7. Stability

Same facts → same keep/drop list.

Do not randomize facet order.

Do not prefer “more dramatic” units.

---

END
