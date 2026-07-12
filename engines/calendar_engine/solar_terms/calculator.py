"""
===============================================================================
Calendar Engine - Solar Terms Calculator
-------------------------------------------------------------------------------
Bộ tính Tiết Khí.

Hiện tại module này chỉ chịu trách nhiệm:

    1. Tính kinh độ Mặt Trời.
    2. Xác định Tiết Khí.
    3. Xác định Địa Chi tháng.
    4. Trả về SolarTermContext.

Thuật toán thiên văn sẽ được triển khai theo Jean Meeus.
===============================================================================
"""

from __future__ import annotations

from datetime import datetime

from .models import (
    LiChunResult,
    MonthBranchResult,
    SolarLongitude,
    SolarTerm,
    SolarTermContext,
    SolarTermResult,
)

SOLAR_TERMS = (
    ("Lập Xuân", 315.0, "Dần"),
    ("Vũ Thủy", 330.0, "Dần"),
    ("Kinh Trập", 345.0, "Mão"),
    ("Xuân Phân",   0.0, "Mão"),
    ("Thanh Minh", 15.0, "Thìn"),
    ("Cốc Vũ",     30.0, "Thìn"),
    ("Lập Hạ",     45.0, "Tỵ"),
    ("Tiểu Mãn",   60.0, "Tỵ"),
    ("Mang Chủng", 75.0, "Ngọ"),
    ("Hạ Chí",     90.0, "Ngọ"),
    ("Tiểu Thử",  105.0, "Mùi"),
    ("Đại Thử",   120.0, "Mùi"),
    ("Lập Thu",   135.0, "Thân"),
    ("Xử Thử",    150.0, "Thân"),
    ("Bạch Lộ",   165.0, "Dậu"),
    ("Thu Phân",  180.0, "Dậu"),
    ("Hàn Lộ",    195.0, "Tuất"),
    ("Sương Giáng",210.0,"Tuất"),
    ("Lập Đông",  225.0, "Hợi"),
    ("Tiểu Tuyết",240.0, "Hợi"),
    ("Đại Tuyết", 255.0, "Tý"),
    ("Đông Chí",  270.0, "Tý"),
    ("Tiểu Hàn",  285.0, "Sửu"),
    ("Đại Hàn",   300.0, "Sửu"),
)


class SolarTermCalculator:
    """
    Calculator Tiết Khí.
    """

    def calculate(
        self,
        birth_datetime: datetime,
    ) -> SolarTermContext:
        """
        TODO:
            Giai đoạn V1:
                - Kết nối Astronomy Engine.
                - Tính Solar Longitude.
                - Xác định Tiết Khí.
        """
        raise NotImplementedError(
            "Chưa triển khai thuật toán thiên văn."
        )
