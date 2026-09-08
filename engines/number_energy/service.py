"""Number Energy service — orchestrates parse, pair, modifier, interaction, narrative."""

from __future__ import annotations

from engines.number_energy.exceptions import NumberEnergyEngineError, NumberEnergyValidationError
from engines.number_energy.interaction_engine import apply_interactions
from engines.number_energy.modifier_engine import generate_modifier_pairs
from engines.number_energy.narrative_engine import collect_expert_notes, compose_narrative
from engines.number_energy.pair_engine import generate_adjacent_pairs
from engines.number_energy.parser import parse_number_string
from engines.number_energy.types import (
    NumberEnergyResult,
    PurposeContext,
    UndefinedSegment,
)


class NumberEnergyService:
    """Public service for Number Energy Engine V1 (Bát Cực Linh Số)."""

    def analyze(
        self,
        number: str,
        *,
        purpose_context: str = PurposeContext.GENERIC_NUMBER.value,
    ) -> NumberEnergyResult:
        """Analyze a digit string using only frozen V1 number-energy rules."""
        context = self._validate_purpose(purpose_context)
        try:
            parsed = parse_number_string(number)
            adjacent, undefined_adjacent = generate_adjacent_pairs(parsed)
            bridged, undefined_bridged = generate_modifier_pairs(parsed)
            undefined = _merge_undefined(undefined_adjacent, undefined_bridged)
            (
                occurrences,
                undefined,
                summary,
                approved,
                sequence_state,
                sequence_states,
            ) = apply_interactions(parsed, adjacent, bridged, undefined)
            narrative = compose_narrative(
                input_raw=parsed.input_raw,
                occurrences=occurrences,
                undefined=undefined,
                summary=summary,
                purpose_context=context,
                approved_patterns=approved,
            )
            return NumberEnergyResult(
                input_raw=parsed.input_raw,
                raw_digits=parsed.raw_digits,
                classified_digits=parsed.classified_digits,
                occurrences=occurrences,
                undefined_segments=undefined,
                sequence_state=sequence_state,
                sequence_states=sequence_states,
                approved_patterns=approved,
                purpose_context=context,
                summary=summary,
                narrative=narrative,
                expert_notes=collect_expert_notes(occurrences),
            )
        except NumberEnergyEngineError:
            raise
        except Exception as exc:
            raise NumberEnergyEngineError(
                f"Number energy analysis failed: {exc}"
            ) from exc

    def _validate_purpose(self, purpose_context: str) -> str:
        """Accept only frozen V1 purpose contexts."""
        allowed = {item.value for item in PurposeContext}
        if purpose_context not in allowed:
            raise NumberEnergyValidationError(
                f"purpose_context is not frozen in V1: {purpose_context}"
            )
        return purpose_context


def _merge_undefined(
    left: tuple[UndefinedSegment, ...],
    right: tuple[UndefinedSegment, ...],
) -> tuple[UndefinedSegment, ...]:
    """Merge undefined spans, dropping exact duplicates."""
    merged: list[UndefinedSegment] = []
    seen: set[tuple[tuple[int, int], str, str]] = set()
    for item in (*left, *right):
        key = (item.source_span, item.source_digits, item.reason)
        if key in seen:
            continue
        seen.add(key)
        merged.append(item)
    return tuple(merged)
