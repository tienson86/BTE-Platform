# Registry JSON Schema

---

# Purpose

Defines the canonical JSON schema for Registry Records.

This schema is the official data contract used by:

- Registry Loader
- Registry Validator
- Registry API
- Discovery Service
- Runtime Lookup

---

# Root Object

```json
{
  "identity": {},
  "metadata": {},
  "object": {},
  "classification": {},
  "dependencies": [],
  "validation": {},
  "governance": {},
  "traceability": {},
  "revision_history": []
}
```

---

# Identity

```json
{
  "registry_id": "REG-000001",
  "object_id": "KNO-000001",
  "namespace": "knowledge"
}
```

---

# Metadata

```json
{
  "version": "1.0.0",
  "status": "published",
  "owner": "Knowledge Team",
  "created_date": "",
  "updated_date": ""
}
```

---

# Object

```json
{
  "canonical_name": "",
  "object_type": "",
  "uri": "",
  "path": "",
  "checksum": ""
}
```

---

# Classification

```json
{
  "domain": "",
  "category": "",
  "tags": []
}
```

---

# Dependencies

```json
[
    "REG-000021",
    "REG-000044"
]
```

---

# Validation

```json
{
  "schema_valid": true,
  "dependency_valid": true,
  "checksum_valid": true
}
```

---

# Governance

```json
{
  "reviewer": "",
  "approval_status": "approved",
  "next_review": ""
}
```

---

# Traceability

```json
{
  "trace_id": "TRACE-000001",
  "audit_id": "AUD-000001"
}
```

---

# Revision History

```json
[
  {
    "version": "1.0.0",
    "date": "",
    "summary": ""
  }
]
```

---

# Required Fields

Registry ID

Object ID

Namespace

Version

Status

URI

Owner

Trace ID

---

# Validation Rules

Validators shall verify:

- Registry ID format
- Namespace
- URI uniqueness
- Dependency existence
- Checksum integrity
- Version format
- Traceability completeness

---

# Compatibility

PATCH

No schema changes.

MINOR

Optional fields may be added.

MAJOR

Breaking changes permitted.

---

# Future Extensions

- Digital Signature
- Distributed Registry
- Graph Registry
- Semantic Metadata
- API Discovery Metadata