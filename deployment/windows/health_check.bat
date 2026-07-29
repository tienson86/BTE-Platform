@echo off
setlocal
set API_URL=http://127.0.0.1:8000/api/v1/health
set ADMIN_URL=http://127.0.0.1:8080/healthz
set PORTAL_URL=http://127.0.0.1:8081/healthz

echo Checking BTE health endpoints...
echo.

curl -fsS "%API_URL%" && echo. && echo [OK] API || echo [FAIL] API
curl -fsS "%ADMIN_URL%" && echo. && echo [OK] Admin || echo [FAIL] Admin
curl -fsS "%PORTAL_URL%" && echo. && echo [OK] Portal || echo [FAIL] Portal

endlocal
