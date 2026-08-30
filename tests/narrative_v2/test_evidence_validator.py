"""EvidenceValidator tests (N-IMP-02)."""

from __future__ import annotations

from typing import Any

import pytest

from engines.narrative_v2.evidence import (
    EvidenceBuilder,
    EvidenceItem,
    EvidenceReference,
    EvidenceValidationError,
    EvidenceValidator,
    NarrativeEvidenceContext,
)
from engines.narrative_v2.evidence.evidence_item import STATUS_AVAILABLE


def _item(**overrides: object) -> EvidenceItem:
    base = dict(
        evidence_id="evidence.strength.level",
        domain="strength",
        key="strength_level",
        label="strength class",
        value="strong",
        source_path="strength.strength_level",
        status=STATUS_AVAILABLE,
        references=(
            EvidenceReference(source_path="strength.strength_level", domain="strength"),
        ),
    )
    base.update(overrides)
    return EvidenceItem(**base)  # type: ignore[arg-type]


def test_e4_duplicate_ids_fail() -> None:
    item = _item()
    context = NarrativeEvidenceContext(
        identity=(),
        calendar=(),
        bazi=(),
        strength=(item, item),
        temperature=(),
        pattern=(),
        useful_god=(),
        five_elements=(),
        ten_gods=(),
        shensha=(),
        luck=(),
        references=item.references,
        metadata=(),
        items=(item, item),
        contract_gaps=(),
    )
    with pytest.raises(EvidenceValidationError, match="Duplicate"):
        EvidenceValidator().assert_valid(context)


def test_e5_source_paths_are_traceable(case_0001_canonical: dict[str, Any]) -> None:
    context = EvidenceBuilder().build(case_0001_canonical)
    for item in context.items:
        if item.status != STATUS_AVAILABLE:
            continue
        assert item.source_path
        assert item.references
        root = item.source_path.split(".", 1)[0]
        assert root in case_0001_canonical or root in {
            "identity",
            "calendar",
            "bazi",
            "strength",
            "temperature",
            "pattern",
            "useful_god",
            "five_elements",
            "ten_gods",
            "luck",
            "analysis_id",
            "input",
            "request_id",
            "result_meta",
        }


def test_validator_rejects_customer_prose() -> None:
    item = _item(value="Bạn có nội lực tốt.")
    context = NarrativeEvidenceContext(
        identity=(),
        calendar=(),
        bazi=(),
        strength=(item,),
        temperature=(),
        pattern=(),
        useful_god=(),
        five_elements=(),
        ten_gods=(),
        shensha=(),
        luck=(),
        references=item.references,
        metadata=(),
        items=(item,),
        contract_gaps=(),
    )
    with pytest.raises(EvidenceValidationError, match="Customer prose"):
        EvidenceValidator().assert_valid(context)


def test_validator_rejects_non_canonical_source_path() -> None:
    item = _item(source_path="narrative_result.summary")
    context = NarrativeEvidenceContext(
        identity=(),
        calendar=(),
        bazi=(),
        strength=(item,),
        temperature=(),
        pattern=(),
        useful_god=(),
        five_elements=(),
        ten_gods=(),
        shensha=(),
        luck=(),
        references=item.references,
        metadata=(),
        items=(item,),
        contract_gaps=(),
    )
    with pytest.raises(EvidenceValidationError, match="not canonical"):
        EvidenceValidator().assert_valid(context)
