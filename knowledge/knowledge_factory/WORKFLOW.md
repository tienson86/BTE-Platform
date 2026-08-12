# Workflow — V1.0

| Field | Value |
|-------|-------|
| Document | WORKFLOW |
| Version | 1.0.0 |

---

# 1. Operational workflow (single pack)

```text
┌─────────────────────────────────────────────────────────────┐
│ QG0  Charter → Chief Reviewer approves pack scope           │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ QG1  Author writes Library → Domain Reviewer approves       │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ QG2  Author builds Catalog (Draft) → Domain Reviewer sign-off │
└────────────────────────────┬────────────────────────────────┘
                             ▼
        ┌────────────────────┴────────────────────┐
        ▼  (repeat per topic)                     │
┌───────────────────┐                             │
│ QG3  QA phase     │                             │
│ QG4  Review        │◄────────────────────────────┘
└─────────┬─────────┘
          ▼
┌─────────────────────────────────────────────────────────────┐
│ QG5  Validation (golden alignment) → Validated              │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ QG6  Freeze → Chief Reviewer → Frozen catalog               │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ Production load → Production Owner smoke                    │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ QG7  Release → Release Manager                              │
└─────────────────────────────────────────────────────────────┘
```

---

# 2. Daily operations

| Activity | Role | Frequency |
|----------|------|-----------|
| Author new topic | Knowledge Author | Per sprint |
| Catalog extraction | Author + Cursor | After library topic ready |
| QA phase | QA Assistant | Per catalog topic complete |
| Review sign-off | Domain Reviewer | After each QA phase |
| REVIEW triage | Author + Domain Reviewer | Weekly during QA |
| Validation | Domain Reviewer | Per pack or per golden update |
| Metrics update | Release Manager | Weekly |

---

# 3. Parallel tracks

Allowed:

- Author catalog topic B while QA runs on topic A
- Cursor assists QA while Author fixes REVIEW on prior topic

Forbidden:

- Validation before Review
- Freeze before Validation
- Production before Freeze
- Release before production smoke

---

# 4. Escalation workflow

```text
Issue detected
  ↓
Classify: QA / Golden / Cross-pack / Schema / Safety
  ↓
QA issue → Author fix → re-QA
Golden issue → Reasoning gov + Domain Reviewer
Cross-pack → Chief Reviewer + pack owners
Safety → Hold Validated; Chief Reviewer
  ↓
Document in phase review or change request
```

---

# 5. Change workflow (post-release)

See [CHANGE_PIPELINE.md](CHANGE_PIPELINE.md).

Never bypass factory gates for “small fixes”.

---

# 6. Tooling (future)

| Tool | Factory stage |
|------|---------------|
| Catalog validator | QG2 |
| QA record database | QG3 |
| Golden diff checker | QG5 |
| Production manifest | QG7 |

V1.0 uses markdown artifacts. Workflow unchanged when tooling added.

---

END
