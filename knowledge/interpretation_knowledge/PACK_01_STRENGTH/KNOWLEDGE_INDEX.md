# Knowledge Index — PACK-01 Strength

| Field | Value |
|-------|-------|
| Document | KNOWLEDGE_INDEX |
| Pack | PACK-01 Strength Interpretation Knowledge |
| Version | 1.0.0 |

---

# 1. Purpose

Catalog of Strength interpretation knowledge units by class and topic.

IDs are stable keys for a future engine.

They are not customer-facing text.

---

# 2. ID Convention

```text
IK-STR-<TOPIC>-<CLASS>-<NN>
```

| Part | Values |
|------|--------|
| `IK` | Interpretation Knowledge |
| `STR` | Strength pack |
| `TOPIC` | MEAN / CAUSE / ADV / CHAL / PERS / CAR / WEA / MAR / HEA / LUCK / REC / EDGE / EX |
| `CLASS` | VS / ST / BA / WK / VW / ALL / EDGE |
| `NN` | Two-digit sequence inside that slice |

---

# 3. Coverage Matrix

| Topic | VS | ST | BA | WK | VW | Notes |
|-------|----|----|----|----|----|-------|
| Meanings | yes | yes | yes | yes | yes | 01 |
| Causes | yes | yes | yes | yes | yes | plus ALL cause families in 02 |
| Advantages | yes | yes | yes | yes | yes | 03 |
| Challenges | yes | yes | yes | yes | yes | 04 |
| Personality | yes | yes | yes | yes | yes | 05 |
| Career | yes | yes | yes | yes | yes | 06 |
| Wealth | yes | yes | yes | yes | yes | 07 |
| Marriage | yes | yes | yes | yes | yes | 08 |
| Health | yes | yes | yes | yes | yes | 09 |
| Luck | yes | yes | yes | yes | yes | natal × support / unfavor / transition in 10 |
| Recommendations | yes | yes | yes | yes | yes | 11 |
| Edge cases | — | — | — | — | — | shared in 12 |
| Examples | yes | yes | yes | yes | yes | 13 |

“yes” means the file contains distinct consulting knowledge for that class, not a synonym of another class.

---

# 4. Unit Families

## 4.1 Meanings (`01_MEANINGS.md`)

| ID prefix | Class |
|-----------|-------|
| IK-STR-MEAN-VS | Very Strong |
| IK-STR-MEAN-ST | Strong |
| IK-STR-MEAN-BA | Balanced |
| IK-STR-MEAN-WK | Weak |
| IK-STR-MEAN-VW | Very Weak |

Facets per class: lived_meaning, core_characteristic, natural_tendency.

## 4.2 Causes (`02_CAUSES.md`)

| ID prefix | Family |
|-----------|--------|
| IK-STR-CAUSE-SEASON | Season / Đắc Lệnh |
| IK-STR-CAUSE-ROOT | Root / Đắc Địa / Thông Căn |
| IK-STR-CAUSE-SUPPORT | Support / Đắc Thế |
| IK-STR-CAUSE-DRAIN | Drain |
| IK-STR-CAUSE-CONTROL | Control |
| IK-STR-CAUSE-COMB | Combination / clash / void |
| IK-STR-CAUSE-CLASS-* | How causes cluster into each class |

## 4.3 Advantages (`03_ADVANTAGES.md`)

Facets: decision_making, leadership, learning, discipline, adaptability, responsibility, stress_tolerance.

## 4.4 Challenges (`04_CHALLENGES.md`)

Facets: overconfidence, underconfidence, blind_spot, typical_mistake, emotional_tendency.

## 4.5 Personality (`05_PERSONALITY.md`)

Facets: behavior, communication, thinking, working_style, motivation, conflict_style.

## 4.6 Career (`06_CAREER.md`)

Facets: suitable, unsuitable, management, employment, entrepreneurship.

## 4.7 Wealth (`07_WEALTH.md`)

Facets: behavior, saving, investment, risk, opportunity.

## 4.8 Marriage (`08_MARRIAGE.md`)

Facets: bond, partner, communication, family.

## 4.9 Health (`09_HEALTH.md`)

Facets: energy, stress, lifestyle, balance.

## 4.10 Luck (`10_LUCK.md`)

Facets: supportive, unfavorable, transition. Crossed with each natal class.

## 4.11 Recommendations (`11_RECOMMENDATIONS.md`)

Facets: do, avoid, environment, habits, career_direction, learning, lifestyle.

## 4.12 Edge (`12_EDGE_CASES.md`)

IK-STR-EDGE-01 … borderline, conflict, exception families.

## 4.13 Examples (`13_EXAMPLES.md`)

IK-STR-EX-VS-01 … one vignette family per class, plus one conflict vignette.

---

# 5. Selection Notes for Future Engine

1. Pick class first from published Strength result.
2. Always load meaning for that class.
3. Load cause units only for causes present.
4. Load domain units for required Customer Mode sections.
5. Load luck units only if luck is published.
6. Load recommendations last, matching selected challenges.
7. Compose with Interpretation Standard. Do not dump this index to the customer.

---

# 6. Gaps Intentionally Left Open

This pack does not author:

- Useful God element names as Strength advice
- Pattern names as Strength advice
- Ten God lectures
- Medical diagnoses
- Guaranteed timelines

Those belong to later packs or to professional care outside BTE.

---

END
