"""CK-01C matching runtime. Copies published signals. Does not calculate."""

from __future__ import annotations

from typing import Any, Mapping

from engines.consulting_knowledge.loader import load_consulting_knowledge_catalog
from engines.consulting_knowledge.matching import match_consulting_knowledge, project_signals
from engines.consulting_knowledge.models import ConsultingKnowledgePack


def match_published_knowledge(
    *,
    analysis_result: Mapping[str, Any] | None = None,
    identity: Mapping[str, Any] | None = None,
    integrated_narrative: Mapping[str, Any] | None = None,
) -> ConsultingKnowledgePack:
    """Match frozen catalog units to published inputs. Do not invent wording."""
    signals = project_signals(
        analysis_result=analysis_result,
        identity=identity,
        integrated_narrative=integrated_narrative,
    )
    catalog = load_consulting_knowledge_catalog()
    return match_consulting_knowledge(signals, catalog)
