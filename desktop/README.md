# BTE Platform — Desktop Runtime (WP19)

Visual / desktop edition entry. **Does not modify Engines, Knowledge, or Rule Database.**

## One command

From the repository root:

```bash
python runtime/start.py
```

Or via launcher:

```bash
python launcher/run_bte.py
```

This will:

1. Check Python (≥ 3.10)
2. Check required packages
3. Check `VERSION` + `configs/services.json`
4. Start **API** (`:8000`)
5. Start **Web Admin** (`:8080`)
6. Start **Customer Portal** (`:8081`)
7. Wait until health checks pass
8. Open **http://localhost:8081** in your browser

On success you should see:

```text
BTE Platform 1.0.0
API    http://127.0.0.1:8000
Admin  http://127.0.0.1:8080
Portal http://127.0.0.1:8081
READY
```

## Status

```bash
python runtime/status.py
```

Shows each service as **Running** or **Down** (with reason if down).

## Stop

```bash
python runtime/stop.py
```

Stops all managed processes (PID files under `runtime/run/`).

## Logs

Service logs are written to:

```text
runtime/logs/
  api.log
  web_admin.log
  customer_portal.log
```

## URLs

| Service | URL |
|---------|-----|
| Customer Portal | http://localhost:8081 |
| Web Admin | http://localhost:8080 |
| API docs | http://127.0.0.1:8000/docs |

## Prerequisites

```bash
pip install -r requirements.txt -r applications/requirements.txt
```

Use the same Python interpreter / venv you use for the project.

## Scope

| Allowed | Not in WP19 |
|---------|-------------|
| Runtime / launcher / desktop docs | Engine changes |
| Process start/stop/status | Knowledge / Rule DB edits |
| Browser open to Portal | API or UI business logic changes |
