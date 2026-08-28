# 03 — Knowledge Unit Model

| Field | Value |
|-------|--------|
| Document | CK-01A Knowledge Unit |
| Version | 1.0.0 |
| Status | Canonical for CK-01A |
| Contract id | `bte.consulting.knowledge.v1` |

---

## 1. ConsultingKnowledgeUnit

Every unit contains exactly these consulting fields:

| Field | Speaks |
|-------|--------|
| `condition` | Published signals that must already be true |
| `applicable_scope` | Domain and audience bounds |
| `consulting_meaning` | What this means for the person, as consulting knowledge |
| `customer_wording` | Customer-facing sentences stored in the catalog |
| `recommended_actions` | Stored actions. Never invented at match time |
| `references` | Knowledge / narrative / analysis paths this unit rests on |

Required identity fields:

| Field | Description |
|-------|-------------|
| `unit_id` | Stable catalog id |
| `domain` | One frozen domain id |
| `status` | `complete` / `partial` / `insufficient` |

A unit with missing customer wording is insufficient. It is not filled by generation.

---

## 2. Condition

Conditions are published-key tests.

Example:

```
strength_level = Thân vượng
useful_god contains Chính Quan
```

Match is equality or membership on copied signals.

Match is not a score, rank, or forecast.

---

## 3. ConsultingKnowledgePack

Ordered list of matched units.

`status`:

| Condition | Status |
|-----------|--------|
| At least one complete unit | `complete` or `partial` |
| No matched unit | `insufficient` |

---

## 4. Ownership

| Artifact | Owner |
|----------|--------|
| Analytical fact | Engine result / Identity / Integrated Narrative |
| Catalog wording | Consulting knowledge base |
| Match order | CK-01 framework |
| Delivery layout | Report / Portal (unchanged in CK-01A) |

---

END
