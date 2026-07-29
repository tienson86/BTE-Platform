"""
Applications storage package (WP12 Persistence Layer).

Backends: json (default) | sqlite | postgres (skeleton).
Select via ``BTE_STORAGE_BACKEND``.
"""

from applications.storage.factory import (
    RepositoryBundle,
    RepositoryFactory,
    StorageConfig,
)
from applications.storage.file_store import FileStore
from applications.storage.interfaces import (
    CaseFilter,
    CaseRepository,
    CustomerFilter,
    CustomerRepository,
    DocumentRepository,
    Page,
    PageResult,
    Repository,
)
from applications.storage.json_store import JsonStore
from applications.storage.migrations import MigrationRunner, build_default_runner

__all__ = [
    "CaseFilter",
    "CaseRepository",
    "CustomerFilter",
    "CustomerRepository",
    "DocumentRepository",
    "FileStore",
    "JsonStore",
    "MigrationRunner",
    "Page",
    "PageResult",
    "Repository",
    "RepositoryBundle",
    "RepositoryFactory",
    "StorageConfig",
    "build_default_runner",
]
