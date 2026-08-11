"""Taxonomy firewall tests."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = ("taxonomy_v2", "t1", "t2", "t3", "t4", "t5", "t6", "seven_band")


def test_schemas_have_no_taxonomy_fields() -> None:
    for path in (ROOT / "schemas").glob("*.json"):
        text = path.read_text(encoding="utf-8").lower()
        for token in FORBIDDEN:
            assert f'"{token}"' not in text, f"{path.name}:{token}"


def test_examples_have_no_taxonomy_keys() -> None:
    for path in (ROOT / "examples").glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))

        def walk(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    assert k.lower() not in FORBIDDEN
                    walk(v)
            elif isinstance(obj, list):
                for i in obj:
                    walk(i)

        walk(data)


def test_summary_declares_no_taxonomy() -> None:
    text = (ROOT / "PILOT_1K_SUMMARY.md").read_text(encoding="utf-8")
    assert "TAXONOMY_V2_IMPLEMENTED: NO" in text
    assert "T1_T6_IMPLEMENTED: NO" in text
