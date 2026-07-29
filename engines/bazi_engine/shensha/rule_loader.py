"""
===============================================================================
Bazi Engine - Shen Sha Rule Loader
-------------------------------------------------------------------------------
File:
    bazi_engine/shensha/rule_loader.py

Description:
    Rule Loader cho Shen Sha Engine.

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from pathlib import Path

from typing import Dict
from typing import List
from typing import Optional

from bazi_engine.core.base_rule_loader import (
    BaseRuleLoader,
)


# =============================================================================
# DATABASE
# =============================================================================

DATABASE_ROOT = "08_than_sat"

DATABASE_PATH = Path(DATABASE_ROOT)


# =============================================================================
# EXCEPTIONS
# =============================================================================

class ShenShaRuleLoaderError(Exception):
    """
    Base Exception.
    """


class ShenShaRuleNotFoundError(
    ShenShaRuleLoaderError,
):
    """
    Không tìm thấy Rule.
    """


# =============================================================================
# RULE LOADER
# =============================================================================

class ShenShaRuleLoader(BaseRuleLoader):
    """
    Rule Loader của Shen Sha Engine.

    Tự động nạp toàn bộ *.csv trong
    database/08_than_sat/
    """

    def __init__(
        self,
    ):

        self._rules: List[dict] = []

        self._rule_map: Dict[str, dict] = {}

        self._category_map: Dict[str, List[dict]] = {}

        self._trigger_map: Dict[str, List[dict]] = {}

        super().__init__()

    # -----------------------------------------------------------------
    # LOAD
    # -----------------------------------------------------------------

    def reload(
        self,
    ) -> None:
        """
        Nạp toàn bộ Rule Database.
        """

        self._rules.clear()

        self._rule_map.clear()

        self._category_map.clear()

        self._trigger_map.clear()

        csv_files = sorted(

            DATABASE_PATH.glob("*.csv")

        )

        for csv_file in csv_files:

            rows = self.load_csv(

                f"{DATABASE_ROOT}/{csv_file.name}"

            )

            self._rules.extend(rows)

        self._build_indexes()

        self.mark_loaded()
          # -----------------------------------------------------------------
    # BUILD INDEXES
    # -----------------------------------------------------------------

    def _build_indexes(
        self,
    ) -> None:
        """
        Xây dựng các Index để tăng tốc truy vấn.
        """

        for rule in self._rules:

            #
            # Code
            #

            code = rule.get("code", "")

            if code:

                self._rule_map[code] = rule

            #
            # Category
            #

            category = rule.get(
                "category",
                "",
            )

            if category:

                self._category_map.setdefault(

                    category,

                    []

                ).append(rule)

            #
            # Trigger
            #

            trigger = rule.get(

                "trigger_type",

                "",

            )

            if trigger:

                self._trigger_map.setdefault(

                    trigger,

                    []

                ).append(rule)

    # -----------------------------------------------------------------
    # GETTERS
    # -----------------------------------------------------------------

    def get_all_rules(
        self,
    ) -> List[dict]:
        """
        Toàn bộ Rule.
        """

        return self._rules


    # -----------------------------------------------------------------

    def get_rule(
        self,
        code: str,
    ) -> Optional[dict]:
        """
        Lấy Rule theo Code.
        """

        return self._rule_map.get(
            code
        )


    # -----------------------------------------------------------------

    def find_by_code(
        self,
        code: str,
    ) -> Optional[dict]:
        """
        Alias của get_rule().
        """

        return self.get_rule(
            code
        )


    # -----------------------------------------------------------------

    def find_by_category(
        self,
        category: str,
    ) -> List[dict]:
        """
        Tra cứu theo Category.
        """

        return self._category_map.get(

            category,

            [],

        )


    # -----------------------------------------------------------------

    def find_by_trigger(
        self,
        trigger: str,
    ) -> List[dict]:
        """
        Tra cứu theo Trigger.
        """

        return self._trigger_map.get(

            trigger,

            [],

        )
          # -----------------------------------------------------------------
    # BUILD ADVANCED INDEXES
    # -----------------------------------------------------------------

    def _build_advanced_indexes(
        self,
    ) -> None:
        """
        Xây dựng các Index nâng cao.
        """

        self._pillar_map: Dict[
            str,
            List[dict],
        ] = {}

        self._source_map: Dict[
            str,
            List[dict],
        ] = {}

        self._target_map: Dict[
            str,
            List[dict],
        ] = {}

        for rule in self._rules:

            #
            # Pillar
            #

            pillar = rule.get(
                "pillar",
                "",
            )

            if pillar:

                self._pillar_map.setdefault(

                    pillar,

                    []

                ).append(rule)

            #
            # Source
            #

            source = rule.get(
                "source",
                "",
            )

            if source:

                self._source_map.setdefault(

                    source,

                    []

                ).append(rule)

            #
            # Target
            #

            target = rule.get(
                "target",
                "",
            )

            if target:

                self._target_map.setdefault(

                    target,

                    []

                ).append(rule)


    # -----------------------------------------------------------------
    # ADVANCED QUERY
    # -----------------------------------------------------------------

    def find_by_pillar(
        self,
        pillar: str,
    ) -> List[dict]:
        """
        Tra cứu theo Trụ.
        """

        return self._pillar_map.get(

            pillar,

            [],

        )


    # -----------------------------------------------------------------

    def find_by_source(
        self,
        source: str,
    ) -> List[dict]:
        """
        Tra cứu theo nguồn kích hoạt.
        """

        return self._source_map.get(

            source,

            [],

        )


    # -----------------------------------------------------------------

    def find_by_target(
        self,
        target: str,
    ) -> List[dict]:
        """
        Tra cứu theo đối tượng.
        """

        return self._target_map.get(

            target,

            [],

        )


    # -----------------------------------------------------------------

    def search(
        self,
        **conditions,
    ) -> List[dict]:
        """
        Tìm Rule theo nhiều điều kiện.

        Ví dụ:

            search(
                category="cat_than",
                trigger_type="branch",
            )
        """

        results = self._rules

        for key, value in conditions.items():

            results = [

                rule

                for rule in results

                if str(

                    rule.get(key)

                ) == str(value)

            ]

        return results


    # -----------------------------------------------------------------

    def contains(
        self,
        code: str,
    ) -> bool:
        """
        Rule có tồn tại hay không.
        """

        return code in self._rule_map
          # -----------------------------------------------------------------
    # INFORMATION
    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, int]:
        """
        Thống kê Rule Database.
        """

        return {

            "rules":
                len(self._rules),

            "categories":
                len(self._category_map),

            "triggers":
                len(self._trigger_map),

            "pillars":
                len(self._pillar_map),

            "sources":
                len(self._source_map),

            "targets":
                len(self._target_map),

        }


    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra trạng thái Rule Loader.
        """

        return (

            self.loaded

            and

            len(self._rules) > 0

        )


    # -----------------------------------------------------------------

    def debug(
        self,
    ) -> Dict[str, object]:
        """
        Thông tin Debug.
        """

        return {

            "loader":
                self.__class__.__name__,

            "loaded":
                self.loaded,

            "statistics":
                self.statistics(),

        }


    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa toàn bộ dữ liệu trong bộ nhớ.
        """

        self._rules.clear()

        self._rule_map.clear()

        self._category_map.clear()

        self._trigger_map.clear()

        self._pillar_map.clear()

        self._source_map.clear()

        self._target_map.clear()

        super().clear_cache()


    # -----------------------------------------------------------------

    def __contains__(
        self,
        code: str,
    ) -> bool:
        """
        Kiểm tra Rule theo mã.
        """

        return code in self._rule_map


    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<ShenShaRuleLoader "

            f"rules={len(self._rules)} "

            f"loaded={self.loaded}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

shensha_rule_loader = ShenShaRuleLoader()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "ShenShaRuleLoader",

    "ShenShaRuleLoaderError",

    "ShenShaRuleNotFoundError",

    "shensha_rule_loader",

]
