import pytest

from engines.useful_god_engine.loader import UsefulGodLoader


def test_loader_loads_groups() -> None:
    loader = UsefulGodLoader("database/13_useful_god")
    grouped = loader.load_rule_groups()
    assert "strength" in grouped
    assert "season" in grouped
    assert len(grouped["strength"]) > 0


def test_loader_rejects_duplicate_rule_ids() -> None:
    with pytest.raises(ValueError, match="Duplicate Useful God rule_id"):
        UsefulGodLoader._validate_rule_pack(
            {
                "strength": [{"rule_id": "dup", "conditions": "[]"}],
                "flow": [{"rule_id": "dup", "conditions": "[]"}],
            }
        )


def test_loader_rejects_favorable_unfavorable_overlap() -> None:
    with pytest.raises(ValueError, match="overlap"):
        UsefulGodLoader._validate_rule_pack(
            {
                "strength": [
                    {
                        "rule_id": "bad",
                        "conditions": "[]",
                        "favorable_gods": '["Nhâm"]',
                        "unfavorable_gods": '["Nhâm"]',
                    }
                ]
            }
        )
