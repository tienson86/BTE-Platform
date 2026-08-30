"""N-IMP-10A Narrative Studio tests. Read-only workspace."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from applications.narrative_studio.approvals import ApprovalStore
from applications.narrative_studio.app import create_app
from applications.narrative_studio.catalog import list_cases
from applications.narrative_studio.golden import diff_presentations, load_golden_presentation
from applications.narrative_studio.service import NarrativeStudioService, StudioReview

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


@pytest.fixture(scope="module")
def knowledge_before() -> str:
    return _file_fingerprint(KNOWLEDGE_ROOT)


@pytest.fixture(scope="module")
def studio_service() -> NarrativeStudioService:
    return NarrativeStudioService()


@pytest.fixture(scope="module")
def case0001(studio_service: NarrativeStudioService) -> StudioReview:
    return studio_service.load("CASE-0001")


def test_catalog_exposes_case_0001_and_0002() -> None:
    ids = [case.case_id for case in list_cases()]
    assert ids == ["CASE-0001", "CASE-0002"]


def test_studio_loads_presentation_trace_knowledge_decision_compare_golden(
    studio_service: NarrativeStudioService,
    case0001: StudioReview,
    knowledge_before: str,
) -> None:
    again = studio_service.load("CASE-0001")
    assert again is case0001
    assert case0001.presentation is not None
    assert case0001.presentation["metadata"]["version"] == "bte.presentation.v2.1"
    assert case0001.consulting_flow
    assert case0001.structured["observation"]
    assert case0001.trace["evidence"]
    assert case0001.trace["knowledge"]
    assert case0001.trace["presentation"]
    assert case0001.knowledge["ids"]
    assert case0001.decisions
    assert case0001.pack05 is not None
    assert case0001.pack05.get("contract") == "pack05_narrative_result_v1"
    assert case0001.golden_available is True
    assert case0001.presentation_fingerprint == again.presentation_fingerprint
    assert _file_fingerprint(KNOWLEDGE_ROOT) == knowledge_before


def test_studio_does_not_mutate_presentation_or_golden(case0001: StudioReview) -> None:
    golden = load_golden_presentation("CASE-0001")
    assert golden is not None
    original = dict(golden)
    assert load_golden_presentation("CASE-0001") == original
    assert case0001.presentation is not None
    copied = dict(case0001.presentation)
    diffs = diff_presentations(case0001.presentation, golden)
    assert isinstance(diffs, list)
    assert case0001.presentation == copied


def test_studio_http_is_internal_and_read_only(
    studio_service: NarrativeStudioService,
    tmp_path: Path,
    knowledge_before: str,
) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")
    client = TestClient(create_app(service=studio_service, approvals=store))
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
    assert _file_fingerprint(KNOWLEDGE_ROOT) == knowledge_before


def test_studio_not_on_customer_portal() -> None:
    source = PORTAL_APP.read_text(encoding="utf-8")
    assert "narrative_studio" not in source
    assert "/studio" not in source
