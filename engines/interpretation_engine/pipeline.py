"""
pipeline.py
===========

Điều phối toàn bộ Interpretation Engine.

Luồng xử lý:

Validator
    ↓
Context
    ↓
Rule Loader
    ↓
Rule Matcher
    ↓
Rule Scoring
    ↓
Priority
    ↓
Interpretation Builder
    ↓
Formatter
"""

from .validators import InterpretationValidator


class InterpretationPipeline:

    def __init__(
        self,
        context_builder,
        rule_loader,
        rule_matcher,
        rule_scoring,
        priority,
        interpretation_builder,
        formatter,
    ):

        self.context_builder = context_builder
        self.rule_loader = rule_loader
        self.rule_matcher = rule_matcher
        self.rule_scoring = rule_scoring
        self.priority = priority
        self.interpretation_builder = interpretation_builder
        self.formatter = formatter

    def run(self, chart):

        # 1. Xây dựng context
        context = self.context_builder.build(chart)

        # 2. Kiểm tra dữ liệu
        InterpretationValidator.validate(context)

        # 3. Nạp Rule
        rules = self.rule_loader.load_all()

        # 4. So khớp Rule
        matched = self.rule_matcher.match(
            context=context,
            rules=rules,
        )

        # 5. Chấm điểm
        scored = self.rule_scoring.score(matched)

        # 6. Sắp xếp ưu tiên
        ordered = self.priority.sort(scored)

        # 7. Xây dựng diễn giải
        interpretation = self.interpretation_builder.build(
            ordered,
            context,
        )

        # 8. Định dạng kết quả
        return self.formatter.format(
            interpretation
        )
