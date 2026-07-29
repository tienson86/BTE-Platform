# CHANGELOG.md

> Module: Knowledge Framework
>
> Component: Reference Examples
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Changelog
>
> BTE Platform

---

# Changelog

Tài liệu này ghi lại toàn bộ thay đổi đối với thư mục:

```
knowledge/docs/reference_examples/
```

Theo chính sách:

- VERSIONING_POLICY.md
- METADATA_STANDARD.md

---

## [1.0.0] - 2026-07-29

### Added

Khởi tạo Reference Examples V1.0.

Package documents:

```
README.md
REFERENCE_EXAMPLE_CHECKLIST.md
CHANGELOG.md
MANIFEST.json
```

Directories:

```
rule/
context/
result/
pipeline/
validation/
metadata/
```

Rule examples:

```
rule/rule_complete_v1.json
rule/rule_minimal_v1.json
rule/rule_invalid_missing_id_v1.json
rule/rule_invalid_bad_version_v1.json
rule/rule_invalid_unknown_enum_v1.json
```

Context examples:

```
context/context_complete_v1.json
context/context_minimal_v1.json
```

Result examples:

```
result/result_complete_v1.json
result/result_minimal_v1.json
```

Pipeline examples:

```
pipeline/pipeline_complete_v1.md
pipeline/pipeline_minimal_v1.md
```

Validation examples:

```
validation/validation_complete_v1.json
validation/validation_minimal_v1.json
```

Metadata examples:

```
metadata/metadata_complete_v1.json
metadata/metadata_minimal_v1.json
```

### Governance

Reference Examples được xác định là:

- Canonical Reference
- Golden Dataset Source
- Documentation Reference
- AI Training Reference

Mọi example sử dụng:

- version: 1.0.0
- schema_version: 1.0.0
- origin: reference_example
- author: BTE

Invalid examples (một lỗi duy nhất mỗi file):

- `rule_invalid_missing_id_v1.json` — thiếu trường `id`
- `rule_invalid_bad_version_v1.json` — `metadata.version` không đúng semver (`v1.0.0`)
- `rule_invalid_unknown_enum_v1.json` — `priority.level` = `ultra_high` (enum không hợp lệ)

### Validation

Áp dụng:

- Validation Level 1–5
- JSON Style Guide
- Metadata Standard
- Naming Convention
- Versioning Policy

### Fixed

- Chuyển toàn bộ file JSON sang LF line endings (JSON_STYLE_GUIDE.md).
- Sửa `validation/validation_complete_v1.json`: `total_objects` = 15, `errors` = 3, bao phủ đủ 15 example trong MANIFEST.json.
- Sửa invalid rule examples: một lỗi duy nhất mỗi file, rule code duy nhất, prefix ATT cho attack domain (`rule_invalid_bad_version_v1.json`).

---

## Versioning Policy

### MAJOR

Breaking changes.

### MINOR

Thêm Example mới.

### PATCH

Sửa Metadata.

Sửa Documentation.

Sửa lỗi nhỏ.

---

## Future Roadmap

Planned:

- Advanced Rule Examples
- Combination Rule Examples
- Priority Examples
- Context Extensions
- Result Extensions
- Validation Failure Library
- AI Evaluation Dataset
