"""
Variable Checker

Kiểm tra các placeholder trong Sentence.

Ví dụ:

{day_master}

{strength}

{pattern}
"""

from __future__ import annotations

import re


class VariableError(Exception):
    """Lỗi biến."""


class VariableChecker:

    VARIABLE_PATTERN = re.compile(r"\{([A-Za-z0-9_]+)\}")

    def __init__(self, variable_schema):

        self.allowed = {

            item["name"]

            for item in variable_schema["variables"]

        }

        self.errors = []

    def extract(self, text):

        return self.VARIABLE_PATTERN.findall(text)

    def validate(self, text):

        self.errors.clear()

        variables = self.extract(text)

        for variable in variables:

            if variable not in self.allowed:

                self.errors.append(variable)

        return len(self.errors) == 0

    def validate_rows(self, rows):

        self.errors.clear()

        invalid = []

        for index, row in enumerate(rows):

            text = row.get("text", "")

            variables = self.extract(text)

            for var in variables:

                if var not in self.allowed:

                    invalid.append({

                        "row": index + 1,

                        "variable": var

                    })

        self.errors = invalid

        return len(self.errors) == 0

    def raise_if_errors(self):

        if self.errors:

            messages = []

            for err in self.errors:

                messages.append(
                    f"Dòng {err['row']} "
                    f"biến {{{err['variable']}}} "
                    f"không được khai báo."
                )

            raise VariableError(
                "\n".join(messages)
            )
