"""Interpreter registry version manager."""

from __future__ import annotations

from engines.interpretation_engine.exceptions.registry_error import InterpretationRegistryError
from engines.interpretation_engine.registry.metadata import InterpreterRegistryEntry

_STABLE_STATUSES: frozenset[str] = frozenset(
    {
        "active",
        "registered",
        "published",
        "validated",
        "approved",
    }
)
_EXCLUDED_DEFAULT_STATUSES: frozenset[str] = frozenset(
    {
        "archived",
        "removed",
    }
)


class VersionManager:
    """Manage interpreter registry versions without sentence generation.

    Priority: requested version → compatible version → latest stable version.
    """

    def parse_version(self, version: str) -> tuple[int, int, int]:
        """Parse a ``major.minor.patch`` version string."""
        parts = version.strip().split(".")
        if len(parts) < 1 or len(parts) > 3:
            raise InterpretationRegistryError(f"invalid_version:{version}")
        try:
            major = int(parts[0])
            minor = int(parts[1]) if len(parts) > 1 else 0
            patch = int(parts[2]) if len(parts) > 2 else 0
        except ValueError as exc:
            raise InterpretationRegistryError(f"invalid_version:{version}") from exc
        return (major, minor, patch)

    def compare(self, left: str, right: str) -> int:
        """Compare two versions. Return -1, 0, or 1."""
        left_parts = self.parse_version(left)
        right_parts = self.parse_version(right)
        if left_parts < right_parts:
            return -1
        if left_parts > right_parts:
            return 1
        return 0

    def is_compatible(self, candidate: str, requested: str) -> bool:
        """Return True when candidate is backward-compatible with requested."""
        cand = self.parse_version(candidate)
        req = self.parse_version(requested)
        if cand[0] != req[0]:
            return False
        if cand[1] < req[1]:
            return False
        if cand[1] == req[1] and cand[2] < req[2]:
            return False
        return True

    def resolve(
        self,
        entries: tuple[InterpreterRegistryEntry, ...],
        *,
        requested_version: str | None = None,
        allow_compatible: bool = True,
        allow_deprecated: bool = False,
    ) -> InterpreterRegistryEntry:
        """Resolve a single entry from versioned candidates."""
        if not entries:
            raise InterpretationRegistryError("version_resolution_empty_candidates")

        if requested_version is not None:
            exact = tuple(
                entry for entry in entries if entry.version == requested_version
            )
            if exact:
                return self._prefer_stable(exact, allow_deprecated=allow_deprecated)
            if not allow_compatible:
                raise InterpretationRegistryError(f"version_not_found:{requested_version}")
            compatible = tuple(
                entry
                for entry in entries
                if self._is_visible(entry, allow_deprecated=allow_deprecated)
                and self.is_compatible(entry.version, requested_version)
            )
            if not compatible:
                raise InterpretationRegistryError(
                    f"compatible_version_not_found:{requested_version}"
                )
            return self._latest(compatible)

        visible = tuple(
            entry
            for entry in entries
            if self._is_visible(entry, allow_deprecated=allow_deprecated)
        )
        if not visible:
            raise InterpretationRegistryError("stable_version_not_found")
        return self._latest(visible)

    def _is_visible(
        self,
        entry: InterpreterRegistryEntry,
        *,
        allow_deprecated: bool,
    ) -> bool:
        """Apply default visibility rules for unresolved requests."""
        status = entry.status.lower()
        if status in _EXCLUDED_DEFAULT_STATUSES:
            return False
        if status == "deprecated":
            return allow_deprecated
        return True

    def _prefer_stable(
        self,
        entries: tuple[InterpreterRegistryEntry, ...],
        *,
        allow_deprecated: bool,
    ) -> InterpreterRegistryEntry:
        """Prefer a stable-status entry when multiple exact matches exist."""
        stable = tuple(
            entry for entry in entries if entry.status.lower() in _STABLE_STATUSES
        )
        if stable:
            return stable[0]
        visible = tuple(
            entry
            for entry in entries
            if self._is_visible(entry, allow_deprecated=allow_deprecated)
        )
        if visible:
            return visible[0]
        raise InterpretationRegistryError("version_match_not_visible")

    def _latest(
        self,
        entries: tuple[InterpreterRegistryEntry, ...],
    ) -> InterpreterRegistryEntry:
        """Return the highest version entry; ties break by entry_id."""
        return max(
            entries,
            key=lambda entry: (self.parse_version(entry.version), entry.entry_id),
        )
