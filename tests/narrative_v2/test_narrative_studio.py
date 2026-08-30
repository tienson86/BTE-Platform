"""N-IMP-10A Narrative Studio tests. Read-only workspace."""

from __future__ import annotations

import hashlib
from pathlib import Path

from fastapi.testclient import TestClient

from applications.narrative_studio.approvals import ApprovalStore
from applications.narrative_studio.app import create_app
from applications.narrative_studio.catalog import list_cases
from applications.narrative_studio.golden import diff_presentations, load_golden_presentation
from applications.narrative_studio.service import NarrativeStudioService

REPO = Path(__file__).resolve().parents[2]
KNOWLEDGE_ROOT = REPO / "knowledge" / "narrative_v2"
PORTAL_APP = REPO / "applications" / "customer_portal" / "app.py"


def _file_fingerprint(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        if not item.is_file():
            continue
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(item.read_bytes())
    return digest.hexdigest()


def test_catalog_exposes_case_0001_and_0002() -> None:
    ids = [case.case_id for case in list_cases()]
    assert ids == ["CASE-0001", "CASE-0002"]


def test_studio_loads_presentation_trace_knowledge_decision_compare_golden() -> None:
    before_knowledge = _file_fingerprint(KNOWLEDGE_ROOT)
    service = NarrativeStudioService()
    review = service.load("CASE-0001")
    again = service.load("CASE-0001")
    assert again is review
    assert review.presentation is not None
    assert review.presentation["metadata"]["version"] == "bte.presentation.v2.1"
    assert review.consulting_flow
    assert review.structured["observation"]
    assert review.trace["evidence"]
    assert review.trace["knowledge"]
    assert review.trace["presentation"]
    assert review.knowledge["ids"]
    assert review.decisions
    assert review.pack05 is not None
    assert review.pack05.get("contract") == "pack05_narrative_result_v1"
    assert review.golden_available is True
    assert review.presentation_fingerprint == again.presentation_fingerprint
    assert _file_fingerprint(KNOWLEDGE_ROOT) == before_knowledge


def test_studio_does_not_mutate_presentation_or_golden() -> None:
    golden = load_golden_presentation("CASE-0001")
    assert golden is not None
    original = dict(golden)
    service = NarrativeStudioService()
    review = service.load("CASE-0001")
    assert load_golden_presentation("CASE-0001") == original
    assert review.presentation is not None
    copied = dict(review.presentation)
    diffs = diff_presentations(review.presentation, golden)
    assert isinstance(diffs, list)
    assert review.presentation == copied


def test_studio_http_is_internal_and_read_only(tmp_path: Path) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")
    service = NarrativeStudioService()
    client = TestClient(create_app(service=service, approvals=store))
    overview = client.get("/studio?case=CASE-0001&panel=overview")
    assert overview.status_code == 200
    assert "NOT CUSTOMER PORTAL" in overview.text
    assert 'data-studio-panel="overview"' in overview.text
    consulting = client.get("/studio?case=CASE-0001&panel=consulting")
    assert "data-studio-consulting-flow" in consulting.text
    trace = client.get("/studio?case=CASE-0001&panel=trace")
    assert 'data-studio-trace="evidence"' in trace.text
    compare = client.get("/studio?case=CASE-0001&panel=compare")
    assert "Pack05" in compare.text
    assert "Narrative V2" in compare.text
    golden = client.get("/studio?case=CASE-0001&panel=golden")
    assert "Golden View" in golden.text
    recorded = client.post(
        "/studio/approval",
        data={
            "case": "CASE-0001",
            "verdict": "REVIEW",
            "comment": "internal studio note",
            "reviewer": "nimp10a",
        },
        follow_redirects=True,
    )
    assert recorded.status_code == 200
    assert "REVIEW" in recorded.text
    latest = store.latest("CASE-0001")
    assert latest is not None
    assert latest.verdict == "REVIEW"
    assert "narrative_studio" not in PORTAL_APP.read_text(encoding="utf-8")


def test_studio_not_on_customer_portal() -> None:
    source = PORTAL_APP.read_text(encoding="utf-8")
    assert "narrative_studio" not in source
    assert "/studio" not in source
