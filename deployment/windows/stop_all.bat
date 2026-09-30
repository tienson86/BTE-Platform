@echo off
setlocal
echo Stopping BTE uvicorn processes...

REM These ports are reserved for the local BTE stack. Stopping by listening port
REM avoids deprecated WMIC and does not require access to process command lines.
for %%R in (8000 8080 8081 8082 8686) do (
  for /f "tokens=5" %%P in ('netstat -ano ^| findstr /R /C:":%%R .*LISTENING" 2^>nul') do (
    if not "%%P"=="0" (
      echo Killing PID %%P on port %%R
      taskkill /PID %%P /F >nul 2>&1
    )
  )
)

REM Also stop by window titles opened via start_all.bat
taskkill /FI "WINDOWTITLE eq BTE API*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq BTE Web Admin*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq BTE Customer Portal*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq BTE Marriage API*" /F >nul 2>&1

echo Done.
endlocal
