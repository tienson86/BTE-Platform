"""Account ownership for isolated consulting API; identity verified by main API."""
from contextvars import ContextVar
import os
import httpx
from fastapi.responses import JSONResponse

identity = ContextVar('bte_consulting_identity', default=None)

def creator_fields():
    user = identity.get()
    if not user:
        raise RuntimeError('Authenticated creator required')
    return {'owner_user_id': user['user_id'], 'creator_username': user.get('username', ''),
            'creator_display_name': user.get('display_name', '') or ''}

def can_read(stored):
    user = identity.get()
    return bool(user and (user.get('role') == 'ADMIN' or
                         getattr(stored, 'owner_user_id', None) == user['user_id']))

def register_consulting_access(app, marriage_api, childbirth_repository):
    @app.middleware('http')
    async def account_scope(request, call_next):
        path = request.url.path
        if not path.startswith('/api/v1/consulting/'):
            return await call_next(request)
        authorization = request.headers.get('authorization', '')
        if not authorization:
            return JSONResponse({'detail': 'Bạn cần đăng nhập'}, status_code=401)
        base = os.getenv('BTE_API_BASE_URL') or ('http://127.0.0.1:' + os.getenv('API_PORT', '8000'))
        try:
            async with httpx.AsyncClient(timeout=8, follow_redirects=False) as client:
                response = await client.get(base.rstrip('/')+'/api/v1/auth/me',
                                            headers={'Authorization': authorization})
            if response.status_code != 200:
                return JSONResponse({'detail': 'Phiên đăng nhập không hợp lệ'}, status_code=401 if response.status_code in (401,403) else 503)
            user = response.json()
            if not isinstance(user, dict) or not user.get('user_id'):
                raise ValueError('Invalid auth response')
            if not user.get('member_access', False):
                return JSONResponse({'detail': 'Tài khoản chưa có quyền thành viên đang còn hiệu lực.',
                                     'code': 'membership_required', 'membership_url': '/membership'}, status_code=403)
        except Exception:
            return JSONResponse({'detail': 'Chưa xác thực được tài khoản. Hãy thử lại.'}, status_code=503)
        token = identity.set(user)
        try:
            # Check ownership before route handlers, exports or save operations execute.
            parts = path.strip('/').split('/')
            if len(parts) > 4:
                kind, identifier = parts[3], parts[4]
                if kind == 'marriage' and identifier == 'business':
                    identifier = parts[5] if len(parts) > 5 else ''
                reserved = {'', 'history', 'analyze'}
                if identifier not in reserved:
                    try:
                        stored = (childbirth_repository.get(identifier) if kind == 'childbirth'
                                  else marriage_api._repository.get(identifier))
                    except KeyError:
                        stored = None
                    if stored is None or not can_read(stored):
                        return JSONResponse({'detail': 'Không tìm thấy hồ sơ trong quyền truy cập của bạn'}, status_code=404)
            if request.method == 'POST':
                from consulting.usage_client import feature_for, with_allowance
                try:
                    inputs = await request.json()
                except Exception:
                    inputs = {}
                feature = feature_for(path, inputs) if isinstance(inputs, dict) else None
                if feature:
                    return await with_allowance(request,call_next,base,authorization,feature,inputs)
            return await call_next(request)
        finally:
            identity.reset(token)
