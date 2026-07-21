"""
validator.py
Golden Dataset Validator V2.0

PART 1/3
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


# ==========================================================
# Constants
# ==========================================================

DEFAULT_DATASET_ROOT = Path(__file__).parent

SCHEMA_FOLDER = "schemas"

INPUT_SCHEMA = "input_schema.json"

EXPECTED_SCHEMA = "expected_schema.json"

ENGINE_SCHEMAS = {

    "calendar_engine": "calendar_engine/schema.json",

    "bazi_engine": "bazi_engine/schema.json",

    "pattern_engine": "pattern_engine/schema.json",

    "score_engine": "score_engine/schema.json",

    "interpretation_engine": "interpretation_engine/schema.json",

    "report_engine": "report_engine/schema.json",

}


# ==========================================================
# Validation Error
# ==========================================================


@dataclass(slots=True)
class ValidationError:
    """
    Một lỗi validation.
    """

    file: str

    schema: str

    path: str

    message: str

    value: Any | None = None


# ==========================================================
# Validation Result
# ==========================================================


@dataclass(slots=True)
class ValidationResult:
    """
    Kết quả validate một file.
    """

    file: str

    schema: str

    valid: bool

    elapsed_ms: float

    errors: list[ValidationError] = field(default_factory=list)

    @property
    def error_count(self) -> int:

        return len(self.errors)


# ==========================================================
# Validation Summary
# ==========================================================


@dataclass(slots=True)
class ValidationSummary:
    """
    Tổng hợp kết quả.
    """

    total_files: int = 0

    passed_files: int = 0

    failed_files: int = 0

    elapsed_ms: float = 0.0

    results: list[ValidationResult] = field(default_factory=list)

    def add_result(
        self,
        result: ValidationResult,
    ) -> None:

        self.total_files += 1

        self.elapsed_ms += result.elapsed_ms

        self.results.append(result)

        if result.valid:

            self.passed_files += 1

        else:

            self.failed_files += 1

    @property
    def success(self) -> bool:

        return self.failed_files == 0


# ==========================================================
# Schema Registry
# ==========================================================


class SchemaRegistry:
    """
    Quản lý toàn bộ schema.
    """

    def __init__(
        self,
        schema_root: Path,
    ) -> None:

        self.schema_root = schema_root

        self._cache: dict[Path, Draft202012Validator] = {}

    # ------------------------------------------------------

    def has_schema(
        self,
        schema_name: str,
    ) -> bool:

        return (self.schema_root / schema_name).exists()

    # ------------------------------------------------------

    def load_schema(
        self,
        schema_name: str,
    ) -> Draft202012Validator:

        path = self.schema_root / schema_name

        if path not in self._cache:

            with path.open(
                "r",
                encoding="utf-8",
            ) as f:

                schema = json.load(f)

            self._cache[path] = Draft202012Validator(schema)

        return self._cache[path]

    # ------------------------------------------------------

    def detect_schema(
        self,
        json_file: Path,
    ) -> str | None:

        parts = json_file.parts

        if "input" in parts:

            return INPUT_SCHEMA

        if "expected" in parts:

            return EXPECTED_SCHEMA

        for engine, schema in ENGINE_SCHEMAS.items():

            if engine in parts:

                return schema

        return None


# ==========================================================
# Json Validator
# ==========================================================


class JsonValidator:
    """
    Validate một file JSON theo JSON Schema.
    """

    def __init__(
        self,
        registry: SchemaRegistry,
    ) -> None:

        self.registry = registry

    # ------------------------------------------------------

    def validate_file(
        self,
        json_file: Path,
    ) -> ValidationResult:

        start = time.perf_counter()

        schema_name = self.registry.detect_schema(json_file)

        if schema_name is None:

            elapsed = (time.perf_counter() - start) * 1000

            return ValidationResult(
                file=str(json_file),
                schema="UNKNOWN",
                valid=False,
                elapsed_ms=elapsed,
                errors=[
                    ValidationError(
                        file=str(json_file),
                        schema="UNKNOWN",
                        path="<root>",
                        message="Cannot detect schema.",
                    )
                ],
            )

        validator = self.registry.load_schema(schema_name)

        with json_file.open(
            "r",
            encoding="utf-8",
        ) as f:

            data = json.load(f)

        errors: list[ValidationError] = []

        for err in sorted(
            validator.iter_errors(data),
            key=lambda e: list(e.path),
        ):

            path = ".".join(
                map(str, err.path)
            )

            if path == "":
                path = "<root>"

            errors.append(

                ValidationError(

                    file=str(json_file),

                    schema=schema_name,

                    path=path,

                    message=err.message,

                    value=err.instance,

                )

            )

        elapsed = (time.perf_counter() - start) * 1000

        return ValidationResult(

            file=str(json_file),

            schema=schema_name,

            valid=len(errors) == 0,

            elapsed_ms=elapsed,

            errors=errors,

        )


# ==========================================================
# Directory Validator
# ==========================================================


class DirectoryValidator:
    """
    Validate toàn bộ Golden Dataset.
    """

    def __init__(
        self,
        dataset_root: Path | None = None,
    ) -> None:

        if dataset_root is None:
            self.dataset_root = DEFAULT_DATASET_ROOT
        else:
            self.dataset_root = dataset_root

        self.schema_root = self.dataset_root / SCHEMA_FOLDER

        self.registry = SchemaRegistry(self.schema_root)

        self.validator = JsonValidator(self.registry)

    # ------------------------------------------------------

    def validate_directory(
        self,
    ) -> ValidationSummary:

        summary = ValidationSummary()

        json_files = self.collect_json_files()

        for json_file in json_files:

            result = self.validator.validate_file(
                json_file,
            )

            summary.add_result(result)

        return summary

    # ------------------------------------------------------

    def collect_json_files(
        self,
    ) -> list[Path]:

        files: list[Path] = []

        for file in sorted(
            self.dataset_root.rglob("*.json")
        ):

            if SCHEMA_FOLDER in file.parts:
                continue

            files.append(file)

        return files

    # ------------------------------------------------------

    def validate_input(
        self,
    ) -> ValidationSummary:

        return self._validate_subfolder(
            "input"
        )

    # ------------------------------------------------------

    def validate_expected(
        self,
    ) -> ValidationSummary:

        return self._validate_subfolder(
            "expected"
        )

    # ------------------------------------------------------

    def validate_engine(
        self,
        engine_name: str,
    ) -> ValidationSummary:

        return self._validate_subfolder(
            f"snapshots/{engine_name}"
        )

    # ------------------------------------------------------

    def _validate_subfolder(
        self,
        folder: str,
    ) -> ValidationSummary:

        summary = ValidationSummary()

        target = self.dataset_root / folder

        if not target.exists():

            return summary

        for json_file in sorted(
            target.rglob("*.json")
        ):

            result = self.validator.validate_file(
                json_file
            )

            summary.add_result(result)

        return summary

    # ------------------------------------------------------

    def validate_calendar(
        self,
    ) -> ValidationSummary:

        return self.validate_engine(
            "calendar_engine"
        )

    # ------------------------------------------------------

    def validate_bazi(
        self,
    ) -> ValidationSummary:

        return self.validate_engine(
            "bazi_engine"
        )

    # ------------------------------------------------------

    def validate_pattern(
        self,
    ) -> ValidationSummary:

        return self.validate_engine(
            "pattern_engine"
        )

    # ------------------------------------------------------

    def validate_score(
        self,
    ) -> ValidationSummary:

        return self.validate_engine(
            "score_engine"
        )

    # ------------------------------------------------------

    def validate_interpretation(
        self,
    ) -> ValidationSummary:

        return self.validate_engine(
            "interpretation_engine"
        )

    # ------------------------------------------------------

    def validate_report(
        self,
    ) -> ValidationSummary:

        return self.validate_engine(
            "report_engine"
        )

    # ------------------------------------------------------

    def validate_all(
        self,
    ) -> dict[str, ValidationSummary]:

        return {

            "input": self.validate_input(),

            "expected": self.validate_expected(),

            "calendar": self.validate_calendar(),

            "bazi": self.validate_bazi(),

            "pattern": self.validate_pattern(),

            "score": self.validate_score(),

            "interpretation": self.validate_interpretation(),

            "report": self.validate_report(),

            "dataset": self.validate_directory(),

        }


# ==========================================================
# Console Report
# ==========================================================


def print_result(
    result: ValidationResult,
) -> None:

    status = "PASS"

    if not result.valid:
        status = "FAIL"

    print(
        f"[{status}] "
        f"{result.file} "
        f"({result.elapsed_ms:.2f} ms)"
    )

    if result.valid:
        return

    for error in result.errors:

        print(
            f"    Path    : {error.path}"
        )

        print(
            f"    Message : {error.message}"
        )

        print(
            f"    Value   : {repr(error.value)}"
        )

        print()


# ==========================================================
# Summary Report
# ==========================================================


def print_summary(
    summary: ValidationSummary,
) -> None:

    print("=" * 60)

    print("Golden Dataset Validation")

    print("=" * 60)

    print(
        f"Files    : {summary.total_files}"
    )

    print(
        f"Passed   : {summary.passed_files}"
    )

    print(
        f"Failed   : {summary.failed_files}"
    )

    print(
        f"Elapsed  : "
        f"{summary.elapsed_ms:.2f} ms"
    )

    print("=" * 60)

    for result in summary.results:

        print_result(result)


# ==========================================================
# CLI
# ==========================================================

import argparse
import sys


def create_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        prog="validator.py",
        description="Golden Dataset Validator V2.0",
    )

    parser.add_argument(
        "dataset",
        nargs="?",
        default="tests/golden_dataset",
        help="Golden Dataset root directory",
    )

    parser.add_argument(
        "--input",
        action="store_true",
        help="Validate input only",
    )

    parser.add_argument(
        "--expected",
        action="store_true",
        help="Validate expected only",
    )

    parser.add_argument(
        "--calendar",
        action="store_true",
        help="Validate Calendar Engine snapshot",
    )

    parser.add_argument(
        "--bazi",
        action="store_true",
        help="Validate Bazi Engine snapshot",
    )

    parser.add_argument(
        "--pattern",
        action="store_true",
        help="Validate Pattern Engine snapshot",
    )

    parser.add_argument(
        "--score",
        action="store_true",
        help="Validate Score Engine snapshot",
    )

    parser.add_argument(
        "--interpretation",
        action="store_true",
        help="Validate Interpretation Engine snapshot",
    )

    parser.add_argument(
        "--report",
        action="store_true",
        help="Validate Report Engine snapshot",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all files",
    )

    return parser


# ==========================================================
# Runner
# ==========================================================


def run_validation(
    args: argparse.Namespace,
) -> int:

    dataset_root = Path(args.dataset)

    if not dataset_root.exists():

        print()

        print(f"Dataset not found: {dataset_root}")

        return 1

    validator = DirectoryValidator(
        dataset_root,
    )

    if args.input:

        summary = validator.validate_input()

    elif args.expected:

        summary = validator.validate_expected()

    elif args.calendar:

        summary = validator.validate_calendar()

    elif args.bazi:

        summary = validator.validate_bazi()

    elif args.pattern:

        summary = validator.validate_pattern()

    elif args.score:

        summary = validator.validate_score()

    elif args.interpretation:

        summary = validator.validate_interpretation()

    elif args.report:

        summary = validator.validate_report()

    else:

        summary = validator.validate_directory()

    print_summary(summary)

    if summary.success:

        return 0

    return 1


# ==========================================================
# Main
# ==========================================================


def main() -> None:

    parser = create_parser()

    args = parser.parse_args()

    exit_code = run_validation(args)

    raise SystemExit(exit_code)


# ==========================================================
# Entry
# ==========================================================

if __name__ == "__main__":

    main()
