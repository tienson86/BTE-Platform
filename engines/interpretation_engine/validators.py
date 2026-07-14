"""
validators.py
==============

Kiểm tra dữ liệu đầu vào của Interpretation Engine.

Nhiệm vụ:
- Kiểm tra cấu trúc dữ liệu lá số.
- Kiểm tra các trường bắt buộc.
- Kiểm tra kiểu dữ liệu.
- Phát hiện dữ liệu không hợp lệ trước khi diễn giải.
"""

from typing import Any, Dict, List


class ValidationError(Exception):
    """Ngoại lệ khi dữ liệu không hợp lệ."""


class InterpretationValidator:

    REQUIRED_FIELDS = [
        "chart",
        "day_master",
        "month_branch",
        "strength",
        "useful_god",
    ]

    @classmethod
    def validate(cls, context: Dict[str, Any]) -> None:
        """
        Kiểm tra dữ liệu đầu vào.

        Raises:
            ValidationError
        """

        if context is None:
            raise ValidationError("Context không được để None.")

        if not isinstance(context, dict):
            raise ValidationError("Context phải là dict.")

        missing: List[str] = []

        for field in cls.REQUIRED_FIELDS:
            if field not in context:
                missing.append(field)

        if missing:
            raise ValidationError(
                f"Thiếu trường bắt buộc: {', '.join(missing)}"
            )

        if not isinstance(context["chart"], dict):
            raise ValidationError("chart phải là dict.")

        if not isinstance(context["strength"], str):
            raise ValidationError("strength phải là chuỗi.")

        if not isinstance(context["useful_god"], str):
            raise ValidationError("useful_god phải là chuỗi.")

    @classmethod
    def is_valid(cls, context: Dict[str, Any]) -> bool:
        try:
            cls.validate(context)
            return True
        except ValidationError:
            return False
