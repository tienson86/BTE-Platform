"""Golden tests for BTE-WEALTH-01."""

from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.wealth_reasoning import (
    analyze_wealth_modifier,
    build_wealth_reasoning,
)


def _case_0001_payload() -> dict:
    return OrchestratorService().analyze(
        year=1987,
        month=1,
        day=21,
        hour=4,
        minute=30,
        gender="male",
        timezone="Asia/Ho_Chi_Minh",
    )


def test_case_0001_natal_wealth_truth() -> None:
    wealth = build_wealth_reasoning(_case_0001_payload())

    assert wealth["status"] == "ready"
    assert wealth["core_rule"] == "Presence of Wealth Star must never directly produce a favorable wealth conclusion"
    assert wealth["day_master"]["stem"] == "Canh"
    assert wealth["wealth_stems"] == {"indirect_wealth": "Giáp", "direct_wealth": "Ất"}

    indirect = wealth["stars"]["indirect_wealth"]
    assert indirect["stem"] == "Giáp"
    assert indirect["natal_present"] is True
    assert indirect["count"] == 2
    assert indirect["rooted"] is True
    assert indirect["exposed"] is False
    assert [(item["pillar"], item["branch"], item["hidden_level"]) for item in indirect["occurrences"]] == [
        ("year", "Dần", "primary"),
        ("hour", "Dần", "primary"),
    ]

    direct = wealth["stars"]["direct_wealth"]
    assert direct["stem"] == "Ất"
    assert direct["natal_present"] is False

    peer = wealth["findings"][3]["evidence_chain"]
    assert "visible:month:Tân" in peer
    assert wealth["flow"]["observed_flow"] == "Giáp → Bính → Mậu → Canh"
    assert wealth["flow"]["state"] == "wealth_generates_officer"
    assert "latent_wealth" in wealth["states"]
    assert "rooted_wealth" in wealth["states"]
    assert "wealth_present_not_obtained" in wealth["states"]
    assert "wealth_obtainable" in wealth["states"]


def test_case_0001_money_source_is_evidence_based_not_job_based() -> None:
    wealth = build_wealth_reasoning(_case_0001_payload())
    source_ids = {item["id"] for item in wealth["money_sources"]}

    assert {
        "market_network_clients",
        "expertise_reputation_trust",
        "long_term_projects_assets",
    }.issubset(source_ids)
    customer_text = " ".join(wealth["customer"]["paragraphs"])
    assert "Tiền đến từ đâu?" in customer_text
    assert "Kiếm tiền bằng cách nào?" in customer_text
    assert "Điểm rò tiền" in customer_text
    assert "Khả năng giữ tiền" in customer_text
    assert "Con đường tích sản" in customer_text
    assert "nghề hiện tại" in customer_text
    assert "Engine" not in customer_text
    assert "phát tài" not in customer_text


def test_case_0001_required_luck_and_annual_modifiers() -> None:
    payload = _case_0001_payload()
    expectations = {
        "Ất Tỵ": {"stem_combine_with_day_master", "wealth_roots_punished_or_harmed", "direct_wealth_exposed"},
        "Mậu Thân": {"wealth_roots_moving", "restructuring_volatility"},
        "Canh Tuất": {"peer_competition", "three_harmony_fire_candidate"},
        "Tân Hợi": {"wealth_roots_combined", "wealth_contested_by_peer"},
        "Giáp Dần": {"indirect_wealth_exposed", "wealth_root_repeated"},
        "Ất Mão": {"direct_wealth_exposed", "strong_direct_wealth_branch_activation"},
        "Canh Thân": {"peer_competition", "wealth_roots_moving", "restructuring_volatility"},
        "Quý Hợi": {"wealth_roots_combined"},
        "Giáp Tý": {"indirect_wealth_exposed"},
        "Ất Sửu": {"direct_wealth_exposed"},
        "Bính Dần": {"wealth_root_repeated"},
    }
    for gan_zhi, expected_effects in expectations.items():
        reading = analyze_wealth_modifier(payload, gan_zhi=gan_zhi)
        assert expected_effects.issubset(set(reading["effects"])), gan_zhi
        assert reading["does_not_override_natal_truth"] is True
        assert "tự động" in reading["reading"] or reading["effects"]


def test_case_0001_ding_wei_storage_is_not_raw_rich_rule() -> None:
    reading = analyze_wealth_modifier(_case_0001_payload(), gan_zhi="Đinh Mùi", label="2043-2053", kind="dayun")
    storage = reading["storage"]

    assert "wealth_storage_present" in reading["effects"]
    assert storage["wealth_storage_branch"] == "Mùi"
    assert storage["modifier_storage_present"] is True
    assert storage["storage_has_wealth"] is True
    assert storage["wealth_entering_storage"] is True
    assert storage["storage_opened"] is True
    assert "Sửu" in storage["opened_by"]
    assert "giàu" not in reading["reading"]
