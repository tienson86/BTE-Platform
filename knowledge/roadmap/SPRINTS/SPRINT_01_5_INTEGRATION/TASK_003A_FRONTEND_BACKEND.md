# BTE Platform V1.0

# TASK_003A — Frontend ↔ Backend Integration

> **STATUS: CANCELLED (2026-08-05)**  
> Product Owner yêu cầu hủy Integration cho đến khi Canonical Portal UI được phê duyệt / UI Freeze.  
> Không kết nối API · Không Backend work trong task này · Mở lại sau Sprint 01 UI Freeze.

---

# Document Information

| Item | Value |
|------|-------|
| Task | TASK_003A |
| Name | Frontend ↔ Backend Integration |
| Sprint | Sprint 01.5 |
| Phase | Integration |
| Version | 1.0 |
| Status | **CANCELLED** (2026-08-05) — chờ Product Owner phê duyệt Canonical Portal UI trước khi Integration |
| Priority | P0 |
| Estimated | 2–3 Days |

---

# Objective

Tích hợp React Portal (`applications/customer_portal`) với Backend FastAPI để thay thế Mock Data bằng API thật.

Sau khi hoàn thành task này:

- Frontend không còn phụ thuộc vào dữ liệu giả trong luồng chính.
- Toàn bộ request đi qua FastAPI.
- UI hiển thị dữ liệu từ Backend.
- Component không cần thay đổi khi chuyển từ Mock sang API.

---

# Business Goal

Người dùng có thể:

1. Nhập thông tin lá số.
2. Gửi yêu cầu phân tích.
3. Nhận kết quả từ Backend.
4. Xem kết quả trên Portal.

Task này **không xử lý logic phân tích**. Chỉ thiết lập đường truyền dữ liệu.

---

# Scope

Bao gồm:

- API Client
- DTO
- Request / Response Models
- Error Handling
- Loading State
- Retry Policy
- Timeout
- Environment Configuration
- Mock → Real API Switch

---

# Out of Scope

Không thực hiện:

- Analysis Engine Logic
- Interpretation Logic
- Report Generation
- Authentication nâng cao
- Business Rule
- Database Migration

---

# Integration Flow

```text
React Portal
      │
      │ HTTP / REST
      ▼
FastAPI
      │
      ▼
Response DTO
      │
      ▼
React State
      │
      ▼
UI Components
```

---

# Directory Scope

## Frontend

```text
applications/customer_portal/

src/

api/

services/

hooks/

pages/

screens/

models/

config/

utils/
```

## Backend

```text
applications/api/

routers/

controllers/

schemas/

services/
```

Không được truy cập trực tiếp Engine từ Frontend.

---

# API Principles

## Principle 1

Frontend chỉ gọi REST API.

Không import module Python.

---

## Principle 2

API trả về JSON chuẩn.

Không trả HTML.

---

## Principle 3

Response phải thống nhất.

Ví dụ:

```json
{
  "success": true,
  "data": {},
  "message": "",
  "errors": []
}
```

---

## Principle 4

Mọi lỗi đều trả về Error DTO.

Không throw raw exception ra Frontend.

---

# Environment

Sử dụng:

```text
.env.development

.env.production
```

Ví dụ:

```text
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Không hardcode URL.

---

# API Client

Tạo một API Client duy nhất.

Ví dụ:

```text
src/api/

client.ts

endpoints.ts

interceptors.ts

types.ts
```

Không gọi `fetch()` trực tiếp trong Screen.

---

# DTO Standard

## Request

```text
CreateChartRequest

AnalyzeChartRequest

GenerateReportRequest
```

## Response

```text
ChartResponse

AnalysisResponse

InterpretationResponse

ReportResponse

ApiErrorResponse
```

---

# State Management

Không hardcode dữ liệu.

Luồng:

Loading

↓

Success

↓

Error

↓

Retry

Không duplicate state.

---

# Error Handling

Các nhóm lỗi:

- Validation Error
- Network Error
- Timeout
- Unauthorized
- Forbidden
- Not Found
- Server Error

Mỗi nhóm phải có UI tương ứng.

---

# Loading Rules

Trong lúc gọi API:

- Skeleton
- Progress
- Disable Submit Button

Không block toàn bộ UI nếu không cần thiết.

---

# Mock Migration Strategy

Bước 1

Mock Data

↓

Adapter

↓

Component

Bước 2

API

↓

Adapter

↓

Component

Component không được sửa khi đổi nguồn dữ liệu.

---

# Security

Không lưu:

- JWT trong source code
- Secret Key
- API Key

Mọi cấu hình đọc từ Environment.

---

# Acceptance Criteria

PASS khi:

- Portal gọi API thật.
- Không còn Mock Data trong luồng chính.
- DTO thống nhất.
- Error Handling đầy đủ.
- Loading hoạt động.
- Build PASS.
- TypeScript PASS.
- Không tạo duplicate API Client.

---

# Deliverables

- API Client
- DTO
- Service Layer
- Environment Config
- Error Handling
- Loading Integration

---

# Cursor Instructions

Bắt buộc:

- Tuân thủ ADR.
- Không sửa Engine.
- Không sửa Business Logic.
- Không sửa Component Library.
- Không thêm Dependency nếu không thật sự cần thiết.
- Không refactor ngoài phạm vi.

Nếu phát hiện vấn đề ngoài Scope:

→ ghi TODO

→ không tự sửa.

---

# Completion Report

## Files Created

...

## Files Modified

...

## API Endpoints Connected

...

## DTO Added

...

## Mock Data Removed

...

## Build

PASS / FAIL

## TypeScript

PASS / FAIL

## Integration Tests

PASS / FAIL

## Remaining TODO

...

## Risks

...

## Notes

...