"""RB05-C wealth nodes, 4-stage phone wealth flow, later_outcome, wealth_story."""

from __future__ import annotations

from engines.number_energy import NumberEnergyEngine
from engines.number_energy.constants import FORBIDDEN_CUSTOMER_PHRASES

FORBIDDEN_WEALTH_KEYS = {
    "occurrence_id",
    "source_span",
    "energy_id",
    "strength_rank",
    "state",
    "classification",
    "rank",
    "effect_type",
    "start_index",
    "end_index",
}

GUARANTEE_PHRASES = (
    "chắc chắn phát tài",
    "chắc chắn giữ được tiền",
    "về già chắc chắn",
    "rất giàu",
    "chắc chắn giàu",
    "cuối đời sẽ",
)

GOLDEN_STAGE_LABELS = ("TÀI VẬN", "TÀI TỪ ĐÂU?", "TÀI ĐI ĐÂU?", "HẬU VẬN")
GOLDEN_STAGE_IDS = ("WF-01", "WF-02", "WF-03", "WF-04")


def _phone(number: str = "0328278786", purpose_context: str = "phone_number"):
    return NumberEnergyEngine().analyze(number, purpose_context=purpose_context)


def _assert_customer_safe(payload: dict) -> None:
    assert FORBIDDEN_WEALTH_KEYS.isdisjoint(payload.keys())
    blob = str(payload).lower()
    for phrase in (*FORBIDDEN_CUSTOMER_PHRASES, *GUARANTEE_PHRASES):
        assert phrase.lower() not in blob


def test_golden_phone_wealth_flow_four_stages() -> None:
    result = _phone()
    flow = result.wealth_flow
    assert flow is not None
    stages = [item.to_dict() for item in flow.stages]
    assert len(stages) == 4
    assert [item["id"] for item in stages] == list(GOLDEN_STAGE_IDS)
    assert [item["label"] for item in stages] == list(GOLDEN_STAGE_LABELS)

    stage1, stage2, stage3, stage4 = stages
    assert stage1["headline"] == "Có Thiên Y"
    assert stage1["evidence"] == "27 · 86"
    assert stage1["interaction"] == ""
    assert "rất giàu" not in stage1["narrative"]

    assert stage2["headline"] == "Quý nhân & cơ hội"
    assert stage2["evidence"] == "827"
    assert stage2["interaction"] == "Sinh Khí → Thiên Y"

    assert stage3["headline"] == "Sự nghiệp & lập nghiệp"
    assert stage3["evidence"] == "278"
    assert stage3["interaction"] == "Thiên Y → Diên Niên"

    assert stage4["headline"] == "Thiên Y"
    assert stage4["evidence"] == "786"
    assert stage4["interaction"] == "Diên Niên → Thiên Y"
    assert stage4["narrative"].startswith("Phần cuối dãy")
    assert "về già" not in stage4["narrative"].lower()

    for item in stages:
        _assert_customer_safe(item)
        assert item["interpretation_status"] == "DEFINED"


def test_golden_phone_later_outcome_and_story() -> None:
    result = _phone()
    later = result.later_outcome
    assert later is not None
    payload = later.to_dict()
    assert payload["terminal_pair_digits"] == "86"
    assert payload["terminal_energy_label"] == "Thiên Y"
    assert payload["terminal_triple_digits"] == "786"
    assert payload["terminal_interaction_label"] == "Diên Niên → Thiên Y"
    assert payload["customer_summary"]
    assert payload["customer_summary"].startswith("Phần cuối dãy quy về Thiên Y")
    _assert_customer_safe(payload)

    story = result.wealth_story
    assert story is not None
    story_payload = story.to_dict()
    assert story_payload["nodes"] == [
        "Quý nhân & cơ hội",
        "Tài",
        "Sự nghiệp",
        "Tài",
    ]
    assert story_payload["display"] == "Quý nhân & cơ hội → Tài → Sự nghiệp → Tài"
    assert "Quý nhân & cơ hội → Tài → Sự nghiệp → Tài" in story_payload["display"]
    assert story_payload["synthesis"]
    _assert_customer_safe(story_payload)


def test_golden_phone_wealth_nodes_roles_and_safety() -> None:
    nodes = [item.to_dict() for item in _phone().wealth_nodes]
    roles = [item["role"] for item in nodes]
    assert roles.count("PRESENCE") == 2
    assert "SOURCE" in roles
    assert "DESTINATION" in roles
    assert "LATER_OUTCOME" in roles
    by_role = {item["role"]: item for item in nodes if item["role"] != "PRESENCE"}
    presence = [item for item in nodes if item["role"] == "PRESENCE"]
    assert [item["evidence_digits"] for item in presence] == ["27", "86"]
    assert by_role["SOURCE"]["evidence_digits"] == "827"
    assert by_role["SOURCE"]["customer_headline"] == "Quý nhân & cơ hội"
    assert by_role["SOURCE"]["interaction_label"] == "Sinh Khí → Thiên Y"
    assert by_role["DESTINATION"]["evidence_digits"] == "278"
    assert by_role["DESTINATION"]["customer_headline"] == "Sự nghiệp & lập nghiệp"
    assert by_role["LATER_OUTCOME"]["evidence_digits"] == "786"
    assert by_role["LATER_OUTCOME"]["target_energy_label"] == "Thiên Y"
    for item in nodes:
        _assert_customer_safe(item)
        assert item["interpretation_status"] == "DEFINED"


def test_non_phone_does_not_emit_phone_wealth_flow() -> None:
    result = _phone(purpose_context="car_plate")
    assert result.wealth_nodes == ()
    assert result.wealth_flow is None
    assert result.later_outcome is None
    assert result.wealth_story is None


def test_phone_without_source_still_has_four_stages() -> None:
    result = _phone("103")
    assert result.wealth_flow is not None
    stages = [item.to_dict() for item in result.wealth_flow.stages]
    assert len(stages) == 4
    assert stages[0]["headline"] == "Có Thiên Y"
    assert stages[0]["evidence"] == "13"
    assert stages[1]["interpretation_status"] == "UNDEFINED"
    assert stages[2]["interpretation_status"] == "UNDEFINED"
    assert stages[3]["headline"] == "Thiên Y"
    later = result.later_outcome
    assert later is not None
    assert later.terminal_pair_digits == "13"
    assert later.terminal_energy_label == "Thiên Y"
    assert later.terminal_triple_digits is None
    for item in stages:
        _assert_customer_safe(item)
