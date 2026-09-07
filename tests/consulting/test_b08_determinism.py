"""TV1-B08 determinism. Semantic signatures must be identical across repeats."""

from __future__ import annotations

import json

from tests.consulting.api_fixtures import api_client, api_service, valid_body
from tests.consulting.golden.cases import run_golden_case
from tests.consulting.golden.signature import semantic_signature

REPEAT_COUNT = 10
DETERMINISTIC_CASES = ("CASE-M01", "CASE-M02", "CASE-M09", "CASE-M12")


def _semantic_payload(signature: dict) -> str:
    """Stable comparison payload. Volatile ids/timestamps are already omitted."""
    return json.dumps(signature, sort_keys=True, ensure_ascii=False)


def test_golden_pipeline_is_deterministic_across_ten_runs() -> None:
    """Ten repeats of selected Golden fixtures keep the same semantic signature."""
    for case_id in DETERMINISTIC_CASES:
        first = _semantic_payload(run_golden_case(case_id)["signature"])
        for _ in range(REPEAT_COUNT - 1):
            assert _semantic_payload(run_golden_case(case_id)["signature"]) == first


def test_api_replay_keeps_semantic_signature() -> None:
    """Repeated identical POSTs share Decision semantics while consultation ids differ."""
    client, container = api_client()
    signatures = []
    ids = []
    for index in range(REPEAT_COUNT):
        payload = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]
        ids.append(payload["consultation_id"])
        stored = api_service(container).get_stored(payload["consultation_id"])
        signatures.append(
            _semantic_payload(
                semantic_signature(stored.result, stored.narrative, stored.report_model)
            )
        )
    assert len(set(ids)) == REPEAT_COUNT
    assert len(set(signatures)) == 1
    assert json.loads(signatures[0])["score"] is None
