"""
Health Check

Kiểm tra toàn bộ Interpretation Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class HealthResult:

    success: bool = True

    checks: dict = field(default_factory=dict)

    errors: list = field(default_factory=list)

    warnings: list = field(default_factory=list)


class HealthCheck:

    def __init__(

        self,

        registry=None,

        schema_loader=None,

        validator=None,

        plugin_manager=None

    ):

        self.registry = registry

        self.schema_loader = schema_loader

        self.validator = validator

        self.plugin_manager = plugin_manager

    def run(self):

        result = HealthResult()

        # Registry

        if self.registry:

            result.checks["modules"] = self.registry.count()

            if self.registry.count() == 0:

                result.success = False

                result.errors.append(

                    "Registry chưa có module nào."

                )

        # Schema

        if self.schema_loader:

            schemas = self.schema_loader.list()

            result.checks["schemas"] = len(schemas)

            if len(schemas) == 0:

                result.success = False

                result.errors.append(

                    "Không tìm thấy schema."

                )

        # Plugin

        if self.plugin_manager:

            result.checks["plugins"] = len(

                self.plugin_manager.list_plugins()

            )

        return result

    def print_report(self, result):

        print("=" * 60)

        print("BTE HEALTH CHECK")

        print("=" * 60)

        print()

        print("Success :", result.success)

        print()

        for key, value in result.checks.items():

            print(f"{key:15} : {value}")

        print()

        if result.errors:

            print("ERRORS")

            for err in result.errors:

                print(" -", err)

        if result.warnings:

            print()

            print("WARNINGS")

            for warn in result.warnings:

                print(" -", warn)

        print()

        print("=" * 60)
