# Changelog — Classical Knowledge Base

## 0.3.1 (2026-08-08)

### Changed / Added

- Sprint C: **Career Selection Assessment** completion in `22_domain01_career_business.csv`.
- SEL pack: 11 units under `CAP-D1-CA-SEL` / wave `W-D01-C-SEL` (direction → 90-day plan).
- KU-CN-LE-000001 and KU-AC-BU-000001 retained unchanged (other capabilities).

### SEL units

| Id | Title |
|----|-------|
| KU-CN-CA-000001 | Career Work Direction |
| KU-CN-CA-000010 | Career Environment Fit |
| KU-CN-CA-000011 | Career Organizational Role |
| KU-CN-CA-000012 | Leadership vs Specialist Posture |
| KU-CN-CA-000013 | Employment vs Entrepreneurship Posture |
| KU-CN-CA-000014 | Career Competitive Advantages |
| KU-RK-CA-000010 | Career Selection Primary Risks |
| KU-MT-CA-000010 | Career Selection Mitigation |
| KU-CN-CA-000015 | Career Development Priorities |
| KU-CN-CA-000016 | Career Decision Timing Light |
| KU-AC-CA-000001 | Career 90-Day Action Plan |

### Notes

- Wave 1.1 unchanged. No runtime. No Promotion/Leadership/Partnership/Management packs.

## 0.3.0 (2026-08-08)

### Added

- Domain 01 Career & Business **P0** Knowledge Units in `22_domain01_career_business.csv` (exactly **4** units).
- Additive Domain columns: `capability_id`, `decision_ids`, `executive_summary_support`, `recommendation_support`, `decision_support`, `traceability`.

### Units (Domain 01 P0)

| Id | Title | Capability |
|----|-------|------------|
| KU-CN-CA-000001 | Career Work Direction | CAP-D1-CA-SEL |
| KU-AC-CA-000001 | Career Role-Fit Next Step | CAP-D1-CA-SEL / CAP-D1-CA-DEV |
| KU-CN-LE-000001 | Leadership Style Light | CAP-D1-CA-LED |
| KU-AC-BU-000001 | Employment vs Independent Posture | CAP-D1-BU-ENP |

### Notes

- Wave 1.1 (`21_knowledge_units.csv`) **unchanged**.
- No P1/P2 Domain units in this release.
- Production Adapter wiring of `22_*.csv` is a follow-up (content authored only).

## 0.2.1 (2026-08-08)

### Changed

- EPIC 7 Sprint B P0 revision of Wave 1.1 units in `21_knowledge_units.csv` (same five ids).
- Versions bumped to `1.0.1`; content status set to `approved` (Publish still Product-owned).
- Commercial label language, Weakness→Risk→Mitigation→Opportunity arc, mitigation-first recommendation.

### Units (Golden Baseline V1 candidate)

| Id | Title | Version |
|----|-------|---------|
| KU-ID-001 | Identity Core | 1.0.1 |
| KU-ST-001 | Strength Core | 1.0.1 |
| KU-WK-001 | Weakness Core | 1.0.1 |
| KU-UG-001 | Useful God Core | 1.0.1 |
| KU-RC-001 | Core Recommendation | 1.0.1 |

### Notes

- No new Knowledge Units; no Wave 1.2.
- Schema / ids / narrative targets / primary·secondary usage unchanged.
- Companion: commercial band labels + weakness dedupe in commercial knowledge signal projection.

## 0.2.0 (2026-08-08)

### Added

- Wave 1.1 core Commercial Knowledge Units in `21_knowledge_units.csv` (exactly **5** units).
- Extended logical schema file for Knowledge Units (additive; does not alter columns of `01`–`20`).

### Units (awaiting review)

| Id | Title |
|----|-------|
| KU-ID-001 | Identity Core |
| KU-ST-001 | Strength Core |
| KU-WK-001 | Weakness Core |
| KU-UG-001 | Useful God Core |
| KU-RC-001 | Core Recommendation |

### Notes

- No calculation engines modified.
- No runtime wiring in this wave.
- Review status: `awaiting_review` — not production-Published until approval.

## 0.1.0 (2026-08-02)

### Added

- Created `database/20_knowledge/` foundation for Epic 03 Milestone 01.
- Standardized schema across 20 CSV topic files (header only; no content rows).
- Added `README.md`, `CHANGELOG.md`, and `COVERAGE.md`.

### Schema

```text
id,topic,keyword,condition,classical_text,modern_interpretation,priority,confidence,reference
```

### Notes

- Content population is deferred to later milestones.
- No calculation engines were modified.
