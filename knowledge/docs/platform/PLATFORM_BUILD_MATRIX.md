# Platform Build Matrix

| Field | Value |
|-------|-------|
| **Document** | PLATFORM_BUILD_MATRIX |
| **Platform version** | 1.0.0 |
| **Status** | Canonical |
| **Owner** | Release Manager |

AF-1 does not introduce new build tooling. This matrix records freeze-relevant surfaces.

---

## Runtime / language

| Surface | Baseline |
|---------|----------|
| Language | Python 3 (repository virtualenv) |
| App API | `applications/api`, companion `api/` |
| Portal | `applications/customer_portal` |
| Knowledge consoles | `applications/knowledge_console`, `applications/validation_console` |

---

## Install / lockfiles

| Artifact | Role |
|----------|------|
| `requirements.txt` | Runtime dependencies (no AF-1 additions) |
| `requirements-dev.txt` | Dev / test dependencies |
| `docker/` `deployment/` | Packaging / deploy assets (unchanged by AF-1) |

New third-party dependencies require explicit product request and are not part of this freeze sprint.

---

## Buildable products (v1.0 architecture)

| Product | Consumes | Notes |
|---------|----------|-------|
| Analysis service | Calendar, Bazi, Analysis, Decision | Canonical pipelines |
| Full consult stack | + Luck, Interpretation, Report | Official v1.0 path |
| Knowledge generator | Profiles + templates | Authoring only |
| Portal | API contracts | Presentation; no engine internals |

---

## Non-build (documentation-only AF-1)

| Path | Role |
|------|------|
| `knowledge/docs/platform/` | Freeze docs |
| `knowledge/governance/architecture/ADR/` | ADRs |
| `knowledge/releases/v1.0/` | Seal artifacts |

These paths are not compiled and must not contain runtime logic.

---

## Renderer build note

RE-3 renderers emit in-memory envelopes. They are not standalone native PDF/DOCX writer products and do not require extra native SDKs for the v1.0 freeze identity.
