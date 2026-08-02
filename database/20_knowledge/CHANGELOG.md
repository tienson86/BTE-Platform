# Changelog — Classical Knowledge Base

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
