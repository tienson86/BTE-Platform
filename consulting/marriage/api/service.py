"""TV1-B06 public API service. Delivery only. No Decision or Narrative logic."""

from __future__ import annotations

import logging

from consulting.marriage.api.contract import MarriageApiContract
from consulting.marriage.api.parse import request_fingerprint
from consulting.marriage.api.serializers import summary_dto
from consulting.marriage.api.versions import HISTORY_DEFAULT_LIMIT, HISTORY_MAX_LIMIT
from consulting.marriage.dto.history import MarriageHistoryRecord, MarriageStoredResult
from consulting.marriage.dto.request import MarriageConsultationRequest
from consulting.marriage.dto.response import MarriageConsultationSummary, MarriageRuntimeResponse
from consulting.marriage.exceptions import MarriageConflictError, MarriageNotFoundError, MarriageValidationError
from consulting.marriage.models.enums import MarriageRuntimeStatus
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.repository.memory import InMemoryMarriageRepository
from consulting.marriage.runtime.narrative_pipeline import MarriageReportOrchestrator
from consulting.marriage.validation.runtime import MarriageRuntimeValidation

logger = logging.getLogger(__name__)


class MarriageConsultationApi(MarriageApiContract):
    """Validate, invoke B05 runtime, persist, and return stored resources."""

    def __init__(
        self,
        *,
        orchestrator: MarriageReportOrchestrator,
        repository: InMemoryMarriageRepository,
        validation: MarriageRuntimeValidation,
    ) -> None:
        self._orchestrator = orchestrator
        self._repository = repository
        self._validation = validation
        self.last_create_was_replay = False

    def create_consultation(
        self,
        request: MarriageConsultationRequest,
    ) -> MarriageRuntimeResponse:
        """POST consultation. Idempotent when a key is present."""
        self.last_create_was_replay = False
        self._validation.validate_request(request)
        key = request.request_meta.idempotency_key if request.request_meta else None
        fingerprint = request_fingerprint(request)
        if key:
            existing = self._repository.get_by_idempotency_key(key)
            if existing is not None:
                if existing.request_fingerprint != fingerprint:
                    raise MarriageConflictError("idempotency_conflict")
                self.last_create_was_replay = True
                return _runtime_from_stored(existing)
        response = self._orchestrator.run(request)
        if response.status is not MarriageRuntimeStatus.SUCCESS:
            logger.info(
                "marriage_api_create_failed",
                extra={
                    "consultation_id": response.consultation_id,
                    "stage": response.error.stage if response.error else "runtime",
                    "status": response.status.value,
                },
            )
            return response
        stored = self._persist(request, response, key, fingerprint)
        response.result = stored.result
        return response

    def get_consultation(self, consultation_id: str) -> MarriageDecisionResult:
        """Return the stored Decision Result. HTTP layer serializes the public DTO."""
        return self._require(consultation_id).result

    def get_summary(self, consultation_id: str) -> MarriageConsultationSummary:
        """Return the compact summary resource."""
        return summary_dto(self._require(consultation_id))

    def get_report(self, consultation_id: str) -> MarriageDecisionResult:
        """ABC report accessor. HTTP serializes the stored semantic report."""
        return self._require(consultation_id).result

    def list_history(self) -> list[MarriageHistoryRecord]:
        """Return stored history rows."""
        return self._repository.list_history()

    def get_stored(self, consultation_id: str) -> MarriageStoredResult:
        """Return the full stored payload for public serialization."""
        return self._require(consultation_id)

    def list_history_page(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        status: str | None = None,
        language: str | None = None,
        grade: str | None = None,
    ) -> tuple[list[MarriageHistoryRecord], str | None]:
        """Cursor-based history page."""
        size = limit if limit is not None else HISTORY_DEFAULT_LIMIT
        if size < 1 or size > HISTORY_MAX_LIMIT:
            raise MarriageValidationError("history_limit_invalid")
        return self._repository.list_history_page(
            cursor=cursor,
            limit=size,
            status=status,
            language=language,
            grade=grade,
        )

    def _require(self, consultation_id: str) -> MarriageStoredResult:
        """Load a stored consultation or fail closed."""
        stored = self._repository.get(consultation_id)
        if stored is None:
            raise MarriageNotFoundError("consultation_not_found")
        return stored

    def _persist(
        self,
        request: MarriageConsultationRequest,
        response: MarriageRuntimeResponse,
        key: str | None,
        fingerprint: str,
    ) -> MarriageStoredResult:
        """Save B05 outputs through the repository contract."""
        session = self._orchestrator.session
        if session is None or session.context.decision_result is None:
            raise MarriageValidationError("consultation_result_missing")
        result = session.context.decision_result
        label = _display_label(result.person_a.display_name, result.person_b.display_name)
        stored = MarriageStoredResult(
            history=MarriageHistoryRecord(
                consultation_id=result.consultation_id,
                person_a_analysis_id=result.person_a.analysis_id,
                person_b_analysis_id=result.person_b.analysis_id,
                score=None,
                grade=None,
                confidence=result.confidence.overall,
                versions=result.versions,
                created_at=result.created_at,
                display_label=label,
                status=response.status.value,
                overall_state=result.overall.state.value if result.overall.state else None,
                language=request.options.language if request.options else None,
            ),
            request=request,
            result=result,
            narrative=session.context.narrative,
            report_model=session.context.report_model,
            warnings=list(response.warnings),
            status=response.status,
            idempotency_key=key,
            request_fingerprint=fingerprint,
        )
        self._repository.save(stored)
        return stored


def _runtime_from_stored(stored: MarriageStoredResult) -> MarriageRuntimeResponse:
    """Replay a stored success without re-running Decision."""
    return MarriageRuntimeResponse(
        status=stored.status,
        consultation_id=stored.result.consultation_id,
        result=stored.result,
        warnings=list(stored.warnings),
    )


def _display_label(name_a: str | None, name_b: str | None) -> str:
    """Customer history identity from presentation-safe names."""
    left = name_a.strip() if name_a and name_a.strip() else "Người A"
    right = name_b.strip() if name_b and name_b.strip() else "Người B"
    return f"{left} / {right}"
