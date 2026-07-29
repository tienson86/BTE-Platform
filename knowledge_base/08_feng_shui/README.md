# 08_feng_shui — Feng Shui Knowledge Base Framework (FS-01A)

## Mục tiêu module

Module `08_feng_shui` là **Knowledge Base** lưu tri thức **Cung Phi (Mệnh Quái)** của BTE Platform.

Work Package **FS-01A** chỉ dựng **framework**:

- Schema chuẩn
- Validator
- Khung 8 file gua (mảng để trống)

**Không** làm ở WP này:

- Không viết nội dung chuyên môn (personality, career, health, …)
- Không sinh luận giải / narrative
- Không dùng AI điền dữ liệu
- Không viết business rule / sentence template

> Nội dung các mảng sẽ do **đội chuyên môn** bổ sung sau. Ở trạng thái framework, mọi mảng **phải rỗng**.

---

## Cấu trúc thư mục

```text
knowledge_base/
  08_feng_shui/
    README.md            # tài liệu module
    metadata.json        # version / author / schema_version / map file
    schema.json          # JSON Schema chuẩn cho mỗi gua
    validator.py         # kiểm tra 1 object/file theo schema
    validate_all.py      # chạy validate toàn bộ 01_gua/
    examples/
      sample.json        # file mẫu (khung rỗng)
    01_gua/
      kham.json          # 1 Khảm  — Đông Tứ Trạch
      khon.json          # 2 Khôn  — Tây Tứ Trạch
      chan.json          # 3 Chấn  — Đông Tứ Trạch
      ton.json           # 4 Tốn   — Đông Tứ Trạch
      can.json           # 6 Càn   — Tây Tứ Trạch
      doai.json          # 7 Đoài  — Tây Tứ Trạch
      can_gen.json       # 8 Cấn   — Tây Tứ Trạch
      ly.json            # 9 Ly    — Đông Tứ Trạch
```

Số 5 không có file riêng (quy ước Cung Phi: nam → Khôn, nữ → Cấn).

---

## Schema

Mọi file trong `01_gua/` dùng **cùng một schema** (xem `schema.json`). Không thêm/bớt field.

| Field | Kiểu | Ghi chú |
|-------|------|---------|
| `id` | string | Định danh, khớp `^gua_[a-z_]+$` |
| `name` | string | Tên quái (Tiếng Việt) |
| `number` | integer | 1–4, 6–9 |
| `group` | string | `Đông Tứ Trạch` \| `Tây Tứ Trạch` |
| `element` | string | Ngũ hành |
| `direction` | string | Phương vị |
| `aliases` | string[] | Tên gọi khác |
| `keywords` | string[] | Từ khóa |
| `overview` | string[] | Tổng quan |
| `personality` | string[] | Tính cách |
| `strengths` | string[] | Điểm mạnh |
| `weaknesses` | string[] | Điểm yếu |
| `career` | string[] | Sự nghiệp |
| `wealth` | string[] | Tài lộc |
| `relationship` | string[] | Quan hệ |
| `family` | string[] | Gia đình |
| `health` | string[] | Sức khỏe |
| `learning` | string[] | Học tập |
| `leadership` | string[] | Lãnh đạo |
| `communication` | string[] | Giao tiếp |
| `suitable_jobs` | string[] | Nghề phù hợp |
| `unsuitable_jobs` | string[] | Nghề không phù hợp |
| `development_advice` | string[] | Lời khuyên phát triển |
| `notes` | string[] | Ghi chú |
| `references` | string[] | Nguồn tham chiếu |

Các field scalar nhận dạng (`id`, `name`, `number`, `group`, `element`, `direction`) đã điền sẵn vì là dữ liệu định danh cố định của quái. **Tất cả field mảng để rỗng** cho tới khi đội chuyên môn nhập.

---

## Cách thêm dữ liệu

1. Mở file quái tương ứng trong `01_gua/`.
2. Chỉ thêm phần tử **string** vào các mảng — giữ nguyên tên field và field scalar.
3. Không đổi schema. Muốn thêm field mới → bump `schema_version` (xem dưới), cập nhật `schema.json`, README, và **cả 8 file**.
4. Chạy validator trước khi commit:

```bash
python knowledge_base/08_feng_shui/validate_all.py
```

Exit code `0` = tất cả hợp lệ; `1` = có lỗi (in chi tiết từng field thiếu/thừa/sai kiểu).

---

## Quy tắc đặt id

- Tiền tố bắt buộc: `gua_`
- Chữ thường, không dấu, dùng `_` phân tách: `^gua_[a-z_]+$`
- Trùng khớp tên file (không phần mở rộng) khi có thể.
- Trường hợp trùng phiên âm: Càn = `gua_can`, Cấn = `gua_can_gen` (thêm hậu tố để phân biệt).

---

## Quy tắc encoding

- Tất cả file JSON lưu **UTF-8** (không BOM).
- Giữ nguyên dấu tiếng Việt trong giá trị (`"Khảm"`, `"Đông Tứ Trạch"`).
- Không escape unicode (`\uXXXX`); viết ký tự trực tiếp.
- Xuống dòng LF.

---

## Quy tắc viết tiếng Việt

- Có dấu đầy đủ, đúng chính tả.
- Mỗi phần tử mảng là **một ý ngắn** (cụm từ / fact), không phải đoạn văn luận giải.
- Không viết câu hoàn chỉnh mang tính narrative/report.
- Không nhúng điều kiện `if/else`, placeholder template, hay logic nghiệp vụ.
- Thuật ngữ Bát Tự / Phong Thủy dùng nhất quán với phần còn lại của hệ thống.

---

## Metadata

`metadata.json` chứa: `version`, `author`, `updated_at`, `schema_version`, map `number → file`, và nhóm Đông/Tây Tứ Trạch.

---

## Liên kết

- Engine tính toán: `engines/feng_shui_engine/`
- Work Package: FS-01A — Feng Shui Knowledge Base Framework
