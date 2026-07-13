"""
===============================================================================
Bazi Engine - Five Elements Rule Loader
-------------------------------------------------------------------------------
File:
    bazi_engine/five_elements/rule_loader.py

Description:
    Nạp dữ liệu quy tắc Ngũ Hành.

Database:

    Thiên Can  -> Ngũ Hành

    Địa Chi    -> Ngũ Hành

    Tàng Can   -> Ngũ Hành

    Sinh Khắc  -> Quan hệ Ngũ Hành


Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from typing import Dict
from typing import List
from typing import Optional


from database.loader import DatabaseLoader


# =============================================================================
# DATABASE PATH
# =============================================================================

STEM_ELEMENT_DATABASE = (
    "11_five_elements/stems_elements.csv"
)

BRANCH_ELEMENT_DATABASE = (
    "11_five_elements/branches_elements.csv"
)

HIDDEN_STEM_DATABASE = (
    "11_five_elements/"
    "hidden_stems_elements.csv"
)

GENERATING_DATABASE = (
    "11_five_elements/"
    "generating_cycle.csv"
)

CONTROLLING_DATABASE = (
    "11_five_elements/"
    "controlling_cycle.csv"
)


# =============================================================================
# EXCEPTIONS
# =============================================================================

class FiveElementRuleLoaderError(
    Exception,
):
    """
    Base Exception.
    """


class FiveElementRuleNotFoundError(
    FiveElementRuleLoaderError,
):
    """
    Không tìm thấy Rule.
    """



# =============================================================================
# RULE LOADER
# =============================================================================

class FiveElementRuleLoader:
    """
    Loader dữ liệu Ngũ Hành.
    """

    def __init__(
        self,
    ):

        self._loader = DatabaseLoader()


        self._stem_elements: Dict[
            str,
            dict,
        ] = {}


        self._branch_elements: Dict[
            str,
            dict,
        ] = {}


        self._hidden_stems: Dict[
            str,
            List[dict],
        ] = {}


        self._generating: List[
            dict
        ] = []


        self._controlling: List[
            dict
        ] = []


        self.reload()


    # -----------------------------------------------------------------

    def reload(
        self,
    ) -> None:
        """
        Load toàn bộ Rule.
        """

        self._load_stems()

        self._load_branches()

        self._load_hidden_stems()

        self._load_generating()

        self._load_controlling()


    # -----------------------------------------------------------------

    def _load_stems(
        self,
    ) -> None:
        """
        Load Thiên Can.
        """

        rows = self._loader.load_csv(
            STEM_ELEMENT_DATABASE
        )

        self._stem_elements.clear()


        for row in rows:

            self._stem_elements[
                row["stem"]
            ] = row


    # -----------------------------------------------------------------

    def _load_branches(
        self,
    ) -> None:
        """
        Load Địa Chi.
        """

        rows = self._loader.load_csv(
            BRANCH_ELEMENT_DATABASE
        )

        self._branch_elements.clear()


        for row in rows:

            self._branch_elements[
                row["branch"]
            ] = row
              # -----------------------------------------------------------------
    # LOAD HIDDEN STEMS
    # -----------------------------------------------------------------

    def _load_hidden_stems(
        self,
    ) -> None:
        """
        Load Tàng Can của Địa Chi.
        """

        rows = self._loader.load_csv(
            HIDDEN_STEM_DATABASE
        )

        self._hidden_stems.clear()


        for row in rows:

            branch = row["branch"]

            if branch not in self._hidden_stems:

                self._hidden_stems[branch] = []


            self._hidden_stems[branch].append(
                row
            )


    # -----------------------------------------------------------------

    def _load_generating(
        self,
    ) -> None:
        """
        Load vòng Sinh Ngũ Hành.
        """

        rows = self._loader.load_csv(
            GENERATING_DATABASE
        )

        self._generating = rows


    # -----------------------------------------------------------------

    def _load_controlling(
        self,
    ) -> None:
        """
        Load vòng Khắc Ngũ Hành.
        """

        rows = self._loader.load_csv(
            CONTROLLING_DATABASE
        )

        self._controlling = rows


    # -----------------------------------------------------------------
    # QUERY STEM
    # -----------------------------------------------------------------

    def get_stem_element(
        self,
        stem: str,
    ) -> dict:
        """
        Lấy Ngũ Hành của Thiên Can.
        """

        if stem not in self._stem_elements:

            raise FiveElementRuleNotFoundError(

                f"Không tìm thấy Thiên Can: {stem}"

            )


        return self._stem_elements[stem]


    # -----------------------------------------------------------------

    def has_stem(
        self,
        stem: str,
    ) -> bool:
        """
        Kiểm tra Thiên Can tồn tại.
        """

        return stem in self._stem_elements


    # -----------------------------------------------------------------
    # QUERY BRANCH
    # -----------------------------------------------------------------

    def get_branch_element(
        self,
        branch: str,
    ) -> dict:
        """
        Lấy Ngũ Hành của Địa Chi.
        """

        if branch not in self._branch_elements:

            raise FiveElementRuleNotFoundError(

                f"Không tìm thấy Địa Chi: {branch}"

            )


        return self._branch_elements[branch]


    # -----------------------------------------------------------------

    def has_branch(
        self,
        branch: str,
    ) -> bool:
        """
        Kiểm tra Địa Chi tồn tại.
        """

        return branch in self._branch_elements


    # -----------------------------------------------------------------
    # HIDDEN STEM
    # -----------------------------------------------------------------

    def get_hidden_stems(
        self,
        branch: str,
    ) -> List[dict]:
        """
        Lấy Tàng Can của Địa Chi.
        """

        return self._hidden_stems.get(

            branch,

            []

        )


    # -----------------------------------------------------------------
    # RELATION
    # -----------------------------------------------------------------

    def get_generating_rules(
        self,
    ) -> List[dict]:
        """
        Lấy quan hệ Sinh.
        """

        return self._generating


    # -----------------------------------------------------------------

    def get_controlling_rules(
        self,
    ) -> List[dict]:
        """
        Lấy quan hệ Khắc.
        """

        return self._controlling


    # -----------------------------------------------------------------

    def get_relation(
        self,
        source: str,
        target: str,
    ) -> Optional[str]:
        """
        Tra cứu quan hệ giữa hai Ngũ Hành.
        """

        for rule in self._generating:

            if (

                rule["source"] == source

                and

                rule["target"] == target

            ):

                return "Sinh"


        for rule in self._controlling:

            if (

                rule["source"] == source

                and

                rule["target"] == target

            ):

                return "Khắc"


        return None


    # -----------------------------------------------------------------
    # INFORMATION
    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, int]:
        """
        Thống kê dữ liệu.
        """

        return {

            "stems":
                len(self._stem_elements),

            "branches":
                len(self._branch_elements),

            "hidden_stems":
                len(self._hidden_stems),

            "generating":
                len(self._generating),

            "controlling":
                len(self._controlling),

        }


    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra dữ liệu.
        """

        return (

            len(self._stem_elements) == 10

            and

            len(self._branch_elements) == 12

            and

            len(self._generating) > 0

            and

            len(self._controlling) > 0

        )


    # -----------------------------------------------------------------

    def refresh(
        self,
    ) -> None:
        """
        Reload Database.
        """

        self.reload()


    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa dữ liệu trong RAM.
        """

        self._stem_elements.clear()

        self._branch_elements.clear()

        self._hidden_stems.clear()

        self._generating.clear()

        self._controlling.clear()


    # -----------------------------------------------------------------

    def debug(
        self,
    ) -> Dict[str, object]:
        """
        Debug information.
        """

        return {

            "health":
                self.health_check(),

            "statistics":
                self.statistics(),

        }


    # -----------------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return (

            len(self._stem_elements)

            +

            len(self._branch_elements)

        )


    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<FiveElementRuleLoader "

            f"stems={len(self._stem_elements)} "

            f"branches={len(self._branch_elements)}>"

        )



# =============================================================================
# SINGLETON
# =============================================================================

five_element_rule_loader = FiveElementRuleLoader()



# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "FiveElementRuleLoader",

    "FiveElementRuleLoaderError",

    "FiveElementRuleNotFoundError",

    "five_element_rule_loader",

]
