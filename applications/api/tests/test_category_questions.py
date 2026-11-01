import sqlite3
from uuid import uuid4
import pytest
from applications.api.tests.test_communications import system
from applications.api.services.communications import CommunicationsService
from applications.api.services.knowledge import KnowledgeService,INITIAL_CATEGORIES
from applications.api.schemas.knowledge import ArticleInput


@pytest.fixture(autouse=True)
def isolated_library(tmp_path,monkeypatch):
    monkeypatch.setenv('BTE_KNOWLEDGE_DB_PATH',str(tmp_path/'library.sqlite3'))


def question(system,category='co-ban',name='member',**kwargs):
    payload={'title':'Câu hỏi của thành viên','body':'Xin trao đổi về nội dung đã học.',**kwargs}
    if category is not None:payload['category_id']=category
    response=system.call('POST','/community/topics',payload,name)
    assert response.status_code==201,response.text
    return response.json()['topic']


def approve(system,item):
    response=system.call('POST','/community/topics/'+item['id']+'/moderate',{'decision':'approve','expected_revision':item['revision']},'operator')
    assert response.status_code==200,response.text
    return response.json()['topic']


@pytest.mark.parametrize('category',[item[0] for item in INITIAL_CATEGORIES])
def test_each_of_nine_categories_requires_approval_before_public_answers(system,category):
    item=question(system,category);path='/community/topics/'+item['id']
    assert item['status']=='pending' and item['category_id']==category
    assert system.call('GET','/community/topics?category_id='+category,name='other').json()['total']==0
    assert system.call('GET',path,name='other').status_code==404
    assert system.call('POST',path+'/comments',{'body':'Too early'}).status_code==409
    pending=system.call('GET','/community/topics?scope=pending&category_id='+category,name='operator').json()
    assert pending['total']==1 and pending['items'][0]['id']==item['id']
    approve(system,item)
    assert system.call('GET','/community/topics?category_id='+category,name='other').json()['items'][0]['id']==item['id']
    assert system.call('POST',path+'/comments',{'body':'Cộng đồng trả lời'},'other').status_code==201
    assert system.call('POST',path+'/comments',{'body':'Admin giải đáp'},'operator').status_code==201


def test_categories_are_member_only_and_filters_do_not_mix_questions(system):
    assert system.client.get('/api/v1/community/categories').status_code==401
    for name in ('pending','expired'):
        assert system.call('GET','/community/categories',name=name).status_code==403
        assert system.call('GET','/community/topics?category_id=co-ban',name=name).status_code==403
    labels=system.call('GET','/community/categories').json()['items']
    assert [row['title'] for row in labels]==[item[1] for item in INITIAL_CATEGORIES]
    basic=approve(system,question(system,'co-ban'))
    approve(system,question(system,'nha-o'))
    general=approve(system,question(system,None))
    assert general['category_id'] is None
    rows=system.call('GET','/community/topics?category_id=co-ban',name='other').json()['items']
    assert [row['id'] for row in rows]==[basic['id']]
    assert system.call('GET','/community/topics',name='other').json()['total']==3
    assert system.call('GET','/community/topics?scope=mine&category_id=co-ban',name='other').json()['total']==0


def test_invalid_category_or_attempt_to_change_category_is_rejected(system):
    assert system.call('POST','/community/topics',{'title':'X','body':'Y','category_id':'absent'}).status_code==404
    assert system.call('GET','/community/topics?category_id=absent').status_code==404
    assert system.call('POST','/community/topics',{'title':'X','body':'Y','category_id':''}).status_code==422
    item=question(system)
    assert system.call('PATCH','/community/topics/'+item['id'],{'title':'X','body':'Y','expected_revision':1,'category_id':'nha-o'}).status_code==422


def test_nonce_is_bound_to_category_and_edited_question_requires_review_again(system):
    key=uuid4().hex
    item=question(system,client_key=key)
    assert question(system,client_key=key)['id']==item['id']
    assert system.call('POST','/community/topics',{'title':item['title'],'body':item['body'],'category_id':'nha-o','client_key':key}).status_code==409
    published=approve(system,item)
    changed=system.call('PATCH','/community/topics/'+item['id'],{'title':'Câu hỏi đã sửa','body':'Nội dung mới','expected_revision':published['revision']}).json()['topic']
    assert changed['category_id']=='co-ban' and changed['status']=='pending'
    assert system.call('GET','/community/topics?category_id=co-ban',name='other').json()['total']==0
    assert system.call('POST','/community/topics/'+item['id']+'/moderate',{'decision':'approve','expected_revision':published['revision']},'operator').status_code==409


def test_authored_faq_articles_and_allowances_are_preserved(system):
    library=KnowledgeService(system.store)
    saved=library.save_article(system.store.get_by_username('operator'),ArticleInput(group_id='co-ban-4',title='Bài giải đáp đã biên soạn',body='Nội dung Admin đã viết.',status='published'))
    item=approve(system,question(system))
    comment=system.call('POST','/community/topics/'+item['id']+'/comments',{'body':'Câu trả lời của tôi'},'other').json()['comment']
    assert system.call('DELETE','/community/comments/'+comment['id'],{'expected_revision':1}).status_code==403
    assert system.call('DELETE','/community/comments/'+comment['id'],{'expected_revision':1},'operator').status_code==200
    category=library.category(system.store.get_by_username('member'),'co-ban')['category']
    faq=next(group for group in category['groups'] if group['id']=='co-ban-4')
    assert faq['is_faq'] and faq['articles'][0]['id']==saved['id']
    assert sum(group['is_faq'] for group in category['groups'])==1
    member=system.store.get_by_username('member')
    assert (member.analysis_limit,member.analyses_used)==(31,3)
    with system.service.activity.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM activity_results WHERE kind!='contact'").fetchone()[0]==0


def test_existing_forum_schema_upgrades_without_losing_approved_topics(system):
    path=system.tmp/'legacy-communications.sqlite3'
    with sqlite3.connect(path) as connection:
        connection.executescript("""CREATE TABLE knowledge_topics(
          id TEXT PRIMARY KEY,author_id TEXT NOT NULL,author_name TEXT NOT NULL,author_username TEXT NOT NULL,
          author_is_admin INTEGER NOT NULL,title TEXT NOT NULL,body TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'pending',
          revision INTEGER NOT NULL DEFAULT 1,client_key TEXT NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,
          approved_at TEXT,approved_by TEXT,moderation_note TEXT NOT NULL DEFAULT '',deleted_by TEXT,
          UNIQUE(author_id,client_key));""")
        connection.execute("INSERT INTO knowledge_topics(id,author_id,author_name,author_username,author_is_admin,title,body,status,client_key,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            ('old-topic','u-member','member','member',0,'Chủ đề cũ','Nội dung cũ','approved','legacy-key-123456','2026-10-01','2026-10-01'))
    service=CommunicationsService(system.store,path)
    member=system.store.get_by_username('member')
    items=service.list_topics(member)['items']
    assert items[0]['id']=='old-topic' and items[0]['category_id'] is None
    assert service.topic_detail(member,'old-topic')['body']=='Nội dung cũ'
    assert service.list_topics(member,category_id='co-ban')['total']==0
    assert CommunicationsService(system.store,path).list_topics(member)['total']==1
