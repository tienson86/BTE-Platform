"""P7-IMP-09R: canonical Domain Driver IDs, not customer/dimension/risk labels."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.api.app import create_app
from engines.detailed_interpretation_engine.diagnostics import diagnostics_from_payload
from engines.detailed_interpretation_engine.domain_interpretation.constants import (
    AUTHORITY_DRIVER_IDS,
    CAREER_DRIVER_IDS,
    DOMAIN_DRIVER_IDS,
    FORBIDDEN_AUTHORITY_DRIVER_IDS,
    FORBIDDEN_VITALITY_DRIVER_IDS,
    FORBIDDEN_WEALTH_DRIVER_IDS,
    VITALITY_DRIVER_IDS,
    WEALTH_DRIVER_IDS,
)
from engines.detailed_interpretation_engine.domain_interpretation.labels import DAMAGE_LABELS, DRIVER_LABELS
from engines.detailed_interpretation_engine.enums import DiagnosticStatus, DomainState
from tests.detailed_interpretation.test_p7_imp_09_domains import (
    CASE_0001,
    _LOW,
    _bind,
    _payload,
    _profiles,
)


def _natal(context, domain_id: str):
    return getattr(context.runtime.domains, domain_id).natal


def test_vitality_damage_is_not_vitality_driver() -> None:
    vitality = _natal(_bind(_payload())[0], "vitality")
    assert vitality.driver_id in VITALITY_DRIVER_IDS
    assert vitality.driver_id not in FORBIDDEN_VITALITY_DRIVER_IDS
    assert vitality.driver not in set(DAMAGE_LABELS.values())
    assert "Ấn quá vượng" not in vitality.driver


def test_wealth_retention_is_not_wealth_driver() -> None:
    wealth = _natal(_bind(_payload())[0], "wealth")
    assert wealth.driver_id in WEALTH_DRIVER_IDS
    assert wealth.driver_id not in FORBIDDEN_WEALTH_DRIVER_IDS
    assert wealth.driver not in {"Giữ tài", "Tạo tài", "Tích lũy"}
    assert wealth.dimensions.get("retention")


def test_wealth_volatility_is_not_wealth_driver() -> None:
    wealth = _natal(_bind(_payload())[0], "wealth")
    assert wealth.driver_id != "volatility"
    assert wealth.driver != "Biến động tài cao"
    assert wealth.risk == "Biến động tài cao" or "Biến động" in wealth.risk or wealth.dimensions.get("volatility")


def test_career_achievement_list_is_not_career_driver() -> None:
    career = _natal(_bind(_payload())[0], "career")
    assert career.driver_id in CAREER_DRIVER_IDS
    assert " · " not in career.driver
    assert career.driver_id != "academic,entrepreneurship,management"


def test_authority_generic_label_is_not_canonical_mechanism() -> None:
    authority = _natal(_bind(_payload())[0], "authority")
    assert authority.driver_id in AUTHORITY_DRIVER_IDS
    assert authority.driver_id not in FORBIDDEN_AUTHORITY_DRIVER_IDS
    assert authority.driver != "Quyền hạn"


def test_shen_sha_is_not_domain_driver() -> None:
    context, _ = _bind(_payload())
    for domain_id in DOMAIN_DRIVER_IDS:
        natal = _natal(context, domain_id)
        assert natal.driver_id not in {"hong_luan", "hong_loan", "thien_hy"}
        assert "shen_sha" not in natal.driver_source.lower()


def test_risk_evidence_does_not_become_driver() -> None:
    baseline, _ = _bind(_payload())
    extra = _profiles()
    extra["damage"] = [
        {"damage_type": "resource_overload", "severity": "major"},
        {"damage_type": "peer_robs_wealth", "severity": "major"},
    ]
    mutated, _ = _bind(_payload(extra))
    for domain_id in ("authority", "career", "wealth", "relationship", "legacy", "vitality"):
        before = _natal(baseline, domain_id)
        after = _natal(mutated, domain_id)
        assert after.driver_id == before.driver_id
        assert after.driver_id not in set(DAMAGE_LABELS)
        assert after.driver not in set(DAMAGE_LABELS.values())


def test_improve_retention_does_not_change_wealth_driver() -> None:
    weak, _ = _bind(_payload(_profiles(retention=_LOW)))
    strong, _ = _bind(_payload(_profiles(retention="high")))
    assert _natal(weak, "wealth").driver_id == _natal(strong, "wealth").driver_id
    assert _natal(strong, "wealth").dimensions.get("retention") == "high"


def test_career_pressure_does_not_become_vitality_driver() -> None:
    baseline, _ = _bind(_payload())
    extra = _profiles()
    extra["damage"] = [{"damage_type": "resource_overload", "severity": "major"}]
    pressed, _ = _bind(_payload(extra))
    vitality = _natal(pressed, "vitality")
    assert vitality.driver_id == _natal(baseline, "vitality").driver_id
    assert vitality.driver_id != "career_pressure"
    assert vitality.driver_id != "career_overload"
    assert vitality.driver_id not in FORBIDDEN_VITALITY_DRIVER_IDS


def test_support_is_not_the_bottleneck_label() -> None:
    context, _ = _bind(_payload())
    for domain_id in DOMAIN_DRIVER_IDS:
        natal = _natal(context, domain_id)
        if natal.support and natal.bottleneck:
            assert natal.support != natal.bottleneck


def test_canonical_driver_ids_on_fixture() -> None:
    context, _ = _bind(_payload())
    for domain_id in DOMAIN_DRIVER_IDS:
        natal = _natal(context, domain_id)
        if natal.support and natal.bottleneck:
            assert natal.support != natal.bottleneck
    context, _ = _bind(_payload())
    forbidden = FORBIDDEN_WEALTH_DRIVER_IDS | FORBIDDEN_VITALITY_DRIVER_IDS | FORBIDDEN_AUTHORITY_DRIVER_IDS
    for domain_id in DOMAIN_DRIVER_IDS:
        natal = _natal(context, domain_id)
        assert natal.state is not DomainState.NOT_EVALUATED
        assert natal.driver_id in DOMAIN_DRIVER_IDS[domain_id]
        assert natal.driver == DRIVER_LABELS.get(natal.driver_id, natal.driver)
        assert natal.driver != natal.bottleneck or not natal.driver
        assert natal.driver_id not in forbidden


def test_live_case_0001_uses_canonical_drivers() -> None:
    client = TestClient(create_app())
    analyzed = client.post("/api/v1/analyze", json=CASE_0001)
    assert analyzed.status_code == 200
    body = analyzed.json()["data"]
    items = {item["id"]: item for item in (body.get("domains") or {}).get("items") or []}
    assert set(items) >= set(DOMAIN_DRIVER_IDS)
    for domain_id, item in items.items():
        allowed = DOMAIN_DRIVER_IDS[domain_id]
        assert item["driver_id"] in allowed
        assert item["driver"] == DRIVER_LABELS.get(item["driver_id"], item["driver"])
        assert item["driver"] != item.get("bottleneck") or not item["driver"]
        if item.get("support") and item.get("bottleneck"):
            assert item["support"] != item["bottleneck"]
        assert item["driver"] not in set(DAMAGE_LABELS.values())
        assert " · " not in (item["driver"] or "")
        assert item["state"] in {
            "conditional",
            "fragmented",
            "moderate",
            "strong",
            "weak",
            "very_strong",
            "blocked",
            "unresolved",
        }
    assert items["authority"]["state"] == "conditional"
    assert items["career"]["state"] == "conditional"
    assert items["wealth"]["state"] == "fragmented"
    assert items["relationship"]["state"] == "fragmented"
    assert items["legacy"]["state"] == "conditional"
    assert items["vitality"]["state"] == "conditional"
    diagnostics = diagnostics_from_payload(body)
    assert diagnostics.domains is DiagnosticStatus.PASS
    live = client.post("/api/v1/dev/pack07/diagnostics", json=CASE_0001)
    assert live.status_code == 200
    assert live.json()["data"]["domains"] == "PASS"
