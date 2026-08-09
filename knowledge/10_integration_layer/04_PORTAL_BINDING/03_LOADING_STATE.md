# Portal Loading State Specification

**Location**

```
knowledge/10_integration_layer/04_PORTAL_BINDING/03_LOADING_STATE.md
```

---

# Purpose

This document defines the canonical loading experience of the BTE Customer Portal.

Loading is considered part of the consulting experience rather than a technical waiting period.

Customers should always understand that their BaZi report is being professionally prepared.

---

# Status

Document Type

UX / Runtime Specification

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Product

---

# Design Principles

Loading follows these principles.

- Never show a blank page
- Always communicate progress
- Progressive disclosure
- No technical terminology
- Smooth transition
- Deterministic behavior

---

# Loading Lifecycle

```
Customer Clicks Analyze

↓

Request Submitted

↓

Validation

↓

Analysis Pipeline

↓

Report Assembly

↓

Rendering

↓

Completed
```

---

# Runtime States

The Portal defines six runtime states.

```
IDLE

↓

SUBMITTING

↓

PROCESSING

↓

ASSEMBLING

↓

RENDERING

↓

READY
```

---

# State 1 — IDLE

Description

Customer has not started analysis.

Portal displays

- Input form
- Analyze button

No loading indicators.

---

# State 2 — SUBMITTING

Triggered when

Customer presses

```
Analyze
```

Portal behavior

- Disable submit button
- Prevent duplicate submission
- Display immediate visual feedback

Expected duration

Less than one second.

---

# State 3 — PROCESSING

Applications API is executing

```
Analyze Pipeline
```

Portal displays

Main loading screen.

Suggested message

```
Đang phân tích lá số Bát Tự...
```

Optional subtitle

```
Hệ thống đang tổng hợp thông tin để tạo báo cáo tư vấn.
```

No technical stage names.

---

# State 4 — ASSEMBLING

Report Builder is generating

```
ReportResponse
```

Portal displays

```
Đang hoàn thiện báo cáo tư vấn...
```

Progress indicator remains visible.

---

# State 5 — RENDERING

Portal Adapter creates

```
CanonicalViewModel
```

React renders the Result Page.

Portal behavior

- Keep skeleton layout visible
- Prevent layout shift
- Avoid flashing content

---

# State 6 — READY

Report successfully rendered.

Portal displays

Full Result Page.

Loading components are removed.

---

# Loading Timeline

```
Analyze

↓

Submitting

↓

Processing

↓

Assembling

↓

Rendering

↓

Ready
```

The sequence is fixed.

---

# Skeleton Strategy

During loading

Display skeletons for

```
Hero

Executive Summary

Identity

Recommendation

Domain Cards
```

Do not display empty white panels.

---

# Progressive Reveal

Commercial V1

Disabled.

The complete report appears only after validation succeeds.

Future versions may support progressive rendering.

---

# Loading Components

| Component | Behavior |
|------------|----------|
| Hero | Skeleton |
| Executive Summary | Skeleton |
| Identity | Skeleton |
| Recommendation | Skeleton |
| Domain Cards | Skeleton |
| Charts | Hidden |
| Knowledge | Hidden |

---

# Button Behavior

During loading

```
Analyze Button

↓

Disabled
```

Text changes to

```
Đang phân tích...
```

---

# Navigation

During processing

Customer may

- Stay on page

Customer should not

- Submit another request

---

# Timeout Handling

If processing exceeds configured timeout

↓

Stop loading

↓

Display friendly error message

↓

Offer Retry

---

# Cancellation

Commercial V1

Cancellation is not supported.

Future versions may introduce

```
Cancel Analysis
```

---

# Error Transition

```
Processing

↓

Failure

↓

Error Screen

↓

Retry
```

No partial report is displayed.

---

# Success Transition

```
Rendering

↓

Fade In

↓

Result Page
```

Avoid abrupt transitions.

---

# Accessibility

Loading indicators shall

- Support screen readers
- Expose ARIA status
- Announce state changes
- Maintain keyboard focus

---

# Performance Targets

Portal should

- Show loading feedback immediately
- Prevent layout shifts
- Minimize visual flicker

---

# Telemetry

Record

- Request start
- Request finish
- Loading duration
- Rendering duration

Internal only.

---

# Future Enhancements

Future versions may include

- Progressive section loading
- Streaming ReportResponse
- Animated timeline
- Estimated remaining time
- Background analysis

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_COMPONENT_MAPPING.md | Component ownership |
| 02_DATA_BINDING.md | Data binding |
| 03_LOADING_STATE.md | Loading UX (this document) |
| 04_RENDER_POLICY.md | Rendering rules |
| 05_ERROR_PRESENTATION.md | Error UX |

---

# Acceptance Criteria

The loading experience is accepted when

✓ No blank screen appears

✓ Loading feedback is immediate

✓ Skeleton layout matches final layout

✓ No technical terminology is shown

✓ Duplicate submissions are prevented

✓ Successful rendering transitions smoothly

✓ Errors terminate loading cleanly

✓ Accessibility requirements are met

---

# Official Status

Document

Portal Loading State Specification

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Product