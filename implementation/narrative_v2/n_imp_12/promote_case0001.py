"""Promote certified CASE-0001 into the Narrative V2 Golden Dataset."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from engines.narrative_v2.golden import GoldenDataset, GoldenHistory
from engines.narrative_v2.golden.golden_history import DEFAULT_ROOT

REPO = Path(__file__).resolve().parents[3]
FROZEN = REPO / "implementation" / "narrative_v2" / "n_imp_09a" / "case0001_presentation_v2_1.json"
CERT_HISTORY = REPO / "implementation" / "narrative_v2" / "n_imp_11a" / "certification_history.json"
OUT = REPO / "implementation" / "narrative_v2" / "n_imp_12"


def main() -> None:
    """Copy certified CASE-0001 into Golden. Does not rewrite Presentation."""
    presentation = json.loads(FROZEN.read_text(encoding="utf-8"))
    rows = json.loads(CERT_HISTORY.read_text(encoding="utf-8"))
    certified = [row for row in rows if row.get("status") == "CERTIFIED"][-1]
    canonical = {
        "case_id": CASE_0001_REQUEST.case_id,
        "year": CASE_0001_REQUEST.year,
        "month": CASE_0001_REQUEST.month,
        "day": CASE_0001_REQUEST.day,
        "hour": CASE_0001_REQUEST.hour,
        "minute": CASE_0001_REQUEST.minute,
        "gender": CASE_0001_REQUEST.gender,
        "timezone": CASE_0001_REQUEST.timezone,
        "stage": "luck",
    }
    dataset = GoldenDataset(history=GoldenHistory(DEFAULT_ROOT))
    golden = dataset.promote(
        case_id="CASE-0001",
        presentation=presentation,
        certification=certified,
        canonical=canonical,
        created="2026-08-30T07:00:00+00:00",
    )
    compare = dataset.compare(case_id="CASE-0001", presentation=presentation)
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(DEFAULT_ROOT / "cases" / "CASE-0001" / "v1.json", OUT / "case0001_golden.json")
    shutil.copyfile(DEFAULT_ROOT / "registry.json", OUT / "golden_registry.json")
    diffs = compare["diffs"]
    matched = "YES" if compare["matched"] else "NO"
    if diffs:
        table = ["| Path | Kind | Current | Golden |", "| --- | --- | --- | --- |"]
        for row in diffs:
            table.append(
                f"| {row['path']} | {row['kind']} | {row['current']} | {row['golden']} |"
            )
        diff_body = "\n".join(table)
    else:
        diff_body = (
            "No presentation drift. Golden Presentation equals the certified CASE-0001 baseline.\n\n"
            "Regression compare against this Golden Case is the baseline for future Narrative changes."
        )
    (OUT / "golden_diff.md").write_text(
        (
            "# Golden Diff — CASE-0001\n\n"
            "Source Presentation: implementation/narrative_v2/n_imp_09a/case0001_presentation_v2_1.json\n"
            "Golden version: 1\n\n"
            f"Matched: {matched}\n"
            f"Diff count: {len(diffs)}\n\n"
            f"{diff_body}\n"
        ),
        encoding="utf-8",
    )
    schema = golden.metadata["schema"]
    (OUT / "hash_report.md").write_text(
        (
            "# Hash Report — CASE-0001\n\n"
            f"Golden schema: {schema}\n"
            f"Version: {golden.version}\n"
            f"Status: {golden.status}\n"
            f"Reviewer: {golden.reviewer}\n"
            f"Created: {golden.created}\n\n"
            "| Hash | Value |\n"
            "| --- | --- |\n"
            f"| canonical_hash | {golden.canonical_hash} |\n"
            f"| presentation_hash | {golden.presentation_hash} |\n"
            f"| review_hash | {golden.review_hash} |\n"
            f"| certification_hash | {golden.certification_hash} |\n"
            f"| narrative_hash | {golden.narrative_hash} |\n\n"
            "Canonical identity hashed (not hardcoded Narrative).\n"
            "Presentation source: certified freeze n_imp_09a (copied, not rewritten).\n"
            "Certification source: n_imp_11a CERTIFIED record (product-owner).\n"
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
