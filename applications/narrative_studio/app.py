"""Internal Narrative Studio HTTP app.

Bind to loopback. Not mounted on the customer Portal.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Form, Query, Request
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
    def record_approval(
        case: str = Form(DEFAULT_CASE_ID),
        verdict: str = Form("REVIEW"),
        comment: str = Form(""),
        reviewer: str = Form("internal"),
    ) -> RedirectResponse:
        case_id = _safe_case(case)
        store.record(case_id=case_id, verdict=verdict, comment=comment, reviewer=reviewer)
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


app = create_app()
