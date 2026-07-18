"""
Golden Dataset Validator

Chức năng:
- Kiểm tra cấu trúc output
- Kiểm tra kiểu dữ liệu
- Kiểm tra field bắt buộc
- Kiểm tra enum
- Kiểm tra range

Validator KHÔNG:
- So sánh với expected
- Sinh báo cáo
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import json


# ==========================================================
# Validation Error
# ==========================================================

@dataclass(slots=True)
class ValidationError:
    """
    Một lỗi validation.
    """

    field: str
    message: str
    value: Any


# ==========================================================
# Validator
# ==========================================================

class OutputValidator:
    """
    Validator cho Golden Dataset.
    """

    REQUIRED_FIELDS = {
        "chart",
        "strength",
        "pattern",
        "useful_god",
        "score",
        "sentences",
    }

    ENUM_FIELDS = {
        "strength": {
            "than_vuong",
            "than_nhuoc",
            "than_can_bang",
        },
        "useful_god": {
            "kim",
            "moc",
            "thuy",
            "hoa",
            "tho",
        },
    }

    SCORE_RANGE = (0, 100)

    def validate(self, data: dict[str, Any]) -> list[ValidationError]:
        """
        Validate toàn bộ output.
        """

        errors: list[ValidationError] = []

        errors.extend(self._validate_required(data))
        errors.extend(self._validate_types(data))
        errors.extend(self._validate_enum(data))
        errors.extend(self._validate_score(data))

        return errors

    # ======================================================

    def _validate_required(
        self,
        data: dict[str, Any],
    ) -> list[ValidationError]:

        errors = []

        for field in self.REQUIRED_FIELDS:

            if field not in data:

                errors.append(
                    ValidationError(
                        field=field,
                        message="Missing required field",
                        value=None,
                    )
                )

        return errors

    # ======================================================

    def _validate_types(
        self,
        data: dict[str, Any],
    ) -> list[ValidationError]:

        errors = []

        if "chart" in data and not isinstance(data["chart"], dict):

            errors.append(
                ValidationError(
                    "chart",
                    "Must be dict",
                    data["chart"],
                )
            )

        if "score" in data and not isinstance(data["score"], int):

            errors.append(
                ValidationError(
                    "score",
                    "Must be int",
                    data["score"],
                )
            )

        if "pattern" in data and not isinstance(data["pattern"], str):

            errors.append(
                ValidationError(
                    "pattern",
                    "Must be string",
                    data["pattern"],
                )
            )

        if "useful_god" in data and not isinstance(data["useful_god"], str):

            errors.append(
                ValidationError(
                    "useful_god",
                    "Must be string",
                    data["useful_god"],
                )
            )

        if "sentences" in data and not isinstance(data["sentences"], list):

            errors.append(
                ValidationError(
                    "sentences",
                    "Must be list",
                    data["sentences"],
                )
            )

        return errors

    # ======================================================

    def _validate_enum(
        self,
        data: dict[str, Any],
    ) -> list[ValidationError]:

        errors = []

        for field, values in self.ENUM_FIELDS.items():

            if field not in data:
                continue

            if data[field] not in values:

                errors.append(
                    ValidationError(
                        field,
                        f"Must be one of {sorted(values)}",
                        data[field],
                    )
                )

        return errors

    # ======================================================

    def _validate_score(
        self,
        data: dict[str, Any],
    ) -> list[ValidationError]:

        errors = []

        if "score" not in data:
            return errors

        score = data["score"]

        if not isinstance(score, int):
            return errors

        minimum, maximum = self.SCORE_RANGE

        if score < minimum or score > maximum:

            errors.append(
                ValidationError(
                    "score",
                    f"Must be between {minimum} and {maximum}",
                    score,
                )
            )

        return errors


# ==========================================================
# Helpers
# ==========================================================

def validate_file(path: Path) -> list[ValidationError]:
    """
    Validate một file JSON.
    """

    with path.open(
        "r",
        encoding="utf-8",
    ) as f:

        data = json.load(f)

    validator = OutputValidator()

    return validator.validate(data)


def validate_files(
    files: list[Path],
) -> dict[str, list[ValidationError]]:
    """
    Validate nhiều file.
    """

    result: dict[str, list[ValidationError]] = {}

    for file in files:

        result[file.stem] = validate_file(file)

    return result
