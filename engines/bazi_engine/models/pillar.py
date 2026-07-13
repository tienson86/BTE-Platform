"""
===============================================================================
Bazi Engine - Pillar Model
-------------------------------------------------------------------------------
File:
    bazi_engine/models/pillar.py

Description:
    Domain Model của một Trụ Bát Tự.

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import asdict
from typing import Dict


# =============================================================================
# MODEL
# =============================================================================

@dataclass(slots=True)
class Pillar:
    """
    Một Trụ Can Chi.
    """

    # ---------------------------------------------------------
    # Heavenly Stem
    # ---------------------------------------------------------

    stem: str

    stem_index: int

    stem_element: str

    stem_yinyang: str

    # ---------------------------------------------------------
    # Earthly Branch
    # ---------------------------------------------------------

    branch: str

    branch_index: int

    branch_element: str

    branch_yinyang: str

    # ---------------------------------------------------------
    # Optional
    # ---------------------------------------------------------

    hidden_stems: tuple = ()

    ten_gods: tuple = ()

    shensha: tuple = ()

    nayin: str = ""

    xunkong: str = ""

    # ---------------------------------------------------------

    @property
    def ganzhi(self) -> str:

        return f"{self.stem}{self.branch}"

    # ---------------------------------------------------------

    @property
    def stem_code(self) -> str:

        return self.stem.upper()

    # ---------------------------------------------------------

    @property
    def branch_code(self) -> str:

        return self.branch.upper()

    # ---------------------------------------------------------

    @property
    def is_yang(self) -> bool:

        return self.stem_yinyang == "Dương"

    # ---------------------------------------------------------

    @property
    def is_yin(self) -> bool:

        return self.stem_yinyang == "Âm"

    # ---------------------------------------------------------

    @property
    def element_pair(self):

        return (

            self.stem_element,

            self.branch_element,

        )

    # ---------------------------------------------------------

    def to_dict(self) -> Dict:

        return asdict(self)

    # ---------------------------------------------------------

    @classmethod
    def from_dict(
        cls,
        data: Dict,
    ):

        return cls(

            stem=data["stem"],

            stem_index=int(
                data["stem_index"]
            ),

            stem_element=data[
                "stem_element"
            ],

            stem_yinyang=data[
                "stem_yinyang"
            ],

            branch=data[
                "branch"
            ],

            branch_index=int(
                data["branch_index"]
            ),

            branch_element=data[
                "branch_element"
            ],

            branch_yinyang=data[
                "branch_yinyang"
            ],

            hidden_stems=tuple(
                data.get(
                    "hidden_stems",
                    (),
                )
            ),

            ten_gods=tuple(
                data.get(
                    "ten_gods",
                    (),
                )
            ),

            shensha=tuple(
                data.get(
                    "shensha",
                    (),
                )
            ),

            nayin=data.get(
                "nayin",
                "",
            ),

            xunkong=data.get(
                "xunkong",
                "",
            ),
        )

    # ---------------------------------------------------------

    def copy(self):

        return Pillar(

            stem=self.stem,

            stem_index=self.stem_index,

            stem_element=self.stem_element,

            stem_yinyang=self.stem_yinyang,

            branch=self.branch,

            branch_index=self.branch_index,

            branch_element=self.branch_element,

            branch_yinyang=self.branch_yinyang,

            hidden_stems=self.hidden_stems,

            ten_gods=self.ten_gods,

            shensha=self.shensha,

            nayin=self.nayin,

            xunkong=self.xunkong,
        )

    # ---------------------------------------------------------

    def __str__(self):

        return self.ganzhi

    # ---------------------------------------------------------

    def __repr__(self):

        return (

            f"<Pillar "

            f"{self.ganzhi} "

            f"{self.stem_element}/"

            f"{self.branch_element}>"

        )


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "Pillar",

]
