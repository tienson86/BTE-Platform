"""BZ-ID-03: publish existing engine fields onto identity. No new calculations."""

from __future__ import annotations

import inspect

from applications.api.models.analysis_result import AnalysisMeta, AnalysisResult
from applications.api.services.bazi_truth import build_bazi_view
from applications.api.services.luck_truth import shape_luck_payload
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
from engines.identity.contract import IDENTITY_CONTRACT, UNPUBLISHED
from engines.identity.models import BoneWeightIdentity, PillarIdentity
from engines.luck_engine import LuckEngine

PILLAR_KEYS = ("year", "month", "day", "hour")
PILLAR_FIELDS = ("stem", "branch", "can_chi", "nayin_element", "cung_phi")
PERSON_FIELDS = (
    "full_name",
    "gender",
    "solar_birth",
    "lunar_birth",
    "birth_time",
    "birth_place",
    "timezone",
)


def test_publish_layer_does_not_calculate_or_lookup() -> None:
    source = inspect.getsource(assemble_module)
    assert "DictReader" not in source
    assert "GanzhiAlgorithm" not in source
    assert "from datetime" not in source
    assert "LuckEngine" not in source
    assert "luck_engine.build" not in source
    assert "01_nap_am.csv" not in source
    assert "ha_nguyen_cung.csv" not in source
    assert "can_xuong" not in source


def test_bone_weight_stays_empty_without_engine_payload() -> None:
    empty = bone_weight_identity_from_payload(None)
    assert empty.to_dict() == BoneWeightIdentity().to_dict()
    assert empty.weight == ""
    assert empty.classification == ""
    assert empty.rating == ""
    assert empty.summary == ""
    identity = build_canonical_identity().to_dict()
    assert identity["bone_weight"] == empty.to_dict()


def test_luck_publishes_existing_cycle_and_liunian_fields() -> None:
    calendar = CalendarEngine().build(1987, 1, 21, 4, 30)
    chart = BaziEngine().build(calendar, gender="male")
    luck_context = LuckEngine().build(calendar=calendar, bazi=chart)
    shaped = shape_luck_payload(luck_context)
    assert "current_liunian" not in shaped or shaped.get("current_liunian") is None
    raw = luck_context.to_dict()
    liunian = raw.get("current_liunian") or {}
    identity = build_canonical_identity(
        luck=shaped,
        luck_engine_raw=raw,
    ).luck.to_dict()
    dayun = raw.get("current_dayun") or {}
    metadata = dayun.get("metadata") or {}
    if dayun:
        assert identity["current_cycle"]
        assert identity["current_cycle_ganzhi"] == identity["current_cycle"]
        assert identity["cycle_index"] == str(dayun.get("index"))
        assert identity["reference_year"] == str(metadata.get("reference_year") or "")
    if liunian:
        assert identity["current_liunian_ganzhi"] == str(liunian.get("ganzhi") or "")
        assert identity["current_liunian_year"] == str(liunian.get("year") or "")
        civil = (liunian.get("metadata") or {}).get("civil_year")
        assert identity["current_year"] == str(civil or "")
    copied = luck_identity_from_payload(
        {
            "current_cycle": {"gan_zhi": "Đinh Dậu", "index": 2},
            "current_age_for_luck": 41,
            "current_dayun": {"metadata": {"reference_year": 2026}},
            "current_liunian": {
                "year": 2026,
                "ganzhi": "Bính Ngọ",
                "metadata": {"civil_year": 2026},
            },
        }
    ).to_dict()
    assert copied["current_cycle_ganzhi"] == "Đinh Dậu"
    assert copied["current_cycle_age"] == "41"
    assert copied["cycle_index"] == "2"
    assert copied["reference_year"] == "2026"
    assert copied["current_year"] == "2026"
    assert copied["current_liunian_ganzhi"] == "Bính Ngọ"
    assert copied["current_liunian_year"] == "2026"


def test_current_year_empty_when_liunian_not_published() -> None:
    luck = luck_identity_from_payload(
        {"current_dayun": {"metadata": {"reference_year": 2026}}}
    )
    assert luck.reference_year == "2026"
    assert luck.current_year == ""
    assert luck.current_liunian_ganzhi == ""


def test_interpretation_publishes_conclusion_action_and_section_ids() -> None:
    payload = interpretation_identity_from_payload(
        None,
        {
            "summary": {
                "next_action": "Giữ nhịp làm việc hiện tại.",
                "priority_recommendation": "Ưu tiên sức khỏe.",
            },
            "recommendations": [
                {"id": "rec-0", "action": "do-not-invent"},
            ],
            "sections": [
                {"id": "sec-observation", "paragraphs": [{"text": "do-not-copy"}]},
                {"id": "sec-reasoning", "paragraphs": [{"text": "do-not-copy"}]},
                {"id": "sec-recommendation", "paragraphs": [{"text": "do-not-copy"}]},
                {
                    "id": "sec-conclusion",
                    "paragraphs": [{"text": "Kết luận đã có."}],
                },
            ],
        },
    ).to_dict()
    assert payload["observation_id"] == "sec-observation"
    assert payload["reasoning_id"] == "sec-reasoning"
    assert payload["recommendation_id"] == "sec-recommendation"
    assert payload["conclusion_id"] == "sec-conclusion"
    assert payload["conclusion"] == "Kết luận đã có."
    assert payload["action"]["next_action"] == "Giữ nhịp làm việc hiện tại."
    assert payload["action"]["priority_recommendation"] == "Ưu tiên sức khỏe."
    assert payload["action"]["recommendation_ids"] == ["rec-0"]
    assert payload["section_keys"] == [
        "sec-observation",
        "sec-reasoning",
        "sec-recommendation",
        "sec-conclusion",
    ]
    assert "do-not-copy" not in payload["conclusion"]
    empty = interpretation_identity_from_payload(None, None).to_dict()
    assert empty["conclusion"] == ""
    assert empty["action"] == {}


def test_four_pillars_publish_stem_branch_can_chi_nayin_cung_phi() -> None:
    chart = BaziEngine().build(2026, 8, 28, 12, 0)
    four = build_canonical_identity(bazi=chart).to_dict()["four_pillars"]
    assert set(four) == set(PILLAR_KEYS)
    for key in PILLAR_KEYS:
        cell = four[key]
        for field in PILLAR_FIELDS:
            assert cell[field]
        assert set(PILLAR_FIELDS).issubset(cell)


def test_person_publishes_existing_canonical_values() -> None:
    calendar = CalendarEngine().build(2026, 8, 28, 12, 0)
    person = person_identity_from_sources(
        person={
            "full_name": "Nguyễn Văn A",
            "birth_place": "Hà Nội",
        },
        calendar=calendar,
        input_fields={"gender": "male", "timezone": "Asia/Ho_Chi_Minh"},
    ).to_dict()
    for field in PERSON_FIELDS:
        assert field in person
    assert person["full_name"] == "Nguyễn Văn A"
    assert person["gender"] == "male"
    assert person["solar_birth"] == calendar.solar_date
    assert person["lunar_birth"] == calendar.lunar_date
    assert person["birth_time"] == "12:00"
    assert person["birth_place"] == "Hà Nội"
    assert person["timezone"] == "Asia/Ho_Chi_Minh"


def test_calendar_publishes_solar_term_only_from_calendar_result() -> None:
    calendar = CalendarEngine().build(2026, 8, 28, 12, 0)
    payload = calendar_identity_from_calendar(calendar).to_dict()
    assert payload["solar_term"] == calendar.solar_term.name
    assert payload["weekday"] == ""
    assert payload["season"] == ""
    serialized = calendar.to_dict()
    assert "weekday" not in serialized
    assert "season" not in serialized
    assert "season" not in (serialized.get("solar_term") or {})


def test_analysis_result_identity_is_complete_published_layer() -> None:
    calendar = CalendarEngine().build(2026, 8, 28, 12, 0)
    chart = BaziEngine().build(calendar, gender="male")
    view = build_bazi_view(chart)
    identity = build_canonical_identity(
        bazi=view,
        calendar=calendar,
        person={"full_name": "A", "gender": "male"},
        luck={
            "current_cycle": {"gan_zhi": "Bính Ngọ", "index": 0},
            "current_liunian": {
                "year": 2026,
                "ganzhi": "Bính Ngọ",
                "metadata": {"civil_year": 2026},
            },
        },
        narrative={
            "summary": {"next_action": "Giữ nhịp."},
            "sections": [{"id": "sec-conclusion", "paragraphs": [{"text": "Đóng."}]}],
        },
    )
    analysis = AnalysisResult(
        bazi=view,
        identity=identity,
        meta=AnalysisMeta(contract_version="1.0"),
    )
    published = analysis.identity_dict()
    assert tuple(published) == (
        "person",
        "calendar",
        "four_pillars",
        "bone_weight",
        "luck",
        "interpretation",
    )
    assert published["luck"]["current_year"] == "2026"
    assert published["interpretation"]["conclusion"] == "Đóng."
    assert published["bone_weight"]["summary"] == ""


def test_contract_mapping_has_one_identity_path_per_row() -> None:
    paths = [row["identity"] for row in IDENTITY_CONTRACT]
    assert paths
    assert len(paths) == len(set(paths))
    unpublished_fields = {row["field"] for row in UNPUBLISHED}
    assert "identity.bone_weight.*" in unpublished_fields
    assert "identity.calendar.weekday" in unpublished_fields
    assert "identity.calendar.season" in unpublished_fields
    for row in IDENTITY_CONTRACT:
        assert row["owner"]
        assert row["analysis_result"].startswith("identity.")
        assert row["future_consumers"]


def test_pillar_identity_type_is_not_recalculated() -> None:
    cell = PillarIdentity(
        stem="Bính",
        branch="Ngọ",
        can_chi="Bính Ngọ",
        nayin_element="Thủy",
        cung_phi="Khảm",
        pillar_type="Year",
    )
    assert cell.to_dict()["stem"] == "Bính"
    assert cell.to_dict()["branch"] == "Ngọ"
