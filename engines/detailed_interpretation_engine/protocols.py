"""Pack 07 foundation protocols and type aliases."""

from __future__ import annotations

from typing import Any, Mapping, Protocol, runtime_checkable


@runtime_checkable
class SerializableContract(Protocol):
    """Object that can be rebuilt from a mapping."""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> SerializableContract:
        """Rebuild from a mapping."""
        ...


@runtime_checkable
class AnalysisIdentity(Protocol):
    """Any published Pack 07 object that carries analysis_id."""

    @property
    def analysis_id(self) -> str:
        """Canonical analysis identity."""
        ...


@runtime_checkable
class RuntimeResultFactory(Protocol):
    """Factory that can instantiate an empty published result."""

    def empty_published_result(self, analysis_id: str) -> Any:
        """Return a serializable CanonicalRuntimeResult shell."""
        ...
