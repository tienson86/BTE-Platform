"""Repository factory — selects storage backend from config/env."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from applications.storage.interfaces.case_repository import CaseRepository
from applications.storage.interfaces.customer_repository import CustomerRepository
from applications.storage.json.case_repository import JsonCaseRepository
from applications.storage.json.customer_repository import JsonCustomerRepository
from applications.storage.postgres.case_repository import PostgresCaseRepository
from applications.storage.postgres.customer_repository import (
    PostgresCustomerRepository,
)
from applications.storage.sqlite.case_repository import SQLiteCaseRepository
from applications.storage.sqlite.customer_repository import SQLiteCustomerRepository
from applications.storage.sqlite.database import SQLiteDatabase

StorageBackend = Literal["json", "sqlite", "postgres"]


@dataclass(slots=True)
class StorageConfig:
    """Persistence configuration (env-driven)."""

    backend: StorageBackend = "json"
    data_dir: str = "applications/data"
    sqlite_path: str | None = None
    postgres_dsn: str | None = None

    @classmethod
    def from_env(cls) -> StorageConfig:
        """
        Build config from environment.

        - ``BTE_STORAGE_BACKEND`` = json | sqlite | postgres
        - ``BTE_DATA_DIR`` = JSON root directory
        - ``BTE_SQLITE_PATH`` = SQLite file path
        - ``BTE_POSTGRES_DSN`` = PostgreSQL DSN (skeleton)
        """
        raw = (os.getenv("BTE_STORAGE_BACKEND") or "json").strip().lower()
        if raw not in {"json", "sqlite", "postgres"}:
            raise ValueError(
                f"Unsupported BTE_STORAGE_BACKEND={raw!r}; "
                "expected json|sqlite|postgres"
            )
        default_data = Path(__file__).resolve().parents[1] / "data"
        return cls(
            backend=raw,  # type: ignore[arg-type]
            data_dir=os.getenv("BTE_DATA_DIR", str(default_data)),
            sqlite_path=os.getenv("BTE_SQLITE_PATH"),
            postgres_dsn=os.getenv("BTE_POSTGRES_DSN"),
        )


@dataclass(slots=True)
class RepositoryBundle:
    """Customer + case repositories for one backend."""

    backend: StorageBackend
    customers: CustomerRepository
    cases: CaseRepository


class RepositoryFactory:
    """
    Create repositories without leaking backend details to business code.

    Example::

        bundle = RepositoryFactory.create()
        customer_repo = bundle.customers
    """

    @staticmethod
    def create(config: StorageConfig | None = None) -> RepositoryBundle:
        """Create repositories for the configured backend."""
        cfg = config or StorageConfig.from_env()
        if cfg.backend == "json":
            root = Path(cfg.data_dir)
            root.mkdir(parents=True, exist_ok=True)
            return RepositoryBundle(
                backend="json",
                customers=JsonCustomerRepository(root / "customers.json"),
                cases=JsonCaseRepository(root / "cases.json"),
            )
        if cfg.backend == "sqlite":
            db_path = Path(
                cfg.sqlite_path
                or str(Path(cfg.data_dir) / "bte.sqlite3")
            )
            database = SQLiteDatabase(db_path)
            return RepositoryBundle(
                backend="sqlite",
                customers=SQLiteCustomerRepository(database),
                cases=SQLiteCaseRepository(database),
            )
        # postgres skeleton
        return RepositoryBundle(
            backend="postgres",
            customers=PostgresCustomerRepository(cfg.postgres_dsn),
            cases=PostgresCaseRepository(cfg.postgres_dsn),
        )

    @staticmethod
    def create_customer_repository(
        config: StorageConfig | None = None,
    ) -> CustomerRepository:
        """Return only the customer repository."""
        return RepositoryFactory.create(config).customers

    @staticmethod
    def create_case_repository(
        config: StorageConfig | None = None,
    ) -> CaseRepository:
        """Return only the case repository."""
        return RepositoryFactory.create(config).cases
