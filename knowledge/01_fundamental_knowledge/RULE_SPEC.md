# Fundamental Knowledge Rule Specification

**Module:** Fundamental Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Business Rule Policy)

---

# 1. Purpose

This document defines the rule policy of Fundamental Knowledge.

---

# 2. Policy Statement

Fundamental Knowledge publishes **no analytical business rules**.

It publishes canonical knowledge only.

---

# 3. What Is Excluded

The following are out of scope and must not appear as Rule Assets in this module:

- Day Master strength scoring rules
- climate / temperature scoring rules
- Pattern candidate and resolution rules
- Useful God determination rules
- Ten Gods quality evaluation rules
- Combination activation / transformation business rules
- ShenSha detection rules
- Luck impact evaluation rules
- interpretation selection rules
- report rendering rules

---

# 4. What May Exist Instead

Structural knowledge may exist as:

- Mapping Tables
- Reference Tables
- Relationship matrices
- Structural Formula Library entries
- Terminology

These are not business Rule Assets.

---

# 5. Downstream Ownership

Business rules belong to domain Knowledge Modules, for example:

| Concern | Owning Module |
|---------|---------------|
| Strength rules | Strength Knowledge |
| Temperature rules | Temperature Knowledge |
| Pattern rules | Pattern Knowledge |
| Useful God rules | Useful God Knowledge |

---

# 6. Validation Implication

Publication validation shall fail if analytical Rule Assets are introduced under Fundamental Knowledge without a MAJOR scope change.

---

# 7. Acceptance Criteria

This policy is satisfied when:

- no business Rule Database is declared;
- canonical knowledge remains mapping/reference/terminology based;
- domain decision logic remains outside this module.
