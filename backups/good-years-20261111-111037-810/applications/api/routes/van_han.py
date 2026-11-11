from typing import Literal
from fastapi import APIRouter,Request,HTTPException,Query
from fastapi.responses import FileResponse
from pydantic import BaseModel,Field
from starlette.background import BackgroundTask
from applications.api.auth.dependencies import get_auth_service
from applications.api.services.analysis_archive import _connect,get_snapshot
from applications.api.services.van_han_service import calculate,save_result,get_result,list_results

router=APIRouter(prefix='/van-han',tags=['Tính vận hạn'])
def current_user(request):
    user=getattr(request.state,'user',None) or get_auth_service().resolve_user_from_request(request)
    if not user:raise HTTPException(401,'Bạn cần đăng nhập để tính và lưu vận hạn')
    return user
def is_admin(user):return getattr(user.role,'value',user.role)=='ADMIN'

class CalculateRequest(BaseModel):
    analysis_id:str=Field(min_length=1)
    source_owner:str|None=None
    start_year:int=Field(ge=1900,le=2100)
    end_year:int=Field(ge=1900,le=2100)

@router.get('/sources')
def sources(request:Request,q:str=Query('',max_length=120),limit:int=Query(30,ge=1,le=100),
            offset:int=Query(0,ge=0),analysis_id:str='',source_owner:str=''):
    user=current_user(request);owner='user:'+user.user_id
    if source_owner and source_owner!=owner and not is_admin(user):
        raise HTTPException(403,'Bạn không được tìm hồ sơ của tài khoản khác')
    from applications.api.services.van_han_source_index import search
    with _connect() as conn:
        rows,total=search(conn,owner,is_admin(user),q,limit,offset,analysis_id,source_owner)
    from applications.api.routes.admin_archive import creator
    users={}
    items=[]
    for row in rows:
        if row[0] not in users:users[row[0]]=creator(row[0])['creator_username']
        items.append({'owner':row[0],'id':row[1],'created_at':row[2],'name':row[3],
                      'birth_date':row[4],'birth_time':row[5],'gender':row[6],'creator_username':users[row[0]]})
    return {'items':items,'total':total,'offset':offset,'limit':limit,'has_more':offset+len(items)<total}

@router.post('/analyze')
def analyze(request:Request,body:CalculateRequest):
    user=current_user(request);owner='user:'+user.user_id
    if body.source_owner and body.source_owner!=owner:
        if not is_admin(user):raise HTTPException(403,'Bạn không được dùng hồ sơ của tài khoản khác')
        owner=body.source_owner
    row=get_snapshot(owner,body.analysis_id)
    if row is None:raise HTTPException(404,'Không tìm thấy lá số trong quyền truy cập của bạn')
    try:result=calculate(row,body.start_year,body.end_year)
    except (ValueError,KeyError,TypeError) as error:raise HTTPException(422,str(error)) from error
    result['source_owner']=owner
    return {'row':save_result(user,result)}

@router.get('/history')
def history(request:Request):
    user=current_user(request)
    return {'items':list_results('user:'+user.user_id,is_admin(user))}

def owned(request,identifier):
    user=current_user(request);row=get_result('user:'+user.user_id,identifier,is_admin(user))
    if row is None:raise HTTPException(404,'Không tìm thấy hồ sơ vận hạn trong quyền truy cập của bạn')
    return row

@router.get('/{identifier}')
def get_one(identifier:str,request:Request):return {'row':owned(request,identifier)}

@router.get('/{identifier}/export/{fmt}')
def export(identifier:str,fmt:Literal['pdf','docx'],request:Request):
    row=owned(request,identifier)
    from applications.api.services.van_han_export import export_file
    from consulting.marriage.report.export import cleanup_marriage_export
    import logging
    try:artifact=export_file(row,fmt)
    except Exception:
        logging.getLogger(__name__).exception('van_han_export_failed id=%s format=%s',identifier,fmt)
        raise HTTPException(500,'Chưa tạo được '+fmt.upper()+'. Mã hồ sơ: '+identifier+'. Hãy gửi kết quả kiểm tra tải tài liệu để xác định lỗi.') from None
    return FileResponse(str(artifact.path),media_type=artifact.media_type,filename=artifact.filename,
                        background=BackgroundTask(cleanup_marriage_export,artifact.path))
