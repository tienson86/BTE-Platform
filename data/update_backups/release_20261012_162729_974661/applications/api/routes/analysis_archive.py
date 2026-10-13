"""Archive shared by portal origins, isolated by authenticated account."""
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Any
from applications.api.auth.dependencies import get_auth_service
from applications.api.services.analysis_archive import save_snapshot, list_snapshots, delete_snapshots, get_snapshot

router = APIRouter(tags=["analysis archive"])

def archive_owner(request: Request) -> str:
    user = getattr(request.state, "user", None)
    if user is None and request.headers.get("authorization"):
        user = get_auth_service().resolve_user_from_request(request)
        if user is None:
            raise HTTPException(401, "Phiên đăng nhập không hợp lệ")
    if user is not None:
        return "user:" + user.user_id
    raise HTTPException(401, "Bạn cần đăng nhập để lưu và xem hồ sơ theo tài khoản")

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


# BTE_ACCOUNT_SINGLE_DELETE_V1
@router.delete("/analysis-archive/{analysis_id}")
def delete_one_history(analysis_id: str, request: Request):
    from applications.api.services.analysis_archive import _connect
    owner = archive_owner(request)
    if not owner.startswith("user:"):
        raise HTTPException(401, "Bạn cần đăng nhập để xóa hồ sơ")
    with _connect() as conn:
        deleted = conn.execute("DELETE FROM analyses WHERE owner=? AND id=?", (owner, analysis_id)).rowcount
        if not deleted:
            raise HTTPException(404, "Không tìm thấy hồ sơ trong tài khoản của bạn")
    return {"deleted": True, "analysis_id": analysis_id}


@router.get("/analysis-archive/{analysis_id}")
def get_one_history(analysis_id: str, request: Request):
    row = get_snapshot(archive_owner(request), analysis_id)
    if row is None:
        raise HTTPException(404, "Không tìm thấy hồ sơ trong tài khoản của bạn")
    return {"row": row}

from applications.api.routes.admin_archive import router as admin_archive_router
router.include_router(admin_archive_router)
