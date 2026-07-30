"""Golden dataset tests for Interpretation Engine Sprint 2 outputs."""

from __future__ import annotations

import json
from pathlib import Path

from engines.analysis_engine.interpretation_engine import (
    InterpretationContext,
    InterpretationEngine,
    create_default_knowledge_session,
)
from tests.interpretation_engine.conftest import build_analysis_result

GOLDEN_DIR = Path(__file__).parent / "golden"


def _run_default_case():
    return InterpretationEngine().interpret(
        InterpretationContext(
            analysis_result=build_analysis_result("interp-golden-001"),
            chart={"day_master": "Giáp"},
            knowledge_session=create_default_knowledge_session(),
            knowledge_version="1.0.0",
        )
    )


def test_golden_markdown_matches() -> None:
    result = _run_default_case()
    expected = (GOLDEN_DIR / "case_default.markdown").read_text(encoding="utf-8")
    assert result.markdown == expected


def test_golden_html_matches() -> None:
    result = _run_default_case()
    expected = (GOLDEN_DIR / "case_default.html").read_text(encoding="utf-8")
    assert result.html == expected


def test_golden_json_structure_matches() -> None:
    result = _run_default_case()
    expected = json.loads((GOLDEN_DIR / "case_default.json").read_text(encoding="utf-8"))
    actual = result.to_dict()
    for key in ("markdown", "html", "json_text"):
        actual.pop(key, None)
    assert actual == expected
