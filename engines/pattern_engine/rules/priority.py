"""
Priority Resolver.
"""

from typing import List

from ..models.pattern_rule import PatternRule


class PriorityResolver:

    @staticmethod
    def resolve(

        rules: List[PatternRule]

    ) -> PatternRule | None:

        if not rules:

            return None

        return max(

            rules,

            key=lambda x: (

                x.priority,

                x.score

            )

        )
