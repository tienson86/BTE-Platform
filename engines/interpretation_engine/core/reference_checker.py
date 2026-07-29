"""
Reference Checker

Kiểm tra Foreign Key giữa các bảng dữ liệu.
"""

from __future__ import annotations


class ReferenceError(Exception):
    """Lỗi tham chiếu."""


class ReferenceChecker:

    def __init__(self):

        self.errors = []

    def check_reference(
        self,
        source_rows,
        source_field,
        target_rows,
        target_field
    ):

        target_values = {

            row[target_field]

            for row in target_rows

            if target_field in row

        }

        self.errors.clear()

        for index, row in enumerate(source_rows):

            value = row.get(source_field)

            if value is None:
                continue

            if value not in target_values:

                self.errors.append({

                    "row": index + 1,

                    "field": source_field,

                    "value": value,

                    "message": "Reference not found"

                })

        return len(self.errors) == 0

    def has_errors(self):

        return len(self.errors) > 0

    def get_errors(self):

        return self.errors

    def raise_if_errors(self):

        if self.errors:

            messages = []

            for err in self.errors:

                messages.append(
                    f"Dòng {err['row']} : "
                    f"{err['field']} = {err['value']} "
                    f"không tồn tại."
                )

            raise ReferenceError(
                "\n".join(messages)
            )
