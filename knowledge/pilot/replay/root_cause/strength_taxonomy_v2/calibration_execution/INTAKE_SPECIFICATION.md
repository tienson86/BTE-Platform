# INTAKE_SPECIFICATION

## Required intake fields

- acquisition_id
- source_type
- source_reference
- received_at
- consent_status
- privacy_status
- birth_date
- birth_time
- birth_place
- timezone
- gender
- calendar_type
- data_precision
- verification_status
- case_status

## Rules

- Prefer anonymized identifiers.
- Do not store unnecessary PII.
- `cal_id` remains null until eligibility passes.
- Template: `templates/intake_record.json`
