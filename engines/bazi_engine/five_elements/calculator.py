"""
===============================================================================
Bazi Engine - Five Elements Calculator
-------------------------------------------------------------------------------
File:
    bazi_engine/five_elements/calculator.py

Description:
    Bộ tính Ngũ Hành trong Bát Tự.

Flow:

        FourPillars
             |
             ▼
    FiveElementCalculator
             |
             ▼
    FiveElementRuleLoader
             |
             ▼
      ElementBalance


Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations


from typing import Dict
from typing import List


from bazi_engine.core.base_calculator import BaseCalculator

from bazi_engine.models import FourPillars
from bazi_engine.models import Pillar


from .element import (
    Element,
    ElementBalance,
)

from .rule_loader import (
    five_element_rule_loader,
)



# =============================================================================
# EXCEPTIONS
# =============================================================================

class FiveElementCalculatorError(
    Exception,
):
    """
    Base Exception.
    """



class FiveElementCalculationError(
    FiveElementCalculatorError,
):
    """
    Calculation Error.
    """



# =============================================================================
# CALCULATOR
# =============================================================================

class FiveElementCalculator(
    BaseCalculator,
):
    """
    Bộ tính Ngũ Hành.
    """


    def __init__(
        self,
    ):

        super().__init__()


        self._loader = (
            five_element_rule_loader
        )


        self.mark_loaded()



    # -----------------------------------------------------------------
    # INTERNAL
    # -----------------------------------------------------------------

    def _create_element(
        self,
        data: dict,
    ) -> Element:
        """
        Tạo Element Object từ Rule.
        """

        return Element(

            code=data.get(
                "element",
                "",
            ),

            name=data.get(
                "element",
                "",
            ),

            chinese=data.get(
                "chinese",
                "",
            ),

            yin_yang=data.get(
                "yin_yang",
                "",
            ),

            description=data.get(
                "description",
                "",
            ),

            metadata=data,

        )



    # -----------------------------------------------------------------

    def get_stem_element(
        self,
        stem: str,
    ) -> Element:
        """
        Lấy Ngũ Hành của Thiên Can.
        """

        data = self._loader.get_stem_element(
            stem
        )


        return self._create_element(
            data
        )



    # -----------------------------------------------------------------

    def get_branch_element(
        self,
        branch: str,
    ) -> Element:
        """
        Lấy Ngũ Hành của Địa Chi.
        """

        data = self._loader.get_branch_element(
            branch
        )


        return self._create_element(
            data
        )
          # -----------------------------------------------------------------
    # HIDDEN STEMS
    # -----------------------------------------------------------------

    def get_hidden_stem_elements(
        self,
        branch: str,
    ) -> List[Element]:
        """
        Lấy Ngũ Hành của toàn bộ Tàng Can trong Địa Chi.
        """

        hidden_stems = (
            self._loader.get_hidden_stems(
                branch
            )
        )


        result = []


        for item in hidden_stems:

            element = self._create_element(
                item
            )

            result.append(
                element
            )


        return result



    # -----------------------------------------------------------------
    # PILLAR
    # -----------------------------------------------------------------

    def calculate_pillar(
        self,
        pillar: Pillar,
    ) -> Dict[str, object]:
        """
        Tính Ngũ Hành của một Trụ.

        Bao gồm:

        - Thiên Can
        - Địa Chi
        - Tàng Can
        """

        stem_element = (
            self.get_stem_element(
                pillar.stem
            )
        )


        branch_element = (
            self.get_branch_element(
                pillar.branch
            )
        )


        hidden_elements = (
            self.get_hidden_stem_elements(
                pillar.branch
            )
        )


        return {

            "stem":

                stem_element,


            "branch":

                branch_element,


            "hidden_stems":

                hidden_elements,

        }



    # -----------------------------------------------------------------
    # HEAVENLY STEMS
    # -----------------------------------------------------------------

    def calculate_stems(
        self,
        pillars: FourPillars,
    ) -> Dict[str, Element]:
        """
        Tính Ngũ Hành của 4 Thiên Can.
        """

        return {


            "year":

                self.get_stem_element(
                    pillars.year.stem
                ),


            "month":

                self.get_stem_element(
                    pillars.month.stem
                ),


            "day":

                self.get_stem_element(
                    pillars.day.stem
                ),


            "hour":

                self.get_stem_element(
                    pillars.hour.stem
                ),

        }



    # -----------------------------------------------------------------
    # BRANCHES
    # -----------------------------------------------------------------

    def calculate_branches(
        self,
        pillars: FourPillars,
    ) -> Dict[str, Element]:
        """
        Tính Ngũ Hành của 4 Địa Chi.
        """

        return {


            "year":

                self.get_branch_element(
                    pillars.year.branch
                ),


            "month":

                self.get_branch_element(
                    pillars.month.branch
                ),


            "day":

                self.get_branch_element(
                    pillars.day.branch
                ),


            "hour":

                self.get_branch_element(
                    pillars.hour.branch
                ),

        }
          # -----------------------------------------------------------------
    # ELEMENT SCORE
    # -----------------------------------------------------------------

    def _add_element_score(
        self,
        balance: ElementBalance,
        element: str,
        value: float = 1.0,
    ) -> None:
        """
        Cộng điểm cho một Ngũ Hành.
        """

        if element == "Mộc":

            balance.wood += value


        elif element == "Hỏa":

            balance.fire += value


        elif element == "Thổ":

            balance.earth += value


        elif element == "Kim":

            balance.metal += value


        elif element == "Thủy":

            balance.water += value



    # -----------------------------------------------------------------

    def calculate_pillar_balance(
        self,
        pillar: Pillar,
        balance: ElementBalance,
    ) -> None:
        """
        Cộng điểm Ngũ Hành của một Trụ.
        """

        # Thiên Can

        stem_element = (
            self.get_stem_element(
                pillar.stem
            )
        )


        self._add_element_score(

            balance,

            stem_element.name,

            1.0,

        )


        # Địa Chi

        branch_element = (
            self.get_branch_element(
                pillar.branch
            )
        )


        self._add_element_score(

            balance,

            branch_element.name,

            1.0,

        )


        # Tàng Can

        hidden_elements = (
            self.get_hidden_stem_elements(
                pillar.branch
            )
        )


        for element in hidden_elements:

            self._add_element_score(

                balance,

                element.name,

                0.5,

            )



    # -----------------------------------------------------------------
    # FULL BALANCE
    # -----------------------------------------------------------------

    def calculate_balance(
        self,
        pillars: FourPillars,
    ) -> ElementBalance:
        """
        Tính tổng cân bằng Ngũ Hành của lá số.

        Công thức V1.0:

        Thiên Can:
            1 điểm

        Địa Chi:
            1 điểm

        Tàng Can:
            0.5 điểm
        """

        balance = ElementBalance()


        self.calculate_pillar_balance(

            pillars.year,

            balance,

        )


        self.calculate_pillar_balance(

            pillars.month,

            balance,

        )


        self.calculate_pillar_balance(

            pillars.day,

            balance,

        )


        self.calculate_pillar_balance(

            pillars.hour,

            balance,

        )


        balance.metadata = {

            "method":

                "stem_1_branch_1_hidden_0.5",

            "pillar_count":

                4,

        }


        return balance



    # -----------------------------------------------------------------

    def calculate(
        self,
        pillars: FourPillars,
    ) -> ElementBalance:
        """
        API chính tính Ngũ Hành.
        """

        self.ensure_loaded()


        return self.calculate_balance(
            pillars
        )
          # -----------------------------------------------------------------
    # ANALYSIS
    # -----------------------------------------------------------------

    def calculate_percentage(
        self,
        pillars: FourPillars,
    ) -> Dict[str, float]:
        """
        Tính tỷ lệ phần trăm Ngũ Hành.
        """

        balance = self.calculate_balance(
            pillars
        )


        return balance.get_percentage()



    # -----------------------------------------------------------------

    def dominant_element(
        self,
        pillars: FourPillars,
    ) -> str:
        """
        Lấy Ngũ Hành vượng nhất.
        """

        balance = self.calculate_balance(
            pillars
        )


        return balance.dominant_element()



    # -----------------------------------------------------------------

    def weakest_element(
        self,
        pillars: FourPillars,
    ) -> str:
        """
        Lấy Ngũ Hành yếu nhất.
        """

        balance = self.calculate_balance(
            pillars
        )


        return balance.weakest_element()



    # -----------------------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------------------

    def verify(
        self,
        pillars: FourPillars,
    ) -> bool:
        """
        Kiểm tra có thể tính toán hay không.
        """

        try:

            balance = self.calculate(
                pillars
            )

            return balance.total > 0


        except Exception:

            return False



    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra trạng thái Calculator.
        """

        if not self.loaded:

            return False


        return self._loader.health_check()



    # -----------------------------------------------------------------
    # INFORMATION
    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, object]:
        """
        Thống kê Calculator.
        """

        return {

            "calculator":

                self.__class__.__name__,


            "rule_loader":

                self._loader.statistics(),

        }



    # -----------------------------------------------------------------

    def debug(
        self,
    ) -> Dict[str, object]:
        """
        Thông tin Debug.
        """

        return {

            "loaded":

                self.loaded,


            "health":

                self.health_check(),


            "statistics":

                self.statistics(),

        }



    # -----------------------------------------------------------------
    # RELOAD
    # -----------------------------------------------------------------

    def refresh(
        self,
    ) -> None:
        """
        Reload Database.
        """

        self._loader.refresh()

        self.mark_loaded()



    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa cache Rule.
        """

        self._loader.clear_cache()



    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<FiveElementCalculator "

            f"loaded={self.loaded}>"

        )



# =============================================================================
# SINGLETON
# =============================================================================

five_element_calculator = FiveElementCalculator()



# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "FiveElementCalculator",

    "FiveElementCalculatorError",

    "FiveElementCalculationError",

    "five_element_calculator",

]
