"""Applications storage package (JSON first; SQL later)."""

from applications.storage.file_store import FileStore
from applications.storage.json_store import JsonStore
from applications.storage.repository import DocumentRepository, Repository

__all__ = [
    "DocumentRepository",
    "FileStore",
    "JsonStore",
    "Repository",
]
