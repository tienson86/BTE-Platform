# Deployment Guide

Version: 1.0.0  
Sprint: Beta-1

---

## Prerequisites

- Docker Engine 24+ and Compose v2  
- Repository checkout at a known git SHA  
- Copied env file **outside git** for beta/production secrets  

---

## Development

```bash
cp deployment/docker/.env.example deployment/docker/.env
docker compose -f deployment/docker/docker-compose.dev.yml --env-file deployment/docker/.env up --build
```

Portal: `http://127.0.0.1:8081` · API: `http://127.0.0.1:8000`

---

## Beta

```bash
cp deployment/docker/.env.production.example /secure/bte-beta.env
# edit secrets offline
docker compose -f deployment/docker/docker-compose.beta.yml --env-file /secure/bte-beta.env up -d --build
```

Ingress: nginx on 80/443 (TLS files mounted; domain **not** hardcoded).

---

## Production

```bash
docker compose -f deployment/docker/docker-compose.production.yml --env-file /secure/bte-prod.env up -d --build
```

Follow [RELEASE_PLAYBOOK.md](./RELEASE_PLAYBOOK.md) (approval gates, smoke, rollback).

---

## Build images only

```bash
docker build -f deployment/docker/Dockerfile.api -t bte-api:1.0.0 .
docker build -f deployment/docker/Dockerfile.portal -t bte-portal:1.0.0 .
docker build -f deployment/docker/Dockerfile.worker -t bte-worker:1.0.0 .
```

---

## Stop / restart

```bash
docker compose -f <compose-file> --env-file <env> stop
docker compose -f <compose-file> --env-file <env> up -d
```

See [OPERATIONS_RUNBOOK.md](./OPERATIONS_RUNBOOK.md).

---

END
