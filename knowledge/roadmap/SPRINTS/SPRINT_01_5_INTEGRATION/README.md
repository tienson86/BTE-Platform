# BTE Platform V1.0

# Sprint 01.5 — Integration

---

## Document Information

| Item | Value |
|------|-------|
| Document | Sprint 01.5 Integration |
| Version | 1.0 |
| Status | READY |
| Sprint | 01.5 |
| Phase | Release Candidate Integration |
| Priority | P0 |
| Owner | BTE Architecture Team |

---

# Sprint Goal

Hoàn thành việc tích hợp toàn bộ các thành phần của BTE Platform V1.0 để tạo thành một quy trình vận hành hoàn chỉnh từ Portal đến Engine và Report.

Sprint này **không phát triển tính năng mới**.

Mục tiêu duy nhất là biến các module đã hoàn thiện thành một sản phẩm có thể sử dụng và trình diễn.

---

# Business Objective

Sau khi Sprint 01.5 hoàn thành, người dùng phải có thể:

1. Nhập thông tin ngày giờ sinh.
2. Tạo lá số Bát Tự.
3. Thực hiện phân tích.
4. Nhận kết quả luận giải.
5. Xem kết quả trên Portal.
6. Xuất báo cáo PDF.

Đây là luồng nghiệp vụ tối thiểu (Minimum Commercial Workflow) của BTE Platform V1.0.

---

# Integration Architecture

```text
┌─────────────────────────────────────────────┐
│             React Portal UI                 │
│     applications/customer_portal            │
└───────────────────┬─────────────────────────┘
                    │ REST API
                    ▼
┌─────────────────────────────────────────────┐
│                 FastAPI                     │
│ Controllers • DTO • Validation • Auth       │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│             Analysis Engine                 │
│  Chart Builder → Context → Analysis         │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│          Interpretation Engine             │
│ Rules → Templates → Sentences → Result      │
└───────────────────┬─────────────────────────┘
                    │
          ┌─────────┴──────────┐
          ▼                    ▼
┌─────────────────┐   ┌──────────────────────┐
│ Report Engine   │   │ JSON Response Model  │
└─────────────────┘   └──────────────────────┘
          │                    │
          └─────────┬──────────┘
                    ▼
           React Portal UI
```

---

# Integration Principles

## Principle 1 — One Direction Flow

Dữ liệu luôn đi theo một chiều:

Portal

↓

FastAPI

↓

Analysis Engine

↓

Interpretation Engine

↓

Report Engine

↓

Portal

Không được tạo luồng ngược hoặc phụ thuộc vòng.

---

## Principle 2 — Engine Independence

Portal không được gọi trực tiếp Engine.

Mọi truy cập đều phải đi qua FastAPI.

---

## Principle 3 — UI Independence

Engine không biết Portal.

Engine chỉ trả về dữ liệu.

Portal chịu trách nhiệm hiển thị.

---

## Principle 4 — API First

Mọi giao tiếp giữa Portal và Backend phải thông qua API được định nghĩa rõ ràng.

Không truy cập trực tiếp file hoặc module nội bộ.

---

## Principle 5 — Replace Mock Data

Mock Data chỉ được dùng trong Sprint 01.

Trong Sprint 01.5:

- Thay thế từng phần bằng API thật.
- Không thay đổi Component.

---

# Scope

Sprint này bao gồm:

- Frontend ↔ Backend Integration.
- Backend ↔ Analysis Engine.
- Analysis ↔ Interpretation.
- Report Integration.
- Authentication cơ bản.
- Navigation hoàn chỉnh.
- API Error Handling.
- Loading State.
- Production DTO.

---

# Out of Scope

Không thực hiện:

- Module Phong Thủy.
- Xem ngày.
- Sim số.
- AI Rewrite.
- Marketplace.
- Payment.
- Notification.
- Multi-language.
- Mobile App.

Các nội dung trên thuộc V1.1 hoặc V2.0.

---

# Sprint Structure

Sprint 01.5 gồm 5 nhiệm vụ:

| Task | Mục tiêu |
|------|----------|
| TASK_003A_FRONTEND_BACKEND | Portal ↔ FastAPI |
| TASK_003B_ENGINE_BINDING | FastAPI ↔ Analysis & Interpretation |
| TASK_003C_REPORT_BINDING | Report API ↔ Portal |
| TASK_003D_AUTH_ROUTING | Authentication & Navigation |
| TASK_003E_INTEGRATION_REVIEW | Kiểm thử và xác nhận tích hợp |

---

# Success Criteria

Sprint 01.5 được xem là hoàn thành khi:

- Portal gọi được API thật.
- Không còn Mock Data trong luồng chính.
- Analysis Engine trả dữ liệu thành công.
- Interpretation Engine sinh nội dung đúng.
- Portal hiển thị dữ liệu thật.
- Report PDF hoạt động.
- Authentication hoạt động.
- Build PASS.
- TypeScript PASS.
- Integration Tests PASS.

---

# Deliverables

Sau Sprint 01.5 phải có:

- Portal chạy trên dữ liệu thật.
- API tích hợp hoàn chỉnh.
- Luồng nghiệp vụ hoàn chỉnh.
- Báo cáo PDF hoạt động.
- Integration Review Report.

---

# Exit Criteria

Sprint 01.5 chỉ được đóng khi:

- Tất cả TASK_003A → TASK_003E hoàn thành.
- Không còn Blocker mức Critical.
- Release Review xác nhận PASS.

Sau khi Sprint 01.5 hoàn thành, dự án chuyển sang Sprint 02:

- Golden Dataset Validation.
- Regression Testing.
- GO / NO-GO Review.
- Production Release.

---

# Definition of Done

Sprint 01.5 hoàn tất khi BTE Platform V1.0 có thể thực hiện toàn bộ quy trình sau mà không cần thao tác thủ công:

1. Người dùng nhập thông tin.
2. Portal gửi yêu cầu.
3. FastAPI tiếp nhận và kiểm tra dữ liệu.
4. Analysis Engine phân tích lá số.
5. Interpretation Engine sinh nội dung luận giải.
6. Report Engine tạo báo cáo.
7. Portal hiển thị kết quả.
8. Người dùng tải báo cáo PDF.

Đây là tiêu chuẩn hoàn thành tối thiểu để BTE Platform V1.0 đủ điều kiện bước vào giai đoạn kiểm thử phát hành.