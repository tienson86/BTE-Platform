"""
Migrate legacy Golden Dataset expected JSON files to V1 (InterpretationReport) shape.

Legacy wrapper:

    case_id, engine_version, generated_at, expected_result, ...

V1 expected output:

    success, text, sections
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent

EXPECTED_DIR = REPO_ROOT / "tests" / "golden_dataset" / "expected"
OUTPUT_DIR = REPO_ROOT / "tests" / "golden_dataset" / "expected_v2"

V1_KEYS = frozenset({"success", "text", "sections"})
LEGACY_MARKER = "expected_result"


@dataclass(slots=True)
class MigrationSummary:
    """Kết quả chạy migration."""

    total_files: int = 0
    migrated_legacy: int = 0
    copied_v1: int = 0
    skipped_invalid: int = 0
    errors: list[str] = field(default_factory=list)


def is_legacy_schema(data: Any) -> bool:
    """
    Nhận diện file expected bọc legacy (có expected_result).
    """

    return isinstance(data, dict) and LEGACY_MARKER in data


def is_v1_schema(data: Any) -> bool:
    """
    Nhận diện file đã ở dạng V1 (success, text, sections).
    """

    if not isinstance(data, dict):
        return False

    if LEGACY_MARKER in data:
        return False

    return V1_KEYS.issubset(data.keys())


def legacy_to_v1(data: dict[str, Any]) -> dict[str, Any]:
    """
    Chuyển expected_result legacy sang dict tương thích JSON V1.
    """

    expected = data.get(LEGACY_MARKER)
    if not isinstance(expected, dict):
        expected = {}

    status = expected.get("status")
    success = status == "success" if isinstance(status, str) else bool(status)

    interpretation = expected.get("interpretation")
    text = ""
    if isinstance(interpretation, dict):
        summary = interpretation.get("summary")
        if isinstance(summary, str):
            text = summary

    return {
        "success": success,
        "text": text,
        "sections": [],
    }


def normalize_to_v1(data: Any) -> dict[str, Any] | None:
    """
    Trả về payload V1 hoặc None nếu không nhận diện được schema.
    """

    if is_legacy_schema(data):
        return legacy_to_v1(data)

    if is_v1_schema(data):
        return {
            "success": bool(data["success"]),
            "text": data["text"] if isinstance(data["text"], str) else str(data["text"]),
            "sections": data["sections"] if isinstance(data["sections"], list) else [],
        }

    return None


def write_v1_file(target: Path, payload: dict[str, Any]) -> None:
    """
    Ghi file JSON V1 (không ghi đè thư mục expected gốc).
    """

    target.parent.mkdir(parents=True, exist_ok=True)

    with target.open("w", encoding="utf-8") as handle:
        json.dump(
            payload,
            handle,
            ensure_ascii=False,
            indent=4,
            sort_keys=True,
        )


def migrate_expected_dataset() -> MigrationSummary:
    """
    Đọc tests/golden_dataset/expected/*.json, ghi bản V1 vào expected_v2/.
    """

    summary = MigrationSummary()

    if not EXPECTED_DIR.is_dir():
        summary.errors.append(f"Expected directory not found: {EXPECTED_DIR}")
        return summary

    json_files = sorted(EXPECTED_DIR.glob("*.json"))
    summary.total_files = len(json_files)

    for source_path in json_files:
        try:
            with source_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            summary.skipped_invalid += 1
            summary.errors.append(f"{source_path.name}: read failed — {exc}")
            continue

        v1_payload = normalize_to_v1(data)
        if v1_payload is None:
            summary.skipped_invalid += 1
            summary.errors.append(
                f"{source_path.name}: unknown schema (not legacy or V1)",
            )
            continue

        dest_path = OUTPUT_DIR / source_path.name
        write_v1_file(dest_path, v1_payload)

        if is_legacy_schema(data):
            summary.migrated_legacy += 1
        else:
            summary.copied_v1 += 1

    return summary


def print_summary(summary: MigrationSummary) -> None:
    """
    In báo cáo migration ra stdout.
    """

    print("Golden Dataset expected migration")
    print(f"  Source : {EXPECTED_DIR}")
    print(f"  Output : {OUTPUT_DIR}")
    print(f"  Total files      : {summary.total_files}")
    print(f"  Migrated (legacy): {summary.migrated_legacy}")
    print(f"  Copied (already V1): {summary.copied_v1}")
    print(f"  Skipped / invalid: {summary.skipped_invalid}")

    if summary.errors:
        print("  Errors:")
        for message in summary.errors:
            print(f"    - {message}")


def main() -> int:
    """Entry point."""

    summary = migrate_expected_dataset()
    print_summary(summary)

    if summary.errors and summary.migrated_legacy + summary.copied_v1 == 0:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
