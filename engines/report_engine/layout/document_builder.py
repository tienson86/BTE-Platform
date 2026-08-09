"""Deterministic document builder. Structure only. No rendering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.report_engine.foundation_constants import CANONICAL_MODULE_ORDER
from engines.report_engine.layout.layout_context import LayoutContext

DOCUMENT_ID = "DOC-report-1"
TITLE_ID = "TTL-primary"
HEADER_ID = "HDR-primary"
FOOTER_ID = "FTR-primary"


@dataclass(slots=True)
class TitleModel:
    """Logical title identity. No typography."""

    title_id: str
    source_ref: str
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize the title model."""
        return {"title_id": self.title_id, "source_ref": self.source_ref, "status": self.status}


@dataclass(slots=True)
class HeaderModel:
    """Logical header identity. No styling."""

    header_id: str
    title_ref: str
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize the header model."""
        return {"header_id": self.header_id, "title_ref": self.title_ref, "status": self.status}


@dataclass(slots=True)
class FooterModel:
    """Logical footer identity. No page numbers."""

    footer_id: str
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize the footer model."""
        return {"footer_id": self.footer_id, "status": self.status}


@dataclass(slots=True)
class PageModel:
    """Logical page slot. No pagination rendering."""

    page_id: str
    sequence: int
    section_id: str
    header_id: str
    footer_id: str
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize the page model."""
        return {
            "page_id": self.page_id,
            "sequence": self.sequence,
            "section_id": self.section_id,
            "header_id": self.header_id,
            "footer_id": self.footer_id,
            "status": self.status,
        }


@dataclass(slots=True)
class DocumentLayout:
    """Canonical document structure. No export bytes."""

    document_id: str
    title: TitleModel
    header: HeaderModel
    footer: FooterModel
    pages: tuple[PageModel, ...]
    metadata: dict[str, Any]
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize the document layout."""
        return {
            "document_id": self.document_id,
            "title": self.title.to_dict(),
            "header": self.header.to_dict(),
            "footer": self.footer.to_dict(),
            "pages": [item.to_dict() for item in self.pages],
            "metadata": dict(self.metadata),
            "status": self.status,
        }


class DocumentBuilder:
    """Build the logical report document, pages, header, footer, and title."""

    def build(self, context: LayoutContext) -> DocumentLayout:
        """Emit one logical page per registered report module."""
        pages = tuple(
            PageModel(
                page_id=f"PAGE-{module_id}",
                sequence=index,
                section_id=f"LSEC-{module_id}",
                header_id=HEADER_ID,
                footer_id=FOOTER_ID,
                status="assembled",
            )
            for index, module_id in enumerate(CANONICAL_MODULE_ORDER)
        )
        return DocumentLayout(
            document_id=DOCUMENT_ID,
            title=TitleModel(
                title_id=TITLE_ID,
                source_ref="interpretation.canonical_interpretation",
                status="assembled",
            ),
            header=HeaderModel(header_id=HEADER_ID, title_ref=TITLE_ID, status="assembled"),
            footer=FooterModel(footer_id=FOOTER_ID, status="assembled"),
            pages=pages,
            metadata={
                "report_version": context.report_version,
                "layout_version": context.layout_version,
                "module_ids": list(CANONICAL_MODULE_ORDER),
                "rendering": False,
                "export": False,
            },
            status="assembled",
        )
