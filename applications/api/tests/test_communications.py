from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
import json
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from applications.api import dependencies
from applications.api.app import create_app
from applications.api.auth.password_hasher import hash_password
from applications.api.auth.roles import Role
from applications.api.auth.store import JsonUserStore, UserRecord
from applications.api.services.auth_service import AuthService
from applications.api.services.communications import CommunicationsService
from applications.api.schemas.communications import ThreadInput, TopicInput


@pytest.fixture
def system(tmp_path, monkeypatch):
    for name, leaf in (("BTE_USAGE_DB_PATH","activity.sqlite3"),("BTE_COMMUNICATIONS_DB_PATH","communications.sqlite3"),
                       ("BTE_ANALYSIS_ARCHIVE_PATH","analyses.sqlite3"),("BTE_MARRIAGE_DATA_PATH","marriage.json"),
                       ("BTE_CHILDBIRTH_DATA_DIR","childbirth")):
        monkeypatch.setenv(name,str(tmp_path/leaf))
    store=JsonUserStore(tmp_path/"users.json")
    password=hash_password("test-password-123")
    for name in ("operator","member","other","pending","expired","legacy"):
        membership=None
        if name not in ("operator","legacy"):
            membership={"status":"pending" if name=="pending" else "active",
                        "expires_at":(datetime.now(timezone.utc)+timedelta(days=-1 if name=="expired" else 30)).isoformat()}
        store.add_user(UserRecord("u-"+name,name,password,Role.ADMIN if name=="operator" else Role.CUSTOMER,
            display_name=name,phone="0912345678",analysis_limit=31,analyses_used=3,membership=membership))
    auth=AuthService(store)
    monkeypatch.setattr(dependencies,"get_auth_service",lambda:auth)
    client=TestClient(create_app())
    headers={name:{"Authorization":"Bearer "+auth.login(name,"test-password-123")[1].access_token} for name in ("operator","member","other","pending","expired","legacy")}
    def call(method,path,body=None,name="member"):
        return client.request(method,"/api/v1"+path,headers=headers[name],**({"json":body} if body is not None else {}))
    return SimpleNamespace(client=client,store=store,service=CommunicationsService(store),call=call,tmp=tmp_path)


def thread(system,name="member",**kwargs):
    data={"subject":"Hỏi Admin","message":"Cần hỗ trợ",**kwargs}
    response=system.call("POST","/communications/threads",data,name)
    assert response.status_code==201,response.text
    return response.json()["thread"]


def topic(system,name="member",approved=False):
    response=system.call("POST","/community/topics",{"title":"Câu hỏi Bát Tự","body":"Xin trao đổi về cách đọc lá số."},name)
    assert response.status_code==201,response.text
    result=response.json()["topic"]
    if approved:
        result=system.call("POST",f"/community/topics/{result['id']}/moderate",{"decision":"approve","expected_revision":result["revision"]},"operator").json()["topic"]
    return result


@pytest.mark.parametrize("path",["/communications/summary","/communications/threads","/communications/recipients","/community/topics"])
def test_guests_cannot_read_member_data(system,path):
    assert system.client.get("/api/v1"+path).status_code==401


@pytest.mark.parametrize("name",["pending","expired"])
def test_support_available_but_forum_requires_membership(system,name):
    assert thread(system,name)["owner"]["username"]==name
    assert system.call("GET","/community/topics",name=name).status_code==403
    assert system.call("POST","/community/topics",{"title":"Question","body":"Body"},name).status_code==403
    assert system.call("GET","/communications/summary",name=name).json()["can_community"] is False


def test_legacy_granted_members_keep_forum_access(system):
    assert system.call("GET","/community/topics",name="legacy").status_code==200


def test_private_threads_cannot_be_read_written_or_marked_by_another_member(system):
    item=thread(system);identifier=item["id"]
    for method,path,body in (("GET",f"/communications/threads/{identifier}/messages",None),
                             ("POST",f"/communications/threads/{identifier}/messages",{"message":"Forged"}),
                             ("POST",f"/communications/threads/{identifier}/read",{"last_message_id":999})):
        assert system.call(method,path,body,"other").status_code==404
    assert system.call("GET","/communications/threads",name="other").json()["total"]==0
    assert system.call("GET","/communications/recipients").status_code==403
    assert system.call("POST","/communications/threads",{"subject":"X","message":"X","recipient_user_id":"u-other"}).status_code==403
    assert system.call("GET",f"/communications/threads/{identifier}/messages",name="operator").status_code==200


def test_admin_can_start_and_reply_with_durable_read_history(system):
    item=thread(system,"operator",recipient_user_id="u-member")
    identifier=item["id"];base=f"/communications/threads/{identifier}"
    assert system.call("GET","/communications/summary").json()["unread_messages"]==1
    assert system.call("GET","/communications/summary",name="other").json()["unread_messages"]==0
    own=system.call("POST",base+"/messages",{"message":"Cảm ơn Admin"}).json()["message"]
    assert system.call("GET","/communications/summary",name="operator").json()["unread_messages"]==1
    assert system.call("POST",base+"/read",{"last_message_id":own["id"]}).status_code==200
    system.call("POST",base+"/read",{"last_message_id":0})
    assert system.call("GET","/communications/summary").json()["unread_messages"]==0
    reply=system.call("POST",base+"/messages",{"message":"Admin đã ghi nhận"},"operator").json()["message"]
    fresh=CommunicationsService(JsonUserStore(system.store.path))
    history=fresh.thread_messages(system.store.get_by_username("member"),identifier)
    assert [row["body"] for row in history["messages"]]==["Cần hỗ trợ","Cảm ơn Admin","Admin đã ghi nhận"]
    assert history["thread"]["unread"]==1 and reply["sender_is_admin"]==1
    assert system.call("GET","/communications/recipients",name="operator").status_code==200


def test_message_pagination_and_nonce_retries(system):
    item=thread(system,client_key="same-thread-123456")
    assert thread(system,client_key="same-thread-123456")["id"]==item["id"]
    base=f"/communications/threads/{item['id']}/messages"
    for number in range(5):
        payload={"message":str(number),"client_key":"message-key-123456-"+str(number)}
        assert system.call("POST",base,payload).json()==system.call("POST",base,payload).json()
    recent=system.call("GET",base+"?limit=3").json()
    older=system.call("GET",base+f"?limit=3&before={recent['before']}").json()
    assert [row["body"] for row in older["messages"]+recent["messages"]]==["Cần hỗ trợ","0","1","2","3","4"]
    assert recent["has_more"] and not older["has_more"]
    assert system.call("POST",base,{"message":"Changed","client_key":"message-key-123456-0"}).status_code==409


def test_contact_import_uses_verified_owner_never_private_notes_or_phone_matching(system):
    payload={"full_name":"Thành viên thử","phone":"0912345678","subject":"Liên hệ cũ","message":"Tin gốc của khách"}
    contact=system.call("POST","/contacts",payload).json()["id"]
    guest=system.client.post("/api/v1/contacts",json=payload).json()["id"]
    manual=system.call("POST","/contacts",{**payload,"channel":"phone"},"operator").json()["id"]
    system.call("PATCH","/admin/contacts/"+contact,{"status":"handling","admin_note":"SECRET-NOTE-DO-NOT-EXPOSE"},"operator")
    listing=system.call("GET","/communications/threads").json()
    assert listing["total"]==1 and listing["items"][0]["contact_id"]==contact
    identifier=listing["items"][0]["id"]
    messages=system.call("GET",f"/communications/threads/{identifier}/messages")
    assert messages.json()["messages"][0]["body"]=="Tin gốc của khách"
    assert "SECRET-NOTE" not in messages.text and "admin_note" not in messages.text
    assert system.call("GET","/communications/threads").json()["total"]==1
    assert system.call("GET","/communications/threads",name="other").json()["total"]==0
    for contact_id in (guest,manual):
        assert system.call("POST",f"/communications/contacts/{contact_id}/thread",{},"operator").status_code==404
    assert system.call("POST",f"/communications/contacts/{contact}/thread",{},"operator").json()["thread"]["id"]==identifier


@pytest.mark.parametrize("author",["member","operator"])
def test_every_topic_requires_explicit_approval_and_remains_private_until_then(system,author):
    item=topic(system,author);base="/community/topics/"+item["id"]
    assert item["status"]=="pending"
    assert system.call("GET","/community/topics",name="other").json()["total"]==0
    assert system.call("GET",base,name="other").status_code==404
    assert system.call("GET",base,name=author).status_code==200
    assert system.call("GET","/community/topics?scope=pending",name="operator").json()["total"]==1
    assert system.call("GET","/community/topics?scope=pending").status_code==403
    assert system.call("POST",base+"/comments",{"body":"Too early"},author).status_code==409
    assert system.call("POST",base+"/moderate",{"decision":"approve","expected_revision":1}).status_code==403
    approved=system.call("POST",base+"/moderate",{"decision":"approve","expected_revision":1},"operator")
    assert approved.status_code==200
    assert system.call("GET","/community/topics",name="other").json()["total"]==1
    assert system.call("POST",base+"/comments",{"body":"Tôi cùng trao đổi"},"other").status_code==201


def test_cannot_forge_ownership_or_moderation_fields(system):
    for extra in ({"status":"approved"},{"author_id":"u-operator"},{"approved_by":"u-operator"}):
        assert system.call("POST","/community/topics",{"title":"X","body":"Y",**extra}).status_code==422
    assert system.call("POST","/communications/threads",{"subject":"X","message":"Y","owner_id":"u-other"}).status_code==422
    assert system.call("POST","/community/topics",{"title":"   ","body":"Y"}).status_code==422


def test_edit_requeues_topic_and_prevents_stale_approval(system):
    item=topic(system,approved=True);base="/community/topics/"+item["id"]
    edited=system.call("PATCH",base,{"title":"New title","body":"New body","expected_revision":item["revision"]}).json()["topic"]
    assert edited["status"]=="pending" and edited["approved_at"] is None
    assert system.call("GET",base,name="other").status_code==404
    assert system.call("POST",base+"/moderate",{"decision":"approve","expected_revision":item["revision"]},"operator").status_code==409
    rejected=system.call("POST",base+"/moderate",{"decision":"reject","note":"Hãy bổ sung câu hỏi","expected_revision":edited["revision"]},"operator").json()["topic"]
    assert rejected["moderation_note"]=="Hãy bổ sung câu hỏi"
    assert system.call("GET",base).json()["topic"]["status"]=="rejected"


def test_comment_owner_can_edit_delete_admin_can_remove_but_not_rewrite_others(system):
    item=topic(system,approved=True);base="/community/topics/"+item["id"]
    comment=system.call("POST",base+"/comments",{"body":"Original comment"},"other").json()["comment"]
    path="/community/comments/"+comment["id"]
    for name in ("member","operator"):
        assert system.call("PATCH",path,{"body":"Forged edit","expected_revision":1},name).status_code==403
    assert system.call("DELETE",path,{"expected_revision":1}).status_code==403
    edited=system.call("PATCH",path,{"body":"Edited by owner","expected_revision":1},"other").json()["comment"]
    assert edited["revision"]==2 and edited["body"]=="Edited by owner"
    assert system.call("DELETE",path,{"expected_revision":1},"other").status_code==409
    removed=system.call("DELETE",path,{"expected_revision":2},"other").json()["comment"]
    assert removed["deleted"] and removed["body"]=="" and removed["author_id"] is None
    second=system.call("POST",base+"/comments",{"body":"Remove this too"},"other").json()["comment"]
    assert system.call("DELETE","/community/comments/"+second["id"],{"expected_revision":1},"operator").status_code==200
    visible=system.call("GET",base+"/comments").text
    assert "Original comment" not in visible and "Remove this too" not in visible
    with system.service.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM community_audit WHERE action='comment_deleted'").fetchone()[0]==2


def test_admin_can_remove_topic_and_comments_no_longer_exposed(system):
    item=topic(system,approved=True);base="/community/topics/"+item["id"]
    assert system.call("DELETE",base,{"expected_revision":item["revision"]}).status_code==403
    assert system.call("DELETE",base,{"expected_revision":item["revision"]},"operator").status_code==200
    assert system.call("GET",base,name="other").status_code==404
    assert system.call("GET",base).json()["topic"]["body"]==""
    assert system.call("GET",base+"/comments").json()["items"]==[]


def test_concurrent_retries_create_one_record_without_using_any_consultation_allowance(system):
    user=system.store.get_by_username("member")
    payload=TopicInput(title="Concurrent question",body="Body",client_key=uuid4().hex)
    with ThreadPoolExecutor(max_workers=6) as pool:
        results=list(pool.map(lambda _:system.service.create_topic(user,payload),range(6)))
    assert len({result["id"] for result in results})==1
    request=ThreadInput(subject="Concurrent message",message="Body",client_key=uuid4().hex)
    with ThreadPoolExecutor(max_workers=6) as pool:
        results=list(pool.map(lambda _:system.service.create_thread(user,request),range(6)))
    assert len({result["id"] for result in results})==1
    fresh=JsonUserStore(system.store.path).get_by_username("member")
    assert (fresh.analysis_limit,fresh.analyses_used)==(31,3)
    with system.service.activity.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM activity_results WHERE kind!='contact'").fetchone()[0]==0
