# Adjudication Module (PILOT-1E-B)

**Scope:** Agreement analysis + adjudication records for dual-reviewed calibration cases.  
**In this sprint:** CAL-000001, CAL-000006 only.

## Rules

- Preserve Expert-A and Expert-B separately.  
- Never overwrite source reviews.  
- Adjudicate only when protocol requires it.  
- Do not invent consensus or adjudicated labels when `NOT_REQUIRED`.  
- Do not promote to Released Golden Dataset.

## Layout

| Path | Role |
|---|---|
| `ADJUDICATION_PROTOCOL.md` | When / how to adjudicate |
| `AGREEMENT_RESULTS.md` | Expert agreement results (n=2) |
| `CASE_000001_ADJUDICATION.json` | Per-case adjudication status |
| `CASE_000006_ADJUDICATION.json` | Per-case adjudication status |
| `validation/` | Integrity checks |
