"""Canonical ReportResponse contract."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .version import SCHEMA_VERSION


class Metadata(BaseModel):
    """Response metadata contract."""

    model_config = ConfigDict(extra="forbid")

    request_id: str = Field(..., description="Correlation identifier for the request.")
    timestamp: datetime = Field(..., description="UTC timestamp when the response was produced.")
    api_version: str = Field(..., description="API contract version used to produce the response.")
    schema_version: str = Field(
        default=SCHEMA_VERSION,
        description="ReportResponse schema version.",
    )
    engine_version: str = Field(..., description="Engine version used during processing.")
    knowledge_version: str = Field(..., description="Knowledge layer version used during processing.")
    processing_time_ms: int = Field(..., description="End-to-end processing duration in milliseconds.")


class PillarInfo(BaseModel):
    """Single pillar contract."""

    model_config = ConfigDict(extra="forbid")

    stem: str | None = Field(default=None, description="Heavenly stem identifier.")
    branch: str | None = Field(default=None, description="Earthly branch identifier.")


class FourPillarsInfo(BaseModel):
    """Four pillars chart contract."""

    model_config = ConfigDict(extra="forbid")

    year: PillarInfo | None = Field(default=None, description="Year pillar.")
    month: PillarInfo | None = Field(default=None, description="Month pillar.")
    day: PillarInfo | None = Field(default=None, description="Day pillar.")
    hour: PillarInfo | None = Field(default=None, description="Hour pillar.")


class HiddenStemsInfo(BaseModel):
    """Hidden stems chart contract."""

    model_config = ConfigDict(extra="forbid")

    year: list[str] = Field(default_factory=list, description="Year pillar hidden stems.")
    month: list[str] = Field(default_factory=list, description="Month pillar hidden stems.")
    day: list[str] = Field(default_factory=list, description="Day pillar hidden stems.")
    hour: list[str] = Field(default_factory=list, description="Hour pillar hidden stems.")


class LuckCycleInfo(BaseModel):
    """Luck cycle entry contract."""

    model_config = ConfigDict(extra="forbid")

    index: int | None = Field(default=None, description="Cycle index.")
    stem: str | None = Field(default=None, description="Cycle stem identifier.")
    branch: str | None = Field(default=None, description="Cycle branch identifier.")
    start_age: int | None = Field(default=None, description="Cycle start age.")
    end_age: int | None = Field(default=None, description="Cycle end age.")


class BasicInformationInfo(BaseModel):
    """Basic chart information contract."""

    model_config = ConfigDict(extra="forbid")

    gender: str | None = Field(default=None, description="Gender identifier.")
    calendar_type: str | None = Field(default=None, description="Calendar type identifier.")
    timezone: str | None = Field(default=None, description="Timezone identifier.")
    notes: list[str] = Field(default_factory=list, description="Optional notes.")


class ChartPayload(BaseModel):
    """Chart section contract."""

    model_config = ConfigDict(extra="forbid")

    four_pillars: FourPillarsInfo = Field(..., description="Four pillars chart payload.")
    hidden_stems: HiddenStemsInfo = Field(..., description="Hidden stems payload.")
    luck_cycles: list[LuckCycleInfo] = Field(..., description="Luck cycle entries.")
    basic_information: BasicInformationInfo = Field(..., description="Basic chart information.")


class ScoreInfo(BaseModel):
    """Score analysis contract."""

    model_config = ConfigDict(extra="forbid")

    code: str | None = Field(default=None, description="Score identifier.")
    label: str | None = Field(default=None, description="Score label.")
    value: float | None = Field(default=None, description="Numeric score value.")
    summary: str | None = Field(default=None, description="Short score summary.")


class StrengthInfo(BaseModel):
    """Strength analysis contract."""

    model_config = ConfigDict(extra="forbid")

    code: str | None = Field(default=None, description="Strength identifier.")
    label: str | None = Field(default=None, description="Strength label.")
    value: float | None = Field(default=None, description="Numeric strength value.")
    summary: str | None = Field(default=None, description="Short strength summary.")


class UsefulGodInfo(BaseModel):
    """Useful god analysis contract."""

    model_config = ConfigDict(extra="forbid")

    code: str | None = Field(default=None, description="Useful god identifier.")
    label: str | None = Field(default=None, description="Useful god label.")
    elements: list[str] = Field(default_factory=list, description="Useful god elements.")
    summary: str | None = Field(default=None, description="Short useful god summary.")


class PatternInfo(BaseModel):
    """Pattern analysis contract."""

    model_config = ConfigDict(extra="forbid")

    code: str | None = Field(default=None, description="Pattern identifier.")
    label: str | None = Field(default=None, description="Pattern label.")
    summary: str | None = Field(default=None, description="Short pattern summary.")


class RelationshipInfo(BaseModel):
    """Relationship analysis contract."""

    model_config = ConfigDict(extra="forbid")

    code: str | None = Field(default=None, description="Relationship identifier.")
    label: str | None = Field(default=None, description="Relationship label.")
    summary: str | None = Field(default=None, description="Short relationship summary.")


class SummaryInfo(BaseModel):
    """Analysis summary contract."""

    model_config = ConfigDict(extra="forbid")

    code: str | None = Field(default=None, description="Summary identifier.")
    label: str | None = Field(default=None, description="Summary label.")
    text: str | None = Field(default=None, description="Summary text.")


class AnalysisPayload(BaseModel):
    """Analysis section contract."""

    model_config = ConfigDict(extra="forbid")

    scores: ScoreInfo = Field(..., description="Score analysis payload.")
    strength: StrengthInfo = Field(..., description="Strength analysis payload.")
    useful_god: UsefulGodInfo = Field(..., description="Useful god analysis payload.")
    pattern: PatternInfo = Field(..., description="Pattern analysis payload.")
    relationships: RelationshipInfo = Field(..., description="Relationship analysis payload.")
    summary: SummaryInfo = Field(..., description="Analysis summary payload.")


class SectionInfo(BaseModel):
    """Interpretation section contract."""

    model_config = ConfigDict(extra="forbid")

    id: str | None = Field(default=None, description="Section identifier.")
    title: str | None = Field(default=None, description="Section title.")
    content: str | None = Field(default=None, description="Section content.")


class SentenceInfo(BaseModel):
    """Interpretation sentence contract."""

    model_config = ConfigDict(extra="forbid")

    id: str | None = Field(default=None, description="Sentence identifier.")
    text: str = Field(..., description="Sentence text.")


class ReferenceInfo(BaseModel):
    """Interpretation reference contract."""

    model_config = ConfigDict(extra="forbid")

    id: str | None = Field(default=None, description="Reference identifier.")
    source: str | None = Field(default=None, description="Reference source.")
    locator: str | None = Field(default=None, description="Reference locator.")


class InterpretationPayload(BaseModel):
    """Interpretation section contract."""

    model_config = ConfigDict(extra="forbid")

    sections: list[SectionInfo] = Field(..., description="Interpretation section entries.")
    sentences: list[SentenceInfo] = Field(..., description="Interpretation sentence entries.")
    references: list[ReferenceInfo] = Field(..., description="Interpretation reference entries.")
    confidence: float | None = Field(
        default=None,
        description="Optional overall interpretation confidence score.",
    )


class ReportBlock(BaseModel):
    """Report content block contract."""

    model_config = ConfigDict(extra="forbid")

    id: str | None = Field(default=None, description="Block identifier.")
    type: str | None = Field(default=None, description="Block type.")
    title: str | None = Field(default=None, description="Block title.")
    content: str | None = Field(default=None, description="Block content.")


class ThemeInfo(BaseModel):
    """Report theme contract."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, description="Theme name.")
    variant: str | None = Field(default=None, description="Theme variant.")


class LayoutInfo(BaseModel):
    """Report layout contract."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, description="Layout name.")
    variant: str | None = Field(default=None, description="Layout variant.")


class RenderOptionsInfo(BaseModel):
    """Report render options contract."""

    model_config = ConfigDict(extra="forbid")

    format: str | None = Field(default=None, description="Render format.")
    locale: str | None = Field(default=None, description="Render locale.")


class ReportPayload(BaseModel):
    """Report section contract."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(..., description="Report title.")
    blocks: list[ReportBlock] = Field(..., description="Ordered report content blocks.")
    theme: ThemeInfo = Field(..., description="Report theme payload.")
    layout: LayoutInfo = Field(..., description="Report layout payload.")
    render_options: RenderOptionsInfo = Field(..., description="Render options payload.")


class WarningInfo(BaseModel):
    """Diagnostic warning contract."""

    model_config = ConfigDict(extra="forbid")

    code: str | None = Field(default=None, description="Warning code.")
    message: str = Field(..., description="Warning message.")


class ValidationInfo(BaseModel):
    """Validation diagnostic contract."""

    model_config = ConfigDict(extra="forbid")

    code: str | None = Field(default=None, description="Validation error code.")
    message: str = Field(..., description="Validation error message.")
    field: str | None = Field(default=None, description="Related field name.")


class RuntimeMessageInfo(BaseModel):
    """Runtime diagnostic message contract."""

    model_config = ConfigDict(extra="forbid")

    code: str | None = Field(default=None, description="Runtime message code.")
    message: str = Field(..., description="Runtime message text.")
    level: str | None = Field(default=None, description="Message severity level.")


class DebugInfo(BaseModel):
    """Debug diagnostic contract."""

    model_config = ConfigDict(extra="forbid")

    messages: list[str] = Field(default_factory=list, description="Debug messages.")
    context: list[str] = Field(default_factory=list, description="Debug context entries.")


class DiagnosticsPayload(BaseModel):
    """Diagnostics section contract."""

    model_config = ConfigDict(extra="forbid")

    warnings: list[WarningInfo] = Field(..., description="Non-fatal diagnostic warnings.")
    validation_errors: list[ValidationInfo] = Field(
        ...,
        description="Validation diagnostic errors.",
    )
    runtime_messages: list[RuntimeMessageInfo] = Field(
        ...,
        description="Runtime diagnostic messages.",
    )
    debug_info: DebugInfo | None = Field(
        default=None,
        description="Optional debug diagnostic payload.",
    )


class ReportResponse(BaseModel):
    """Canonical API report response."""

    model_config = ConfigDict(extra="forbid")

    success: bool = Field(default=True, description="Whether the request completed successfully.")
    metadata: Metadata = Field(..., description="Response metadata.")
    chart: ChartPayload = Field(..., description="Chart payload section.")
    analysis: AnalysisPayload = Field(..., description="Analysis payload section.")
    interpretation: InterpretationPayload = Field(
        ...,
        description="Interpretation payload section.",
    )
    report: ReportPayload = Field(..., description="Report payload section.")
    diagnostics: DiagnosticsPayload = Field(..., description="Diagnostics payload section.")
