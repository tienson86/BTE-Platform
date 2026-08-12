# REMAINING_ISSUES — New Register (post CDR V1.1)

Resolved baseline issues are **not** carried forward.

Severity: S0 blocker · S1 high · S2 medium · S3 low

---

## RV-001 — Claim-plan keys leak into customer prose

| Field | Content |
|-------|---------|
| Severity | **S1** |
| Symptom | Customer Identity/Career/Executive show `balance:Nhâm`, `align_operating_role:…`, `avoid_*` keys, pipe-joined identity_core |
| Customer impact | Calculator / internal-tool feel; weak commercial polish |
| Suspected layer | COMPOSER |
| Evidence | `_summary_c2.json` identity_report / career_report / executive_consulting |
| Recommended owner | Feature composers (Identity / Career / Executive) |
| Fix category | Composer/prose mapping from claim plan → Vietnamese sentences |

## RV-002 — Career AUTHORITY still generic “chuẩn mực”

| Field | Content |
|-------|---------|
| Severity | **S1** |
| Symptom | Primary is Thương Quan/output, but Career AUTHORITY states chuẩn mực/trách nhiệm (from SUPPORTING OPERATING_STANDARDS / Chính Quan) |
| Customer impact | Dilutes output-led career story |
| Suspected layer | COMPOSER (+ theme salience for CAREER) |
| Evidence | career_report AUTHORITY section; themes include OPERATING_STANDARDS SUPPORTING |
| Recommended owner | CareerFeatureComposer / theme salience policy |
| Fix category | Composer priority rules for CAREER context |

## RV-003 — Nhâm / stems not lived into actions

| Field | Content |
|-------|---------|
| Severity | **S2** |
| Symptom | Balance = “Nhâm”; unfavorable Bính/Đinh remain opaque in domain text |
| Customer impact | Customer cannot act without BaZi literacy |
| Suspected layer | KNOWLEDGE / COMPOSER |
| Evidence | useful_god conclusion; executive DIRECTION “Nhâm” |
| Recommended owner | Useful God knowledge pack + composers |
| Fix category | Knowledge + prose translation |

## RV-004 — Pattern field internal wording clash remains

| Field | Content |
|-------|---------|
| Severity | **S2** |
| Symptom | `than_vuong_nhuoc=Trung hòa` while `cach_cuc` contains “cực nhược” |
| Customer impact | Advanced readers may still see inconsistency inside Pattern domain |
| Suspected layer | ENGINE (publish wording) |
| Evidence | engine.pattern fields unchanged vs baseline |
| Recommended owner | Pattern engine / publish contract |
| Fix category | Runtime data / engine publish clarification (policy-backed) |

## RV-005 — Master Consulting still NOT_AVAILABLE

| Field | Content |
|-------|---------|
| Severity | **S2** |
| Symptom | Package C master markdown not generated for non-golden cases |
| Customer impact | Full Advisor Edition not deliverable |
| Suspected layer | FEATURE_PACKAGING / POLICY |
| Evidence | section_status.master_interpretation = NOT_AVAILABLE |
| Recommended owner | Packaging / master composition product |
| Fix category | Feature packaging (not CASE-0002 special-case) |

## RV-006 — Emotional / lived Identity depth thin

| Field | Content |
|-------|---------|
| Severity | **S2** |
| Symptom | Identity answers structure but not “felt life” (environment, memory, resonance) |
| Customer impact | Package A not yet sellable at commercial prose bar |
| Suspected layer | FEATURE_PACKAGING / COMPOSER |
| Evidence | CUSTOMER_REVIEW Identity scores |
| Recommended owner | Identity feature packaging |
| Fix category | Composer + packaging templates |

---

## Counts

| Severity | n |
|----------|---|
| S0 | 0 |
| S1 | 2 |
| S2 | 4 |
| **Total** | **6** |
