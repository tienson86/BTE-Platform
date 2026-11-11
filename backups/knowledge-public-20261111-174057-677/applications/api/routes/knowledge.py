"""Member reads and Admin-only content authoring for the ordered library."""
from typing import Literal
from fastapi import APIRouter,Query
from applications.api.auth.dependencies import CurrentUser
from applications.api.schemas.knowledge import CategoryInput,CategoryEdit,GroupInput,GroupEdit,ArticleInput,ArticleEdit
from applications.api.services.knowledge import get_knowledge_service

router=APIRouter(tags=["Knowledge library"])

@router.get("/knowledge/catalog")
def catalog(user:CurrentUser):
    return get_knowledge_service().catalog(user)

@router.get("/knowledge/categories/{identifier}")
def category(identifier:str,user:CurrentUser):
    return get_knowledge_service().category(user,identifier)

@router.get("/knowledge/articles/{identifier}")
def article(identifier:str,user:CurrentUser):
    return get_knowledge_service().article(user,identifier)

@router.get("/knowledge/search")
def search(user:CurrentUser,q:str=Query(min_length=1,max_length=120),page:int=Query(1,ge=1),limit:int=Query(20,ge=1,le=50)):
    return get_knowledge_service().search(user,q,page,limit)

@router.get("/admin/knowledge/catalog")
def admin_catalog(user:CurrentUser):
    return get_knowledge_service().catalog(user,management=True)

@router.get("/admin/knowledge/articles")
def articles(user:CurrentUser,q:str=Query("",max_length=120),category_id:str|None=Query(None,max_length=100),group_id:str|None=Query(None,max_length=100),status:Literal["draft","published"]|None=None,page:int=Query(1,ge=1),limit:int=Query(20,ge=1,le=50)):
    return get_knowledge_service().search(user,q,page,limit,True,category_id,group_id,status)

@router.get("/admin/knowledge/articles/{identifier}")
def admin_article(identifier:str,user:CurrentUser):
    return get_knowledge_service().article(user,identifier,management=True)

@router.post("/admin/knowledge/categories",status_code=201)
def create_category(body:CategoryInput,user:CurrentUser):
    return {"category":get_knowledge_service().save_category(user,body)}

@router.patch("/admin/knowledge/categories/{identifier}")
def edit_category(identifier:str,body:CategoryEdit,user:CurrentUser):
    return {"category":get_knowledge_service().save_category(user,body,identifier)}

@router.post("/admin/knowledge/groups",status_code=201)
def create_group(body:GroupInput,user:CurrentUser):
    return {"group":get_knowledge_service().save_group(user,body)}

@router.patch("/admin/knowledge/groups/{identifier}")
def edit_group(identifier:str,body:GroupEdit,user:CurrentUser):
    return {"group":get_knowledge_service().save_group(user,body,identifier)}

@router.post("/admin/knowledge/articles",status_code=201)
def create_article(body:ArticleInput,user:CurrentUser):
    return {"article":get_knowledge_service().save_article(user,body)}

@router.patch("/admin/knowledge/articles/{identifier}")
def edit_article(identifier:str,body:ArticleEdit,user:CurrentUser):
    return {"article":get_knowledge_service().save_article(user,body,identifier)}
