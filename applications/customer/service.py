"""Customer application service."""

from __future__ import annotations

from applications.customer.models import CustomerModel
from applications.customer.repository import CustomerRepository
from applications.customer.search import search_customers
from applications.customer.validators import (
    CustomerValidationError,
    validate_birth_datetime,
    validate_email,
    validate_full_name,
    validate_phone,
    validate_tags,
)


class CustomerNotFoundError(LookupError):
    """Customer id not found."""


class CustomerService:
    """CRUD + search for customers (no billing / email)."""

    def __init__(self, repository: CustomerRepository) -> None:
        self.repository = repository

    def create(
        self,
        *,
        full_name: str,
        gender: str | None = None,
        birth_datetime: str | None = None,
        timezone: str = "Asia/Ho_Chi_Minh",
        language: str = "vi",
        phone: str | None = None,
        email: str | None = None,
        notes: str | None = None,
        tags: list[str] | None = None,
    ) -> CustomerModel:
        """Validate and create a customer."""
        customer = CustomerModel.create(
            full_name=validate_full_name(full_name),
            gender=gender,
            birth_datetime=validate_birth_datetime(birth_datetime),
            timezone=timezone or "Asia/Ho_Chi_Minh",
            language=language or "vi",
            phone=validate_phone(phone),
            email=validate_email(email),
            notes=notes,
            tags=validate_tags(tags),
        )
        return self.repository.create(customer)

    def get(self, customer_id: str) -> CustomerModel:
        """Get customer or raise."""
        customer = self.repository.get(customer_id)
        if customer is None:
            raise CustomerNotFoundError(customer_id)
        return customer

    def list(self) -> list[CustomerModel]:
        """List all customers."""
        return self.repository.list()

    def update(
        self,
        customer_id: str,
        *,
        full_name: str | None = None,
        gender: str | None = None,
        birth_datetime: str | None = None,
        timezone: str | None = None,
        language: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        notes: str | None = None,
        tags: list[str] | None = None,
    ) -> CustomerModel:
        """Partial update of customer fields."""
        customer = self.get(customer_id)
        if full_name is not None:
            customer.full_name = validate_full_name(full_name)
        if gender is not None:
            customer.gender = gender
        if birth_datetime is not None:
            customer.birth_datetime = validate_birth_datetime(birth_datetime)
        if timezone is not None:
            customer.timezone = timezone
        if language is not None:
            customer.language = language
        if phone is not None:
            customer.phone = validate_phone(phone)
        if email is not None:
            customer.email = validate_email(email)
        if notes is not None:
            customer.notes = notes
        if tags is not None:
            customer.tags = validate_tags(tags)
        return self.repository.update(customer)

    def delete(self, customer_id: str) -> bool:
        """Delete customer; False if missing."""
        return self.repository.delete(customer_id)

    def search(
        self,
        *,
        name: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        tag: str | None = None,
        created_from: str | None = None,
        created_to: str | None = None,
    ) -> list[CustomerModel]:
        """Search customers with optional filters."""
        return search_customers(
            self.repository.list(),
            name=name,
            phone=phone,
            email=email,
            tag=tag,
            created_from=created_from,
            created_to=created_to,
        )


__all__ = [
    "CustomerNotFoundError",
    "CustomerService",
    "CustomerValidationError",
]
