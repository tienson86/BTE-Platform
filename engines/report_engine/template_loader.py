"""
BTE Platform
Report Engine

File: template_loader.py
Version: 1.0
"""

from __future__ import annotations

from pathlib import Path


class TemplateLoader:
    """
    Quản lý template của Report Engine.
    """

    _DEFAULT_TEMPLATE_DIR: Path = Path(__file__).parent / "templates"

    def __init__(
        self,
        template_dir: str | Path | None = None,
    ) -> None:

        if template_dir is None:
            self.template_dir = self._DEFAULT_TEMPLATE_DIR
        else:
            self.template_dir = Path(template_dir)

    # =====================================================
    # Path
    # =====================================================

    def get_path(
        self,
        name: str,
    ) -> Path:
        """
        Lấy đường dẫn template.
        """

        return self.template_dir / f"{name}.md"

    def list(self) -> list[str]:
        """
        Trả về danh sách tên các template hiện có.
        """

        if not self.template_dir.exists():
            return []

        templates = []

        for path in self.template_dir.iterdir():
            if path.is_file():
                templates.append(path.stem)

        templates.sort()

        return templates

    # =====================================================
    # Exists
    # =====================================================

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Kiểm tra template có tồn tại hay không.
        """

        return self.get_path(name).exists()

    # =====================================================
    # Load
    # =====================================================

    def load(
        self,
        name: str,
    ) -> str:
        """
        Đọc nội dung template.
        """

        path = self.get_path(name)

        if not path.exists():

            raise FileNotFoundError(
                f"Template '{name}' không tồn tại."
            )

        return path.read_text(
            encoding="utf-8"
        )

    # =====================================================
    # Save
    # =====================================================

    def save(
        self,
        name: str,
        content: str,
    ) -> None:
        """
        Lưu template.
        """

        self.template_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        path = self.get_path(name)

        path.write_text(
            content,
            encoding="utf-8",
        )

    # =====================================================
    # Delete
    # =====================================================

    def delete(
        self,
        name: str,
    ) -> bool:
        """
        Xóa template.
        """

        path = self.get_path(name)

        if not path.exists():

            return False

        path.unlink()

        return True

    # =====================================================
    # List
    # =====================================================

    def list_templates(
        self,
    ) -> list[str]:
        """
        Danh sách template.
        """

        if not self.template_dir.exists():

            return []

        return sorted(

            file.stem

            for file in self.template_dir.glob("*.md")

        )

    # =====================================================
    # Reload
    # =====================================================

    def reload(
        self,
        name: str,
    ) -> str:
        """
        Đọc lại template từ ổ đĩa.
        """

        return self.load(name)
