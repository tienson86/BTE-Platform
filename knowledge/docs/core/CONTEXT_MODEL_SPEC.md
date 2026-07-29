# CONTEXT_MODEL_SPEC.md

> Module: Knowledge Framework
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Context Model Specification
>
> BTE Platform

---

# 1. Mục đích

`CONTEXT_MODEL_SPEC.md` định nghĩa **Context Model chuẩn** của BTE Platform.

Context là tập hợp toàn bộ dữ liệu đầu vào được chuẩn hóa để các Engine sử dụng trong quá trình phân tích.

Context không chứa thuật toán, không chứa Rule và không chứa kết quả diễn giải.

---

# 2. Mục tiêu

Context Model được xây dựng nhằm:

- Chuẩn hóa dữ liệu đầu vào.
- Loại bỏ sự phụ thuộc giữa các Engine.
- Cho phép nhiều Engine sử dụng chung một nguồn dữ liệu.
- Hỗ trợ kiểm thử.
- Hỗ trợ Debug.
- Hỗ trợ mở rộng.

---

# 3. Vai trò của Context

Trong kiến trúc tổng thể:

```
Raw Data
    │
    ▼
Context Builder
    │
    ▼
Context
    │
    ├── Rule Engine
    ├── Score Engine
    ├── Interpretation Engine
    ├── Report Engine
    └── AI Services
```

Context là **Single Source of Truth** cho mọi dữ liệu phân tích.

---

# 4. Nguyên tắc thiết kế

Context phải tuân thủ các nguyên tắc sau:

- Immutable trong Runtime.
- Serializable (JSON).
- Deterministic.
- Engine Independent.
- Extensible.
- Versioned.

---

# 5. Cấu trúc tổng quát

```
Context
│
├── Metadata
├── Subject
├── Calendar
├── Natal Chart
├── Analysis
├── Luck
├── Runtime
└── Extensions
```

Mỗi nhóm dữ liệu có trách nhiệm rõ ràng và không chồng chéo.

---

# 6. Metadata

Metadata mô tả thông tin quản trị của Context.

Ví dụ:

```json
{
  "metadata": {
    "context_version": "1.0.0",
    "generated_at": "2026-07-29T09:00:00Z",
    "generator": "context_builder"
  }
}
```

Metadata không tham gia phân tích.

---

# 7. Subject

Thông tin đối tượng được phân tích.

Ví dụ:

```json
{
  "subject": {
    "id": "person_001",
    "gender": "male",
    "birth_datetime": "1987-01-21T04:10:00",
    "timezone": "Asia/Ho_Chi_Minh",
    "location": "Ha Tay, Vietnam"
  }
}
```

Subject chỉ chứa dữ liệu gốc, không chứa dữ liệu đã tính toán.

---

# 8. Calendar

Thông tin lịch đã được chuẩn hóa.

Bao gồm:

- Dương lịch.
- Âm lịch.
- Tiết khí.
- Julian Day.
- Múi giờ.

Ví dụ:

```json
{
  "calendar": {
    "solar_date": "...",
    "lunar_date": "...",
    "solar_term": "...",
    "julian_day": 2446817
  }
}
```

---

# 9. Natal Chart

Thông tin lá số đã được xây dựng.

Bao gồm:

- Four Pillars.
- Hidden Stems.
- Five Elements.
- Ten Gods.
- Na Yin.
- Twelve Growth Phases.
- Void Branches (Không Vong).
- Shen Sha.

Ví dụ:

```json
{
  "natal_chart": {
    "year": {},
    "month": {},
    "day": {},
    "hour": {}
  }
}
```

Đây là dữ liệu đã qua tính toán của Bazi Engine.

---

# 10. Analysis

Kết quả phân tích trung gian.

Bao gồm:

- Day Master Strength.
- Seasonal Influence.
- Temperature.
- Pattern.
- Useful God.
- Favorable Elements.
- Unfavorable Elements.

Ví dụ:

```json
{
  "analysis": {
    "strength": {},
    "pattern": {},
    "useful_god": {}
  }
}
```

Analysis không chứa diễn giải ngôn ngữ tự nhiên.

---

# 11. Luck

Thông tin vận hạn.

Bao gồm:

- Đại vận.
- Lưu niên.
- Lưu nguyệt.
- Lưu nhật.
- Lưu thời.

Ví dụ:

```json
{
  "luck": {
    "major_cycle": {},
    "annual": {},
    "monthly": {}
  }
}
```

---

# 12. Runtime

Thông tin phục vụ quá trình thực thi.

Ví dụ:

```json
{
  "runtime": {
    "locale": "vi-VN",
    "language": "vi",
    "debug": false
  }
}
```

Runtime không được ghi vào Rule Database.

---

# 13. Extensions

Cho phép mở rộng Context mà không phá vỡ cấu trúc chuẩn.

Ví dụ:

```json
{
  "extensions": {
    "feng_shui": {},
    "numerology": {},
    "custom": {}
  }
}
```

Mọi Extension phải có namespace riêng.

---

# 14. Context Lifecycle

```
Raw Input
    │
    ▼
Validation
    │
    ▼
Normalization
    │
    ▼
Calculation
    │
    ▼
Context Build
    │
    ▼
Frozen Context
```

Sau khi được tạo, Context không được chỉnh sửa trực tiếp trong quá trình Engine thực thi.

---

# 15. Context Invariants

Mọi Context phải đảm bảo:

- Có Metadata.
- Có Subject.
- Có Calendar.
- Có Natal Chart.
- Có cấu trúc hợp lệ.
- Có thể Serialize thành JSON.
- Không chứa Rule.
- Không chứa Interpretation.
- Không chứa Report.
- Không chứa trạng thái Runtime của Engine.

---

# 16. Quan hệ với các Model khác

```
Context
    │
    ├── được tạo từ Raw Data
    ├── được sử dụng bởi Rule Engine
    ├── được sử dụng bởi Score Engine
    ├── được sử dụng bởi Interpretation Engine
    ├── được sử dụng bởi Report Engine
    └── tạo ra Result
```

Context không phụ thuộc vào Result.

---

# 17. Versioning

Context Model tuân theo Semantic Versioning.

```
MAJOR.MINOR.PATCH
```

Mọi thay đổi phá vỡ khả năng tương thích chỉ được thực hiện trong Major Version.

---

# 18. Governance

Mọi Engine trong BTE Platform phải:

- Đọc Context theo chuẩn này.
- Không sửa đổi Context trong Runtime.
- Không thêm trường ngoài Extension nếu chưa được chuẩn hóa.
- Không phụ thuộc vào cấu trúc nội bộ của Engine khác.

---

# 19. Kết luận

`CONTEXT_MODEL_SPEC.md` định nghĩa **Input Model chuẩn** của BTE Platform.

Việc chuẩn hóa Context giúp mọi Engine sử dụng cùng một nguồn dữ liệu, giảm sự phụ thuộc lẫn nhau, nâng cao khả năng kiểm thử và tạo nền tảng vững chắc cho việc mở rộng hệ thống trong tương lai.