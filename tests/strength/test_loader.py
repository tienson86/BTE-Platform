from engines.strength_engine.loader import StrengthLoader


def test_loader_reads_all_rule_groups() -> None:
    loader = StrengthLoader("database/12_strength")
    groups = loader.load_rule_groups()
    assert "season" in groups
    assert "root" in groups
    assert "support" in groups
    assert "control" in groups
    assert "drain" in groups
    assert len(groups["season"]) >= 5


def test_loader_reads_config() -> None:
    loader = StrengthLoader("database/12_strength")
    config = loader.load_config()
    assert config["baseline"] == 50.0
    assert config["scale"] == 100.0
    assert config["strong_threshold"] == 0.65


def test_loader_reads_level_rules() -> None:
    loader = StrengthLoader("database/12_strength")
    levels = loader.load_level_rules()
    assert any(r.get("strength_level") == "strong" for r in levels)
    assert any(r.get("strength_level") == "weak" for r in levels)
