# CONSULTING LANGUAGE PACK

# 06_CUSTOMER_WORDING.md

Document ID: LANG-PACK-06

Version: 0.1.0-skeleton

Status: DRAFT — STRUCTURAL SLOTS ONLY

---

# 1. Purpose

Mô tả cách semantic facts trở thành readable language.

Không finalize câu thương mại trong LANG-01.

---

# 2. Pipeline

```
Comparison / Decision fact
  ↓
source_fact identity (example: useful_god_support)
  ↓
supporting_fact_template
  ↓
slot fill ({person_a}, {element}, {person_b})
  ↓
customer bullet
```

Missing source fact → omit the bullet. Do not invent.

---

# 3. Structural Example

Technical fact (not customer prose):

```
useful_god_support(A→B, Fire)
```

Customer wording slot (structure only; not Product Owner approved copy):

```
{person_a} mang yếu tố {element} phù hợp với phần mà {person_b} đang cần.
```

YAML stores this as `status: placeholder` until Product Owner authors the final sentence.

Do not treat the slot example as frozen commercial copy.

---

# 4. Verdict Mapping (keys only)

| Semantic | Language key | Headline in LANG-01 |
|---|---|---|
| supportive compatibility | `marriage.q1.supportive` | `__PRODUCT_OWNER_WORDING_REQUIRED__` |
| mixed compatibility | `marriage.q1.mixed` | `__PRODUCT_OWNER_WORDING_REQUIRED__` |
| pressured compatibility | `marriage.q1.pressured` | `__PRODUCT_OWNER_WORDING_REQUIRED__` |
| children unpublished | `marriage.q5.insufficient` | `__PRODUCT_OWNER_WORDING_REQUIRED__` |
| can progress | `marriage.q6.can_progress` | `__PRODUCT_OWNER_WORDING_REQUIRED__` |

R02 live answers (`Trung bình.`, `Insufficient.`, …) stay in Assessment projector until a later ticket.

---

# 5. Slot Names

Standard slots:

- `{person_a}` `{person_b}`
- `{element}`
- `{day_master_a}` `{day_master_b}`
- `{direction}` (`A_TO_B` / `B_TO_A`)
- `{role}`

Unknown slot left unsubstituted is a validation error at integration time. LANG-01 does not fill live names.

---

# 6. Insufficient Data

Q5 and other unpublished domains use `marriage.*.insufficient`.

Wording must say the domain is unsupported.

Wording must not predict fertility, child count, or gender.

---

# 7. Authoring Rule

Product Owner writes Vietnamese into YAML.

Cursor must not complete those fields with generic consulting prose to make files look finished.
