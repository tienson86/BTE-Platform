"""Shared helpers for engine route handlers."""

from __future__ import annotations

from fastapi import Request

from applications.api.schemas.common import APIResponse, BirthRequest
from applications.api.services.orchestrator import OrchestratorService, Stage


def run_birth_stage(
    *,
    request: Request,
    body: BirthRequest,
    orchestrator: OrchestratorService,
    stage: Stage,
    message: str,
) -> APIResponse:
    """Orchestrate one pipeline stage and wrap the API envelope."""
    data = orchestrator.run_stage(
        stage,
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
        message=message,
        data=data,
        request_id=getattr(request.state, "request_id", None),
    )
