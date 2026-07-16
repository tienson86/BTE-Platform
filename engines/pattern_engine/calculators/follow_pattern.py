"""
Kiểm tra Tòng Cách.
"""


class FollowPatternCalculator:

    FOLLOW_PATTERNS = {

        "Tòng Tài",

        "Tòng Quan",

        "Tòng Sát",

        "Tòng Nhi",

        "Tòng Thế",

    }

    def evaluate(self, pattern: str) -> bool:

        return pattern in self.FOLLOW_PATTERNS
