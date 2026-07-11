"""
=========================================================
BTE PLATFORM

Calendar Algorithm

File:
    jdn_to_lunar.py

Version:
    1.0

Description:
    Convert Julian Day Number to Lunar Date

=========================================================
"""


class JDNToLunar:
    """
    Chuyển Julian Day Number sang Âm lịch.

    Phiên bản:
        v1.0

    Ghi chú:
        Thuật toán chuyển đổi sẽ sử dụng các
        hàm thiên văn của Calendar Engine.
    """

    @staticmethod
    def convert(jdn, timezone=7):

        new_moon = JDNToLunar.get_new_moon_day(jdn, timezone)

        lunar_month11 = JDNToLunar.get_lunar_month11(
            new_moon,
            timezone
        )

        leap_month = JDNToLunar.get_leap_month_offset(
            lunar_month11,
            timezone
        )

        result = {

            "day": None,

            "month": None,

            "year": None,

            "leap": False,

            "new_moon": new_moon,

            "month11": lunar_month11,

            "leap_offset": leap_month

        }

        return result


    # ====================================================

    # NEW MOON

    # ====================================================

    @staticmethod
    def get_new_moon_day(jdn, timezone):

        """
        Xác định Sóc gần nhất.

        Thuật toán sẽ hiện thực
        trong Lunar Astronomy Library.
        """

        return None


    # ====================================================

    # MONTH 11

    # ====================================================

    @staticmethod
    def get_lunar_month11(new_moon, timezone):

        """
        Xác định tháng 11 âm lịch.
        """

        return None


    # ====================================================

    # LEAP MONTH

    # ====================================================

    @staticmethod
    def get_leap_month_offset(month11, timezone):

        """
        Xác định tháng nhuận.
        """

        return None
