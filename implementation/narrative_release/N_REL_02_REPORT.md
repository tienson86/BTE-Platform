# N-REL-02 DUAL RUN & RELEASE MONITORING REPORT

Sprint: N-REL-02
Module: `engines.narrative_v2.release`
Mode: Production operations (V2 production, Pack05 fallback)
Status: READY FOR PRODUCT OWNER REVIEW

STOP. N-REL-03 was not started.

---

## 1. Status

PASS

The operational monitoring layer can answer whether Narrative V2 should stay switched. CASE-0001 production dual-run is healthy: runtime, Presentation, Portal, export parity, Golden, and Certification are PASS. Fallback count is 0. Pack05 remains the fallback path. Pack05 was not retired. Release was not frozen.

---

## 2. Architecture

```
Narrative V2  → Production
Pack05        → Fallback
ReleaseMonitor → Health / Parity / Alerts / History / Dashboard
```

Location: `engines/narrative_v2/release/`

| File | Role |
| --- | --- |
| `release_monitor.py` | Dual-run observation facade |
| `release_health.py` | `ReleaseHealth` + surface assessment |
| `release_metrics.py` | Operational counters |
| `release_events.py` | Event types (no personal data) |
| `release_history.py` | Append-only log |
| `release_alerts.py` | WARNING / FAIL rules |
| `release_parity.py` | Content hashes for Portal / PDF / DOCX / JSON |
| `release_dashboard.py` | Internal HTML only |
| `release_errors.py` | Typed errors |

Portal production switch from N-REL-01 is unchanged. This sprint observes it.

---

## 3. Release Health

`ReleaseHealth` fields:

| Field | CASE-0001 |
| --- | --- |
| runtime_status | PASS |
| presentation_status | PASS |
| portal_status | PASS |
| export_status | PASS |
| provider | v2 |
| fallback_count | 0 |
| parity_status | PASS |
| golden_status | PASS |
| certification_status | PASS |
| timestamp | 2026-08-30T07:57:50+00:00 |
| overall | PASS |

States: PASS, WARNING, FAIL, UNKNOWN. No extra states.

FAIL wins. Fallback count > 0 raises overall WARNING.

---

## 4. Monitoring

Runtime: Narrative Runtime success, Presentation generation, validation, version `bte.presentation.v2.1`.

Portal: provider, Pack05 vs V2 selection, fallback events, switch events.

Export: content hashes of Narrative strings for Portal, PDF (HTML text), DOCX (paragraphs), JSON. File bytes are not hashed.

No names, birth data, or Narrative prose are stored in events.

---

## 5. Dashboard

Internal only.

`implementation/narrative_release/n_rel_02/release_dashboard.html`

`data-release-dashboard="internal"` · `data-customer-access="false"`

Not mounted on Customer Portal. Shows Runtime, Presentation, Portal, Exports, Fallbacks, Golden, Certification, Health, parity hashes, alerts.

Screenshot: `release_dashboard.png`

---

## 6. Fallback

Tracked:

- automatic fallback (invalid Presentation → Pack05)
- manual rollback (`provider=pack05`)
- provider changes
- timestamp
- reason

CASE-0001 production path: 0 automatic, 0 manual.

Tests cover both automatic WARNING and manual rollback recording.

---

## 7. Parity

Same Presentation → same content hash.

CASE-0001 hash (all four consumers):

`6b8c1b3cd79491ef4d2028e1676ec2e9908a1da94ae2f4afff0a0412e1f12960`

Portal = PDF = DOCX = JSON. matched: true.

---

## 8. Alerts

| Condition | Level |
| --- | --- |
| fallback_count > 0 | WARNING |
| Presentation invalid | FAIL |
| Export parity fail | FAIL |
| Golden mismatch | FAIL |

CASE-0001: no alerts.

---

## 9. CASE-0001

Live luck Canonical Analysis → Narrative Runtime → Presentation v2.1. No hardcoded Narrative.

Production provider = v2. Golden matched. Certification CERTIFIED. Fallback = 0. Overall PASS.

---

## 10. Tests

`py -m pytest tests/narrative_v2/test_release_monitor.py -q`

**10 passed**

- Runtime health
- Presentation health
- Export parity
- Fallback
- Provider
- Dashboard
- Alerts
- History (append-only)

---

## 11. Artifacts

`implementation/narrative_release/n_rel_02/`

| File |
| --- |
| `release_dashboard.png` |
| `release_dashboard.html` |
| `release_health.json` |
| `release_history.json` |
| `parity_hashes.json` |
| `fallback_report.md` |

---

## 12. Out-of-scope

| Item | Status |
| --- | --- |
| No Pack05 retirement | YES |
| No Freeze | YES |
| No Dashboard / card / PDF redesign | YES |
| N-REL-03 Pack05 Retirement | Not started |

---

## 13. Verdict

READY FOR PRODUCT OWNER REVIEW

STOP.

Do not start N-REL-03.

---

## Files changed

Created:

- `engines/narrative_v2/release/*.py`
- `tests/narrative_v2/test_release_monitor.py`
- `implementation/narrative_release/n_rel_02/*`
- `implementation/narrative_release/N_REL_02_REPORT.md`

Modified: none of Customer Portal, Pack05, Narrative Runtime, Presentation contract, Golden freeze files, or Certification records.

Reason: operational dual-run monitoring after the N-REL-01 switch.

Impact: operators can see whether V2 should stay in production. Customers are not exposed to the dashboard. Pack05 remains rollback.

---

## Remaining failures

None in `tests/narrative_v2/test_release_monitor.py`.
