from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import json
from types import SimpleNamespace
import pytest
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from applications.api import dependencies
from applications.api.app import create_app
from applications.api.auth.password_hasher import hash_password
from applications.api.auth.roles import Role
from applications.api.auth.store import JsonUserStore, UserRecord
from applications.api.auth.usage_access import register_usage_access
from applications.api.schemas.membership import MemberRegistration, MembershipPlan
from applications.api.services.activity_service import ActivityService, ActivityError, FEATURES
from applications.api.services.auth_service import AuthService
from applications.api.services.membership_service import MembershipService

@pytest.fixture
def system(tmp_path,monkeypatch):
    monkeypatch.setenv("BTE_USAGE_DB_PATH",str(tmp_path/"activity.sqlite3"))
    monkeypatch.setenv("BTE_ANALYSIS_ARCHIVE_PATH",str(tmp_path/"analyses.sqlite3"))
    monkeypatch.setenv("BTE_MARRIAGE_DATA_PATH",str(tmp_path/"marriage.json"))
    monkeypatch.setenv("BTE_CHILDBIRTH_DATA_DIR",str(tmp_path/"childbirth"))
    monkeypatch.setenv("BTE_INTERNAL_SERVICE_SECRET","test-internal-key-not-for-real-use")
    store=JsonUserStore(tmp_path/"users.json")
    for name,role in (("operator",Role.ADMIN),("member",Role.CUSTOMER),("other",Role.CUSTOMER)):
        store.add_user(UserRecord("u-"+name,name,hash_password("test-password-123"),role,display_name=name,phone="0912345678",analysis_limit=1))
    auth=AuthService(store);monkeypatch.setattr(dependencies,"get_auth_service",lambda:auth)
    client=TestClient(create_app())
    def headers(name="member",internal=False):
        result={"Authorization":"Bearer "+auth.login(name,"test-password-123")[1].access_token}
        if internal:result["X-BTE-Service-Key"]="test-internal-key-not-for-real-use"
        return result
    return SimpleNamespace(client=client,store=store,service=ActivityService(store),auth=auth,headers=headers,tmp=tmp_path)

def output(identifier="result-1"):
    return {"status":"SUCCESS","data":{"consultation_id":identifier,"meaning":"Kết quả thử"}}

@pytest.mark.parametrize("feature",list(FEATURES))
def test_each_tool_has_its_own_cap_and_idempotent_result(system,feature):
    user=system.store.get_by_username("member");service=system.service
    ticket=service.reserve(user,feature,"op1",{"full_name":"Tên thử"})
    assert service.summary(user)[list(FEATURES).index(feature)]["pending"]==1
    service.finish(user,ticket["ticket"],output())
    service.finish(user,ticket["ticket"],output())
    item=next(row for row in service.summary(user) if row["feature"]==feature)
    assert (item["used"],item["remaining"],item["pending"])==(1,0,0)
    with pytest.raises(ActivityError,match="liên hệ ADMIN") as error:
        service.reserve(user,feature,"op2",{})
    assert error.value.status==429
    assert service.reserve(user,feature,"op1",{"full_name":"Tên thử"})["replay"] is True
    restarted=ActivityService(JsonUserStore(system.store.path))
    assert restarted.get(feature,"result-1","user:"+user.user_id)["creator_username"]=="member"
    other_feature="naming" if feature!="naming" else "marriage"
    assert next(row for row in service.summary(user) if row["feature"]==other_feature)["remaining"]==1

def test_cancel_and_failed_retry_do_not_consume_a_successful_allowance(system):
    user=system.store.get_by_username("member")
    ticket=system.service.reserve(user,"naming","op",{})
    system.service.cancel(user,ticket["ticket"])
    assert system.service.reserve(user,"naming","op",{})["replay"] is False
    with pytest.raises(ActivityError):system.service.reserve(user,"naming","op",{"changed":True})

def test_concurrent_reservations_cannot_exceed_limit(system):
    user=system.store.get_by_username("member")
    def reserve(index):
        try:return system.service.reserve(user,"naming",str(index),{})["ticket"]
        except ActivityError:return None
    with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(reserve,range(6)))
    assert sum(ticket is not None for ticket in results)==1

def test_existing_usage_is_preserved_and_legacy_consultations_are_counted_once(system,monkeypatch):
    user=system.store.get_by_username("member");user.analysis_limit=10;user.analyses_used=4
    records=[{"owner_user_id":user.user_id,"history":{"consultation_id":"old-1"},"request":{}}]
    (system.tmp/"marriage.json").write_text(json.dumps(records),encoding="utf-8")
    usage={row["feature"]:row for row in system.service.summary(user)}
    assert usage["bazi"]["used"]==4 and usage["marriage"]["used"]==1
    ticket=system.service.reserve(user,"marriage","old-replay",{})
    system.service.finish(user,ticket["ticket"],output("old-1"))
    assert next(row for row in system.service.summary(user) if row["feature"]=="marriage")["used"]==1

def test_phone_is_validated_persisted_and_does_not_rewrite_old_profiles(system):
    service=MembershipService(system.store,system.tmp/"plan.json")
    service.configure(MembershipPlan(amount_vnd=100000,validity_days=365,registration_enabled=True))
    request=MemberRegistration(username="newmember",display_name="Tên thử",phone="+84 912 345 678",password="test-password-123")
    data=service.register(request)
    assert data["user"]["phone"]=="+84912345678"
    assert JsonUserStore(system.store.path).get_by_username("newmember").phone=="+84912345678"
    with pytest.raises(ValueError):MemberRegistration(username="newperson",display_name="Tên thử",phone="not a phone",password="test-password-123")
    assert system.store.get_by_username("member").analysis_limit==1

def test_customer_directory_is_admin_only_and_contains_customer_roles(system):
    path="/api/v1/admin/registered-customers"
    assert system.client.get(path).status_code==401
    assert system.client.get(path,headers=system.headers()).status_code==403
    items=system.client.get(path,headers=system.headers("operator")).json()["items"]
    assert {item["username"] for item in items}=={"member","other"}
    assert all(item["phone"]=="0912345678" for item in items)
    assert all(len(item["usage"])==7 for item in items)
    user=system.store.get_by_username("member")
    ticket=system.service.reserve(user,"naming","op",{});system.service.finish(user,ticket["ticket"],output())
    changed=system.client.patch(path+"/member",headers=system.headers("operator"),json={"analysis_limit":31,"phone":"0987654321"})
    assert changed.status_code==200 and changed.json()["phone"]=="0987654321"
    naming=next(item for item in changed.json()["usage"] if item["feature"]=="naming")
    assert naming["used"]==1 and naming["remaining"]==30

def test_internal_allowance_protocol_requires_both_identity_and_service_key(system):
    body={"feature":"naming","operation_key":"op","input":{}}
    path="/api/v1/internal/usage/reserve"
    assert system.client.post(path,json=body,headers=system.headers()).status_code==403
    response=system.client.post(path,json=body,headers=system.headers(internal=True))
    assert response.status_code==200
    ticket=response.json()["ticket"]
    assert system.client.post(f"/api/v1/internal/usage/{ticket}/finish",headers=system.headers("other",True),json={"output":output()}).status_code==409

def test_contacts_are_archived_and_only_admin_can_read_and_mark_resolved(system):
    body={"full_name":"Khách liên hệ","phone":"0912345678","subject":"Cấp thêm lượt","message":"Tôi cần được hỗ trợ cấp thêm hạn mức.","channel":"phone"}
    result=system.client.post("/api/v1/contacts",json=body)
    assert result.status_code==201
    identifier=result.json()["id"]
    path="/api/v1/admin-archive/contact/"+identifier
    assert system.client.get(path,headers=system.headers()).status_code==403
    record=system.client.get(path,headers=system.headers("operator")).json()["row"]
    assert record["contact"]["channel"]=="website"
    changed=system.client.patch("/api/v1/admin/contacts/"+identifier,headers=system.headers("operator"),json={"status":"resolved","admin_note":"Đã gọi lại hỗ trợ"})
    assert changed.status_code==200 and changed.json()["row"]["status"]=="resolved"
    listing=system.client.get("/api/v1/admin-archive?kind=contact",headers=system.headers("operator")).json()
    assert listing["total"]==1 and listing["items"][0]["phone"]=="0912345678"

def test_main_api_reserves_before_computing_and_does_not_charge_failed_results(system):
    app=FastAPI();register_usage_access(app);calls=[]
    @app.post("/api/v1/date-selection/search")
    def compute(body:dict):
        calls.append(body)
        return JSONResponse({"success":not body.get("fail"),"data":{"id":"day-test"}},status_code=422 if body.get("fail") else 200)
    client=TestClient(app)
    assert client.post("/api/v1/date-selection/search",json={"fail":True},headers=system.headers()).status_code==422
    assert client.post("/api/v1/date-selection/search",json={},headers=system.headers()).status_code==200
    assert client.post("/api/v1/date-selection/search",json={},headers=system.headers()).status_code==429
    assert len(calls)==2

def test_consulting_calls_primary_quota_and_saves_naming_without_charging_history(system,monkeypatch):
    from consulting.archive_access import register_consulting_access
    import consulting.archive_access
    class Relay:
        def __init__(self,*args,**kwargs):pass
        async def __aenter__(self):return self
        async def __aexit__(self,*args):return False
        async def get(self,url,headers=None):return system.client.get("/api/v1/auth/me",headers=headers)
        async def post(self,url,headers=None,json=None):return system.client.post("/api/v1/"+url.split("/api/v1/",1)[1],headers=headers,json=json)
    monkeypatch.setattr(consulting.archive_access.httpx,"AsyncClient",Relay)
    app=FastAPI();calls=[]
    register_consulting_access(app,None,None)
    @app.post("/api/v1/consulting/naming/analyze")
    def compute(body:dict):calls.append(body);return output("named-1")
    @app.get("/api/v1/consulting/naming/history")
    def history():return {"items":[]}
    client=TestClient(app)
    assert client.post("/api/v1/consulting/naming/analyze",json={"surname":"Nguyễn"},headers=system.headers()).status_code==200
    assert client.get("/api/v1/consulting/naming/history",headers=system.headers()).status_code==200
    assert client.post("/api/v1/consulting/naming/analyze",json={},headers=system.headers()).status_code==429
    assert len(calls)==1
    assert system.service.get("naming","named-1")["creator_username"]=="member"

def test_releasing_stale_reservations_requires_admin_and_preserves_fresh_ones(system):
    user=system.store.get_by_username("member")
    ticket=system.service.reserve(user,"naming","held",{})
    route="/api/v1/admin/registered-customers/member/release-pending"
    assert system.client.post(route,headers=system.headers()).status_code==403
    assert system.client.post(route,headers=system.headers("operator")).json()["released"]==0
    with system.service.connect() as connection:
        connection.execute("UPDATE usage_tickets SET created_at=? WHERE id=?",((datetime.now(timezone.utc)-timedelta(minutes=31)).isoformat(),ticket["ticket"]))
    assert system.client.post(route,headers=system.headers("operator")).json()["released"]==1


def test_chart_archive_keeps_the_canonical_shape_for_existing_result_viewer(system):
    from applications.api.services.analysis_archive import save_snapshot
    user=system.store.get_by_username("member")
    save_snapshot("user:"+user.user_id,{"analysis_id":"chart-canonical","input":{"full_name":"Tên thử"},"data":{"analysis_id":"chart-canonical","canary":True}})
    ticket=system.service.reserve(user,"bazi","chart",{})
    system.service.finish(user,ticket["ticket"],{"success":True,"data":{"analysis_id":"chart-canonical","canary":True}})
    response=system.client.get("/api/v1/admin-archive/bazi/chart-canonical?owner=user:"+user.user_id,headers=system.headers("operator"))
    assert response.status_code==200 and response.json()["row"]["data"]["canary"] is True
    listing=system.client.get("/api/v1/admin-archive?kind=bazi",headers=system.headers("operator")).json()
    assert listing["total"]==1


def test_edited_quota_and_phone_roll_back_on_storage_failure(system,monkeypatch):
    from applications.api.services.user_service import UserService
    user=system.store.get_by_username("member")
    def fail():raise OSError("disk test")
    monkeypatch.setattr(system.store,"_after_change",fail)
    with pytest.raises(OSError):UserService(system.store).update_user("member",analysis_limit=31,phone="0987654321")
    assert user.analysis_limit==1 and user.phone=="0912345678"


def test_chart_usage_can_be_refunded_when_archive_write_fails(system):
    assert system.store.consume_analysis("u-member") is True
    system.store.refund_analysis("u-member")
    assert system.store.get_by_username("member").analyses_used==0
    assert JsonUserStore(system.store.path).get_by_username("member").analyses_used==0
