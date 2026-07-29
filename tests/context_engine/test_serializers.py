from engines.context_engine.builder import UnifiedContextBuilder
from engines.context_engine.serializers import serialize_context, ANALYSIS_CONTEXT_SCHEMA


def test_serialize_includes_version() -> None:
    ctx = UnifiedContextBuilder().build(
        bazi={"day_master": "Giáp"},
        pattern={"pattern": "chinh_quan"},
    )
    payload = serialize_context(ctx)
    assert payload["_version"] == "2.0.0"
    assert payload["_schema"] == ANALYSIS_CONTEXT_SCHEMA["$id"]
    assert payload["pattern"]["main"] == "chinh_quan"
