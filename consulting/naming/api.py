"""Stateless naming routes, under the existing consulting authentication."""

from __future__ import annotations

import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from consulting.naming.models import NamingRequest
from consulting.naming.service import analyze_naming

logger = logging.getLogger(__name__)


def build_naming_router() -> APIRouter:
    router = APIRouter(prefix="/consulting/naming", tags=["consulting-naming"])

    @router.post("/analyze")
    def analyze(body: NamingRequest) -> JSONResponse:
        try:
            result = analyze_naming(body)
        except Exception:
            logger.exception("Naming consultation failed")
            return JSONResponse(status_code=503, content={
                "status": "FAILED", "data": None,
                "errors": [{"code": "NAMING_UNAVAILABLE", "message": "Chưa hoàn tất phân tích đặt tên. Vui lòng thử lại sau."}],
            })
        return JSONResponse(content={"status": "SUCCESS", "data": result, "errors": []})

    return router
