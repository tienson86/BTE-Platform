"""Protected naming consultation and stateless public current-name routes."""

from __future__ import annotations

import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from consulting.naming.models import CurrentNameBirthRequest, CurrentNameRequest, NamingRequest
from consulting.naming.service import analyze_naming
from consulting.naming.current_name import analyze_current_name, analyze_current_name_birth

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


def build_public_naming_router() -> APIRouter:
    router = APIRouter(prefix="/public/naming", tags=["public-name-analysis"])

    @router.post("/analyze-current")
    def analyze_current(body: CurrentNameRequest) -> JSONResponse:
        try:
            result = analyze_current_name(body)
        except Exception:
            logger.exception("Current name analysis failed")
            return JSONResponse(status_code=503, content={
                "status": "FAILED", "data": None,
                "errors": [{"code": "NAME_ANALYSIS_UNAVAILABLE", "message": "Chưa phân tích được tên lúc này. Vui lòng thử lại sau."}],
            })
        return JSONResponse(content={"status": "SUCCESS", "data": result, "errors": []})

    @router.post("/analyze-current-birth")
    def analyze_current_birth(body: CurrentNameBirthRequest) -> JSONResponse:
        try:
            result = analyze_current_name_birth(body)
        except Exception as error:
            logger.warning("Current name birth analysis failed (%s)", type(error).__name__)
            return JSONResponse(status_code=503, content={
                "status": "FAILED", "data": None,
                "errors": [{"code": "NAME_ANALYSIS_UNAVAILABLE", "message": "Chưa phân tích được tên lúc này. Vui lòng thử lại sau."}],
            })
        return JSONResponse(
            content={"status": "SUCCESS", "data": result, "errors": []},
            headers={"Cache-Control": "private, no-store"},
        )

    return router
