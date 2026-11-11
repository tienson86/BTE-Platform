from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import pytest
from pydantic import ValidationError

from applications.api.tests.test_knowledge import system
from applications.api.schemas.courses import CourseSettings, CourseRedeem
from applications.api.services.courses import CourseService
from applications.api.services.activity_service import ActivityError
from applications.api.services.member_rewards import balance

COURSE = 'mai-hoa-nhap-mon'


def config(system, **changes):
    row=system.call('GET','/admin/courses').json()['courses'][0]
    body={key:row[key] for key in ('title','summary','price','access_days','status')}
    body.update(expected_revision=row['revision'],**changes)
    return system.call('PUT','/admin/courses/'+COURSE,body)


def fund(system, amount=100):
    svc=CourseService(system.store)
    with svc.activity.connect() as c:
        c.execute("INSERT INTO linh_ledger VALUES('test-credit','u-member',?,'test','Test',NULL,?)",(amount,datetime.now(timezone.utc).isoformat()))
    return svc


def purchase(system,key='purchase_0001',revision=None):
    if revision is None:revision=system.call('GET','/courses/'+COURSE,name='member').json()['revision']
    return system.call('POST','/courses/'+COURSE+'/redeem',{'operation_key':key,'expected_revision':revision},'member')


def test_defaults_are_closed_trial_is_readable_and_paid_content_is_hidden(system):
    data=system.call('GET','/courses',name='member').json()
    assert [(c['id'], c['status']) for c in data['courses']] == [(COURSE, 'draft'), ('kinh-dich-nhap-mon', 'published')]
    assert 'body' not in str(data)
    assert system.call('GET','/courses/'+COURSE+'/lessons/am-duong-bat-quai',name='member').status_code==200
    assert system.call('GET','/courses/'+COURSE+'/lessons/lap-que-hai-so',name='member').status_code==403
    assert system.call('GET','/courses/'+COURSE+'/lessons/video-thuc-hanh/video',name='member').status_code==403
    assert purchase(system).status_code==409


@pytest.mark.parametrize('name',['pending','expired'])
def test_inactive_members_cannot_read_trial_buy_or_mark_progress(system,name):
    for path in ['/courses','/courses/'+COURSE,'/courses/'+COURSE+'/lessons/am-duong-bat-quai']:
        assert system.call('GET',path,name=name).status_code==403
    assert system.call('POST','/courses/'+COURSE+'/redeem',{'operation_key':'test_12345','expected_revision':1},name).status_code==403
    assert system.call('PUT','/courses/'+COURSE+'/lessons/am-duong-bat-quai/progress',{'completed':True},name).status_code==403


def test_guests_and_non_admins_cannot_access_admin_settings(system):
    assert system.client.get('/api/v1/courses').status_code==401
    assert system.client.get('/api/v1/admin/courses').status_code==401
    assert system.call('GET','/admin/courses',name='member').status_code==403
    row=system.call('GET','/admin/courses').json()['courses'][0]
    body={key:row[key] for key in ('title','summary','price','access_days','status')};body['expected_revision']=1
    assert system.call('PUT','/admin/courses/'+COURSE,body,'member').status_code==403


def test_price_duration_changes_are_persisted_and_stale_edits_rejected(system):
    changed=config(system,price=17,access_days=45,status='published').json()
    assert changed['revision']==2 and changed['price']==17
    svc=CourseService(system.store)
    row=svc.catalog(system.store.get_by_username('operator'),True)['courses'][0]
    assert row['access_days']==45
    body={k:row[k] for k in ('title','summary','price','access_days','status')};body['expected_revision']=1
    assert system.call('PUT','/admin/courses/'+COURSE,body).status_code==409


def test_purchase_debits_once_preserves_snapshot_and_progress_is_private(system):
    svc=fund(system)
    assert config(system,price=20,access_days=30,status='published').status_code==200
    first=purchase(system);assert first.status_code==200
    assert first.json()['balance']==80 and first.json()['access']['price']==20
    expires=first.json()['access']['expires_at']
    assert config(system,price=90,access_days=2).status_code==200
    assert purchase(system).json()['balance']==80
    assert purchase(system,'different_0002').json()['balance']==80
    row=system.call('GET','/courses/'+COURSE,name='member').json()
    assert row['access']['expires_at']==expires and row['access']['price']==20
    assert system.call('GET','/courses/'+COURSE+'/lessons/lap-que-hai-so',name='member').status_code==200
    assert system.call('GET','/courses/'+COURSE+'/lessons/lap-que-hai-so',name='legacy').status_code==403
    assert system.call('PUT','/courses/'+COURSE+'/lessons/lap-que-hai-so/progress',{'completed':True},'member').status_code==200
    assert next(l for l in system.call('GET','/courses/'+COURSE,name='member').json()['lessons'] if l['id']=='lap-que-hai-so')['completed']
    assert not any(l['completed'] for l in system.call('GET','/courses/'+COURSE,name='legacy').json()['lessons'])
    with svc.activity.connect() as c:
        assert c.execute("SELECT COUNT(*) FROM linh_ledger WHERE kind='course_purchase'").fetchone()[0]==1


def test_insufficient_balance_and_price_revision_changes_do_not_charge(system):
    svc=fund(system,10)
    config(system,price=11,access_days=1,status='published')
    assert purchase(system).status_code==409
    config(system,price=3)
    assert purchase(system,revision=2).status_code==409
    with svc.activity.connect() as c: assert balance(c,'u-member')==10


def test_expiry_repurchase_and_old_operation_replay(system):
    svc=fund(system)
    config(system,price=10,access_days=1,status='published')
    user=system.store.get_by_username('member')
    now=datetime.now(timezone.utc)
    svc.clock=lambda:now
    body=CourseRedeem(operation_key='expire_0001',expected_revision=2)
    first=svc.redeem(user,COURSE,body)
    svc.clock=lambda:now+timedelta(days=1)
    with pytest.raises(ActivityError) as err:svc.lesson(user,COURSE,'lap-que-hai-so')
    assert err.value.status==403
    assert svc.lesson(user,COURSE,'am-duong-bat-quai')['trial']
    assert svc.redeem(user,COURSE,body)['balance']==90
    second=svc.redeem(user,COURSE,CourseRedeem(operation_key='expire_0002',expected_revision=2))
    assert second['balance']==80 and second['access']['id']!=first['access']['id']


def test_lifetime_access_survives_restart_and_pausing_does_not_revoke_existing_access(system):
    svc=fund(system)
    config(system,price=5,access_days=None,status='published')
    assert purchase(system).json()['access']['expires_at'] is None
    config(system,status='paused')
    reopened=CourseService(system.store,clock=lambda:datetime.now(timezone.utc)+timedelta(days=4000))
    assert reopened.lesson(system.store.get_by_username('member'),COURSE,'lap-que-hai-so')
    assert system.call('POST','/courses/'+COURSE+'/redeem',{'operation_key':'legacy_0001','expected_revision':3},'legacy').status_code==409


def test_parallel_redemptions_cannot_double_charge_or_overspend(system):
    svc=fund(system,20);config(system,price=20,access_days=30,status='published')
    user=system.store.get_by_username('member')
    def buy(n):return svc.redeem(user,COURSE,CourseRedeem(operation_key='parallel_'+str(n),expected_revision=2))
    with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(buy,range(6)))
    assert all(r['balance']==0 for r in results)
    with svc.activity.connect() as c:
        assert c.execute('SELECT COUNT(*) FROM courses_access').fetchone()[0]==1
        assert balance(c,user.user_id)==0


def test_video_is_authorized_and_accepts_range_requests(system):
    fund(system);config(system,price=1,access_days=30,status='published');purchase(system)
    path='/courses/'+COURSE+'/lessons/video-thuc-hanh/video'
    assert system.call('GET',path,name='legacy').status_code==403
    response=system.call('GET',path,name='member')
    assert response.status_code==200 and response.headers['content-type']=='video/mp4'
    assert len(response.content)>1000 and response.headers['cache-control']=='private, no-store'
    from applications.api import dependencies
    token=dependencies.get_auth_service().login('member','test-password-123')[1].access_token
    partial=system.client.get('/api/v1'+path,headers={'Authorization':'Bearer '+token,'Range':'bytes=0-99'})
    assert partial.status_code==206 and len(partial.content)==100


def test_course_settings_and_redemption_reject_invalid_values(system):
    row=system.call('GET','/admin/courses').json()['courses'][1]
    body={k:row[k] for k in ('title','summary','price','access_days','status')}
    body.update(status='published',expected_revision=1)
    for changes in [{'price':-1},{'price':True},{'access_days':0},{'access_days':True}]:
        with pytest.raises(ValidationError):CourseSettings(**{**body,**changes})
    assert system.call('POST','/courses/'+COURSE+'/redeem',{'operation_key':'test_12345','expected_revision':1,'price':0},'member').status_code==422


@pytest.mark.parametrize("tier", [1, 2, 3])
def test_kinh_dich_trial_and_redemption_for_each_member_tier(system, tier):
    user = system.store.get_by_username("member")
    user.membership["tier"] = tier
    path = "/courses/kinh-dich-nhap-mon"
    view = system.call("GET", path, name="member").json()
    assert view["status"] == "published" and view["price"] == 5 and view["lesson_count"] == 7
    assert system.call("GET", path + "/lessons/nhap-mon", name="member").status_code == 200
    locked = path + "/lessons/thai-va-bi"
    assert system.call("GET", locked, name="member").status_code == 403
    request = {"operation_key": "kinh_dich_test_1", "expected_revision": view["revision"]}
    assert system.call("POST", path + "/redeem", request, "member").status_code == 409
    fund(system, 10)
    for _ in range(2):
        response = system.call("POST", path + "/redeem", request, "member")
        assert response.status_code == 200 and response.json()["balance"] == 5
    assert system.call("GET", locked, name="member").status_code == 200


def test_kinh_dich_upgrades_original_placeholder_once(system):
    import json

    service = CourseService(system.store)
    placeholder = {
        "title": "Kinh Dịch nhập môn",
        "summary": "Nền tảng Dịch học, 64 quẻ và ý nghĩa hào. Nội dung đang biên soạn.",
        "price": 0, "access_days": None, "status": "draft",
    }
    with service.activity.connect() as connection:
        connection.execute("UPDATE courses_settings SET payload=? WHERE id='kinh-dich-nhap-mon'",
                           (json.dumps(placeholder, ensure_ascii=False),))
    path = "/courses/kinh-dich-nhap-mon"
    view = system.call("GET", path, name="member").json()
    assert view["status"] == "published" and view["revision"] == 2
    settings = {key: view[key] for key in ("title", "summary", "price", "access_days", "status")}
    settings.update(price=8, status="paused", expected_revision=2)
    assert system.call("PUT", "/admin" + path, settings).status_code == 200
    view = system.call("GET", path, name="member").json()
    assert (view["status"], view["price"], view["revision"]) == ("paused", 8, 3)
