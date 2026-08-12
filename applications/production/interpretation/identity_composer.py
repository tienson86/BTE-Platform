"""Identity Report feature — CDR claim plan → Commercial Language Layer."""

from __future__ import annotations

from applications.production.interpretation.contracts import (
    DomainSection,
    DomainStatus,
    ExecutiveConsultingResult,
    KnowledgeStatus,
)
from applications.production.interpretation.cross_domain.models import (
    CrossDomainReasoningResult,
)
from applications.production.language.service import CommercialLanguageService


class IdentityFeatureComposer:
    """Answer identity questions via CLL — not raw claim keys."""

    def __init__(self, language_service: CommercialLanguageService | None = None) -> None:
        self._language = language_service or CommercialLanguageService()

    def compose(
        self,
        reasoning: CrossDomainReasoningResult,
    ) -> ExecutiveConsultingResult:
        """Build Identity feature body from CDR via CLL."""
        if not reasoning.claims:
            return ExecutiveConsultingResult(
                status=DomainStatus.NOT_AVAILABLE,
                body="IDENTITY_REPORT_NOT_AVAILABLE",
                sections=[],
                recommendations=[],
                version="1.2.0",
                knowledge_status=KnowledgeStatus.PILOT,
                diagnostics={"reason": "no_claims"},
            )

        realized = self._language.compose_identity(reasoning)
        sections = [
            DomainSection(section_id=sid, title=title, paragraphs=paragraphs)
            for sid, title, paragraphs in realized.sections
        ]
        status = DomainStatus.AVAILABLE
        if reasoning.diagnostics.get("missing_domains"):
            status = DomainStatus.PARTIAL

        return ExecutiveConsultingResult(
            status=status,
            body=realized.body,
            sections=sections,
            recommendations=list(realized.recommendations)[:3],
            version="1.2.0",
            knowledge_status=KnowledgeStatus.PILOT,
            diagnostics={
                "question_context": reasoning.question_context.value,
                "primary_theme": reasoning.primary_theme,
                "conflicts": list(reasoning.conflicts),
                "tensions": list(reasoning.tensions),
                "unresolved": list(reasoning.unresolved),
                "why_primary": dict(reasoning.diagnostics.get("why_primary") or {}),
                "cll": dict(realized.diagnostics),
                "memory_line": realized.memory_line,
            },
        )
