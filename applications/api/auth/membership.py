"""Enforce paid product access before computation, archive reads, or downloads."""
from fastapi.responses import JSONResponse

_ENGINE_PATHS = {"analyze", "bazi", "pattern", "score", "interpretation", "report", "narrative", "discussion"}
_MEMBER_PREFIXES = ("/api/v1/analysis-archive", "/api/v1/export", "/api/v1/van-han",
                    "/api/v1/date-selection/search", "/api/v1/date-selection/report",
                    "/api/v1/cases", "/api/v1/customers")


def requires_membership(path: str) -> bool:
    path = path.rstrip("/")
    return (path == "/analysis" or path in {"/api/v1/" + name for name in _ENGINE_PATHS}
            or any(path == prefix or path.startswith(prefix + "/") for prefix in _MEMBER_PREFIXES))


def register_membership_access(app):
    @app.middleware("http")
    async def member_access(request, call_next):
        if request.method == "OPTIONS" or not requires_membership(request.url.path):
            return await call_next(request)
        from applications.api.dependencies import get_auth_service
        try:
            user = get_auth_service().resolve_user_from_request(request)
        except Exception:
            user = None
        if user is None:
            return JSONResponse({"detail": "Vui lòng đăng nhập để sử dụng chức năng thành viên.", "code": "unauthorized"}, status_code=401)
        if not user.has_member_access():
            return JSONResponse({"detail": "Tài khoản chưa được kích hoạt thành viên hoặc đã hết hạn. Vui lòng xem trạng thái thành viên.",
                                 "code": "membership_required", "membership_url": "/membership"}, status_code=403)
        request.state.user = user
        return await call_next(request)
