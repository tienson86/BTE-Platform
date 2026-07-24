"""Per-engine and analyze API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from applications.api.dependencies import get_orchestrator
from applications.api.routes._helpers import run_birth_stage
from applications.api.schemas.common import APIResponse, BirthRequest
from applications.api.services.orchestrator import OrchestratorService

router = APIRouter(tags=["engines"])


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
    return APIResponse(
        success=True,
        message="Analyze OK",
        data=data,
        request_id=getattr(request.state, "request_id", None),
    )
