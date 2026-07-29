"""
Rule Matcher.
"""

from ..matcher import PatternMatcher


class RuleMatcher:

    def __init__(self):

        self.matcher = PatternMatcher()

    def match(self, context, rules):

        matched = []

        for rule in rules:

            if self.matcher.match(

                context,

                {

                    "conditions": rule.conditions

                }

            ):

                matched.append(rule)

        return matched
