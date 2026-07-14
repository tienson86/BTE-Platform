"""
conftest.py
===========

Pytest fixtures dùng chung cho toàn bộ Interpretation Engine.
"""

from __future__ import annotations

import pytest

from engines.interpretation_engine.models import (
    InterpretationContext,
    Rule,
)


# =====================================================
# Context
# =====================================================

@pytest.fixture
def sample_context() -> InterpretationContext:
    """
    Context mẫu dùng cho tất cả test.
    """

    context = InterpretationContext()

    context.update({

        "bazi": {

            "day_master": "Canh",

            "month_branch": "Sửu",

            "hour_branch": "Dần",

        },

        "strength": {

            "level": "WEAK",

            "score": 42,

        },

        "pattern": {

            "name": "Chính Quan",

        },

        "useful_god": {

            "primary": "Hỏa",

            "secondary": "Mộc",

        }

    })

    return context


# =====================================================
# Rule
# =====================================================

@pytest.fixture
def sample_rule() -> Rule:
    """
    Rule mẫu.
    """

    return Rule(

        id="DT001",

        name="Dụng thần",

        module="useful_god",

        category="Mệnh cục",

        topic="Dụng thần",

        section="Mệnh cục",

        condition="strength.level == 'WEAK'",

        result="Mệnh chủ thân nhược, dụng thần là {useful_god.primary}.",

        priority=100,

        enabled=True,
    )


# =====================================================
# Rule List
# =====================================================

@pytest.fixture
def sample_rules(sample_rule):

    return [sample_rule]
