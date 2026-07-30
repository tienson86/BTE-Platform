# Wood Knowledge Record — Relationship Report

**Source record:** `KNO-000001` Wood (木)  
**Date:** 2026-07-30  
**Model:** Classical Wu Xing cycles (Sheng / Ke / Cheng / Wu)  
**No Rule logic embedded.**  

---

## 1. Relationship matrix

| Slot | Type | Target ID | Target element | Cycle |
|------|------|-----------|----------------|-------|
| `generates` | generates | `KNO-000002` | Fire | Sheng |
| `generated_by` | generated_by | `KNO-000005` | Water | Sheng |
| `controls` | controls | `KNO-000003` | Earth | Ke |
| `controlled_by` | controlled_by | `KNO-000004` | Metal | Ke |
| `overacts` | overacts | `KNO-000003` | Earth | Cheng |
| `overacted_by` | overacted_by | `KNO-000004` | Metal | Cheng |
| `insults` | insults | `KNO-000004` | Metal | Wu |
| `insulted_by` | insulted_by | `KNO-000003` | Earth | Wu |

---

## 2. Graph (from Wood)

```text
Water (KNO-000005)
        │ generated_by
        ▼
Wood (KNO-000001)
   │ generates          │ controls / overacts
   ▼                    ▼
Fire (KNO-000002)    Earth (KNO-000003)
                           │ insulted_by (from Earth to Wood)
Metal (KNO-000004) ◄───────┘
   ▲
   │ controlled_by / overacted_by / insults
   └── Wood
```

---

## 3. ID allocation used

| Element | Knowledge ID | Record file |
|---------|--------------|-------------|
| Wood | `KNO-000001` | `wood.json` (this record) |
| Fire | `KNO-000002` | not created |
| Earth | `KNO-000003` | not created |
| Metal | `KNO-000004` | not created |
| Water | `KNO-000005` | not created |

IDs are reserved within `KNO-000001 – KNO-000099` (Five Elements domain range).

---

## 4. Validation status

| Check | Result |
|-------|--------|
| Required relationship slots filled | PASS |
| Knowledge ID format on all targets | PASS |
| relationship_type present on all links | PASS |
| Target records resolvable in Canon | FAIL (pending implementation of Fire/Earth/Metal/Water) |
| `validation.relationship_valid` | `false` |

---

## 5. Academic Review questions

1. Confirm reserved IDs `KNO-000002`–`KNO-000005` for sibling elements.
2. Confirm Cheng/Wu pairings as recorded (same Ke axis, excess/reverse forms).
3. Confirm no additional Wood relationship types are required beyond WOOD_SPEC §9.
