"""Runtime dependency name resolution and preflight package checks.

Pip / importlib.metadata use *distribution* names (e.g. ``python-dateutil``).
``importlib.import_module`` uses *import* names (e.g. ``dateutil``).
This module maps between the two so preflight never treats an installed
distribution as missing solely because the two names differ.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from importlib.metadata import PackageNotFoundError, distribution
from typing import Iterable, Sequence


# ---------------------------------------------------------------------------
# General mapping: distribution name (PEP 503 normalized) → import module
# Only entries where distribution name ≠ import top-level name belong here.
# ---------------------------------------------------------------------------
DISTRIBUTION_IMPORT_MAP: dict[str, str] = {
    "python-dateutil": "dateutil",
    "pyyaml": "yaml",
    "pillow": "PIL",
    "beautifulsoup4": "bs4",
    "scikit-learn": "sklearn",
    "opencv-python": "cv2",
    "opencv-python-headless": "cv2",
    "attrs": "attr",
}


def normalize_distribution_name(name: str) -> str:
    """Normalize a distribution name (lowercase, underscore → hyphen)."""
    return name.strip().lower().replace("_", "-")


def _import_to_distribution_map() -> dict[str, str]:
    """Reverse map: import module → preferred distribution name."""
    reverse: dict[str, str] = {}
    for dist_name, import_name in DISTRIBUTION_IMPORT_MAP.items():
        reverse.setdefault(import_name, dist_name)
    return reverse


IMPORT_TO_DISTRIBUTION: dict[str, str] = _import_to_distribution_map()


# Canonical required distributions (pip / requirements.txt names).
REQUIRED_DISTRIBUTIONS: tuple[str, ...] = (
    "fastapi",
    "uvicorn",
    "pydantic",
    "httpx",
    "pandas",
    "numpy",
    "pyyaml",
    "openpyxl",
    "python-dateutil",
)


@dataclass(slots=True, frozen=True)
class PackageSpec:
    """One installable package with its import module name."""

    distribution: str
    import_name: str

    @property
    def pip_name(self) -> str:
        """Name to use in pip install / error messages."""
        return self.distribution


@dataclass(slots=True, frozen=True)
class PackageCheckResult:
    """Outcome of checking one package."""

    spec: PackageSpec
    importable: bool
    distribution_found: bool
    error: str | None = None

    @property
    def ok(self) -> bool:
        """True when the import module loads successfully."""
        return self.importable


def resolve_package_spec(name: str) -> PackageSpec:
    """
    Resolve a requirement token to ``(distribution, import_name)``.

    Accepts either a pip distribution name or an import module name.
    Unknown identity packages keep the same token for both roles.
    """
    raw = name.strip()
    if not raw:
        raise ValueError("package name must not be empty")

    norm = normalize_distribution_name(raw)

    if norm in DISTRIBUTION_IMPORT_MAP:
        return PackageSpec(
            distribution=norm,
            import_name=DISTRIBUTION_IMPORT_MAP[norm],
        )

    if raw in IMPORT_TO_DISTRIBUTION:
        dist = IMPORT_TO_DISTRIBUTION[raw]
        return PackageSpec(distribution=dist, import_name=raw)

    for dist_name, import_name in DISTRIBUTION_IMPORT_MAP.items():
        if import_name == raw or normalize_distribution_name(import_name) == norm:
            return PackageSpec(distribution=dist_name, import_name=import_name)

    # Identity: distribution name matches import name (pandas, fastapi, …).
    import_name = raw if raw.isidentifier() or "." in raw else norm
    return PackageSpec(distribution=norm, import_name=import_name)


def is_distribution_installed(name: str) -> bool:
    """Return True if importlib.metadata can find the distribution."""
    try:
        distribution(name)
        return True
    except PackageNotFoundError:
        return False


def check_package(spec: PackageSpec) -> PackageCheckResult:
    """
    Check one package.

    Importability is the pass criterion (runtime needs the module).
    Distribution metadata is recorded for diagnostics and install hints.
    """
    dist_found = is_distribution_installed(spec.distribution)
    try:
        import_module(spec.import_name)
    except Exception as exc:  # noqa: BLE001 — report any import failure honestly
        return PackageCheckResult(
            spec=spec,
            importable=False,
            distribution_found=dist_found,
            error=f"{type(exc).__name__}: {exc}",
        )
    return PackageCheckResult(
        spec=spec,
        importable=True,
        distribution_found=dist_found,
        error=None,
    )


def iter_required_specs(
    names: Sequence[str] | None = None,
) -> list[PackageSpec]:
    """Build package specs for the required set (or an override list)."""
    source: Iterable[str] = names if names is not None else REQUIRED_DISTRIBUTIONS
    return [resolve_package_spec(item) for item in source]


def check_required_packages(
    names: Sequence[str] | None = None,
) -> tuple[bool, str, list[PackageCheckResult]]:
    """
    Verify required packages are importable.

    Returns ``(ok, message, results)``. Missing entries are reported by
    **distribution / pip name** so install hints match requirements.txt.
    """
    results = [check_package(spec) for spec in iter_required_specs(names)]
    failed = [item for item in results if not item.ok]
    if not failed:
        return True, f"Required packages OK ({len(results)})", results

    parts: list[str] = []
    for item in failed:
        pip_name = item.spec.pip_name
        if item.distribution_found:
            detail = item.error or "import failed"
            parts.append(
                f"{pip_name} (distribution present, import "
                f"'{item.spec.import_name}' failed: {detail})"
            )
        else:
            parts.append(pip_name)

    message = (
        "Missing packages: "
        + ", ".join(parts)
        + ". Install with: pip install -r requirements.txt "
        "-r applications/requirements.txt"
    )
    return False, message, results
