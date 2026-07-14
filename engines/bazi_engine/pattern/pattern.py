"""
===============================================================================
Bazi Engine - Pattern Models
-------------------------------------------------------------------------------
File:
    bazi_engine/pattern/pattern.py

Description:
    Domain Models cho Cách Cục (格局).

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List


# =============================================================================
# PATTERN
# =============================================================================

@dataclass(slots=True)
class Pattern:
    """
    Thông tin một Cách Cục.
    """

    code: str = ""

    name: str = ""

    category: str = ""

    priority: int = 0

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

            "<Pattern "

            f"{self.name} "

            f"category={self.category}>"

        )


# =============================================================================
# PATTERN RESULT
# =============================================================================

@dataclass(slots=True)
class PatternResult:
    """
    Kết quả xác định Cách Cục.
    """

    main_pattern: Pattern = field(
        default_factory=Pattern
    )

    matched_patterns: List[Pattern] = field(
        default_factory=list
    )

    follow_pattern: bool = False

    transformation_pattern: bool = False

    special_pattern: bool = False

    confidence: float = 0.0

    description: str = ""

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # -----------------------------------------------------------------

    def has_pattern(
        self,
    ) -> bool:
        """
        Đã xác định được Cách Cục.
        """

        return bool(
            self.main_pattern.name
        )

    # -----------------------------------------------------------------

    def matched_names(
        self,
    ) -> List[str]:
        """
        Danh sách tên các Cách Cục phù hợp.
        """

        return [

            item.name

            for item in self.matched_patterns

        ]
    # -----------------------------------------------------------------

    @property
    def pattern_name(
        self,
    ) -> str:
        """
        Tên Cách Cục chính.
        """

        return self.main_pattern.name


    # -----------------------------------------------------------------

    @property
    def pattern_category(
        self,
    ) -> str:
        """
        Loại Cách Cục.
        """

        return self.main_pattern.category


    # -----------------------------------------------------------------

    @property
    def pattern_score(
        self,
    ) -> float:
        """
        Điểm Cách Cục.
        """

        return self.main_pattern.score


    # -----------------------------------------------------------------

    def summary(
        self,
    ) -> Dict[str, Any]:
        """
        Tóm tắt kết quả.
        """

        return {

            "pattern":

                self.pattern_name,

            "category":

                self.pattern_category,

            "score":

                self.pattern_score,

            "follow_pattern":

                self.follow_pattern,

            "transformation_pattern":

                self.transformation_pattern,

            "special_pattern":

                self.special_pattern,

            "confidence":

                self.confidence,

            "matched_patterns":

                self.matched_names(),

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

            "main_pattern":

                self.main_pattern.to_dict(),

            "matched_patterns":

                [

                    item.to_dict()

                    for item in self.matched_patterns

                ],

            "follow_pattern":

                self.follow_pattern,

            "transformation_pattern":

                self.transformation_pattern,

            "special_pattern":

                self.special_pattern,

            "confidence":

                self.confidence,

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

            "<PatternResult "

            f"pattern={self.pattern_name} "

            f"confidence={self.confidence:.2f}>"

        )


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "Pattern",

    "PatternResult",

]
