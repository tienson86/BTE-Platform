"""
JSON Renderer
"""

from __future__ import annotations

from .base_renderer import BaseRenderer

from ..models import Chapter


class JsonRenderer(BaseRenderer):

    name = "json"

    extension = ".json"

    mime_type = "application/json"

    def render(
        self,
        chapters: list[Chapter],
    ) -> dict:

        return {

            "chapters": [

                {

                    "title": chapter.title,

                    "paragraphs": [

                        {

                            "title": paragraph.title,

                            "sentences": [

                                sentence.text

                                for sentence

                                in paragraph.sentences

                            ],

                        }

                        for paragraph

                        in chapter.paragraphs

                    ],

                }

                for chapter

                in chapters

            ]

        }
