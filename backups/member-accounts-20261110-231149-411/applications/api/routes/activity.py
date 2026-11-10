"""Customer directory, support inbox and authenticated internal allowance protocol."""
import secrets
from fastapi import APIRouter, Depends, Header, Request
from fastapi.responses import JSONResponse
from applications.api.auth.dependencies import CurrentUser, require_role
from applications.api.auth.roles import Role
from applications.api.schemas.activity import ContactRequest, ContactUpdate, ReserveRequest, FinishRequest
from applications.api.schemas.user import AdminUserUpdate
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

@router.get("/admin/registered-customers")
def customers(admin=Depends(require_role(Role.ADMIN)), q: str=""):
    service = get_activity_service()
    users = [user for user in service.store.users_by_id.values() if user.role == Role.CUSTOMER]
    needle = q.strip().casefold()
    users = [user for user in users if not needle or needle in " ".join((user.username,user.display_name,user.phone)).casefold()]
    return {"items":[{**user.to_public_dict(),"usage":service.summary(user)} for user in sorted(users,key=lambda user:user.username.casefold())]}

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
    user = users.update_user(username, **changes)
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
