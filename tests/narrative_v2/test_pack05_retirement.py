"""N-REL-03 Pack05 retirement: archive, not deletion."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest

from applications.api.exceptions import CustomerExportError
from applications.api.services.narrative_production_export import export_production_json
from applications.api.services.narrative_v2_shadow import attach_narrative_v2_shadow
from applications.customer_portal.config import PortalSettings, _narrative_provider, _pack05_legacy
from applications.narrative_studio.renderer import render_studio
from applications.narrative_studio.service import StudioReview
from engines.narrative_v2.presentation import PRESENTATION_VERSION
from engines.narrative_v2.release import (
    EXPORT_SOURCE_ARCHIVE,
    EXPORT_SOURCE_V2,
    PACK05_CONTRACT,
    PRODUCTION_PROVIDER,
    load_pack05_archive,
    pack05_legacy_enabled,
    resolve_production_provider,
    select_export_source,
)

REPO = Path(__file__).resolve().parents[2]
FROZEN = REPO / "implementation" / "narrative_v2" / "n_imp_09a" / "case0001_presentation_v2_1.json"
EXPORT_PY = REPO / "applications" / "api" / "routes" / "export.py"


def _presentation() -> dict[str, Any]:
    return json.loads(FROZEN.read_text(encoding="utf-8"))


def _dual_payload() -> dict[str, Any]:
    pack05: dict[str, Any] = {
        "contract": PACK05_CONTRACT,
        "status": "ok",
        "summary": {"identity": "historical pack05", "priority_recommendation": "archive only"},
    }
    return {
        "narrative_result": pack05,
        "narrative_v2_shadow": {
            "status": "ok",
            "replaces_pack05": False,
            "presentation": _presentation(),
            "error": None,
        },
    }


def test_production_provider_ignores_pack05_and_auto() -> None:
    assert resolve_production_provider("pack05") == PRODUCTION_PROVIDER
    assert resolve_production_provider("auto") == "v2"
    assert resolve_production_provider("v2") == "v2"
    assert _narrative_provider() == "v2"


def test_production_env_cannot_select_pack05(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NARRATIVE_PROVIDER", "pack05")
    assert _narrative_provider() == "v2"
    monkeypatch.setenv("NARRATIVE_PROVIDER", "auto")
    assert _narrative_provider() == "v2"
    settings = PortalSettings()
    assert settings.narrative_provider == "v2"


def test_pack05_legacy_is_read_only_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PACK05_LEGACY", raising=False)
    assert pack05_legacy_enabled() is False
    assert _pack05_legacy() is False
    monkeypatch.setenv("PACK05_LEGACY", "pack05")
    assert pack05_legacy_enabled() is True
    assert _pack05_legacy() is True


def test_pack05_archive_preserves_history_without_mutation() -> None:
    data = _dual_payload()
    original = copy.deepcopy(data["narrative_result"])
    archive = load_pack05_archive(data)
    assert archive.available is True
    assert archive.read_only is True
    assert archive.contract == PACK05_CONTRACT
    assert archive.payload == original
    data["narrative_v2_shadow"]["status"] = "ok"
    assert data["narrative_result"] == original
    assert load_pack05_archive(data).payload == original


def test_legacy_export_reads_archive_production_export_is_v2() -> None:
    data = _dual_payload()
    assert select_export_source(data, legacy=False) == EXPORT_SOURCE_V2
    assert select_export_source(data, legacy=True) == EXPORT_SOURCE_ARCHIVE
    missing = {"narrative_result": data["narrative_result"]}
    assert select_export_source(missing, legacy=False) == EXPORT_SOURCE_ARCHIVE


def test_production_json_export_is_presentation_not_pack05() -> None:
    data = _dual_payload()
    payload = export_production_json(data)
    assert payload["metadata"]["version"] == PRESENTATION_VERSION
    assert payload["interpretation"]["consulting_flow"]
    assert "pack05_narrative_result_v1" not in json.dumps(payload)
    with pytest.raises(CustomerExportError) as caught:
        export_production_json({"narrative_result": data["narrative_result"]})
    assert caught.value.code == "export_presentation_unavailable"


def test_official_report_export_route_untouched() -> None:
    source = EXPORT_PY.read_text(encoding="utf-8")
    assert "narrative_v2" not in source


def test_studio_compare_is_historical_archive_only() -> None:
    review = StudioReview(
        case_id="CASE-0001",
        full_name="CASE-0001",
        presentation={"overview": {"headline": "V2 headline"}},
        pack05={"contract": PACK05_CONTRACT, "status": "ok", "identity": "archive"},
        consulting_flow="Consulting flow from Narrative V2",
        structured={},
        trace={},
        decisions=[],
        actions=[],
        knowledge={},
        contract={},
        quality={},
        golden_diffs=[],
        golden_available=False,
        runtime_status="ok",
        presentation_fingerprint="",
    )
    html = render_studio(
        cases=(),
        review=review,
        panel="compare",
        approval=None,
        history=[],
    )
    assert 'data-pack05-archive="historical"' in html
    assert "legacy archive" in html
    assert PACK05_CONTRACT in html
    assert "Consulting flow from Narrative V2" in html
    assert "Not a production provider" in html


def test_attach_does_not_overwrite_pack05() -> None:
    envelope = attach_narrative_v2_shadow({"source": "canonical_analysis_placeholder"})
    assert envelope["replaces_pack05"] is False
    assert envelope["status"] in {"ok", "error"}
