"""
WP0B integration test — InterpretationEngine.run() end-to-end.
"""

from __future__ import annotations

import json
from dataclasses import asdict

from engines.interpretation_engine import (
    InterpretationEngine,
    InterpretationResult,
)


def test_engine_run_returns_interpretation_result():
    """engine.run(context) must return InterpretationResult without error."""

    engine = InterpretationEngine()
    context = {
        "day_master": "Canh",
        "month_branch": "Suu",
    }

    result = engine.run(context)

    assert isinstance(result, InterpretationResult)
    assert result is not None

    # JSON-serializable via dataclass / engine.to_json
    payload = asdict(result)
    encoded = json.dumps(payload, ensure_ascii=False, default=str)
    assert isinstance(encoded, str)
    assert json.loads(encoded) is not None

    encoded_via_engine = engine.to_json(result)
    assert isinstance(encoded_via_engine, str)
    assert json.loads(encoded_via_engine) is not None
