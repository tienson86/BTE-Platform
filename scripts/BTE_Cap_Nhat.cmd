@echo off
setlocal
set "PYTHONUTF8=1"
cd /d "%~dp0.."
if "%~1"=="" (
 echo Can chi dinh thu muc goi cap nhat co manifest.json.
 pause
 exit /b 1
)
if exist ".venv\Scripts\python.exe" (
 ".venv\Scripts\python.exe" -X utf8 "scripts\server_runtime\bte_maintenance.py" "%CD%" "%~f1"
) else (
 python -X utf8 "scripts\server_runtime\bte_maintenance.py" "%CD%" "%~f1"
)
pause
