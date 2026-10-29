"""Consulting services reserve and finalize allowances through the primary API only."""
import json
from uuid import uuid4
import httpx
from fastapi.responses import JSONResponse, Response
from applications.api.services.activity_service import service_key

def feature_for(path, inputs):
    path = path.rstrip("/")
    if path == "/api/v1/consulting/marriage":
        client = ((inputs.get("request_meta") or {}).get("client") or "").split(";",1)[0]
        return "business" if client == "business_consulting" else "marriage"
    return {"/api/v1/consulting/naming/analyze":"naming", "/api/v1/consulting/childbirth/analyze":"childbirth"}.get(path)

async def with_allowance(request, call_next, base, authorization, feature, inputs):
    headers={"Authorization":authorization,"X-BTE-Service-Key":service_key()}
    operation=request.headers.get("Idempotency-Key") or uuid4().hex
    async with httpx.AsyncClient(timeout=30,follow_redirects=False) as client:
        try:
            reserved=await client.post(base.rstrip("/")+"/api/v1/internal/usage/reserve",headers=headers,
                                       json={"feature":feature,"operation_key":operation,"input":inputs})
        except httpx.HTTPError:
            return JSONResponse({"detail":"Chưa kiểm tra được hạn mức. Vui lòng thử lại."},status_code=503)
        if reserved.status_code != 200:
            return JSONResponse(reserved.json(),status_code=reserved.status_code)
        reservation=reserved.json()
        if reservation["replay"]:
            return JSONResponse(reservation["output"],status_code=200)
        ticket=reservation["ticket"]
        completed=False
        try:
            response=await call_next(request)
            content=b"".join([part async for part in response.body_iterator])
            try: payload=json.loads(content)
            except (ValueError,UnicodeError): payload=None
            if 200 <= response.status_code < 300 and isinstance(payload,dict) and payload.get("status") != "FAILED" and payload.get("success",True):
                # Repeating finalization is safe if a response is lost after committing.
                for attempt in range(3):
                    try:
                        saved=await client.post(base.rstrip("/")+"/api/v1/internal/usage/"+ticket+"/finish",headers=headers,
                                                json={"output":payload,"status_code":response.status_code})
                        if saved.status_code == 200:
                            completed=True; break
                    except httpx.HTTPError:
                        pass
                if not completed:
                    # Preserve the held allowance: a computed result may already exist.
                    completed=True
                    return JSONResponse({"detail":"Kết quả đã được xử lý nhưng chưa xác nhận lưu trữ. Vui lòng liên hệ ADMIN, không gửi lại nhiều lần."},status_code=503)
            return Response(content=content,status_code=response.status_code,headers=dict(response.headers),background=response.background)
        finally:
            if not completed:
                try:
                    await client.post(base.rstrip("/")+"/api/v1/internal/usage/"+ticket+"/cancel",headers=headers,json={})
                except httpx.HTTPError:
                    pass
