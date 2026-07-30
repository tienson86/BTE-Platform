# Wood Knowledge Record — Integrity Report

**Record:** `KNO-000001`  
**Date:** 2026-07-30  

---

## 1. Identity integrity

| Check | Result |
|-------|--------|
| Knowledge ID format `KNO-NNNNNN` | PASS (`KNO-000001`) |
| Canonical name | PASS (`Wood`) |
| Chinese | PASS (`木`) |
| Pinyin | PASS (`Mu`) |
| English name | PASS (`Wood`) |
| ID uniqueness within authored Five Elements JSON records | PASS (only Wood record present) |

---

## 2. Classification integrity

| Check | Result |
|-------|--------|
| `domain` = `five_elements` | PASS |
| `category` = `element` | PASS |
| Subcategory present | FAIL vs WOOD_SPEC (omitted for schema compliance) |

---

## 3. Reference integrity

| Reference ID | Title | In Reference Library index? |
|--------------|-------|-----------------------------|
| `REF-000001` | Yuan Hai Zi Ping | Yes |
| `REF-000002` | Di Tian Sui | Yes |
| `REF-000003` | San Ming Tong Hui | Yes |
| `REF-000005` | Zi Ping Zhen Quan | Yes |

| Check | Result |
|-------|--------|
| All reference IDs resolve in library catalog | PASS |
| Chapter citations verified | FAIL (`TODO_REVIEW`) |
| `validation.reference_valid` | `true` (IDs valid; chapters pending Academic Review) |

---

## 4. Relationship integrity

| Check | Result |
|-------|--------|
| All relationship slots present | PASS |
| Each link has Knowledge ID + relationship_type | PASS |
| No self-reference (`KNO-000001` → `KNO-000001`) | PASS |
| Target records exist on disk | FAIL (Fire/Earth/Metal/Water not authored) |
| `validation.relationship_valid` | `false` |

---

## 5. Content integrity

| Check | Result |
|-------|--------|
| No Rule Engine logic | PASS |
| No scoring | PASS |
| No interpretation / fortune text | PASS |
| Uncertain academic values marked `TODO_REVIEW` | PASS |
| Schema compliance | PASS |
| Locked specs unmodified | PASS |

---

## 6. Integrity verdict

**Structural integrity:** PASS for schema and authored fields.  
**Cross-record integrity:** PENDING sibling element records.  
**Academic citation integrity:** PENDING Academic Review (`TODO_REVIEW` chapters).  

Overall: **Draft-ready for Academic Review, not Official.**
