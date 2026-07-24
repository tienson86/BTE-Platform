# Pattern Rules Module

## 1. Mục đích

Module **Pattern Rules** chịu trách nhiệm xác định **Cách cục (Pattern)** của lá số Bát Tự.

Đây là tầng nghiệp vụ nằm sau quá trình:

- Xây dựng Tứ Trụ
- Tính Ngũ Hành
- Xác định Thân Vượng/Nhược
- Tính Thập Thần

và trước các module:

- Dụng Thần
- Luận giải
- Báo cáo

Module này hoạt động hoàn toàn theo Rule-Based Engine và không chứa bất kỳ logic nghiệp vụ cứng (hard-code) nào.

---

# 2. Kiến trúc

```
04_pattern_rules/

├── pattern_rules.json
├── pattern_score_rules.json
├── pattern_priority.json
├── pattern_labels.json
├── pattern_examples.json
└── README.md
```

---

# 3. Chức năng từng file

## pattern_rules.json

Định nghĩa các điều kiện nhận diện Cách cục.

Ví dụ:

- Chính Quan Cách
- Thất Sát Cách
- Chính Tài Cách
- Thiên Tài Cách
- Chính Ấn Cách
- Thiên Ấn Cách
- Thực Thần Cách
- Thương Quan Cách
- Tỷ Kiên Cách
- Kiếp Tài Cách
- Tòng Cách
- Chuyên Vượng Cách
- Hóa Khí Cách
- Giả Tòng Cách

Output:

```
candidate_patterns[]
```

---

## pattern_score_rules.json

Tính điểm cho từng ứng viên Cách cục.

Nguồn điểm bao gồm:

- Nguyệt lệnh
- Thập thần lộ
- Thập thần có gốc
- Quan hệ sinh khắc
- Phá cách
- Điều kiện đặc biệt

Output:

```
pattern_score

pattern_strength

confidence
```

---

## pattern_priority.json

Giải quyết trường hợp có nhiều Cách cục hợp lệ.

Pipeline:

```
Collect Candidates

↓

Score Candidates

↓

Apply Override

↓

Priority Rules

↓

Tie Break

↓

Final Pattern
```

Output:

```
final_pattern
```

---

## pattern_labels.json

Định nghĩa toàn bộ Label đa ngôn ngữ.

Bao gồm:

- Pattern Name
- Pattern Family
- Pattern Strength
- Confidence
- Priority Level
- Metadata Labels

Ngôn ngữ hỗ trợ:

- Vietnamese
- English
- Chinese

---

## pattern_examples.json

Golden Dataset dùng để kiểm thử.

Bao phủ:

- Standard Pattern
- Multiple Candidates
- Conflict
- Follow Pattern
- Transformation Pattern
- Priority
- Edge Cases
- Integration Cases

---

# 4. Luồng xử lý

```
Input

↓

Pattern Rules

↓

Candidate Patterns

↓

Pattern Score

↓

Priority Engine

↓

Final Pattern
```

---

# 5. Dữ liệu đầu vào

Module sử dụng các dữ liệu chuẩn hóa từ các Engine trước.

Ví dụ:

```
month_commander_ten_god

visible_ten_gods

supported_ten_gods

destroyed_ten_gods

day_master_strength

special_flags
```

---

# 6. Dữ liệu đầu ra

Module trả về:

```
candidate_patterns

final_pattern

pattern_score

pattern_strength

confidence

priority_level

reason_codes
```

Các kết quả này sẽ được sử dụng bởi:

- Useful God Engine
- Interpretation Engine
- Report Engine

---

# 7. Quy tắc thiết kế

Toàn bộ Rule Database phải tuân thủ các nguyên tắc sau:

- Không hard-code nghiệp vụ.
- Rule và Engine tách biệt hoàn toàn.
- Mỗi Rule có mã định danh duy nhất.
- Rule có thể bật/tắt bằng trường `enabled`.
- Mọi điều kiện đều được khai báo trong dữ liệu.
- Engine chỉ đọc và thực thi Rule.

---

# 8. Quy tắc đặt mã

## Pattern

```
PAT001
PAT002
...
```

## Score Rule

```
PSC001
PSC002
...
```

## Priority Rule

```
PPR001
PPR002
...
```

## Example

```
PEX001
PEX002
...
```

---

# 9. Quy trình kiểm thử

Thứ tự kiểm thử khuyến nghị:

1. Pattern Rules
2. Pattern Score Rules
3. Priority Rules
4. Pattern Examples
5. Interpretation Engine

Toàn bộ Golden Dataset phải vượt qua trước khi phát hành phiên bản mới.

---

# 10. Mở rộng trong tương lai

Kiến trúc hiện tại được thiết kế để dễ dàng mở rộng mà không thay đổi Engine.

Có thể bổ sung:

- Cách cục của từng trường phái khác nhau.
- Quy tắc ưu tiên mới.
- Quy tắc chấm điểm mới.
- Label đa ngôn ngữ mới.
- Golden Dataset mới.
- Rule Override theo phiên bản.
- Rule Override theo trường phái.

---

# 11. Phiên bản

| Thuộc tính | Giá trị |
|------------|---------|
| Module | Pattern Rules |
| Phiên bản | V1.0 |
| Kiến trúc | Rule-Based |
| Định dạng | JSON |
| Engine | Pattern Engine |
| Trạng thái | Stable |
| Golden Dataset | 40 Examples |
| Hard-code | Không |
| Hỗ trợ đa ngôn ngữ | Có |

---

# 12. Phụ thuộc

Module này phụ thuộc vào các thành phần sau:

```
calendar_engine
        ↓
bazi_engine
        ↓
strength_engine
        ↓
ten_god_engine
        ↓
pattern_engine
        ↓
useful_god_engine
        ↓
interpretation_engine
        ↓
report_engine
```

Mỗi Engine chỉ giao tiếp thông qua dữ liệu chuẩn hóa và không phụ thuộc trực tiếp vào cài đặt nội bộ của Engine khác, giúp toàn bộ hệ thống dễ kiểm thử, dễ bảo trì và dễ mở rộng.