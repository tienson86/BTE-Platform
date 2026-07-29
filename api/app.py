"""
BTE Platform

API Application

File: api/app.py
Version: 1.0
"""

from __future__ import annotations

from fastapi import FastAPI

from api.routers.health import router as health_router
from api.routers.calendar import router as calendar_router
from api.routers.bazi import router as bazi_router
from api.routers.score import router as score_router
from api.routers.interpretation import router as interpretation_router
from api.routers.report import router as report_router
from api.routers.analysis import router as analysis_router


def create_app() -> FastAPI:
    """
    Tạo FastAPI Application.
    """

    app = FastAPI(
        title="BTE Platform API",
        description="Bazi & Feng Shui Engine Platform",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # ======================================================
    # Routers
    # ======================================================

    app.include_router(
        health_router,
        prefix="/health",
        tags=["Health"],
    )

    app.include_router(
        calendar_router,
        prefix="/calendar",
        tags=["Calendar"],
    )

    app.include_router(
        bazi_router,
        prefix="/bazi",
        tags=["Bazi"],
    )

    app.include_router(
        score_router,
        prefix="/score",
        tags=["Score"],
    )

    app.include_router(
        interpretation_router,
        prefix="/interpretation",
        tags=["Interpretation"],
    )

    app.include_router(
        report_router,
        prefix="/report",
        tags=["Report"],
    )

    app.include_router(
        analysis_router,
        prefix="/analysis",
        tags=["Analysis"],
    )

    return app


app = create_app()


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
