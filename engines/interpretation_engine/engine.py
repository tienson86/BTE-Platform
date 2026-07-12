
from .rule_loader import RuleLoader
from .rule_matcher import RuleMatcher
from .rule_scoring import RuleScoring
from .interpretation_builder import InterpretationBuilder
from .sentence_generator import SentenceGenerator



class InterpretationEngine:



    def __init__(self):

        self.loader = RuleLoader()

        self.matcher = RuleMatcher()

        self.scoring = RuleScoring()

        self.builder = InterpretationBuilder()

        self.generator = SentenceGenerator()



    def run(
        self,
        rule_file,
        chart_data
    ):


        #1 Load CSV

        rules = self.loader.load_csv(
            rule_file
        )



        #2 Match

        matched = self.matcher.match_rules(
            rules,
            chart_data
        )



        #3 Score

        scored = self.scoring.scoring_rules(
            matched
        )



        #4 Build

        grouped = self.builder.build(
            scored
        )



        #5 Generate

        result=self.generator.generate(
            grouped
        )



        return {

            "matched_rules": scored,

            "interpretation": result

        }
