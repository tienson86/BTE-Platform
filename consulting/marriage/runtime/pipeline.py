"""TV1-B02 marriage runtime pipeline. Stops after snapshots. No Decision."""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from typing import Callable

from consulting.marriage.adapters.canonical_runtime import (
    CanonicalOrchestratorAdapter,
    build_person_analysis,
)
from consulting.marriage.constants import MODULE_ID, MODULE_VERSION
from consulting.marriage.dto.request import (
    CanonicalBirthInput,
    MarriageConsultationRequest,
    NormalizedMarriageRequest,
)
from consulting.marriage.dto.response import MarriageRuntimeResponse, RuntimeError, RuntimeWarning
from consulting.marriage.exceptions import (
    MarriageCanonicalAnalysisError,
    MarriageCanonicalContractError,
    MarriageConsultingError,
    MarriageValidationError,
)
from consulting.marriage.models.enums import MarriageRuntimeStatus, PersonSide
from consulting.marriage.models.person import CanonicalVersionReference
from consulting.marriage.models.versioning import MarriageVersionBundle
from consulting.marriage.orchestrator.contract import MarriageOrchestrator
from consulting.marriage.runtime.consultation_id import generate_consultation_id
from consulting.marriage.runtime.context import MarriageRuntimeContext
from consulting.marriage.runtime.lifecycle import RuntimeLifecycleState
from consulting.marriage.runtime.normalizer import normalize_marriage_request
from consulting.marriage.runtime.phase import (
    B02_PIPELINE_STAGES,
    BUILD_PHASE_B02,
    DEFAULT_CANONICAL_TIMEZONE,
    UNBOUND_VERSION,
)
from consulting.marriage.runtime.session import MarriageRuntimeSession
from consulting.marriage.runtime.snapshot_builder import build_marriage_snapshot
from consulting.marriage.runtime.trace import StageTrace
from consulting.marriage.validation.runtime import MarriageRuntimeValidation

logger = logging.getLogger(__name__)

StageFn = Callable[[], None]


class MarriageRuntimeOrchestrator(MarriageOrchestrator):
    """Runs Canonical integration through snapshot. Later stages stay unimplemented."""

    def __init__(
        self,
        *,
        validation: MarriageRuntimeValidation,
        canonical_adapter: CanonicalOrchestratorAdapter,
    ) -> None:
        self._validation = validation
        self._canonical_adapter = canonical_adapter
        self._session: MarriageRuntimeSession | None = None
        self._pending_traces: list[StageTrace] = []

    @property
    def session(self) -> MarriageRuntimeSession | None:
        """Return the session from the last run, if any."""
        return self._session

    def run(self, request: MarriageConsultationRequest) -> MarriageRuntimeResponse:
        """Execute the TV1-B02 runtime pipeline and stop after snapshots."""
        consultation_id = generate_consultation_id()
        self._pending_traces = []
        self._session = None
        try:
            self._execute(consultation_id, request)
        except MarriageValidationError as exc:
            return self._failed(consultation_id, "request_validation", "VALIDATION_ERROR", exc)
        except MarriageCanonicalAnalysisError as exc:
            return self._failed(
                consultation_id,
                "canonical_analysis",
                "CANONICAL_ANALYSIS_ERROR",
                exc,
            )
        except MarriageCanonicalContractError as exc:
            return self._failed(
                consultation_id,
                "canonical_contract_validation",
                "CANONICAL_CONTRACT_ERROR",
                exc,
            )
        except MarriageConsultingError as exc:
            return self._failed(consultation_id, "runtime", "INTERNAL_ERROR", exc)
        session = self._session
        if session is None:
            return self._failed(
                consultation_id,
                "runtime",
                "INTERNAL_ERROR",
                MarriageConsultingError("runtime_session_missing"),
            )
        return MarriageRuntimeResponse(
            status=MarriageRuntimeStatus.SUCCESS,
            consultation_id=consultation_id,
            warnings=list(session.context.warnings),
        )

    def _execute(
        self,
        consultation_id: str,
        request: MarriageConsultationRequest,
    ) -> None:
        """Run B02 stages in order."""
        self._run_stage(
            consultation_id,
            None,
            B02_PIPELINE_STAGES[0],
            lambda: self._validation.validate_request(request),
        )
        normalized_holder: dict[str, NormalizedMarriageRequest] = {}

        def normalize() -> None:
            normalized_holder["request"] = normalize_marriage_request(request)

        self._run_stage(consultation_id, None, B02_PIPELINE_STAGES[1], normalize)
        normalized = normalized_holder["request"]
        session = self._create_session(consultation_id, normalized)
        self._session = session
        for trace in self._pending_traces:
            session.add_trace(trace)
        self._pending_traces = []
        session.transition(RuntimeLifecycleState.VALIDATED)
        analysis_a_id = f"{consultation_id}-A"
        analysis_b_id = f"{consultation_id}-B"
        self._warn_input_limits(session, normalized.person_a, "A")
        self._warn_input_limits(session, normalized.person_b, "B")
        analysis_a = {"analysis_id": analysis_a_id}
        analysis_b = {"analysis_id": analysis_b_id}

        def run_a() -> None:
            result = build_person_analysis(
                self._canonical_adapter,
                normalized.person_a,
                analysis_id=analysis_a_id,
                side=PersonSide.A,
            )
            analysis_a.update(result)
            session.context.analysis_a = dict(analysis_a)

        def run_b() -> None:
            result = build_person_analysis(
                self._canonical_adapter,
                normalized.person_b,
                analysis_id=analysis_b_id,
                side=PersonSide.B,
            )
            analysis_b.update(result)
            session.context.analysis_b = dict(analysis_b)

        self._run_stage(consultation_id, session, B02_PIPELINE_STAGES[2], run_a)
        self._run_stage(consultation_id, session, B02_PIPELINE_STAGES[3], run_b)
        self._run_stage(
            consultation_id,
            session,
            B02_PIPELINE_STAGES[4],
            lambda: self._validation.validate_canonical_contract(analysis_a, analysis_b),
        )
        session.transition(RuntimeLifecycleState.CANONICAL_READY)

        def build_snapshots() -> None:
            session.context.snapshot_a = build_marriage_snapshot(
                analysis=analysis_a,
                person=normalized.person_a,
                analysis_id=analysis_a_id,
                side=PersonSide.A,
            )
            session.context.snapshot_b = build_marriage_snapshot(
                analysis=analysis_b,
                person=normalized.person_b,
                analysis_id=analysis_b_id,
                side=PersonSide.B,
            )

        self._run_stage(consultation_id, session, B02_PIPELINE_STAGES[5], build_snapshots)
        session.transition(RuntimeLifecycleState.SNAPSHOT_READY)
        self._after_snapshots(session)

    def _after_snapshots(self, session: MarriageRuntimeSession) -> None:
        """B02 stop. Later phases continue from snapshot-ready through this seam."""
        session.transition(RuntimeLifecycleState.COMPLETED)

    def _create_session(
        self,
        consultation_id: str,
        request: NormalizedMarriageRequest,
    ) -> MarriageRuntimeSession:
        """Create a CREATED runtime session after normalization."""
        context = MarriageRuntimeContext(
            consultation_id=consultation_id,
            request=request,
            versions=MarriageVersionBundle(
                module_version=MODULE_VERSION,
                decision_profile_version=UNBOUND_VERSION,
                score_model_version=UNBOUND_VERSION,
                rule_catalog_version=UNBOUND_VERSION,
                canonical_versions=CanonicalVersionReference(),
                narrative_version=UNBOUND_VERSION,
            ),
        )
        return MarriageRuntimeSession(
            context=context,
            lifecycle_state=RuntimeLifecycleState.CREATED,
        )

    def _warn_input_limits(
        self,
        session: MarriageRuntimeSession,
        person: CanonicalBirthInput,
        side: str,
    ) -> None:
        """Record input limitations. Does not invent missing values."""
        if person.birth_time is None:
            session.add_warning(
                RuntimeWarning(
                    code="BIRTH_TIME_UNKNOWN",
                    stage="birth_input_normalization",
                    message_key="birth_time_unknown",
                    affected_domain=side,
                )
            )
        if person.timezone is None:
            session.add_warning(
                RuntimeWarning(
                    code="TIMEZONE_UNSPECIFIED",
                    stage="birth_input_normalization",
                    message_key="timezone_unspecified",
                    technical_detail=DEFAULT_CANONICAL_TIMEZONE,
                    affected_domain=side,
                )
            )

    def _run_stage(
        self,
        consultation_id: str,
        session: MarriageRuntimeSession | None,
        stage: str,
        action: StageFn,
    ) -> None:
        """Run one stage with timing, logging, and tracing."""
        started = time.perf_counter()
        start_time = _utc_now()
        logger.info(
            "marriage_stage_start",
            extra={
                "consultation_id": consultation_id,
                "stage": stage,
                "status": "STARTED",
                "module_id": MODULE_ID,
                "build_phase": BUILD_PHASE_B02,
            },
        )
        try:
            action()
        except Exception:
            duration_ms = (time.perf_counter() - started) * 1000.0
            end_time = _utc_now()
            self._record_trace(
                session,
                StageTrace(
                    stage=stage,
                    start_time=start_time,
                    end_time=end_time,
                    duration_ms=duration_ms,
                    status="FAILED",
                ),
            )
            logger.info(
                "marriage_stage_end",
                extra={
                    "consultation_id": consultation_id,
                    "stage": stage,
                    "status": "FAILED",
                    "duration": duration_ms,
                },
            )
            raise
        duration_ms = (time.perf_counter() - started) * 1000.0
        end_time = _utc_now()
        self._record_trace(
            session,
            StageTrace(
                stage=stage,
                start_time=start_time,
                end_time=end_time,
                duration_ms=duration_ms,
                status="SUCCESS",
            ),
        )
        logger.info(
            "marriage_stage_end",
            extra={
                "consultation_id": consultation_id,
                "stage": stage,
                "status": "SUCCESS",
                "duration": duration_ms,
            },
        )

    def _record_trace(
        self,
        session: MarriageRuntimeSession | None,
        trace: StageTrace,
    ) -> None:
        """Store a stage trace on the session or until the session exists."""
        if session is not None:
            session.add_trace(trace)
            return
        self._pending_traces.append(trace)

    def _failed(
        self,
        consultation_id: str,
        stage: str,
        code: str,
        exc: BaseException,
    ) -> MarriageRuntimeResponse:
        """Build a FAILED envelope. Does not expose stack traces."""
        error = RuntimeError(
            code=code,
            stage=stage,
            retryable=False,
            technical_detail=str(exc),
        )
        if self._session is not None:
            self._session.errors.append(error)
        return MarriageRuntimeResponse(
            status=MarriageRuntimeStatus.FAILED,
            consultation_id=consultation_id,
            warnings=list(self._session.context.warnings) if self._session else [],
            error=error,
        )


def _utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()
