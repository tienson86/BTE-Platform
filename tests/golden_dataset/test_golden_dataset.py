"""
Golden Dataset Integration Test

Pipeline

Inputs
    ↓
Runner
    ↓
Snapshots
    ↓
Validator
    ↓
Comparator
    ↓
Report
    ↓
Pytest
"""

from __future__ import annotations

import pytest

from engines.interpretation_engine.engine import InterpretationEngine

from tests.golden_dataset.runner import run_all_cases
from tests.golden_dataset.validator import DirectoryValidator
from tests.golden_dataset.compare import compare_all_cases
from tests.golden_dataset.report import (
    CaseReport,
    export_markdown,
    export_csv,
    export_html,
)


def test_golden_dataset() -> None:
    """
    Chạy toàn bộ Golden Dataset.
    """

    # ======================================================
    # Run Engine
    # ======================================================

    engine = InterpretationEngine()

    run_all_cases(engine)

    # ======================================================
    # Validate Dataset
    # ======================================================

    validator = DirectoryValidator()

    validation_summary = validator.validate_directory()

    validation_errors = {}

    for result in validation_summary.results:

        case_name = result.file.stem

        validation_errors[case_name] = result.errors

    # ======================================================
    # Compare
    # ======================================================

    compare_results = compare_all_cases()

    # ======================================================
    # Build Report
    # ======================================================

    reports: list[CaseReport] = []

    failed = False

    case_names = sorted(

        set(compare_results.keys())

        | set(validation_errors.keys())

    )

    for case_name in case_names:

        report = CaseReport(

            case_name=case_name,

            validation_errors=validation_errors.get(
                case_name,
                [],
            ),

            differences=compare_results.get(
                case_name,
                [],
            ),

        )

        reports.append(report)

        if not report.passed:

            failed = True

    # ======================================================
    # Export Report
    # ======================================================

    export_markdown(reports)

    export_csv(reports)

    export_html(reports)

    # ======================================================
    # Pytest
    # ======================================================

    if failed:

        pytest.fail(
            "Golden Dataset failed. "
            "See tests/golden_dataset/reports/"
        )
