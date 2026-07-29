"""
===============================================================================
Bazi Engine - Useful God Models
-------------------------------------------------------------------------------
File:
    bazi_engine/useful_god/useful_god.py

Description:
    Domain Models cho Dụng Thần - Hỷ Thần - Kỵ Thần.

Version:
    1.1.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List


# =============================================================================
# GOD ELEMENT
# =============================================================================

@dataclass(slots=True)
class GodElement:
    """
    Thông tin một Ngũ Hành trong hệ thống Dụng Thần.
    """

    code: str = ""

    name: str = ""

    role: str = ""

    score: float = 0.0

    description: str = ""

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # -----------------------------------------------------------------

    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return asdict(self)

    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<GodElement "

            f"{self.name} "

            f"role={self.role}>"

        )


# =============================================================================
# USEFUL GOD RESULT
# =============================================================================

@dataclass(slots=True)
class UsefulGodResult:
    """
    Kết quả xác định Dụng Thần.
    """

    useful_god: GodElement = field(
        default_factory=GodElement
    )

    favorable_gods: List[GodElement] = field(
        default_factory=list
    )

    unfavorable_gods: List[GodElement] = field(
        default_factory=list
    )

    neutral_gods: List[GodElement] = field(
        default_factory=list
    )

    strength: str = ""

    pattern: str = ""

    description: str = ""

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # -----------------------------------------------------------------

    def has_useful_god(
        self,
    ) -> bool:
        """
        Kiểm tra đã xác định Dụng Thần.
        """

        return bool(
            self.useful_god.name
        )

    # -----------------------------------------------------------------

    def favorable_names(
        self,
    ) -> List[str]:

        return [

            item.name

            for item in self.favorable_gods

        ]

    # -----------------------------------------------------------------

    def unfavorable_names(
        self,
    ) -> List[str]:

        return [

            item.name

            for item in self.unfavorable_gods

        ]
          # -----------------------------------------------------------------

    def neutral_names(
        self,
    ) -> List[str]:
        """
        Danh sách tên Nhàn Thần.
        """

        return [

            item.name

            for item in self.neutral_gods

        ]


    # -----------------------------------------------------------------

    @property
    def useful_name(
        self,
    ) -> str:
        """
        Tên Dụng Thần.
        """

        return self.useful_god.name


    # -----------------------------------------------------------------

    @property
    def useful_role(
        self,
    ) -> str:
        """
        Vai trò của Dụng Thần.
        """

        return self.useful_god.role


    # -----------------------------------------------------------------

    def summary(
        self,
    ) -> Dict[str, Any]:
        """
        Tóm tắt kết quả.
        """

        return {

            "useful_god":

                self.useful_name,


            "strength":

                self.strength,


            "pattern":

                self.pattern,


            "favorable":

                self.favorable_names(),


            "unfavorable":

                self.unfavorable_names(),


            "neutral":

                self.neutral_names(),


            "description":

                self.description,

        }


    # -----------------------------------------------------------------

    def to_dict(
        self,
    ) -> Dict[str, Any]:
        """
        Chuyển sang Dictionary.
        """

        return {

            "useful_god":

                self.useful_god.to_dict(),


            "favorable_gods":

                [

                    item.to_dict()

                    for item in self.favorable_gods

                ],


            "unfavorable_gods":

                [

                    item.to_dict()

                    for item in self.unfavorable_gods

                ],


            "neutral_gods":

                [

                    item.to_dict()

                    for item in self.neutral_gods

                ],


            "strength":

                self.strength,


            "pattern":

                self.pattern,


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

            "<UsefulGodResult "

            f"useful={self.useful_name} "

            f"strength={self.strength}>"

        )


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "GodElement",

    "UsefulGodResult",

]
