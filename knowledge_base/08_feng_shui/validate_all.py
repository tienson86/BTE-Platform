"""
Batch validator for 08_feng_shui/01_gua.

Chạy trực tiếp:
    python knowledge_base/08_feng_shui/validate_all.py

Trả về exit code 0 nếu tất cả file hợp lệ, 1 nếu có lỗi.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).parent))
    from validator import ValidationResult, load_schema_fields, validate_file
else:  # pragma: no cover - import khi dùng như package
    from .validator import ValidationResult, load_schema_fields, validate_file

GUA_DIR = Path(__file__).with_name("01_gua")


def run(gua_dir: Path = GUA_DIR) -> list[ValidationResult]:
    """Validate tất cả file *.json trong thư mục gua."""
    schema_fields = load_schema_fields()
    results: list[ValidationResult] = []
    for file_path in sorted(gua_dir.glob("*.json")):
        results.append(validate_file(file_path, schema_fields))
    return results


def main() -> int:
    """Chạy validate và in báo cáo; trả exit code."""
    results = run()
    if not results:
        print("[WARN] Không tìm thấy file gua nào trong 01_gua/")
        return 1

    failed = 0
    for result in results:
        name = Path(result.path).name
        if result.ok:
            print(f"[OK]   {name}")
        else:
            failed += 1
            print(f"[FAIL] {name}")
            for err in result.errors:
                print(f"        - {err}")

    total = len(results)
    print(f"\nSummary: {total - failed}/{total} file hợp lệ.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
