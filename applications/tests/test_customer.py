"""Customer service / search / validator tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from applications.customer.repository import CustomerRepository
from applications.customer.service import (
    CustomerNotFoundError,
    CustomerService,
    CustomerValidationError,
)


def _service(tmp_path: Path) -> CustomerService:
    return CustomerService(CustomerRepository(tmp_path / "customers.json"))


def test_customer_crud(tmp_path: Path) -> None:
    service = _service(tmp_path)
    created = service.create(
        full_name="Nguyen Van A",
        gender="male",
        birth_datetime="1990-05-15T10:30:00",
        phone="+84901234567",
        email="a@example.com",
        tags=["vip", "hn"],
    )
    assert created.customer_id
    assert service.get(created.customer_id).full_name == "Nguyen Van A"

    updated = service.update(created.customer_id, notes="note1", tags=["vip"])
    assert updated.notes == "note1"
    assert updated.tags == ["vip"]

    assert service.delete(created.customer_id) is True
    with pytest.raises(CustomerNotFoundError):
        service.get(created.customer_id)


def test_customer_search(tmp_path: Path) -> None:
    service = _service(tmp_path)
    service.create(
        full_name="Tran Thi B",
        phone="0901111222",
        email="b@example.com",
        tags=["south"],
        birth_datetime="1992-01-01T08:00:00",
    )
    service.create(
        full_name="Le Van C",
        phone="0903333444",
        email="c@example.com",
        tags=["north", "vip"],
        birth_datetime="1988-12-31T12:00:00",
    )

    by_name = service.search(name="tran")
    assert len(by_name) == 1
    assert by_name[0].full_name == "Tran Thi B"

    by_tag = service.search(tag="vip")
    assert len(by_tag) == 1
    assert by_tag[0].full_name == "Le Van C"

    by_email = service.search(email="c@example")
    assert len(by_email) == 1


def test_customer_validation(tmp_path: Path) -> None:
    service = _service(tmp_path)
    with pytest.raises(CustomerValidationError):
        service.create(full_name="  ")
    with pytest.raises(CustomerValidationError):
        service.create(full_name="A", email="not-an-email")
