"""
template_loader.py
==================

Quản lý template báo cáo.

Nhiệm vụ:
- Đọc template JSON
- Kiểm tra hợp lệ
- Cung cấp cấu hình cho ReportBuilder
"""

import json
from pathlib import Path


class TemplateLoader:

    def __init__(self, template_dir=None):

        if template_dir is None:
            template_dir = (
                Path(__file__).parent.parent
                / "templates"
            )

        self.template_dir = Path(template_dir)


    def list_templates(self):
        """
        Trả về danh sách template
        """

        if not self.template_dir.exists():
            return []

        return sorted(
            [
                f.stem
                for f in self.template_dir.glob("*.json")
            ]
        )


    def load(self, template_name="default"):
        """
        Đọc template
        """

        file_path = self.template_dir / f"{template_name}.json"

        if not file_path.exists():
            raise FileNotFoundError(
                f"Không tìm thấy template: {file_path}"
            )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        self.validate(data)

        return data


    def validate(self, template):

        required = [
            "title",
            "font",
            "sections"
        ]

        for item in required:

            if item not in template:

                raise ValueError(
                    f"Template thiếu '{item}'"
                )

        return True


    def exists(self, template_name):

        return (
            self.template_dir /
            f"{template_name}.json"
        ).exists()
