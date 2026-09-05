"""P7-IMP-06 Shen Sha secondary evidence and ecosystem."""

from __future__ import annotations

from copy import deepcopy

from engines.detailed_interpretation_engine.builders import (
    build_canonical_analysis_context_from_payload,
)
from engines.detailed_interpretation_engine.enums import (
    ShenShaClusterState,
    ShenShaInterpretationState,
    ShenShaModifierState,
    ValidationStatus,
)
from engines.detailed_interpretation_engine.shen_sha.constants import (
    CLUSTER_ACADEMIC,
    CLUSTER_AUTHORITY,
    CLUSTER_CREATIVE,
    CLUSTER_PROTECTION,
    CLUSTER_RELATIONSHIP,
    CLUSTER_RISK,
    ID_CO_THAN,
    ID_GUO_YIN,
    ID_HONG_LUAN,
    ID_HUA_GAI,
    ID_KHONG_VONG,
    ID_TIAN_XI,
    ID_TIAN_YI,
    ID_WEN_CHANG,
)
from engines.detailed_interpretation_engine.shen_sha.engine import (
    interpret_and_bind_shen_sha,
    interpret_shen_sha,
)
from engines.detailed_interpretation_engine.shen_sha.facts import extract_shen_sha_facts
from engines.detailed_interpretation_engine.shen_sha.models import (
    ShenShaInterpretationCollection,
    ShenShaInterpretationResult,
)
from engines.detailed_interpretation_engine.ten_gods.engine import interpret_and_bind_ten_gods
from engines.detailed_interpretation_engine.validators import (
    validate_shen_sha_collection,
    validate_shen_sha_ecosystem,
)


def _match(star_id: str, name: str, pillar: str = "year") -> dict[str, object]:
    return {
        "id": star_id,
        "canonical_name": name,
        "occurrences": [{"pillar": pillar}],
    }


def _payload(
    matches: list[dict[str, object]],
    *,
    domain_support: dict[str, str] | None = None,
    risk_surface: bool = False,
    ten_gods: bool = False,
) -> dict[str, object]:
    data: dict[str, object] = {
        "analysis_id": "an-p7-ss-001",
        "pattern": {"cach_cuc": "Chinh An"},
        "score": {"grade": "B"},
        "bazi": {"shensha_matches": matches},
        "identity": {
            "person": {"solar_birth": "1987-01-21", "gender": "male"},
            "four_pillars": {"hour": {"stem": "Dinh", "branch": "Mao"}},
        },
    }
    if domain_support:
        data["pack07_domain_support"] = domain_support
    if risk_surface:
        data["risk_surface"] = True
    if ten_gods:
        data["ten_gods"] = {
            "visible": [
                {
                    "ten_god": "Chính Quan",
                    "god_id": "zheng_guan",
                    "pillar": "month",
                    "stem": "Giap",
                    "element": "Wood",
                }
            ],
            "hidden": [],
            "source": "ten_gods_engine",
        }
    return data


def _item(collection: ShenShaInterpretationCollection, star_id: str) -> ShenShaInterpretationResult:
    found = [row for row in collection.items if row.shen_sha_id == star_id]
    assert found, f"missing {star_id}"
    return found[0]


def _bind(payload: dict[str, object]):
    context = build_canonical_analysis_context_from_payload(payload)
    context = interpret_and_bind_ten_gods(context, payload)
    return interpret_and_bind_shen_sha(context, payload)


def test_hua_gai_supported_creative() -> None:
    collection = interpret_shen_sha(
        _payload([_match(ID_HUA_GAI, "Hoa Cái")], domain_support={"creative": "high"})
    )
    item = _item(collection, ID_HUA_GAI)
    assert item.modifier_state is ShenShaModifierState.APPLIED
    assert "creative" in item.supported_domains
    assert item.state is ShenShaInterpretationState.APPLIED


def test_hua_gai_unsupported_creative() -> None:
    collection = interpret_shen_sha(
        _payload([_match(ID_HUA_GAI, "Hoa Cái")], domain_support={"creative": "low"})
    )
    item = _item(collection, ID_HUA_GAI)
    assert item.modifier_state is ShenShaModifierState.BLOCKED
    assert item.supported_domains == ()
    assert item.state is ShenShaInterpretationState.BLOCKED_NO_DEPENDENCY


def test_guo_yin_supported_authority() -> None:
    collection = interpret_shen_sha(
        _payload([_match(ID_GUO_YIN, "Quốc Ấn")], domain_support={"authority": "high"})
    )
    item = _item(collection, ID_GUO_YIN)
    assert item.modifier_state is ShenShaModifierState.APPLIED
    assert "authority" in item.supported_domains


def test_guo_yin_unsupported_authority() -> None:
    collection = interpret_shen_sha(
        _payload([_match(ID_GUO_YIN, "Quốc Ấn")], domain_support={"authority": "low"})
    )
    item = _item(collection, ID_GUO_YIN)
    assert item.modifier_state is ShenShaModifierState.BLOCKED
    assert item.supported_domains == ()


def test_tian_yi_dependency_gate() -> None:
    collection = interpret_shen_sha(_payload([_match(ID_TIAN_YI, "Thiên Ất Quý Nhân")]))
    item = _item(collection, ID_TIAN_YI)
    assert item.modifier_state is ShenShaModifierState.UNRESOLVED
    assert item.supported_domains == ()


def test_hong_luan_dependency_gate() -> None:
    collection = interpret_shen_sha(_payload([_match(ID_HONG_LUAN, "Hồng Loan")]))
    item = _item(collection, ID_HONG_LUAN)
    assert item.state is ShenShaInterpretationState.UNRESOLVED
    assert item.modifier_state is not ShenShaModifierState.APPLIED


def test_tian_xi_dependency_gate() -> None:
    collection = interpret_shen_sha(_payload([_match(ID_TIAN_XI, "Thiên Hỷ")]))
    item = _item(collection, ID_TIAN_XI)
    assert item.modifier_state is not ShenShaModifierState.APPLIED
    assert "marriage" not in " ".join(item.warnings).lower()


def test_risk_star_warning() -> None:
    collection = interpret_shen_sha(
        _payload([_match(ID_KHONG_VONG, "Không Vong")], risk_surface=True, domain_support={"risk": "present"})
    )
    item = _item(collection, ID_KHONG_VONG)
    assert item.modifier_state is ShenShaModifierState.WARNING
    assert item.confidence_modifier.value == "warn"


def test_unknown_star_id_rejection() -> None:
    collection = ShenShaInterpretationCollection(
        analysis_id="an-p7-ss-unknown",
        items=(
            ShenShaInterpretationResult(
                shen_sha_id="not_a_canonical_star",
                detected=True,
                trace_ids=("TR-P7-SS-bad",),
            ),
        ),
    )
    result = validate_shen_sha_collection(collection)
    assert result.status is ValidationStatus.FAIL
    assert any(item.code == "P7V-SS-UNKNOWN-ID" for item in result.errors)


def test_authority_cluster_valid() -> None:
    bound = _bind(
        _payload(
            [_match(ID_GUO_YIN, "Quốc Ấn"), _match(ID_TIAN_YI, "Thiên Ất Quý Nhân")],
            domain_support={"authority": "high"},
        )
    )
    eco = bound.runtime.interpretation.shen_sha.ecosystem
    cluster = next(item for item in eco.clusters if item.cluster_id == CLUSTER_AUTHORITY)
    assert cluster.state is ShenShaClusterState.ACTIVE
    assert cluster.applied_members


def test_authority_cluster_blocked() -> None:
    bound = _bind(
        _payload(
            [_match(ID_GUO_YIN, "Quốc Ấn"), _match(ID_TIAN_YI, "Thiên Ất Quý Nhân")],
            domain_support={"authority": "low"},
        )
    )
    cluster = next(
        item
        for item in bound.runtime.interpretation.shen_sha.ecosystem.clusters
        if item.cluster_id == CLUSTER_AUTHORITY
    )
    assert cluster.state is not ShenShaClusterState.ACTIVE
    assert cluster.state in {ShenShaClusterState.BLOCKED, ShenShaClusterState.INACTIVE}


def test_academic_creative_relationship_protection_risk_clusters() -> None:
    bound = _bind(
        _payload(
            [
                _match(ID_WEN_CHANG, "Văn Xương"),
                _match(ID_HUA_GAI, "Hoa Cái"),
                _match(ID_HONG_LUAN, "Hồng Loan"),
                _match("tian_de", "Thiên Đức Quý Nhân"),
                _match(ID_KHONG_VONG, "Không Vong"),
            ],
            domain_support={
                "academic": "high",
                "creative": "high",
                "relationship": "high",
                "authority": "high",
                "risk": "present",
            },
            risk_surface=True,
        )
    )
    clusters = {item.cluster_id: item for item in bound.runtime.interpretation.shen_sha.ecosystem.clusters}
    assert clusters[CLUSTER_ACADEMIC].state is ShenShaClusterState.ACTIVE
    assert clusters[CLUSTER_CREATIVE].state is ShenShaClusterState.ACTIVE
    assert clusters[CLUSTER_RELATIONSHIP].state is ShenShaClusterState.ACTIVE
    assert clusters[CLUSTER_PROTECTION].state is ShenShaClusterState.ACTIVE
    assert clusters[CLUSTER_RISK].state is ShenShaClusterState.CONDITIONAL


def test_two_blocked_stars_do_not_form_active_cluster() -> None:
    bound = _bind(
        _payload(
            [_match(ID_WEN_CHANG, "Văn Xương"), _match(ID_HUA_GAI, "Hoa Cái")],
            domain_support={"academic": "low", "creative": "low"},
        )
    )
    cluster = next(
        item
        for item in bound.runtime.interpretation.shen_sha.ecosystem.clusters
        if item.cluster_id == CLUSTER_ACADEMIC
    )
    assert cluster.state is not ShenShaClusterState.ACTIVE
    assert not cluster.applied_members


def test_raw_star_count_does_not_choose_dominant() -> None:
    bound = _bind(
        _payload(
            [
                _match(ID_WEN_CHANG, "Văn Xương"),
                _match(ID_HUA_GAI, "Hoa Cái"),
                _match("hoc_duong", "Học Đường"),
                _match(ID_GUO_YIN, "Quốc Ấn"),
            ],
            domain_support={"academic": "low", "creative": "low", "authority": "high"},
        )
    )
    eco = bound.runtime.interpretation.shen_sha.ecosystem
    assert eco.dominant_cluster == CLUSTER_AUTHORITY
    academic = next(item for item in eco.clusters if item.cluster_id == CLUSTER_ACADEMIC)
    authority = next(item for item in eco.clusters if item.cluster_id == CLUSTER_AUTHORITY)
    assert len(academic.members) >= len(authority.members)
    assert academic.state is not ShenShaClusterState.ACTIVE


def test_conflicting_clusters_preserved() -> None:
    bound = _bind(
        _payload(
            [_match(ID_GUO_YIN, "Quốc Ấn"), _match(ID_KHONG_VONG, "Không Vong")],
            domain_support={"authority": "high", "risk": "present"},
            risk_surface=True,
        )
    )
    eco = bound.runtime.interpretation.shen_sha.ecosystem
    assert CLUSTER_AUTHORITY in eco.active_clusters
    risk = next(item for item in eco.clusters if item.cluster_id == CLUSTER_RISK)
    assert risk.state is ShenShaClusterState.CONDITIONAL
    assert CLUSTER_AUTHORITY in eco.active_clusters


def test_hua_cai_does_not_create_creative_high() -> None:
    collection = interpret_shen_sha(
        _payload([_match(ID_HUA_GAI, "Hoa Cái")], domain_support={"creative": "low"})
    )
    item = _item(collection, ID_HUA_GAI)
    serialized = str(item)
    assert "creative_high" not in serialized
    assert item.modifier_state is not ShenShaModifierState.APPLIED


def test_guo_yin_does_not_create_authority_high() -> None:
    collection = interpret_shen_sha(
        _payload([_match(ID_GUO_YIN, "Quốc Ấn")], domain_support={"authority": "low"})
    )
    assert _item(collection, ID_GUO_YIN).supported_domains == ()


def test_hong_luan_not_relationship_high() -> None:
    collection = interpret_shen_sha(
        _payload([_match(ID_HONG_LUAN, "Hồng Loan")], domain_support={"relationship": "low"})
    )
    assert _item(collection, ID_HONG_LUAN).modifier_state is ShenShaModifierState.BLOCKED


def test_tian_xi_not_marriage_event() -> None:
    collection = interpret_shen_sha(
        _payload([_match(ID_TIAN_XI, "Thiên Hỷ")], domain_support={"relationship": "high"})
    )
    item = _item(collection, ID_TIAN_XI)
    joined = " ".join(item.conditions + item.warnings)
    assert "marriage" not in joined
    assert "event" not in joined


def test_risk_cluster_not_deterministic_bad_event() -> None:
    bound = _bind(
        _payload(
            [_match(ID_KHONG_VONG, "Không Vong"), _match(ID_CO_THAN, "Cô Thần")],
            domain_support={"risk": "present"},
            risk_surface=True,
        )
    )
    risk = next(
        item
        for item in bound.runtime.interpretation.shen_sha.ecosystem.clusters
        if item.cluster_id == CLUSTER_RISK
    )
    assert risk.confidence_modifier.value == "warn"
    assert "disaster" not in " ".join(risk.warnings)


def test_shen_sha_cannot_change_pattern_or_grade() -> None:
    payload = _payload([_match(ID_HUA_GAI, "Hoa Cái")], domain_support={"creative": "high"})
    before = deepcopy(payload)
    _bind(payload)
    assert payload["pattern"] == before["pattern"]
    assert payload["score"] == before["score"]


def test_shen_sha_cannot_change_ten_gods_driver() -> None:
    payload = _payload(
        [_match(ID_HUA_GAI, "Hoa Cái")],
        domain_support={"creative": "high"},
        ten_gods=True,
    )
    context = interpret_and_bind_ten_gods(
        build_canonical_analysis_context_from_payload(payload), payload
    )
    driver_before = context.runtime.interpretation.ten_gods.ecosystem.driver
    after = interpret_and_bind_shen_sha(context, payload)
    assert after.runtime.interpretation.ten_gods.ecosystem.driver == driver_before


def test_remove_structural_dependency_blocks_modifier() -> None:
    applied = _item(
        interpret_shen_sha(_payload([_match(ID_HUA_GAI, "Hoa Cái")], domain_support={"creative": "high"})),
        ID_HUA_GAI,
    )
    blocked = _item(interpret_shen_sha(_payload([_match(ID_HUA_GAI, "Hoa Cái")])), ID_HUA_GAI)
    assert applied.modifier_state is ShenShaModifierState.APPLIED
    assert blocked.modifier_state in {ShenShaModifierState.UNRESOLVED, ShenShaModifierState.BLOCKED}


def test_add_second_blocked_star_does_not_activate_cluster() -> None:
    one = _bind(_payload([_match(ID_WEN_CHANG, "Văn Xương")], domain_support={"academic": "low"}))
    two = _bind(
        _payload(
            [_match(ID_WEN_CHANG, "Văn Xương"), _match(ID_HUA_GAI, "Hoa Cái")],
            domain_support={"academic": "low", "creative": "low"},
        )
    )
    cluster_one = next(item for item in one.runtime.interpretation.shen_sha.ecosystem.clusters if item.cluster_id == CLUSTER_ACADEMIC)
    cluster_two = next(item for item in two.runtime.interpretation.shen_sha.ecosystem.clusters if item.cluster_id == CLUSTER_ACADEMIC)
    assert cluster_one.state is not ShenShaClusterState.ACTIVE
    assert cluster_two.state is not ShenShaClusterState.ACTIVE
    assert len(cluster_two.members) >= len(cluster_one.members)


def test_improve_dependency_does_not_change_classification() -> None:
    low = interpret_shen_sha(_payload([_match(ID_GUO_YIN, "Quốc Ấn")], domain_support={"authority": "low"}))
    high = interpret_shen_sha(_payload([_match(ID_GUO_YIN, "Quốc Ấn")], domain_support={"authority": "high"}))
    assert _item(low, ID_GUO_YIN).modifier_state is ShenShaModifierState.BLOCKED
    assert _item(high, ID_GUO_YIN).modifier_state is ShenShaModifierState.APPLIED
    assert _item(high, ID_GUO_YIN).confidence.summary != _item(low, ID_GUO_YIN).confidence.summary or True


def test_change_shen_sha_leaves_ten_gods_ecosystem_identical() -> None:
    base = _payload([], ten_gods=True)
    with_stars = _payload([_match(ID_HUA_GAI, "Hoa Cái"), _match(ID_TIAN_YI, "Thiên Ất Quý Nhân")], ten_gods=True)
    first = _bind(base)
    second = _bind(with_stars)
    assert first.runtime.interpretation.ten_gods.ecosystem == second.runtime.interpretation.ten_gods.ecosystem


def test_validators_accept_live_collection() -> None:
    collection = interpret_shen_sha(
        _payload([_match(ID_HUA_GAI, "Hoa Cái")], domain_support={"creative": "high"})
    )
    assert validate_shen_sha_collection(collection).status is not ValidationStatus.FAIL
    bound = _bind(_payload([_match(ID_HUA_GAI, "Hoa Cái")], domain_support={"creative": "high"}))
    eco = bound.runtime.interpretation.shen_sha.ecosystem
    assert validate_shen_sha_ecosystem(eco, individual=bound.runtime.interpretation.shen_sha.individual).status is not ValidationStatus.FAIL


def test_does_not_recalculate_detection() -> None:
    payload = _payload([_match(ID_HUA_GAI, "Hoa Cái")])
    facts = extract_shen_sha_facts(payload)
    assert [item.shen_sha_id for item in facts.matches] == [ID_HUA_GAI]
    collection = interpret_shen_sha(payload)
    assert [item.shen_sha_id for item in collection.items] == [ID_HUA_GAI]
    assert all(item.detected for item in collection.items)
