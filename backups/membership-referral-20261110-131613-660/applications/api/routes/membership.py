"""Public plan/registration, own payment notice, and admin-only approval/config."""
from functools import lru_cache
from pathlib import Path
from fastapi import APIRouter, Depends

from applications.api.auth.dependencies import CurrentUser, require_role
from applications.api.auth.roles import Role
from applications.api.auth.store import UserRecord
from applications.api.dependencies import get_settings, get_user_store
from applications.api.schemas.membership import MemberRegistration, MembershipPlan, MembershipReview, PaymentReport
from applications.api.services.membership_service import MembershipService

router = APIRouter(prefix="/membership", tags=["Membership"])


@lru_cache(maxsize=1)
def get_membership_service():
    return MembershipService(get_user_store(), Path(get_settings().data_dir) / "membership_settings.json")


@router.get("/plan")
def plan(service: MembershipService = Depends(get_membership_service)):
    return service.public_plan()


@router.post("/register", status_code=201)
def register(body: MemberRegistration, service: MembershipService = Depends(get_membership_service)):
    return service.register(body)


@router.get("/me")
def me(user: CurrentUser, service: MembershipService = Depends(get_membership_service)):
    return service.details(user)


@router.post("/payment-notice")
def payment_notice(body: PaymentReport, user: CurrentUser, service: MembershipService = Depends(get_membership_service)):
    return service.report_payment(user, body.note)


@router.put("/admin/settings")
def configure(body: MembershipPlan, _admin: UserRecord = Depends(require_role(Role.ADMIN)),
              service: MembershipService = Depends(get_membership_service)):
    return service.configure(body)


@router.get("/admin/applications")
def applications(_admin: UserRecord = Depends(require_role(Role.ADMIN)),
                 service: MembershipService = Depends(get_membership_service)):
    return {"items": service.applications()}


@router.post("/admin/applications/{user_id}/review")
def review(user_id: str, body: MembershipReview, admin: UserRecord = Depends(require_role(Role.ADMIN)),
           service: MembershipService = Depends(get_membership_service)):
    return service.review(user_id, body, admin)
