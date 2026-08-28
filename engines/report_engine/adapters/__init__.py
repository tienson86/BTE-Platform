"""Adapters bridging runtime pipeline data to ReportInputV1."""

from engines.report_engine.adapters.report_input_v1_adapter import (
    ReportInputV1Adapter,
    ReportInputV1Source,
    build_report_input_v1,
)
from engines.report_engine.adapters.commercial_presentation_adapter import (
    COMMERCIAL_PRESENTATION_EMPTY,
    CommercialPresentationAdapter,
    CommercialPresentationModel,
    CommercialPresentationSection,
)
from engines.report_engine.adapters.wp6_assembly_bridge import (
    build_report_model_from_input,
    report_input_to_interpretation_dict,
)

__all__ = [
    "COMMERCIAL_PRESENTATION_EMPTY",
    "CommercialPresentationAdapter",
    "CommercialPresentationModel",
    "CommercialPresentationSection",
    "ReportInputV1Adapter",
    "ReportInputV1Source",
    "build_report_input_v1",
    "build_report_model_from_input",
    "report_input_to_interpretation_dict",
]
