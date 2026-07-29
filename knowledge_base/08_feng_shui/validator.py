"""
Validator for 08_feng_shui Gua knowledge files (Framework FS-01A).

Kiểm tra:
- schema (đúng bộ field theo schema.json)
- field bắt buộc
- kiểu dữ liệu
- thiếu field
- field thừa

Không kiểm tra nội dung chuyên môn (do đội chuyên môn nhập sau).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SCHEMA_FILE = Path(__file__).with_name("schema.json")

# Kiểu dữ liệu mong đợi cho từng field (str | int | list).
SCALAR_STR_FIELDS: tuple[str, ...] = (
    "id",
    "name",
    "group",
    "element",
    "direction",
)
SCALAR_INT_FIELDS: tuple[str, ...] = ("number",)
ARRAY_FIELDS: tuple[str, ...] = (
    "aliases",
    "keywords",
    "overview",
    "personality",
    "strengths",
    "weaknesses",
    "career",
    "wealth",
    "relationship",
    "family",
    "health",
    "learning",
    "leadership",
    "communication",
    "suitable_jobs",
    "unsuitable_jobs",
    "development_advice",
    "notes",
    "references",
)

VALID_NUMBERS: frozenset[int] = frozenset({1, 2, 3, 4, 6, 7, 8, 9})
VALID_GROUPS: frozenset[str] = frozenset({"Đông Tứ Trạch", "Tây Tứ Trạch"})


@dataclass(slots=True)
class ValidationResult:
    """Kết quả kiểm tra một file."""

    path: str
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True khi không có lỗi."""
        return not self.errors


def load_schema_fields() -> list[str]:
    """Đọc danh sách field bắt buộc từ schema.json (giữ thứ tự khai báo)."""
    schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
    return list(schema.get("properties", {}).keys())


def _check_types(data: dict[str, Any], result: ValidationResult) -> None:
    for key in SCALAR_STR_FIELDS:
        if key in data and not isinstance(data[key], str):
            result.errors.append(f"field '{key}' phải là string")
    for key in SCALAR_INT_FIELDS:
        # bool là subclass của int → loại trừ tường minh
        if key in data and (not isinstance(data[key], int) or isinstance(data[key], bool)):
            result.errors.append(f"field '{key}' phải là integer")
    for key in ARRAY_FIELDS:
        if key in data:
            value = data[key]
            if not isinstance(value, list):
                result.errors.append(f"field '{key}' phải là array")
            elif not all(isinstance(item, str) for item in value):
                result.errors.append(f"field '{key}' chỉ được chứa string")


def _check_enums(data: dict[str, Any], result: ValidationResult) -> None:
    if isinstance(data.get("number"), int) and not isinstance(data["number"], bool):
        if data["number"] not in VALID_NUMBERS:
            result.errors.append(
                f"field 'number' = {data['number']} không hợp lệ (cho phép {sorted(VALID_NUMBERS)})"
            )
    if isinstance(data.get("group"), str) and data["group"] not in VALID_GROUPS:
        result.errors.append(
            f"field 'group' = {data['group']!r} không hợp lệ (cho phép {sorted(VALID_GROUPS)})"
        )
    if isinstance(data.get("id"), str) and not data["id"].startswith("gua_"):
        result.errors.append("field 'id' phải bắt đầu bằng 'gua_'")


def validate_data(data: Any, path: str, schema_fields: list[str] | None = None) -> ValidationResult:
    """
    Kiểm tra một object gua theo schema.

    Args:
        data: nội dung JSON đã parse.
        path: nhãn hiển thị (đường dẫn file).
        schema_fields: danh sách field chuẩn; None → đọc từ schema.json.

    Returns:
        ValidationResult với danh sách lỗi (rỗng nếu hợp lệ).
    """
    fields = schema_fields if schema_fields is not None else load_schema_fields()
    result = ValidationResult(path=path)

    if not isinstance(data, dict):
        result.errors.append("root phải là JSON object")
        return result

    expected = set(fields)
    actual = set(data.keys())

    for missing in sorted(expected - actual):
        result.errors.append(f"thiếu field '{missing}'")
    for extra in sorted(actual - expected):
        result.errors.append(f"field thừa '{extra}'")

    _check_types(data, result)
    _check_enums(data, result)
    return result


def validate_file(file_path: Path, schema_fields: list[str] | None = None) -> ValidationResult:
    """Đọc và kiểm tra một file JSON gua."""
    fields = schema_fields if schema_fields is not None else load_schema_fields()
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return ValidationResult(path=str(file_path), errors=[f"không đọc/parse được JSON: {exc}"])
    return validate_data(data, str(file_path), fields)
