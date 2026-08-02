"""Runtime dependency version policy (pip names + version constraints).

Policy is the source of truth for *what* Runtime requires.
Import-name discovery belongs to ``DependencyResolver``, not this module.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]

# Requirement files that define the commercial Runtime baseline.
POLICY_REQUIREMENT_FILES: tuple[Path, ...] = (
    ROOT / "requirements.txt",
    ROOT / "applications" / "requirements.txt",
)

# Packages needed at Runtime startup (engines + API stack).
# Keys are PEP 503 normalized distribution names.
RUNTIME_VERSION_POLICY: dict[str, str] = {
    "fastapi": ">=0.115.0",
    "uvicorn": ">=0.30.0",
    "pydantic": ">=2.0.0",
    "httpx": ">=0.27.0",
    "pandas": ">=2.3.1",
    "numpy": ">=2.3.1",
    "pyyaml": ">=6.0",
    "openpyxl": ">=3.1",
    "python-dateutil": ">=2.9",
}

# Optional extras recorded for suggested install commands.
RUNTIME_EXTRAS: dict[str, tuple[str, ...]] = {
    "uvicorn": ("standard",),
}


_REQ_LINE = re.compile(
    r"""
    ^\s*
    (?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)
    (?:\[(?P<extras>[^\]]+)\])?
    \s*
    (?P<specifier>(?:[=<>!~]=?[^;#\s]+(?:\s*,\s*[=<>!~]=?[^;#\s]+)*)?)?
    """,
    re.VERBOSE,
)


@dataclass(slots=True, frozen=True)
class PolicyRequirement:
    """One versioned distribution requirement from Runtime policy."""

    distribution: str
    specifier: str
    extras: tuple[str, ...] = ()
    import_hint: str | None = None

    @property
    def pip_token(self) -> str:
        """Token suitable for ``pip install`` (name[extras]specifier)."""
        name = self.distribution
        if self.extras:
            name = f"{name}[{','.join(self.extras)}]"
        return f"{name}{self.specifier}" if self.specifier else name


def normalize_distribution_name(name: str) -> str:
    """Normalize a distribution name (lowercase, underscore → hyphen)."""
    return name.strip().lower().replace("_", "-")


def parse_requirement_line(line: str) -> PolicyRequirement | None:
    """Parse one requirements.txt line into a policy requirement."""
    text = line.strip()
    if not text or text.startswith("#") or text.startswith("-"):
        return None
    text = text.split(";", 1)[0].strip()
    match = _REQ_LINE.match(text)
    if not match:
        return None
    name = normalize_distribution_name(match.group("name"))
    extras_raw = match.group("extras") or ""
    extras = tuple(
        part.strip() for part in extras_raw.split(",") if part.strip()
    )
    specifier = (match.group("specifier") or "").strip().replace(" ", "")
    return PolicyRequirement(distribution=name, specifier=specifier, extras=extras)


def load_requirements_file(path: Path) -> list[PolicyRequirement]:
    """Load policy requirements from a requirements file if it exists."""
    if not path.is_file():
        return []
    items: list[PolicyRequirement] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        parsed = parse_requirement_line(line)
        if parsed is not None:
            items.append(parsed)
    return items


def merge_policy(
    *groups: Iterable[PolicyRequirement],
    base: dict[str, str] | None = None,
) -> list[PolicyRequirement]:
    """
    Merge requirement groups.

    Later entries override earlier ones for the same distribution.
    ``base`` supplies default specifiers when a file omits them.
    """
    defaults = {
        normalize_distribution_name(k): v for k, v in (base or RUNTIME_VERSION_POLICY).items()
    }
    merged: dict[str, PolicyRequirement] = {}
    for group in groups:
        for item in group:
            key = normalize_distribution_name(item.distribution)
            specifier = item.specifier or defaults.get(key, "")
            extras = item.extras or RUNTIME_EXTRAS.get(key, ())
            merged[key] = PolicyRequirement(
                distribution=key,
                specifier=specifier,
                extras=extras,
                import_hint=item.import_hint,
            )
    # Ensure every Runtime policy key is present even if absent from files.
    for key, specifier in defaults.items():
        if key not in merged:
            merged[key] = PolicyRequirement(
                distribution=key,
                specifier=specifier,
                extras=RUNTIME_EXTRAS.get(key, ()),
            )
    return [merged[k] for k in sorted(merged)]


def default_policy_requirements() -> list[PolicyRequirement]:
    """Build the default Runtime version policy from files + baseline."""
    file_reqs: list[PolicyRequirement] = []
    for path in POLICY_REQUIREMENT_FILES:
        file_reqs.extend(load_requirements_file(path))
    # Keep only packages declared in RUNTIME_VERSION_POLICY for startup gate.
    allowed = set(RUNTIME_VERSION_POLICY)
    filtered = [r for r in file_reqs if r.distribution in allowed]
    return merge_policy(filtered, base=RUNTIME_VERSION_POLICY)


def policy_by_name(
    names: Sequence[str] | None = None,
) -> list[PolicyRequirement]:
    """Return policy requirements, optionally filtered/extended by name list."""
    full = {r.distribution: r for r in default_policy_requirements()}
    if names is None:
        return [full[k] for k in sorted(full)]
    result: list[PolicyRequirement] = []
    for raw in names:
        key = normalize_distribution_name(raw)
        if key in full:
            result.append(full[key])
            continue
        # Allow import-style aliases to be resolved later; keep placeholder.
        result.append(
            PolicyRequirement(
                distribution=key,
                specifier=RUNTIME_VERSION_POLICY.get(key, ""),
                extras=RUNTIME_EXTRAS.get(key, ()),
            )
        )
    return result
