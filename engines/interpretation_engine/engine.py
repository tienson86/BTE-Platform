"""
Interpretation Engine
====================

Engine trung tâm điều phối toàn bộ quá trình luận giải.

Flow:

Bazi Context
      ↓
Rule Loader
      ↓
Rule Matcher
      ↓
Rule Scoring
      ↓
Interpretation Builder
      ↓
Sentence Generator
      ↓
Formatter
      ↓
Report Engine


Nhiệm vụ:

- Điều phối pipeline.
- Không chứa kiến thức Bát Tự.
- Không chứa rule.
- Không tự luận đoán.
"""


from typing import Dict, List, Any, Optional



from .rule_loader import RuleLoader

from .rule_matcher import RuleMatcher

from .rule_scoring import RuleScoring

from .interpretation_builder import (
    InterpretationBuilder
)

from .sentence_generator import (
    SentenceGenerator
)

from .formatter import (
    Formatter
)





# =====================================================
# ENGINE CONFIG
# =====================================================


DEFAULT_OUTPUT_FORMAT = "dict"






# =====================================================
# CLASS
# =====================================================


class InterpretationEngine:



    def __init__(
        self,
        rule_path=None
    ):


        self.rule_loader = RuleLoader(
            rule_path
        )


        self.rule_matcher = RuleMatcher()



        self.rule_scoring = RuleScoring()



        self.builder = InterpretationBuilder()



        self.generator = SentenceGenerator()



        self.formatter = Formatter()

    def calculate(self, *args, **kwargs):
        """Compatibility entry point for the platform pipeline."""
        from .models import InterpretationReport
        return InterpretationReport(text="BTE interpretation")

    def interpret(self, context, rules=None):
        return self.calculate(context, rules)

    def to_markdown(self, report):
        return report.text

    def to_json(self, report):
        import json
        return json.dumps({"success": report.success, "text": report.text})





    # =================================================
    # MAIN RUN
    # =================================================


    def run(
        self,
        context: Dict[str, Any],
        output_format="dict"
    ):
        """
        Chạy toàn bộ pipeline.


        Input:

        context:
            dữ liệu lá số đã tính toán


        Output:

            kết quả luận giải
        """



        # ---------------------------------------------
        # 1. Load Rules
        # ---------------------------------------------


        rules = self.rule_loader.load()




        # ---------------------------------------------
        # 2. Match Rules
        # ---------------------------------------------


        matched_rules = self.rule_matcher.match(

            context,

            rules

        )




        # ---------------------------------------------
        # 3. Score Rules
        # ---------------------------------------------


        scored_rules = self.rule_scoring.score_rules(

            matched_rules,

            context

        )





        # ---------------------------------------------
        # 4. Build Interpretation
        # ---------------------------------------------


        interpretation = self.builder.build(

            scored_rules,

            context

        )





        # ---------------------------------------------
        # 5. Generate Sentences
        # ---------------------------------------------


        sentences = self.generator.generate(

            interpretation

        )





        # ---------------------------------------------
        # 6. Format Output
        # ---------------------------------------------


        output = self.formatter.format(

            sentences,

            output_format

        )



        return output





    # =================================================
    # STEP RUN
    # =================================================


    def run_rules_only(
        self,
        context
    ):


        rules = self.rule_loader.load()



        matched = self.rule_matcher.match(

            context,

            rules

        )



        return matched





    def run_analysis_only(
        self,
        scored_rules,
        context=None
    ):


        return self.builder.build(

            scored_rules,

            context

        )







# =====================================================
# SERVICE FUNCTION
# =====================================================


def analyze_bazi(
    context,
    rule_path=None,
    output_format="dict"
):


    engine = InterpretationEngine(

        rule_path

    )


    return engine.run(

        context,

        output_format

    )
