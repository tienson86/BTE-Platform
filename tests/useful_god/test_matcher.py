from engines.useful_god_engine.matcher import UsefulGodMatcher


class Dummy:
    strength_level = "weak"
    tags = ["a", "b"]


def test_matcher_supports_contains() -> None:
    m = UsefulGodMatcher()
    rule = {
        "conditions": '[{"field":"strength_level","operator":"==","value":"weak"},{"field":"tags","operator":"contains","value":"a"}]'
    }
    assert m.match(Dummy(), rule)
