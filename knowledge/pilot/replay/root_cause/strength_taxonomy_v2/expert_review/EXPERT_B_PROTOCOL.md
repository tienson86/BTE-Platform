# Expert-B Protocol

## Role

`EXPERT-B` is an independent second Strength reviewer.  
Do not invent a real person's identity in artifacts.

## Blinding

Expert-B receives only:

- anonymized calibration case ID  
- verified birth data (no PII beyond location/time needed for BaZi)  
- verified four pillars + solar-term verification  
- neutral structural evidence  
- taxonomy definitions + confidence scale  
- review instructions + form  

Expert-B must **not** receive:

- Expert-A classification, confidence, or rationale  
- adjudication / expected taxonomy level  
- runtime strength band or score as a suggested answer  
- prior hypotheses framed as the “correct” explanation  

## Workflow

1. Confirm packet blinding manifest.  
2. Deliver `REVIEW_PACKET.md` + `REVIEW_FORM.md` / `.json`.  
3. Expert completes form independently.  
4. Intake validates completeness (`SUBMITTED` → `VALIDATED` or `REJECTED`).  
5. Only after submission: agreement analysis (future sprint).  
6. Adjudication only if protocol requires it **after** Expert-B exists.

## Allowed review statuses

`PENDING` → `IN_REVIEW` → `SUBMITTED` → `VALIDATED` | `REJECTED`

Initial state for both cases: **PENDING**.
