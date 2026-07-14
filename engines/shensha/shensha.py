"""
===============================================================================
Bazi Engine - Shen Sha Models
-------------------------------------------------------------------------------
File:
    bazi_engine/shensha/shensha.py

Description:
    Domain Models cho Thần Sát (神煞).

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field

from typing import Any
from typing import Dict
from typing import List


# =============================================================================
# SHEN SHA
# =============================================================================

@dataclass(slots=True)
class ShenSha:
    """
    Thông tin một Thần Sát.
    """

    code: str = ""

    name: str = ""

    category: str = ""

    level: str = ""

    element: str = ""

    yin_yang: str = ""

    description: str = ""

    effect: str = ""

    priority: int = 0

    score: float = 0.0

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

            "<ShenSha "

            f"{self.name} "

            f"category={self.category}>"

        )


# =============================================================================
# SHEN SHA RESULT
# =============================================================================

@dataclass(slots=True)
class ShenShaResult:
    """
    Kết quả lập Thần Sát.
    """

    shensha_list: List[ShenSha] = field(
        default_factory=list
    )

    auspicious: List[ShenSha] = field(
        default_factory=list
    )

    inauspicious: List[ShenSha] = field(
        default_factory=list
    )

    neutral: List[ShenSha] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # -----------------------------------------------------------------

    def has_shensha(
        self,
    ) -> bool:
        """
        Có Thần Sát hay không.
        """

        return len(
            self.shensha_list
        ) > 0

    # -----------------------------------------------------------------

    def count(
        self,
    ) -> int:
        """
        Tổng số Thần Sát.
        """

        return len(
            self.shensha_list
        )

    # -----------------------------------------------------------------

    def names(
        self,
    ) -> List[str]:
        """
        Danh sách tên Thần Sát.
        """

        return [

            item.name

            for item in self.shensha_list

        ]
    # -----------------------------------------------------------------

    @property
    def auspicious_count(
        self,
    ) -> int:
        """
        Tổng số Cát Thần.
        """

        return len(
            self.auspicious
        )


    # -----------------------------------------------------------------

    @property
    def inauspicious_count(
        self,
    ) -> int:
        """
        Tổng số Hung Thần.
        """

        return len(
            self.inauspicious
        )


    # -----------------------------------------------------------------

    @property
    def neutral_count(
        self,
    ) -> int:
        """
        Tổng số Trung Tính.
        """

        return len(
            self.neutral
        )


    # -----------------------------------------------------------------

    def find(
        self,
        code: str,
    ) -> ShenSha | None:
        """
        Tìm Thần Sát theo mã.
        """

        for item in self.shensha_list:

            if item.code == code:

                return item

        return None


    # -----------------------------------------------------------------

    def exists(
        self,
        code: str,
    ) -> bool:
        """
        Kiểm tra Thần Sát có tồn tại.
        """

        return self.find(
            code
        ) is not None


    # -----------------------------------------------------------------

    def filter_by_category(
        self,
        category: str,
    ) -> List[ShenSha]:
        """
        Lọc theo nhóm.
        """

        return [

            item

            for item in self.shensha_list

            if item.category == category

        ]


    # -----------------------------------------------------------------

    def filter_by_level(
        self,
        level: str,
    ) -> List[ShenSha]:
        """
        Lọc theo cấp độ.
        """

        return [

            item

            for item in self.shensha_list

            if item.level == level

        ]
# =============================================================================
# SHEN SHA OCCURRENCE
# =============================================================================

@dataclass(slots=True)
class ShenShaOccurrence:
    """
    Một lần xuất hiện của Thần Sát.
    """

    shensha: ShenSha = field(
        default_factory=ShenSha
    )

    pillar: str = ""
    """
    year / month / day / hour
    """

    position: str = ""
    """
    stem / branch / hidden_stem
    """

    source: str = ""
    """
    Quy tắc sinh Thần Sát.
    """

    value: str = ""
    """
    Giá trị Can hoặc Chi kích hoạt.
    """

    active: bool = True

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # -----------------------------------------------------------------

    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return {

            "shensha":

                self.shensha.to_dict(),

            "pillar":

                self.pillar,

            "position":

                self.position,

            "source":

                self.source,

            "value":

                self.value,

            "active":

                self.active,

            "metadata":

                self.metadata,

        }

    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<ShenShaOccurrence "

            f"{self.shensha.name} "

            f"{self.pillar}.{self.position}>"

        )
    # -----------------------------------------------------------------

    def summary(
        self,
    ) -> Dict[str, Any]:
        """
        Tóm tắt kết quả Thần Sát.
        """

        return {

            "total":

                self.count(),

            "auspicious":

                self.auspicious_count,

            "inauspicious":

                self.inauspicious_count,

            "neutral":

                self.neutral_count,

            "names":

                self.names(),

        }


    # -----------------------------------------------------------------

    def to_dict(
        self,
    ) -> Dict[str, Any]:
        """
        Chuyển kết quả sang Dictionary.
        """

        return {

            "shensha_list":

                [

                    item.to_dict()

                    for item in self.shensha_list

                ],

            "occurrences":

                [

                    item.to_dict()

                    for item in self.occurrences

                ],

            "auspicious":

                [

                    item.to_dict()

                    for item in self.auspicious

                ],

            "inauspicious":

                [

                    item.to_dict()

                    for item in self.inauspicious

                ],

            "neutral":

                [

                    item.to_dict()

                    for item in self.neutral

                ],

            "metadata":

                self.metadata,

        }


    # -----------------------------------------------------------------

    def clear(
        self,
    ) -> None:
        """
        Xóa toàn bộ kết quả.
        """

        self.shensha_list.clear()

        self.occurrences.clear()

        self.auspicious.clear()

        self.inauspicious.clear()

        self.neutral.clear()

        self.metadata.clear()


    # -----------------------------------------------------------------

    def __len__(
        self,
    ) -> int:
        """
        Tổng số Thần Sát.
        """

        return len(
            self.occurrences
        )


    # -----------------------------------------------------------------

    def __iter__(
        self,
    ):
        """
        Duyệt các lần xuất hiện.
        """

        return iter(
            self.occurrences
        )


    # -----------------------------------------------------------------

    def __contains__(
        self,
        code: str,
    ) -> bool:
        """
        Kiểm tra mã Thần Sát có tồn tại.
        """

        return self.exists(
            code
        )


    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<ShenShaResult "

            f"count={len(self)} "

            f"auspicious={self.auspicious_count} "

            f"inauspicious={self.inauspicious_count}>"

        )


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "ShenSha",

    "ShenShaOccurrence",

    "ShenShaResult",

]
