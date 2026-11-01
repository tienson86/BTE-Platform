"""Authenticated private support and paid-member knowledge discussions."""
from typing import Literal
from fastapi import APIRouter, Query
from applications.api.auth.dependencies import CurrentUser
from applications.api.schemas.communications import (
    ThreadInput, MessageInput, ReadInput, TopicInput, TopicEdit,
    ModerateInput, RevisionInput, CommentInput, CommentEdit,
)
from applications.api.services.communications import get_communications_service

router=APIRouter(tags=["Member communications"])

@router.get("/communications/summary")
def summary(user:CurrentUser):
    return get_communications_service().summary(user)

@router.get("/communications/recipients")
def recipients(user:CurrentUser):
    return {"items":get_communications_service().recipients(user)}

@router.get("/communications/threads")
def threads(user:CurrentUser,page:int=Query(1,ge=1),limit:int=Query(30,ge=1,le=100)):
    return get_communications_service().list_threads(user,page,limit)

@router.post("/communications/threads",status_code=201)
def create_thread(body:ThreadInput,user:CurrentUser):
    return {"thread":get_communications_service().create_thread(user,body)}

@router.get("/communications/threads/{identifier}/messages")
def messages(identifier:str,user:CurrentUser,before:int|None=Query(None,ge=1),limit:int=Query(50,ge=1,le=100)):
    return get_communications_service().thread_messages(user,identifier,before,limit)

@router.post("/communications/threads/{identifier}/messages",status_code=201)
def send(identifier:str,body:MessageInput,user:CurrentUser):
    return {"message":get_communications_service().send_message(user,identifier,body)}

@router.post("/communications/threads/{identifier}/read")
def mark_read(identifier:str,body:ReadInput,user:CurrentUser):
    return get_communications_service().mark_read(user,identifier,body.last_message_id)

@router.post("/communications/contacts/{identifier}/thread")
def contact_thread(identifier:str,user:CurrentUser):
    return {"thread":get_communications_service().contact_thread(user,identifier)}

@router.get("/community/topics")
def topics(user:CurrentUser,scope:Literal["feed","mine","pending","all"]="feed",page:int=Query(1,ge=1),limit:int=Query(30,ge=1,le=100)):
    return get_communications_service().list_topics(user,scope,page,limit)

@router.post("/community/topics",status_code=201)
def create_topic(body:TopicInput,user:CurrentUser):
    return {"topic":get_communications_service().create_topic(user,body)}

@router.get("/community/topics/{identifier}")
def topic(identifier:str,user:CurrentUser):
    return {"topic":get_communications_service().topic_detail(user,identifier)}

@router.patch("/community/topics/{identifier}")
def edit_topic(identifier:str,body:TopicEdit,user:CurrentUser):
    return {"topic":get_communications_service().edit_topic(user,identifier,body)}

@router.post("/community/topics/{identifier}/moderate")
def moderate(identifier:str,body:ModerateInput,user:CurrentUser):
    return {"topic":get_communications_service().moderate(user,identifier,body)}

@router.delete("/community/topics/{identifier}")
def delete_topic(identifier:str,body:RevisionInput,user:CurrentUser):
    return get_communications_service().delete_topic(user,identifier,body.expected_revision)

@router.get("/community/topics/{identifier}/comments")
def comments(identifier:str,user:CurrentUser,page:int=Query(1,ge=1),limit:int=Query(50,ge=1,le=100)):
    return get_communications_service().comments(user,identifier,page,limit)

@router.post("/community/topics/{identifier}/comments",status_code=201)
def add_comment(identifier:str,body:CommentInput,user:CurrentUser):
    return {"comment":get_communications_service().create_comment(user,identifier,body)}

@router.patch("/community/comments/{identifier}")
def edit_comment(identifier:str,body:CommentEdit,user:CurrentUser):
    return {"comment":get_communications_service().change_comment(user,identifier,body.expected_revision,body.body)}

@router.delete("/community/comments/{identifier}")
def delete_comment(identifier:str,body:RevisionInput,user:CurrentUser):
    return {"comment":get_communications_service().change_comment(user,identifier,body.expected_revision)}
