# N-IMP-06 Summary Contract Gaps

Sprint: N-IMP-06
Status: documented, not repaired

No new approved knowledge was invented in this sprint.

---

## sentence library

**SENTENCE LIBRARY RUNTIME GAP** (carried from N-IMP-05).

`SentenceSelector.select()` returns None. Summary Builder does not create a local sentence library.

Assembly uses only:

- approved rewrite unit `customer_language`
- deterministic sentence split / whitespace join

Missing: dedicated Executive Summary sentence assets.

---

## headline assets

No registered headline templates.

Headline = first sentence of the primary rewrite unit, if word count ≤ 25.

If that sentence is unsafe or too long, `headline = None`.

CASE-0001: first sentence of `rewrite.pattern.chinh_an.001` was used.

---

## identity semantics

Spec wants Nhật Chủ / Thân / Mệnh Cục as a short identity line.

Runtime: no dedicated customer-safe identity rewrite unit.

Day Master is not rewritten. Copying the pattern unit into `identity` would duplicate the primary insight.

`identity = None` (`identity_status = unresolved`).

---

## balance semantics

Spec wants Dụng Thần / Điều Hậu.

Runtime: Useful God and Temperature rewrite keys are unresolved.

Do not map raw Useful God or Temperature into `balance`.

`balance = None` (`balance_status = unresolved`).

---

## useful god

`core.useful_god_context` unresolved from Rewrite (`source_not_customer_safe`).

Not invented. Not used as primary insight. Not used as balance.

---

## temperature

`core.temperature_balancing_context` unresolved from Knowledge/Rewrite.

Not invented. Not used as balance.

---

## luck

`core.luck_temporal_context` unresolved from Knowledge/Rewrite.

Not invented. No luck sentence in Overview.

---

## conclusion assets

No remaining unused rewrite sentence that could form a non-duplicate 1–2 sentence conclusion without new meaning.

`conclusion = None` (`conclusion_status = omitted`).

---

## product-quality note

CASE-0001 Overview is a short assembly of pattern + strength rewrite units.

It is not a polished consultant paragraph. That requires sentence-library / identity / balance assets in later sprints. Honest `partial` is preferred over invented completeness.
