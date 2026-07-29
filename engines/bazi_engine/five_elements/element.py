"""
===============================================================================
Bazi Engine - Five Elements Models
-------------------------------------------------------------------------------
File:
    bazi_engine/five_elements/element.py

Description:
    Domain Models cho Ngũ Hành.

Bao gồm:

    Element
    ElementRelation
    ElementBalance

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


# =============================================================================
# ELEMENT
# =============================================================================

@dataclass(slots=True)
class Element:
    """
    Mô hình một Ngũ Hành.

    Ví dụ:

        Giáp -> Mộc
        Bính -> Hỏa
        Canh -> Kim
    """

    code: str = ""

    name: str = ""

    chinese: str = ""

    yin_yang: str = ""

    description: str = ""

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # -----------------------------------------------------------------

    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return asdict(
            self
        )

    # -----------------------------------------------------------------

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "Element":

        return cls(
            **data
        )

    # -----------------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return self.name

    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"<Element "

            f"{self.code}:{self.name}>"

        )


# =============================================================================
# ELEMENT RELATION
# =============================================================================

@dataclass(slots=True)
class ElementRelation:
    """
    Quan hệ giữa hai Ngũ Hành.

    Ví dụ:

        Mộc sinh Hỏa

        Hỏa khắc Kim
    """

    source: str = ""

    target: str = ""

    relation: str = ""

    strength: float = 1.0

    description: str = ""

    metadata: Dict[str, Any] = field(
        default_factory=dict
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

            f"<ElementRelation "

            f"{self.source}"

            f"-"

            f"{self.relation}"

            f"-"

            f"{self.target}>"

        )


# =============================================================================
# ELEMENT BALANCE
# =============================================================================

@dataclass(slots=True)
class ElementBalance:
    """
    Tổng hợp phân bố Ngũ Hành trong một lá số.

    Ví dụ:

        Mộc : 30
        Hỏa : 20
        Thổ : 15
        Kim : 25
        Thủy: 10
    """

    wood: float = 0.0

    fire: float = 0.0

    earth: float = 0.0

    metal: float = 0.0

    water: float = 0.0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # -----------------------------------------------------------------

    @property
    def total(
        self,
    ) -> float:

        return (

            self.wood

            + self.fire

            + self.earth

            + self.metal

            + self.water

        )

    # -----------------------------------------------------------------

    def values(
        self,
    ) -> Dict[str, float]:

        return {

            "Mộc":
                self.wood,

            "Hỏa":
                self.fire,

            "Thổ":
                self.earth,

            "Kim":
                self.metal,

            "Thủy":
                self.water,

        }
          # -----------------------------------------------------------------
    # ANALYSIS
    # -----------------------------------------------------------------

    def dominant_element(
        self,
    ) -> Optional[str]:
        """
        Tìm Ngũ Hành mạnh nhất.
        """

        values = self.values()

        if not values:

            return None

        return max(

            values,

            key=values.get,

        )

    # -----------------------------------------------------------------

    def weakest_element(
        self,
    ) -> Optional[str]:
        """
        Tìm Ngũ Hành yếu nhất.
        """

        values = self.values()

        if not values:

            return None

        return min(

            values,

            key=values.get,

        )

    # -----------------------------------------------------------------

    def get_value(
        self,
        element: str,
    ) -> float:
        """
        Lấy giá trị của một Ngũ Hành.
        """

        mapping = {

            "Mộc":
                self.wood,

            "Hỏa":
                self.fire,

            "Thổ":
                self.earth,

            "Kim":
                self.metal,

            "Thủy":
                self.water,

        }

        return mapping.get(
            element,
            0.0,
        )

    # -----------------------------------------------------------------

    def get_percentage(
        self,
    ) -> Dict[str, float]:
        """
        Tính phần trăm phân bố Ngũ Hành.
        """

        total = self.total

        if total == 0:

            return {

                key: 0.0

                for key

                in self.values()

            }

        return {

            key:

                round(

                    value / total * 100,

                    2,

                )

            for key, value

            in self.values().items()

        }

    # -----------------------------------------------------------------

    def has_element(
        self,
        element: str,
    ) -> bool:
        """
        Kiểm tra có Ngũ Hành hay không.
        """

        return self.get_value(
            element
        ) > 0

    # -----------------------------------------------------------------

    def contains(
        self,
        element: str,
    ) -> bool:
        """
        Alias của has_element().
        """

        return self.has_element(
            element
        )

    # -----------------------------------------------------------------

    def sorted_elements(
        self,
    ) -> List[tuple]:
        """
        Sắp xếp Ngũ Hành theo mạnh đến yếu.
        """

        return sorted(

            self.values().items(),

            key=lambda item:

                item[1],

            reverse=True,

        )

    # -----------------------------------------------------------------

    def summary(
        self,
    ) -> Dict[str, Any]:
        """
        Tóm tắt phân bố Ngũ Hành.
        """

        return {

            "total":
                self.total,

            "values":
                self.values(),

            "percentage":
                self.get_percentage(),

            "dominant":
                self.dominant_element(),

            "weakest":
                self.weakest_element(),

        }

    # -----------------------------------------------------------------

    def clear(
        self,
    ) -> None:
        """
        Xóa dữ liệu.
        """

        self.wood = 0.0

        self.fire = 0.0

        self.earth = 0.0

        self.metal = 0.0

        self.water = 0.0

        self.metadata.clear()

    # -----------------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return sum(

            1

            for value

            in self.values().values()

            if value > 0

        )

    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<ElementBalance "

            f"dominant={self.dominant_element()} "

            f"total={self.total}>"

        )


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "Element",

    "ElementRelation",

    "ElementBalance",

]
