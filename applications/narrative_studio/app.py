"""Internal Narrative Studio HTTP app.

Bind to loopback. Not mounted on the customer Portal.
"""

from __future__ import annotations

from pathlib import Path

from urllib.parse import parse_qs

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from applications.narrative_studio.approvals import ApprovalStore
from applications.narrative_studio.catalog import DEFAULT_CASE_ID, get_case, list_cases
from applications.narrative_studio.renderer import PANELS, render_studio
from applications.narrative_studio.service import NarrativeStudioService

STATIC_DIR = Path(__file__).resolve().parent / "static"
PANEL_IDS = {item[0] for item in PANELS}

_service = NarrativeStudioService()
_approvals = ApprovalStore()


def create_app(
    *,
    service: NarrativeStudioService | None = None,
    approvals: ApprovalStore | None = None,
) -> FastAPI:
    """Create the internal Studio application."""
    studio_service = service or _service
    store = approvals or _approvals
    app = FastAPI(
        title="BTE Narrative Studio",
        description="Internal Narrative V2 review workspace. Not customer Portal.",
        version="nimp10a.1.0",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    @app.middleware("http")
    async def _internal_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Robots-Tag"] = "noindex, nofollow"
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.get("/", include_in_schema=False)
    def root() -> RedirectResponse:
        return RedirectResponse("/studio", status_code=302)

    @app.get("/studio", response_class=HTMLResponse)
    def studio(
        case: str = Query(DEFAULT_CASE_ID),
        panel: str = Query("overview"),
        notice: str = Query(""),
    ) -> HTMLResponse:
        case_id = _safe_case(case)
        active = panel if panel in PANEL_IDS else "overview"
        review = studio_service.load(case_id)
        html = render_studio(
            cases=list_cases(),
            review=review,
            panel=active,
            approval=store.latest(case_id),
            history=store.list_for(case_id),
            notice=notice,
        )
        return HTMLResponse(html)

    @app.post("/studio/approval")
    async def record_approval(request: Request) -> RedirectResponse:
        fields = await _read_fields(request)
        case_id = _safe_case(str(fields.get("case") or DEFAULT_CASE_ID))
        store.record(
            case_id=case_id,
            verdict=str(fields.get("verdict") or "REVIEW"),
            comment=str(fields.get("comment") or ""),
            reviewer=str(fields.get("reviewer") or "internal"),
        )
        return RedirectResponse(
            f"/studio?case={case_id}&panel=approval&notice=recorded",
            status_code=303,
        )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "app": "narrative_studio", "mode": "internal_shadow"}

    return app


def _safe_case(case_id: str) -> str:
    try:
        return get_case(case_id).case_id
    except KeyError:
        return DEFAULT_CASE_ID


async def _read_fields(request: Request) -> dict[str, str]:
    """Parse JSON or urlencoded body without python-multipart."""
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        payload = await request.json()
        if isinstance(payload, dict):
            return {str(key): str(value) for key, value in payload.items()}
        return {}
    raw = (await request.body()).decode("utf-8")
    parsed = parse_qs(raw, keep_blank_values=True)
    return {key: (values[0] if values else "") for key, values in parsed.items()}


app = create_app()
