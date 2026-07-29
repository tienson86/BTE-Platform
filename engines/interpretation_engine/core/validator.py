"""
Data Validator

Kiểm tra dữ liệu theo JSON Schema.
"""

from __future__ import annotations

from jsonschema import Draft202012Validator


class ValidationError(Exception):
    pass


class DataValidator:

    def __init__(self, schema_loader):

        self.schema_loader = schema_loader

    def validate(self, data, schema_name):

        schema = self.schema_loader.load(schema_name)

        validator = Draft202012Validator(schema)

        errors = sorted(

            validator.iter_errors(data),

            key=lambda e: e.path

        )

        return errors

    def validate_or_raise(self, data, schema_name):

        errors = self.validate(data, schema_name)

        if errors:

            messages = []

            for err in errors:

                path = ".".join(map(str, err.path))

                messages.append(f"{path}: {err.message}")

            raise ValidationError("\n".join(messages))

        return True
