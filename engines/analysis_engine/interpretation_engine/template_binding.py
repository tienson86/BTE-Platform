"""Template Binding — attach template text to selected sentences."""

from __future__ import annotations

from engines.analysis_engine.interpretation_engine.exceptions import (
    InterpretationBindingError,
    InterpretationKnowledgeError,
)
from engines.analysis_engine.interpretation_engine.knowledge_access import (
    ASSET_TEMPLATES,
    KnowledgeSession,
)
from engines.analysis_engine.interpretation_engine.models import (
    BoundTemplate,
    SelectedSentence,
)


class TemplateBinder:
    """Bind selected sentences to template texts from knowledge."""

    def bind(
        self,
        selected: tuple[SelectedSentence, ...],
        *,
        session: KnowledgeSession,
    ) -> tuple[BoundTemplate, ...]:
        """Resolve template_id for each selected sentence."""
        templates = dict(session.get_asset(ASSET_TEMPLATES).data.get("templates") or {})
        if not templates:
            raise InterpretationKnowledgeError(
                "interpretation.templates has no templates",
            )

        bound: list[BoundTemplate] = []
        for item in selected:
            text = templates.get(item.template_id)
            if text is None or not str(text).strip():
                raise InterpretationBindingError(
                    f"Template not found: {item.template_id}",
                    details={
                        "template_id": item.template_id,
                        "sentence_id": item.sentence_id,
                    },
                )
            bound.append(
                BoundTemplate(
                    sentence_id=item.sentence_id,
                    section_id=item.section_id,
                    source_stage=item.source_stage,
                    template_id=item.template_id,
                    template_text=str(text),
                    priority=item.priority,
                    placeholders=item.placeholders,
                    required_placeholders=item.required_placeholders,
                    metadata=dict(item.metadata),
                )
            )
        return tuple(bound)
