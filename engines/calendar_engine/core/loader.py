"""
=========================================================
BTE PLATFORM
Calendar Engine

File:
    loader.py

Version:
    1.0

Author:
    BTE Platform

Description:
    Load configuration, mapping, formula and workflow.

=========================================================
"""

from pathlib import Path
import pandas as pd


class Loader:
    """
    Calendar Engine Loader

    Chức năng:

    - Đọc toàn bộ file cấu hình.
    - Đọc Rule CSV.
    - Đọc Mapping CSV.
    - Đọc Workflow CSV.
    - Đưa dữ liệu vào bộ nhớ.
    """

    def __init__(self, config_path):

        self.config_path = Path(config_path)

        self.config = None

        self.timezone = None

        self.error_code = None

        self.module_dependency = None

        self.processor_registry = None

        self.output_schema = None

        self.mapping = None

        self.formula = None

        self.workflow = None


    # =====================================================

    # CONFIG

    # =====================================================

    def load_configuration(self):

        self.config = self._read_csv(
            self.config_path / "01_engine_config.csv"
        )

        self.timezone = self._read_csv(
            self.config_path / "02_timezone.csv"
        )

        self.error_code = self._read_csv(
            self.config_path / "03_error_code.csv"
        )

        self.module_dependency = self._read_csv(
            self.config_path / "04_module_dependency.csv"
        )

        self.processor_registry = self._read_csv(
            self.config_path / "05_processor_registry.csv"
        )

        self.output_schema = self._read_csv(
            self.config_path / "06_output_schema.csv"
        )


    # =====================================================

    # DATA

    # =====================================================

    def load_mapping(self):

        file = Path("../../lich_am_duong/02_mapping.csv")

        self.mapping = self._read_csv(file)


    def load_formula(self):

        file = Path("../../lich_am_duong/03_cong_thuc.csv")

        self.formula = self._read_csv(file)


    def load_workflow(self):

        file = Path("../../lich_am_duong/04_thu_tu_tinh.csv")

        self.workflow = self._read_csv(file)


    # =====================================================

    # COMMON

    # =====================================================

    def _read_csv(self, file_path):

        return pd.read_csv(
            file_path,
            encoding="utf-8"
        )


    # =====================================================

    # GETTER

    # =====================================================

    def get_config(self):

        return self.config


    def get_timezone(self):

        return self.timezone


    def get_error_code(self):

        return self.error_code


    def get_mapping(self):

        return self.mapping


    def get_formula(self):

        return self.formula


    def get_workflow(self):

        return self.workflow


    def get_processor_registry(self):

        return self.processor_registry


    def get_output_schema(self):

        return self.output_schema
