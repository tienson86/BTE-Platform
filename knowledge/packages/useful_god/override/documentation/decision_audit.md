# Decision Audit

Every run publishes `decision_audit`:

| Field | Meaning |
|-------|---------|
| `audit_id` | Stable audit identifier |
| `legality` | `pass` / `rejected` / `applied` |
| `upstream_untouched` | Always true |
| `new_outputs_only` | Always true |
| `prohibition_checked` | Prohibition catalog evaluated |
| `exceptional_condition` | Exception type or null |
| `override_applied` | Boolean |
| `reason_codes` | Structured codes |

`decision_trace` records eligibility → prerequisites → prohibition → exception → typed override → publication, activated rule ids, and the passthrough or replaced final decision.
