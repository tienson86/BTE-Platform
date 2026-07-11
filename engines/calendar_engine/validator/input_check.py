"""
=========================================================
BTE PLATFORM
Calendar Engine

File:
    input_validator.py

Version:
    1.0

Author:
    BTE Platform

Description:
    Validate input data before Calendar Engine processing.

=========================================================
"""

from datetime import datetime


class InputValidator:
    """
    Kiểm tra dữ liệu đầu vào của Calendar Engine.
    """

    REQUIRED_FIELDS = [
        "solar_date",
        "solar_time",
        "timezone"
    ]


    def execute(self, context):

        input_data = context.get("input", {})

        self.validate_required(input_data)

        self.validate_date(input_data)

        self.validate_time(input_data)

        self.validate_timezone(input_data)

        context["validated"] = True

        return context


    # ====================================================

    # REQUIRED

    # ====================================================

    def validate_required(self, data):

        for field in self.REQUIRED_FIELDS:

            if field not in data:

                raise ValueError(
                    f"Missing required field: {field}"
                )


    # ====================================================

    # DATE

    # ====================================================

    def validate_date(self, data):

        value = data["solar_date"]

        try:

            datetime.strptime(
                value,
                "%d/%m/%Y"
            )

        except Exception:

            raise ValueError(
                "Invalid solar_date format (dd/MM/yyyy)"
            )


    # ====================================================

    # TIME

    # ====================================================

    def validate_time(self, data):

        value = data["solar_time"]

        try:

            datetime.strptime(
                value,
                "%H:%M"
            )

        except Exception:

            raise ValueError(
                "Invalid solar_time format (HH:mm)"
            )


    # ====================================================

    # TIMEZONE

    # ====================================================

    def validate_timezone(self, data):

        timezone = data["timezone"]

        if timezone is None:

            raise ValueError(
                "Timezone is required."
            )

        if len(timezone.strip()) == 0:

            raise ValueError(
                "Timezone cannot be empty."
            )
