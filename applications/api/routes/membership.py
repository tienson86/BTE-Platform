"""Public plan/registration, own payment notice, and admin-only approval/config."""
from functools import lru_cache
from pathlib import Path
from fastapi import APIRouter, Depends, Header

from applications.api.auth.dependencies import CurrentUser, require_role
from applications.api.auth.roles import Role
from applications.api.auth.store import UserRecord
from applications.api.dependencies import get_settings, get_user_store
from applications.api.schemas.membership import MemberRegistration, MembershipPlan, MembershipReview, PaymentReport, LinhThachRedeem, MembershipUpgrade, UpgradePaymentReport
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


@router.post("/upgrade")
def upgrade(body: MembershipUpgrade, user: CurrentUser, service: MembershipService = Depends(get_membership_service)):
    return service.request_upgrade(user, body.tier)


@router.post("/upgrade/payment-notice")
def upgrade_payment_notice(body: UpgradePaymentReport, user: CurrentUser,
                           service: MembershipService = Depends(get_membership_service)):
    return service.report_upgrade_payment(user, body.reference, body.note)


@router.post("/payment-notice")
def payment_notice(body: PaymentReport, user: CurrentUser, service: MembershipService = Depends(get_membership_service)):
    return service.report_payment(user, body.note)


@router.put("/admin/settings")
def configure(body: MembershipPlan, _admin: UserRecord = Depends(require_role(Role.ADMIN)),
              service: MembershipService = Depends(get_membership_service), if_match: str | None = Header(default=None)):
    return service.configure(body, expected_revision=if_match)


@router.get("/admin/settings")
def settings(_admin: UserRecord = Depends(require_role(Role.ADMIN)),
             service: MembershipService = Depends(get_membership_service)):
    return service.admin_settings()


@router.get("/admin/applications")
def applications(_admin: UserRecord = Depends(require_role(Role.ADMIN)),
                 service: MembershipService = Depends(get_membership_service)):
    return {"items": service.applications()}


@router.post("/admin/applications/{user_id}/review")
def review(user_id: str, body: MembershipReview, admin: UserRecord = Depends(require_role(Role.ADMIN)),
           service: MembershipService = Depends(get_membership_service)):
    return service.review(user_id, body, admin)


@router.get("/referral/{code}")
def referral_preview(code: str, service: MembershipService = Depends(get_membership_service)):
    from applications.api.services.member_rewards import find_referrer
    from applications.api.exceptions import ApplicationsAPIError
    user = find_referrer(service.store, code)
    if not user or not user.has_member_access():
        raise ApplicationsAPIError("Mã giới thiệu không hợp lệ.", status_code=404, code="referral_invalid")
    return {"code": code.upper(), "name": user.display_name or user.username, "discount_percent": 20}


@router.get("/rewards")
def rewards(user: CurrentUser, service: MembershipService = Depends(get_membership_service)):
    from applications.api.services.activity_service import ActivityService
    from applications.api.services.member_rewards import referral_code, wallet, discounted_price
    activity = ActivityService(service.store)
    return {**wallet(activity, user),
            "referral_tiers": [{"tier": tier.tier, "title": tier.title, "amount_vnd": tier.amount_vnd,
                                "discounted_amount_vnd": discounted_price(tier.amount_vnd),
                                "referral_reward": tier.referral_reward, "enabled": tier.enabled}
                               for tier in service.plan().configured_tiers()],
            "referral_base_url": service.plan().public_base_url, "referral_code": referral_code(user) if user.has_member_access() else None,
            "usage": activity.summary(user)}


@router.post("/rewards/redeem")
def redeem_reward(body: LinhThachRedeem, user: CurrentUser,
                  service: MembershipService = Depends(get_membership_service)):
    from applications.api.services.activity_service import ActivityService
    from applications.api.services.member_rewards import redeem
    return redeem(ActivityService(service.store), user, body.feature, body.operation_key)


@router.get("/wallet-balance")
def wallet_balance(user: CurrentUser, service: MembershipService = Depends(get_membership_service)):
    from fastapi.responses import JSONResponse
    from applications.api.services.activity_service import ActivityService
    from applications.api.services.member_rewards import balance, sync_referrals
    activity = ActivityService(service.store)
    sync_referrals(activity)
    with activity.connect() as connection:
        amount = balance(connection, user.user_id)
    return JSONResponse({"balance": amount}, headers={"Cache-Control": "private, no-store"})
