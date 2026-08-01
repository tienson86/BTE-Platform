"""Analysis Engine compiler build result model."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class BuildArtifact:
    """Public contract for a single compiler output artifact."""

    artifact_id: str
    path: Path
    artifact_type: str
    checksum: str | None = None


@dataclass(slots=True)
class BuildResult:
    """Public contract for a compiler build result."""

    build_id: str
    success: bool
    artifacts: tuple[BuildArtifact, ...] = ()
    messages: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def artifact_ids(self) -> tuple[str, ...]:
        """Return artifact identifiers in the result."""
        raise NotImplementedError

    def artifact_for(self, artifact_id: str) -> BuildArtifact | None:
        """Return an artifact by identifier."""
        raise NotImplementedError
