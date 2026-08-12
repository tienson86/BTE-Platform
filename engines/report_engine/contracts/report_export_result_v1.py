"""Report Export V1 result contract."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

MEDIA_TYPE_PDF = "application/pdf"
MEDIA_TYPE_DOCX = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)

EXPORT_FORMAT_PDF = "pdf"
EXPORT_FORMAT_DOCX = "docx"


@dataclass(slots=True)
class ReportExportResultV1:
    """Metadata for a completed Report V1 file export."""

    format: str
    file_path: str
    file_name: str
    media_type: str
    size_bytes: int
    report_version: str
    case_id: str
    generated_at: str
    page_count: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize export metadata for API layers."""
        return dict(asdict(self))
