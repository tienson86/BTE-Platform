# CURRENT_COMPOSER_AUDIT — Pre-CLL Implementation

| Field | Value |
|-------|-------|
| Date | 2026-08-12 |
| Scope | Identity / Career / Executive composers |
| Code changes at audit time | None |

---

## IdentityFeatureComposer

| Finding | Evidence |
|---------|----------|
| Direct claim-key rendering | `change` joins `plan.priorities` raw (`align_operating_role:…`) |
| identity_core pipe dump | WHO = `plan.identity_core` verbatim |
| support key leak | `balance:Nhâm` |
| Safe-template only | Sections are single raw strings, not consulting paragraphs |
| Missing required sections | No Environment / Pressure / Life lesson / Summary as specified for V1.2 |
| Weak action | Priorities dumped as keys |
| Weak transitions / memory | None |
| Jargon | Pattern label with “cực nhược / Thực/Thương” in identity_core |

## CareerFeatureComposer

| Finding | Evidence |
|---------|----------|
| AUTHORITY = generic “chuẩn mực” | `_authority` prefers OPERATING_STANDARDS even when primary is OUTPUT (RV-002) |
| Claim-key priorities/avoids | Joined raw plan keys |
| identity_core in STRUCTURE | Pipe dump |
| balance bare stem | `Nhâm` without lived framing |
| Forbidden token hack | Replaces “thu nhập” with `[không công bố]` mid-sentence (awkward) |
| Section title still “chuẩn mực” | AUTHORITY title |

## ExecutiveConsultingComposer

| Finding | Evidence |
|---------|----------|
| WHO/SUPPORTS dump plan slots | identity_core / `balance:Nhâm` |
| Partial key mapping | priorities/avoids partially mapped; WHO not |
| Concatenation risk | Nuance appended to limits; insight still theme labels |
| Closing | Insight + boilerplate — not memorable chart-specific line |
| “Bạn…” openings | Legacy fallback uses “Bạn mang…” |

## Shared

- No CLL runtime boundary
- No ConsultingParagraph structure
- No deterministic pattern selection by intent
- CASE-0001 endurance stitch already removed at CDR (good) — composers still leak keys

## Fix target (this implementation)

Wire all three composers through `applications/production/language/` without changing CDR or engines.
