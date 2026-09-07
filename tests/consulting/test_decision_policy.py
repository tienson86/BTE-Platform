"""TV1-B03 Marriage Policy and Policy Context tests."""

from __future__ import annotations

from consulting.marriage.models.enums import FiveElement
from consulting.marriage.policy.provider import MarriagePolicyV1Provider
from consulting.marriage.policy.v1 import load_marriage_policy_v1
from consulting.marriage.policy.versions import POLICY_ID, POLICY_VERSION, policy_version_token
from tests.consulting.decision_fixtures import golden_pair, make_snapshot, policy_context_for
from consulting.marriage.models.enums import CanonicalGender, PersonSide


def test_marriage_policy_loads_version() -> None:
    """marriage.policy.v1 is the executable canonical policy."""
    policy = load_marriage_policy_v1()
    provider = MarriagePolicyV1Provider(policy)
    descriptor = provider.descriptor()
    assert descriptor.policy_id == POLICY_ID
    assert descriptor.version == POLICY_VERSION
    assert policy_version_token() == "marriage.policy.v1@1.0.0"
    assert policy.objectives == (
        "relationship_stability",
        "family_harmony",
        "mutual_growth",
    )
    assert [item.domain.value for item in policy.domains] == [
        "five_elements",
        "stem_branch",
        "ten_gods",
        "interaction",
        "finance",
        "family",
        "children",
        "luck",
    ]
    tiers = {item.domain.value: item.tier for item in policy.domains}
    assert tiers["five_elements"] == 1
    assert tiers["stem_branch"] == 1
    assert tiers["ten_gods"] == 1
    assert tiers["interaction"] == 2
    assert tiers["luck"] == 3


def test_policy_context_is_read_only_and_preserves_snapshots() -> None:
    """Policy Context exposes canonical snapshots without mutating them."""
    snapshot_a, snapshot_b = golden_pair()
    original_stem = snapshot_a.day_master.stem
    original_id = snapshot_a.source_analysis_id
    context = policy_context_for(snapshot_a, snapshot_b)
    assert context.snapshot_a is snapshot_a
    assert context.snapshot_b is snapshot_b
    assert context.source_analysis_id_a == "MC-GOLDEN-A"
    assert context.source_analysis_id_b == "MC-GOLDEN-B"
    assert context.snapshot_a.day_master.stem == original_stem
    assert context.snapshot_a.source_analysis_id == original_id
    assert context.limitations == ()


def test_policy_context_preserves_missing_hour_limitation() -> None:
    """Missing birth hour is a limitation, not a hidden default."""
    snapshot_a = make_snapshot(
        analysis_id="MC-HOUR-A",
        side=PersonSide.A,
        gender=CanonicalGender.MALE,
        day_stem="Canh",
        day_branch="Tý",
        day_element=FiveElement.METAL,
        useful=FiveElement.FIRE,
        hour_known=False,
    )
    snapshot_b, _unused = golden_pair()
    context = policy_context_for(snapshot_a, snapshot_b)
    assert "birth_time_unknown" in context.limitations
    assert context.snapshot_a.pillars.hour is None
