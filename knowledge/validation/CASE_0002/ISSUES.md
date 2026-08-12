# CASE-0002 — Issue Register

| Field | Value |
|-------|-------|
| Subject | Hoàng Thị Thu Phương · 1997-07-01 |
| Fixes | **None this cycle** |

Severity: S0 blocker · S1 high · S2 medium · S3 low

---

## ISS-001 — Identity Feature not generated

| Field | Content |
|-------|---------|
| Symptom | No Feature 01 Identity Report from pipeline |
| Customer impact | Cannot deliver “Who am I?” product |
| Evidence | Orchestrator outputs domain dicts only; IDENTITY_REVIEW FAIL |
| Suspected layer | Commercial / Composer |
| Severity | **S0** |

## ISS-002 — Career Feature not generated

| Field | Content |
|-------|---------|
| Symptom | No Feature 02 Career Report from pipeline |
| Customer impact | Cannot deliver career direction product |
| Evidence | CAREER_REVIEW FAIL |
| Suspected layer | Commercial / Composer |
| Severity | **S0** |

## ISS-003 — Strength vs Pattern intensity contradiction unexplained

| Field | Content |
|-------|---------|
| Symptom | Strength = balanced/trung hòa; Pattern label = “Nhật chủ cực nhược…” (Tòng Nhi) |
| Customer impact | Confusing self-image; trust break |
| Evidence | strength_level balanced 0.61; pattern.cach_cuc Tòng Nhi cực nhược; integrated.conflicts = [] |
| Suspected layer | Reasoning / Narrative / Engine publish wording |
| Severity | **S1** |

## ISS-004 — Executive insight template mismatch

| Field | Content |
|-------|---------|
| Symptom | Insight = “sức bền / đầu ra có chu kỳ / không gánh thêm” on a balanced + Tòng Nhi + Thương Quan chart |
| Customer impact | Feels like wrong person’s advice (CASE-0001-shaped) |
| Evidence | executive_body insight vs domains (balanced, Tòng Nhi, Thương Quan, Nhâm) |
| Suspected layer | Reasoning / Narrative / Composer |
| Severity | **S1** |

## ISS-005 — Customer jargon / stem opacity

| Field | Content |
|-------|---------|
| Symptom | Thông căn, Thực/Thương, Nhâm/Bính/Đinh, relationship dumps without life meaning |
| Customer impact | Calculator feel; fails commercial composition rules |
| Evidence | domain section bodies in `_raw_pipeline.json` |
| Suspected layer | Composer / Knowledge |
| Severity | **S1** |

## ISS-006 — Conflict detector silent

| Field | Content |
|-------|---------|
| Symptom | `conflicts: []` despite strength↔pattern wording clash |
| Customer impact | No qualified language; false confidence |
| Evidence | integrated.conflicts empty |
| Suspected layer | Reasoning |
| Severity | **S1** |

## ISS-007 — Pressure copy ignores output-led system

| Field | Content |
|-------|---------|
| Symptom | Ten Gods pressure text = generic “trách nhiệm và chuẩn mực” while primary is Thương Quan (expression/output) |
| Customer impact | Misstates operating style |
| Evidence | ten_gods PRESSURE section vs primary shang_guan |
| Suspected layer | Composer / Knowledge |
| Severity | **S1** |

## ISS-008 — Useful God not translated to work/life actions

| Field | Content |
|-------|---------|
| Symptom | “Hướng Nhâm / tránh Bính Đinh” without career or identity so-what |
| Customer impact | Unusable balance advice for paying customer |
| Evidence | useful_god sections |
| Suspected layer | Knowledge / Composer |
| Severity | **S2** |

## ISS-009 — DRAFT_KNOWLEDGE on all domains

| Field | Content |
|-------|---------|
| Symptom | All domain knowledge_status = DRAFT_KNOWLEDGE |
| Customer impact | Pilot quality ceiling |
| Evidence | domain diagnostics |
| Suspected layer | Knowledge |
| Severity | **S2** |

## ISS-010 — Master interpretation NOT_AVAILABLE

| Field | Content |
|-------|---------|
| Symptom | No Master markdown; Executive substitutes poorly |
| Customer impact | Package C not deliverable |
| Evidence | section_status.master_interpretation |
| Suspected layer | Commercial / Narrative |
| Severity | **S2** |

## ISS-011 — Avoid list mismatched to chart risks

| Field | Content |
|-------|---------|
| Symptom | Avoids emphasize “nhận thêm tải / tự gánh” — may not be primary risk for follow-output / balanced profile |
| Customer impact | Wrong career risk narrative |
| Evidence | executive avoids vs chart characteristics |
| Suspected layer | Narrative / Composer |
| Severity | **S2** |

## ISS-012 — Pattern qualifier “Trung hòa” vs “cực nhược” in same view

| Field | Content |
|-------|---------|
| Symptom | than_vuong_nhuoc=Trung hòa while cach_cuc text says cực nhược |
| Customer impact | Internal inconsistency even before cross-domain |
| Evidence | pattern object fields |
| Suspected layer | Engine |
| Severity | **S2** |

---

## Counts

| Severity | n |
|----------|---|
| S0 | 2 |
| S1 | 5 |
| S2 | 5 |
| **Total** | **12** |
