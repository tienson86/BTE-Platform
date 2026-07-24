# 06_report_templates

## Tổng quan

`06_report_templates` là **thư viện Template Framework** dùng cho Report Engine của BTE Platform.

Module này **không** chứa nội dung luận giải.

Module này **không** sinh dữ liệu luận giải.

Module này chỉ định nghĩa:

- Schema chuẩn của Report Template
- Metadata từng nhóm báo cáo
- Index để lookup template
- Labels (kiểu block / kiểu hiển thị)
- Examples minh họa cấu trúc

Đây là tầng **Presentation Structure** của pipeline báo cáo.

---

## Vai trò trong hệ thống

```text
Interpretation Engine
        ↓
Priority Engine
        ↓
Report Engine
        ↓
Report Template   ← Module này (06_report_templates)
        ↓
Final Report
```

| Tầng | Trách nhiệm |
|------|-------------|
| Interpretation Engine | Sinh nội dung luận giải từ Rule Database |
| Priority Engine | Quyết định rule nào được ưu tiên / ghi đè / bỏ qua |
| Report Engine | Chọn template, bind dữ liệu, render báo cáo |
| Report Template | Cấu trúc khung hiển thị (sections, blocks, placeholders) |
| Final Report | Kết quả đầu ra cho người dùng |

**Nguyên tắc tách biệt:**

- Interpretation = **What to say**
- Priority = **What wins**
- Template = **How to structure**
- Report Engine = **How to render**

---

## Cấu trúc thư mục

```text
06_report_templates/

├── README.md
├── template_schema.json          ⭐ Schema dùng chung (DUY NHẤT)
│
├── 01_summary/
├── 02_personality/
├── 03_career/
├── 04_wealth/
├── 05_relationship/
├── 06_health/
├── 07_children/
├── 08_useful_god/
├── 09_luck_cycle/
└── 10_yearly_fortune/
```

Mỗi module con có cấu trúc thống nhất:

```text
0X_module_name/

├── README.md
├── metadata.json
├── template_index.json
├── template_labels.json
└── template_examples.json
```

---

## 1. template_schema.json

File quan trọng nhất của Framework.

Định nghĩa schema chuẩn cho **mọi** Report Template:

- `template_id`, `template_name`, `module`, `category`
- `title`, `description`, `version`, `priority`
- `conditions`, `placeholders`, `variables`
- `sections`, `blocks`
- `tags`, `language`, `enabled`
- `schema_version`, metadata phụ trợ

**Quy tắc:**

- Chỉ tồn tại **một** file schema ở thư mục gốc
- Không copy schema vào từng module
- Mọi template tương lai phải tuân thủ schema này
- Thiết kế hướng V2 qua `extension_hooks`

---

## 2. metadata.json

Metadata của từng module báo cáo.

Bao gồm:

- `module_id`, `module_name`, `module_title`
- `description`, `version`, `status`
- `language`, `encoding`, `author`
- `created_at`, `updated_at`, `schema_version`

Dùng để Report Engine nhận diện module và kiểm tra compatibility.

---

## 3. template_index.json

Index (mục lục) của module.

Chỉ chứa danh sách entry nhẹ:

- `template_id`
- `template_name`
- `category`
- `priority`
- `version`
- `enabled`

**Không** chứa nội dung template đầy đủ.

Khi mở rộng lên hàng nghìn template, Report Engine chỉ cần đọc index để lọc / sắp xếp trước khi load file template cụ thể.

---

## 4. template_labels.json

Dictionary kiểu hiển thị của module.

Ví dụ các loại label:

- `title`, `subtitle`, `paragraph`
- `summary`, `important`, `warning`
- `recommendation`, `quote`, `table`, `note`

Labels mô tả **cách render block**, không chứa luận giải.

---

## 5. template_examples.json

Chứa **một** example minh họa schema.

Mục đích:

- Giúp developer hiểu cấu trúc
- Dùng cho validation / smoke test
- Không phải nội dung báo cáo thật

---

## Quy trình dữ liệu

```text
1. Interpretation Engine
   → tạo Interpretation Result (nội dung luận giải)

2. Priority Engine
   → resolve priority, chọn rule / interpretation thắng

3. Report Engine
   → đọc metadata + template_index
   → chọn template phù hợp theo module / conditions / priority
   → validate theo template_schema.json
   → bind placeholders từ Interpretation Result
   → render sections / blocks theo labels

4. Final Report
   → báo cáo hoàn chỉnh cho người dùng
```

---

## Quy tắc Framework

1. **Không** viết nội dung luận giải trong template framework.
2. **Không** tạo hàng trăm file template trong V1.0.
3. **Không** hard-code rule luận giải vào schema.
4. Mọi module phải dùng chung `template_schema.json`.
5. Thêm template mới = thêm file JSON + cập nhật `template_index.json`.
6. Không đổi tên field đã ổn định; mở rộng qua `extensions` (V2).
7. Encoding UTF-8, JSON hợp lệ.
8. Giữ backward compatibility.

---

## Quy tắc đặt tên template (tương lai)

```text
{module_short}_{nnn}.json

Ví dụ:
  summary_001.json
  career_012.json
  wealth_003.json
  luck_cycle_001.json
```

V1.0 chỉ định nghĩa quy tắc. **Không** tạo các file template thực tế.

---

## Mở rộng lên V2

Framework V1.0 đã chuẩn bị:

- `extension_hooks` trong schema
- `style` / `render_hints` sẵn sàng trên block
- Index tách khỏi nội dung template
- Module isolation (thêm module mới không phá module cũ)

Khi scale lên hàng nghìn template:

1. Giữ nguyên cấu trúc thư mục
2. Chỉ bổ sung file template + cập nhật index
3. Không cần sửa schema gốc trừ khi bump `schema_version`

---

## Trạng thái

| Mục | Giá trị |
|-----|---------|
| Framework version | 1.0.0 |
| Schema version | 1.0.0 |
| Status | active |
| Encoding | UTF-8 |
| Language | vi |

---

END
