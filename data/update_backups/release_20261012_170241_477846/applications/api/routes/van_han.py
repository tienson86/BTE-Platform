from typing import Literal
from fastapi import APIRouter,Request,HTTPException
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
def sources(request:Request):
    user=current_user(request);owner='user:'+user.user_id
    with _connect() as conn:
        sql="SELECT owner,id,saved_at,json_extract(snapshot,'$.input.full_name') FROM analyses"
        rows=conn.execute(sql+('' if is_admin(user) else ' WHERE owner=?')+' ORDER BY saved_at DESC',() if is_admin(user) else (owner,)).fetchall()
    from applications.api.routes.admin_archive import creator
    return {'items':[{'owner':r[0],'id':r[1],'created_at':r[2],'name':r[3] or 'Chưa đặt tên',
                      'creator_username':creator(r[0])['creator_username']} for r in rows]}

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
    artifact=export_file(row,fmt)
    return FileResponse(str(artifact.path),media_type=artifact.media_type,filename=artifact.filename,
                        background=BackgroundTask(cleanup_marriage_export,artifact.path))
