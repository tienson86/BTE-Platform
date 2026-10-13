"""Local BTE releases: exact-source preflight, backup, asset hashes, restart."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess
import sys
from urllib.parse import parse_qsl, urlencode, urlsplit

def digest(text):
    return hashlib.sha256(text.replace('\r\n','\n').encode('utf-8')).hexdigest()

def version_plans(root):
    portal=root/'applications/customer_portal'
    static=(portal/'static').resolve()
    pattern=re.compile(r'(?P<head>\b(?:src|href)\s*=\s*)(?P<quote>["\'])(?P<url>/static/[^"\'<>\s]+)(?P=quote)', re.I)
    plans=[]
    hashes={}
    for path in (portal/'templates').rglob('*.html'):
        original=path.read_bytes()
        text=original.decode('utf-8-sig')
        def replace(match):
            parts=urlsplit(match['url'])
            if not parts.path.lower().endswith(('.js','.css')): return match[0]
            asset=(static/parts.path.removeprefix('/static/')).resolve()
            if not asset.is_relative_to(static): raise ValueError('Asset path escapes static directory')
            if not asset.is_file(): return match[0]
            if asset not in hashes:
                hashes[asset]=hashlib.sha256(asset.read_bytes()).hexdigest()[:16]
            params=[(k,v) for k,v in parse_qsl(parts.query,keep_blank_values=True) if k!='v']
            params.append(('v','BTE-'+hashes[asset]))
            url=parts.path+'?'+urlencode(params)
            if parts.fragment:url+='#'+parts.fragment
            return match['head']+match['quote']+url+match['quote']
        updated=pattern.sub(replace,text)
        if updated!=text: plans.append((path,original,updated))
    return plans

def backup_data(root):
    script=root/'scripts/server_backup/bte_backup.py'
    if not script.is_file(): raise RuntimeError('Install daily backup step before this release.')
    subprocess.run([sys.executable,'-X','utf8',str(script),str(root)],check=True,cwd=root)

def stop_services(root,script):
    subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(script),'-BteRoot',str(root)],check=True,cwd=root)

def start_services(root):
    script=root/'scripts/server_runtime/start_checked.py'
    if not script.is_file(): raise RuntimeError('Missing verified BTE startup helper')
    subprocess.run([sys.executable,'-X','utf8',str(script)],check=True,cwd=root)

def write_plans(root,plans,backup_dir,originals):
    for path,original,text in plans:
        if path not in originals:
            originals[path]=original
            if original is not None:
                dest=backup_dir/path.relative_to(root)
                dest.parent.mkdir(parents=True,exist_ok=True)
                dest.write_bytes(original)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(text,encoding='utf-8',newline='\n')

def rollback(originals):
    for path,original in reversed(list(originals.items())):
        if original is None:path.unlink(missing_ok=True)
        else:path.write_bytes(original)

def package_plans(root,package):
    manifest=json.loads((package/'manifest.json').read_text(encoding='utf-8-sig'))
    plans=[]
    seen=set()
    for item in manifest['files']:
        target=(root/item['path']).resolve()
        source=(package/item['payload']).resolve()
        if not target.is_relative_to(root) or not source.is_relative_to(package): raise ValueError('Invalid release path')
        if target in seen:raise ValueError('Duplicate release target')
        seen.add(target)
        updated=source.read_text(encoding='utf-8-sig')
        if digest(updated)!=item['after_sha256']:raise ValueError('Release payload checksum does not match: '+item['path'])
        original=target.read_bytes() if target.exists() else None
        current=digest(original.decode('utf-8-sig')) if original is not None else None
        if current==item['after_sha256']:continue
        if current!=item['before_sha256']:raise ValueError('Source differs from reviewed release: '+item['path']+'. No files changed.')
        if target.suffix=='.py':
            import ast
            ast.parse(updated,filename=str(target))
        plans.append((target,original,updated))
    return manifest['release_id'],plans

def run(root,package=None,stop_script=None):
    root=Path(root).resolve()
    if not (root/'applications/customer_portal').is_dir():raise ValueError('Invalid BTE root')
    release,plans=package_plans(root,Path(package).resolve()) if package else ('restart',[])
    # Check all release targets before backup or stopping any process.
    backup_data(root)
    stop_script=Path(stop_script) if stop_script else root/'scripts/server_runtime/bte_stop_checked.ps1'
    stop_services(root,stop_script)
    folder=root/'data/update_backups'/('release_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    folder.mkdir(parents=True)
    originals={}
    try:
        write_plans(root,plans,folder,originals)
        versions=version_plans(root)
        write_plans(root,versions,folder,originals)
        start_services(root)
    except Exception:
        rollback(originals)
        print('RELEASE_FAILED: source edits rolled back. Data backup retained. Services are not assumed ready.')
        raise
    report={'release_id':release,'completed_at':datetime.datetime.now().astimezone().isoformat(),
            'source_files_changed':len(plans),'template_versions_changed':len(versions),
            'source_backup':str(folder),'api_and_portal_ready':True}
    (root/'logs/BTE_Cap_Nhat_Da_Kiem_Tra.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('RELEASE_OK: backed up, asset versions refreshed, API and Portal ready.')

if __name__=='__main__':
    try:
        root=Path(sys.argv[1])
        package=Path(sys.argv[2]) if len(sys.argv)>2 else None
        run(root,package)
    except Exception as error:
        print('MAINTENANCE_FAILED: '+str(error))
        sys.exit(1)
