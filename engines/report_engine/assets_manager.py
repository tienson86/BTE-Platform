"""
assets_manager.py
=================

Quản lý toàn bộ tài nguyên báo cáo.

Ví dụ:

logo

icon

watermark

ảnh ngũ hành

ảnh bát quái

QR Code

...
"""

from pathlib import Path


class AssetsManager:

    def __init__(self, assets_dir=None):

        if assets_dir is None:

            assets_dir = (
                Path(__file__).parent.parent
                / "assets"
            )

        self.assets_dir = Path(assets_dir)


    def get(self, filename):

        path = self.assets_dir / filename

        if not path.exists():

            raise FileNotFoundError(
                f"Không tìm thấy asset: {filename}"
            )

        return str(path)


    def exists(self, filename):

        return (
            self.assets_dir /
            filename
        ).exists()


    def list_assets(self):

        if not self.assets_dir.exists():

            return []

        return sorted(

            [
                f.name
                for f in self.assets_dir.iterdir()
                if f.is_file()
            ]

        )


    def logo(self):

        if self.exists("logo.png"):

            return self.get("logo.png")

        return None


    def watermark(self):

        if self.exists("watermark.png"):

            return self.get("watermark.png")

        return None


    def icon(self, name):

        filename = f"{name}.png"

        if self.exists(filename):

            return self.get(filename)

        return None


    def image(self, filename):

        return self.get(filename)
