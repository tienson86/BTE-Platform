@echo off
setlocal
cd /d "%~dp0"

echo ========================================
echo  BTE Platform — starting all services
echo ========================================

if not exist "..\..\logs" mkdir "..\..\logs"
if not exist "..\..\reports" mkdir "..\..\reports"
if not exist "..\..\applications\data" mkdir "..\..\applications\data"

start "BTE API" cmd /k "%~dp0start_api.bat"
timeout /t 2 /nobreak >nul
start "BTE Web Admin" cmd /k "%~dp0start_admin.bat"
timeout /t 1 /nobreak >nul
start "BTE Customer Portal" cmd /k "%~dp0start_portal.bat"

echo.
echo Started:
echo   API     http://127.0.0.1:8000/docs
echo   Admin   http://127.0.0.1:8080
echo   Portal  http://127.0.0.1:8081
echo.
echo Logs: logs\api.log , logs\admin.log , logs\portal.log
echo Use stop_all.bat to stop uvicorn processes.
endlocal
