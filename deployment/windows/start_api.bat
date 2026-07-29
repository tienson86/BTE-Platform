@echo off
setlocal
cd /d "%~dp0..\..\.."

if not exist "logs" mkdir logs
if not exist "reports" mkdir reports
if not exist "applications\data" mkdir applications\data

set HOST=127.0.0.1
set PORT=8000
set BTE_LOG_LEVEL=INFO
set BTE_STORAGE_BACKEND=json
set BTE_DATA_DIR=applications\data
set BTE_LICENSE_PATH=applications\data\licenses.json
set BTE_REPORT_PATH=reports

if exist "deployment\env\development.env" (
  for /f "usebackq tokens=1,* delims==" %%A in (`findstr /v /b /c:"#" "deployment\env\development.env"`) do (
    if not "%%A"=="" set "%%A=%%B"
  )
)

echo Starting BTE API on %HOST%:%PORT% ...
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" -m uvicorn applications.api.app:app --host %HOST% --port %PORT% >> "logs\api.log" 2>&1
) else (
  python -m uvicorn applications.api.app:app --host %HOST% --port %PORT% >> "logs\api.log" 2>&1
)
endlocal
