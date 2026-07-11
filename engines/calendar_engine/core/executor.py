"""
=========================================================
BTE PLATFORM
Calendar Engine

File:
    executor.py

Version:
    1.0

Author:
    BTE Platform

Description:
    Calendar Workflow Executor

=========================================================
"""

from processor.input_validator import InputValidator
from processor.timezone_processor import TimezoneProcessor
from processor.julian_day_processor import JulianDayProcessor
from processor.lunar_converter import LunarConverter
from processor.ganzhi_year import GanzhiYearProcessor
from processor.jieqi import JieQiProcessor
from processor.ganzhi_month import GanzhiMonthProcessor
from processor.ganzhi_day import GanzhiDayProcessor
from processor.ganzhi_hour import GanzhiHourProcessor
from processor.nap_am import NapAmProcessor
from processor.zhiri import ZhiRiProcessor
from processor.huangdao import HuangDaoProcessor
from processor.result_validator import ResultValidator


class Executor:
    """
    Calendar Workflow Executor
    """

    def __init__(self):

        self.processor_map = {

            "InputValidator": InputValidator(),

            "TimezoneProcessor": TimezoneProcessor(),

            "JulianDayProcessor": JulianDayProcessor(),

            "LunarConverter": LunarConverter(),

            "GanzhiYearProcessor": GanzhiYearProcessor(),

            "JieQiProcessor": JieQiProcessor(),

            "GanzhiMonthProcessor": GanzhiMonthProcessor(),

            "GanzhiDayProcessor": GanzhiDayProcessor(),

            "GanzhiHourProcessor": GanzhiHourProcessor(),

            "NapAmProcessor": NapAmProcessor(),

            "ZhiRiProcessor": ZhiRiProcessor(),

            "HuangDaoProcessor": HuangDaoProcessor(),

            "ResultValidator": ResultValidator()

        }


    # ====================================================

    # MAIN

    # ====================================================

    def run(
        self,
        input_data,
        loader
    ):

        context = {}

        context["input"] = input_data

        context["config"] = loader.get_config()

        context["timezone"] = loader.get_timezone()

        context["mapping"] = loader.get_mapping()

        context["formula"] = loader.get_formula()

        context["workflow"] = loader.get_workflow()

        registry = loader.get_processor_registry()

        registry = registry.sort_values("step_order")


        for _, row in registry.iterrows():

            if row["enabled"] is False:
                continue

            class_name = row["class_name"]

            processor = self.processor_map.get(class_name)

            if processor is None:
                raise Exception(
                    f"Processor not found : {class_name}"
                )

            context = processor.execute(context)

        return context
