"""Registry loader contract interface.

Compatible with Pack 01 Registry read-only loading semantics.
No implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from engines.analysis_engine.registry.registry_models import RegistrySnapshot


class RegistryLoaderContract(ABC):
    """Public loader contract aligned with Pack 01 Registry serve/load boundaries.

    Loaders may read Pack 01 registry artifacts and snapshots.
    Loaders must not write, update, or delete Pack 01 knowledge.
    """

    @abstractmethod
    def load_snapshot(self, path: Path) -> RegistrySnapshot:
        """Load a Pack-compatible registry snapshot from a filesystem path."""

    @abstractmethod
    def load_pack_registry(self, pack_id: str) -> RegistrySnapshot:
        """Load a registry snapshot for a pack identifier such as PACK_01."""

    @abstractmethod
    def list_entry_ids(self, path: Path) -> tuple[str, ...]:
        """List entry identifiers available at a Pack-compatible registry path."""

    @abstractmethod
    def supports_pack(self, pack_id: str) -> bool:
        """Indicate whether this loader supports the given pack identifier."""
