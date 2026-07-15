from abc import ABC, abstractmethod

from .calculator_result import CalculatorResult


class BaseCalculator(ABC):
    """
    Base class cho toàn bộ Calculator.

    Các Calculator đều kế thừa class này.

    Luồng chuẩn:

        load_rules()

            ↓

        match_rules()

            ↓

        calculate()

            ↓

        normalize()

            ↓

        return CalculatorResult
    """

    module_name = "base"

    def __init__(self, loader):

        self.loader = loader

    @abstractmethod
    def calculate(self, context) -> CalculatorResult:
        """
        Hàm bắt buộc phải override.
        """
        raise NotImplementedError

    def load_rules(self, relative_path):
        """
        Đọc Rule từ CSV.
        """
        return self.loader.load_csv(relative_path)

    def normalize(
        self,
        score: float,
        minimum: float = 0,
        maximum: float = 100
    ) -> float:
        """
        Chuẩn hóa điểm.
        """

        if score < minimum:
            return minimum

        if score > maximum:
            return maximum

        return score

    def create_result(self) -> CalculatorResult:
        """
        Tạo đối tượng kết quả mặc định.
        """

        result = CalculatorResult()

        result.module = self.module_name

        return result

    def apply_weight(
        self,
        result: CalculatorResult,
        weight: float
    ) -> CalculatorResult:
        """
        Áp dụng trọng số.
        """

        result.weight = weight
        result.calculate()

        return result

    def safe_execute(self, context) -> CalculatorResult:
        """
        Thực thi an toàn.

        Không để Calculator làm dừng toàn bộ Engine.
        """

        try:

            return self.calculate(context)

        except Exception as ex:

            result = self.create_result()

            result.success = False

            result.message = str(ex)

            return result
