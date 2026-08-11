# EXECUTION_WORKFLOW

```
Intake
  → Source Verification
  → Data Verification
  → Calendar Verification
  → Eligibility
  → Expert-A Review
  → Blinded Expert-B Review
  → Agreement
  → Adjudication when required
  → Calibration Record
```

## Lifecycle states

- `intake_pending`
- `source_verification`
- `data_verification`
- `calendar_verification`
- `eligibility_review`
- `ready_for_expert_a`
- `expert_a_in_progress`
- `expert_a_complete`
- `ready_for_expert_b`
- `expert_b_in_progress`
- `expert_b_complete`
- `agreement_review`
- `adjudication_required`
- `adjudication_complete`
- `calibration_complete`
- `rejected`
- `withdrawn`

## Program states

- `no_data` — valid when no authorized charts are available (current)
- Active cases use lifecycle states above

## CAL ID allocation rule

Do **not** allocate `CAL-*` until a real authorized chart passes intake eligibility.
Next free ID remains `CAL-000008` until then.
