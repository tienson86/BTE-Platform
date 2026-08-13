# BETA_PROTOCOL

| Field | Value |
|-------|-------|
| Program | RC3 Internal Beta |
| Status | **FROZEN** |

Do not rewrite pipeline output to please a participant.

---

## Official workflow

```text
Invite (persona match)
    ↓
Consent + context (reader role, package)
    ↓
Run frozen production path once
    ↓
Deliver customer Mode only
    ↓
Feedback form (same sitting)
    ↓
Score commercial metrics
    ↓
Triage issues
    ↓
Do not fix during the session
```

---

## Session rules

| Rule | Detail |
|------|--------|
| One chart | No second birth date “to make it nicer” |
| One reader | SELF or PARENT as bound |
| No coaching the form | Facilitator may clarify words, not suggest scores |
| No live rewrite | Output is as produced |
| Timebox | 45–75 minutes including read + form |
| Language | Vietnamese customer bodies; form may be VI or EN |

---

## Facilitator script (short)

1. This is a consulting report, not a fortune or medical document.  
2. Some limits are stated on purpose.  
3. Score what you received, not what you wish existed.  
4. You may stop at any time.

---

## Capture

| Artifact | Store |
|----------|-------|
| Form | Dated copy per CASE_id (offline or later `knowledge/beta/RC3/forms/` — not created until first session) |
| Metric row | [COMMERCIAL_METRICS.md](COMMERCIAL_METRICS.md) snapshot at close |
| Defects | [ISSUE_TRIAGE.md](ISSUE_TRIAGE.md) |

Do not put raw PII in git.

---

## After each session

1. Check CASE_0001 freeze still respected (if any follow-up engineering is later proposed).  
2. File issues with one quality category (see Quality Gate backlog).  
3. Do not start an engine change inside RC3.

---

END
