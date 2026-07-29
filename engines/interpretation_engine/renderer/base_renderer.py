"""
BTE Platform
Base Renderer

Định nghĩa giao diện chung cho tất cả Renderer.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import (
    Chapter,
)


class BaseRenderer(ABC):
    """
    Abstract Base Renderer.
    """

    name: str = "base"

    extension: str = ""

    mime_type: str = ""

    def __repr__(self) -> str:

        return (
            f"<{self.__class__.__name__}"
            f" format={self.name}>"
        )

    # =====================================================
    # Main
    # =====================================================

    @abstractmethod
    def render(
        self,
        chapters: list[Chapter],
    ):
        """
        Render dữ liệu.

        Returns
        -------
        str | dict | bytes
        """

        raise NotImplementedError

    # =====================================================
    # Metadata
    # =====================================================

    @property
    def format(self) -> str:

        return self.name

    @property
    def file_extension(self) -> str:

        return self.extension

    @property
    def content_type(self) -> str:

        return self.mime_type

    # =====================================================
    # Optional Hooks
    # =====================================================

    def before_render(
        self,
        chapters: list[Chapter],
    ) -> None:
        """
        Hook trước khi render.
        """

        return None

    def after_render(
        self,
        result,
    ):
        """
        Hook sau khi render.
        """

        return result

    # =====================================================
    # Execute
    # =====================================================

    def execute(
        self,
        chapters: list[Chapter],
    ):

        self.before_render(chapters)

        result = self.render(chapters)

        return self.after_render(result)
