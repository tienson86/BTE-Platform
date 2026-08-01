"""Shared version type aliases and literals."""

from __future__ import annotations

from typing import Literal, TypedDict, TypeAlias

VersionString: TypeAlias = str
SchemaVersion: TypeAlias = str
EngineVersion: TypeAlias = str
ModuleVersion: TypeAlias = str

VersionKind = Literal["major", "minor", "patch", "prerelease"]

CompatibilityMode = Literal["strict", "backward", "forward", "any"]


class VersionParts(TypedDict):
    """Structured semantic version parts."""

    major: int
    minor: int
    patch: int
    prerelease: str | None
    build: str | None


class VersionRef(TypedDict):
    """Version reference payload."""

    version: VersionString
    schema_version: SchemaVersion
    kind: VersionKind
