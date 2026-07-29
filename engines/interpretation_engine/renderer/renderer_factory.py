"""
BTE Platform
Renderer Factory

Tạo Renderer theo định dạng đầu ra.
"""

from __future__ import annotations

from .markdown_renderer import MarkdownRenderer
from .html_renderer import HtmlRenderer
from .json_renderer import JsonRenderer
from .pdf_renderer import PdfRenderer
from .docx_renderer import DocxRenderer
from .excel_renderer import ExcelRenderer


class RendererFactory:
    """
    Factory tạo Renderer.
    """

    _renderers = {
        "markdown": MarkdownRenderer,
        "md": MarkdownRenderer,
        "html": HtmlRenderer,
        "json": JsonRenderer,
        "pdf": PdfRenderer,
        "docx": DocxRenderer,
        "word": DocxRenderer,
        "xlsx": ExcelRenderer,
        "excel": ExcelRenderer,
    }

    @classmethod
    def create(
        cls,
        output_format: str,
    ):
        """
        Tạo Renderer theo định dạng.
        """

        renderer_cls = cls._renderers.get(
            output_format.lower()
        )

        if renderer_cls is None:

            supported = ", ".join(
                sorted(cls._renderers.keys())
            )

            raise ValueError(
                f"Renderer '{output_format}' không được hỗ trợ. "
                f"Các định dạng hỗ trợ: {supported}"
            )

        return renderer_cls()

    @classmethod
    def register(
        cls,
        name: str,
        renderer_class,
    ) -> None:
        """
        Đăng ký Renderer mới.
        """

        cls._renderers[name.lower()] = renderer_class

    @classmethod
    def unregister(
        cls,
        name: str,
    ) -> None:
        """
        Gỡ Renderer.
        """

        cls._renderers.pop(
            name.lower(),
            None,
        )

    @classmethod
    def supported_formats(
        cls,
    ) -> list[str]:
        """
        Danh sách định dạng hỗ trợ.
        """

        return sorted(
            set(cls._renderers.keys())
        )
