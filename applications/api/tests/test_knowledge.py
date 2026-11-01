from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timedelta,timezone
from types import SimpleNamespace
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from applications.api import dependencies
from applications.api.app import create_app
from applications.api.auth.password_hasher import hash_password
from applications.api.auth.roles import Role
from applications.api.auth.store import JsonUserStore,UserRecord
from applications.api.services.auth_service import AuthService
from applications.api.services.knowledge import KnowledgeService
from applications.api.schemas.knowledge import ArticleInput


@pytest.fixture
def system(tmp_path,monkeypatch):
    monkeypatch.setenv('BTE_KNOWLEDGE_DB_PATH',str(tmp_path/'library.sqlite3'))
    monkeypatch.setenv('BTE_USAGE_DB_PATH',str(tmp_path/'activity.sqlite3'))
    store=JsonUserStore(tmp_path/'users.json');password=hash_password('test-password-123')
    for name in ('operator','member','pending','expired','legacy'):
        membership=None if name in ('operator','legacy') else {'status':'pending' if name=='pending' else 'active','expires_at':(datetime.now(timezone.utc)+timedelta(days=-1 if name=='expired' else 30)).isoformat()}
        store.add_user(UserRecord('u-'+name,name,password,Role.ADMIN if name=='operator' else Role.CUSTOMER,display_name=name,analysis_limit=31,analyses_used=7,membership=membership))
    auth=AuthService(store);monkeypatch.setattr(dependencies,'get_auth_service',lambda:auth)
    headers={name:{'Authorization':'Bearer '+auth.login(name,'test-password-123')[1].access_token} for name in ('operator','member','pending','expired','legacy')}
    client=TestClient(create_app())
    def call(method,path,body=None,name='operator'):
        return client.request(method,'/api/v1'+path,headers=headers[name],**({'json':body} if body is not None else {}))
    return SimpleNamespace(call=call,client=client,store=store,service=KnowledgeService(store),tmp=tmp_path)


def article(system,**kwargs):
    payload={'group_id':'ngay-gio-1','title':'Bài phương pháp ngày giờ','summary':'Giới thiệu bài','body':'## Kiến thức nền\n\nNội dung thử riêng.','status':'draft','position':10,**kwargs}
    response=system.call('POST','/admin/knowledge/articles',payload)
    assert response.status_code==201,response.text
    return response.json()['article']


def edit_payload(item,**changes):
    return {**{key:item[key] for key in ('group_id','title','summary','body','position','status')},'expected_revision':item['revision'],**changes}


@pytest.mark.parametrize('path',['/knowledge/catalog','/knowledge/categories/ngay-gio','/knowledge/articles/id','/knowledge/search?q=ten','/admin/knowledge/catalog','/admin/knowledge/articles'])
def test_guest_cannot_access_library(system,path):
    assert system.client.get('/api/v1'+path).status_code==401


@pytest.mark.parametrize('name',['pending','expired'])
@pytest.mark.parametrize('path',['/knowledge/catalog','/knowledge/categories/ngay-gio','/knowledge/articles/id','/knowledge/search?q=ten'])
def test_every_read_requires_current_member_access(system,name,path):
    assert system.call('GET',path,name=name).status_code==403


def test_initial_structure_is_idempotent_and_preserves_admin_edits(system):
    catalog=system.call('GET','/knowledge/catalog',name='legacy').json()
    assert len(catalog['categories'])==4 and len(catalog['latest'])==0
    assert all(len(item['groups'])==4 and item['article_count']==0 for item in catalog['categories'])
    row=catalog['categories'][0]
    changed=system.call('PATCH','/admin/knowledge/categories/'+row['id'],{'title':'Chuyên mục đã chỉnh','description':'Mô tả riêng','position':55,'expected_revision':row['revision']})
    assert changed.status_code==200
    fresh=KnowledgeService(JsonUserStore(system.store.path)).catalog(system.store.get_by_username('legacy'))
    assert len(fresh['categories'])==4
    assert next(item for item in fresh['categories'] if item['id']==row['id'])['title']=='Chuyên mục đã chỉnh'


def test_drafts_are_never_exposed_by_detail_lists_search_counts_or_next_links(system):
    draft=article(system,title='SECRET-DRAFT-ONLY')
    public=article(system,title='Public article',status='published')
    for name in ('member','operator'):
        for path in ('/knowledge/catalog','/knowledge/categories/ngay-gio','/knowledge/search?q=SECRET','/knowledge/articles/'+public['id']):
            response=system.call('GET',path,name=name)
            assert response.status_code==200 and 'SECRET-DRAFT' not in response.text
        assert system.call('GET','/knowledge/articles/'+draft['id'],name=name).status_code==404
    assert system.call('GET','/admin/knowledge/articles/'+draft['id']).json()['article']['body']==draft['body']
    catalog=system.call('GET','/knowledge/catalog',name='member').json()
    assert catalog['categories'][0]['article_count']==1
    assert len(catalog['latest'])==1


@pytest.mark.parametrize('collection,payload',[('categories',{'title':'X'}),('groups',{'title':'X','category_id':'ngay-gio'}),('articles',{'title':'X','group_id':'ngay-gio-1','body':'Y'})])
def test_member_cannot_author_content(system,collection,payload):
    assert system.call('POST','/admin/knowledge/'+collection,payload,'member').status_code==403
    assert system.call('GET','/admin/knowledge/catalog',name='member').status_code==403


def test_publish_unpublish_and_latest_six_apply_immediately(system):
    item=article(system)
    posted=system.call('PATCH','/admin/knowledge/articles/'+item['id'],edit_payload(item,status='published')).json()['article']
    assert posted['published_at']
    assert system.call('GET','/knowledge/articles/'+item['id'],name='member').status_code==200
    for number in range(7):article(system,title='Bài '+str(number),status='published')
    assert len(system.call('GET','/knowledge/catalog',name='member').json()['latest'])==6
    hidden=system.call('PATCH','/admin/knowledge/articles/'+item['id'],edit_payload(posted,status='draft'))
    assert hidden.status_code==200 and hidden.json()['article']['published_at'] is None
    assert system.call('GET','/knowledge/articles/'+item['id'],name='member').status_code==404


def test_lesson_sequence_follows_group_then_article_position_skipping_drafts(system):
    last=article(system,group_id='ngay-gio-2',position=1,status='published',title='Last')
    second=article(system,position=20,status='published',title='Second')
    first=article(system,position=10,status='published',title='First')
    article(system,position=15,title='Hidden in between')
    item=system.call('GET','/knowledge/articles/'+second['id'],name='member').json()
    assert item['previous']['id']==first['id'] and item['next']['id']==last['id']
    assert system.call('GET','/knowledge/articles/'+first['id'],name='member').json()['previous'] is None
    assert system.call('GET','/knowledge/articles/'+last['id'],name='member').json()['next'] is None


def test_search_supports_unaccented_vietnamese_body_matches_and_literal_wildcards(system):
    item=article(system,title='Tìm hiểu Địa lý',body='Phương pháp tính ngày giờ và bố trí không gian.',status='published')
    assert system.call('GET','/knowledge/search?q=dia%20ly',name='member').json()['items'][0]['id']==item['id']
    assert system.call('GET','/knowledge/search?q=NGAY%20GIO',name='member').json()['total']==1
    assert system.call('GET','/knowledge/search?q=%25',name='member').json()['total']==0
    assert system.call('GET','/knowledge/search?q=%27%20OR%201%3D1--',name='member').json()['total']==0


def test_article_and_structure_revisions_prevent_lost_updates(system):
    item=article(system);path='/admin/knowledge/articles/'+item['id'];body=edit_payload(item,title='New version')
    assert system.call('PATCH',path,body).status_code==200
    assert system.call('PATCH',path,body).status_code==409
    category={'title':'Updated title','description':'','position':1,'expected_revision':1}
    assert system.call('PATCH','/admin/knowledge/categories/ngay-gio',category).status_code==200
    assert system.call('PATCH','/admin/knowledge/categories/ngay-gio',category).status_code==409
    group={'title':'Group title','description':'','position':1,'category_id':'nha-o','expected_revision':1}
    assert system.call('PATCH','/admin/knowledge/groups/ngay-gio-1',group).status_code==200
    assert system.call('PATCH','/admin/knowledge/groups/ngay-gio-1',group).status_code==409


def test_new_structure_group_moves_and_filters(system):
    category=system.call('POST','/admin/knowledge/categories',{'title':'Chuyên mục mới','position':70}).json()['category']
    group=system.call('POST','/admin/knowledge/groups',{'title':'Nhóm mới','category_id':category['id'],'position':10}).json()['group']
    item=article(system,group_id=group['id'],status='published')
    assert system.call('GET','/admin/knowledge/articles?category_id='+category['id']+'&status=published').json()['total']==1
    moved=system.call('PATCH','/admin/knowledge/groups/'+group['id'],{'title':group['title'],'category_id':'nha-o','position':90,'expected_revision':group['revision']})
    assert moved.status_code==200
    assert system.call('GET','/knowledge/articles/'+item['id'],name='member').json()['article']['category_id']=='nha-o'


def test_validation_and_missing_parents_do_not_create_partial_records(system):
    assert system.call('POST','/admin/knowledge/articles',{'title':'X','group_id':'absent','body':'Y'}).status_code==404
    assert system.call('POST','/admin/knowledge/groups',{'title':'X','category_id':'absent'}).status_code==404
    for extra in ({'author_id':'forged'},{'revision':100},{'status':'approved'}):
        assert system.call('POST','/admin/knowledge/articles',{'title':'X','group_id':'ngay-gio-1','body':'Y',**extra}).status_code==422
    assert system.call('POST','/admin/knowledge/categories',{'title':'   '}).status_code==422
    assert system.call('GET','/admin/knowledge/articles').json()['total']==0


def test_search_pagination_and_idempotent_concurrent_save_use_no_allowance(system):
    user=system.store.get_by_username('operator')
    request=ArticleInput(group_id='ngay-gio-1',title='Same save',body='Body',status='published',client_key=uuid4().hex)
    with ThreadPoolExecutor(max_workers=6) as pool:
        rows=list(pool.map(lambda _:system.service.save_article(user,request),range(6)))
    assert len({row['id'] for row in rows})==1
    for index in range(22):article(system,title='Body lesson '+str(index),status='published')
    first=system.call('GET','/knowledge/search?q=body&page=1',name='member').json()
    second=system.call('GET','/knowledge/search?q=body&page=2',name='member').json()
    assert first['total']==23 and len(first['items'])==20 and len(second['items'])==3
    assert len({item['id'] for item in first['items']+second['items']})==23
    member=JsonUserStore(system.store.path).get_by_username('member')
    assert (member.analysis_limit,member.analyses_used)==(31,7)
    assert not (system.tmp/'activity.sqlite3').exists()
