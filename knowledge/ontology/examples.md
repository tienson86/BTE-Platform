# Ontology Examples

Illustrative only. No analytical rule content is authored here.

---

## Example 1 — Specialization

- Base: `ONT-RULE` / Follow Pattern family
- Specialized: Follow Wealth rule record
- Link: `specializes`
- Structural membership: belongs_to `DOM-PATTERN` / follow category / follow package

---

## Example 2 — Composition

- Whole: Rule `STR-000001`
- Parts: Condition (`month_status == prosperous`) + Result (`strength_score` effect)
- Link: `composes`
- Structural: package `contains` rule; rule `contains` conditions/result

---

## Example 3 — Language equivalence

- Base record id: `KR-000100`
- Vietnamese payload language `vi`
- English variant declares `translation_of` → `KR-000100`
- Same identity, different presentation

---

## Example 4 — Override

- Shared package rule priority order 50
- Project overlay declares `project_override` on same target with order 90
- Resolution: project overlay wins; shared rule remains stored and immutable

---

## Example 5 — Future school expansion

- Base BaZi useful-god concept
- School variant under `DOM-SCHOOL` specializes selection thresholds
- Link: `same_as_school` / `specializes`
- No change to core BaZi domain identity
