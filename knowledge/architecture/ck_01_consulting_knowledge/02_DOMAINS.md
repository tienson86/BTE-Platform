# 02 — Knowledge Domains

| Field | Value |
|-------|--------|
| Document | CK-01A Knowledge Domains |
| Version | 1.0.0 |
| Status | Canonical for CK-01A |

---

## 1. Frozen domain catalog

Every knowledge unit belongs to exactly one domain.

| Order | Id | Customer title |
|-------|----|----------------|
| 1 | `career` | Sự nghiệp |
| 2 | `finance` | Tài chính |
| 3 | `relationship` | Quan hệ |
| 4 | `health` | Sức khỏe |
| 5 | `leadership` | Lãnh đạo |
| 6 | `management` | Quản lý |
| 7 | `communication` | Giao tiếp |
| 8 | `business` | Kinh doanh |
| 9 | `personality` | Tính cách |
| 10 | `action_library` | Thư viện hành động |

This list is the CK-01A freeze. Later sprints add units inside a domain. They do not add a domain without an architecture change.

---

## 2. Domain rules

- A unit does not span two domains. Duplicate the unit with a new id if two domains need the same condition.
- `action_library` stores reusable recommended actions. Other domains may reference those actions. They do not calculate new actions.
- Domains are consulting scopes, not engine topics. Strength / Pattern / Useful God remain analytical.

---

## 3. Brand

Consultant, not calculator. Domain advice stays reversible and non-medical / non-legal as a guarantee.

---

END
