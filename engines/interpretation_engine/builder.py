"""
.. deprecated:: WP0B
    Stub builder. Active pipeline dùng ``legacy_builder.InterpretationBuilder``.
    Giữ lại để tương thích; refactor ở WP1.
"""

from .models import InterpretationReport


class InterpretationBuilder:
    def build(self, context):
        return InterpretationReport(text="BTE interpretation")
