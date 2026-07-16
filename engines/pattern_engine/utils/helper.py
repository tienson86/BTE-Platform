"""
Các hàm hỗ trợ Pattern Engine.
"""


class PatternHelper:

    @staticmethod
    def normalize(text):

        if text is None:

            return ""

        return str(text).strip()

    @staticmethod
    def is_empty(value):

        return value in (None, "", [], {}, ())
