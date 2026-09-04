# P-003B.2 Coverage report

Date: 2026-09-04

Lookup: published visible names, drop Nhật Chủ, exact supported unit, else longest supported subset. Classified but unsupported sets omit the combination card.

---

## Pair coverage

| Metric | Value |
|--------|------:|
| Possible visible pairs | 45 |
| Supported | 16 |
| Deferred | 13 |
| Conflicting | 12 |
| Low value | 2 |
| Not customer safe | 2 |
| Pair coverage | 35.6% |

---

## Triple coverage

| Metric | Value |
|--------|------:|
| Possible triples | 120 |
| Supported | 2 |
| Deferred (use strongest pair) | 118 |

V1.0 does not attempt full triple coverage.

---

## CASE-0001

Visible: Kiếp Tài, Thất Sát, Thiên Ấn  
Bound: exact triple **Kiếp Tài · Thất Sát · Thiên Ấn**  
Hidden Thiên Tài · Chính Ấn: muted support only (LOW_VALUE as a full model)

---

## CASE-0002

Visible: Thương Quan, Thực Thần, Chính Quan  
Bound: exact triple **Thực Thần · Thương Quan · Chính Quan**

---

## launch_08 fixtures

| Fixture | Visible role gods | Bound | Note |
|---------|-------------------|-------|------|
| case_001 | Kiếp Tài, Thất Sát, Thiên Ấn | triple CASE-0001 | same published set |
| case_002 | Kiếp Tài, Thất Sát, Chính Tài | Kiếp Tài · Thất Sát | leftover Chính Tài stays a P-003 card |
| case_003 | Thực Thần, Thương Quan | Thực Thần · Thương Quan | exact pair |
| case_004 | Chính Tài, Thực Thần, Kiếp Tài | Thực Thần · Chính Tài | leftover Kiếp Tài stays a P-003 card |
| case_005 | Tỷ Kiên, Kiếp Tài, Thiên Tài | Kiếp Tài · Thiên Tài | leftover Tỷ Kiên stays a P-003 card |
| case_006 | Chính Quan, Kiếp Tài | omitted | CONFLICTING — short rhythm vs approval |
| case_007 | Thất Sát, Thương Quan, Chính Tài | omitted | no supported pair; NCS / DEFERRED / CONFLICTING |
| case_008 | Thực Thần, Thiên Ấn, Kiếp Tài | Thực Thần · Thiên Ấn | leftover Kiếp Tài stays a P-003 card |

Fixture bind-or-correct-omit: **8 / 8**.  
Fixture with a supported model: **6 / 8**.  
Two omissions are classified, not gaps in lookup.

---

## Unknown

Members outside the ten role gods, or a single role god, classify as UNKNOWN and omit the combination card.
