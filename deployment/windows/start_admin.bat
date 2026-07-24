@echo off
setlocal
cd /d "%~dp0..\..\.."

if not exist "logs" mkdir logs

set HOST=127.0.0.1
set PORT=8080
set BTE_API_BASE_URL=http://127.0.0.1:8000
set BTE_LOG_LEVEL=INFO

if exist "deployment\env\development.env" (
  for /f "usebackq tokens=1,* delims==" %%A in (`findstr /v /b /c:"#" "deployment\env\development.env"`) do (
    if not "%%A"=="" set "%%A=%%B"
  )
)
if defined ADMIN_PORT set PORT=%ADMIN_PORT%

echo Starting BTE Web Admin on %HOST%:%PORT% ...
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" -m uvicorn applications.web_admin.app:app --host %HOST% --port %PORT% >> "logs\admin.log" 2>&1
) else (
  python -m uvicorn applications.web_admin.app:app --host %HOST% --port %PORT% >> "logs\admin.log" 2>&1
)
endlocal
