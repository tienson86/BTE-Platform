# Applications API Endpoints

**Location**

```
knowledge/10_integration_layer/03_API_INTEGRATION/02_ENDPOINTS.md
```

---

# Purpose

This document defines the official public endpoints exposed by the BTE Applications API.

The Applications API is the only entry point for customer-facing applications.

No client shall communicate directly with analytical engines.

---

# Status

Document Type

Architecture Specification

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Architecture

---

# API Principles

The Applications API follows these principles:

- One Public Entry Point
- Engine Isolation
- Stateless
- Versioned
- Deterministic
- Contract First
- Backward Compatible

---

# API Architecture

```
Customer Portal
        │
Mobile App
        │
Public SDK
        │
Third-party Clients
        │
        ▼
=========================
 Applications API
=========================
        │
        ▼
Analyze Pipeline
        │
        ▼
ReportResponse
```

Clients never communicate with:

- Calendar Engine
- BaZi Engine
- Analysis Engine
- Interpretation Engine
- Commercial Knowledge
- Report Builder

---

# API Version

Current

```
/api/v1
```

Future versions

```
/api/v2
```

Major versions never modify existing contracts.

---

# Endpoint Catalog

| Method | Endpoint | Purpose |
|----------|----------|----------|
| POST | `/api/v1/analyze` | Generate ReportResponse |
| GET | `/api/v1/report/{id}` | Retrieve previously generated report |
| GET | `/api/v1/health` | Service health check |
| GET | `/api/v1/version` | API and contract versions |

Future endpoints are additive.

---

# POST /api/v1/analyze

## Purpose

Execute the complete BTE analysis pipeline.

---

## Request

```
AnalyzeRequest
```

Contains

- Customer
- Birth Information
- Calendar Type
- Runtime Options

---

## Processing

```
Validate

↓

Calendar

↓

BaZi

↓

Analysis

↓

Interpretation

↓

Commercial Knowledge

↓

Report Builder

↓

Validation

↓

ReportResponse
```

---

## Success Response

```
HTTP 200

ReportResponse
```

---

## Failure Responses

```
400 Bad Request

422 Unprocessable Entity

500 Internal Server Error
```

---

# GET /api/v1/report/{id}

## Purpose

Retrieve a previously generated report.

---

## Input

```
Report ID
```

---

## Output

```
ReportResponse
```

---

## Failure

```
404 Not Found
```

---

# GET /api/v1/health

## Purpose

Health monitoring.

---

## Output

```
status

uptime

version

dependencies
```

---

## Example

```
{
  "status": "healthy"
}
```

---

# GET /api/v1/version

## Purpose

Expose public version information.

---

## Output

Contains

- API Version
- Report Contract Version
- Commercial Version
- Knowledge Version
- Capability Versions

---

# Request Model

```
AnalyzeRequest

├── customer
├── birth_information
├── options
└── metadata
```

---

# Response Model

```
ReportResponse
```

Defined in

```
01_REPORT_CONTRACT/
```

---

# HTTP Status Codes

| Code | Meaning |
|------|----------|
| 200 | Success |
| 400 | Invalid Request |
| 404 | Resource Not Found |
| 409 | Version Conflict |
| 422 | Invalid Birth Information |
| 500 | Internal Processing Error |
| 503 | Service Unavailable |

---

# Authentication

Current Commercial V1

No authentication defined in this specification.

Future versions may support

- JWT
- OAuth2
- API Keys

Authentication is independent of the Analyze Pipeline.

---

# Idempotency

Analyze requests are deterministic.

The same request shall always produce the same ReportResponse, assuming identical:

- Contract Version
- Knowledge Version
- Runtime Configuration

---

# Error Response

Every error returns

```
ErrorResponse

├── code
├── message
├── details
├── request_id
└── timestamp
```

No internal stack traces shall be exposed.

---

# Rate Limiting

Commercial V1

Not specified.

Future versions may define

- Requests per minute
- Burst limits
- Customer tiers

---

# Compatibility Rules

Applications shall

- Ignore unknown fields
- Use API versioning
- Never depend on field ordering
- Consume only ReportResponse

---

# Forbidden Access

Clients shall never access

- Calendar Engine
- BaZi Engine
- Analysis Engine
- Interpretation Engine
- Commercial Knowledge
- Report Builder
- Rule Database

All access must pass through the Applications API.

---

# Observability

Every request should generate

```
request_id

contract_version

pipeline_version

execution_time

status
```

These values are used for diagnostics and tracing.

---

# API Lifecycle

```
Receive Request

↓

Validate

↓

Execute Analyze Pipeline

↓

Validate ReportResponse

↓

Return Response

↓

Complete Request
```

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_ANALYZE_PIPELINE.md | Request execution flow |
| 02_ENDPOINTS.md | Public API contract (this document) |
| 03_ERROR_HANDLING.md | Error strategy |
| 04_VERSION_NEGOTIATION.md | API compatibility |
| 01_REPORT_RESPONSE_SPEC.md | Response contract |

---

# Acceptance Criteria

The Applications API is accepted when

✓ All public endpoints are documented

✓ Every endpoint has one responsibility

✓ Analyze returns ReportResponse only

✓ Public clients cannot access internal engines

✓ HTTP status codes are standardized

✓ ErrorResponse is standardized

✓ API versioning is defined

✓ Backward compatibility is guaranteed

---

# Official Status

Document

Applications API Endpoints

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Architecture