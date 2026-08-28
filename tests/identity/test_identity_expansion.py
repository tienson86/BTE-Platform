"""BZ-ID-02: expanded identity objects copy existing outputs only."""

from __future__ import annotations

import inspect

from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.identity import assemble as assemble_module
from engines.identity.assemble import (
    bone_weight_identity_from_payload,
    build_canonical_identity,
    calendar_identity_from_calendar,
    interpretation_identity_from_payload,
    luck_identity_from_payload,
    person_identity_from_sources,
)
from engines.identity.models import BoneWeightIdentity, LuckIdentity

IDENTITY_KEYS = (
    "person",
    "calendar",
    "four_pillars",
    "bone_weight",
    "luck",
    "interpretation",
)


def test_assemble_does_not_calculate_or_reload_tables() -> None:
    source = inspect.getsource(assemble_module)
    assert "DictReader" not in source
    assert "GanzhiAlgorithm" not in source
    assert "luck_engine.build" not in source
    assert "pillar_contract" not in source
    assert "01_nap_am.csv" not in source
    assert "ha_nguyen_cung.csv" not in source


def test_person_identity_copies_request_and_calendar_labels() -> None:
    calendar = CalendarEngine().build(2026, 8, 28, 12, 0)
    person = person_identity_from_sources(
        person={"full_name": "Nguyễn Văn A", "birth_place": "Hà Nội"},
        calendar=calendar,
        input_fields={"gender": "male", "timezone": "Asia/Ho_Chi_Minh"},
    )
    payload = person.to_dict()
    assert payload["full_name"] == "Nguyễn Văn A"
    assert payload["gender"] == "male"
    assert payload["solar_birth"] == calendar.solar_date
    assert payload["lunar_birth"] == calendar.lunar_date
    assert payload["birth_time"] == "12:00"
    assert payload["timezone"] == "Asia/Ho_Chi_Minh"
    assert payload["birth_place"] == "Hà Nội"


def test_calendar_identity_copies_existing_calendar_fields_only() -> None:
    calendar = CalendarEngine().build(2026, 8, 28, 12, 0)
    identity = calendar_identity_from_calendar(calendar)
    payload = identity.to_dict()
    assert payload["solar_date"] == calendar.solar_date
    assert payload["lunar_date"] == calendar.lunar_date
    assert payload["solar_term"] == calendar.solar_term.name
    assert payload["weekday"] == ""
    assert payload["season"] == ""
    copied = calendar_identity_from_calendar(
        {**calendar.to_dict(), "weekday": "Friday", "season": "Thu"}
    )
    assert copied.weekday == "Friday"
    assert copied.season == "Thu"


def test_bone_weight_identity_empty_when_unavailable() -> None:
    empty = bone_weight_identity_from_payload(None)
    assert empty.to_dict() == BoneWeightIdentity().to_dict()
    assert empty.weight == ""
    assert empty.classification == ""
    assert empty.rating == ""
    copied = bone_weight_identity_from_payload(
        {"weight": "3.2", "classification": "Trung", "rating": "B"}
    )
    assert copied.weight == "3.2"
    assert copied.classification == "Trung"
    assert copied.rating == "B"


def test_luck_identity_copies_published_cycle_fields() -> None:
    empty = luck_identity_from_payload(None)
    assert empty.to_dict() == LuckIdentity().to_dict()
    luck = luck_identity_from_payload(
        {
            "current_cycle": {"gan_zhi": "Đinh Dậu", "index": 3, "age_start": 36},
            "current_age_for_luck": 40,
            "current_dayun": {"metadata": {"reference_year": 2026}},
        }
    )
    payload = luck.to_dict()
    assert payload["current_cycle"] == "Đinh Dậu"
    assert payload["current_cycle_ganzhi"] == "Đinh Dậu"
    assert payload["current_cycle_age"] == "40"
    assert payload["cycle_index"] == "3"
    assert payload["current_year"] == "2026"


def test_interpretation_identity_uses_stable_keys_without_narrative() -> None:
    empty = interpretation_identity_from_payload(None, None).to_dict()
    assert empty["observation_id"] == "sec-observation"
    assert empty["reasoning_id"] == "sec-reasoning"
    assert empty["recommendation_id"] == "sec-recommendation"
    assert "sec-observation" in empty["section_keys"]
    copied = interpretation_identity_from_payload(
        None,
        {
            "sections": [
                {"id": "sec-observation", "body": "do-not-copy"},
                {"id": "sec-reasoning", "body": "do-not-copy"},
                {"id": "sec-recommendation", "body": "do-not-copy"},
            ]
        },
    ).to_dict()
    assert copied["observation_id"] == "sec-observation"
    assert copied["reasoning_id"] == "sec-reasoning"
    assert copied["recommendation_id"] == "sec-recommendation"
    assert "do-not-copy" not in str(copied)


def test_analysis_result_identity_contains_all_domains() -> None:
    calendar = CalendarEngine().build(2026, 8, 28, 12, 0)
    chart = BaziEngine().build(calendar, gender="male")
    identity = build_canonical_identity(
        bazi=chart,
        calendar=calendar,
        person={"full_name": "A", "gender": "male"},
        luck={"current_cycle": {"gan_zhi": "Bính Ngọ", "index": 0}},
    )
    payload = identity.to_dict()
    assert tuple(payload) == IDENTITY_KEYS
    assert payload["person"]["full_name"] == "A"
    assert payload["calendar"]["solar_date"] == calendar.solar_date
    assert payload["four_pillars"]["month"]["can_chi"] == "Bính Thân"
    assert payload["four_pillars"]["month"]["pillar_type"] == "Month"
    assert payload["bone_weight"] == {"weight": "", "classification": "", "rating": ""}
    assert payload["luck"]["current_cycle_ganzhi"] == "Bính Ngọ"
    assert payload["interpretation"]["observation_id"] == "sec-observation"
