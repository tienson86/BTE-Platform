"""
test_service.py
===============
"""

from engines.interpretation_engine.services import (
    InterpretationService,
)


def test_service_create():

    service = InterpretationService()

    assert service is not None


def test_service_evaluate(sample_context, sample_rules):

    service = InterpretationService()

    results = service.evaluate(

        context=sample_context,

        rules=sample_rules,

    )

    assert isinstance(results, list)
