"""Small searchable server-side source metadata; chart payloads stay in analyses."""
import json
import unicodedata
from datetime import date

def folded(value):
    return ' '.join(''.join(c for c in unicodedata.normalize('NFD',str(value or '').casefold().replace('đ','d'))
                            if unicodedata.category(c)!='Mn').split())

def create_index(conn):
    conn.execute('CREATE TABLE IF NOT EXISTS van_han_source_index (owner TEXT NOT NULL,id TEXT NOT NULL,saved_at TEXT NOT NULL,name TEXT NOT NULL,normalized_name TEXT NOT NULL,birth_date TEXT,birth_time TEXT,gender TEXT,PRIMARY KEY(owner,id))')
    conn.execute('CREATE INDEX IF NOT EXISTS vh_source_owner_date ON van_han_source_index(owner,saved_at DESC)')
    conn.execute('CREATE TRIGGER IF NOT EXISTS vh_source_after_delete AFTER DELETE ON analyses BEGIN DELETE FROM van_han_source_index WHERE owner=OLD.owner AND id=OLD.id; END')

def index_row(conn,owner,row):
    inputs=row.get('input') or {};birthday='';time=''
    try:birthday=date(int(inputs['year']),int(inputs['month']),int(inputs['day'])).isoformat()
    except (KeyError,TypeError,ValueError):pass
    try:
        if inputs.get('hour') is not None:
            hour,minute=int(inputs['hour']),int(inputs.get('minute') or 0)
            if 0<=hour<24 and 0<=minute<60:time=f'{hour:02d}:{minute:02d}'
    except (TypeError,ValueError):pass
    identifier=str(row.get('analysis_id') or row.get('id'))
    name=str(inputs.get('full_name') or 'Chưa đặt tên')
    conn.execute('INSERT OR IGNORE INTO van_han_source_index VALUES(?,?,?,?,?,?,?,?)',
                 (owner,identifier,str(row.get('saved_at') or row.get('created_at') or ''),name,folded(name),birthday,time,str(inputs.get('gender') or '')))

def backfill(conn):
    create_index(conn)
    # Read full payloads only for records not yet indexed; subsequent searches read metadata.
    cursor=conn.execute('SELECT a.owner,a.id,a.saved_at,a.snapshot FROM analyses a WHERE NOT EXISTS (SELECT 1 FROM van_han_source_index i WHERE i.owner=a.owner AND i.id=a.id)')
    for owner,identifier,saved_at,raw in cursor:
        row=dict(json.loads(raw),id=identifier,analysis_id=identifier,saved_at=saved_at)
        index_row(conn,owner,row)

def search(conn,owner,admin=False,q='',limit=30,offset=0,identifier='',source_owner=''):
    backfill(conn)
    clauses=[];params=[]
    if not admin:clauses.append('owner=?');params.append(owner)
    if source_owner:clauses.append('owner=?');params.append(source_owner)
    if identifier:clauses.append('id=?');params.append(identifier)
    for token in folded(q).split():
        literal=token.replace('\\','\\\\').replace('%','\\%').replace('_','\\_')
        clauses.append("normalized_name LIKE ? ESCAPE '\\'");params.append('%'+literal+'%')
    where=(' WHERE '+' AND '.join(clauses)) if clauses else ''
    total=conn.execute('SELECT count(*) FROM van_han_source_index'+where,params).fetchone()[0]
    rows=conn.execute('SELECT owner,id,saved_at,name,birth_date,birth_time,gender FROM van_han_source_index'+where+
                      ' ORDER BY saved_at DESC,id DESC LIMIT ? OFFSET ?',[*params,limit,offset]).fetchall()
    return rows,total
