"""Runtime dependency facade (V2).

Public compatibility surface for ``runtime.manager`` and existing tests.
Implementation lives in ``dependency_policy`` + ``dependency_resolver``.
"""

from __future__ import annotations

from typing import Sequence

from runtime.dependency_policy import (  # noqa: F401
    RUNTIME_VERSION_POLICY,
    PolicyRequirement,
    default_policy_requirements,
    normalize_distribution_name,
    policy_by_name,
)
from runtime.dependency_resolver import (  # noqa: F401
    IMPORT_ALIAS_HINTS,
    DependencyResolver,
    DependencyStatus,
    PackageCheckResult,
    PackageDiagnosis,
    PackageSpec,
    check_package,
    check_required_packages,
    is_distribution_installed,
    resolve_package_spec,
    version_satisfies,
)

# Backward-compatible names used by V1 callers / tests.
DISTRIBUTION_IMPORT_MAP = IMPORT_ALIAS_HINTS
IMPORT_TO_DISTRIBUTION = {
    import_name: dist for dist, import_name in IMPORT_ALIAS_HINTS.items()
}

REQUIRED_DISTRIBUTIONS: tuple[str, ...] = tuple(
    sorted(RUNTIME_VERSION_POLICY.keys())
)


def iter_required_specs(names: Sequence[str] | None = None) -> list[PackageSpec]:
    """Build package specs for the required set (or an override list)."""
    resolver = DependencyResolver()
    if names is None:
        names = REQUIRED_DISTRIBUTIONS
    return [resolve_package_spec(item) for item in names]
