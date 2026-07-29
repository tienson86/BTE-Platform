# Report Engine Specification

Version: 1.0

Status: Official

---

# 1. Purpose

Report Engine định dạng kết quả cuối cùng để hiển thị hoặc xuất báo cáo.

Không thực hiện tính toán hay luận giải.

---

# 2. Responsibilities

Xuất:

- Markdown
- HTML
- JSON
- PDF
- DOCX
- Plain Text

Quản lý:

- Templates
- Themes
- Layout
- Assets

---

# 3. Non-Responsibilities

Không:

- Tính Bát Tự
- Chấm điểm
- Xác định Pattern
- Luận giải

---

# 4. Input

InterpretationResult

---

# 5. Output

ReportResult

Bao gồm:

- markdown
- html
- json
- pdf_path
- docx_path
- metadata

---

# 6. Public API

ReportService

Các phương thức:

generate()

render_markdown()

render_html()

render_pdf()

render_docx()

export()

---

# 7. Internal Components

renderer.py

markdown_renderer.py

html_renderer.py

pdf_renderer.py

docx_renderer.py

template_loader.py

theme_loader.py

asset_manager.py

service.py

exceptions.py

---

# 8. Processing Flow

InterpretationResult

↓

Load Template

↓

Apply Theme

↓

Render Sections

↓

Generate Output

↓

ReportResult

---

# 9. Dependencies

Depends On

- Interpretation Engine
- Template Database

Không phụ thuộc

- Calendar Engine
- Bazi Engine
- Score Engine
- Pattern Engine

---

# 10. Error Handling

ReportError

TemplateNotFoundError

RenderError

ExportError

---

# 11. Performance

Mục tiêu

Markdown

<50ms

HTML

<100ms

PDF

<500ms

Template phải cache.

---

# 12. Testing Strategy

Unit Test

- Renderer
- Template Loader
- Export

Golden Dataset

Visual Regression

Snapshot Test

---

# 13. Future Extensions

- Interactive HTML Report
- Responsive Report
- Report Themes
- Watermark
- Multi-language Export
- Cloud Export

---

END
