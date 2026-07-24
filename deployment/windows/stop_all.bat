@echo off
setlocal
echo Stopping BTE uvicorn processes...

REM Stop uvicorn workers started for BTE applications
for /f "tokens=2 delims=," %%P in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH 2^>nul') do (
  wmic process where "ProcessId=%%~P" get CommandLine 2>nul | findstr /I "uvicorn applications.api.app applications.web_admin.app applications.customer_portal.app" >nul
  if not errorlevel 1 (
    echo Killing PID %%~P
    taskkill /PID %%~P /F >nul 2>&1
  )
)

REM Also stop by window titles opened via start_all.bat
taskkill /FI "WINDOWTITLE eq BTE API*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq BTE Web Admin*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq BTE Customer Portal*" /F >nul 2>&1

echo Done.
endlocal
