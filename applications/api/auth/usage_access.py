"""Reserve before computing; commit an allowance and archive only a successful result."""
import json
from uuid import uuid4
from fastapi.responses import JSONResponse, Response
from applications.api.services.activity_service import ActivityError, get_activity_service

CHART_PATHS = {"/analysis"} | {"/api/v1/"+name for name in ("analyze","bazi","pattern","score","interpretation","report","narrative")}
PATHS = {**{path:"bazi" for path in CHART_PATHS},
         "/api/v1/date-selection/search":"date_selection", "/api/v1/van-han/analyze":"van_han"}

def failed(error):
    return JSONResponse({"detail":str(error),"message":str(error),"code":error.code,
                         "status":"FAILED","errors":[{"code":error.code,"message":str(error)}]}, status_code=error.status)

def successful(status, payload):
    return 200 <= status < 300 and isinstance(payload,dict) and payload.get("success",True) is not False and payload.get("status") not in ("FAILED","ERROR")

def register_usage_access(app):
    @app.middleware("http")
    async def usage_scope(request, call_next):
        feature = PATHS.get(request.url.path.rstrip("/")) if request.method == "POST" else None
        if request.method == "POST" and request.url.path.startswith("/api/v1/customers/") and request.url.path.rstrip("/").endswith("/analyze"):
            feature="bazi"
        if not feature:
            return await call_next(request)
        from applications.api.dependencies import get_auth_service
        user = get_auth_service().resolve_user_from_request(request)
        if user is None or not user.has_member_access():
            return await call_next(request)
        service = get_activity_service()
        try:
            inputs = await request.json() if await request.body() else {}
        except Exception:
            return await call_next(request)
        try:
            operation = request.url.path.rstrip("/")+":"+request.headers["Idempotency-Key"] if request.headers.get("Idempotency-Key") else uuid4().hex
            reservation = service.reserve(user,feature,operation,inputs,
                                          legacy=request.url.path.rstrip("/") == "/api/v1/analyze")
        except ActivityError as error:
            return failed(error)
        if reservation["replay"]:
            return JSONResponse(reservation["output"],status_code=200)
        ticket = reservation["ticket"]
        completed = False
        try:
            response = await call_next(request)
            content = b"".join([part async for part in response.body_iterator])
            try:
                payload = json.loads(content)
            except (ValueError,UnicodeError):
                payload = None
            if successful(response.status_code,payload):
                service.finish(user,ticket,payload,response.status_code)
                completed = True
            return Response(content=content,status_code=response.status_code,headers=dict(response.headers),background=response.background)
        finally:
            if not completed:
                service.cancel(user,ticket)
