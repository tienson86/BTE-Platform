# Versioning Policy

Version: 1.0.0  
Sprint: Beta-2

## Semantic Versioning

Public product versions follow SemVer: `MAJOR.MINOR.PATCH`.

| Change | SemVer | API mount |
|--------|--------|-----------|
| Bugfix / docs | PATCH | `/api/v1/` unchanged |
| Additive, compatible | MINOR | `/api/v1/` unchanged |
| Breaking contract | MAJOR | new mount, e.g. `/api/v2/` |

Current:

- Product / API semver: `1.0.0`
- Public mount: `/api/v1/`
- Schema version: `1.0.0`

## Backward compatibility (v1)

Allowed:

- New optional request fields
- New response `data` fields
- New endpoints under `/api/v1/`
- New error codes that do not change existing code meaning

Not allowed in v1:

- Removing or renaming fields
- Changing field types
- Changing error code semantics
- Returning engine objects
- Mounting `/api/v2/`

## Breaking changes

A breaking change requires:

1. New major SemVer
2. New mount path
3. Written migration notes
4. Deprecation window on the previous mount

## Deprecation

Deprecated v1 fields or endpoints must remain functional for at least one minor release after announcement. Deprecation is documented in OpenAPI `deprecated: true` and release notes.

## Negotiation

Clients may send `API-Version: v1`.  
Unsupported or reserved versions return `BTE-400-UNSUPPORTED_VERSION`.

---

END
