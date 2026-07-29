# BTE Platform — Windows Deployment

## Prerequisites

- Python 3.11+ (or 3.12)
- Virtualenv recommended: `.venv`
- Dependencies:

```bat
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt -r applications\requirements.txt
```

## Start all services

From repository root:

```bat
deployment\windows\start_all.bat
```

This opens **three separate console windows**:

1. BTE API → http://127.0.0.1:8000/docs  
2. BTE Web Admin → http://127.0.0.1:8080  
3. BTE Customer Portal → http://127.0.0.1:8081  

## Start individually

```bat
deployment\windows\start_api.bat
deployment\windows\start_admin.bat
deployment\windows\start_portal.bat
```

## Stop

```bat
deployment\windows\stop_all.bat
```

## Health check

```bat
scripts\health_check.bat
```

or

```bat
deployment\windows\health_check.bat
```

## Environment

Defaults load from `deployment\env\development.env` when present.

Override examples:

```bat
set BTE_STORAGE_BACKEND=sqlite
set BTE_API_BASE_URL=http://127.0.0.1:8000
set BTE_LOG_LEVEL=INFO
```

## Logs

- `logs\api.log`
- `logs\admin.log`
- `logs\portal.log`
