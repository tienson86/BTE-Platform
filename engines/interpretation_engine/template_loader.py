"""
Template Loader
===============

Chịu trách nhiệm nạp các template luận giải từ thư mục templates/.

TemplateLoader KHÔNG sinh câu.

Chỉ:
    - đọc template
    - cache template
    - trả template theo topic
"""

from __future__ import annotations

import json
from pathlib import Path


class TemplateLoader:

    def __init__(
        self,
        template_dir: str | Path,
    ):

        self.template_dir = Path(template_dir)

        self._cache: dict[str, dict] = {}

    # -------------------------------------------------

    def load(
        self,
        topic: str,
    ) -> dict:

        """
        Load template theo topic.

        Ví dụ:

            than_vuong_nhuoc.json
        """

        if topic in self._cache:

            return self._cache[topic]

        path = self.template_dir / f"{topic}.json"

        if not path.exists():

            return {}

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as f:

            data = json.load(f)

        self._cache[topic] = data

        return data

    # -------------------------------------------------

    def clear_cache(self):

        self._cache.clear()

    # -------------------------------------------------

    def exists(
        self,
        topic: str,
    ) -> bool:

        return (
            self.template_dir /
            f"{topic}.json"
        ).exists()

    # -------------------------------------------------

    def available_topics(
        self,
    ) -> list[str]:

        return sorted(

            file.stem

            for file in self.template_dir.glob("*.json")

        )
