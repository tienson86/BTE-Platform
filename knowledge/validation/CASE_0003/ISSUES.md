# ISSUES — CASE-0003 Extreme Validation

Severity: S0 blocker · S1 high · S2 medium · S3 low  
**No fixes applied this cycle.**

---

## ISS-C3-001 — Stated pillars ≠ engine pillars

| Field | Content |
|-------|---------|
| Severity | **S1** |
| Symptom | Input 2015-02-15 + stated Giáp Ngọ/Đinh Sửu/…; engine publishes Ất Mùi/Mậu Dần/Nhâm Tuất/Quý Mão |
| Customer impact | Chart identity dispute if customer holds traditional pillars |
| Suspected layer | RUNTIME_DATA / Calendar boundary / input documentation |
| Evidence | BASELINE pillar table; `_raw_pipeline.json` |

## ISS-C3-002 — Positive-language bias on weak chart

| Field | Content |
|-------|---------|
| Severity | **S1** |
| Symptom | Memory/closing: “Bạn mạnh hơn khi đi đúng kênh biểu đạt…” despite strength weak 0.19 |
| Customer impact | Undercuts conservation message; feels like motivational copy |
| Suspected layer | COMPOSER / CLL memory templates |
| Evidence | Identity SUMMARY · Executive CONCLUSION |

## ISS-C3-003 — TRUE_CONFLICT UG↔weak under-surfaced in Customer Mode

| Field | Content |
|-------|---------|
| Severity | **S1** |
| Symptom | CDR has `ug_drain_vs_weak` + `TRUE_CONFLICT_NEEDS_ARBITRATION`; customer features emphasize follow/strength nuance, not UG drain vs weak body |
| Customer impact | False completeness; trust risk for advanced readers |
| Suspected layer | COMPOSER / CLL limitation selection |
| Evidence | CDR conflicts vs Identity/Executive LIMITS text |

## ISS-C3-004 — Career packaging ignores age / extreme weakness

| Field | Content |
|-------|---------|
| Severity | **S1** |
| Symptom | Full adult career decision report for 2015-born subject |
| Customer impact | Commercially inappropriate; action realism fail |
| Suspected layer | FEATURE_PACKAGING |
| Evidence | Career body; birth year 2015 |

## ISS-C3-005 — Overconfidence / empowerment template dominance

| Field | Content |
|-------|---------|
| Severity | **S1** |
| Symptom | OPERATING_OUTPUT templates (“ổn hơn”, “rõ và bền hơn”, “quyền quyết định trên đầu ra”) dominate over CAPACITY_WEAK conservation |
| Customer impact | Sounds like strong/output adult chart |
| Suspected layer | CLL theme priority in prose (primary theme wins too hard) |
| Evidence | Identity/Career/Executive bodies |

## ISS-C3-006 — Action realism weak for low capacity

| Field | Content |
|-------|---------|
| Severity | **S2** |
| Symptom | Priorities still “điều phối tuần làm việc / đừng nhận việc trái nhịp” without explicit load-minimization for weak 0.19 |
| Customer impact | Advice may encourage activity volume |
| Suspected layer | ACTION_LANGUAGE / claim-plan avoid list |
| Evidence | ACTIONS / FOCUS / PRIORITIES sections |

## ISS-C3-007 — Pattern label vs follow flag readability

| Field | Content |
|-------|---------|
| Severity | **S2** |
| Symptom | cach_cuc=Thực Thần while tong_cach=Tòng Nhi; CLL structure cue often generic “khung dài hạn đã xác định” |
| Customer impact | Follow nature under-explained vs CASE-0002 |
| Suspected layer | COMPOSER cue parsing / ENGINE publish pairing |
| Evidence | plan.identity_core structure:Thực Thần; tong_cach Tòng Nhi |

## ISS-C3-008 — Child/minor policy not published

| Field | Content |
|-------|---------|
| Severity | **S2** |
| Symptom | No feature gate for minors on Career/Executive action intensity |
| Customer impact | Product risk |
| Suspected layer | POLICY / FEATURE_PACKAGING |
| Evidence | Birth 2015 + Career AVAILABLE |

---

## Counts

| Severity | n |
|----------|---|
| S0 | 0 |
| S1 | 5 |
| S2 | 3 |
| **Total** | **8** |
