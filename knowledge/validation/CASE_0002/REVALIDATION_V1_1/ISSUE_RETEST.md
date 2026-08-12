# ISSUE_RETEST — Original CASE-0002 Issues vs CDR V1.1

Source register: `../ISSUES.md` (ISS-001 … ISS-012).

Classifications: RESOLVED | IMPROVED | UNCHANGED | REGRESSED

| Issue | Severity (orig.) | Classification | Evidence (AFTER) |
|-------|------------------|----------------|------------------|
| ISS-001 Identity not generated | S0 | **RESOLVED** | `section_status.identity_report = AVAILABLE`; Identity body generated |
| ISS-002 Career not generated | S0 | **RESOLVED** | `section_status.career_report = AVAILABLE`; Career body generated |
| ISS-003 Strength “trung hòa” vs Pattern “cực nhược / Tòng Nhi” unexplained | S1 | **RESOLVED** | Customer-safe nuance in Identity/Executive LIMITS; CDR tensions populated; both signals kept |
| ISS-004 Executive insight CASE-0001 endurance/carry | S1 | **RESOLVED** | No “gánh thêm vô hạn” / endurance stitch; insight = Tòng + output |
| ISS-005 Jargon / opaque stems | S1 | **IMPROVED** | Enums/reason codes hidden; stems (Nhâm, Bính/Đinh, Thực/Thương) still in domain + claim-key surfaces |
| ISS-006 Conflict detector silent | S1 | **RESOLVED** | CDR `tensions[]` non-empty; relations include DEPENDENCY_OVERRIDE / DIFFERENT_SCOPE / CONDITIONAL_NUANCE (legacy integrator conflicts may still be empty — CDR is authoritative) |
| ISS-007 PRESSURE “chuẩn mực” vs Thương Quan | S1 | **IMPROVED** | Primary theme/operating = Thương Quan / output; Career AUTHORITY still emits chuẩn mực because SUPPORTING `OPERATING_STANDARDS` (Chính Quan secondary) |
| ISS-008 UG not translated to work/life actions | S2 | **IMPROVED** | Nhâm appears in claim plan + priorities; still stem-level, not lived career actions |
| ISS-009 DRAFT_KNOWLEDGE all domains | S2 | **UNCHANGED** | Knowledge status unchanged (validation diagnostics) |
| ISS-010 Master interpretation NOT_AVAILABLE | S2 | **UNCHANGED** | Policy: golden master only |
| ISS-011 Avoid list mismatched (gánh tải) | S2 | **RESOLVED** | Avoids: ordinary DM frame / suppress expression / overexertion — chart-fit |
| ISS-012 Pattern than_vuong_nhuoc “Trung hòa” vs “cực nhược” in label | S2 | **UNCHANGED** | Engine publish fields unchanged (out of CDR scope) |

### Counts

| Class | n |
|-------|---|
| RESOLVED | 6 |
| IMPROVED | 3 |
| UNCHANGED | 3 |
| REGRESSED | 0 |

### User-facing issue map (prompt list)

| Prompt issue | Class |
|--------------|-------|
| S0 Identity / Career not wired | RESOLVED |
| S1 Strength vs Pattern unexplained | RESOLVED |
| S1 Executive CASE-0001 endurance/carry | RESOLVED |
| S1 Thương Quan + generic “chuẩn mực” pressure | IMPROVED |
| S1 Jargon / opaque stems | IMPROVED |
