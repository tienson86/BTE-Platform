"""Per-engine and analyze API routes."""

from __future__ import annotations

import logging
from fastapi import APIRouter, Depends, HTTPException, Request

from applications.api.dependencies import get_orchestrator
from applications.api.routes._helpers import attach_presentation_metadata, run_birth_stage
from applications.api.schemas.common import APIResponse, BirthRequest, DiscussionRequest
from applications.api.services.knowledge_expert_service import KnowledgeExpertService
from applications.api.services.orchestrator import OrchestratorService
from engines.knowledge_engine import KnowledgePipeline

router = APIRouter(tags=["engines"])
logger = logging.getLogger(__name__)


@router.post("/calendar", response_model=APIResponse)
def calendar_endpoint(
    request: Request,
    body: BirthRequest,
    orchestrator: OrchestratorService = Depends(get_orchestrator),
) -> APIResponse:
    """Run CalendarEngine only."""
    return run_birth_stage(
        request=request,
        body=body,
        orchestrator=orchestrator,
        stage="calendar",
        message="Calendar OK",
    )


@router.post("/bazi", response_model=APIResponse)
def bazi_endpoint(
    request: Request,
    body: BirthRequest,
    orchestrator: OrchestratorService = Depends(get_orchestrator),
) -> APIResponse:
    """Run Calendar → Bazi."""
    return run_birth_stage(
        request=request,
        body=body,
        orchestrator=orchestrator,
        stage="bazi",
        message="Bazi OK",
    )


@router.post("/pattern", response_model=APIResponse)
def pattern_endpoint(
    request: Request,
    body: BirthRequest,
    orchestrator: OrchestratorService = Depends(get_orchestrator),
) -> APIResponse:
    """Run Calendar → Bazi → Pattern."""
    return run_birth_stage(
        request=request,
        body=body,
        orchestrator=orchestrator,
        stage="pattern",
        message="Pattern OK",
    )


@router.post("/score", response_model=APIResponse)
def score_endpoint(
    request: Request,
    body: BirthRequest,
    orchestrator: OrchestratorService = Depends(get_orchestrator),
) -> APIResponse:
    """Run through ScoreEngine."""
    return run_birth_stage(
        request=request,
        body=body,
        orchestrator=orchestrator,
        stage="score",
        message="Score OK",
    )


@router.post("/interpretation", response_model=APIResponse)
def interpretation_endpoint(
    request: Request,
    body: BirthRequest,
    orchestrator: OrchestratorService = Depends(get_orchestrator),
) -> APIResponse:
    """Run through InterpretationEngine."""
    return run_birth_stage(
        request=request,
        body=body,
        orchestrator=orchestrator,
        stage="interpretation",
        message="Interpretation OK",
    )


@router.post("/report", response_model=APIResponse)
def report_endpoint(
    request: Request,
    body: BirthRequest,
    orchestrator: OrchestratorService = Depends(get_orchestrator),
) -> APIResponse:
    """Run through ReportEngine."""
    return run_birth_stage(
        request=request,
        body=body,
        orchestrator=orchestrator,
        stage="report",
        message="Report OK",
    )


@router.post("/narrative", response_model=APIResponse)
def narrative_endpoint(
    request: Request,
    body: BirthRequest,
    orchestrator: OrchestratorService = Depends(get_orchestrator),
) -> APIResponse:
    """Run full pipeline through NarrativeEngine."""
    return run_birth_stage(
        request=request,
        body=body,
        orchestrator=orchestrator,
        stage="narrative",
        message="Narrative OK",
    )


@router.post("/analyze", response_model=APIResponse)
def analyze_endpoint(
    request: Request,
    body: BirthRequest,
    orchestrator: OrchestratorService = Depends(get_orchestrator),
) -> APIResponse:
    """Primary end-to-end analysis endpoint."""
    data = orchestrator.analyze(
        year=body.year,
        month=body.month,
        day=body.day,
        hour=body.hour,
        minute=body.minute,
        gender=body.gender,
        timezone=body.timezone,
    )
    payload = attach_presentation_metadata(data, body)
    # Additive Knowledge Expert status — does not alter pipeline/narrative.
    payload["knowledge_expert"] = KnowledgePipeline.portal_status()
    logger.info(
        "api.analyze response pattern_keys=%s interpretation_keys=%s section_count=%s",
        sorted((payload.get("pattern") or {}).keys()),
        sorted((payload.get("interpretation") or {}).keys()),
        (payload.get("interpretation") or {}).get("section_count", 0),
    )
    return APIResponse(
        success=True,
        message="Analyze OK",
        data=payload,
        request_id=getattr(request.state, "request_id", None),
    )


@router.post("/discussion", response_model=APIResponse)
def discussion_endpoint(
    request: Request,
    body: DiscussionRequest,
    orchestrator: OrchestratorService = Depends(get_orchestrator),
) -> APIResponse:
    """Knowledge Expert discussion endpoint (Evidence/Knowledge/Reasoning grounded)."""
    questions = list(body.questions or [])
    if body.question:
        questions = [body.question, *questions]
    if not questions:
        raise HTTPException(status_code=422, detail="question or questions is required")

    service = KnowledgeExpertService(orchestrator=orchestrator)
    if len(questions) == 1:
        data = service.discuss(
            year=body.year,
            month=body.month,
            day=body.day,
            hour=body.hour,
            minute=body.minute,
            gender=body.gender,
            timezone=body.timezone,
            question=questions[0],
            show_citations=body.show_citations,
        )
        message = "Discussion OK"
    else:
        data = service.converse(
            year=body.year,
            month=body.month,
            day=body.day,
            hour=body.hour,
            minute=body.minute,
            gender=body.gender,
            timezone=body.timezone,
            questions=questions,
            show_citations=body.show_citations,
        )
        message = "Discussion conversation OK"

    payload = attach_presentation_metadata(data, body)
    return APIResponse(
        success=True,
        message=message,
        data=payload,
        request_id=getattr(request.state, "request_id", None),
    )
