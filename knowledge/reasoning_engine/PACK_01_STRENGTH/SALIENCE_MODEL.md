# Salience Model

| Field | Value |
|-------|-------|
| Document | SALIENCE_MODEL |
| Version | 1.0.0 |

---

# 1. Purpose

Salience answers: **what is most worth saying?**

Relevance = belongs here.

Salience = deserves emphasis / early position / budget slot.

---

# 2. Factors

| Factor | Question |
|--------|----------|
| Evidence strength | How well is this claim grounded in present facts? |
| Specificity | Is it this chart’s weather, or any Strong person? |
| Life impact | Does it change how the person operates? |
| Risk severity | Is there an operating cost that can harm if ignored? |
| Customer usefulness | Can they do something with it? |
| Uniqueness | Would dropping it lose a distinct idea? |
| Actionability | Does it connect to a later recommendation? |

---

# 3. Contrast

| | Relevant | Salient |
|--|----------|---------|
| “Strong people can persist” | often | rarely (generic) |
| “Thin root + control: force with a hand on the neck” | yes if facts match | high |
| “Luck overdrive” | no if luck MISSING | n/a (ineligible) |
| Extra career facet #4 | yes | low once budget filled |

---

# 4. Required vs salient

Some units are **required shells** (Conclusion) even if salience of extra meaning units is low.

Salience never deletes Conclusion.

Salience decides which Why causes lead, which domain implications survive the budget, and whether a WARNING is emitted.

---

# 5. Warnings

A unit with `severity = warning` and high salience may add `warnings[]` on the NarrativePlan **and** a Customer Mode caution only if Advice Safety allows (no doom, no absolute).

Control present on Strong → caution about closed ear / over-push is salient; “you will be destroyed by Thất Sát” is not allowed.

---

END
