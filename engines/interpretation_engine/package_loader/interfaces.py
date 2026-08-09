"""Interfaces for future Interpretation Package loading. No packages yet."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Protocol


@dataclass(frozen=True, slots=True)
class LoadedInterpretationPackage:
    """Immutable snapshot of a future Interpretation Package identity."""

    package_id: str
    package_name: str
    package_type: str
    package_version: str
    schema_version: str
    status: str
    checksum: str | None
    root: Path | None
    published_inputs: tuple[str, ...]
    published_outputs: tuple[str, ...]
    manifest: Mapping[str, Any]


class InterpretationPackageLoaderInterface(Protocol):
    """Read-only loader protocol for released Interpretation Packages."""

    def list_available(self) -> tuple[str, ...]:
        """Return admitted package identifiers."""

    def load(
        self,
        package_id: str,
        *,
        version_constraint: str | None = None,
    ) -> LoadedInterpretationPackage:
        """Admit one released package or fail closed."""
