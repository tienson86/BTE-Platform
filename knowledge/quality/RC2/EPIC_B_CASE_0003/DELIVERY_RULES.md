# DELIVERY_RULES

| Field | Value |
|-------|-------|
| Epic | EPIC-B |
| Owner | Product Context Engine V1.1 |
| Does not own | Engine facts, CDR, CLL source |

---

## Adaptive vs filter

| Filter (V1.0) | Adaptive (V1.1) |
|---------------|-----------------|
| Hide Career | Hide Career **and** deliver Development + Learning + Confidence |
| Dump diagnostics into Development | Customer development prose from claim-plan cues |
| Thin parent checklist | Parent actions + parent voice |
| Keep adult theme labels | Map theme → development frame |

Adult SELF default remains **pass_through** (CASE-0001 / CASE-0002 unchanged).

---

## Flow (unchanged architecture)

```text
Truth composition (CLL)     ← frozen
        ↓
ProductContextEngine.resolve
        ↓
Feature filter (safety)
        ↓
ContextDeliveryAdapter.apply
        ↓
Adaptive frames if not pass_through
        ↓
Customer deliverable
```

---

## Audience rules

| If | Then |
|----|------|
| ADULT + SELF | Pass through CLL bodies |
| CHILD or PARENT | Parent language; Career hidden; Development on |
| Weak capacity | Conservation first — no empowerment close |
| Unresolved CDR | Condition spoken to phụ huynh — no fake single label |

---

## Safety (unchanged)

Child/teen never receive adult Career Decision, business expansion, or marriage timing — even if `report_type=CAREER`.

---

END
