"""
Golden Dataset Test

Quy trình:

Runner
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

from tests.golden_dataset.runner import run_all_cases
from tests.golden_dataset.validator import validate_files
from tests.golden_dataset.compare import compare_all_cases
from tests.golden_dataset.report import (
    CaseReport,
    export_csv,
    export_html,
    export_markdown,
)

from engines.interpretation.engine import InterpretationEngine


def test_golden_dataset():

    engine = InterpretationEngine()

    output_files = run_all_cases(engine)

    validation_result = validate_files(
        output_files
    )

    compare_result = compare_all_cases()

    reports = []

    failed = False

    for case_name in sorted(compare_result.keys()):

        report = CaseReport(
            case_name=case_name,
            validation_errors=validation_result.get(
                case_name,
                [],
            ),
            differences=compare_result.get(
                case_name,
                [],
            ),
        )

        reports.append(report)

        if not report.passed:

            failed = True

    export_markdown(reports)
    export_csv(reports)
    export_html(reports)

    if failed:

        pytest.fail(
            "Golden Dataset failed. "
            "See tests/golden_dataset/reports/"
        )
