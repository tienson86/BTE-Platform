"""Shared helpers for engine route handlers."""

from __future__ import annotations

from typing import Any

from fastapi import Request

from applications.api.schemas.common import APIResponse, BirthRequest
from applications.api.services.orchestrator import OrchestratorService, Stage


def customer_metadata_from_request(body: BirthRequest) -> dict[str, Any]:
    """Build presentation-only customer/chart metadata (not used by engines)."""
    meta = dict(body.metadata or {})
    return {
        "full_name": body.full_name,
        "birth_place": body.birth_place,
        "gender": body.gender,
        "timezone": body.timezone,
        "customer_id": body.customer_id,
        "metadata": meta,
    }


def attach_presentation_metadata(
    data: dict[str, Any],
    body: BirthRequest,
) -> dict[str, Any]:
    """Attach customer metadata (+ optional bat_trach echo) without mutating engines."""
    payload = dict(data)
    customer = customer_metadata_from_request(body)
    payload["customer"] = customer

    # Echo bat_trach only when the client/API already supplied it — never compute.
    bat = None
    if isinstance(customer.get("metadata"), dict):
        bat = customer["metadata"].get("bat_trach") or customer["metadata"].get(
            "batrach"
        )
    if bat is None and isinstance(body.metadata, dict):
        bat = body.metadata.get("bat_trach")
    if bat is not None and "bat_trach" not in payload:
        payload["bat_trach"] = bat
    return payload


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
        data=attach_presentation_metadata(data, body),
        request_id=getattr(request.state, "request_id", None),
    )
