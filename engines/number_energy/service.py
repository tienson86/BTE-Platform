"""Number Energy service — orchestrates parse, pair, modifier, interaction, narrative."""

from __future__ import annotations

from engines.number_energy.exceptions import NumberEnergyEngineError, NumberEnergyValidationError
from engines.number_energy.interaction_engine import apply_interactions
from engines.number_energy.modifier_engine import generate_modifier_pairs
from engines.number_energy.narrative_engine import collect_expert_notes, compose_narrative
from engines.number_energy.pair_engine import generate_adjacent_pairs
from engines.number_energy.parser import parse_number_string
from engines.number_energy.phone_input import split_phone_input
from engines.number_energy.plate_input import normalize_plate_input
from engines.number_energy.presentation_assessment import build_phone_assessment
from engines.number_energy.presentation_findings import build_phone_findings
from engines.number_energy.presentation_pairs import (
    build_energy_distribution,
    build_pair_occurrences,
    build_pair_summary,
)
from engines.number_energy.presentation_score import build_phone_score
from engines.number_energy.presentation_triples import build_chain, build_triple_occurrences
from engines.number_energy.presentation_wealth import build_phone_wealth
from engines.number_energy.reading import build_reading
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
            leading_zero = False
            input_raw, analyzed_raw = self._prepare_input(number, context)
            if context == PurposeContext.PHONE_NUMBER.value:
                analyzed_raw, leading_zero = split_phone_input(analyzed_raw)
                if not analyzed_raw:
                    raise NumberEnergyValidationError("number input must not be empty")
            parsed = parse_number_string(analyzed_raw)
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
                input_raw=input_raw,
                occurrences=occurrences,
                undefined=undefined,
                summary=summary,
                purpose_context=context,
                approved_patterns=approved,
            )
            result = NumberEnergyResult(
                input_raw=input_raw,
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
                analyzed_input=parsed.input_raw,
                leading_phone_zero=leading_zero,
                pair_occurrences=build_pair_occurrences(occurrences),
                pair_summary=build_pair_summary(occurrences),
                energy_distribution=build_energy_distribution(occurrences),
            )
            triples = build_triple_occurrences(occurrences)
            result.triple_occurrences = triples
            result.chain = build_chain(occurrences, triples)
            (
                result.wealth_nodes,
                result.wealth_flow,
                result.later_outcome,
                result.wealth_story,
            ) = build_phone_wealth(context, occurrences, triples, result.chain)
            (
                result.domain_insights,
                result.strengths,
                result.cautions,
                result.evidence,
            ) = build_phone_findings(
                context,
                result.pair_occurrences,
                result.pair_summary,
                result.energy_distribution,
                triples,
                result.chain,
                result.wealth_flow,
                result.later_outcome,
            )
            result.assessment, result.recommendation = build_phone_assessment(
                context,
                result.pair_summary,
                result.chain,
                result.wealth_story,
                result.strengths,
            )
            result.score = build_phone_score(
                context,
                result.pair_occurrences,
                result.pair_summary,
                result.energy_distribution,
                triples,
                result.wealth_nodes,
                result.wealth_flow,
                result.later_outcome,
                occurrences,
            )
            result.verified_by_runtime = result.score is not None
            result.reading = build_reading(result)
            return result
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

    def _prepare_input(self, number: str, context: str) -> tuple[str, str]:
        """Return the customer input and the digit string analyzed by the engine."""
        if not isinstance(number, str):
            raise NumberEnergyValidationError("number input must be a string")
        input_raw = number.strip()
        if context in {
            PurposeContext.CAR_PLATE.value,
            PurposeContext.MOTORBIKE_PLATE.value,
            PurposeContext.ID_NUMBER.value,
        }:
            return input_raw, normalize_plate_input(input_raw)
        parsed = parse_number_string(input_raw)
        return parsed.input_raw, parsed.input_raw


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
