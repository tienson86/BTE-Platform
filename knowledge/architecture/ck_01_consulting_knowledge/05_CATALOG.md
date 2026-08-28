# 05 — Knowledge Catalog

| Field | Value |
|-------|--------|
| Document | CK-01B Knowledge Catalog |
| Version | 1.0.0 |
| Status | Canonical for CK-01B |
| Catalog id | `bte.consulting.knowledge.catalog.v1` |

---

## 1. Purpose

Store Consulting Knowledge Units as deterministic catalog entries.

This sprint does not match. It does not compose. It does not render.

---

## 2. Structure

```
Knowledge Domains
        ↓
Knowledge Units
        ↓
Condition
Applicable scope
Consulting meaning
Customer wording
Recommended actions
References
```

Machine store:

`engines/consulting_knowledge/catalog.py`

Load surface (no match):

`engines/consulting_knowledge/loader.py`

---

## 3. Catalog rules

- Every frozen domain has at least one complete unit.
- `unit_id` is stable. Format: `ck-{domain}-{nnn}` (`action_library` uses `ck-action-{nnn}`).
- Wording is stored. It is never generated at load time.
- `action_library` holds reusable recommended actions. Other domains may reference those ids. They do not invent new actions at runtime.
- Same catalog load → same ordered tuple.

---

## 4. What this sprint does not do

- No condition matching against published signals
- No signal projection
- No Composer
- No UI
- No Report / PDF / DOCX wire
- No Calendar / Bazi / Identity / Narrative change

---

## 5. Unit index

| unit_id | Domain | Condition key |
|---------|--------|----------------|
| `ck-career-001` | career | `strength_level` = Thân vượng |
| `ck-career-002` | career | `strength_level` = Thân nhược |
| `ck-finance-001` | finance | `strength_level` = Thân vượng |
| `ck-finance-002` | finance | `strength_level` = Thân nhược |
| `ck-relationship-001` | relationship | `strength_level` = Thân vượng |
| `ck-relationship-002` | relationship | `strength_level` = Thân nhược |
| `ck-health-001` | health | `strength_level` = Thân vượng |
| `ck-health-002` | health | `strength_level` = Thân nhược |
| `ck-leadership-001` | leadership | `useful_god` contains Chính Quan |
| `ck-leadership-002` | leadership | `strength_level` = Thân vượng |
| `ck-management-001` | management | `strength_level` = Thân vượng |
| `ck-management-002` | management | `strength_level` = Thân nhược |
| `ck-communication-001` | communication | `strength_level` = Thân vượng |
| `ck-communication-002` | communication | `strength_level` = Thân nhược |
| `ck-business-001` | business | `strength_level` = Thân vượng |
| `ck-business-002` | business | `strength_level` = Thân nhược |
| `ck-personality-001` | personality | `strength_level` = Thân vượng |
| `ck-personality-002` | personality | `strength_level` = Thân nhược |
| `ck-action-001` | action_library | `action_kind` = operating_frame |
| `ck-action-002` | action_library | `action_kind` = rest_on_calendar |
| `ck-action-003` | action_library | `action_kind` = named_ally |
| `ck-action-004` | action_library | `action_kind` = one_channel |

---

END
