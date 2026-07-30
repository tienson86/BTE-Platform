"""Smoke test against the real knowledge/registry scaffold."""

from __future__ import annotations

from pathlib import Path

from services.registry_loader import RegistryLoader
from services.registry_statistics import RegistryStatistics
from services.registry_validator import RegistryValidator


def test_real_registry_scaffold_validates(project_root: Path) -> None:
    root = project_root / "knowledge" / "registry"
    loader = RegistryLoader(registry_root=root, project_root=project_root)
    result = RegistryValidator(loader).validate_all(include_samples=True)
    assert result.ok, [issue.message for issue in result.errors]
    stats = RegistryStatistics(loader).compute()
    assert stats.total_records == 0
    assert len(loader.load_all_catalogs()) == 8
