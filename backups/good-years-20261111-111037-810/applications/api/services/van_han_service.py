"""Vận hạn reads canonical saved BTE truth; results are stored only in SQLite."""
from datetime import datetime,timezone
import json
from uuid import uuid4
from applications.api.services.analysis_archive import _connect
from applications.api.services.van_han_core import build, validate

def profile_from_snapshot(snapshot):
    data=snapshot.get('data') or {};inputs=snapshot.get('input') or {}
    bazi=data.get('bazi') or {};calendar=data.get('calendar') or {};useful=data.get('useful_god') or {}
    if not useful.get('success') or useful.get('overall_incomplete'):
        raise ValueError('Hồ sơ chưa có Dụng thần đầy đủ; cần chạy lại lá số trước khi tính vận hạn.')
    def elements(roles,gods):
        from engines.bazi_engine.ten_god import stem_element
        result={r.get('element') for r in roles if r.get('element')}
        if not result:result={stem_element(s) for s in gods if stem_element(s)}
        return sorted(result)
    pillars={}
    for key in ('year','month','day','hour'):
        p=bazi.get(key+'_pillar') or {}
        pillars[key]=p.get('ganzhi') or (str(p.get('stem') or '')+' '+str(p.get('branch') or '')).strip()
    luck=data.get('luck') or {}
    profile={'name':inputs.get('full_name') or 'Chưa đặt tên', 'gender':inputs.get('gender') or bazi.get('gender'),
             'lunar_birth_year':calendar.get('lunar_year') or (calendar.get('lunar') or {}).get('year'),
             'pillars':pillars,'strength':(data.get('strength') or {}).get('reasoning') or '',
             'useful':{'element':useful.get('useful_element'),'stem':useful.get('useful_stem'),
                       'favorable':elements(useful.get('favorable_roles') or [],useful.get('favorable_gods') or []),
                       'unfavorable':elements(useful.get('unfavorable_roles') or [],useful.get('unfavorable_gods') or [])},
             'cycles':luck.get('cycles') or [],'cycle_precision':luck.get('precision') or 'unknown',
             'climate_element':useful.get('climate_element'), 'source_palace':calendar.get('cung_phi')}
    validate(profile)
    from engines.calendar_engine.cung_phi import calculate_cung_phi
    palace=calculate_cung_phi(year=profile['lunar_birth_year'],gender=profile['gender']).cung_phi
    if profile['source_palace'] and palace != profile['source_palace']:
        raise ValueError('Cung phi nguồn khác bảng tính hiện tại. Cần kiểm tra phiên bản trước khi tính vận hạn.')
    return profile

def ensure_table(conn):
    conn.execute('CREATE TABLE IF NOT EXISTS van_han_results (owner TEXT NOT NULL,id TEXT NOT NULL,saved_at TEXT NOT NULL,snapshot TEXT NOT NULL,PRIMARY KEY(owner,id))')

def calculate(snapshot,start,end):
    profile=profile_from_snapshot(snapshot)
    result=build(profile,start,end)
    result.update(profile=profile,source_analysis_id=snapshot.get('analysis_id') or snapshot.get('id'),
                  status='INITIAL_RELEASE', scope_note='Đối chiếu cung phi, Can Chi và Dụng/Hỷ/Kỵ thần, lục hợp/lục xung. Các quan hệ hình/hại/phá và điều kiện hợp hóa chưa được dùng để kết luận trong bản này.')
    return result

def save_result(user,result):
    identifier='VH-'+uuid4().hex;now=datetime.now(timezone.utc).isoformat()
    row={'id':identifier,'created_at':now,'saved_at':now,'owner_user_id':user.user_id,
         'creator_username':user.username,'creator_display_name':user.display_name,
         'result':result}
    with _connect() as conn:
        ensure_table(conn)
        conn.execute('INSERT INTO van_han_results VALUES(?,?,?,?)',('user:'+user.user_id,identifier,now,json.dumps(row,ensure_ascii=False)))
    return row

def get_result(owner,identifier,admin=False):
    with _connect() as conn:
        ensure_table(conn)
        if admin:rows=conn.execute('SELECT snapshot FROM van_han_results WHERE id=?',(identifier,)).fetchall()
        else:rows=conn.execute('SELECT snapshot FROM van_han_results WHERE owner=? AND id=?',(owner,identifier)).fetchall()
    if len(rows)!=1:return None
    return json.loads(rows[0][0])

def list_results(owner,admin=False):
    with _connect() as conn:
        ensure_table(conn)
        query="SELECT id,saved_at,json_extract(snapshot,'$.result.name'),json_extract(snapshot,'$.creator_username'),json_extract(snapshot,'$.creator_display_name') FROM van_han_results"
        rows=conn.execute(query+('' if admin else ' WHERE owner=?')+' ORDER BY saved_at DESC',() if admin else (owner,)).fetchall()
    return [{'id':r[0],'created_at':r[1],'name':r[2],'creator_username':r[3],'creator_display_name':r[4]} for r in rows]
