# Changelog — Classical Knowledge Base

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
