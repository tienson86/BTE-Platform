"""Start one local API and Portal, after checking ports and API readiness."""
from pathlib import Path
import datetime
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request

def free(port):
    with socket.socket() as s:
        try: s.bind(('127.0.0.1', port)); return True
        except OSError: return False

def wait_json(url, process, required=None):
    deadline=time.monotonic()+45
    while time.monotonic()<deadline:
        if process.poll() is not None: raise RuntimeError('Dịch vụ đã dừng. Xem nhật ký trong thư mục logs.')
        try:
            with urllib.request.urlopen(url,timeout=2) as response: data=json.load(response)
            if required and not all(p in data.get('paths',{}) for p in required):
                raise RuntimeError('API đang chạy thiếu các route bắt buộc. Dừng để kiểm tra mã nguồn.')
            return
        except RuntimeError: raise
        except Exception: time.sleep(0.5)
    raise RuntimeError('Dịch vụ chưa sẵn sàng sau 45 giây. Xem nhật ký, không tiếp tục báo thành công.')

def main():
    root=Path(__file__).resolve().parents[2]
    env=os.environ.copy()
    env.update(PYTHONUTF8='1',BTE_LOG_LEVEL='INFO',BTE_STORAGE_BACKEND='json',
               BTE_DATA_DIR=str(root/'applications'/'data'),BTE_LICENSE_PATH=str(root/'applications'/'data'/'licenses.json'),
               BTE_REPORT_PATH=str(root/'reports'),PORT='8000',PORTAL_PORT='8686')
    config=root/'deployment'/'env'/'development.env'
    if config.exists():
        for line in config.read_text(encoding='utf-8-sig').splitlines():
            if not line.strip() or line.lstrip().startswith('#') or '=' not in line: continue
            key,value=line.split('=',1)
            env[key.strip()]=value.strip()
    api_port=int(env['PORT']);portal_port=int(env['PORTAL_PORT'])
    if api_port==portal_port: raise RuntimeError('API và Portal không được dùng chung cổng.')
    for port in (api_port,portal_port):
        if not free(port): raise RuntimeError('Cổng '+str(port)+' đang được sử dụng. Đóng cửa sổ BTE cũ rồi thử lại; không tự kết thúc tiến trình khác.')
    env['BTE_API_BASE_URL']='http://127.0.0.1:'+str(api_port)
    (root/'logs').mkdir(exist_ok=True)
    (root/'reports').mkdir(exist_ok=True)
    (root/'applications'/'data').mkdir(parents=True,exist_ok=True)
    python=root/'.venv'/'Scripts'/'python.exe'
    if not python.exists(): python=Path(sys.executable)
    started=[]
    def launch(module,port,log):
        with (root/'logs'/log).open('ab') as handle:
            handle.write(('\nBTE_START '+datetime.datetime.now().isoformat()+' module='+module+' port='+str(port)+'\n').encode())
            handle.flush()
            process=subprocess.Popen([str(python),'-X','utf8','-m','uvicorn',module,'--host','127.0.0.1','--port',str(port),'--log-level','info'],cwd=root,env=env,stdout=handle,stderr=subprocess.STDOUT,creationflags=getattr(subprocess,'CREATE_NEW_CONSOLE',0))
        started.append(process)
        return process
    try:
        api=launch('applications.api.app:app',api_port,'api_checked.log')
        wait_json('http://127.0.0.1:'+str(api_port)+'/openapi.json',api,
                  ['/api/v1/auth/login','/api/v1/analyze','/api/v1/analysis-archive'])
        portal=launch('applications.customer_portal.app:app',portal_port,'portal_checked.log')
        # Test the Portal's API proxy, not only the separate API port.
        wait_json('http://127.0.0.1:'+str(portal_port)+'/backend/openapi.json',portal,
                  ['/api/v1/auth/login','/api/v1/analysis-archive'])
        report={'checked_at':datetime.datetime.now().astimezone().isoformat(),'root':str(root),
                'api_pid':api.pid,'portal_pid':portal.pid,'api_port':api_port,'portal_port':portal_port,
                'api_ready':True,'portal_proxy_ready':True,'auth_store_source':'applications/api/auth/store.py'}
        (root/'logs'/'BTE_Khoi_Dong_Da_Kiem_Tra.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        # Keep additional services on their existing scripts and configuration.
        for script,port in [('start_admin.bat',8688),('start_marriage.bat',8082)]:
            path=root/'deployment'/'windows'/script
            if path.exists() and free(port):
                subprocess.Popen(['cmd','/c',str(path)],cwd=root,env=env,creationflags=getattr(subprocess,'CREATE_NEW_CONSOLE',0))
        print('API sẵn sàng; Portal kết nối đúng API. Nhật ký: logs\\api_checked.log và logs\\portal_checked.log')
        print('Các dịch vụ phụ vẫn dùng tệp khởi động riêng; chưa nghiệm thu trong bước này.')
        print('Mở: http://127.0.0.1:'+str(portal_port)+'/login')
    except Exception:
        for process in reversed(started):
            if process.poll() is None:
                process.terminate()
                try: process.wait(timeout=10)
                except subprocess.TimeoutExpired: process.kill()
        raise

if __name__=='__main__':
    try: main()
    except Exception as error:
        print('START_FAILED '+str(error))
        sys.exit(1)
