"""
Generic Score Calculator

Template Method cho các Score Calculator.
"""

from .base_calculator import BaseCalculator

from ..matcher import RuleMatcher
from ..utils.validator import ScoreValidator
from ..utils.scorer import RuleScorer
from ..utils.normalizer import ScoreNormalizer


class GenericScoreCalculator(BaseCalculator):

    RULE_FOLDER = ""

    def __init__(self, loader):

        super().__init__(loader)

        self.matcher = RuleMatcher()

        self.validator = ScoreValidator()

        self.scorer = RuleScorer()

        self.normalizer = ScoreNormalizer()

    # ==================================================

    def load_rules(self):

        return self.loader.load_group(
            self.RULE_FOLDER
        )

    def validate_rules(self, dataframe):

        self.validator.validate_dataframe(
            dataframe
        )

    def match_rules(
        self,
        dataframe,
        context
    ):

        return self.matcher.match(
            dataframe,
            context
        )

    def calculate_score(
        self,
        matched_rules
    ):

        self.scorer.reset()

        for rule in matched_rules:

            score = float(
                rule.get("score", 0)
            )

            if score >= 0:

                self.scorer.add(
                    score,
                    rule.get("rule_code", ""),
                    rule.get("description", ""),
                )

            else:

                self.scorer.subtract(
                    abs(score),
                    rule.get("rule_code", ""),
                    rule.get("description", ""),
                )

        return self.scorer.score

    def normalize_score(
        self,
        score
    ):

        return self.normalizer.clamp(score)

    def build_result(
        self,
        result,
        matched_rules,
        score
    ):

        result.score = score

        result.weighted_score = score

        result.weight = 1.0

        result.matched_rules = matched_rules

        result.history = self.scorer.history

        return result

    def post_process(
        self,
        result,
        context
    ):

        return result

    # ==================================================

    def calculate(
        self,
        context
    ):

        result = self.create_result()

        groups = self.load_rules()

        matched = []

        for _, dataframe in groups.items():

            if (
                "condition" not in dataframe.columns
                or "score" not in dataframe.columns
            ):
                continue

            self.validate_rules(dataframe)

            matched.extend(

                self.match_rules(
                    dataframe,
                    context
                )

            )

        score = self.calculate_score(
            matched
        )

        score = self.normalize_score(
            score
        )

        result = self.build_result(
            result,
            matched,
            score
        )

        return self.post_process(
            result,
            context
        )
