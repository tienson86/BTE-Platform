"""Filesystem helpers for WP11 storage."""

from __future__ import annotations

from pathlib import Path


class FileStore:
    """Create directories and resolve paths under a root data folder."""

    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def ensure_dir(self, *parts: str) -> Path:
        """Ensure a subdirectory exists and return it."""
        path = self.root.joinpath(*parts)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def path(self, *parts: str) -> Path:
        """Resolve a path under the root (does not create)."""
        return self.root.joinpath(*parts)

    def write_text(self, relative: str, content: str, *, encoding: str = "utf-8") -> Path:
        """Write a text file under the root."""
        target = self.path(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding=encoding)
        return target

    def read_text(self, relative: str, *, encoding: str = "utf-8") -> str:
        """Read a text file under the root."""
        return self.path(relative).read_text(encoding=encoding)
