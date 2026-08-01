"""Pack 02 input contract for Pack 03 Interpretation Engine.

Architecture only. Pack 02 FinalAnalysisResult is the only allowed input.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Pack02InputContract:
    """Declare that Pack 03 consumes Pack 02 final analysis output only."""

    input_type: str = "FinalAnalysisResult"
    source_pack: str = "PACK_02"
    source_model: str = "engines.analysis_engine.models.final_result.FinalResult"
    required_fields: tuple[str, ...] = (
        "id",
        "version",
        "metadata",
        "trace",
        "timestamps",
        "pipeline_id",
        "success",
    )
    optional_fields: tuple[str, ...] = (
        "analysis_result",
        "module_results",
        "scores",
        "decisions",
        "summary_codes",
    )
    forbidden_inputs: tuple[str, ...] = (
        "raw_chart_bypass",
        "pack01_direct_mutation",
        "hardcoded_sentence_payload",
    )
