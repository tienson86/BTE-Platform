# Knowledge Base Validation Report

- Generated: `2026-07-27 04:20:32 UTC`
- Root: `knowledge_base/`
- Status: **PASS**
- JSON files scanned: **11**
- Data files: **9**
- Schema files: **1**
- Metadata files: **1**
- Errors: **0**
- Warnings: **3**
- Info: **0**

## Checks

| Check | Description |
|-------|-------------|
| `json_format` | File parse được như JSON |
| `utf8` | Encoding UTF-8, không BOM |
| `schema` | Khớp schema.json của module |
| `duplicate_id` | Không trùng `id` giữa các file |
| `duplicate_alias` | Không trùng `aliases` |
| `empty_required` | Field bắt buộc scalar không rỗng |
| `references` | Mục `references` hợp lệ / tồn tại nếu là path |

## File inventory

| File | Kind | Schema |
|------|------|--------|
| `knowledge_base/08_feng_shui/01_gua/can.json` | data | `knowledge_base/08_feng_shui/schema.json` |
| `knowledge_base/08_feng_shui/01_gua/can_gen.json` | data | `knowledge_base/08_feng_shui/schema.json` |
| `knowledge_base/08_feng_shui/01_gua/chan.json` | data | `knowledge_base/08_feng_shui/schema.json` |
| `knowledge_base/08_feng_shui/01_gua/doai.json` | data | `knowledge_base/08_feng_shui/schema.json` |
| `knowledge_base/08_feng_shui/01_gua/kham.json` | data | `knowledge_base/08_feng_shui/schema.json` |
| `knowledge_base/08_feng_shui/01_gua/khon.json` | data | `knowledge_base/08_feng_shui/schema.json` |
| `knowledge_base/08_feng_shui/01_gua/ly.json` | data | `knowledge_base/08_feng_shui/schema.json` |
| `knowledge_base/08_feng_shui/01_gua/ton.json` | data | `knowledge_base/08_feng_shui/schema.json` |
| `knowledge_base/08_feng_shui/examples/sample.json` | data | `knowledge_base/08_feng_shui/schema.json` |
| `knowledge_base/08_feng_shui/metadata.json` | metadata | `—` |
| `knowledge_base/08_feng_shui/schema.json` | schema | `—` |

## Summary by check

| Check | Errors | Warnings |
|-------|--------|----------|
| `json_format` (OK) | 0 | 0 |
| `utf8` (OK) | 0 | 0 |
| `schema` (OK) | 0 | 0 |
| `duplicate_id` (OK) | 0 | 0 |
| `duplicate_alias` (OK) | 0 | 0 |
| `empty_required` (WARN) | 0 | 3 |
| `references` (OK) | 0 | 0 |

## Findings

| Severity | Check | Path | Message |
|----------|-------|------|---------|
| warning | `empty_required` | `knowledge_base/08_feng_shui/examples/sample.json` | field bắt buộc 'direction' đang rỗng |
| warning | `empty_required` | `knowledge_base/08_feng_shui/examples/sample.json` | field bắt buộc 'element' đang rỗng |
| warning | `empty_required` | `knowledge_base/08_feng_shui/examples/sample.json` | field bắt buộc 'name' đang rỗng |

## Policy

- Tool **chỉ đọc** `knowledge_base/`.
- **Không** sửa dữ liệu nguồn.
- Report được ghi đè mỗi lần chạy tại `knowledge_base/validation_report.md`.
