# Relevance Policy — FROZEN V1.0

| Field | Value |
|-------|-------|
| Document | RELEVANCE_POLICY |
| Status | FROZEN |
| Form | Deterministic levels — no production formula |

---

# 1. What Relevance is

Relevance answers: **does this official unit belong to this chart’s conversation?**

It is not Strength Score.

It is not Salience.

It is not Rule Priority.

---

# 2. Frozen levels (assign exactly one)

| Level | Code | When | Why |
|-------|------|------|-----|
| Not relevant | `REL_0` | Gate FAIL | Must not rank |
| Cause-locked | `REL_1` | required cause facts AVAILABLE and polarity matches | This chart’s weather |
| Class-core | `REL_2` | `class_only` / meaning-challenge-advantage for matching class | About this standing, not a specific cause |
| Class-domain | `REL_3` | domain unit, class match, no extra cause required | Life area for this class |
| Generic | `REL_4` | `specificity = generic` | Weak lock to this chart |

Lower number = more relevant.

---

# 3. Assignment rules (deterministic)

1. If gate ≠ pass → `REL_0`.
2. Else if unit has a required cause fact (season, root, control, …) that is AVAILABLE → `REL_1`.
3. Else if purpose in {MEANING, ADVANTAGE, CHALLENGE, EDGE_QUALIFIER, WHY cluster} and class matches → `REL_2`.
4. Else if domain ≠ strength_core and class matches → `REL_3`.
5. Else → `REL_4`.

No weights. No floats. No ML.

---

# 4. Sort key (with other policies)

See [DETERMINISM.md](DETERMINISM.md). Relevance is key 2 after gate.

---

# 5. Future packs

Reuse the **same five levels**.

Replace only the fact keys in rule 2 (Pattern facts, Useful God facts, …).

Do not invent `REL_5` without freeze V1.1.

Do not use domain engine scores as relevance.

---

END
