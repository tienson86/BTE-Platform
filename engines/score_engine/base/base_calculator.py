"""
Base Calculator

Lớp cha của toàn bộ Calculator.
"""

import time
from abc import ABC, abstractmethod

from .calculator_result import CalculatorResult


class BaseCalculator(ABC):

    MODULE_NAME = ""

    DIMENSION_NAME = ""

    DESCRIPTION = ""

    def __init__(self, loader):

        self.loader = loader

    # =====================================

    def create_result(self):

        result = CalculatorResult()

        result.module = self.MODULE_NAME

        result.dimension = self.DIMENSION_NAME

        return result

    # =====================================

    def before_execute(
        self,
        context
    ):

        pass

    def after_execute(
        self,
        result,
        context
    ):

        return result

    # =====================================

    def safe_execute(
        self,
        context
    ):

        start = time.perf_counter()

        result = self.create_result()

        try:

            self.before_execute(context)

            result = self.calculate(context)

            result.success = True

        except Exception as ex:

            result.success = False

            result.add_error(str(ex))

        end = time.perf_counter()

        result.execution_time = round(
            end - start,
            6
        )

        return self.after_execute(
            result,
            context
        )

    # =====================================

    @abstractmethod
    def calculate(
        self,
        context
    ):

        raise NotImplementedError

    # =====================================

    def __repr__(self):

        return (

            f"<{self.__class__.__name__}"

            f" module={self.MODULE_NAME}>"
        )
