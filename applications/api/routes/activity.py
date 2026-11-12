"""Customer directory, support inbox and authenticated internal allowance protocol."""
from datetime import datetime, timedelta, timezone
import secrets
import unicodedata
from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, Response
from fastapi.responses import JSONResponse
from applications.api.auth.dependencies import CurrentUser, require_role
from applications.api.auth.roles import Role
from applications.api.schemas.activity import ContactRequest, ContactUpdate, ReserveRequest, FinishRequest
from applications.api.schemas.user import AdminUserUpdate
from applications.api.services.member_directory import member_history, member_list_activity, membership_source, setup_member_catalog
from applications.api.services.activity_service import ActivityError, get_activity_service, service_key

router = APIRouter(tags=["Customer activity"])

def internal_key(x_bte_service_key: str = Header(default="")):
    from fastapi import HTTPException
    if not secrets.compare_digest(x_bte_service_key, service_key()):
        raise HTTPException(403,"Lời gọi dịch vụ không hợp lệ.")

def register_activity_errors(app):
    @app.exception_handler(ActivityError)
    async def handle(request, error):
        return JSONResponse({"detail":str(error),"message":str(error),"code":error.code,"status":"FAILED",
                             "errors":[{"code":error.code,"message":str(error)}]},status_code=error.status)

@router.get("/usage")
def usage(user: CurrentUser):
    return {"items":get_activity_service().summary(user)}

@router.post("/internal/usage/reserve", dependencies=[Depends(internal_key)])
def reserve(body: ReserveRequest, user: CurrentUser):
    return get_activity_service().reserve(user,body.feature,body.operation_key,body.input)

@router.post("/internal/usage/{ticket}/finish", dependencies=[Depends(internal_key)])
def finish(ticket: str, body: FinishRequest, user: CurrentUser):
    return get_activity_service().finish(user,ticket,body.output,body.status_code)

@router.post("/internal/usage/{ticket}/cancel", dependencies=[Depends(internal_key)])
def cancel(ticket: str, user: CurrentUser):
    get_activity_service().cancel(user,ticket)
    return {"cancelled":True}

def _search_key(value):
    return "".join(char for char in unicodedata.normalize("NFD", value.casefold())
                   if unicodedata.category(char) != "Mn").replace("đ", "d")


@router.get("/admin/registered-customers")
def customers(response: Response, admin=Depends(require_role(Role.ADMIN)), q: str="", deleted: bool=False,
              page: int | None = Query(None, ge=1), tier: str = "", status: str = "",
              expiring: bool = False, pending: bool = False):
    response.headers["Cache-Control"] = "no-store"
    service = get_activity_service()
    with service.store._lock:
        users = [user for user in service.store.users_by_id.values()
                 if user.role == Role.CUSTOMER and bool(user.deleted_at) == deleted]
    needle = _search_key(q.strip())
    users = [user for user in users if not needle or needle in _search_key(
        " ".join((user.username, user.display_name, user.phone)))]
    users.sort(key=lambda user: (user.username.casefold(), user.user_id))
    if page is None:
        return {"items": [{**user.to_public_dict(), "usage": service.summary(user)} for user in users]}

    now = datetime.now(timezone.utc)
    profiles = []
    for user in users:
        profile = user.to_public_dict()
        member_status = profile["membership_status"]
        if not user.is_active:
            member_status = "locked"
        elif member_status == "active" and not profile["member_access"]:
            member_status = "expired"
        if status and status != member_status:
            continue
        if tier and tier != str(profile["member_tier"] or "none"):
            continue
        if expiring:
            try:
                expires = datetime.fromisoformat(profile["membership_expires_at"])
            except (TypeError, ValueError):
                continue
            if member_status != "active" or expires.tzinfo is None or not now < expires <= now + timedelta(days=30):
                continue
        profile["source_label"] = membership_source(user.membership or {})
        profiles.append(profile)

    with service.connect() as connection:
        setup_member_catalog(connection)
        if pending:
            owners = {row[0] for row in connection.execute(
                "SELECT DISTINCT owner FROM member_submissions WHERE status='pending'")}
            owners.update(user.user_id for user in users
                          if (user.membership or {}).get("status") == "pending"
                          or ((user.membership or {}).get("upgrade_order") or {}).get("status") == "pending")
            profiles = [row for row in profiles if row["user_id"] in owners]
        total = len(profiles)
        page = min(page, max(1, (total + 24) // 25))
        items = profiles[(page - 1) * 25:page * 25]
        for item in items:
            item.update(member_list_activity(connection, item["user_id"]))
    return {"items": items, "total": total, "page": page, "page_size": 25}


def _member_target(service, user_id):
    user = service.store.get_by_id(user_id)
    if not user or user.role != Role.CUSTOMER:
        raise HTTPException(404, "Không tìm thấy thành viên.")
    return user


@router.get("/admin/registered-customers/{user_id}/history")
def customer_history(user_id: str, response: Response, admin=Depends(require_role(Role.ADMIN)),
                     section: str = "membership", page: int = Query(1, ge=1, le=100000)):
    response.headers["Cache-Control"] = "no-store"
    service = get_activity_service()
    user = _member_target(service, user_id)
    return member_history(service, user, section, page)


@router.get("/admin/registered-customers/{user_id}/usage")
def customer_usage(user_id: str, response: Response, admin=Depends(require_role(Role.ADMIN))):
    response.headers["Cache-Control"] = "no-store"
    service = get_activity_service()
    return {"items": service.summary(_member_target(service, user_id))}


@router.patch("/admin/registered-customers/{username}")
def update_customer(username: str, body: AdminUserUpdate, admin=Depends(require_role(Role.ADMIN))):
    from applications.api.services.user_service import UserService
    from fastapi import HTTPException
    service = get_activity_service(); users = UserService(service.store)
    user = users.get_by_username(username)
    if user.role != Role.CUSTOMER:
        raise HTTPException(404,"Không tìm thấy khách hàng.")
    changes = body.model_dump(exclude_unset=True)
    # The customer directory adjusts the shared allowance without erasing past usage.
    changes.pop("analyses_used", None)
    user = users.update_user(username, actor=admin, **changes)
    return {**user.to_public_dict(),"usage":service.summary(user)}

@router.post("/admin/registered-customers/{username}/release-pending")
def release_pending(username: str, admin=Depends(require_role(Role.ADMIN))):
    from applications.api.services.user_service import UserService
    service=get_activity_service()
    user=UserService(service.store).get_by_username(username)
    return {"released":service.release_stale(user)}

@router.post("/contacts", status_code=201)
def contact(body: ContactRequest, request: Request):
    from applications.api.dependencies import get_auth_service
    actor = get_auth_service().resolve_user_from_request(request)
    if actor is None or actor.role != Role.ADMIN:
        body = body.model_copy(update={"channel":"website"})
    return get_activity_service().contact(body,actor)

@router.patch("/admin/contacts/{identifier}")
def update_contact(identifier: str, body: ContactUpdate, admin=Depends(require_role(Role.ADMIN))):
    return {"row":get_activity_service().update_contact(identifier,body.status,body.admin_note)}
