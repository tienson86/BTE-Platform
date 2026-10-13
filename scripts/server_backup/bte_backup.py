"""Online SQLite backups; source databases are opened read-only."""
from contextlib import closing
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile
import time

def backup(root, destination=None):
    root = Path(root).resolve()
    source = Path(os.environ.get('BTE_ANALYSIS_ARCHIVE_PATH') or root/'data'/'analysis_archive.sqlite3').resolve()
    if not source.is_file():
        raise RuntimeError('Không tìm thấy kho hồ sơ: '+str(source))
    target = Path(destination or os.environ.get('BTE_BACKUP_DIR') or root/'data'/'server_backups').resolve()
    target.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    stage = Path(tempfile.mkdtemp(prefix='.pending_', dir=target))
    report = {'created_at':datetime.datetime.now().astimezone().isoformat(), 'databases':[], 'data_files':[]}
    sources = {source}
    try:
        for folder in (root/'data', root/'applications'/'data'):
            if not folder.exists(): continue
            for p in folder.rglob('*'):
                if not p.is_file() or p.is_symlink(): continue
                if any(part in ('server_backups','update_backups') or part.startswith('.pending_') for part in p.relative_to(folder).parts): continue
                if p.resolve().is_relative_to(target): continue
                if p.suffix.lower() in ('.db','.sqlite','.sqlite3'): sources.add(p.resolve())
                elif p.suffix.lower() == '.json':
                    rel=p.relative_to(root)
                    dest=stage/'data_files'/rel
                    dest.parent.mkdir(parents=True,exist_ok=True)
                    shutil.copy2(p,dest)
                    report['data_files'].append(str(rel))
        for index, p in enumerate(sorted(sources)):
            dest=stage/('database_%03d.sqlite3'%index)
            with closing(sqlite3.connect(p.as_uri()+'?mode=ro', uri=True, timeout=30)) as src:
                with closing(sqlite3.connect(dest)) as dst:
                    started=time.monotonic()
                    def progress(status,remaining,total):
                        if time.monotonic()-started>600:
                            raise RuntimeError('Sao lưu vượt 10 phút. Không công bố bản sao chưa hoàn tất.')
                    src.backup(dst, pages=1024, sleep=0.05, progress=progress)
                    integrity=dst.execute('PRAGMA integrity_check').fetchone()[0]
                    if integrity!='ok': raise RuntimeError('Bản sao không toàn vẹn: '+str(p))
                    tables=[r[0] for r in dst.execute("SELECT name FROM sqlite_master WHERE type='table'")]
                    owners=[]
                    if 'analyses' in tables:
                        owners=[{'owner':o,'count':c} for o,c in dst.execute('SELECT owner,COUNT(*) FROM analyses GROUP BY owner')]
            report['databases'].append({'source':str(p),'backup':dest.name,'integrity':'ok','owners':owners,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
        (stage/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        final=target/('BTE_BACKUP_'+stamp)
        stage.rename(final)
        print('BACKUP_OK '+str(final))
        return final
    except Exception:
        shutil.rmtree(stage,ignore_errors=True)
        raise

if __name__=='__main__':
    try:
        root=Path(sys.argv[1]).resolve()
        backup(root, sys.argv[2] if len(sys.argv)>2 else None)
    except Exception as error:
        print('BACKUP_FAILED '+str(error),file=sys.stderr)
        sys.exit(1)
