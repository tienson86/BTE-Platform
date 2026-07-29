import pytest

from engines.context_engine.builder import UnifiedContextBuilder
from engines.context_engine.validators import ContextValidationError, ContextValidator


def test_validator_passes_complete_context() -> None:
    ctx = UnifiedContextBuilder().build(
        bazi={"day_master": "Giáp", "month_branch": "Dần"},
        strength={"strength_level": "strong", "strength_score": 0.7},
        temperature={"temperature_level": "warm", "type": "warm", "temperature_score": 0.55},
        pattern={"pattern": "chinh_quan"},
        useful_god={"useful_god": "Chính Quan"},
    )
    report = ContextValidator().validate(ctx)
    assert report["valid"] is True
    assert "strength" in report["field_inventory"]


def test_validator_fails_missing_day_master() -> None:
    ctx = UnifiedContextBuilder().build()
    with pytest.raises(ContextValidationError):
        ContextValidator().validate(ctx)
