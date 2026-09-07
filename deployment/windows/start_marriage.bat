@echo off
setlocal
cd /d "%~dp0..\..\.."

if not exist "logs" mkdir logs

set HOST=127.0.0.1
set PORT=8082
set BTE_LOG_LEVEL=INFO

if exist "deployment\env\development.env" (
  for /f "usebackq tokens=1,* delims==" %%A in (`findstr /v /b /c:"#" "deployment\env\development.env"`) do (
    if not "%%A"=="" set "%%A=%%B"
  )
)
if defined BTE_MARRIAGE_PORT set PORT=%BTE_MARRIAGE_PORT%

echo Starting BTE Marriage Public API on %HOST%:%PORT% ...
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" -m uvicorn consulting.marriage.api.http:create_marriage_api_app --factory --host %HOST% --port %PORT% >> "logs\marriage_api.log" 2>&1
) else (
  python -m uvicorn consulting.marriage.api.http:create_marriage_api_app --factory --host %HOST% --port %PORT% >> "logs\marriage_api.log" 2>&1
)
endlocal
