# Scaling Guide

Version: 1.0.0  
Sprint: Beta-1

---

## Vertical

Increase CPU/memory for `api` first (analysis is CPU-bound). Portal is lighter.

## Horizontal

- **Portal**: stateless → scale replicas behind nginx `least_conn`.  
- **API**: scale only if storage backend is shared and safe; JSON file backend is **single-writer**. Default Beta-1: **one API replica**.  
- **Nginx**: one replica sufficient until TLS termination moves to a load balancer.  
- **Worker**: reserved — do not scale.

## Autoscale

Not enabled. Document thresholds later: CPU > 70% for 10m → page ops; do not auto-scale API on JSON storage.

---

END
