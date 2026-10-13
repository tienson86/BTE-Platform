"""Archive shared by portal origins, isolated by authenticated account."""
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Any
from applications.api.auth.dependencies import get_auth_service
from applications.api.services.analysis_archive import save_snapshot, list_snapshots, delete_snapshots

router = APIRouter(tags=["analysis archive"])

def archive_owner(request: Request) -> str:
    user = getattr(request.state, "user", None)
    if user is None and request.headers.get("authorization"):
        user = get_auth_service().resolve_user_from_request(request)
        if user is None:
            raise HTTPException(401, "Phiên đăng nhập không hợp lệ")
    if user is not None:
        return "user:" + user.user_id
    if request.client and request.client.host in ("127.0.0.1", "::1", "localhost", "testclient"):
        return "local-guest"
    raise HTTPException(401, "Cần đăng nhập để lưu hồ sơ")

class SnapshotRequest(BaseModel):
    rows: list[dict[str, Any]]

@router.get("/analysis-archive")
def history(request: Request):
    return {"rows": list_snapshots(archive_owner(request))}

@router.post("/analysis-archive")
def import_history(request: Request, body: SnapshotRequest):
    owner = archive_owner(request)
    for row in body.rows:
        try:
            save_snapshot(owner, row)
        except ValueError as error:
            raise HTTPException(422, str(error)) from error
    return {"saved": len(body.rows)}

@router.delete("/analysis-archive")
def clear_history(request: Request):
    delete_snapshots(archive_owner(request))
    return {"cleared": True}
