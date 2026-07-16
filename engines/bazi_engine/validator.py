"""
BTE Platform
Bazi Engine Validator

Kiểm tra dữ liệu đầu vào và đầu ra của Bazi Engine.
"""

from __future__ import annotations

from typing import Any

from .models import (
    BaziContext,
    BaziResult,
    FourPillars,
    Pillar,
)

from .exceptions import (
    BaziValidationError,
    InvalidBirthDataError,
    InvalidPillarError,
)

from engines.core.enums import (
    Operation,
)


class BaziValidator:
    """
    Validator của Bazi Engine.
    """

    # ======================================================
    # Context
    # ======================================================

    def validate_context(
        self,
        context: BaziContext,
    ) -> None:
        """
        Kiểm tra BaziContext.
        """

        if context is None:
            raise BaziValidationError(
                "BaziContext không được để trống."
            )

        self.validate_operation(context.operation)

        if context.four_pillars is not None:
            self.validate_four_pillars(
                context.four_pillars
            )

    # ======================================================
    # Operation
    # ======================================================

    def validate_operation(
        self,
        operation: Any,
    ) -> None:
        """
        Kiểm tra loại tác vụ.
        """

        if isinstance(operation, Operation):
            return

        try:
            Operation(operation)
        except Exception:
            raise BaziValidationError(
                f"Operation không hợp lệ: {operation}"
            )

    # ======================================================
    # Four Pillars
    # ======================================================

    def validate_four_pillars(
        self,
        pillars: FourPillars,
    ) -> None:

        if not isinstance(
            pillars,
            FourPillars,
        ):
            raise InvalidPillarError(
                "Sai kiểu dữ liệu FourPillars."
            )

        self.validate_pillar(pillars.year)

        self.validate_pillar(pillars.month)

        self.validate_pillar(pillars.day)

        self.validate_pillar(pillars.hour)

    # ======================================================
    # Pillar
    # ======================================================

    def validate_pillar(
        self,
        pillar: Pillar,
    ) -> None:

        if not isinstance(
            pillar,
            Pillar,
        ):
            raise InvalidPillarError(
                "Sai kiểu dữ liệu Pillar."
            )

        if pillar.stem is None:
            raise InvalidPillarError(
                "Thiếu Heavenly Stem."
            )

        if pillar.branch is None:
            raise InvalidPillarError(
                "Thiếu Earthly Branch."
            )

    # ======================================================
    # Birth Data
    # ======================================================

    def validate_birth_data(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
    ) -> None:

        if year <= 0:
            raise InvalidBirthDataError(
                "Năm sinh không hợp lệ."
            )

        if month < 1 or month > 12:
            raise InvalidBirthDataError(
                "Tháng sinh không hợp lệ."
            )

        if day < 1 or day > 31:
            raise InvalidBirthDataError(
                "Ngày sinh không hợp lệ."
            )

        if hour < 0 or hour > 23:
            raise InvalidBirthDataError(
                "Giờ sinh không hợp lệ."
            )

    # ======================================================
    # Result
    # ======================================================

    def validate_result(
        self,
        result: BaziResult,
    ) -> None:

        if not isinstance(
            result,
            BaziResult,
        ):
            raise BaziValidationError(
                "Sai kiểu dữ liệu BaziResult."
            )

        if result.success:

            if result.four_pillars is None:
                raise BaziValidationError(
                    "Thiếu Four Pillars."
                )

    # ======================================================
    # Generic
    # ======================================================

    @staticmethod
    def ensure_not_none(
        value: Any,
        name: str,
    ) -> None:

        if value is None:
            raise BaziValidationError(
                f"{name} không được để trống."
            )

    @staticmethod
    def ensure_positive(
        value: float,
        name: str,
    ) -> None:

        if value < 0:
            raise BaziValidationError(
                f"{name} phải >= 0."
            )
