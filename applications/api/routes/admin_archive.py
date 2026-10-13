"""Admin-only unified archive over existing server-owned stores."""
import json
import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query, Request
from applications.api.auth.dependencies import get_auth_service, get_user_service
from applications.api.services.analysis_archive import _connect, get_snapshot

ROOT = Path(__file__).resolve().parents[3]
router = APIRouter(prefix='/admin-archive', tags=['admin archive'])

def require_admin(request):
    user = getattr(request.state, 'user', None) or get_auth_service().resolve_user_from_request(request)
    if user is None:
        raise HTTPException(401, 'Bạn cần đăng nhập')
    if getattr(user.role, 'value', user.role) != 'ADMIN':
        raise HTTPException(403, 'Chỉ quản trị viên được truy cập toàn bộ hồ sơ')
    return user

def marriage_path():
    return Path(os.getenv('BTE_MARRIAGE_DATA_PATH') or ROOT/'applications/data/marriage_consultations.json').expanduser()

def child_path():
    return Path(os.getenv('BTE_CHILDBIRTH_DATA_DIR') or ROOT/'applications/data/childbirth').expanduser()

def creator(owner, username='', name=''):
    uid = owner.removeprefix('user:') if owner.startswith('user:') else ''
    user = get_user_service().store.get_by_id(uid) if uid else None
    return {'owner': owner, 'creator_user_id': uid or None,
            'creator_username': username or (user.username if user else '') or 'Chưa xác định',
            'creator_display_name': name or (getattr(user, 'display_name', '') if user else '') or ''}

def legacy_records():
    records, warnings = [], []
    path = marriage_path()
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding='utf-8-sig'))
            if not isinstance(data, list):
                raise ValueError('Invalid marriage store')
            for stored in data:
                history = stored['history']
                identifier = history['consultation_id']
                request = stored.get('request') or {}
                options = request.get('options') or {}
                audience = options.get('audience', '')
                # Business requests share the compatibility repository.
                client = (request.get('request_meta') or {}).get('client') or ''
                kind = 'business' if stored.get('business_profile') or client.split(';',1)[0] == 'business_consulting' else 'marriage'
                owner = 'user:'+stored['owner_user_id'] if stored.get('owner_user_id') else 'unknown'
                records.append({'kind': kind, 'id': identifier, 'created_at': history.get('created_at'),
                                'customer_name': history.get('display_label') or identifier,
                                **creator(owner, stored.get('creator_username',''), stored.get('creator_display_name',''))})
        except Exception:
            warnings.append('Không đọc đầy đủ kho hôn nhân/hợp tác. Cần kiểm tra dữ liệu nguồn.')
    for path in child_path().glob('CB-*.json'):
        try:
            stored = json.loads(path.read_text(encoding='utf-8-sig'))
            inputs = stored.get('input') or {}
            names = ' / '.join((inputs.get(k) or {}).get('full_name') or default
                               for k, default in [('father','Người bố'),('mother','Người mẹ')])
            owner = 'user:'+stored['owner_user_id'] if stored.get('owner_user_id') else 'unknown'
            records.append({'kind': 'childbirth', 'id': stored['consultation_id'],
                            'created_at': stored.get('created_at'), 'customer_name': names,
                            **creator(owner, stored.get('creator_username',''), stored.get('creator_display_name',''))})
        except Exception:
            warnings.append('Không đọc được một hồ sơ sinh con: '+path.stem)
    return records, warnings

@router.get('')
def list_all(request: Request, kind: str='', username: str='', q: str='',
             page: int=Query(1, ge=1), limit: int=Query(50, ge=1, le=200)):
    require_admin(request)
    with _connect() as conn:
        rows = conn.execute("SELECT owner,id,saved_at,json_extract(snapshot,'$.input.full_name'),json_extract(snapshot,'$.creator_username'),json_extract(snapshot,'$.creator_display_name') FROM analyses ORDER BY saved_at DESC,id DESC").fetchall()
    items = [{'kind':'bazi', 'id':r[1], 'created_at':r[2], 'customer_name':r[3] or 'Chưa đặt tên', **creator(r[0],r[4] or "",r[5] or "")} for r in rows]
    with _connect() as conn:
        exists=conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='van_han_results'").fetchone()
        records=conn.execute("SELECT owner,id,saved_at,json_extract(snapshot,'$.result.name'),json_extract(snapshot,'$.creator_username'),json_extract(snapshot,'$.creator_display_name') FROM van_han_results").fetchall() if exists else []
    items.extend({'kind':'van_han','id':v[1],'created_at':v[2],'customer_name':v[3] or 'Chưa đặt tên',**creator(v[0],v[4] or '',v[5] or '')} for v in records)
    others, warnings = legacy_records()
    items.extend(others)
    counts = {key:sum(r['kind']==key for r in items) for key in ('bazi','marriage','business','childbirth','van_han')}
    users = sorted({r['creator_username'] for r in items})
    items = [r for r in items if (not kind or r['kind']==kind) and
             (not username or r['creator_username']==username) and
             (not q or q.casefold() in ' '.join(str(r.get(k) or '') for k in ('customer_name','id','creator_username','creator_display_name')).casefold())]
    items.sort(key=lambda r:(r.get('created_at') or '',r['id'],r['owner']), reverse=True)
    total = len(items)
    return {'items':items[(page-1)*limit:page*limit], 'total':total, 'page':page, 'limit':limit,
            'counts':counts, 'users':users, 'warnings':warnings}

@router.get('/{kind}/{identifier}')
def get_record(kind: str, identifier: str, request: Request, owner: str=''):
    require_admin(request)
    if kind == 'bazi':
        if not owner:
            raise HTTPException(422, 'Thiếu tài khoản chủ hồ sơ')
        row = get_snapshot(owner, identifier)
    elif kind == 'van_han':
        from applications.api.services.van_han_service import get_result
        row=get_result('',identifier,admin=True)
    elif kind in ('marriage','business'):
        path = marriage_path()
        records = json.loads(path.read_text(encoding='utf-8-sig')) if path.exists() else []
        row = next((r for r in records if r.get('history',{}).get('consultation_id')==identifier),None)
    elif kind == 'childbirth':
        import re
        if not re.fullmatch(r'CB-[a-f0-9]{32}', identifier):
            raise HTTPException(404, 'Không tìm thấy hồ sơ')
        path = child_path()/(identifier+'.json')
        row = json.loads(path.read_text(encoding='utf-8-sig')) if path.exists() else None
    else:
        row = None
    if row is None:
        raise HTTPException(404, 'Không tìm thấy hồ sơ')
    return {'row':row}
