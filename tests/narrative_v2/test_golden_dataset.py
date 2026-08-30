"""N-IMP-12 Narrative V2 Golden Dataset tests."""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from engines.narrative_v2.golden import (
    GoldenDataset,
    GoldenEligibilityError,
    GoldenHistory,
    GoldenImmutabilityError,
    GoldenValidationError,
)
from engines.narrative_v2.golden.golden_case import STATUS_FROZEN
from engines.narrative_v2.golden.golden_registry import GoldenRegistryEntry
from engines.narrative_v2.golden.golden_serializer import presentation_hash

REPO = Path(__file__).resolve().parents[2]
FROZEN = REPO / "implementation" / "narrative_v2" / "n_imp_09a" / "case0001_presentation_v2_1.json"
CERT_HISTORY = REPO / "implementation" / "narrative_v2" / "n_imp_11a" / "certification_history.json"
KNOWLEDGE_ROOT = REPO / "knowledge" / "narrative_v2"
PACK05_GOLDEN = REPO / "tests" / "golden_dataset" / "expected" / "case_0001.json"
PORTAL_APP = REPO / "applications" / "customer_portal" / "app.py"
PACK05_ENGINE = REPO / "engines" / "narrative_engine" / "engine.py"

CANONICAL_IDENTITY = {
    "case_id": "CASE-0001",
    "year": 1987,
    "month": 1,
    "day": 21,
    "hour": 4,
    "minute": 30,
    "gender": "male",
    "timezone": "Asia/Bangkok",
    "stage": "luck",
}


def _presentation() -> dict:
    return json.loads(FROZEN.read_text(encoding="utf-8"))


def _certified() -> dict:
    rows = json.loads(CERT_HISTORY.read_text(encoding="utf-8"))
    certified = [row for row in rows if row.get("status") == "CERTIFIED"]
    assert certified, "CASE-0001 must be CERTIFIED before Golden promotion"
    return copy.deepcopy(certified[-1])


def _dataset(tmp_path: Path) -> GoldenDataset:
    return GoldenDataset(history=GoldenHistory(tmp_path / "golden"))


def test_eligibility_rejects_non_certified(tmp_path: Path) -> None:
    dataset = _dataset(tmp_path)
    review = dict(_certified(), status="REVIEW", golden_eligible=False)
    assert dataset.eligible(review) is False
    with pytest.raises(GoldenEligibilityError):
        dataset.promote(
            case_id="CASE-0001",
            presentation=_presentation(),
            certification=review,
            canonical=CANONICAL_IDENTITY,
        )


def test_promotion_requires_certified_case(tmp_path: Path) -> None:
    dataset = _dataset(tmp_path)
    payload = _presentation()
    certified = _certified()
    assert dataset.eligible(certified) is True
    golden = dataset.promote(
        case_id="CASE-0001",
        presentation=payload,
        certification=certified,
        canonical=CANONICAL_IDENTITY,
        created="2026-08-30T07:00:00+00:00",
    )
    assert golden.status == STATUS_FROZEN
    assert golden.version == 1
    assert golden.reviewer == "product-owner"
    assert golden.presentation["status"] == payload["status"]
    loaded = dataset.get("CASE-0001")
    assert loaded is not None
    assert loaded.presentation_hash == golden.presentation_hash


def test_freeze_never_overwrites(tmp_path: Path) -> None:
    history = GoldenHistory(tmp_path / "golden")
    dataset = GoldenDataset(history=history)
    first = dataset.promote(
        case_id="CASE-0001",
        presentation=_presentation(),
        certification=_certified(),
        canonical=CANONICAL_IDENTITY,
    )
    path = tmp_path / "golden" / "cases" / "CASE-0001" / "v1.json"
    original = path.read_text(encoding="utf-8")
    with pytest.raises(GoldenImmutabilityError):
        history.append(
            first,
            GoldenRegistryEntry(
                case_id="CASE-0001",
                version=1,
                status=STATUS_FROZEN,
                created=first.created,
                reviewer=first.reviewer,
            ),
        )
    assert path.read_text(encoding="utf-8") == original
    with pytest.raises(FrozenInstanceError):
        first.case_id = "CASE-X"  # type: ignore[misc]
    with pytest.raises(TypeError):
        first.presentation["status"] = "tampered"  # type: ignore[index]


def test_hashes_are_stable_and_sensitive(tmp_path: Path) -> None:
    dataset = _dataset(tmp_path)
    payload = _presentation()
    golden = dataset.promote(
        case_id="CASE-0001",
        presentation=payload,
        certification=_certified(),
        canonical=CANONICAL_IDENTITY,
    )
    assert golden.presentation_hash == presentation_hash(payload)
    assert golden.canonical_hash
    assert golden.review_hash
    assert golden.certification_hash
    assert golden.narrative_hash
    assert len({golden.presentation_hash, golden.canonical_hash, golden.review_hash}) == 3
    changed = copy.deepcopy(payload)
    overview = dict(changed["overview"])
    overview["headline"] = "changed"
    changed["overview"] = overview
    assert presentation_hash(changed) != golden.presentation_hash


def test_registry_and_versioning(tmp_path: Path) -> None:
    dataset = _dataset(tmp_path)
    dataset.promote(
        case_id="CASE-0001",
        presentation=_presentation(),
        certification=_certified(),
        canonical=CANONICAL_IDENTITY,
        created="2026-08-30T07:00:00+00:00",
    )
    second = dataset.promote(
        case_id="CASE-0001",
        presentation=_presentation(),
        certification=_certified(),
        canonical=CANONICAL_IDENTITY,
        created="2026-08-30T07:10:00+00:00",
    )
    assert second.version == 2
    v1 = dataset.get("CASE-0001", 1)
    v2 = dataset.get("CASE-0001", 2)
    assert v1 is not None and v2 is not None
    assert v1.version == 1
    assert dataset.get("CASE-0001") is not None
    assert dataset.get("CASE-0001").version == 2  # type: ignore[union-attr]
    rows = dataset.registry()
    assert [row["version"] for row in rows if row["case_id"] == "CASE-0001"] == [1, 2]
    assert rows[0]["status"] == STATUS_FROZEN
    assert rows[0]["reviewer"] == "product-owner"
    assert rows[0]["created"] == "2026-08-30T07:00:00+00:00"
    assert (tmp_path / "golden" / "cases" / "CASE-0001" / "v1.json").exists()
    assert (tmp_path / "golden" / "cases" / "CASE-0001" / "v2.json").exists()


def test_regression_compare(tmp_path: Path) -> None:
    dataset = _dataset(tmp_path)
    payload = _presentation()
    dataset.promote(
        case_id="CASE-0001",
        presentation=payload,
        certification=_certified(),
        canonical=CANONICAL_IDENTITY,
    )
    same = dataset.compare(case_id="CASE-0001", presentation=payload)
    assert same["matched"] is True
    assert same["diffs"] == []
    drifted = copy.deepcopy(payload)
    drifted["status"] = "complete"
    report = dataset.compare(case_id="CASE-0001", presentation=drifted)
    assert report["matched"] is False
    assert any(row["path"] == "status" for row in report["diffs"])


def test_incompatible_presentation_rejected(tmp_path: Path) -> None:
    dataset = _dataset(tmp_path)
    payload = _presentation()
    payload["metadata"] = dict(payload["metadata"], version="bte.presentation.v2")
    with pytest.raises(GoldenValidationError):
        dataset.promote(
            case_id="CASE-0001",
            presentation=payload,
            certification=_certified(),
            canonical=CANONICAL_IDENTITY,
        )


def test_no_mutation_of_sources_or_pack05(tmp_path: Path) -> None:
    payload = _presentation()
    before = copy.deepcopy(payload)
    knowledge_before = tuple(sorted(p.as_posix() for p in KNOWLEDGE_ROOT.rglob("*.md")))
    pack05_before = hashlib.sha256(PACK05_GOLDEN.read_bytes()).hexdigest()
    dataset = _dataset(tmp_path)
    dataset.promote(
        case_id="CASE-0001",
        presentation=payload,
        certification=_certified(),
        canonical=CANONICAL_IDENTITY,
    )
    payload["status"] = "tampered"
    assert json.loads(FROZEN.read_text(encoding="utf-8")) == before
    assert tuple(sorted(p.as_posix() for p in KNOWLEDGE_ROOT.rglob("*.md"))) == knowledge_before
    assert hashlib.sha256(PACK05_GOLDEN.read_bytes()).hexdigest() == pack05_before
    portal = PORTAL_APP.read_text(encoding="utf-8")
    assert "narrative_v2.golden" not in portal
    assert "GoldenDataset" not in PACK05_ENGINE.read_text(encoding="utf-8")
