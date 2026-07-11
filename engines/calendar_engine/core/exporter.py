"""
=========================================================
BTE PLATFORM
Calendar Engine

File:
    exporter.py

Version:
    1.0

Author:
    BTE Platform

Description:
    Export Calendar Engine Result

=========================================================
"""

from pathlib import Path
from datetime import datetime
import pandas as pd


class Exporter:
    """
    Calendar Engine Exporter

    Chức năng:

    - Xuất kết quả ra CSV
    - Chuẩn hóa thứ tự cột
    - Ghi thông tin phiên bản
    - Ghi thời gian sinh dữ liệu
    """

    def __init__(self):

        self.output_path = Path("../output")


    # ====================================================

    # MAIN

    # ====================================================

    def export(self, context):

        schema = context["config"]

        result = self.build_result(context)

        dataframe = self.build_dataframe(result)

        self.save_csv(dataframe)


    # ====================================================

    # BUILD RESULT

    # ====================================================

    def build_result(self, context):

        result = {

            "id": context.get("record_id"),

            "ngay_duong": context.get("solar_date"),

            "thang_duong": context.get("solar_month"),

            "nam_duong": context.get("solar_year"),

            "ngay_am": context.get("lunar_day"),

            "thang_am": context.get("lunar_month"),

            "nam_am": context.get("lunar_year"),

            "thang_nhuan": context.get("leap_month"),

            "can_nam": context.get("year_can"),

            "chi_nam": context.get("year_chi"),

            "can_thang": context.get("month_can"),

            "chi_thang": context.get("month_chi"),

            "can_ngay": context.get("day_can"),

            "chi_ngay": context.get("day_chi"),

            "can_gio": context.get("hour_can"),

            "chi_gio": context.get("hour_chi"),

            "tiet_khi": context.get("jieqi"),

            "nguyet_lenh": context.get("month_commander"),

            "nap_am": context.get("nap_am"),

            "truc_ngay": context.get("day_officer"),

            "hoang_dao": context.get("huang_dao"),

            "julian_day": context.get("julian_day"),

            "timezone": context.get("timezone_name"),

            "engine_version": "1.0",

            "created_at": datetime.now()

        }

        return result


    # ====================================================

    # DATAFRAME

    # ====================================================

    def build_dataframe(self, result):

        dataframe = pd.DataFrame([result])

        return dataframe


    # ====================================================

    # SAVE

    # ====================================================

    def save_csv(self, dataframe):

        self.output_path.mkdir(
            parents=True,
            exist_ok=True
        )

        filename = self.output_path / "calendar_result.csv"

        dataframe.to_csv(

            filename,

            index=False,

            encoding="utf-8-sig"

        )

        return filename
