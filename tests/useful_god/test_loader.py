from engines.useful_god_engine.loader import UsefulGodLoader


def test_loader_loads_groups() -> None:
    loader = UsefulGodLoader("database/13_useful_god")
    grouped = loader.load_rule_groups()
    assert "strength" in grouped
    assert "season" in grouped
    assert len(grouped["strength"]) > 0
