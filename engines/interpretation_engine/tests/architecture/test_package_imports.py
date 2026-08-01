"""Smoke-import architecture packages for Pack 03."""

from __future__ import annotations


def test_import_contracts() -> None:
    """Contracts package imports and exports expected symbols."""
    from engines.interpretation_engine import contracts

    assert hasattr(contracts, "Pack02InputContract")
    assert hasattr(contracts, "PackBoundaryContract")
    assert hasattr(contracts, "InterpretationOutputContract")


def test_import_api() -> None:
    """API package exports facade contracts."""
    from engines.interpretation_engine import api

    assert hasattr(api, "InterpretationEngineAPI")
    assert hasattr(api, "InterpretationRequest")
    assert hasattr(api, "InterpretationResponse")


def test_import_interpreters() -> None:
    """Interpreter skeletons export domain interfaces."""
    from engines.interpretation_engine import interpreters

    assert hasattr(interpreters, "InterpreterInterface")
    assert hasattr(interpreters, "PersonalityInterpreterInterface")


def test_pack02_is_sole_input_contract() -> None:
    """Pack 02 FinalAnalysisResult is declared as sole input."""
    from engines.interpretation_engine.contracts import Pack02InputContract, PackBoundaryContract

    input_contract = Pack02InputContract()
    boundary = PackBoundaryContract()
    assert input_contract.input_type == "FinalAnalysisResult"
    assert boundary.sole_runtime_input == "PACK_02.FinalAnalysisResult"
    assert boundary.may_mutate_pack01 is False
    assert boundary.may_bypass_pack02_final_result is False


def test_legacy_context_reexport() -> None:
    """Legacy InterpretationContext remains importable from context package."""
    from engines.interpretation_engine.context import InterpretationContext

    assert InterpretationContext is not None
