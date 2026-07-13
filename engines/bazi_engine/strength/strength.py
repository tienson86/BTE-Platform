"""
===============================================================================
Bazi Engine - Strength Models
-------------------------------------------------------------------------------
File:
    bazi_engine/strength/strength.py

Description:
    Domain Models cho Thân Vượng - Thân Nhược.

Bao gồm:

    StrengthLevel
    StrengthScore
    StrengthResult

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations


from dataclasses import dataclass, field, asdict

from typing import Any
from typing import Dict
from typing import Optional



# =============================================================================
# STRENGTH LEVEL
# =============================================================================

@dataclass(slots=True)
class StrengthLevel:
    """
    Cấp độ Thân Vượng Nhược.

    Ví dụ:

        Thân Cực Vượng
        Thân Vượng
        Bình Hòa
        Thân Nhược
        Thân Cực Nhược
    """

    code: str = ""

    name: str = ""

    score_min: float = 0.0

    score_max: float = 0.0

    description: str = ""

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


    # -----------------------------------------------------------------

    def contains(
        self,
        score: float,
    ) -> bool:
        """
        Kiểm tra điểm có thuộc cấp độ này không.
        """

        return (

            self.score_min

            <=

            score

            <=

            self.score_max

        )


    # -----------------------------------------------------------------

    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return asdict(
            self
        )


    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<StrengthLevel "

            f"{self.code}:{self.name}>"

        )



# =============================================================================
# STRENGTH SCORE
# =============================================================================

@dataclass(slots=True)
class StrengthScore:
    """
    Điểm tính Thân Vượng Nhược.

    Thành phần:

        - Root (Gốc)
        - Support (Sinh Trợ)
        - Resource (Ấn)
        - Output (Tiết)
        - Wealth (Tài)
        - Officer (Quan)
    """

    root: float = 0.0

    support: float = 0.0

    resource: float = 0.0

    output: float = 0.0

    wealth: float = 0.0

    officer: float = 0.0



    # -----------------------------------------------------------------

    @property
    def total_positive(
        self,
    ) -> float:
        """
        Tổng lực trợ thân.
        """

        return (

            self.root

            +

            self.support

            +

            self.resource

        )



    # -----------------------------------------------------------------

    @property
    def total_negative(
        self,
    ) -> float:
        """
        Tổng lực tiết khắc thân.
        """

        return (

            self.output

            +

            self.wealth

            +

            self.officer

        )



    # -----------------------------------------------------------------

    @property
    def balance(
        self,
    ) -> float:
        """
        Cân bằng lực lượng.

        Dương:
            Thân mạnh

        Âm:
            Thân yếu
        """

        return (

            self.total_positive

            -

            self.total_negative

        )



    # -----------------------------------------------------------------

    def to_dict(
        self,
    ) -> Dict[str, float]:

        return {

            "root":
                self.root,

            "support":
                self.support,

            "resource":
                self.resource,

            "output":
                self.output,

            "wealth":
                self.wealth,

            "officer":
                self.officer,

            "positive":
                self.total_positive,

            "negative":
                self.total_negative,

            "balance":
                self.balance,

        }
      # =============================================================================
# STRENGTH RESULT
# =============================================================================

@dataclass(slots=True)
class StrengthResult:
    """
    Kết quả phân tích Thân Vượng Nhược.

    Ví dụ:

        Nhật Chủ:
            Canh Kim

        Điểm:
            72

        Kết luận:
            Thân Vượng
    """

    day_master: str = ""

    element: str = ""

    score: float = 0.0

    level: Optional[StrengthLevel] = None

    strength_score: StrengthScore = field(
        default_factory=StrengthScore
    )

    month_branch: str = ""

    description: str = ""

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


    # -----------------------------------------------------------------

    @property
    def level_name(
        self,
    ) -> str:
        """
        Lấy tên cấp độ.
        """

        if self.level:

            return self.level.name


        return ""



    # -----------------------------------------------------------------

    def is_strong(
        self,
    ) -> bool:
        """
        Kiểm tra Thân Vượng.
        """

        return self.score > 50



    # -----------------------------------------------------------------

    def is_weak(
        self,
    ) -> bool:
        """
        Kiểm tra Thân Nhược.
        """

        return self.score < 50



    # -----------------------------------------------------------------

    def is_balanced(
        self,
    ) -> bool:
        """
        Kiểm tra Bình Hòa.
        """

        return self.score == 50



    # -----------------------------------------------------------------

    def percentage(
        self,
    ) -> float:
        """
        Quy đổi điểm sang phần trăm.

        V1.0:

        0 - 100 điểm
        """

        if self.score < 0:

            return 0.0


        if self.score > 100:

            return 100.0


        return self.score



    # -----------------------------------------------------------------

    def summary(
        self,
    ) -> Dict[str, Any]:
        """
        Tổng hợp kết quả.
        """

        return {

            "day_master":

                self.day_master,


            "element":

                self.element,


            "score":

                self.score,


            "level":

                self.level_name,


            "month_branch":

                self.month_branch,


            "balance":

                self.strength_score.balance,


            "strength_score":

                self.strength_score.to_dict(),

        }



    # -----------------------------------------------------------------

    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return {

            "day_master":

                self.day_master,


            "element":

                self.element,


            "score":

                self.score,


            "level":

                self.level.to_dict()

                if self.level

                else None,


            "strength_score":

                self.strength_score.to_dict(),


            "month_branch":

                self.month_branch,


            "description":

                self.description,


            "metadata":

                self.metadata,

        }



    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<StrengthResult "

            f"{self.day_master} "

            f"score={self.score} "

            f"level={self.level_name}>"

        )



# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "StrengthLevel",

    "StrengthScore",

    "StrengthResult",

]
