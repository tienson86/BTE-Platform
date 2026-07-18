"""
Golden Dataset Comparator

Chức năng:
- So sánh expected và actual
- Trả về danh sách khác biệt

Comparator KHÔNG:
- Validate dữ liệu
- Sinh báo cáo
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


# ==========================================================
# Directories
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

EXPECTED_DIR = BASE_DIR / "expected"
ACTUAL_DIR = BASE_DIR / "actual"


# ==========================================================
# Difference
# ==========================================================

@dataclass(slots=True)
class Difference:
    """
    Một khác biệt giữa expected và actual.
    """

    field: str
    expected: Any
    actual: Any


# ==========================================================
# Helpers
# ==========================================================

def load_json(path: Path) -> dict[str, Any]:
    """
    Đọc file JSON.
    """

    with path.open(
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


# ==========================================================
# Comparator
# ==========================================================

class OutputComparator:
    """
    So sánh hai output.
    """

    def compare(
        self,
        expected: dict[str, Any],
        actual: dict[str, Any],
    ) -> list[Difference]:

        differences: list[Difference] = []

        self._compare_dict(
            "",
            expected,
            actual,
            differences,
        )

        return differences

    # ======================================================

    def _compare_dict(
        self,
        prefix: str,
        expected: Any,
        actual: Any,
        differences: list[Difference],
    ) -> None:

        # dict
        if isinstance(expected, dict) and isinstance(actual, dict):

            keys = sorted(
                set(expected.keys()) | set(actual.keys())
            )

            for key in keys:

                field = f"{prefix}.{key}" if prefix else key

                self._compare_dict(
                    field,
                    expected.get(key),
                    actual.get(key),
                    differences,
                )

            return

        # list
        if isinstance(expected, list) and isinstance(actual, list):

            length = max(len(expected), len(actual))

            for i in range(length):

                field = f"{prefix}[{i}]"

                e = expected[i] if i < len(expected) else None
                a = actual[i] if i < len(actual) else None

                self._compare_dict(
                    field,
                    e,
                    a,
                    differences,
                )

            return

        # primitive
        if expected != actual:

            differences.append(
                Difference(
                    field=prefix,
                    expected=expected,
                    actual=actual,
                )
            )


# ==========================================================
# Public API
# ==========================================================

def compare_case(
    case_name: str,
) -> list[Difference]:
    """
    So sánh một test case.
    """

    expected_file = EXPECTED_DIR / f"{case_name}.json"
    actual_file = ACTUAL_DIR / f"{case_name}.json"

    expected = load_json(expected_file)
    actual = load_json(actual_file)

    comparator = OutputComparator()

    return comparator.compare(
        expected,
        actual,
    )


def compare_all_cases() -> dict[str, list[Difference]]:
    """
    So sánh toàn bộ Golden Dataset.
    """

    result: dict[str, list[Difference]] = {}

    for expected_file in sorted(EXPECTED_DIR.glob("*.json")):

        case_name = expected_file.stem

        result[case_name] = compare_case(case_name)

    return result
