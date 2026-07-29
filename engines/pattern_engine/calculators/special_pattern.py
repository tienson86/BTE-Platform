"""
Kiểm tra Chuyên Cách.
"""


class SpecialPatternCalculator:

    SPECIAL_PATTERNS = {

        "Khúc Trực",

        "Viêm Thượng",

        "Nhuận Hạ",

        "Giá Sắc",

        "Tòng Vượng",

        "Tòng Cường",

    }

    def evaluate(self, pattern: str) -> bool:

        return pattern in self.SPECIAL_PATTERNS
