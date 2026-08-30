"""N-IMP-11A Narrative Certification Gate tests."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from applications.narrative_studio.approvals import ApprovalStore
from applications.narrative_studio.app import create_app
from applications.narrative_studio.renderer import render_studio
from applications.narrative_studio.service import StudioReview
from engines.narrative_v2.certification import (
    CERTIFICATION_VERSION,
    QUALITY_GATES,
    STATUS_CERTIFIED,
    STATUS_DRAFT,
    STATUS_REJECTED,
    STATUS_REVIEW,
    STATUS_REVOKED,
    CertificationGate,
    CertificationHistory,
    CertificationRejectedError,
    CertificationTransitionError,
    can_transition,
)
from engines.narrative_v2.presentation.presentation_status import PRESENTATION_VERSION

REPO = Path(__file__).resolve().parents[2]
FROZEN = REPO / "implementation" / "narrative_v2" / "n_imp_09a" / "case0001_presentation_v2_1.json"
KNOWLEDGE_ROOT = REPO / "knowledge" / "narrative_v2"
PORTAL_APP = REPO / "applications" / "customer_portal" / "app.py"


def _presentation() -> dict:
    return json.loads(FROZEN.read_text(encoding="utf-8"))


def _gate(tmp_path: Path) -> CertificationGate:
    return CertificationGate(history=CertificationHistory(tmp_path / "history.json"))


def _studio_review(case_id: str = "CASE-0001") -> StudioReview:
    return StudioReview(
        case_id=case_id,
        full_name="CASE-0001",
        presentation=_presentation(),
        pack05=None,
        consulting_flow="consulting flow",
        structured={
            "observation": "o",
            "reasoning": "r",
            "meaning": "m",
            "impact": "i",
            "recommendation": "rec",
            "closing": "c",
        },
        trace={},
        decisions=[],
        actions=[],
        knowledge={},
        contract={},
        quality={},
        golden_diffs=[],
        golden_available=False,
        runtime_status="complete",
        presentation_fingerprint="fp",
    )


class _FakeStudio:
    def load(self, case_id: str) -> StudioReview:
        return _studio_review(case_id)


def test_states_and_transitions() -> None:
    assert can_transition(STATUS_DRAFT, STATUS_REVIEW)
    assert not can_transition(STATUS_DRAFT, STATUS_CERTIFIED)
    assert can_transition(STATUS_REVIEW, STATUS_CERTIFIED)
    assert can_transition(STATUS_CERTIFIED, STATUS_REVOKED)
    assert not can_transition(STATUS_CERTIFIED, STATUS_REVIEW)


def test_inspect_does_not_certify_automatically(tmp_path: Path) -> None:
    path = tmp_path / "history.json"
    gate = CertificationGate(history=CertificationHistory(path))
    snapshot = gate.inspect(case_id="CASE-0001", presentation=_presentation())
    assert snapshot["status"] == STATUS_DRAFT
    assert snapshot["golden_eligible"] is False
    assert snapshot["quality_summary"]["all_passed"] is True
    for name in QUALITY_GATES:
        assert snapshot["quality_summary"]["gates"][name] == "PASS"
    assert not path.exists()


def test_reviewer_required_and_certified_needs_review(tmp_path: Path) -> None:
    gate = _gate(tmp_path)
    payload = _presentation()
    with pytest.raises(CertificationRejectedError):
        gate.submit(case_id="CASE-0001", presentation=payload, decision="REVIEW", reviewer="")
    with pytest.raises(CertificationTransitionError):
        gate.submit(
            case_id="CASE-0001",
            presentation=payload,
            decision="CERTIFIED",
            reviewer="product-owner",
        )
    review = gate.submit(
        case_id="CASE-0001",
        presentation=payload,
        decision="REVIEW",
        reviewer="product-owner",
        review_comment="studio review",
        review_time="2026-08-30T00:00:00+00:00",
    )
    assert review.status == STATUS_REVIEW
    assert review.golden_eligible is False
    certified = gate.submit(
        case_id="CASE-0001",
        presentation=payload,
        decision="CERTIFIED",
        reviewer="product-owner",
        review_comment="reference standard",
        review_time="2026-08-30T00:05:00+00:00",
    )
    assert certified.status == STATUS_CERTIFIED
    assert certified.certification_version == CERTIFICATION_VERSION
    assert certified.references["presentation_version"] == PRESENTATION_VERSION
    assert certified.golden_eligible is True
    assert gate.eligible_for_golden("CASE-0001") is True
    revoked = gate.submit(
        case_id="CASE-0001",
        presentation=payload,
        decision="REVOKED",
        reviewer="product-owner",
        review_comment="withdrawn",
        review_time="2026-08-30T00:10:00+00:00",
    )
    assert revoked.status == STATUS_REVOKED
    assert gate.eligible_for_golden("CASE-0001") is False


def test_failed_gates_block_certified(tmp_path: Path) -> None:
    gate = _gate(tmp_path)
    payload = _presentation()
    payload["metadata"] = dict(payload["metadata"], version="bte.presentation.v2")
    gate.submit(case_id="CASE-X", presentation=payload, decision="REVIEW", reviewer="qa")
    with pytest.raises(CertificationRejectedError):
        gate.submit(case_id="CASE-X", presentation=payload, decision="CERTIFIED", reviewer="qa")


def test_history_is_append_only(tmp_path: Path) -> None:
    gate = _gate(tmp_path)
    payload = _presentation()
    first = gate.submit(case_id="CASE-0001", presentation=payload, decision="REVIEW", reviewer="po")
    path = tmp_path / "history.json"
    original = path.read_text(encoding="utf-8")
    second = gate.submit(
        case_id="CASE-0001",
        presentation=payload,
        decision="REJECTED",
        reviewer="po",
        review_comment="hold",
    )
    rows = json.loads(path.read_text(encoding="utf-8"))
    assert rows[0]["review_id"] == first.review_id
    assert rows[1]["review_id"] == second.review_id
    assert first.review_id in original
    assert original != path.read_text(encoding="utf-8")
    assert rows[0] == json.loads(original)[0]


def test_no_mutation_of_presentation_or_knowledge(tmp_path: Path) -> None:
    payload = _presentation()
    before = copy.deepcopy(payload)
    knowledge_before = tuple(sorted(p.as_posix() for p in KNOWLEDGE_ROOT.rglob("*.md")))
    gate = _gate(tmp_path)
    gate.submit(case_id="CASE-0001", presentation=payload, decision="REVIEW", reviewer="po")
    assert payload == before
    assert tuple(sorted(p.as_posix() for p in KNOWLEDGE_ROOT.rglob("*.md"))) == knowledge_before
    assert "narrative_v2.certification" not in PORTAL_APP.read_text(encoding="utf-8")


def test_studio_certification_panel(tmp_path: Path) -> None:
    html = render_studio(
        cases=(),
        review=_studio_review(),
        panel="certification",
        approval=None,
        history=[],
        certification={"status": "DRAFT", "golden_eligible": False, "quality_summary": {}},
        certification_history=[],
    )
    assert 'data-studio-panel="certification"' in html
    assert "data-studio-certification" in html
    assert "data-certification-status" in html
    client = TestClient(
        create_app(
            service=_FakeStudio(),  # type: ignore[arg-type]
            approvals=ApprovalStore(tmp_path / "approvals.json"),
            certifications=CertificationHistory(tmp_path / "certs.json"),
        )
    )
    page = client.get("/studio?case=CASE-0001&panel=certification")
    assert page.status_code == 200
    assert 'data-studio-panel="certification"' in page.text
    review = client.post(
        "/studio/certification",
        data={"case": "CASE-0001", "decision": "REVIEW", "reviewer": "product-owner", "comment": "ok"},
        follow_redirects=True,
    )
    assert review.status_code == 200
    assert "REVIEW" in review.text
    certified = client.post(
        "/studio/certification",
        data={
            "case": "CASE-0001",
            "decision": "CERTIFIED",
            "reviewer": "product-owner",
            "comment": "golden eligible",
        },
        follow_redirects=True,
    )
    assert "data-certification-status" in certified.text
    assert ">CERTIFIED<" in certified.text
