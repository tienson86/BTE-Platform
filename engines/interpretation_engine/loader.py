"""
BTE Platform
Interpretation Engine Loader

Quản lý việc nạp dữ liệu cho Interpretation Engine.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from engines.core.base_loader import BaseLoader

from .config import InterpretationConfig


class InterpretationLoader(BaseLoader):
    """
    Loader của Interpretation Engine.
    """

    def __init__(
        self,
        config: InterpretationConfig,
    ) -> None:

        super().__init__()

        self.config = config

        self.data_dir = Path(config.data_directory)

        self.template_dir = Path(
            config.template_directory
        )

        self.asset_dir = Path(
            config.asset_directory
        )

        self._cache: dict[str, Any] = {}

    # =====================================================
    # Generic
    # =====================================================

    def load(
        self,
        name: str,
    ):

        if name in self._cache:
            return self._cache[name]

        method = getattr(
            self,
            f"load_{name}",
            None,
        )

        if method is None:
            raise ValueError(
                f"Không tồn tại loader '{name}'."
            )

        data = method()

        self._cache[name] = data

        return data

    def clear_cache(self):

        self._cache.clear()

    # =====================================================
    # Load All
    # =====================================================

    def load_all(self):

        self.load_rules()

        self.load_templates()

        self.load_sentences()

        self.load_paragraphs()

        self.load_chapters()

        self.load_assets()

        self.load_styles()

    # =====================================================
    # Rules
    # =====================================================

    def load_rules(self):

        return self.load_json(
            self.data_dir
            / "rules.json"
        )

    # =====================================================
    # Templates
    # =====================================================

    def load_templates(self):

        return self.load_json(
            self.template_dir
            / "templates.json"
        )

    # =====================================================
    # Sentences
    # =====================================================

    def load_sentences(self):

        return self.load_json(
            self.template_dir
            / "sentences.json"
        )

    # =====================================================
    # Paragraphs
    # =====================================================

    def load_paragraphs(self):

        return self.load_json(
            self.template_dir
            / "paragraphs.json"
        )

    # =====================================================
    # Chapters
    # =====================================================

    def load_chapters(self):

        return self.load_json(
            self.template_dir
            / "chapters.json"
        )

    # =====================================================
    # Assets
    # =====================================================

    def load_assets(self):

        return self.load_json(
            self.asset_dir
            / "assets.json"
        )

    # =====================================================
    # Styles
    # =====================================================

    def load_styles(self):

        return self.load_json(
            self.asset_dir
            / "styles.json"
        )

    # =====================================================
    # Helpers
    # =====================================================

    def get_rule(
        self,
        code: str,
    ):

        rules = self.load_rules()

        return rules.get(code)

    def get_template(
        self,
        code: str,
    ):

        templates = self.load_templates()

        return templates.get(code)

    def get_sentence(
        self,
        code: str,
    ):

        data = self.load_sentences()

        return data.get(code)

    def get_paragraph(
        self,
        code: str,
    ):

        data = self.load_paragraphs()

        return data.get(code)

    def get_chapter(
        self,
        code: str,
    ):

        data = self.load_chapters()

        return data.get(code)

    # =====================================================
    # Cache
    # =====================================================

    @property
    def cache(self):

        return self._cache
