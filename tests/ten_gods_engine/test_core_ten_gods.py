"""Unit tests for Ten Gods Core Engine."""

from __future__ import annotations

import json

import pytest

from engines.bazi_engine.ten_god import ten_god_name
from engines.ten_gods_engine import TenGodsEngine, TenGodsValidationError, run_case_0001
from engines.ten_gods_engine.constants import (
    GOD_ID_TO_LABEL,
    LABEL_TO_GOD_ID,
    TEN_GOD_LABELS,
)
from engines.ten_gods_engine.interaction_matrix import INTERACTION_SEMANTICS
from engines.ten_gods_engine.loader import HiddenStemWeightLoader
from engines.ten_gods_engine.mapper import map_stem_to_ten_god


@pytest.fixture
def engine() -> TenGodsEngine:
    return TenGodsEngine()


class TestCanonicalMapping:
    @pytest.mark.parametrize(
        ("day_master", "other_stem", "expected_label"),
        [
            ("Giáp", "Giáp", "Tỷ Kiên"),
            ("Giáp", "Ất", "Kiếp Tài"),
            ("Giáp", "Bính", "Thực Thần"),
            ("Giáp", "Đinh", "Thương Quan"),
            ("Giáp", "Mậu", "Thiên Tài"),
            ("Giáp", "Kỷ", "Chính Tài"),
            ("Giáp", "Canh", "Thất Sát"),
            ("Giáp", "Tân", "Chính Quan"),
            ("Giáp", "Nhâm", "Thiên Ấn"),
            ("Giáp", "Quý", "Chính Ấn"),
        ],
    )
    def test_all_ten_gods_mapping(
        self,
        day_master: str,
        other_stem: str,
        expected_label: str,
    ) -> None:
        assert ten_god_name(day_master, other_stem) == expected_label
        if other_stem != day_master:
            label, god_id = map_stem_to_ten_god(day_master, other_stem)
            assert label == expected_label
            assert god_id == LABEL_TO_GOD_ID[expected_label]
        else:
            label, god_id = map_stem_to_ten_god(day_master, other_stem)
            assert label == "Tỷ Kiên"
            assert god_id == LABEL_TO_GOD_ID["Tỷ Kiên"]
            presented, presented_id = map_stem_to_ten_god(
                day_master,
                other_stem,
                pillar="day",
                visibility="visible",
            )
            assert presented == "Nhật Chủ"
            assert presented_id == "day_master"

    def test_yin_yang_polarity_mapping(self) -> None:
        """Same element + same polarity → Tỷ Kiên; diff polarity → Kiếp Tài."""
        assert ten_god_name("Giáp", "Giáp") == "Tỷ Kiên"
        assert map_stem_to_ten_god("Giáp", "Ất")[0] == "Kiếp Tài"

    def test_ten_labels_complete(self) -> None:
        assert len(TEN_GOD_LABELS) == 10
        assert set(LABEL_TO_GOD_ID) == set(TEN_GOD_LABELS)
        assert set(GOD_ID_TO_LABEL.values()) == set(TEN_GOD_LABELS)


class TestHiddenStemWeights:
    def test_canonical_hidden_weights_exist(self) -> None:
        loader = HiddenStemWeightLoader()
        slots = loader.load_branch_slots("Sửu")
        assert len(slots) == 3
        assert slots[0].hidden_stem == "Kỷ"
        assert slots[0].weight == 0.6
        assert slots[1].weight == 0.3
        assert slots[2].weight == 0.1

    def test_ngọ_two_stem_weights(self) -> None:
        loader = HiddenStemWeightLoader()
        slots = loader.load_branch_slots("Ngọ")
        assert len(slots) == 2
        assert slots[0].weight == 0.7
        assert slots[1].weight == 0.3


class TestVisibleAndHiddenLayers:
    def test_visible_stems_mapped(self, engine: TenGodsEngine) -> None:
        result = engine.calculate_from_stems(
            day_master="Canh",
            year_stem="Bính",
            year_branch="Dần",
            month_stem="Tân",
            month_branch="Sửu",
            day_stem="Canh",
            day_branch="Ngọ",
            hour_stem="Mậu",
            hour_branch="Dần",
        )
        visible_by_pillar = {entry.pillar: entry.ten_god for entry in result.visible}
        assert visible_by_pillar["year"] == "Thất Sát"
        assert visible_by_pillar["month"] == "Kiếp Tài"
        assert visible_by_pillar["day"] == "Nhật Chủ"
        assert visible_by_pillar["hour"] == "Thiên Ấn"
        assert len(result.hidden) == 11

    def test_hidden_stems_have_weights(self, engine: TenGodsEngine) -> None:
        result = run_case_0001()
        assert all(entry.weight > 0 for entry in result.hidden)
        assert sum(1 for w in result.weights if w.layer == "hidden") == 11


class TestDistributionAndWeighting:
    def test_occurrence_and_weight_separate(self, engine: TenGodsEngine) -> None:
        result = run_case_0001()
        for entry in result.distribution:
            if entry.god_id == "day_master":
                continue
            assert entry.occurrence_count >= 0
            assert entry.weighted_contribution >= 0
            if entry.visible_count > 0:
                assert entry.weighted_contribution >= float(entry.visible_count)


class TestDominanceAndHierarchy:
    def test_dominance_policy_runs(self) -> None:
        result = run_case_0001()
        assert result.dominant.status in {"DETERMINED", "UNDETERMINED"}
        assert result.dominant.policy
        assert "day_master" not in result.dominant.weighted_totals

    def test_hierarchy_covers_ten_gods(self) -> None:
        result = run_case_0001()
        hierarchy_ids = {entry.god_id for entry in result.hierarchy}
        assert hierarchy_ids == set(LABEL_TO_GOD_ID.values())
        tiers = {entry.tier for entry in result.hierarchy}
        assert tiers.issubset(
            {
                "PRIMARY",
                "SECONDARY",
                "SUPPORTING",
                "DORMANT",
                "UNDETERMINED",
            }
        )


class TestRelationshipsAndMatrix:
    def test_relationship_graph_present(self) -> None:
        result = run_case_0001()
        assert result.relationships
        relations = {edge.relation for edge in result.relationships}
        assert relations.issubset({"generation", "restriction", "support"})

    def test_interaction_matrix_semantics_documented(self) -> None:
        assert INTERACTION_SEMANTICS["SUPPORT"]
        assert INTERACTION_SEMANTICS["CONTROL"]
        assert INTERACTION_SEMANTICS["DRAIN"]

    def test_interaction_matrix_square(self) -> None:
        result = run_case_0001()
        present = {
            entry.god_id
            for entry in result.visible + result.hidden
            if entry.god_id != "day_master"
        }
        assert len(result.interaction_matrix) == len(present) ** 2


class TestDeterministicSerialization:
    def test_to_dict_roundtrip(self, engine: TenGodsEngine) -> None:
        from engines.ten_gods_engine.models import TenGodsResult

        first = run_case_0001()
        rebuilt = TenGodsResult.from_dict(first.to_dict())
        assert rebuilt.to_dict() == first.to_dict()

    def test_json_stable(self) -> None:
        left = json.dumps(run_case_0001().to_dict(), sort_keys=True)
        right = json.dumps(run_case_0001().to_dict(), sort_keys=True)
        assert left == right


class TestValidation:
    def test_missing_pillar_fails(self, engine: TenGodsEngine) -> None:
        with pytest.raises(TenGodsValidationError):
            engine.calculate(
                day_master="Canh",
                pillars={
                    "year": {"stem": "Bính", "branch": "Dần"},
                    "month": {"stem": "Tân", "branch": "Sửu"},
                    "day": {"stem": "Canh", "branch": "Ngọ"},
                },
            )
