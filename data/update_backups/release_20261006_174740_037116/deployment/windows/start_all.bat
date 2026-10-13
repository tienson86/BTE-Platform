@echo off
setlocal
set "PYTHONUTF8=1"
cd /d "%~dp0..\.."
if exist ".venv\Scripts\python.exe" (
 ".venv\Scripts\python.exe" -X utf8 "scripts\server_runtime\start_checked.py"
) else (
 python -X utf8 "scripts\server_runtime\start_checked.py"
)
if errorlevel 1 (
 echo BTE chua khoi dong thanh cong. Kiem tra thong bao va nhat ky.
 pause
 exit /b 1
)
echo Da kiem tra API va ket noi Portal. Bao cao: logs\BTE_Khoi_Dong_Da_Kiem_Tra.json
pause
