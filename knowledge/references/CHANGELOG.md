# Knowledge Reference Library Changelog

**Module:** `knowledge/references`  
**Versioning:** Semantic (`MAJOR.MINOR.PATCH`)

---

## [1.0.0] — 2026-07-30

### Added

- Official machine-readable Reference Library layer:
  - `references.json`
  - `reference_index.json`
  - `REFERENCES_SPEC.md`
  - `citation_style.md`
  - `validation_rules.md`
  - `validate_references.py`
- Initial classical seed REF-000001 … REF-000007:
  - Huang Di Nei Jing
  - Zhou Yi
  - Yuan Hai Zi Ping
  - San Ming Tong Hui
  - Di Tian Sui
  - Zi Ping Zhen Quan
  - Qiong Tong Bao Jian
- Reports: `VALIDATION_REPORT.md`, `REFERENCE_COVERAGE_REPORT.md`, `TODO_REVIEW.md`

### Changed

- `README.md` updated to declare `references.json` as Reference ID Single Source of Truth
- Field name normalized to `identifier` (Foundation Freeze V1.0)

### Notes

- Legacy Markdown placeholders under `classics/` remain for coexistence
- ID assignment in V1.0 seed differs from legacy classics INDEX placeholders — see coverage/TODO reports
- Uncertain bibliographic metadata marked `TODO_REVIEW`
- Foundation Freeze candidate for V1.0

---

## Unreleased

_No unreleased changes recorded._
