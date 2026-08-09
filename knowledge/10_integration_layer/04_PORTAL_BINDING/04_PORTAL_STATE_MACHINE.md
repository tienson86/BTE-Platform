# Portal Runtime State Machine

**Location**

```
knowledge/10_integration_layer/04_PORTAL_BINDING/04_PORTAL_STATE_MACHINE.md
```

---

# Purpose

This document defines the canonical runtime state machine of the BTE Customer Portal.

The Portal shall be driven by a finite state machine rather than multiple independent boolean flags.

This guarantees deterministic rendering, predictable transitions, and consistent customer experience.

---

# Status

Document Type

Architecture Specification

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Product Architecture

---

# Design Principles

The Portal Runtime State Machine follows these principles.

- One active state at any time
- Explicit transitions
- Deterministic rendering
- Stateless UI components
- One-way state flow
- No conflicting UI states

---

# Runtime State Machine

```
                    START
                      │
                      ▼
                   IDLE
                      │
          Click Analyze
                      │
                      ▼
                SUBMITTING
                      │
          Request Accepted
                      │
                      ▼
                PROCESSING
                      │
          Pipeline Finished
          │               │
          │               │
          ▼               ▼
     RENDERING         ERROR
          │               │
          ▼               │
         READY            │
          │               │
          └──── Retry ────┘
```

---

# Runtime States

The Portal defines six runtime states.

| State | Description |
|--------|-------------|
| IDLE | Waiting for customer input |
| SUBMITTING | Sending request |
| PROCESSING | Analyze Pipeline running |
| RENDERING | Building ViewModel and rendering |
| READY | Report fully available |
| ERROR | Request failed |

Exactly one state may be active.

---

# State — IDLE

Purpose

Portal is ready for customer input.

Visible

- Input Form
- Analyze Button

Hidden

- Result Page
- Error Banner
- Loading Overlay

Allowed Transition

```
IDLE

↓

SUBMITTING
```

---

# State — SUBMITTING

Purpose

Request is being sent.

Behavior

- Disable Analyze button
- Prevent duplicate submission
- Display immediate feedback

Allowed Transition

```
SUBMITTING

↓

PROCESSING
```

Failure

```
SUBMITTING

↓

ERROR
```

---

# State — PROCESSING

Purpose

Analyze Pipeline is executing.

Visible

- Loading Screen
- Progress Indicator
- Skeleton Layout

Hidden

- Result Content

Allowed Transition

```
PROCESSING

↓

RENDERING
```

Failure

```
PROCESSING

↓

ERROR
```

---

# State — RENDERING

Purpose

Transform ReportResponse into ViewModel.

Activities

- Portal Adapter
- ViewModel Factory
- Visibility Policy
- Component Tree

Allowed Transition

```
RENDERING

↓

READY
```

Failure

```
RENDERING

↓

ERROR
```

---

# State — READY

Purpose

Final consulting report is visible.

Visible

- Hero
- Executive Summary
- Identity
- Recommendations
- Domain Cards
- Evidence
- Charts

Hidden

- Loading Overlay

Allowed Transition

```
READY

↓

SUBMITTING
```

(New analysis)

---

# State — ERROR

Purpose

An unrecoverable failure occurred.

Visible

- Friendly Error Message
- Retry Button

Hidden

- Partial Report
- Broken Components

Allowed Transition

```
ERROR

↓

SUBMITTING
```

(Retry)

---

# Transition Rules

Only the following transitions are valid.

```
IDLE

↓

SUBMITTING

↓

PROCESSING

↓

RENDERING

↓

READY
```

Error transitions

```
SUBMITTING

↓

ERROR

PROCESSING

↓

ERROR

RENDERING

↓

ERROR
```

All other transitions are invalid.

---

# State Ownership

| State | Owner |
|--------|-------|
| IDLE | Portal |
| SUBMITTING | API Client |
| PROCESSING | Analyze Pipeline |
| RENDERING | Portal Adapter |
| READY | React Runtime |
| ERROR | Error Handler |

---

# UI Visibility Matrix

| Component | IDLE | PROCESSING | READY | ERROR |
|------------|------|------------|-------|-------|
| Input Form | ✓ | ✗ | ✓ | ✓ |
| Loading Overlay | ✗ | ✓ | ✗ | ✗ |
| Skeleton | ✗ | ✓ | ✗ | ✗ |
| Hero | ✗ | ✗ | ✓ | ✗ |
| Executive Summary | ✗ | ✗ | ✓ | ✗ |
| Identity | ✗ | ✗ | ✓ | ✗ |
| Recommendations | ✗ | ✗ | ✓ | ✗ |
| Error Banner | ✗ | ✗ | ✗ | ✓ |

---

# State Data

Each state owns a subset of runtime data.

```
IDLE

↓

AnalyzeRequest

↓

PROCESSING

↓

ReportResponse

↓

RENDERING

↓

CanonicalViewModel

↓

READY
```

---

# Runtime Objects

```
PortalState

├── current_state
├── request
├── report
├── view_model
├── error
├── timings
└── diagnostics
```

Only PortalState is mutable.

---

# State Entry Actions

IDLE

- Reset UI

SUBMITTING

- Disable controls
- Create request

PROCESSING

- Show loading
- Start timer

RENDERING

- Create ViewModel
- Mount components

READY

- Enable interactions

ERROR

- Map ErrorResponse
- Show retry

---

# State Exit Actions

SUBMITTING

- Lock request

PROCESSING

- Stop loading timer

RENDERING

- Release temporary objects

READY

- Preserve report state

ERROR

- Clear temporary runtime objects

---

# Invalid State Prevention

The Portal shall never allow

```
READY

+

PROCESSING
```

or

```
ERROR

+

READY
```

or

```
PROCESSING

+

IDLE
```

Only one runtime state is valid.

---

# Performance

State transitions shall

- Avoid unnecessary re-rendering
- Preserve component identity
- Minimize layout shift
- Maintain smooth UX

---

# Accessibility

Every state transition shall

- Preserve keyboard focus
- Announce loading
- Announce completion
- Announce errors
- Maintain semantic landmarks

---

# Future States

Reserved

```
AUTHENTICATING

OFFLINE

SYNCING

STREAMING

CANCELLING

PRINTING

EXPORTING
```

Future states extend the machine without changing existing transitions.

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_COMPONENT_MAPPING.md | Component mapping |
| 02_DATA_BINDING.md | Data binding |
| 03_LOADING_STATE.md | Loading UX |
| 04_EMPTY_STATE.md | Empty-state behavior |
| 04_PORTAL_STATE_MACHINE.md | Runtime state machine (this document) |
| 05_RENDER_POLICY.md | Rendering policy |

---

# Acceptance Criteria

The Portal Runtime State Machine is accepted when

✓ Exactly one runtime state is active

✓ All transitions are explicit

✓ Invalid transitions are rejected

✓ Components render based on state

✓ Loading and Error are mutually exclusive

✓ ViewModel is created only during Rendering

✓ READY state always contains a valid ReportResponse

✓ State transitions are deterministic

---

# Official Status

Document

Portal Runtime State Machine

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Product Architecture