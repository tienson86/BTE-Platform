"""JSON file license repository (local to license package)."""

from __future__ import annotations

from pathlib import Path

from applications.license.models import LicenseModel
from applications.storage.json_store import JsonStore


class LicenseRepository:
    """
    Persist licenses as JSON keyed by ``license_key``.

    Uses JsonStore helper only — does not modify the persistence layer package.
    """

    def __init__(self, path: Path | str) -> None:
        self._store = JsonStore(path)

    def _load(self) -> dict[str, dict]:
        raw = self._store.load_dict()
        return {
            str(key): value
            for key, value in raw.items()
            if isinstance(value, dict)
        }

    def _save(self, data: dict[str, dict]) -> None:
        self._store.save(data)

    def save(self, license_obj: LicenseModel) -> LicenseModel:
        """Insert or replace a license."""
        data = self._load()
        data[license_obj.license_key] = license_obj.to_dict()
        self._save(data)
        return license_obj

    def get(self, license_key: str) -> LicenseModel | None:
        """Fetch by license key."""
        row = self._load().get(license_key)
        return LicenseModel.from_dict(row) if row else None

    def list(self) -> list[LicenseModel]:
        """List all licenses."""
        return [LicenseModel.from_dict(row) for row in self._load().values()]

    def delete(self, license_key: str) -> bool:
        """Delete a license key."""
        data = self._load()
        if license_key not in data:
            return False
        del data[license_key]
        self._save(data)
        return True

    def get_active(self) -> LicenseModel | None:
        """Return the currently active license if any."""
        actives = [lic for lic in self.list() if lic.status == "active"]
        if not actives:
            return None
        actives.sort(key=lambda item: item.activated_at or item.issued_at, reverse=True)
        return actives[0]
