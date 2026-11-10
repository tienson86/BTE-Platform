from copy import deepcopy
from datetime import datetime, timezone
import pytest
from applications.api import dependencies
from applications.api.auth.roles import Role
from applications.api.auth.store import JsonUserStore, UserRecord
from applications.api.schemas.user import ManualMembershipGrant, AccountAction
from applications.api.services.account_admin import AccountAdminService
from applications.api.services.user_service import UserService
from applications.api.services.member_rewards import wallet
from applications.api.services.activity_service import ActivityService
from applications.api.exceptions import ApplicationsAPIError
from applications.api.tests.test_knowledge import system


@pytest.fixture
def env(system,monkeypatch):
    monkeypatch.setattr(dependencies,'get_user_service',lambda:UserService(system.store))
    return system


def row(env,name='member'):
    return env.store.get_by_username(name)


def grant(env,tier=2,name='member',**changes):
    return env.call('POST','/users/'+name+'/membership-grant',{'tier':tier,'validity_days':90,'note':'Cấp quyền thử nghiệm','expected_revision':row(env,name).account_revision,**changes})


def action(env,kind,name='member',**changes):
    return env.call('POST','/users/'+name+'/account-action/'+kind,{'expected_revision':row(env,name).account_revision,'note':'Kiểm tra quản trị',**changes})


@pytest.mark.parametrize('tier,quota',[(1,2),(2,13),(3,131)])
def test_manual_grant_has_explicit_tier_snapshot_expiry_and_no_payment_or_points(env,tier,quota):
    before=row(env).analyses_used
    response=grant(env,tier)
    assert response.status_code==200,response.text
    data=response.json();user=row(env)
    assert data['member_tier']==tier and data['membership_source']=='manual'
    assert data['analysis_limit']==quota and data['analyses_used']==before
    assert 89<(datetime.fromisoformat(data['membership_expires_at'])-datetime.now(timezone.utc)).total_seconds()/86400<=90
    assert user.membership['paid_amount_vnd']==0 and user.membership['referral_reward']==0
    assert set(user.membership['plan']['feature_limits'].values())=={quota}
    assert wallet(ActivityService(env.store),user)['balance']==0
    assert user.admin_events[-1]['actor']=='u-operator'
    restored=JsonUserStore(env.store.path).get_by_username('member')
    assert restored.membership['tier']==tier and restored.admin_events


def test_legacy_accounts_remain_unclassified_and_are_not_inferred_from_quota(env):
    data=env.call('GET','/admin/registered-customers').json()['items']
    assert next(u for u in data if u['username']=='legacy')['member_tier'] is None
    assert grant(env,3,'legacy').json()['member_tier']==3


def test_lock_invalidates_existing_session_and_grant_does_not_unlock_account(env):
    assert action(env,'lock').status_code==200
    assert env.call('GET','/auth/me',name='member').status_code==401
    assert grant(env,3).status_code==200
    assert not row(env).is_active
    assert action(env,'unlock').status_code==200
    assert env.call('GET','/auth/me',name='member').status_code==200


def test_delete_hides_account_preserves_data_and_restore_requires_explicit_unlock(env):
    grant(env)
    original=deepcopy(row(env).membership)
    assert action(env,'delete').status_code==200
    assert row(env).deleted_at and not row(env).is_active
    current=env.call('GET','/admin/registered-customers').json()['items']
    deleted=env.call('GET','/admin/registered-customers?deleted=true').json()['items']
    assert 'member' not in [u['username'] for u in current]
    assert 'member' in [u['username'] for u in deleted]
    assert env.call('GET','/auth/me',name='member').status_code==401
    assert grant(env).status_code==409
    assert env.call('PATCH','/users/member',{'is_active':True}).status_code==409
    assert action(env,'restore').status_code==200
    assert row(env).membership==original and not row(env).is_active
    assert action(env,'unlock').status_code==200
    assert row(env).has_member_access()


def test_member_cannot_grant_lock_delete_or_restore(env):
    for path,body in [('/users/legacy/membership-grant',{'tier':3,'validity_days':90,'note':'Không hợp lệ','expected_revision':1}),
                      *[('/users/legacy/account-action/'+kind,{'note':'Không hợp lệ','expected_revision':1}) for kind in ('lock','unlock','delete','restore')]]:
        assert env.call('POST',path,body,'member').status_code==403


def test_admin_cannot_lock_or_delete_self_via_either_api(env):
    assert action(env,'lock','operator').status_code==409
    assert action(env,'delete','operator').status_code==409
    assert env.call('PATCH','/users/operator',{'is_active':False}).status_code==409
    assert row(env,'operator').is_active


def test_stale_grant_and_lifecycle_requests_are_rejected(env):
    assert grant(env).status_code==200
    assert grant(env,expected_revision=1).status_code==409
    assert action(env,'delete',expected_revision=1).status_code==409
    assert not row(env).deleted_at


def test_persistence_failure_rolls_back_grant_and_delete(env,monkeypatch):
    target=row(env);original=(deepcopy(target.membership),target.account_revision,deepcopy(target.admin_events))
    def broken():raise OSError('Disk unavailable')
    monkeypatch.setattr(env.store,'_after_change',broken)
    service=AccountAdminService(env.store);admin=row(env,'operator')
    with pytest.raises(OSError):service.grant(admin,'member',ManualMembershipGrant(tier=2,validity_days=10,note='Kiểm tra lưu lỗi',expected_revision=1))
    assert (target.membership,target.account_revision,target.admin_events)==original
    with pytest.raises(OSError):service.action(admin,'member','delete',AccountAction(note='Kiểm tra lưu lỗi',expected_revision=1))
    assert not target.deleted_at and target.is_active


def test_manual_grant_is_not_a_payment_approval_and_keeps_prior_referral_obligations(env):
    target=row(env)
    target.membership['referral_events']=[{'event':'prior-referral','owner':'u-legacy','delta':10,'kind':'referral','description':'Đã duyệt trước đây','created_at':datetime.now(timezone.utc).isoformat()}]
    assert grant(env).status_code==200
    assert len(target.membership['referral_events'])==1
    assert wallet(ActivityService(env.store),row(env,'legacy'))['balance']==10
    assert wallet(ActivityService(env.store),row(env,'legacy'))['balance']==10
    svc=AccountAdminService(env.store).memberships
    assert not any(item['user']['username']=='member' for item in svc.applications())
    from applications.api.schemas.membership import MembershipReview
    with pytest.raises(ApplicationsAPIError):svc.review(target.user_id,MembershipReview(decision='refund',note='Thử hoàn tiền',expected_reference=target.membership['reference']),row(env,'operator'))


def test_edits_preserve_per_feature_limits_and_delete_restore_preserve_wallet(env):
    grant(env)
    target=row(env);target.membership['plan']['feature_limits']['naming']=99
    response=env.call('PATCH','/admin/registered-customers/member',{'phone':'0912345678','expected_revision':target.account_revision})
    assert response.status_code==200 and target.membership['plan']['feature_limits']['naming']==99
    svc=ActivityService(env.store)
    with svc.connect() as c:c.execute("INSERT INTO linh_ledger VALUES('member-test-credit','u-member',23,'test','Test',NULL,?)",(datetime.now(timezone.utc).isoformat(),))
    action(env,'delete');action(env,'restore');action(env,'unlock')
    assert wallet(svc,target)['balance']==23


def test_role_escalation_and_invalid_tiers_are_rejected(env):
    assert grant(env,tier=4).status_code==422
    assert grant(env,tier=True).status_code==422
    assert grant(env,validity_days=0).status_code==422
    assert grant(env,role='ADMIN').status_code==422
    assert row(env).role==Role.CUSTOMER
