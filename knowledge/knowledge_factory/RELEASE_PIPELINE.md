# Release Pipeline — V1.0

| Field | Value |
|-------|-------|
| Document | RELEASE_PIPELINE |
| Version | 1.0.0 |
| Section | 10 — Release |

---

# 10.1 Purpose

Move **Frozen** knowledge into **Production** and publish a **Release** customers and consultants can rely on.

```text
Frozen catalog
  ↓
Production load (Reasoning)
  ↓
Production smoke
  ↓
Release tag
  ↓
Customer-visible release
```

---

# 10.2 Production stage

| Field | Value |
|-------|-------|
| **Input** | Frozen catalog version |
| **Action** | Production Owner configures Reasoning to load Frozen units |
| **Verify** | Golden cases produce expected unit selection |
| **Owner** | Production Owner |
| **Gate** | QG6 passed (Freeze complete) |

Production Engine implementation is **outside** Factory docs. Factory defines **requirements**:

- Load Frozen catalog version only
- Reject Draft/Reviewed/Validated units in production path
- Log catalog version in audit trail

---

# 10.3 Production smoke tests

Minimum before Release:

| Test | Pass condition |
|------|----------------|
| Golden CASE-0001 | Expected units selectable |
| Duplicate clusters | Representative selection works |
| Missing fact case | Units with unmet required_facts rejected |
| Customer Mode | No FORBIDDEN unit in Customer path |
| Catalog version | Matches release manifest |

---

# 10.4 Release stage

| Field | Value |
|-------|-------|
| **Input** | Production smoke pass |
| **Output** | Release version published |
| **Owner** | Release Manager |
| **Gate** | QG7 |

Release artifacts:

- Release version tag (see VERSIONING)
- Release notes (pack scope, catalog version, known limits)
- Rollback pointer to prior Frozen version

---

# 10.5 Release vs Freeze

| Event | Technical | Business |
|-------|-----------|----------|
| **Freeze** | Catalog immutable | Internal milestone |
| **Production** | Reasoning loads Frozen | Operational |
| **Release** | Tagged and announced | Customer/consultant visible |

A pack may Freeze without immediate Release (staged rollout).

---

# 10.6 Rollback

If production smoke fails post-release:

```text
Production Owner rolls back to prior Frozen catalog version
  ↓
Release Manager communicates if customer-visible
  ↓
Change pipeline for fix (never edit Frozen in place)
```

Detail: [CHANGE_PIPELINE.md](CHANGE_PIPELINE.md).

---

# 10.7 Exit criteria (QG7)

See [CHECKLISTS.md](CHECKLISTS.md) § Release.

---

END
