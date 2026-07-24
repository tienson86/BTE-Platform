"""Safe configuration exposure for admins."""

from __future__ import annotations

from typing import Any

from applications.storage.factory import StorageConfig


class ConfigurationService:
    """Expose non-secret runtime configuration."""

    def build(self) -> dict[str, Any]:
        """Return configuration snapshot without secrets."""
        from applications.api.config import settings

        storage = StorageConfig.from_env()
        return {
            "app_name": settings.app_name,
            "api_version": settings.app_version,
            "api_prefix": settings.api_prefix,
            "default_timezone": settings.default_timezone,
            "log_level": settings.log_level,
            "jwt_issuer": settings.jwt_issuer,
            "jwt_audience": settings.jwt_audience,
            "access_token_expire_minutes": settings.access_token_expire_minutes,
            "refresh_token_expire_days": settings.refresh_token_expire_days,
            "storage_backend": storage.backend,
            "data_dir": storage.data_dir,
            "sqlite_path": storage.sqlite_path,
            # Never expose jwt_secret / passwords
        }
