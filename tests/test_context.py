"""
Tests for InterpretationContext
"""

import pytest

from engines.interpretation_engine.context import InterpretationContext


def test_create_context():

    ctx = InterpretationContext()

    assert ctx is not None


def test_default_values():

    ctx = InterpretationContext()

    assert ctx.bazi is not None
    assert ctx.elements is not None
    assert ctx.ten_gods is not None
    assert ctx.patterns is not None
    assert ctx.useful_god is not None


def test_assign_bazi():

    ctx = InterpretationContext()

    ctx.bazi = {
        "day_master": "Canh",
        "month_branch": "Sửu",
    }

    assert ctx.bazi["day_master"] == "Canh"


def test_assign_elements():

    ctx = InterpretationContext()

    ctx.elements = {
        "Kim": 5,
        "Mộc": 1,
    }

    assert ctx.elements["Kim"] == 5


def test_assign_ten_gods():

    ctx = InterpretationContext()

    ctx.ten_gods = {
        "Chính Quan": 2,
        "Thiên Tài": 1,
    }

    assert "Chính Quan" in ctx.ten_gods
