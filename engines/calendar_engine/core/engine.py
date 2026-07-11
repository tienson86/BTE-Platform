"""
=========================================================
BTE PLATFORM
Calendar Engine

File:
    engine.py

Version:
    1.0

Author:
    BTE Platform

Description:
    Calendar Engine Entry Point

=========================================================
"""

from core.loader import Loader
from core.executor import Executor
from core.exporter import Exporter


class CalendarEngine:
    """
    Calendar Engine
    """

    def __init__(self, config_path):
        self.config_path = config_path

        self.loader = Loader(config_path)

        self.executor = Executor()

        self.exporter = Exporter()


    def initialize(self):
        """
        Khởi tạo Engine
        """

        self.loader.load_configuration()

        self.loader.load_mapping()

        self.loader.load_formula()

        self.loader.load_workflow()


    def execute(self, input_data):
        """
        Chạy Calendar Engine
        """

        context = self.executor.run(
            input_data=input_data,
            loader=self.loader
        )

        return context


    def export(self, context):
        """
        Xuất dữ liệu
        """

        self.exporter.export(context)


    def run(self, input_data):
        """
        Quy trình đầy đủ
        """

        self.initialize()

        result = self.execute(input_data)

        self.export(result)

        return result
