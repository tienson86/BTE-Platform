"""
BTE Platform

Engine Validator

Điểm vào duy nhất để kiểm tra toàn bộ
Interpretation Database.
"""

from __future__ import annotations

from pathlib import Path

from .schema_loader import SchemaLoader
from .data_loader import DataLoader
from .validator import DataValidator

from .dependency_checker import DependencyChecker
from .reference_checker import ReferenceChecker
from .variable_checker import VariableChecker

from .integrity_checker import IntegrityChecker


class EngineValidator:

    def __init__(

        self,

        schema_directory

    ):

        self.schema_loader = SchemaLoader(
            schema_directory
        )

        self.validator = DataValidator(
            self.schema_loader
        )

        self.reference_checker = ReferenceChecker()

        self.dependency_checker = DependencyChecker()

    def create_variable_checker(

        self,

        variable_schema_path

    ):

        schema = DataLoader.load_json(
            variable_schema_path
        )

        self.variable_checker = VariableChecker(
            schema
        )

    def build_checker(self):

        return IntegrityChecker(

            validator=self.validator,

            dependency_checker=self.dependency_checker,

            reference_checker=self.reference_checker,

            variable_checker=getattr(
                self,
                "variable_checker",
                None
            )

        )

    def validate_templates(

        self,

        template_rows

    ):

        checker = self.build_checker()

        return checker.validate_schema(

            template_rows,

            "template_schema"

        )

    def validate_sentences(

        self,

        sentence_rows

    ):

        checker = self.build_checker()

        schema_report = checker.validate_schema(

            sentence_rows,

            "sentence_schema"

        )

        variable_report = checker.validate_variables(

            sentence_rows

        )

        return checker.merge(

            schema_report,

            variable_report

        )

    def validate_reference(

        self,

        source_rows,

        source_field,

        target_rows,

        target_field

    ):

        checker = self.build_checker()

        return checker.validate_reference(

            source_rows,

            source_field,

            target_rows,

            target_field

        )

    def validate_dependencies(self):

        checker = self.build_checker()

        return checker.validate_dependency()

    def validate_all(

        self,

        template_rows,

        sentence_rows

    ):

        reports = [

            self.validate_templates(

                template_rows

            ),

            self.validate_sentences(

                sentence_rows

            ),

            self.validate_dependencies()

        ]

        return IntegrityChecker.merge(
            *reports
        )
