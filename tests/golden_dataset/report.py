"""
Golden Dataset Report

Chức năng:
- Tổng hợp kết quả Validation
- Tổng hợp kết quả Compare
- Xuất báo cáo Markdown
- Xuất báo cáo CSV
- Xuất báo cáo HTML
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from html import escape

from .compare import Difference
from .validator import ValidationError


# ==========================================================
# Directories
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

INPUTS_FOLDER = "inputs"
EXPECTED_FOLDER = "expected"
ACTUAL_FOLDER = "actual"
REPORTS_FOLDER = "reports"
SCHEMAS_FOLDER = "schemas"
SNAPSHOTS_FOLDER = "snapshots"

REPORT_DIR = BASE_DIR / REPORTS_FOLDER

REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================
# Report Model
# ==========================================================

@dataclass(slots=True)
class CaseReport:

    case_name: str

    validation_errors: list[ValidationError]

    differences: list[Difference]

    @property
    def passed(self) -> bool:

        return (
            len(self.validation_errors) == 0
            and len(self.differences) == 0
        )


# ==========================================================
# Markdown
# ==========================================================

def export_markdown(
    reports: list[CaseReport],
) -> Path:

    path = REPORT_DIR / "golden_dataset_report.md"

    with path.open(
        "w",
        encoding="utf-8",
    ) as f:

        f.write("# Golden Dataset Report\n\n")

        total = len(reports)
        passed = sum(r.passed for r in reports)

        f.write(f"Total Cases : {total}\n\n")
        f.write(f"Passed      : {passed}\n\n")
        f.write(f"Failed      : {total-passed}\n\n")

        f.write("---\n\n")

        for report in reports:

            status = "PASS" if report.passed else "FAIL"

            f.write(f"## {report.case_name} [{status}]\n\n")

            if report.validation_errors:

                f.write("### Validation Errors\n\n")

                for err in report.validation_errors:

                    f.write(
                        f"- {err.path}: {err.message} ({err.value})\n"
                    )

                f.write("\n")

            if report.differences:

                f.write("### Differences\n\n")

                for diff in report.differences:

                    f.write(
                        f"- {diff.field}\n"
                        f"  - expected: {diff.expected}\n"
                        f"  - actual  : {diff.actual}\n"
                    )

                f.write("\n")

    return path


# ==========================================================
# CSV
# ==========================================================

def export_csv(
    reports: list[CaseReport],
) -> Path:

    path = REPORT_DIR / "golden_dataset_report.csv"

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "case",
                "status",
                "validation_errors",
                "differences",
            ]
        )

        for report in reports:

            writer.writerow(
                [
                    report.case_name,
                    "PASS" if report.passed else "FAIL",
                    len(report.validation_errors),
                    len(report.differences),
                ]
            )

    return path


# ==========================================================
# HTML
# ==========================================================

def export_html(
    reports: list[CaseReport],
) -> Path:

    path = REPORT_DIR / "golden_dataset_report.html"

    with path.open(
        "w",
        encoding="utf-8",
    ) as f:

        f.write("<html><body>")
        f.write("<h1>Golden Dataset Report</h1>")

        f.write("<table border='1' cellspacing='0' cellpadding='5'>")

        f.write(
            "<tr>"
            "<th>Case</th>"
            "<th>Status</th>"
            "<th>Validation</th>"
            "<th>Difference</th>"
            "</tr>"
        )

        for report in reports:

            f.write("<tr>")

            f.write(f"<td>{escape(report.case_name)}</td>")

            f.write(
                f"<td>{'PASS' if report.passed else 'FAIL'}</td>"
            )

            f.write(
                f"<td>{len(report.validation_errors)}</td>"
            )

            f.write(
                f"<td>{len(report.differences)}</td>"
            )

            f.write("</tr>")

        f.write("</table>")
        f.write("</body></html>")

    return path
