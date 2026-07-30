"""Report Generator domain models."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from engines.analysis_engine.interpretation_engine.models import InterpretationResult
from engines.analysis_engine.runtime.models import (
    AnalysisResult,
    DiagnosticInfo,
    ExecutionMetadata,
)
from engines.analysis_engine.runtime.constants import CANONICAL_STAGES

SUPPORTED_FORMATS: tuple[str, ...] = ("html", "pdf", "json", "markdown")
FULL_PUBLICATION_FORMATS: tuple[str, ...] = SUPPORTED_FORMATS


@dataclass(slots=True, frozen=True)
class FormatProfile:
    """Declares requested output formats and assembly policy."""

    formats: tuple[str, ...] = FULL_PUBLICATION_FORMATS
    require_analysis_result: bool = False
    mandatory_sections: tuple[str, ...] = ("overview",)
    theme_id: str = "default"
    template_id: str = "default"
    title: str = "BTE Analysis Report"
    include_structured_data: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "formats", tuple(self.formats))
        object.__setattr__(
            self,
            "mandatory_sections",
            tuple(self.mandatory_sections),
        )
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))

    @classmethod
    def full_publication(cls, **kwargs: Any) -> FormatProfile:
        """Return the full HTML/PDF/JSON/Markdown publication profile."""
        return cls(
            formats=FULL_PUBLICATION_FORMATS,
            require_analysis_result=kwargs.pop("require_analysis_result", True),
            include_structured_data=kwargs.pop("include_structured_data", True),
            **kwargs,
        )


@dataclass(slots=True)
class ReportAssemblyContext:
    """Input contract for Report Generator.

    Upstream results are accessed only through this context.
    """

    interpretation_result: InterpretationResult
    format_profile: FormatProfile
    analysis_result: AnalysisResult | None = None
    request_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.interpretation_result is not None and not self.request_id:
            self.request_id = self.interpretation_result.request_id


@dataclass(slots=True, frozen=True)
class ReportTheme:
    """Presentation theme tokens for HTML and layout serializers."""

    theme_id: str
    name: str
    css_variables: Mapping[str, str]
    font_family: str = "Georgia, 'Times New Roman', serif"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "css_variables",
            MappingProxyType(dict(self.css_variables)),
        )
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))

    def css_block(self) -> str:
        """Render CSS custom properties block."""
        lines = [f"  {key}: {value};" for key, value in self.css_variables.items()]
        return ":root {\n" + "\n".join(lines) + "\n}"


@dataclass(slots=True, frozen=True)
class LayoutTemplate:
    """Presentation layout template (structure only, no narrative)."""

    template_id: str
    html_shell: str
    markdown_shell: str
    section_order: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "section_order", tuple(self.section_order))
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(slots=True, frozen=True)
class ReportSection:
    """Presentation section bound from InterpretationResult."""

    section_id: str
    title: str
    body: str
    order: int
    source_sentence_ids: tuple[str, ...] = ()
    source_stages: tuple[str, ...] = ()
    trace: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "trace", MappingProxyType(dict(self.trace)))


@dataclass(slots=True, frozen=True)
class StructuredDataBlock:
    """Read-only analytical data block bound from AnalysisResult."""

    block_id: str
    stage_id: str
    title: str
    payload: Mapping[str, Any]
    order: int
    trace: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload)))
        object.__setattr__(self, "trace", MappingProxyType(dict(self.trace)))


@dataclass(slots=True, frozen=True)
class ReportMetadata:
    """Report identity and version metadata."""

    report_id: str
    request_id: str
    title: str
    module_version: str
    theme_id: str
    template_id: str
    formats: tuple[str, ...]
    extras: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "formats", tuple(self.formats))
        object.__setattr__(self, "extras", MappingProxyType(dict(self.extras)))


@dataclass(slots=True, frozen=True)
class FormatHints:
    """Non-semantic format rendering hints."""

    theme_id: str
    template_id: str
    css_variables: Mapping[str, str] = field(default_factory=dict)
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "css_variables",
            MappingProxyType(dict(self.css_variables)),
        )
        object.__setattr__(self, "details", MappingProxyType(dict(self.details)))


@dataclass(slots=True, frozen=True)
class StructuredReport:
    """Canonical format-neutral assembly model."""

    metadata: ReportMetadata
    sections: tuple[ReportSection, ...]
    data_blocks: tuple[StructuredDataBlock, ...]
    format_hints: FormatHints
    source_trace: Mapping[str, Any]
    overview: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "source_trace",
            MappingProxyType(dict(self.source_trace)),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize StructuredReport for JSON and tests."""
        return {
            "metadata": {
                "report_id": self.metadata.report_id,
                "request_id": self.metadata.request_id,
                "title": self.metadata.title,
                "module_version": self.metadata.module_version,
                "theme_id": self.metadata.theme_id,
                "template_id": self.metadata.template_id,
                "formats": list(self.metadata.formats),
                "extras": dict(self.metadata.extras),
            },
            "overview": self.overview,
            "sections": [
                {
                    "section_id": section.section_id,
                    "title": section.title,
                    "body": section.body,
                    "order": section.order,
                    "source_sentence_ids": list(section.source_sentence_ids),
                    "source_stages": list(section.source_stages),
                    "trace": dict(section.trace),
                }
                for section in self.sections
            ],
            "data_blocks": [
                {
                    "block_id": block.block_id,
                    "stage_id": block.stage_id,
                    "title": block.title,
                    "payload": dict(block.payload),
                    "order": block.order,
                    "trace": dict(block.trace),
                }
                for block in self.data_blocks
            ],
            "format_hints": {
                "theme_id": self.format_hints.theme_id,
                "template_id": self.format_hints.template_id,
                "css_variables": dict(self.format_hints.css_variables),
                "details": dict(self.format_hints.details),
            },
            "source_trace": dict(self.source_trace),
        }


@dataclass(slots=True, frozen=True)
class HtmlReportArtifact:
    """HTML document output."""

    content: str
    content_type: str = "text/html; charset=utf-8"
    encoding: str = "utf-8"


@dataclass(slots=True, frozen=True)
class MarkdownReportArtifact:
    """Markdown document output."""

    content: str
    content_type: str = "text/markdown; charset=utf-8"
    encoding: str = "utf-8"


@dataclass(slots=True, frozen=True)
class JsonReportArtifact:
    """JSON-serializable report envelope."""

    content: str
    payload: Mapping[str, Any]
    content_type: str = "application/json; charset=utf-8"
    encoding: str = "utf-8"

    def __post_init__(self) -> None:
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload)))


@dataclass(slots=True, frozen=True)
class PdfReportArtifact:
    """PDF document output (bytes + optional path)."""

    content: bytes
    content_type: str = "application/pdf"
    path: str | None = None

    @property
    def size(self) -> int:
        """Return PDF byte length."""
        return len(self.content)


@dataclass(slots=True)
class ReportGeneratorResult:
    """Immutable public output of Report Generator."""

    structured_report: StructuredReport
    html: HtmlReportArtifact | None
    pdf: PdfReportArtifact | None
    json: JsonReportArtifact | None
    markdown: MarkdownReportArtifact | None
    diagnostics: tuple[DiagnosticInfo, ...]
    execution_metadata: ExecutionMetadata | None = None
    module_version: str = "1.0.0"
    summary: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "summary", MappingProxyType(dict(self.summary)))

    def to_dict(self) -> dict[str, Any]:
        """Serialize for Delivery Layer and tests."""
        return {
            "module_version": self.module_version,
            "structured_report": self.structured_report.to_dict(),
            "html": None if self.html is None else self.html.content,
            "markdown": None if self.markdown is None else self.markdown.content,
            "json": None if self.json is None else self.json.payload,
            "pdf_size": None if self.pdf is None else self.pdf.size,
            "pdf_path": None if self.pdf is None else self.pdf.path,
            "diagnostics": [
                {
                    "code": item.code,
                    "message": item.message,
                    "level": item.level,
                    "stage_id": item.stage_id,
                    "details": dict(item.details),
                }
                for item in self.diagnostics
            ],
            "summary": dict(self.summary),
        }


def default_stage_titles() -> dict[str, str]:
    """Canonical display titles for structured analytical blocks."""
    return {
        "strength": "Strength",
        "temperature": "Temperature",
        "pattern": "Pattern",
        "useful_god": "Useful God",
        "ten_gods": "Ten Gods",
        "combination": "Combination",
        "shensha": "ShenSha",
        "luck": "Luck",
        "summary": "Summary",
    }


def canonical_stage_order() -> Sequence[str]:
    """Return canonical analytical stage order for data binding."""
    return CANONICAL_STAGES


def dumps_json(payload: Mapping[str, Any]) -> str:
    """Deterministic JSON serialization."""
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2)
