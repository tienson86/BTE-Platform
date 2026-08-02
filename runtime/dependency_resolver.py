"""Dependency Resolver V2 — dynamic distribution / import / version checks.

Static alias tables are *hints* only. Primary resolution uses
``importlib.metadata`` (distribution + top-level module discovery).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from importlib import import_module
from importlib import util as importlib_util
from importlib.metadata import PackageNotFoundError, distribution, version
from pathlib import Path
from typing import Sequence
import sys

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


def suggested_reinstall_command(requirement: PolicyRequirement) -> str:
    """Suggested repair when distribution metadata exists but import fails."""
    name = requirement.distribution
    token = requirement.pip_token
    return (
        f'python -m pip uninstall -y {name} && '
        f'python -m pip install "{token}"'
    )


def find_shadow_candidates(import_name: str) -> list[str]:
    """
    Find ``import_name.py`` / ``import_name/`` entries on ``sys.path``.

    Earlier path entries win and can shadow a healthy site-packages install.
    """
    hits: list[str] = []
    top = import_name.split(".", 1)[0]
    for entry in sys.path:
        base = Path(entry) if entry else Path.cwd()
        try:
            file_hit = base / f"{top}.py"
            dir_hit = base / top
            if file_hit.is_file():
                hits.append(str(file_hit.resolve()))
            if dir_hit.is_dir():
                hits.append(str(dir_hit.resolve()))
        except OSError:
            continue
    # Preserve order, drop duplicates
    seen: set[str] = set()
    ordered: list[str] = []
    for item in hits:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def distribution_init_path(distribution_name: str, import_name: str) -> Path | None:
    """Return expected ``<import>/__init__.py`` path from distribution metadata."""
    try:
        dist = distribution(distribution_name)
    except PackageNotFoundError:
        return None
    top = import_name.split(".", 1)[0]
    try:
        located = Path(str(dist.locate_file(f"{top}/__init__.py")))
    except Exception:
        return None
    return located if located.is_file() else None


def probe_import(
    import_name: str,
    *,
    distribution_name: str | None = None,
) -> dict[str, object]:
    """
    Deep import probe for RCA: find_spec, origin, shadows, dist init path.
    """
    spec = importlib_util.find_spec(import_name)
    shadows = find_shadow_candidates(import_name)
    dist_init = (
        distribution_init_path(distribution_name, import_name)
        if distribution_name
        else None
    )
    origin = spec.origin if spec is not None else None
    shadowed = False
    if origin and dist_init is not None:
        try:
            shadowed = Path(origin).resolve() != dist_init.resolve()
        except OSError:
            shadowed = False
    elif shadows and dist_init is not None:
        try:
            dist_key = str(dist_init.parent.resolve())
            shadowed = any(Path(s).resolve() != Path(dist_key) for s in shadows[:1])
        except OSError:
            shadowed = False

    error: str | None = None
    importable = False
    module_file: str | None = None
    try:
        module = import_module(import_name)
        importable = True
        module_file = getattr(module, "__file__", None)
    except Exception as exc:  # noqa: BLE001
        error = f"{type(exc).__name__}: {exc}"

    dist_importable = None
    dist_error = None
    if not importable and dist_init is not None and dist_init.is_file():
        # Isolate package health from sys.path shadowing.
        try:
            isolated = importlib_util.spec_from_file_location(
                f"_bte_probe_{import_name.replace('.', '_')}",
                dist_init,
            )
            if isolated and isolated.loader:
                mod = importlib_util.module_from_spec(isolated)
                isolated.loader.exec_module(mod)
                dist_importable = True
            else:
                dist_importable = False
                dist_error = "spec_from_file_location failed"
        except Exception as exc:  # noqa: BLE001
            dist_importable = False
            dist_error = f"{type(exc).__name__}: {exc}"

    return {
        "importable": importable,
        "error": error,
        "find_spec": spec is not None,
        "origin": origin,
        "module_file": module_file,
        "shadows": shadows,
        "shadowed": shadowed,
        "distribution_init": str(dist_init) if dist_init else None,
        "distribution_importable": dist_importable,
        "distribution_error": dist_error,
        "sys_path_head": list(sys.path[:8]),
    }


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

        probe = probe_import(
            names.import_name,
            distribution_name=names.distribution,
        )
        importable = bool(probe["importable"])
        reinstall = suggested_reinstall_command(
            PolicyRequirement(
                distribution=names.distribution,
                specifier=requirement.specifier,
                extras=requirement.extras,
            )
        )

        if not importable:
            details: list[str] = []
            if probe.get("error"):
                details.append(str(probe["error"]))
            if probe.get("shadowed") or (
                probe.get("shadows")
                and probe.get("distribution_init")
                and str(probe["shadows"][0])
                != str(Path(str(probe["distribution_init"])).parent)
            ):
                details.append(
                    "possible sys.path shadowing: " + ", ".join(probe["shadows"][:3])  # type: ignore[index]
                )
            if probe.get("origin"):
                details.append(f"find_spec.origin={probe['origin']}")
            if probe.get("distribution_init"):
                details.append(f"dist_init={probe['distribution_init']}")
            if probe.get("distribution_importable") is True:
                details.append(
                    "distribution files import OK in isolation - fix sys.path/shadow"
                )
                suggested = (
                    "Remove shadowing module from sys.path / project root, "
                    f"then retry. sys.path head={probe.get('sys_path_head')}"
                )
            elif probe.get("distribution_importable") is False:
                details.append(
                    f"distribution isolated import failed: {probe.get('distribution_error')}"
                )
                suggested = reinstall
            else:
                suggested = reinstall
            return PackageDiagnosis(
                package=names.distribution,
                import_name=names.import_name,
                installed=installed,
                required=requirement.specifier or "(any)",
                status=DependencyStatus.IMPORT_ERROR,
                suggested_command=suggested,
                error="; ".join(details) if details else "import failed",
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
