"""
Generic Score Calculator

Lớp cơ sở dùng chung cho hầu hết Calculator của Score Engine.

Pipeline chuẩn:

    Load Rules
        ↓
    Validate
        ↓
    Match
        ↓
    Score
        ↓
    Normalize
        ↓
    Build Result

Các Calculator cụ thể chỉ cần khai báo:

    MODULE_NAME
    RULE_FOLDER
"""

from abc import ABC

from .base_calculator import BaseCalculator

from ..utils.validator import ScoreValidator
from ..utils.scorer import RuleScorer
from ..utils.normalizer import ScoreNormalizer

from ..matcher.matcher import RuleMatcher


class GenericScoreCalculator(BaseCalculator, ABC):

    MODULE_NAME = ""

    RULE_FOLDER = ""

    def __init__(self, loader):

        super().__init__(loader)

        self.matcher = RuleMatcher()

        self.validator = ScoreValidator()

        self.normalizer = ScoreNormalizer()

        self.scorer = RuleScorer()

    # =====================================================

    # Main Pipeline

    # =====================================================

    def calculate(self, context):

        result = self.create_result()

        #
        # Reset scorer
        #

        self.scorer.reset()

        #
        # Load toàn bộ Rule trong thư mục
        #

        groups = self.loader.load_group(
            self.RULE_FOLDER
        )

        loaded_files = []

        matched_rules = []

        #
        # Duyệt từng file
        #

        for file_name, dataframe in groups.items():

            loaded_files.append(file_name)

            #
            # Validate CSV
            #

            self.validator.validate_dataframe(
                dataframe
            )

            #
            # Match Rule
            #

            rules = self.matcher.match(
                dataframe,
                context,
            )

            #
            # Score
            #

            for rule in rules:

                score = float(
                    rule.get(
                        "score",
                        0
                    )
                )

                rule_code = rule.get(
                    "rule_code",
                    ""
                )

                description = rule.get(
                    "description",
                    ""
                )

                if score >= 0:

                    self.scorer.add(
                        score,
                        rule_code,
                        description,
                    )

                else:

                    self.scorer.subtract(
                        abs(score),
                        rule_code,
                        description,
                    )

                matched_rules.append(rule)

        #
        # Normalize
        #

        final_score = self.normalizer.clamp(
            self.scorer.score
        )

        #
        # Result
        #

        result.module = self.MODULE_NAME

        result.score = final_score

        result.weighted_score = final_score

        result.matched_rules = matched_rules

        result.details = {

            "rule_folder": self.RULE_FOLDER,

            "loaded_files": loaded_files,

            "matched_rule_count": len(
                matched_rules
            ),

            "history": self.scorer.history,

        }

        return result

    # =====================================================

    # Helper

    # =====================================================

    def get_rule_folder(self):

        return self.RULE_FOLDER

    def get_module_name(self):

        return self.MODULE_NAME

    def __repr__(self):

        return (
            f"<{self.__class__.__name__}"
            f" module={self.MODULE_NAME}>"
        )
