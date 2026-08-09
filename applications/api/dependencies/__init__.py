"""FastAPI dependency providers."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from applications.api.auth.store import InMemoryUserStore, seed_dev_store
from applications.api.config import APISettings, settings
from applications.api.services.auth_service import AuthService
from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.user_service import UserService
from applications.case_management.repository import CaseRepository
from applications.case_management.service import CaseService
from applications.customer.repository import CustomerRepository
from applications.customer.service import CustomerService
from applications.storage.file_store import FileStore


@lru_cache(maxsize=1)
def get_settings() -> APISettings:
    """Return API settings (live module singleton)."""
    from applications.api import config as config_module

    return config_module.settings


@lru_cache(maxsize=1)
def get_user_store() -> InMemoryUserStore:
    """Return seeded in-memory user store (WP10)."""
    return seed_dev_store()


@lru_cache(maxsize=1)
def get_auth_service() -> AuthService:
    """Return shared auth service."""
    return AuthService(get_user_store())


@lru_cache(maxsize=1)
def get_user_service() -> UserService:
    """Return shared user service."""
    return UserService(get_user_store())


@lru_cache(maxsize=1)
def get_orchestrator() -> OrchestratorService:
    """Return shared orchestrator (engine facades only)."""
    return OrchestratorService()


@lru_cache(maxsize=1)
def get_file_store() -> FileStore:
    """Return WP11 file store rooted at ``settings.data_dir``."""
    return FileStore(Path(get_settings().data_dir))


@lru_cache(maxsize=1)
def get_customer_repository() -> CustomerRepository:
    """JSON customer repository."""
    root = get_file_store()
    return CustomerRepository(root.path("customers.json"))


@lru_cache(maxsize=1)
def get_case_repository() -> CaseRepository:
    """JSON case repository."""
    root = get_file_store()
    return CaseRepository(root.path("cases.json"))


@lru_cache(maxsize=1)
def get_customer_service() -> CustomerService:
    """Customer application service."""
    return CustomerService(get_customer_repository())


@lru_cache(maxsize=1)
def get_case_service() -> CaseService:
    """Case application service wired to orchestrator.analyze."""
    orchestrator = get_orchestrator()
    return CaseService(
        get_case_repository(),
        get_customer_service(),
        analyze_fn=orchestrator.analyze,
        engine_version=get_settings().app_version,
    )


def clear_wp11_caches() -> None:
    """Clear WP11 service caches (tests)."""
    get_case_service.cache_clear()
    get_customer_service.cache_clear()
    get_case_repository.cache_clear()
    get_customer_repository.cache_clear()
    get_file_store.cache_clear()
