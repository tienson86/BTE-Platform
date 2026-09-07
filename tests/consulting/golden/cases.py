"""TV-01 Golden Dataset factories. Snapshot-level, Canonical-compatible, deterministic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from consulting.marriage.models.enums import CanonicalGender, FiveElement, PersonSide
from consulting.marriage.models.snapshot import MarriageCanonicalSnapshot, ShenShaItem
from tests.consulting.decision_fixtures import golden_pair, make_snapshot

PolicyKwargs = dict[str, object]
PairFactory = Callable[[], tuple[MarriageCanonicalSnapshot, MarriageCanonicalSnapshot, PolicyKwargs]]

_NO_WATER = {
    FiveElement.WOOD: 3.0,
    FiveElement.FIRE: 3.0,
    FiveElement.EARTH: 2.0,
    FiveElement.METAL: 2.0,
    FiveElement.WATER: 0.0,
}
_NO_FIRE = {
    FiveElement.WOOD: 3.0,
    FiveElement.FIRE: 0.0,
    FiveElement.EARTH: 4.0,
    FiveElement.METAL: 2.0,
    FiveElement.WATER: 1.0,
}
_NO_WOOD = {
    FiveElement.WOOD: 0.0,
    FiveElement.FIRE: 4.0,
    FiveElement.EARTH: 2.0,
    FiveElement.METAL: 3.0,
    FiveElement.WATER: 1.0,
}
_FIRE_ONLY = {
    FiveElement.WOOD: 0.0,
    FiveElement.FIRE: 5.0,
    FiveElement.EARTH: 3.0,
    FiveElement.METAL: 2.0,
    FiveElement.WATER: 0.0,
}


@dataclass(frozen=True, slots=True)
class GoldenCase:
    """One Golden Dataset case identity and factory."""

    case_id: str
    title: str
    category: str
    build: PairFactory


def _support_pair() -> tuple[MarriageCanonicalSnapshot, MarriageCanonicalSnapshot, PolicyKwargs]:
    """Mutual useful support with combination branches and no clash pair."""
    snapshot_a = make_snapshot(
        analysis_id="MC-M01-A",
        side=PersonSide.A,
        gender=CanonicalGender.MALE,
        day_stem="Canh",
        day_branch="Tý",
        day_element=FiveElement.METAL,
        useful=FiveElement.FIRE,
        unfavorable=None,
        year_stem="Bính",
        year_branch="Tý",
        month_stem="Tân",
        month_branch="Sửu",
        hour_stem="Mậu",
        hour_branch="Tý",
        distribution=_NO_WATER,
        ten_god_visible="Chính Quan",
        luck_stem="Bính",
        luck_branch="Ngọ",
        shen_sha=[ShenShaItem(name="Thiên Ất", polarity="support")],
    )
    snapshot_b = make_snapshot(
        analysis_id="MC-M01-B",
        side=PersonSide.B,
        gender=CanonicalGender.FEMALE,
        day_stem="Bính",
        day_branch="Sửu",
        day_element=FiveElement.FIRE,
        useful=FiveElement.WOOD,
        unfavorable=None,
        year_stem="Giáp",
        year_branch="Sửu",
        month_stem="Tân",
        month_branch="Sửu",
        hour_stem="Mậu",
        hour_branch="Sửu",
        distribution=_NO_WATER,
        ten_god_visible="Chính Quan",
        luck_stem="Giáp",
        luck_branch="Dần",
        shen_sha=[ShenShaItem(name="Thiên Ất", polarity="support")],
    )
    return snapshot_a, snapshot_b, {}


def _mixed_pair() -> tuple[MarriageCanonicalSnapshot, MarriageCanonicalSnapshot, PolicyKwargs]:
    """Existing golden pair: useful support plus Tý–Ngọ clash."""
    snapshot_a, snapshot_b = golden_pair()
    return snapshot_a, snapshot_b, {}


def _pressure_rescue_pair() -> tuple[MarriageCanonicalSnapshot, MarriageCanonicalSnapshot, PolicyKwargs]:
    """Clash and harm with useful-god rescue still present."""
    snapshot_a = make_snapshot(
        analysis_id="MC-M03-A",
        side=PersonSide.A,
        gender=CanonicalGender.MALE,
        day_stem="Canh",
        day_branch="Tý",
        day_element=FiveElement.METAL,
        useful=FiveElement.FIRE,
        unfavorable=FiveElement.WATER,
        year_stem="Canh",
        year_branch="Thân",
        month_stem="Tân",
        month_branch="Sửu",
        luck_stem="Quý",
        luck_branch="Hợi",
    )
    snapshot_b = make_snapshot(
        analysis_id="MC-M03-B",
        side=PersonSide.B,
        gender=CanonicalGender.FEMALE,
        day_stem="Bính",
        day_branch="Ngọ",
        day_element=FiveElement.FIRE,
        useful=FiveElement.WOOD,
        unfavorable=FiveElement.WATER,
        year_stem="Giáp",
        year_branch="Dần",
        month_stem="Tân",
        month_branch="Mùi",
        ten_god_visible="Thiên Ấn",
        luck_stem="Quý",
        luck_branch="Hợi",
        distribution={
            FiveElement.WOOD: 2.0,
            FiveElement.FIRE: 4.0,
            FiveElement.EARTH: 1.0,
            FiveElement.METAL: 1.0,
            FiveElement.WATER: 2.0,
        },
    )
    return snapshot_a, snapshot_b, {}


def _asymmetric_a_to_b() -> tuple[MarriageCanonicalSnapshot, MarriageCanonicalSnapshot, PolicyKwargs]:
    """A offers B's useful wood. B does not offer A's useful fire."""
    snapshot_a = make_snapshot(
        analysis_id="MC-M04-A",
        side=PersonSide.A,
        gender=CanonicalGender.MALE,
        day_stem="Giáp",
        day_branch="Dần",
        day_element=FiveElement.WOOD,
        useful=FiveElement.FIRE,
        unfavorable=None,
        year_stem="Giáp",
        year_branch="Dần",
        month_stem="Ất",
        month_branch="Mão",
        hour_stem="Giáp",
        hour_branch="Dần",
        distribution={
            FiveElement.WOOD: 5.0,
            FiveElement.FIRE: 0.0,
            FiveElement.EARTH: 2.0,
            FiveElement.METAL: 2.0,
            FiveElement.WATER: 1.0,
        },
        luck_stem="Giáp",
        luck_branch="Dần",
        shen_sha=[],
        cung_phi=None,
    )
    snapshot_b = make_snapshot(
        analysis_id="MC-M04-B",
        side=PersonSide.B,
        gender=CanonicalGender.FEMALE,
        day_stem="Mậu",
        day_branch="Thìn",
        day_element=FiveElement.EARTH,
        useful=FiveElement.WOOD,
        unfavorable=None,
        year_stem="Kỷ",
        year_branch="Sửu",
        month_stem="Kỷ",
        month_branch="Sửu",
        hour_stem="Mậu",
        hour_branch="Thìn",
        distribution=_NO_FIRE,
        luck_stem="Mậu",
        luck_branch="Thìn",
        shen_sha=[],
        cung_phi=None,
    )
    return snapshot_a, snapshot_b, {"include_shen_sha": False, "include_feng_shui_reference": False}


def _asymmetric_b_to_a() -> tuple[MarriageCanonicalSnapshot, MarriageCanonicalSnapshot, PolicyKwargs]:
    """B offers A's useful fire. A does not offer B's useful wood."""
    snapshot_a = make_snapshot(
        analysis_id="MC-M05-A",
        side=PersonSide.A,
        gender=CanonicalGender.MALE,
        day_stem="Canh",
        day_branch="Thân",
        day_element=FiveElement.METAL,
        useful=FiveElement.FIRE,
        unfavorable=None,
        year_stem="Tân",
        year_branch="Dậu",
        month_stem="Canh",
        month_branch="Thân",
        hour_stem="Tân",
        hour_branch="Dậu",
        distribution=_NO_WOOD,
        luck_stem="Canh",
        luck_branch="Thân",
        shen_sha=[],
        cung_phi=None,
    )
    snapshot_b = make_snapshot(
        analysis_id="MC-M05-B",
        side=PersonSide.B,
        gender=CanonicalGender.FEMALE,
        day_stem="Bính",
        day_branch="Ngọ",
        day_element=FiveElement.FIRE,
        useful=FiveElement.WOOD,
        unfavorable=None,
        year_stem="Đinh",
        year_branch="Tỵ",
        month_stem="Bính",
        month_branch="Ngọ",
        hour_stem="Đinh",
        hour_branch="Tỵ",
        distribution=_FIRE_ONLY,
        luck_stem="Bính",
        luck_branch="Ngọ",
        shen_sha=[],
        cung_phi=None,
    )
    return snapshot_a, snapshot_b, {"include_shen_sha": False, "include_feng_shui_reference": False}


def _secondary_favorable_core_mixed() -> tuple[MarriageCanonicalSnapshot, MarriageCanonicalSnapshot, PolicyKwargs]:
    """Core mixed pair plus extra favorable secondary references."""
    snapshot_a, snapshot_b = golden_pair()
    snapshot_a.shen_sha.items = [
        ShenShaItem(name="Thiên Ất", polarity="support", confidence=0.9),
        ShenShaItem(name="Lộc Thần", polarity="auspicious", confidence=0.8),
    ]
    snapshot_b.shen_sha.items = [
        ShenShaItem(name="Thiên Ất", polarity="support", confidence=0.9),
        ShenShaItem(name="Hồng Loan", polarity="positive", confidence=0.8),
    ]
    return snapshot_a, snapshot_b, {}


def _missing_a_hour() -> tuple[MarriageCanonicalSnapshot, MarriageCanonicalSnapshot, PolicyKwargs]:
    """Golden pair with Person A hour unknown."""
    snapshot_a, snapshot_b = golden_pair()
    snapshot_a = make_snapshot(
        analysis_id="MC-GOLDEN-A",
        side=PersonSide.A,
        gender=CanonicalGender.MALE,
        day_stem="Canh",
        day_branch="Tý",
        day_element=FiveElement.METAL,
        useful=FiveElement.FIRE,
        unfavorable=FiveElement.WATER,
        luck_stem="Quý",
        luck_branch="Hợi",
        hour_known=False,
    )
    return snapshot_a, snapshot_b, {}


def _missing_both_hours() -> tuple[MarriageCanonicalSnapshot, MarriageCanonicalSnapshot, PolicyKwargs]:
    """Golden pair with both hours unknown."""
    snapshot_a = make_snapshot(
        analysis_id="MC-GOLDEN-A",
        side=PersonSide.A,
        gender=CanonicalGender.MALE,
        day_stem="Canh",
        day_branch="Tý",
        day_element=FiveElement.METAL,
        useful=FiveElement.FIRE,
        unfavorable=FiveElement.WATER,
        luck_stem="Quý",
        luck_branch="Hợi",
        hour_known=False,
    )
    snapshot_b = make_snapshot(
        analysis_id="MC-GOLDEN-B",
        side=PersonSide.B,
        gender=CanonicalGender.FEMALE,
        day_stem="Bính",
        day_branch="Ngọ",
        day_element=FiveElement.FIRE,
        useful=FiveElement.WOOD,
        unfavorable=FiveElement.WATER,
        year_stem="Giáp",
        year_branch="Dần",
        ten_god_visible="Chính Quan",
        luck_stem="Giáp",
        luck_branch="Dần",
        hour_known=False,
        distribution={
            FiveElement.WOOD: 3.0,
            FiveElement.FIRE: 4.0,
            FiveElement.EARTH: 1.0,
            FiveElement.METAL: 1.0,
            FiveElement.WATER: 1.0,
        },
    )
    return snapshot_a, snapshot_b, {}


def _finance_pair() -> tuple[MarriageCanonicalSnapshot, MarriageCanonicalSnapshot, PolicyKwargs]:
    """Wealth-role identities that should publish finance findings/actions."""
    snapshot_a, snapshot_b = golden_pair()
    snapshot_a = make_snapshot(
        analysis_id="MC-M09-A",
        side=PersonSide.A,
        gender=CanonicalGender.MALE,
        day_stem="Canh",
        day_branch="Tý",
        day_element=FiveElement.METAL,
        useful=FiveElement.FIRE,
        unfavorable=FiveElement.WATER,
        ten_god_visible="Chính Tài",
        luck_stem="Quý",
        luck_branch="Hợi",
    )
    snapshot_b = make_snapshot(
        analysis_id="MC-M09-B",
        side=PersonSide.B,
        gender=CanonicalGender.FEMALE,
        day_stem="Bính",
        day_branch="Ngọ",
        day_element=FiveElement.FIRE,
        useful=FiveElement.WOOD,
        unfavorable=FiveElement.WATER,
        year_stem="Giáp",
        year_branch="Dần",
        ten_god_visible="Thiên Tài",
        luck_stem="Giáp",
        luck_branch="Dần",
        distribution={
            FiveElement.WOOD: 3.0,
            FiveElement.FIRE: 4.0,
            FiveElement.EARTH: 1.0,
            FiveElement.METAL: 1.0,
            FiveElement.WATER: 1.0,
        },
    )
    return snapshot_a, snapshot_b, {}


def _timing_pair() -> tuple[MarriageCanonicalSnapshot, MarriageCanonicalSnapshot, PolicyKwargs]:
    """Luck stems aligned to useful gods when the current cycle is in window."""
    snapshot_a, snapshot_b = golden_pair()
    snapshot_a = make_snapshot(
        analysis_id="MC-M10-A",
        side=PersonSide.A,
        gender=CanonicalGender.MALE,
        day_stem="Canh",
        day_branch="Tý",
        day_element=FiveElement.METAL,
        useful=FiveElement.FIRE,
        unfavorable=FiveElement.WATER,
        luck_stem="Bính",
        luck_branch="Ngọ",
    )
    snapshot_b = make_snapshot(
        analysis_id="MC-M10-B",
        side=PersonSide.B,
        gender=CanonicalGender.FEMALE,
        day_stem="Bính",
        day_branch="Ngọ",
        day_element=FiveElement.FIRE,
        useful=FiveElement.WOOD,
        unfavorable=FiveElement.WATER,
        year_stem="Giáp",
        year_branch="Dần",
        ten_god_visible="Chính Quan",
        luck_stem="Giáp",
        luck_branch="Dần",
        distribution={
            FiveElement.WOOD: 3.0,
            FiveElement.FIRE: 4.0,
            FiveElement.EARTH: 1.0,
            FiveElement.METAL: 1.0,
            FiveElement.WATER: 1.0,
        },
    )
    return snapshot_a, snapshot_b, {"include_luck": True}


def _unavailable_pair() -> tuple[MarriageCanonicalSnapshot, MarriageCanonicalSnapshot, PolicyKwargs]:
    """Any legitimate pair: D4/D6/D7 remain unpublished under current contracts."""
    return _mixed_pair()


def _dedup_pair() -> tuple[MarriageCanonicalSnapshot, MarriageCanonicalSnapshot, PolicyKwargs]:
    """Repeated pillar identities that share clash/combination predicates."""
    snapshot_a = make_snapshot(
        analysis_id="MC-M12-A",
        side=PersonSide.A,
        gender=CanonicalGender.MALE,
        day_stem="Canh",
        day_branch="Tý",
        day_element=FiveElement.METAL,
        useful=FiveElement.FIRE,
        year_stem="Canh",
        year_branch="Tý",
        month_stem="Nhâm",
        month_branch="Tý",
        hour_stem="Canh",
        hour_branch="Tý",
        luck_stem="Quý",
        luck_branch="Hợi",
    )
    snapshot_b = make_snapshot(
        analysis_id="MC-M12-B",
        side=PersonSide.B,
        gender=CanonicalGender.FEMALE,
        day_stem="Bính",
        day_branch="Ngọ",
        day_element=FiveElement.FIRE,
        useful=FiveElement.WOOD,
        year_stem="Bính",
        year_branch="Ngọ",
        month_stem="Mậu",
        month_branch="Ngọ",
        hour_stem="Bính",
        hour_branch="Ngọ",
        ten_god_visible="Chính Quan",
        luck_stem="Giáp",
        luck_branch="Dần",
    )
    return snapshot_a, snapshot_b, {}


GOLDEN_CASES: tuple[GoldenCase, ...] = (
    GoldenCase("CASE-M01", "Strong structural support", "support", _support_pair),
    GoldenCase("CASE-M02", "Mixed support and clash", "mixed", _mixed_pair),
    GoldenCase("CASE-M03", "Structural pressure with rescue", "rescue", _pressure_rescue_pair),
    GoldenCase("CASE-M04", "Asymmetric A_TO_B support", "asymmetric", _asymmetric_a_to_b),
    GoldenCase("CASE-M05", "Asymmetric B_TO_A support", "asymmetric", _asymmetric_b_to_a),
    GoldenCase("CASE-M06", "Secondary favorable, core mixed", "secondary", _secondary_favorable_core_mixed),
    GoldenCase("CASE-M07", "Missing Person A birth hour", "missing_data", _missing_a_hour),
    GoldenCase("CASE-M08", "Missing both birth hours", "missing_data", _missing_both_hours),
    GoldenCase("CASE-M09", "Finance finding and recommendation", "finance", _finance_pair),
    GoldenCase("CASE-M10", "Timing finding if legitimately supported", "timing", _timing_pair),
    GoldenCase("CASE-M11", "Unavailable D4/D6/D7", "unavailable", _unavailable_pair),
    GoldenCase("CASE-M12", "Evidence semantic deduplication", "dedup", _dedup_pair),
)

CASE_BY_ID = {item.case_id: item for item in GOLDEN_CASES}


def run_golden_case(case_id: str) -> dict:
    """Run one Golden case through Decision → Recommendation → Narrative → Report."""
    from tests.consulting.golden.signature import pipeline_from_snapshots

    case = CASE_BY_ID[case_id]
    snapshot_a, snapshot_b, policy_kwargs = case.build()
    bundle = pipeline_from_snapshots(snapshot_a, snapshot_b, **policy_kwargs)
    bundle["case_id"] = case_id
    bundle["title"] = case.title
    bundle["category"] = case.category
    bundle["signature"]["case_id"] = case_id
    return bundle
