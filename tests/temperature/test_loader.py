from engines.temperature_engine.loader import TemperatureLoader


def test_loader_reads_all_rule_groups() -> None:
    loader = TemperatureLoader("database/11_temperature")
    groups = loader.load_rule_groups()
    assert "season" in groups
    assert "climate" in groups
    assert "dryness" in groups
    assert "humidity" in groups
    assert len(groups["climate"]) >= 4


def test_loader_reads_config() -> None:
    loader = TemperatureLoader("database/11_temperature")
    config = loader.load_config()
    assert config["baseline"] == 35.0
    assert config["hot_threshold"] == 0.65


def test_loader_reads_level_rules() -> None:
    loader = TemperatureLoader("database/11_temperature")
    levels = loader.load_level_rules()
    assert any(r.get("temperature_level") == "hot" for r in levels)
    assert any(r.get("temperature_level") == "cold" for r in levels)
