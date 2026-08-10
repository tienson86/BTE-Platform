# Metrics Guide

Version: 1.0.0  
Sprint: Beta-3

Catalog names are stable. **No instrumentation.** `/metrics` remains reserved (Beta-2).

## API

`request_count` · `request_latency` · `error_rate` · `availability`

## Pipeline

`analysis_duration` · `decision_duration` · `luck_duration` · `interpretation_duration` · `report_duration`

These measure canonical pipeline stages. They must not require engine-internal hooks.

## System

`cpu` · `memory` · `disk` · `network`

Host/container collectors (cAdvisor / Docker) may supply system metrics externally without application code changes.

## Future scrape

When implemented, names in `applications/metrics/` are the contract. Do not rename without an API change policy review.

---

END
