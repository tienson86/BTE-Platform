"""Dependency Resolver V2 — dynamic distribution / import / version checks.

Static alias tables are *hints* only. Primary resolution uses
``importlib.metadata`` (distribution + top-level module discovery).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from importlib import import_module
from importlib.metadata import PackageNotFoundError, distribution, version
from typing import Sequence

from runtime.dependency_policy import (
    PolicyRequirement,
    normalize_distribution_name,
    policy_by_name,
)


# Hints when metadata top_level.txt is missing or ambiguous.
# Not the primary resolver — used only as fallback.
IMPORT_ALIAS_HINTS: dict[str, str] = {
    "python-dateutil": "dateutil",
    "pyyaml": "yaml",
    "pillow": "PIL",
    "beautifulsoup4": "bs4",
    "scikit-learn": "sklearn",
    "opencv-python": "cv2",
    "opencv-python-headless": "cv2",
    "attrs": "attr",
}

_REVERSE_HINTS: dict[str, str] = {
    import_name: dist for dist, import_name in IMPORT_ALIAS_HINTS.items()
}


class DependencyStatus(str, Enum):
    """Normalized dependency failure / success classes."""

    OK = "ok"
    NOT_INSTALLED = "not_installed"
    IMPORT_ERROR = "import_error"
    VERSION_CONFLICT = "version_conflict"


@dataclass(slots=True, frozen=True)
class ResolvedNames:
    """Resolved distribution and import module names."""

    distribution: str
    import_name: str
    source: str


@dataclass(slots=True, frozen=True)
class PackageDiagnosis:
    """Full diagnosis for one required package."""

    package: str
    import_name: str
    installed: str | None
    required: str
    status: DependencyStatus
    suggested_command: str
    error: str | None = None
    distribution_found: bool = False
    importable: bool = False
    resolve_source: str = "identity"

    @property
    def ok(self) -> bool:
        """True when package satisfies policy."""
        return self.status is DependencyStatus.OK

    @property
    def pip_name(self) -> str:
        """Backward-compatible alias for package / distribution name."""
        return self.package


@dataclass(slots=True, frozen=True)
class PackageSpec:
    """Compatibility shim — distribution + import pair."""

    distribution: str
    import_name: str

    @property
    def pip_name(self) -> str:
        """Pip-facing distribution name."""
        return self.distribution


@dataclass(slots=True, frozen=True)
class PackageCheckResult:
    """Compatibility shim over ``PackageDiagnosis``."""

    spec: PackageSpec
    importable: bool
    distribution_found: bool
    error: str | None = None
    diagnosis: PackageDiagnosis | None = None

    @property
    def ok(self) -> bool:
        """True when importable and (if checked) version OK."""
        if self.diagnosis is not None:
            return self.diagnosis.ok
        return self.importable


def version_satisfies(installed: str, specifier: str) -> bool:
    """Return True when ``installed`` satisfies PEP 440 ``specifier``."""
    if not specifier or not specifier.strip():
        return True
    try:
        from packaging.specifiers import SpecifierSet
        from packaging.version import Version

        return SpecifierSet(specifier).contains(Version(installed), prereleases=True)
    except Exception:
        # Minimal fallback: only support '>=X' comparisons.
        spec = specifier.strip()
        if spec.startswith(">="):
            return _cmp_tuple(installed) >= _cmp_tuple(spec[2:].strip())
        if spec.startswith("=="):
            return installed == spec[2:].strip()
        return True


def _cmp_tuple(value: str) -> tuple[int, ...]:
    parts: list[int] = []
    for chunk in value.replace(" ", "").split("."):
        digits = "".join(ch for ch in chunk if ch.isdigit())
        if digits:
            parts.append(int(digits))
        else:
            break
    return tuple(parts) or (0,)


def suggested_install_command(requirement: PolicyRequirement) -> str:
    """Build a reproducible suggested pip install command."""
    return f'python -m pip install "{requirement.pip_token}"'


def _top_level_modules(dist_name: str) -> list[str]:
    """Read top-level import names from distribution metadata when present."""
    try:
        dist = distribution(dist_name)
    except PackageNotFoundError:
        return []
    try:
        text = dist.read_text("top_level.txt")
    except Exception:
        text = None
    if not text:
        return []
    modules = []
    for line in text.splitlines():
        name = line.strip()
        if name and name.isidentifier():
            modules.append(name)
    return modules


class DependencyResolver:
    """
    Resolve and validate Runtime dependencies.

    Checks for each requirement:
    1. Distribution presence (``importlib.metadata``)
    2. Importability (``importlib.import_module``)
    3. Version against Version Policy
    """

    def __init__(self, alias_hints: dict[str, str] | None = None) -> None:
        """Create a resolver with optional import alias hints."""
        self.alias_hints = dict(alias_hints or IMPORT_ALIAS_HINTS)
        self._reverse_hints = {
            import_name: dist for dist, import_name in self.alias_hints.items()
        }

    def resolve_names(self, token: str) -> ResolvedNames:
        """
        Resolve a user/policy token to distribution + import names.

        Order:
        1. Alias hint (distribution → import)
        2. Reverse alias (import → distribution)
        3. Metadata top_level.txt when distribution exists
        4. Identity fallback
        """
        raw = token.strip()
        if not raw:
            raise ValueError("package name must not be empty")
        norm = normalize_distribution_name(raw)

        if norm in self.alias_hints:
            return ResolvedNames(norm, self.alias_hints[norm], "alias_hint")

        if raw in self._reverse_hints:
            dist = self._reverse_hints[raw]
            return ResolvedNames(dist, raw, "reverse_alias")

        for dist_name, import_name in self.alias_hints.items():
            if import_name == raw or normalize_distribution_name(import_name) == norm:
                return ResolvedNames(dist_name, import_name, "alias_hint")

        # Prefer metadata when the token is already a distribution.
        top = _top_level_modules(norm)
        if top:
            preferred = top[0]
            if norm.replace("-", "_") in top:
                preferred = norm.replace("-", "_")
            return ResolvedNames(norm, preferred, "metadata_top_level")

        # Token may be an import name of an installed distribution.
        if raw in self._reverse_hints or norm in self.alias_hints:
            pass  # already handled
        else:
            # Probe: if identity distribution exists, use hyphen→underscore import.
            try:
                distribution(norm)
                import_guess = norm.replace("-", "_")
                return ResolvedNames(norm, import_guess, "metadata_identity")
            except PackageNotFoundError:
                pass

        import_name = raw if raw.isidentifier() or "." in raw else norm.replace("-", "_")
        return ResolvedNames(norm, import_name, "identity")

    def get_installed_version(self, distribution_name: str) -> str | None:
        """Return installed distribution version or None."""
        try:
            return version(distribution_name)
        except PackageNotFoundError:
            return None

    def diagnose(self, requirement: PolicyRequirement) -> PackageDiagnosis:
        """Run distribution + import + version checks for one requirement."""
        names = self.resolve_names(
            requirement.import_hint or requirement.distribution
        )
        # If policy distribution differs from resolved (import alias input),
        # prefer the policy distribution name for pip messaging.
        dist_name = requirement.distribution or names.distribution
        if normalize_distribution_name(dist_name) != names.distribution:
            # Re-resolve using canonical distribution from policy.
            names = self.resolve_names(dist_name)

        installed = self.get_installed_version(names.distribution)
        dist_found = installed is not None
        suggested = suggested_install_command(
            PolicyRequirement(
                distribution=names.distribution,
                specifier=requirement.specifier,
                extras=requirement.extras,
            )
        )

        if not dist_found:
            return PackageDiagnosis(
                package=names.distribution,
                import_name=names.import_name,
                installed=None,
                required=requirement.specifier or "(any)",
                status=DependencyStatus.NOT_INSTALLED,
                suggested_command=suggested,
                error=None,
                distribution_found=False,
                importable=False,
                resolve_source=names.source,
            )

        import_error: str | None = None
        importable = False
        try:
            import_module(names.import_name)
            importable = True
        except Exception as exc:  # noqa: BLE001 — classify honestly
            import_error = f"{type(exc).__name__}: {exc}"

        if not importable:
            return PackageDiagnosis(
                package=names.distribution,
                import_name=names.import_name,
                installed=installed,
                required=requirement.specifier or "(any)",
                status=DependencyStatus.IMPORT_ERROR,
                suggested_command=suggested,
                error=import_error,
                distribution_found=True,
                importable=False,
                resolve_source=names.source,
            )

        if requirement.specifier and not version_satisfies(
            installed or "", requirement.specifier
        ):
            return PackageDiagnosis(
                package=names.distribution,
                import_name=names.import_name,
                installed=installed,
                required=requirement.specifier,
                status=DependencyStatus.VERSION_CONFLICT,
                suggested_command=suggested,
                error=(
                    f"installed {installed} does not satisfy "
                    f"{requirement.specifier}"
                ),
                distribution_found=True,
                importable=True,
                resolve_source=names.source,
            )

        return PackageDiagnosis(
            package=names.distribution,
            import_name=names.import_name,
            installed=installed,
            required=requirement.specifier or "(any)",
            status=DependencyStatus.OK,
            suggested_command=suggested,
            error=None,
            distribution_found=True,
            importable=True,
            resolve_source=names.source,
        )

    def diagnose_all(
        self,
        requirements: Sequence[PolicyRequirement] | None = None,
        names: Sequence[str] | None = None,
    ) -> list[PackageDiagnosis]:
        """Diagnose a requirement set (policy default or name override)."""
        reqs = list(requirements) if requirements is not None else policy_by_name(names)
        if names is not None and requirements is None:
            # Map import-style tokens onto policy rows when possible.
            resolved_reqs: list[PolicyRequirement] = []
            by_dist = {r.distribution: r for r in policy_by_name(None)}
            for token in names:
                resolved = self.resolve_names(token)
                if resolved.distribution in by_dist:
                    resolved_reqs.append(by_dist[resolved.distribution])
                else:
                    resolved_reqs.append(
                        PolicyRequirement(
                            distribution=resolved.distribution,
                            specifier="",
                        )
                    )
            reqs = resolved_reqs
        return [self.diagnose(req) for req in reqs]


_DEFAULT_RESOLVER = DependencyResolver()


def resolve_package_spec(name: str) -> PackageSpec:
    """Compatibility: resolve token to PackageSpec via Resolver V2."""
    resolved = _DEFAULT_RESOLVER.resolve_names(name)
    return PackageSpec(
        distribution=resolved.distribution,
        import_name=resolved.import_name,
    )


def is_distribution_installed(name: str) -> bool:
    """Return True if importlib.metadata can find the distribution."""
    try:
        distribution(name)
        return True
    except PackageNotFoundError:
        return False


def check_package(spec: PackageSpec) -> PackageCheckResult:
    """Compatibility wrapper around Resolver V2 diagnosis."""
    req = PolicyRequirement(distribution=spec.distribution, specifier="")
    diagnosis = _DEFAULT_RESOLVER.diagnose(req)
    return PackageCheckResult(
        spec=spec,
        importable=diagnosis.importable,
        distribution_found=diagnosis.distribution_found,
        error=diagnosis.error,
        diagnosis=diagnosis,
    )


def check_required_packages(
    names: Sequence[str] | None = None,
) -> tuple[bool, str, list[PackageCheckResult]]:
    """
    Verify required packages (Resolver V2).

    Returns ``(ok, summary_message, compatibility_results)``.
    """
    diagnoses = _DEFAULT_RESOLVER.diagnose_all(names=names)
    results = [
        PackageCheckResult(
            spec=PackageSpec(d.package, d.import_name),
            importable=d.importable,
            distribution_found=d.distribution_found,
            error=d.error,
            diagnosis=d,
        )
        for d in diagnoses
    ]
    failed = [d for d in diagnoses if not d.ok]
    if not failed:
        return True, f"Required packages OK ({len(results)})", results

    lines = ["Dependency check failed:", ""]
    lines.append(
        f"{'Package':<22} {'Installed':<12} {'Required':<14} Status"
    )
    lines.append("-" * 72)
    for item in failed:
        lines.append(
            f"{item.package:<22} {str(item.installed or '-'):<12} "
            f"{item.required:<14} {item.status.value}"
        )
        lines.append(f"  suggested: {item.suggested_command}")
        if item.error:
            lines.append(f"  detail: {item.error}")
    message = "\n".join(lines)
    return False, message, results
