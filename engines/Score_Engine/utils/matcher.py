"""
Rule Matcher

Chức năng:

- Kiểm tra Rule có khớp hay không.
- Trả về danh sách Rule đã match.
"""

from typing import Dict, List


class RuleMatcher:

    def __init__(self):
        pass

    def match(
        self,
        rules,
        context
    ) -> List[Dict]:
        """
        Match Rule.

        Hiện tại là skeleton.

        Sau này sẽ parse:

            condition

        trong CSV.
        """

        matched = []

        for _, rule in rules.iterrows():

            if self.evaluate(rule, context):

                matched.append(rule.to_dict())

        return matched

    def evaluate(
        self,
        rule,
        context
    ) -> bool:
        """
        Đánh giá một Rule.

        TODO:

        Parser Expression
        """

        #
        # Tạm thời:
        #

        return False
