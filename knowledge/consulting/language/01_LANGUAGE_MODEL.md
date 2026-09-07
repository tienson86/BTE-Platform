# CONSULTING LANGUAGE PACK

# 01_LANGUAGE_MODEL.md

Document ID: LANG-PACK-01

Version: 0.1.0-skeleton

Status: DRAFT — SCHEMA ONLY

---

# 1. Purpose

Định nghĩa Language Entry.

Language Entry là đơn vị wording đã kiểm soát.

Một semantic meaning → một `language_key` → một Entry (có thể có variants).

---

# 2. Language Entry

Required conceptual fields:

| Field | Required | Role |
|---|---|---|
| `language_key` | yes | Deterministic catalog identity |
| `module` | yes | `marriage` / `business` / `career` / `child` |
| `question_id` | yes | Question Set id (`Q1`…) |
| `semantic_state` | yes | Semantic truth token, not prose |
| `version` | yes | Entry version |
| `status` | yes | `placeholder` / `draft` / `approved` / `frozen` |
| `audience` | no | default `customer` |
| `tone` | no | default `professional_warm` |
| `headline` | no | Kết luận slot |
| `meaning` | no | Ý nghĩa slot |
| `plain_customer_text` | no | Customer sentence without jargon |
| `technical_explanation` | no | Optional Bát Tự reason under the meaning |
| `supporting_fact_templates` | no | Cơ sở slots |
| `limitation_templates` | no | Lưu ý slots |
| `closing` | no | Closing / xem chi tiết |
| `variants` | no | Approved alternate wordings |
| `forbidden_terms` | no | Extra bans for this entry |
| `slots` | no | Placeholder names such as `{person_a}` |

Optional fields may be omitted. Loader fills defaults. Validator only requires the yes-column.

---

# 3. Status Lifecycle

```
placeholder  →  draft  →  approved  →  frozen
```

`placeholder` = Product Owner wording required. Token:

```
__PRODUCT_OWNER_WORDING_REQUIRED__
```

`draft` = authored, not reviewed.

`approved` = Product Owner signed.

`frozen` = behavior-locked. Change requires version bump + ticket.

LANG-01 catalog entries stay `placeholder`.

---

# 4. Technical Term Separation

Entry must be able to carry two layers:

```
plain_customer_text
  ↓
technical_explanation   (optional, collapsed in UI)
```

Không được chỉ phát technical fragment như wording khách hàng.

Bad (forbidden as customer headline):

`Nhật Chủ cùng Kim.`

Required structure when a technical reason is needed:

1. Customer meaning first
2. Technical reason underneath, if the Product Owner later authors it

---

# 5. Supporting Fact Template

A supporting fact is a template, not an invented fact.

```yaml
supporting_fact_templates:
  - id: useful_god_support
    source_fact: useful_god_support
    template: "__PRODUCT_OWNER_WORDING_REQUIRED__"
    slots: [person_offer, person_need, element]
    status: placeholder
```

Renderer later substitutes slots from Decision comparison facts.

Renderer must not invent a fact that Assessment / comparison did not publish.

---

# 6. Assessment Card Slots

Language Entry does not store UI labels.

Presentation binds:

| Order | UI label (Presentation) | Entry field |
|---|---|---|
| 1 | Kết luận | `headline` |
| 2 | Ý nghĩa | `meaning` |
| 3 | Cơ sở | `supporting_fact_templates` |
| 4 | Lưu ý | `limitation_templates` |
| 5 | Closing | `closing` |

---

# 7. Schema File

Machine schema: `knowledge/consulting/language/schema.yaml`

Python model: `consulting/language/models.py`

Hai nguồn phải cùng required field set.
