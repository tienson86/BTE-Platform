@echo off
setlocal
set "PYTHONUTF8=1"
cd /d "%~dp0..\.."
if exist ".venv\Scripts\python.exe" (
 ".venv\Scripts\python.exe" -X utf8 "scripts\server_runtime\bte_maintenance.py" "%CD%"
) else (
 python -X utf8 "scripts\server_runtime\bte_maintenance.py" "%CD%"
)
if errorlevel 1 (
 echo BTE chua khoi dong thanh cong. Giu lai thong bao loi de kiem tra.
 pause
 exit /b 1
)
echo Da sao luu, nap dung ma giao dien va khoi dong lai BTE.
echo Bao cao: logs\BTE_Cap_Nhat_Da_Kiem_Tra.json
pause
