"""JSON + SQLite repository and factory tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from applications.case_management.models import CaseModel
from applications.customer.models import CustomerModel
from applications.storage.factory import RepositoryFactory, StorageConfig
from applications.storage.interfaces.repository import CustomerFilter, Page
from applications.storage.migrations import build_default_runner
from applications.storage.postgres import PostgresNotConfiguredError


def _customer(**kwargs: object) -> CustomerModel:
    defaults = {
        "full_name": "Nguyen Van A",
        "gender": "male",
        "birth_datetime": "1990-05-15T10:30:00",
        "phone": "0901111222",
        "email": "a@example.com",
        "tags": ["vip"],
    }
    defaults.update(kwargs)
    return CustomerModel.create(**defaults)  # type: ignore[arg-type]


@pytest.mark.parametrize("backend", ["json", "sqlite"])
def test_customer_crud_and_search(tmp_path: Path, backend: str) -> None:
    config = StorageConfig(
        backend=backend,  # type: ignore[arg-type]
        data_dir=str(tmp_path / "data"),
        sqlite_path=str(tmp_path / "data" / "test.sqlite3"),
    )
    repo = RepositoryFactory.create_customer_repository(config)

    created = repo.create(_customer())
    assert repo.get(created.customer_id) is not None

    created.notes = "hello"
    updated = repo.update(created)
    assert updated.notes == "hello"

    repo.create(
        _customer(
            full_name="Tran Thi B",
            email="b@example.com",
            phone="0909999888",
            tags=["south"],
        )
    )
    page = repo.search(
        CustomerFilter(name="tran"),
        page=Page(page=1, page_size=10),
    )
    assert page.total == 1
    assert page.items[0].full_name == "Tran Thi B"

    assert repo.delete(created.customer_id) is True
    assert repo.get(created.customer_id) is None


@pytest.mark.parametrize("backend", ["json", "sqlite"])
def test_case_crud_and_list_by_customer(tmp_path: Path, backend: str) -> None:
    config = StorageConfig(
        backend=backend,  # type: ignore[arg-type]
        data_dir=str(tmp_path / "data"),
        sqlite_path=str(tmp_path / "data" / "test.sqlite3"),
    )
    bundle = RepositoryFactory.create(config)
    customer = bundle.customers.create(_customer())
    case = CaseModel.create(
        customer_id=customer.customer_id,
        engine_version="1.0.0",
        interpretation_result={"summary": "ok"},
    )
    bundle.cases.create(case)
    assert bundle.cases.get(case.case_id) is not None
    assert len(bundle.cases.list_by_customer(customer.customer_id)) == 1
    assert bundle.cases.delete(case.case_id) is True


def test_factory_backend_selection(tmp_path: Path) -> None:
    json_bundle = RepositoryFactory.create(
        StorageConfig(backend="json", data_dir=str(tmp_path / "json"))
    )
    assert json_bundle.backend == "json"

    sqlite_bundle = RepositoryFactory.create(
        StorageConfig(
            backend="sqlite",
            data_dir=str(tmp_path / "sqlite"),
            sqlite_path=str(tmp_path / "sqlite" / "db.sqlite3"),
        )
    )
    assert sqlite_bundle.backend == "sqlite"


def test_postgres_skeleton_raises() -> None:
    bundle = RepositoryFactory.create(StorageConfig(backend="postgres"))
    assert bundle.backend == "postgres"
    with pytest.raises(PostgresNotConfiguredError):
        bundle.customers.list()


def test_migration_framework_dry_run() -> None:
    runner = build_default_runner()
    ran = runner.run_pending(dry_run=True)
    assert ran == ["0001_init"]
    assert runner.pending() == []


def test_storage_config_rejects_unknown_backend(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BTE_STORAGE_BACKEND", "redis")
    with pytest.raises(ValueError):
        StorageConfig.from_env()
