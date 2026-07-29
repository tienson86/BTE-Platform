"""
===============================================================================
Bazi Engine - Shen Sha Calculator
-------------------------------------------------------------------------------
File:
    bazi_engine/shensha/calculator.py

Description:
    Engine tính toán Thần Sát.

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from typing import Dict
from typing import List

from bazi_engine.core.base_calculator import BaseCalculator

from bazi_engine.models import FourPillars

from .rule_loader import (
    shensha_rule_loader,
)

from .shensha import (
    ShenSha,
    ShenShaOccurrence,
    ShenShaResult,
)


# =============================================================================
# EXCEPTIONS
# =============================================================================

class ShenShaCalculatorError(Exception):
    """
    Base Exception.
    """


class ShenShaCalculationError(
    ShenShaCalculatorError,
):
    """
    Calculation Error.
    """


# =============================================================================
# CALCULATOR
# =============================================================================

class ShenShaCalculator(BaseCalculator):
    """
    Engine lập Thần Sát.
    """

    def __init__(self):

        super().__init__()

        self._loader = shensha_rule_loader

        self.mark_loaded()

    # -----------------------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------------------

    def build_context(
        self,
        pillars: FourPillars,
    ) -> Dict:
        """
        Xây dựng Context.
        """

        return {

            "pillars": pillars,

            "year_stem":
                pillars.year.stem,

            "month_stem":
                pillars.month.stem,

            "day_stem":
                pillars.day.stem,

            "hour_stem":
                pillars.hour.stem,

            "year_branch":
                pillars.year.branch,

            "month_branch":
                pillars.month.branch,

            "day_branch":
                pillars.day.branch,

            "hour_branch":
                pillars.hour.branch,

            "year_hidden":
                pillars.year.hidden_stems,

            "month_hidden":
                pillars.month.hidden_stems,

            "day_hidden":
                pillars.day.hidden_stems,

            "hour_hidden":
                pillars.hour.hidden_stems,

        }

    # -----------------------------------------------------------------
    # MATCH STEM
    # -----------------------------------------------------------------

    def match_stem_rules(
        self,
        context: Dict,
    ) -> List[dict]:
        """
        Ghép các Rule theo Thiên Can.
        """

        rules = self._loader.find_by_trigger(
            "stem"
        )

        matched = []

        stems = {

            context["year_stem"],
            context["month_stem"],
            context["day_stem"],
            context["hour_stem"],

        }

        for rule in rules:

            trigger = rule.get(
                "trigger_value",
                "",
            )

            if trigger in stems:

                matched.append(rule)

        return matched

    # -----------------------------------------------------------------
    # MATCH BRANCH
    # -----------------------------------------------------------------

    def match_branch_rules(
        self,
        context: Dict,
    ) -> List[dict]:
        """
        Ghép các Rule theo Địa Chi.
        """

        rules = self._loader.find_by_trigger(
            "branch"
        )

        matched = []

        branches = {

            context["year_branch"],
            context["month_branch"],
            context["day_branch"],
            context["hour_branch"],

        }

        for rule in rules:

            trigger = rule.get(
                "trigger_value",
                "",
            )

            if trigger in branches:

                matched.append(rule)

        return matched
          # -----------------------------------------------------------------
    # MATCH HIDDEN STEM
    # -----------------------------------------------------------------

    def match_hidden_stem_rules(
        self,
        context: Dict,
    ) -> List[dict]:
        """
        Ghép Rule theo Tàng Can.
        """

        rules = self._loader.find_by_trigger(
            "hidden_stem"
        )

        matched: List[dict] = []

        hidden_stems = set()

        hidden_stems.update(
            context["year_hidden"]
        )

        hidden_stems.update(
            context["month_hidden"]
        )

        hidden_stems.update(
            context["day_hidden"]
        )

        hidden_stems.update(
            context["hour_hidden"]
        )

        for rule in rules:

            trigger = rule.get(
                "trigger_value",
                "",
            )

            if trigger in hidden_stems:

                matched.append(rule)

        return matched


    # -----------------------------------------------------------------
    # MATCH COMBINATION
    # -----------------------------------------------------------------

    def match_combination_rules(
        self,
        context: Dict,
    ) -> List[dict]:
        """
        Ghép các Rule tổ hợp.

        V1:
            Placeholder.

        V2:
            Tam Hợp
            Tam Hội
            Lục Hợp
            Xung
            Hình
            Hại
            Phá
        """

        return []


    # -----------------------------------------------------------------
    # MATCH SPECIAL
    # -----------------------------------------------------------------

    def match_special_rules(
        self,
        context: Dict,
    ) -> List[dict]:
        """
        Ghép Rule đặc biệt.

        V1:
            Placeholder.
        """

        return []


    # -----------------------------------------------------------------
    # COLLECT
    # -----------------------------------------------------------------

    def collect_rules(
        self,
        context: Dict,
    ) -> List[dict]:
        """
        Thu thập toàn bộ Rule.
        """

        matched: List[dict] = []

        matched.extend(

            self.match_stem_rules(
                context
            )

        )

        matched.extend(

            self.match_branch_rules(
                context
            )

        )

        matched.extend(

            self.match_hidden_stem_rules(
                context
            )

        )

        matched.extend(

            self.match_combination_rules(
                context
            )

        )

        matched.extend(

            self.match_special_rules(
                context
            )

        )

        #
        # Remove duplicate
        #

        unique = {}

        for rule in matched:

            unique[
                rule["code"]
            ] = rule

        return list(

            unique.values()

        )
          # -----------------------------------------------------------------
    # BUILD SHEN SHA
    # -----------------------------------------------------------------

    def build_shensha(
        self,
        rule: dict,
    ) -> ShenSha:
        """
        Rule -> ShenSha
        """

        return ShenSha(

            code=rule.get(
                "code",
                "",
            ),

            name=rule.get(
                "name",
                "",
            ),

            category=rule.get(
                "category",
                "",
            ),

            level=rule.get(
                "level",
                "",
            ),

            element=rule.get(
                "element",
                "",
            ),

            yin_yang=rule.get(
                "yin_yang",
                "",
            ),

            description=rule.get(
                "description",
                "",
            ),

            effect=rule.get(
                "effect",
                "",
            ),

            priority=int(
                rule.get(
                    "priority",
                    0,
                )
            ),

            score=float(
                rule.get(
                    "score",
                    0,
                )
            ),

            metadata=rule,

        )


    # -----------------------------------------------------------------
    # BUILD OCCURRENCE
    # -----------------------------------------------------------------

    def build_occurrence(
        self,
        rule: dict,
    ) -> ShenShaOccurrence:
        """
        Rule -> ShenShaOccurrence
        """

        return ShenShaOccurrence(

            shensha=self.build_shensha(
                rule
            ),

            pillar=rule.get(
                "pillar",
                "",
            ),

            position=rule.get(
                "position",
                "",
            ),

            source=rule.get(
                "source",
                "",
            ),

            value=rule.get(
                "trigger_value",
                "",
            ),

            active=True,

            metadata=rule,

        )


    # -----------------------------------------------------------------
    # CLASSIFY
    # -----------------------------------------------------------------

    def classify(
        self,
        occurrences: List[ShenShaOccurrence],
        result: ShenShaResult,
    ) -> None:
        """
        Phân loại Thần Sát.
        """

        for occurrence in occurrences:

            result.add(
                occurrence
            )

            category = (

                occurrence.shensha.category

                .lower()

            )

            if category in (

                "auspicious",

                "cat",

                "cat_than",

            ):

                result.auspicious.append(

                    occurrence.shensha

                )

            elif category in (

                "inauspicious",

                "hung",

                "hung_than",

            ):

                result.inauspicious.append(

                    occurrence.shensha

                )

            else:

                result.neutral.append(

                    occurrence.shensha

                )


    # -----------------------------------------------------------------
    # SORT
    # -----------------------------------------------------------------

    def sort_occurrences(
        self,
        occurrences: List[
            ShenShaOccurrence
        ],
    ) -> List[
        ShenShaOccurrence
    ]:
        """
        Sắp xếp theo Priority.
        """

        occurrences.sort(

            key=lambda item: (

                item.shensha.priority,

                -item.shensha.score,

            )

        )

        return occurrences
          # -----------------------------------------------------------------
    # BUILD RESULT
    # -----------------------------------------------------------------

    def build_result(
        self,
        occurrences: List[ShenShaOccurrence],
        context: Dict,
    ) -> ShenShaResult:
        """
        Xây dựng ShenShaResult.
        """

        result = ShenShaResult()

        #
        # Sort
        #

        occurrences = self.sort_occurrences(
            occurrences
        )

        #
        # Classify
        #

        self.classify(
            occurrences,
            result,
        )

        #
        # Metadata
        #

        result.metadata = {

            "engine":
                self.__class__.__name__,

            "occurrence_count":
                len(occurrences),

            "context":
                context,

        }

        return result


    # -----------------------------------------------------------------
    # MAIN
    # -----------------------------------------------------------------

    def calculate(
        self,
        pillars: FourPillars,
    ) -> ShenShaResult:
        """
        API chính của ShenSha Engine.
        """

        self.ensure_loaded()

        #
        # Context
        #

        context = self.build_context(
            pillars
        )

        #
        # Match Rules
        #

        matched_rules = self.collect_rules(
            context
        )

        #
        # Occurrences
        #

        occurrences = [

            self.build_occurrence(rule)

            for rule in matched_rules

        ]

        #
        # Result
        #

        return self.build_result(

            occurrences,

            context,

        )


    # -----------------------------------------------------------------
    # INFORMATION
    # -----------------------------------------------------------------

    @property
    def version(
        self,
    ) -> str:
        """
        Phiên bản Calculator.
        """

        return "1.0.0"


    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, object]:
        """
        Thống kê ShenSha Engine.
        """

        return {

            "calculator":
                self.__class__.__name__,

            "version":
                self.version,

            "rule_loader":
                self._loader.statistics(),

        }


    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra trạng thái Calculator.
        """

        return (

            self.loaded

            and

            self._loader.health_check()

        )
          # -----------------------------------------------------------------
    # CACHE
    # -----------------------------------------------------------------

    def refresh(
        self,
    ) -> None:
        """
        Reload Rule Database.
        """

        self._loader.refresh()

        self.mark_loaded()


    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa cache của Calculator.
        """

        self._loader.clear_cache()

        self.mark_unloaded()


    # -----------------------------------------------------------------
    # DEBUG
    # -----------------------------------------------------------------

    def debug(
        self,
    ) -> Dict[str, object]:
        """
        Thông tin Debug.
        """

        return {

            "calculator":
                self.__class__.__name__,

            "version":
                self.version,

            "loaded":
                self.loaded,

            "health":
                self.health_check(),

            "statistics":
                self.statistics(),

            "rule_loader":
                repr(self._loader),

        }


    # -----------------------------------------------------------------
    # MAGIC METHODS
    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<ShenShaCalculator "

            f"version={self.version} "

            f"loaded={self.loaded}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

shensha_calculator = ShenShaCalculator()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "ShenShaCalculator",

    "ShenShaCalculatorError",

    "ShenShaCalculationError",

    "shensha_calculator",

]
